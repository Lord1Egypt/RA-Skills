#!/usr/bin/env python3
"""Execute multiple Bitrix24 REST methods in one HTTP request using batch API."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib import error, parse, request

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bitrix24_config import load_url, normalize_url, validate_url  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch-call Bitrix24 REST methods.")
    parser.add_argument(
        "--cmd",
        action="append",
        required=True,
        help="Command in name=method?params form, e.g. 'tasks=tasks.task.list?filter[STATUS]=2'. Repeat for each method.",
    )
    parser.add_argument("--halt", type=int, default=0, help="Stop on first error (1) or run all (0, default)")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Pretty-print JSON response")
    return parser.parse_args()


def parse_commands(raw_cmds: list[str]) -> dict[str, str]:
    """Parse 'name=method?params' into {name: 'method?params'}."""
    commands: dict[str, str] = {}
    for i, item in enumerate(raw_cmds):
        if "=" not in item:
            raise ValueError(f"Invalid --cmd '{item}'. Use name=method or name=method?params")
        name, method_with_params = item.split("=", 1)
        if not name:
            name = f"cmd{i}"
        commands[name] = method_with_params
    return commands


def main() -> int:
    args = parse_args()
    raw_url, source = load_url()
    if not raw_url:
        print(json.dumps({"ok": False, "error": "No Bitrix24 webhook configured", "source": source}, indent=2))
        return 1

    normalized_url = validate_url(raw_url)

    try:
        commands = parse_commands(args.cmd)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    url = normalize_url(normalized_url) + "batch.json"
    params: list[tuple[str, str]] = [("halt", str(args.halt))]
    for name, method_call in commands.items():
        params.append((f"cmd[{name}]", method_call))

    data = parse.urlencode(params).encode("utf-8")
    req = request.Request(url, data=data, headers={"Accept": "application/json"})

    try:
        with request.urlopen(req, timeout=args.timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
            status = response.getcode()
    except error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        status = exc.code
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc), "source": source}, indent=2))
        return 1

    try:
        body = json.loads(payload)
    except Exception:
        body = {"raw": payload}

    result = {"ok": status < 400, "status": status, "source": source, "commands": list(commands.keys()), "body": body}
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=True))
    return 0 if status < 400 else 1


if __name__ == "__main__":
    sys.exit(main())
