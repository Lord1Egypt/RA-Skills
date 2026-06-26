#!/usr/bin/env python3
"""Cancel a running or queued task.

Usage:
    python3 cancel_task.py <task_id>
"""
from __future__ import annotations

import argparse
import sys

from _client import ApiError, request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    args = p.parse_args()

    try:
        resp = request("DELETE", f"/api/v1/tasks/{args.task_id}")
    except ApiError as e:
        sys.stderr.write(f"Failed to cancel task: {e}\n")
        return 1

    sys.stdout.write(resp.get("message", "Cancelled.") + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
