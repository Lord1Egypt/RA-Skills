#!/usr/bin/env python3
"""Reply to a task that is in the `requires_input` state.

Usage:
    python3 submit_input.py <task_id> "my answer"
    cat answer.txt | python3 submit_input.py <task_id> -
"""
from __future__ import annotations

import argparse
import sys

from _client import ApiError, request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("input", help="Answer to send. Use '-' to read from stdin.")
    args = p.parse_args()

    answer = sys.stdin.read().strip() if args.input == "-" else args.input
    if not answer:
        sys.stderr.write("ERROR: empty input.\n")
        return 2

    try:
        resp = request(
            "POST",
            f"/api/v1/tasks/{args.task_id}/input",
            body={"input": answer},
        )
    except ApiError as e:
        sys.stderr.write(f"Failed to submit input: {e}\n")
        return 1

    sys.stdout.write(resp.get("message", "Input submitted.") + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
