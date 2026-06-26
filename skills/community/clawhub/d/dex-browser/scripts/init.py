#!/usr/bin/env python3
"""
Init — check Playwright is installed and browsers are available.
Run this before using any other script to verify the environment.
Exit code 0 = ready, 1 = not ready, 2 = install needed.
"""

import sys
import json
import subprocess

def check():
    # Check playwright Python package
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "ready": False,
            "playwright_installed": False,
            "error": "Playwright not installed. Run: pip install playwright"
        }

    # Check browsers
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'
            ])
            page = browser.new_page()
            page.goto("about:blank")
            browser.close()
        return {"ready": True, "playwright_installed": True}
    except Exception as e:
        return {"ready": False, "playwright_installed": True, "error": str(e)}

if __name__ == "__main__":
    result = check()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ready"] else (1 if result.get("error", "").startswith("Playwright") else 2))
