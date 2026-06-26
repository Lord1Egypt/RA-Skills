#!/usr/bin/env python3
"""Get the current state of a task (status, result, error, screenshot ref).

Usage:
    python3 get_task.py <task_id>
    python3 get_task.py --field status <task_id>
"""
from __future__ import annotations

import argparse
import sys

from _client import ApiError, print_json, request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("--field", help="Print only one field of task (e.g. status, result).")
    args = p.parse_args()

    try:
        resp = request("GET", f"/api/v1/tasks/{args.task_id}")
    except ApiError as e:
        sys.stderr.write(f"Failed to fetch task: {e}\n")
        return 1

    task = resp["task"]
    if args.field:
        value = task.get(args.field)
        if value is None:
            sys.stderr.write(f"(field '{args.field}' is null/missing)\n")
            return 1
        if isinstance(value, (dict, list)):
            print_json(value)
        else:
            sys.stdout.write(f"{value}\n")
    else:
        print_json(task)
    return 0


if __name__ == "__main__":
    sys.exit(main())
