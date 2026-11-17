#!/usr/bin/env python3
"""
CloakBrowser Stealth Fetch — Unified wrapper for protected site scraping.

Usage:
  python3 fetch.py <url> [options]

Options:
  --wait-until {domcontentloaded|networkidle}  Load strategy (default: networkidle)
  --wait-ms N                                     Extra wait after load (default: 2000)
  --selector CSS_SELECTOR                         Extract specific element text
  --screenshot PATH                               Save full-page screenshot
  --humanize                                      Enable human-like mouse/keyboard/scroll
  --proxy PROXY_URL                               e.g. http://user:pass@host:port
  --output {text|html|json}                       Output format (default: text)
  --max-chars N                                   Truncate text output (default: 5000)

Exit codes:
  0  Success
  1  Anti-bot blocked
  2  Timeout / navigation error
  3  Invalid arguments
"""

import sys
import json
import argparse
from pathlib import Path

# Activate the CloakBrowser venv
def _activate_venv():
    venv = Path.home() / ".venv" / "cloakbrowser"
    site_packages = list((venv / "lib").glob("python*/site-packages"))
    if site_packages:
        sys.path.insert(0, str(site_packages[0]))

_activate_venv()

try:
    from cloakbrowser import launch
except ImportError as e:
    print(json.dumps({"error": f"CloakBrowser not installed: {e}"}), file=sys.stderr)
    sys.exit(3)


def main():
    parser = argparse.ArgumentParser(description="Stealth browser fetch via CloakBrowser")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--wait-until", default="networkidle", choices=["domcontentloaded", "networkidle"])
    parser.add_argument("--wait-ms", type=int, default=2000)
    parser.add_argument("--selector", default="", help="CSS selector for specific element")
    parser.add_argument("--screenshot", default="", help="Path to save screenshot")
    parser.add_argument("--humanize", action="store_true", help="Enable human-like behavior")
    parser.add_argument("--proxy", default="", help="Proxy URL")
    parser.add_argument("--output", default="text", choices=["text", "html", "json"])
    parser.add_argument("--max-chars", type=int, default=5000)
    args = parser.parse_args()

    launch_kwargs = {"headless": True}
    if args.humanize:
        launch_kwargs["humanize"] = True
    if args.proxy:
        launch_kwargs["proxy"] = args.proxy

    try:
        browser = launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(args.url, wait_until=args.wait_until, timeout=45000)

        if args.wait_ms > 0:
            import time
            time.sleep(args.wait_ms / 1000)

        result = {"url": args.url, "title": page.title(), "blocked": False}

        # Anti-bot detection
        body_text = page.inner_text("body").lower()[:500]
        bot_indicators = ["blocked by network security", "you've been blocked", "captcha", "robot", "please verify", "access denied"]
        if any(ind in body_text for ind in bot_indicators):
            result["blocked"] = True
            result["indicator"] = next(ind for ind in bot_indicators if ind in body_text)

        # Content extraction
        if args.selector:
            elements = page.query_selector_all(args.selector)
            result["elements_found"] = len(elements)
            result["text"] = "\n---\n".join(e.inner_text()[:args.max_chars] for e in elements[:20])
        else:
            result["text"] = page.inner_text("body")[:args.max_chars]
            result["html"] = page.content()[:args.max_chars * 2]

        # Screenshot
        if args.screenshot:
            page.screenshot(path=args.screenshot, full_page=True)
            result["screenshot"] = args.screenshot

        browser.close()

        if args.output == "json":
            print(json.dumps(result, indent=2))
        elif args.output == "html":
            print(result.get("html", ""))
        else:
            print(f"Title: {result['title']}")
            print(f"Blocked: {result['blocked']}")
            if result.get("elements_found") is not None:
                print(f"Elements: {result['elements_found']}")
            print("---")
            print(result["text"])

        sys.exit(1 if result["blocked"] else 0)

    except Exception as e:
        error = {"error": str(e), "url": args.url}
        if args.output == "json":
            print(json.dumps(error))
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
