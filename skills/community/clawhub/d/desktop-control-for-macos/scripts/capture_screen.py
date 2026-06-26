#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pyautogui

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from calibration import ensure_calibration  # noqa: E402

DEFAULT_OUTPUT = Path('/tmp/macos_desktop_control/screen_logical.png')


def capture_logical(output: Path) -> Path:
    ensure_calibration()
    output.parent.mkdir(parents=True, exist_ok=True)

    img = pyautogui.screenshot()
    screen_w, screen_h = pyautogui.size()

    img = img.resize((screen_w, screen_h))
    img.save(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description='Capture macOS screen and resize to logical coordinates.')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = capture_logical(args.output)
    print(str(result))


if __name__ == '__main__':
    main()
