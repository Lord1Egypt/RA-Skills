#!/usr/bin/env python3
"""
roty_order_automation.py

Updated automation template for Bitely Flutter Web (vision + coordinate based).
This script captures screenshots, calls a vision hook (placeholder) to find UI elements,
computes center coordinates and performs page.mouse.click(x,y).

This is a template: the vision function must be implemented (OpenCV/Tesseract or external API).
When run in a capable environment the script will:
 - load orders.json (list of OrderLine dicts)
 - open the Bitely page in Playwright
 - take screenshots and call vision_find(text, screenshot_path) to get bounding boxes
 - click centers of matched boxes and log each action
 - stop before final confirm

Usage: python3 roty_order_automation.py orders.json
"""
from __future__ import annotations
import asyncio
import json
import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Playwright import deferred to runtime
try:
    from playwright.async_api import async_playwright
except Exception:
    async_playwright = None


def center_of_box(box: Dict) -> Tuple[int, int]:
    x = int(box['x'] + box['width'] / 2)
    y = int(box['y'] + box['height'] / 2)
    return x, y


# Placeholder vision hook — must be implemented by user/environment.
# Expected to return a dict: { 'label': [ { 'x':.., 'y':.., 'width':.., 'height':.., 'confidence':0.9 }, ... ] }
# e.g. vision_find('Veg Tiffin', 'screenshot.png') -> {'Veg Tiffin': [{...}]}
async def vision_find(label: str, image_path: str) -> List[Dict]:
    # IMPLEMENTATION REQUIRED: replace with real OCR/template-match
    # For now return [] to indicate "not found"; automation will pause and ask.
    return []


async def run_order(order: Dict, dry_run: bool = True):
    if async_playwright is None:
        raise RuntimeError('playwright is not installed in this environment')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        url = 'https://app.bitely.com.au/order/roty/qfiDIvUSocQFrVPzM4zQ'
        print(f'Navigating to {url}')
        await page.goto(url, wait_until='networkidle')

        # take full page screenshot
        screenshot_path = '/data/.openclaw/workspace/skills/add-tiffin-order-roty-input/last_page.png'
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f'Screenshot saved: {screenshot_path}')

        # 1) Find Veg Tiffin card visually
        matches = await vision_find('Veg Tiffin', screenshot_path)
        if not matches:
            print('Veg Tiffin not found by vision. Pausing — please provide coordinates or a zoomed screenshot of the Veg card.')
            await browser.close()
            return
        box = matches[0]
        x, y = center_of_box(box)
        print(f'Clicking Veg Tiffin at ({x},{y}) — box={box}')
        await page.mouse.click(x, y)

        # take screenshot after click
        await page.screenshot(path=screenshot_path, full_page=True)

        # 2) Address handling
        # take another screenshot and call vision for 'Address' label / input
        matches = await vision_find('Address', screenshot_path)
        if matches:
            box = matches[0]
            x, y = center_of_box(box)
            print(f'Address input located at approx ({x},{y}) — clicking and typing address')
            await page.mouse.click(x, y)
            await page.keyboard.type(order.get('address', ''), delay=50)
            # after typing, attempt to capture autocomplete and choose first candidate visually
            await page.wait_for_timeout(1000)
            await page.screenshot(path=screenshot_path, full_page=True)
            candidates = await vision_find('autocomplete-candidate', screenshot_path)
            if candidates:
                cbox = candidates[0]
                cx, cy = center_of_box(cbox)
                print(f'Selecting autocomplete candidate at ({cx},{cy})')
                await page.mouse.click(cx, cy)
            else:
                print('No autocomplete candidate found visually — left typed address')
        else:
            print('Address label/input not found visually; relying on previous fills or page behavior')

        # 3) Calendar selection for dates
        for d in order.get('dates', []):
            # search for date text (day number) on screenshot
            day = int(d.split('-')[2])
            await page.screenshot(path=screenshot_path, full_page=True)
            day_matches = await vision_find(str(day), screenshot_path)
            if not day_matches:
                print(f'Date {d} (day {day}) not found visually. Pause and request guidance.')
                await browser.close()
                return
            day_box = day_matches[0]
            dx, dy = center_of_box(day_box)
            print(f'Clicking calendar date {d} at ({dx},{dy})')
            await page.mouse.click(dx, dy)

        # 4) Modifier1: 6 rotis
        await page.screenshot(path=screenshot_path, full_page=True)
        m1 = await vision_find('6 rotis', screenshot_path)
        if m1:
            bx = m1[0]
            x, y = center_of_box(bx)
            print(f'Clicking modifier1 (6 rotis) at ({x},{y})')
            await page.mouse.click(x, y)
        else:
            print('Modifier1 (6 rotis) not found visually; pausing')
            await browser.close()
            return

        # 5) Modifier2: Extra Rice
        await page.screenshot(path=screenshot_path, full_page=True)
        m2 = await vision_find('Extra Rice', screenshot_path)
        if m2:
            bx = m2[0]
            x, y = center_of_box(bx)
            print(f'Clicking modifier2 (Extra Rice) at ({x},{y})')
            await page.mouse.click(x, y)
        else:
            print('Modifier2 (Extra Rice) not found visually; adding to notes instead')

        # 6) Notes
        await page.screenshot(path=screenshot_path, full_page=True)
        notes = await vision_find('Notes', screenshot_path)
        if notes:
            nb = notes[0]
            nx, ny = center_of_box(nb)
            print(f'Clicking notes area at ({nx},{ny}) and typing special requests')
            await page.mouse.click(nx, ny)
            await page.keyboard.type(order.get('special_requests', ''), delay=40)
        else:
            print('Notes area not found visually; skipping notes fill')

        # 7) Add to cart
        await page.screenshot(path=screenshot_path, full_page=True)
        add = await vision_find('Add to cart', screenshot_path)
        if add:
            ab = add[0]
            ax, ay = center_of_box(ab)
            print(f'Clicking Add to cart at ({ax},{ay})')
            await page.mouse.click(ax, ay)
        else:
            print('Add to cart button not found visually; pausing')
            await browser.close()
            return

        # 8) Proceed to checkout (visual)
        await page.screenshot(path=screenshot_path, full_page=True)
        checkout = await vision_find('Checkout', screenshot_path)
        if checkout:
            cb = checkout[0]
            cx, cy = center_of_box(cb)
            print(f'Clicking Checkout at ({cx},{cy})')
            await page.mouse.click(cx, cy)
        else:
            print('Checkout control not found visually; attempting cart view or skip')

        # 9) Login handling (if modal appears)
        await page.screenshot(path=screenshot_path, full_page=True)
        login = await vision_find('Login', screenshot_path)
        if login:
            lb = login[0]
            lx, ly = center_of_box(lb)
            print(f'Login detected visually at ({lx},{ly}) — will click and fill credentials')
            await page.mouse.click(lx, ly)
            # rely on vision to locate email/password inputs
            await page.wait_for_timeout(1000)
            await page.screenshot(path=screenshot_path, full_page=True)
            email_matches = await vision_find('Email', screenshot_path)
            pwd_matches = await vision_find('Password', screenshot_path)
            if email_matches:
                ex, ey = center_of_box(email_matches[0])
                await page.mouse.click(ex, ey)
                await page.keyboard.type('samwisethebot@gmail.com')
                print('Typed login email')
            if pwd_matches:
                px, py = center_of_box(pwd_matches[0])
                await page.mouse.click(px, py)
                await page.keyboard.type('Samwisethebot')
                print('Typed login password')

        # 10) Checkout final fields: name/phone/address
        await page.screenshot(path=screenshot_path, full_page=True)
        name_f = await vision_find('Name', screenshot_path)
        phone_f = await vision_find('Phone', screenshot_path)
        addr_f = await vision_find('Address', screenshot_path)
        if name_f:
            nx, ny = center_of_box(name_f[0])
            await page.mouse.click(nx, ny)
            await page.keyboard.type(order.get('name',''))
            print(f'Filled checkout name with {order.get("name","")}')
        if phone_f:
            px, py = center_of_box(phone_f[0])
            await page.mouse.click(px, py)
            await page.keyboard.type('0412345678')
            print('Filled checkout phone with 0412345678')
        if addr_f:
            ax, ay = center_of_box(addr_f[0])
            await page.mouse.click(ax, ay)
            await page.keyboard.type('3/12 Smith St, Melbourne VIC 3000')
            print('Filled checkout address')

        # 11) Payment: bank transfer
        await page.screenshot(path=screenshot_path, full_page=True)
        pay = await vision_find('Bank transfer', screenshot_path)
        if pay:
            pb = pay[0]
            px, py = center_of_box(pb)
            await page.mouse.click(px, py)
            print('Selected Bank transfer payment method')
        else:
            print('Bank transfer option not found visually')

        print('Reached final confirmation — Would click confirm here — STOP (safe dry-run). No order placed.')

        await browser.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: roty_order_automation.py orders.json')
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r') as f:
        orders = json.load(f)
    asyncio.run(run_order(orders[0]))
