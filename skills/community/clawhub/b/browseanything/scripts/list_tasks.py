#!/usr/bin/env python3
"""List recent tasks for the current API key.

Usage:
    python3 list_tasks.py                # 20 most recent
    python3 list_tasks.py --limit 50
    python3 list_tasks.py --offset 100 --json
"""
from __future__ import annotations

import argparse
import sys

from _client import ApiError, print_json, request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    try:
        resp = request(
            "GET",
            f"/api/v1/tasks?limit={args.limit}&offset={args.offset}",
        )
    except ApiError as e:
        sys.stderr.write(f"Failed to list tasks: {e}\n")
        return 1

    if args.json:
        print_json(resp)
        return 0

    for t in resp.get("tasks", []):
        status = t.get("status") or "unknown"
        steps = t.get("step_count") or 0
        sys.stdout.write(
            f"{t['id']}  {status:>14}  {steps:>3} steps  "
            f"{t['prompt']}\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
