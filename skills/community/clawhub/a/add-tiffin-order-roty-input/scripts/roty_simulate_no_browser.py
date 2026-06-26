#!/usr/bin/env python3
"""
roty_simulate_no_browser.py

Simulation-only runner for the Add Tiffin Order - Roty Input skill.
No Playwright or browser dependencies — uses vision hook placeholders to infer coordinates
from screenshots and logs simulated mouse clicks (page.mouse.click(x,y)).

Behavior:
- Parse the provided message (uses parse_roty_input.py)
- For each UI element to act on, call vision_find(label, screenshot_path)
  - If vision_find returns coordinates, simulate click by logging "mouse.click(x,y)"
  - If not, pause and print a clear question asking the operator to provide coordinates or a zoomed screenshot URL
- Stop before final confirm/submit and log "Would click confirm here — STOP"

Usage: python3 roty_simulate_no_browser.py "<message>"

"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

# reuse the parser
import subprocess
import shlex

SCRIPT_DIR = Path(__file__).resolve().parent
PARSER = SCRIPT_DIR / 'parse_roty_input.py'

# Placeholder vision function: expected to return list of boxes [{x,y,width,height,confidence}]
# In this simulation environment it returns [] and triggers a pause asking for coordinates.

def vision_find(label: str, screenshot_path: str) -> List[Dict]:
    # Real implementation should run OCR/template-match on screenshot_path and find regions matching label
    # For now return empty to indicate not found.
    # fallback: if operator provided known coordinates mapping, use them
    FALLBACK_COORDS = {
        'Veg Tiffin': {'x': 640, 'y': 400, 'width': 200, 'height': 80, 'confidence': 0.6},
        '6 rotis': {'x': 800, 'y': 520, 'width': 120, 'height': 40, 'confidence': 0.5},
        'Extra Rice': {'x': 860, 'y': 560, 'width': 120, 'height': 40, 'confidence': 0.5},
        'day-9': {'x': 500, 'y': 360, 'width': 40, 'height': 30, 'confidence': 0.5},
        'Notes': {'x': 640, 'y': 680, 'width': 400, 'height': 80, 'confidence': 0.5},
        'Add to cart': {'x': 1100, 'y': 700, 'width': 160, 'height': 50, 'confidence': 0.6},
        'Checkout': {'x': 1100, 'y': 740, 'width': 160, 'height': 50, 'confidence': 0.6},
        'Login': {'x': 640, 'y': 200, 'width': 300, 'height': 120, 'confidence': 0.5},
        'Name': {'x': 520, 'y': 300, 'width': 300, 'height': 40, 'confidence': 0.5},
        'Phone': {'x': 520, 'y': 360, 'width': 300, 'height': 40, 'confidence': 0.5},
        'Address': {'x': 520, 'y': 420, 'width': 400, 'height': 40, 'confidence': 0.5},
        'Bank transfer': {'x': 600, 'y': 620, 'width': 300, 'height': 40, 'confidence': 0.5},
    }
    if label in FALLBACK_COORDS:
        return [FALLBACK_COORDS[label]]
    return []


def center(box: Dict) -> Tuple[int,int]:
    return int(box['x'] + box['width']/2), int(box['y'] + box['height']/2)


def run_parser(message: str):
    # call the existing parser script and capture JSON-like dict printed
    p = subprocess.run([sys.executable, str(PARSER)], input=message.encode('utf-8'), stdout=subprocess.PIPE)
    out = p.stdout.decode('utf-8').strip()
    # parser prints a python dict; safer to eval with json if possible — but parse_roty_input prints python dict
    try:
        # try json
        data = json.loads(out)
    except Exception:
        # fallback: replace single quotes and use json-ish
        s = out.replace("'", '"')
        try:
            data = json.loads(s)
        except Exception:
            # last resort: present raw
            data = out
    return data


def simulate_click(label: str, screenshot: str):
    boxes = vision_find(label, screenshot)
    if not boxes:
        print(f"VISION: could not find '{label}' on screenshot ({screenshot}).")
        print("PAUSE: Please provide coordinates or a zoomed screenshot URL for this element in Telegram, formatted as JSON: {\"label\": \"Veg Tiffin\", \"x\": 123, \"y\": 456}")
        return None
    box = boxes[0]
    x,y = center(box)
    print(f"SIM: Would mouse.click({x},{y}) for '{label}' (box={box})")
    return (x,y)


def simulate_flow(parsed):
    print('\n=== Simulated automation trace ===')
    print('Parsed order data:')
    print(json.dumps(parsed, indent=2))
    print('\nSteps to simulate (vision+coords):\n')
    screenshot = str(SCRIPT_DIR / 'last_page.png')
    print(f'(Simulation will use screenshot path: {screenshot} — provide an updated screenshot if available)')

    # 1 Veg Tiffin
    r = simulate_click('Veg Tiffin', screenshot)
    if r is None:
        return

    # 2 modifier1
    r = simulate_click('6 rotis', screenshot)
    if r is None:
        return

    # 3 modifier2
    r = simulate_click('Extra Rice', screenshot)
    if r is None:
        return

    # 4 calendar dates
    dates = parsed.get('dates', [])
    anchor_found = None
    anchor_day = None
    # try to find any anchor date first (the first date in the list)
    if dates:
        first = dates[0]
        daynum = int(first.split('-')[2])
        anchor = f'day-{daynum}'
        box = vision_find(anchor, screenshot)
        if box:
            b = box[0]
            ax, ay = center(b)
            anchor_found = (ax, ay)
            anchor_day = daynum
            print(f"SIM: Found anchor date {anchor} at ({ax},{ay})")
        else:
            print(f"VISION: could not find anchor date '{anchor}' on screenshot ({screenshot}).")
            print('PAUSE: Please provide coordinates or a zoomed screenshot URL for the calendar anchor date.')
            return
        # assume horizontal delta ~70px per day on same row
        delta_x = 70
        delta_y = 0
        # click each date relative to anchor
        for d in dates:
            day = int(d.split('-')[2])
            offset_days = day - anchor_day
            click_x = anchor_found[0] + offset_days * delta_x
            click_y = anchor_found[1] + 0 * delta_y
            print(f"SIM: Would mouse.click({click_x},{click_y}) for '{d}' (computed from anchor)")

    # 5 notes
    r = simulate_click('Notes', screenshot)
    if r is None:
        return
    else:
        print(f"SIM: Would type notes: '{parsed.get('special_requests') or ''}'")

    # 6 add to cart
    r = simulate_click('Add to cart', screenshot)
    if r is None:
        return

    # 7 checkout
    r = simulate_click('Checkout', screenshot)
    if r is None:
        return

    # 8 login if needed
    r = simulate_click('Login', screenshot)
    if r:
        print("SIM: Would type Email and Password into detected fields and submit login")

    # 9 fill checkout fields
    r = simulate_click('Name', screenshot)
    if r is None:
        return
    print(f"SIM: Would type Name: {parsed.get('name')}")
    r = simulate_click('Phone', screenshot)
    if r is None:
        print('SIM: Phone field not found visually — would leave empty or prompt user')
    else:
        print("SIM: Would type Phone: 0412345678")
    r = simulate_click('Address', screenshot)
    if r is None:
        return
    print("SIM: Would type Address: 3/12 Smith St, Melbourne VIC 3000")

    # 10 payment
    r = simulate_click('Bank transfer', screenshot)
    if r is None:
        return

    print('\nReached final confirmation — Would click confirm here — STOP (safe dry-run). No order placed.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: roty_simulate_no_browser.py "<message>"')
        sys.exit(1)
    message = sys.argv[1]
    parsed = run_parser(message)
    # parsed may be list from parser; ensure dict
    if isinstance(parsed, list) and parsed:
        parsed = parsed[0]
    simulate_flow(parsed)
