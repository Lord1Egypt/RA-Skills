#!/usr/bin/env python3
"""
Interact — click elements and fill forms.
Usage: interact.py <action> <selector> [value] [url]
  action   — click | fill | hover | check | uncheck
  selector — CSS selector for target element
  value    — for 'fill' only: text to type
  url      — optional: navigate here first

Exit codes: 0=success, 1=usage, 2=element not found, 3=browser error
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

def interact(action, selector, value=None, url=None):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=ARGS)
            page = browser.new_page()
            if url:
                page.goto(url, wait_until='networkidle', timeout=20000)
            # Wait for element
            try:
                el = page.wait_for_selector(selector, timeout=5000)
                el.scroll_into_view_if_needed()
            except Exception:
                browser.close()
                return {"success": False, "error": f"Element not found: {selector}"}

            if action == "click":
                el.click()
                page.wait_for_timeout(500)
                result = {"success": True, "action": "click", "selector": selector,
                          "title": page.title(), "url": page.url}
            elif action == "fill":
                el.fill(value or "")
                result = {"success": True, "action": "fill", "selector": selector,
                          "value": value}
            elif action == "hover":
                el.hover()
                result = {"success": True, "action": "hover", "selector": selector}
            elif action == "check":
                el.check()
                result = {"success": True, "action": "check", "selector": selector}
            elif action == "uncheck":
                el.uncheck()
                result = {"success": True, "action": "uncheck", "selector": selector}
            else:
                result = {"success": False, "error": f"Unknown action: {action}"}
            browser.close()
            return result
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: interact.py <click|fill|hover|check|uncheck> <selector> [value] [url]"}))
        sys.exit(1)
    action = sys.argv[1]
    selector = sys.argv[2]
    value = sys.argv[3] if len(sys.argv) > 3 and action == "fill" else None
    url = sys.argv[-1] if len(sys.argv) > 3 and action != "fill" else (sys.argv[4] if len(sys.argv) > 4 else None)
    result = interact(action, selector, value, url)
    print(json.dumps(result, indent=2))
    codes = {"click": 0, "fill": 0, "hover": 0, "check": 0, "uncheck": 0}
    sys.exit(0 if result["success"] else (2 if "not found" in result.get("error", "") else 3))
