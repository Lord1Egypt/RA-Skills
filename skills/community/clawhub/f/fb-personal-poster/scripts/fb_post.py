#!/usr/bin/env python3
"""
Facebook Personal Timeline Poster
Post text + photos to personal Facebook timeline via Patchright (stealth Chromium).
"""

import asyncio
import json
import os
import sys
import random
import time
from pathlib import Path

try:
    from patchright.async_api import async_playwright
except ImportError:
    print("[ERROR] patchright not installed. Run: pip install patchright && python -m patchright install chromium")
    sys.exit(1)


# --- Config ---
COOKIE_FILE = os.environ.get("FB_COOKIE_FILE", "")
STATE_FILE = os.environ.get("FB_STATE_FILE", "/tmp/fb_state.json")
DRY_RUN = os.environ.get("FB_DRY_RUN", "true").lower() == "true"
USER_AGENT = os.environ.get("FB_USER_AGENT", "")


def human_delay(min_s=1, max_s=3):
    """Random human-like delay."""
    time.sleep(random.uniform(min_s, max_s))


async def human_type(page, text, selector=None):
    """Type text with human-like speed and occasional pauses."""
    if selector:
        await page.click(selector)
        await asyncio.sleep(0.5)

    for char in text:
        await page.keyboard.type(char, delay=random.uniform(30, 120))
        if random.random() < 0.05:  # 5% chance of a pause
            await asyncio.sleep(random.uniform(0.3, 0.8))


async def create_session():
    """Create a browser session with cookies."""
    pw = await async_playwright().start()

    launch_args = {
        "headless": False,
        "channel": "chromium",
    }

    browser = await pw.chromium.launch(**launch_args)

    context_args = {}
    if USER_AGENT:
        context_args["user_agent"] = USER_AGENT

    # Load cookies if available
    if COOKIE_FILE and os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE) as f:
            cookies = json.load(f)
        context_args["storage_state"] = {"cookies": cookies}
    elif os.path.exists(STATE_FILE):
        context_args["storage_state"] = STATE_FILE

    context = await browser.new_context(**context_args)
    page = await context.new_page()

    return pw, browser, context, page


async def navigate_to_facebook(page):
    """Navigate to Facebook home page."""
    await page.goto("https://www.facebook.com/", wait_until="networkidle", timeout=30000)
    await asyncio.sleep(random.uniform(2, 4))

    # Check if logged in
    if "login" in page.url:
        print("[ERROR] Not logged in. Please provide valid cookies via FB_COOKIE_FILE")
        return False
    return True


async def post_text(page, message: str) -> dict:
    """Post text-only to personal timeline."""
    print(f"[INFO] Posting text ({len(message)} chars)...")

    # Click on "What's on your mind" box
    try:
        # Try multiple selectors for the post box
        selectors = [
            'div[role="button"][aria-label="在想些什麼？"]',
            'div[role="button"][aria-label="What\'s on your mind"]',
            'span:has-text("在想些什麼？")',
            'span:has-text("What\'s on your mind")',
            '[data-pagelet="Composer"] div[role="button"]',
        ]

        clicked = False
        for sel in selectors:
            try:
                elem = page.locator(sel).first
                if await elem.is_visible(timeout=3000):
                    await elem.click()
                    clicked = True
                    break
            except:
                continue

        if not clicked:
            print("[ERROR] Could not find post input box")
            return {"success": False, "error": "Post box not found"}

        await asyncio.sleep(random.uniform(1, 2))

        # Type the message
        await human_type(page, message)
        await asyncio.sleep(random.uniform(1, 2))

        # Click Post button
        post_selectors = [
            'div[aria-label="發布"][role="button"]',
            'div[aria-label="Post"][role="button"]',
            'div[role="button"]:has-text("發布")',
            'div[role="button"]:has-text("Post")',
        ]

        posted = False
        for sel in post_selectors:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=3000):
                    if DRY_RUN:
                        print("[DRY RUN] Would click Post button")
                        # Close the dialog
                        await page.keyboard.press("Escape")
                        return {"success": True, "dry_run": True}
                    await btn.click()
                    posted = True
                    break
            except:
                continue

        if not posted:
            print("[ERROR] Could not find Post button")
            await page.keyboard.press("Escape")
            return {"success": False, "error": "Post button not found"}

        await asyncio.sleep(random.uniform(2, 4))
        print("[OK] Text post published!")
        return {"success": True}

    except Exception as e:
        print(f"[ERROR] Post failed: {e}")
        return {"success": False, "error": str(e)}


async def post_with_photos(page, message: str, photo_paths: list) -> dict:
    """Post text + photos to personal timeline."""
    print(f"[INFO] Posting with {len(photo_paths)} photo(s)...")

    try:
        # Click on "What's on your mind" box
        selectors = [
            'div[role="button"][aria-label="在想些什麼？"]',
            'div[role="button"][aria-label="What\'s on your mind"]',
            'span:has-text("在想些什麼？")',
            'span:has-text("What\'s on your mind")',
        ]

        clicked = False
        for sel in selectors:
            try:
                elem = page.locator(sel).first
                if await elem.is_visible(timeout=3000):
                    await elem.click()
                    clicked = True
                    break
            except:
                continue

        if not clicked:
            print("[ERROR] Could not find post input box")
            return {"success": False, "error": "Post box not found"}

        await asyncio.sleep(random.uniform(1, 2))

        # Type message first
        await human_type(page, message)
        await asyncio.sleep(random.uniform(0.5, 1))

        # Click photo/video button
        photo_btn_selectors = [
            'div[aria-label="相片/影片"][role="button"]',
            'div[aria-label="Photo/Video"][role="button"]',
            'div[role="button"]:has-text("相片/影片")',
            'div[role="button"]:has-text("Photo/Video")',
            '[aria-label*="photo" i]',
            '[aria-label*="相片"]',
        ]

        photo_btn_found = False
        for sel in photo_btn_selectors:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=3000):
                    await btn.click()
                    photo_btn_found = True
                    break
            except:
                continue

        if not photo_btn_found:
            print("[ERROR] Could not find photo/video button")
            await page.keyboard.press("Escape")
            return {"success": False, "error": "Photo button not found"}

        await asyncio.sleep(random.uniform(1, 2))

        # Upload photos via file chooser
        for i, photo_path in enumerate(photo_paths):
            if not os.path.exists(photo_path):
                print(f"[WARN] Photo not found: {photo_path}")
                continue

            print(f"[INFO] Uploading photo {i+1}/{len(photo_paths)}: {photo_path}")

            # Listen for file chooser
            async with page.expect_file_chooser() as fc_info:
                # Click the add photo button or file input
                add_selectors = [
                    'div[aria-label="相片/影片"][role="button"]',
                    'div[aria-label="Photo/Video"][role="button"]',
                    'input[type="file"][accept*="image"]',
                ]
                for sel in add_selectors:
                    try:
                        if 'input' in sel:
                            await page.set_input_files(sel, photo_path)
                            break
                        else:
                            elem = page.locator(sel).first
                            if await elem.is_visible(timeout=2000):
                                await elem.click()
                                break
                    except:
                        continue

            file_chooser = await fc_info.value
            await file_chooser.set_files(photo_path)
            await asyncio.sleep(random.uniform(2, 4))

        await asyncio.sleep(random.uniform(1, 3))

        # Set sharing to Public (optional)
        try:
            share_btn = page.locator('div[aria-label="編輯分享對象"]').first
            if await share_btn.is_visible(timeout=2000):
                await share_btn.click()
                await asyncio.sleep(1)
                public_btn = page.locator('div[role="button"]:has-text("公開")').first
                if await public_btn.is_visible(timeout=2000):
                    await public_btn.click()
                    await asyncio.sleep(1)
        except:
            pass  # Public setting is optional

        # Click Post button
        post_selectors = [
            'div[aria-label="發布"][role="button"]',
            'div[aria-label="Post"][role="button"]',
            'div[role="button"]:has-text("發布")',
            'div[role="button"]:has-text("Post")',
        ]

        posted = False
        for sel in post_selectors:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=3000):
                    if DRY_RUN:
                        print("[DRY RUN] Would click Post button")
                        await page.keyboard.press("Escape")
                        return {"success": True, "dry_run": True}
                    await btn.click()
                    posted = True
                    break
            except:
                continue

        if not posted:
            print("[ERROR] Could not find Post button")
            await page.keyboard.press("Escape")
            return {"success": False, "error": "Post button not found"}

        await asyncio.sleep(random.uniform(3, 5))
        print("[OK] Photo post published!")
        return {"success": True}

    except Exception as e:
        print(f"[ERROR] Post failed: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Facebook Personal Timeline Poster")
    parser.add_argument("--message", "-m", required=True, help="Post message text")
    parser.add_argument("--photos", "-p", nargs="*", help="Photo file paths")
    parser.add_argument("--dry-run", action="store_true", default=DRY_RUN, help="Dry run mode")
    parser.add_argument("--headless", action="store_true", help="Run headless")
    args = parser.parse_args()

    if args.dry_run:
        os.environ["FB_DRY_RUN"] = "true"
        print("[MODE] DRY RUN - no actual posting")

    pw, browser, context, page = await create_session()

    try:
        if not await navigate_to_facebook(page):
            return

        if args.photos:
            result = await post_with_photos(page, args.message, args.photos)
        else:
            result = await post_text(page, args.message)

        print(f"\nResult: {json.dumps(result, ensure_ascii=False, indent=2)}")

    finally:
        await browser.close()
        await pw.stop()


if __name__ == "__main__":
    asyncio.run(main())
