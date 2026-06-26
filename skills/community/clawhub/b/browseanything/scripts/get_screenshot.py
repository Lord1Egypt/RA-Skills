#!/usr/bin/env python3
"""Download the latest screenshot for a task to a PNG file.

Usage:
    python3 get_screenshot.py <task_id>                   # writes <task_id>.png
    python3 get_screenshot.py <task_id> --out path.png
"""
from __future__ import annotations

import argparse
import sys

from _client import ApiError, request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("--out", help="Output file path. Default: <task_id>.png")
    args = p.parse_args()

    try:
        body, _ = request(
            "GET",
            f"/api/v1/tasks/{args.task_id}/screenshot",
            raw=True,
        )
    except ApiError as e:
        sys.stderr.write(f"Failed to fetch screenshot: {e}\n")
        return 1

    out_path = args.out or f"{args.task_id}.png"
    with open(out_path, "wb") as f:
        f.write(body)
    sys.stdout.write(f"{out_path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
