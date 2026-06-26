#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pyautogui

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from calibration import DEFAULT_CALIBRATION_PATH, save_calibration  # noqa: E402


def detect_mapping() -> dict:
    screenshot = pyautogui.screenshot()
    screen_w, screen_h = pyautogui.size()
    shot_w, shot_h = screenshot.size

    scale_x = shot_w / screen_w
    scale_y = shot_h / screen_h

    mode = 'retina' if round(scale_x, 2) == 2.0 and round(scale_y, 2) == 2.0 else 'unknown'

    return {
        'screen_width_points': screen_w,
        'screen_height_points': screen_h,
        'screenshot_width_pixels': shot_w,
        'screenshot_height_pixels': shot_h,
        'scale_x': scale_x,
        'scale_y': scale_y,
        'mode': mode,
        'note': 'v1 focuses on Retina/single primary display. Add scaled and multi-monitor cases later.',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Initialize macOS screenshot/click coordinate mapping.')
    parser.add_argument('--output', type=Path, default=DEFAULT_CALIBRATION_PATH)
    args = parser.parse_args()

    data = detect_mapping()
    save_calibration(data, args.output)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f'\nSaved calibration to: {args.output}')


if __name__ == '__main__':
    main()
