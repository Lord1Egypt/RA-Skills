#!/usr/bin/env python3
"""
Extract — pull structured data from page elements.
Usage: extract.py <url> <selector>
  url      — page to scrape
  selector — CSS selector for elements to extract

Extracts up to 50 elements. For each, captures:
  text  — innerText (500 char max)
  href  — link href (if link element)
  src   — img src (if img element)
  alt   — img alt text

Exit codes: 0=success, 1=usage, 2=browser/error
"""

import sys
import json
from playwright.sync_api import sync_playwright

ARGS = [
    '--disable-gpu',
    '--remote-allow-origins=*',
    '--no-sandbox',
    '--disable-dev-shm-usage',
]

def extract(url, selector):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=ARGS)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=20000)
            els = page.query_selector_all(selector)
            results = []
            for el in els[:50]:
                item = {"text": el.inner_text()[:500].strip()}
                href = el.get_attribute("href")
                if href:
                    item["href"] = href
                src = el.get_attribute("src")
                if src:
                    item["src"] = src
                alt = el.get_attribute("alt")
                if alt:
                    item["alt"] = alt
                results.append(item)
            browser.close()
        return {"success": True, "count": len(results), "selector": selector, "items": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: extract.py <url> <selector>"}))
        sys.exit(1)
    result = extract(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 2)
