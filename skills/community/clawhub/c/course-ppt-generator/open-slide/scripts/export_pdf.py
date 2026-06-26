#!/usr/bin/env python3
"""
Export an open-slide deck to a single PDF.
Requires: playwright, Pillow (pip install playwright Pillow)

Usage:
  python3 export_pdf.py --url http://localhost:5173/s/my-deck --pages 5 --out /tmp/deck.pdf

IMPORTANT: This script enters Present mode before capturing, which gives
clean slide screenshots without editor navbars/chrome. The approach is:
  1. Open the deck editor URL
  2. Press F to enter Present mode (clean slide view)
  3. Hide any remaining presenter controls via CSS injection
  4. Screenshot each page, advancing with ArrowRight
  5. Combine screenshots into a PDF via Pillow

Do NOT screenshot the editor view directly — it includes navbars and sidebars.
Always use Present mode first.

Options:
  --url      URL of the slide deck (dev server or preview)
  --pages    Number of pages in the deck (required)
  --out      Output PDF path (default: ./deck.pdf)
  --cdp      Optional CDP endpoint for an already-running Chromium browser
  --width    Canvas width in px (default: 1920)
  --height   Canvas height in px (default: 1080)
  --delay    Delay between page navigations in ms (default: 1000)
"""

import argparse
import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return parsed


async def main():
    parser = argparse.ArgumentParser(description="Export open-slide deck to PDF (present mode)")
    parser.add_argument("--url", required=True, help="Slide deck URL (editor route, e.g. /s/my-deck)")
    parser.add_argument("--pages", type=positive_int, required=True, help="Number of pages in the deck")
    parser.add_argument("--out", default="deck.pdf", help="Output PDF path")
    parser.add_argument("--cdp", default=None, help="Optional CDP endpoint")
    parser.add_argument("--width", type=int, default=1920, help="Canvas width")
    parser.add_argument("--height", type=int, default=1080, help="Canvas height")
    parser.add_argument("--delay", type=int, default=1000, help="Delay between pages (ms)")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: playwright not installed. Run: pip install playwright", file=sys.stderr)
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        sys.exit(1)

    tmp_dir = tempfile.mkdtemp(prefix="open-slide-pdf-")
    img_paths = []
    images = []

    try:
        async with async_playwright() as p:
            if args.cdp:
                browser = await p.chromium.connect_over_cdp(args.cdp)
                close_browser = False
                contexts = browser.contexts
                if contexts:
                    ctx = contexts[0]
                    close_context = False
                else:
                    ctx = await browser.new_context(viewport={"width": args.width, "height": args.height})
                    close_context = True
            else:
                browser = await p.chromium.launch()
                close_browser = True
                ctx = await browser.new_context(viewport={"width": args.width, "height": args.height})
                close_context = True

            page = await ctx.new_page()
            await page.set_viewport_size({"width": args.width, "height": args.height})

            # Step 1: Open the deck editor.
            await page.goto(args.url, wait_until="domcontentloaded", timeout=60000)
            try:
                await page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                pass
            await page.wait_for_timeout(2000)

            # Step 2: Enter Present mode by pressing F. This gives a clean slide view
            # without editor navbars, sidebars, or chrome.
            await page.keyboard.press("F")
            await page.wait_for_timeout(1500)

            # Step 3: Hide any remaining presenter controls.
            await page.evaluate("""
                const s = document.createElement('style');
                s.textContent = 'button,[role=toolbar],[aria-label*=Keyboard]{display:none!important}';
                document.head.appendChild(s);
            """)
            await page.wait_for_timeout(500)

            # Step 4: Screenshot each page.
            for i in range(args.pages):
                img_path = os.path.join(tmp_dir, f"slide_{i + 1}.png")
                await page.screenshot(path=img_path, full_page=False)
                size = os.path.getsize(img_path)
                print(f"Slide {i + 1}/{args.pages}: {size} bytes")
                img_paths.append(img_path)

                if i < args.pages - 1:
                    await page.keyboard.press("ArrowRight")
                    await page.wait_for_timeout(args.delay)

            await page.close()
            if close_context:
                await ctx.close()
            if close_browser:
                await browser.close()

        # Step 5: Convert PNG screenshots to a single PDF.
        images = [Image.open(path).convert("RGB") for path in img_paths]
        first = images[0]
        rest = images[1:]
        first.save(out_path, "PDF", resolution=150, save_all=True, append_images=rest)

        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"\nDone: {args.pages} slides -> {out_path} ({size_mb:.1f} MB)")
    finally:
        for image in images:
            image.close()
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    asyncio.run(main())
