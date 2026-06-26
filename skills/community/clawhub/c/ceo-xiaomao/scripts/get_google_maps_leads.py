"""
Google Maps lead scraper
Usage: python3 get_google_maps_leads.py "keyword" "region" 50
"""

import csv
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--lang=en-US')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=options)


def search_google_maps(driver, keyword, location, max_results=50):
    search_url = f"https://www.google.com/maps/search/{keyword}+{location}"
    print(f"Searching: {search_url}")
    driver.get(search_url)
    time.sleep(random.uniform(3, 5))
    results = []
    scroll_count = 0
    while len(results) < max_results and scroll_count <= 20:
        driver.execute_script("document.querySelector('div[role=\"feed\"]').scrollBy(0, 2000)")
        time.sleep(random.uniform(2, 3))
        scroll_count += 1
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
            for card in cards:
                if len(results) >= max_results:
                    break
                try:
                    name_elem = card.find_element(By.CSS_SELECTOR, 'div[data-item-title]')
                    name = name_elem.get_attribute('data-item-title') if name_elem else ''
                    try:
                        card.click()
                        time.sleep(random.uniform(2, 3))
                    except Exception:
                        pass
                    info = {'name': name, 'phone': '', 'address': '', 'website': '', 'email': ''}
                    try:
                        phone = driver.find_element(By.CSS_SELECTOR, 'button[data-item-phone]')
                        info['phone'] = phone.get_attribute('data-item-phone') if phone else ''
                    except Exception:
                        pass
                    try:
                        address = driver.find_element(By.CSS_SELECTOR, 'div[data-item-address]')
                        info['address'] = address.get_attribute('data-item-address') if address else ''
                    except Exception:
                        pass
                    try:
                        website = driver.find_element(By.CSS_SELECTOR, 'a[data-item-website]')
                        info['website'] = website.get_attribute('data-item-website') if website else ''
                    except Exception:
                        pass
                    if name and name not in [r['name'] for r in results]:
                        results.append(info)
                        print(f"Found: {name}")
                except Exception:
                    continue
        except Exception as e:
            print(f"Card fetch error: {e}")
    return results


def save_to_csv(results, filename='leads.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'phone', 'address', 'website', 'email'])
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} rows to {filename}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    keyword = sys.argv[1]
    location = sys.argv[2]
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    driver = setup_driver()
    try:
        results = search_google_maps(driver, keyword, location, max_results)
        save_to_csv(results, f"leads_{keyword.replace(' ', '_')}_{location}.csv")
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
