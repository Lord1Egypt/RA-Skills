#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any, List


def run_osascript(lines: List[str]) -> str:
    proc = subprocess.run(
        ["osascript", *sum([["-e", line] for line in lines], [])],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def emit(payload: dict[str, Any], pretty: bool) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None))


def build_result(action: str, ok: bool = True, **extra: Any) -> dict[str, Any]:
    return {
        'ok': ok,
        'tool': 'applescript_window',
        'action': action,
        **extra,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Inspect macOS application windows through AppleScript.')
    parser.add_argument('--action', required=True, choices=['title', 'count', 'list'])
    parser.add_argument('--app', required=True, help='Application process name, e.g. 微信 or Safari.')
    parser.add_argument('--json-pretty', action='store_true', help='Pretty-print JSON output.')
    args = parser.parse_args()

    if args.action == 'title':
        out = run_osascript([
            'tell application "System Events"',
            f'tell process "{args.app}"',
            'if (count of windows) > 0 then',
            'return name of front window',
            'else',
            'return ""',
            'end if',
            'end tell',
            'end tell',
        ])
        emit(build_result('title', app=args.app, title=out), args.json_pretty)
        return

    if args.action == 'count':
        out = run_osascript([
            'tell application "System Events"',
            f'tell process "{args.app}"',
            'return count of windows',
            'end tell',
            'end tell',
        ])
        emit(build_result('count', app=args.app, count=int(out or '0')), args.json_pretty)
        return

    if args.action == 'list':
        out = run_osascript([
            'tell application "System Events"',
            f'tell process "{args.app}"',
            'if (count of windows) = 0 then',
            'return ""',
            'else',
            'set AppleScript\'s text item delimiters to linefeed',
            'return (name of every window) as text',
            'end if',
            'end tell',
            'end tell',
        ])
        titles = [line for line in out.splitlines() if line.strip()]
        emit(build_result('list', app=args.app, titles=titles), args.json_pretty)
        return

    raise SystemExit(f'Unsupported action: {args.action}')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr or str(e))
        raise
