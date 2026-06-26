#!/usr/bin/env python3
"""Screenshot Capture — take product page screenshots via Playwright."""

import json, os, sys, time
from urllib.parse import urlparse

SCREENSHOT_DIR = os.environ.get("PIPELINE_SCREENSHOT_DIR", "screenshots")
DATA_DIR = os.environ.get("PIPELINE_DATA_DIR", "data")


def capture(url: str, out_path: str) -> str | None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("    ⚠ playwright not installed, skipping screenshots", file=sys.stderr)
        return None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        try:
            page.goto(url, timeout=20000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            page.screenshot(path=out_path, full_page=True)
            print(f"    ✓ {out_path}")
            return out_path
        except Exception as e:
            print(f"    ✗ {url}: {e}", file=sys.stderr)
            return None
        finally:
            browser.close()


def run(launches: list) -> list:
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    results = []
    for i, item in enumerate(launches):
        url = item.get("link", "")
        if not url or not url.startswith("http"):
            continue
        print(f"  [{i+1}/{len(launches)}] Capturing: {url[:70]}")
        parsed = urlparse(url)
        fname = f"{parsed.netloc.replace('.','_')}_{int(time.time())}.png"
        out_path = os.path.join(SCREENSHOT_DIR, fname)
        path = capture(url, out_path)
        item["screenshot_path"] = path
        results.append(item)
        time.sleep(1)

    out_path = os.path.join(DATA_DIR, "screenshot_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"  Captured {sum(1 for r in results if r.get('screenshot_path'))} screenshots")
    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=os.path.join(DATA_DIR, "enriched_launches.json"))
    args = p.parse_args()
    with open(args.input) as f:
        launches = json.load(f)
    run(launches)
