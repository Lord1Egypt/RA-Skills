#!/usr/bin/env python3
"""
Screenshot — capture a page screenshot.
Usage: screenshot.py <url> [path]
  url  — page to screenshot (required)
  path — output path, default /tmp/screenshot.png

Exit codes:
  0 — success
  1 — missing url
  2 — browser error
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

def screenshot(url, path="/tmp/screenshot.png"):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=ARGS)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=20000)
            page.screenshot(path=path, full_page=False)
            title = page.title()
            browser.close()
        return {"success": True, "saved": path, "title": title}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: screenshot.py <url> [path]"}))
        sys.exit(1)
    url = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/screenshot.png"
    result = screenshot(url, path)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 2)
