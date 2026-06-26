#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def render_html(html_path, output_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200,1800')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f'file://{html_path}')

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Give fonts a moment to load
        time.sleep(1)

        # Get the body element and screenshot
        body = driver.find_element(By.TAG_NAME, 'body')
        body.screenshot(output_path)

        print(f'✓ Rendered: {output_path}')
    finally:
        driver.quit()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 render-html.py <input.html> <output.png>')
        sys.exit(1)

    render_html(sys.argv[1], sys.argv[2])
