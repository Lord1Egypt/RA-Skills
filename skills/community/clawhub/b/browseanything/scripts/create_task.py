#!/usr/bin/env python3
"""Low-level: create a task and print the task id (no polling).

Use this when you want to fire-and-forget, or to manage polling yourself.

Usage:
    python3 create_task.py "Prompt..."
    python3 create_task.py --model gpt-5.2 "Prompt..."
"""
from __future__ import annotations

import argparse
import json
import sys

from _client import ApiError, print_json, request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("prompt")
    p.add_argument("--model")
    p.add_argument("--max-steps", type=int)
    p.add_argument("--proxy", dest="proxy_location")
    p.add_argument("--metadata")
    p.add_argument("--json", action="store_true",
                   help="Print full create response instead of just the id.")
    args = p.parse_args()

    body: dict = {"prompt": args.prompt}
    if args.model:
        body["model"] = args.model
    if args.max_steps:
        body["max_steps"] = args.max_steps
    if args.proxy_location:
        body["proxy_location"] = args.proxy_location
    if args.metadata:
        body["metadata"] = json.loads(args.metadata)

    try:
        resp = request("POST", "/api/v1/tasks", body=body)
    except ApiError as e:
        sys.stderr.write(f"Failed to create task: {e}\n")
        return 1

    if args.json:
        print_json(resp)
    else:
        sys.stdout.write(resp["task"]["id"] + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
