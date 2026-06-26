#!/usr/bin/env python3
"""
Scrape — get rendered HTML content from a page.
Usage: scrape.py <url>
  url — page to scrape (required)

Returns JSON with 'title' and 'html' (truncated to 50k chars).
Exit codes: 0=success, 1=usage, 2=browser error
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

def scrape(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=ARGS)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=20000)
            title = page.title()
            html = page.content()
            browser.close()
        return {
            "success": True,
            "title": title,
            "url": page.url,
            "html": html[:50000]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: scrape.py <url>"}))
        sys.exit(1)
    result = scrape(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 2)
