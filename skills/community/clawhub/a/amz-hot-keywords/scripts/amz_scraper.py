import argparse
import os
import sys
import time
import datetime
import random
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# -------------------- Configuration --------------------
SELECTORS = {
    "search_input": "input[name='keyword']",
    "search_button": "button[type='submit']",
    "row": "table tbody tr",
    "cols": {
        "search_term": "td:nth-child(1)",
        "current_rank": "td:nth-child(2)",
        "last_rank": "td:nth-child(3)"
    }
}
BASE_URL = "https://www.amz123.com/usatopkeywords"
MAX_RESULTS_LIMIT = 200
# -------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Scrape Amazon ABA hot keywords from AMZ123.")
    parser.add_argument("--keyword", required=True, help="Base keyword to search for")
    parser.add_argument("--max-results", type=int, default=MAX_RESULTS_LIMIT,
                        help=f"Maximum number of keywords to collect (max {MAX_RESULTS_LIMIT})")
    parser.add_argument("--output-dir", default=".", help="Directory to write the output file")
    parser.add_argument("--format", choices=["csv", "json"], default="csv",
                        help="Output format (csv or json)")
    parser.add_argument("--headless", type=str, default="true",
                        help="Run Chrome headlessly (true/false)")
    return parser.parse_args()

def init_driver(headless: bool):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # Randomize user-agent to reduce bot detection
    ua = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    options.add_argument(f"--user-agent={ua}")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    return driver

def scrape(driver, keyword, max_results):
    driver.get(BASE_URL)
    # Input keyword
    try:
        search_input = driver.find_element(By.CSS_SELECTOR, SELECTORS["search_input"])
        search_input.clear()
        search_input.send_keys(keyword)
        # Submit search
        search_button = driver.find_element(By.CSS_SELECTOR, SELECTORS["search_button"])
        search_button.click()
    except NoSuchElementException as e:
        print(f"[ERROR] Search elements not found: {e}")
        driver.quit()
        sys.exit(1)

    # Wait a bit for results to load
    time.sleep(random.uniform(2, 4))

    rows = driver.find_elements(By.CSS_SELECTOR, SELECTORS["row"])
    data = []
    for i, row in enumerate(rows):
        if i >= max_results:
            break
        try:
            term = row.find_element(By.CSS_SELECTOR, SELECTORS["cols"]["search_term"]).text.strip()
            cur = row.find_element(By.CSS_SELECTOR, SELECTORS["cols"]["current_rank"]).text.strip()
            last = row.find_element(By.CSS_SELECTOR, SELECTORS["cols"]["last_rank"]).text.strip()
            cur_rank = int(cur) if cur.isdigit() else None
            last_rank = int(last) if last.isdigit() else None
            # Determine trend
            if last_rank is None:
                trend = "new"
            elif cur_rank < last_rank:
                trend = "up"
            elif cur_rank > last_rank:
                trend = "down"
            else:
                trend = "flat"
            data.append({
                "search_term": term,
                "current_rank": cur_rank,
                "last_rank": last_rank,
                "trend": trend,
            })
        except Exception as e:
            # Skip malformed rows
            print(f"[WARN] Skipping row due to error: {e}")
            continue
    return data

def write_output(data, output_dir, keyword, fmt):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_keyword = "_".join(keyword.strip().split())
    filename = f"amz123_hotwords_{safe_keyword}_{timestamp}.{fmt}"
    out_path = Path(output_dir) / filename
    df = pd.DataFrame(data)
    df = df.sort_values("current_rank")
    if fmt == "csv":
        df.to_csv(out_path, index=False)
    else:
        df.to_json(out_path, orient="records", force_ascii=False)
    print(out_path.resolve())

def main():
    args = parse_args()
    headless = args.headless.lower() != "false"
    max_results = min(args.max_results, MAX_RESULTS_LIMIT)
    driver = init_driver(headless)
    try:
        data = scrape(driver, args.keyword, max_results)
    finally:
        driver.quit()
    if not data:
        print("[ERROR] No data scraped. Exiting.")
        sys.exit(1)
    write_output(data, args.output_dir, args.keyword, args.format)

if __name__ == "__main__":
    main()
