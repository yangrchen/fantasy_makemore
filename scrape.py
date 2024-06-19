from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


def click_and_extract(
    driver: WebDriver, button_selector: str, div_selector: str, duration=60
):
    """Repeatedly clicks and extracts text from the fantasy name generator for a specified duration.

    Website used can be found at: https://www.fantasynamegenerators.com/dnd-drow-names.php.
    """
    names = ""  # Maintain a list of names to save
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            # Waits for a max of 10 sec. until the button element being looked for is found
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, button_selector))
            )
            button.click()
            div = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, div_selector))
            )
            names += div.text.lower() + "\n"  # Added newline char to end of string to separate each section
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return names


if __name__ == "__main__":
    chrome_options = Options()
    service = Service(os.getenv("CHROMEDRIVER_PATH"))  # Use the chrome driver on system

    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://www.fantasynamegenerators.com/dnd-drow-names.php"
    driver.get(url)

    button_selector = (
        '#nameGen > input[type="button"]'  # Specific button selector for the website
    )
    div_selector = "#result"  # Specific div selector for the generated results

    names = click_and_extract(driver, button_selector, div_selector, duration=120)

    # Write names to a text file
    with open("names.txt", "w") as f:
        f.write(names)

    # Close driver connection
    driver.quit()
