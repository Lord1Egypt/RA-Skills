#!/usr/bin/env python3
"""
Browser automation via Playwright — the "interact" layer.
Used after search and extract when JS-rendering or user interaction is required.

Usage:
  browser.py navigate <url>              # Navigate and print title
  browser.py screenshot [path] [url]   # Screenshot (default: /tmp/screenshot.png)
  browser.py content <url>             # Get full HTML
  browser.py text <url> <selector>     # Get element text
  browser.py click <selector>          # Click element on current page
  browser.py fill <selector> <value>   # Fill input on current page
  browser.py eval <js>                # Run JS on current page
  browser.py extract <url> <selector>  # Extract structured data from page
"""

import sys
import json
import time
from playwright.sync_api import sync_playwright

BROWSER_ARGS = [
    '--disable-gpu',
    '--remote-allow-origins=*',
    '--no-sandbox',
    '--disable-dev-shm-usage',
]

def get_browser(p):
    return p.chromium.launch(headless=True, args=BROWSER_ARGS)

def cmd_navigate(url):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=15000)
        title = page.title()
        url_out = page.url
        browser.close()
    return {"title": title, "url": url_out}

def cmd_screenshot(path, url=None):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        if url:
            page.goto(url, wait_until='networkidle', timeout=15000)
        page.wait_for_timeout(1000)
        page.screenshot(path=path, full_page=False)
        title = page.title()
        browser.close()
    return {"saved": path, "title": title}

def cmd_content(url):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=15000)
        html = page.content()
        browser.close()
    return {"html": html[:10000]}

def cmd_text(url, selector):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=15000)
        try:
            el = page.wait_for_selector(selector, timeout=5000)
            text = el.inner_text()
        except:
            text = f"NOT FOUND: {selector}"
        browser.close()
    return {"text": text[:5000]}

def cmd_extract(url, selector):
    """Extract all matching elements as structured data."""
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=15000)
        try:
            els = page.query_selector_all(selector)
            results = []
            for el in els[:20]:  # cap at 20
                results.append({
                    "text": el.inner_text()[:500],
                    "href": el.get_attribute('href') or '',
                    "src": el.get_attribute('src') or '',
                })
        except Exception as e:
            results = [{"error": str(e)}]
        browser.close()
    return {"count": len(results), "items": results}

def cmd_click(selector, url=None):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        if url:
            page.goto(url, wait_until='networkidle', timeout=15000)
        try:
            el = page.wait_for_selector(selector, timeout=5000)
            el.scroll_into_view_if_needed()
            el.click()
            page.wait_for_timeout(1000)
            result = {"clicked": selector, "title": page.title(), "url": page.url}
        except Exception as e:
            result = {"error": str(e)}
        browser.close()
    return result

def cmd_fill(selector, value, url=None):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        if url:
            page.goto(url, wait_until='networkidle', timeout=15000)
        try:
            el = page.wait_for_selector(selector, timeout=5000)
            el.fill(value)
            page.wait_for_timeout(500)
            result = {"filled": selector, "value": value}
        except Exception as e:
            result = {"error": str(e)}
        browser.close()
    return result

def cmd_eval(js):
    with sync_playwright() as p:
        browser = get_browser(p)
        page = browser.new_page()
        result = page.evaluate(js)
        browser.close()
    return {"result": result}

def main():
    if len(sys.argv) < 2:
        print("Usage: cdp.py <command> [args...]")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == "navigate":
            url = args[0] if args else "about:blank"
            result = cmd_navigate(url)

        elif cmd == "screenshot":
            path = args[0] if len(args) > 0 else "/tmp/screenshot.png"
            url = args[1] if len(args) > 1 else None
            result = cmd_screenshot(path, url)

        elif cmd == "content":
            url = args[0] if args else "about:blank"
            result = cmd_content(url)

        elif cmd == "text":
            url, selector = args[0], args[1]
            result = cmd_text(url, selector)

        elif cmd == "extract":
            url, selector = args[0], args[1]
            result = cmd_extract(url, selector)

        elif cmd == "click":
            selector = args[0]
            url = args[1] if len(args) > 1 else None
            result = cmd_click(selector, url)

        elif cmd == "fill":
            selector, value = args[0], args[1]
            url = args[2] if len(args) > 2 else None
            result = cmd_fill(selector, value, url)

        elif cmd == "eval":
            js = args[0]
            result = cmd_eval(js)

        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
