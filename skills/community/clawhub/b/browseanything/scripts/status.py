#!/usr/bin/env python3
"""Service status: how many tasks are running on the BrowseAnything backend
and how many free slots remain. Useful before submitting a big batch.

Usage:
    python3 status.py
"""
from __future__ import annotations

import sys

from _client import ApiError, print_json, request


def main() -> int:
    try:
        resp = request("GET", "/api/v1/status")
    except ApiError as e:
        sys.stderr.write(f"Failed to get status: {e}\n")
        return 1
    print_json(resp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
