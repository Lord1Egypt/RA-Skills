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
        'tool': 'applescript_app',
        'action': action,
        **extra,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Control macOS applications through AppleScript.')
    parser.add_argument('--action', required=True, choices=['open', 'activate', 'is-running', 'frontmost-app'])
    parser.add_argument('--app', help='Application name, e.g. 微信 or Safari.')
    parser.add_argument('--path', help='Application bundle path for open action, e.g. /Applications/微信.app.')
    parser.add_argument('--json-pretty', action='store_true', help='Pretty-print JSON output.')
    args = parser.parse_args()

    if args.action == 'open':
        if args.path:
            subprocess.run(['open', args.path], check=True)
            emit(build_result('open', path=args.path, launch='open-path'), args.json_pretty)
            return
        if not args.app:
            raise SystemExit("Action 'open' requires --app or --path.")
        run_osascript([
            f'tell application "{args.app}" to activate',
        ])
        emit(build_result('open', app=args.app, launch='activate-app'), args.json_pretty)
        return

    if args.action == 'activate':
        if not args.app:
            raise SystemExit("Action 'activate' requires --app.")
        run_osascript([
            f'tell application "{args.app}" to activate',
            'tell application "System Events"',
            f'tell process "{args.app}" to set frontmost to true',
            'end tell',
        ])
        emit(build_result('activate', app=args.app, frontmost=True), args.json_pretty)
        return

    if args.action == 'is-running':
        if not args.app:
            raise SystemExit("Action 'is-running' requires --app.")
        out = run_osascript([
            f'tell application "System Events" to return (name of processes) contains "{args.app}"',
        ])
        emit(build_result('is-running', app=args.app, running=out.lower() == 'true'), args.json_pretty)
        return

    if args.action == 'frontmost-app':
        out = run_osascript([
            'tell application "System Events"',
            'set frontApp to name of first application process whose frontmost is true',
            'return frontApp',
            'end tell',
        ])
        emit(build_result('frontmost-app', app=out), args.json_pretty)
        return

    raise SystemExit(f'Unsupported action: {args.action}')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr or str(e))
        raise
