#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Optional

import pyautogui

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from calibration import ensure_calibration  # noqa: E402

pyautogui.FAILSAFE = True


def parse_stdin_point() -> tuple[int, int]:
    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError('No stdin input. Expected: "x y" or JSON with x/y.')

    try:
        obj = json.loads(raw)
        if isinstance(obj, dict) and 'x' in obj and 'y' in obj:
            return int(float(obj['x'])), int(float(obj['y']))
    except json.JSONDecodeError:
        pass

    parts = raw.replace(',', ' ').split()
    if len(parts) < 2:
        raise ValueError(f'Invalid point from stdin: {raw!r}')
    return int(float(parts[0])), int(float(parts[1]))


def resolve_point(args: argparse.Namespace) -> tuple[Optional[int], Optional[int]]:
    if args.stdin:
        return parse_stdin_point()
    return args.x, args.y


def require_point(x: Optional[int], y: Optional[int], action: str) -> tuple[int, int]:
    if x is None or y is None:
        raise SystemExit(f'Action {action!r} requires --x and --y, or use --stdin.')
    return x, y


def maybe_sleep(delay: float) -> None:
    if delay > 0:
        time.sleep(delay)


def main() -> None:
    ensure_calibration()
    parser = argparse.ArgumentParser(description='Control macOS mouse using Python/pyautogui.')
    parser.add_argument('--action', default='click', choices=['move', 'click', 'double-click', 'right-click', 'drag', 'mouse-down', 'mouse-up', 'position'])
    parser.add_argument('--x', type=int)
    parser.add_argument('--y', type=int)
    parser.add_argument('--to-x', type=int, help='Drag destination x.')
    parser.add_argument('--to-y', type=int, help='Drag destination y.')
    parser.add_argument('--stdin', action='store_true', help='Read point as "x y" or JSON {"x":...,"y":...} from stdin.')
    parser.add_argument('--duration', type=float, default=0.0, help='Move/drag duration in seconds.')
    parser.add_argument('--button', default='left', choices=['left', 'middle', 'right'])
    parser.add_argument('--delay', type=float, default=0.0, help='Delay before action, in seconds.')
    parser.add_argument('--clicks', type=int, default=2, help='Click count used by double-click action.')
    parser.add_argument('--interval', type=float, default=0.0, help='Interval between repeated clicks.')
    args = parser.parse_args()

    if args.action == 'position':
        pos = pyautogui.position()
        print(json.dumps({'x': pos.x, 'y': pos.y}))
        return

    x, y = resolve_point(args)
    maybe_sleep(args.delay)

    if args.action == 'move':
        x, y = require_point(x, y, args.action)
        pyautogui.moveTo(x, y, duration=args.duration)
        print(json.dumps({'action': 'move', 'x': x, 'y': y}))
        return

    if args.action == 'click':
        x, y = require_point(x, y, args.action)
        pyautogui.moveTo(x, y, duration=args.duration)
        pyautogui.click(x=x, y=y, button=args.button)
        print(json.dumps({'action': 'click', 'x': x, 'y': y, 'button': args.button}))
        return

    if args.action == 'double-click':
        x, y = require_point(x, y, args.action)
        pyautogui.moveTo(x, y, duration=args.duration)
        pyautogui.click(x=x, y=y, clicks=args.clicks, interval=args.interval, button=args.button)
        print(json.dumps({'action': 'double-click', 'x': x, 'y': y, 'button': args.button, 'clicks': args.clicks}))
        return

    if args.action == 'right-click':
        x, y = require_point(x, y, args.action)
        pyautogui.moveTo(x, y, duration=args.duration)
        pyautogui.rightClick(x=x, y=y)
        print(json.dumps({'action': 'right-click', 'x': x, 'y': y}))
        return

    if args.action == 'mouse-down':
        x, y = require_point(x, y, args.action)
        pyautogui.moveTo(x, y, duration=args.duration)
        pyautogui.mouseDown(x=x, y=y, button=args.button)
        print(json.dumps({'action': 'mouse-down', 'x': x, 'y': y, 'button': args.button}))
        return

    if args.action == 'mouse-up':
        x, y = require_point(x, y, args.action)
        pyautogui.moveTo(x, y, duration=args.duration)
        pyautogui.mouseUp(x=x, y=y, button=args.button)
        print(json.dumps({'action': 'mouse-up', 'x': x, 'y': y, 'button': args.button}))
        return

    if args.action == 'drag':
        x, y = require_point(x, y, args.action)
        if args.to_x is None or args.to_y is None:
            raise SystemExit("Action 'drag' requires --to-x and --to-y.")
        pyautogui.moveTo(x, y, duration=0)
        pyautogui.dragTo(args.to_x, args.to_y, duration=args.duration, button=args.button)
        print(json.dumps({
            'action': 'drag',
            'from': {'x': x, 'y': y},
            'to': {'x': args.to_x, 'y': args.to_y},
            'button': args.button,
        }))
        return

    raise SystemExit(f'Unsupported action: {args.action}')


if __name__ == '__main__':
    main()
