#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time

import pyautogui

pyautogui.FAILSAFE = True


def read_text_from_stdin() -> str:
    data = sys.stdin.read()
    if not data:
        raise SystemExit('No stdin input provided.')
    return data


def maybe_sleep(delay: float) -> None:
    if delay > 0:
        time.sleep(delay)


def copy_to_clipboard(text: str) -> None:
    subprocess.run(['pbcopy'], input=text, text=True, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description='Control macOS keyboard using Python/pyautogui.')
    parser.add_argument('--action', required=True, choices=['paste', 'press', 'hotkey', 'key-down', 'key-up'])
    parser.add_argument('--text', help='Text to paste.')
    parser.add_argument('--stdin', action='store_true', help='Read text from stdin for paste action.')
    parser.add_argument('--key', help='Single key for press, key-down, or key-up.')
    parser.add_argument('--keys', nargs='*', help='Multiple keys for hotkey action, e.g. command v.')
    parser.add_argument('--interval', type=float, default=0.0, help='Interval between shortcut key presses.')
    parser.add_argument('--presses', type=int, default=1, help='Repeat count for press action.')
    parser.add_argument('--delay', type=float, default=0.0, help='Delay before action, in seconds.')
    parser.add_argument('--paste-shortcut-delay', type=float, default=0.05, help='Delay after updating clipboard before Command+V.')
    args = parser.parse_args()

    maybe_sleep(args.delay)

    if args.action == 'paste':
        text = read_text_from_stdin() if args.stdin else args.text
        if text is None:
            raise SystemExit("Action 'paste' requires --text or --stdin.")
        copy_to_clipboard(text)
        maybe_sleep(args.paste_shortcut_delay)
        pyautogui.hotkey('command', 'v', interval=args.interval)
        print(json.dumps({'action': 'paste', 'text': text, 'length': len(text)}))
        return

    if args.action == 'press':
        if not args.key:
            raise SystemExit("Action 'press' requires --key.")
        pyautogui.press(args.key, presses=args.presses, interval=args.interval)
        print(json.dumps({'action': 'press', 'key': args.key, 'presses': args.presses}))
        return

    if args.action == 'hotkey':
        if not args.keys:
            raise SystemExit("Action 'hotkey' requires --keys.")
        pyautogui.hotkey(*args.keys, interval=args.interval)
        print(json.dumps({'action': 'hotkey', 'keys': args.keys}))
        return

    if args.action == 'key-down':
        if not args.key:
            raise SystemExit("Action 'key-down' requires --key.")
        pyautogui.keyDown(args.key)
        print(json.dumps({'action': 'key-down', 'key': args.key}))
        return

    if args.action == 'key-up':
        if not args.key:
            raise SystemExit("Action 'key-up' requires --key.")
        pyautogui.keyUp(args.key)
        print(json.dumps({'action': 'key-up', 'key': args.key}))
        return

    raise SystemExit(f'Unsupported action: {args.action}')


if __name__ == '__main__':
    main()
