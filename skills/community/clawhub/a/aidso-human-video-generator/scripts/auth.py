#!/usr/bin/env python3
"""Bind an AIDSO account through the authorization-link flow."""

from __future__ import annotations

import argparse
import sys

from _aidso import AidsoError, authorization_status, complete_authorization, print_json, start_authorization


def main() -> int:
    parser = argparse.ArgumentParser(description="Bind an AIDSO account for this skill.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--start", action="store_true", help="Generate a fresh authorization link and return immediately.")
    mode.add_argument("--complete", action="store_true", help="Check the pending code after the user approves the link.")
    mode.add_argument("--status", action="store_true", help="Check local authorization state without displaying credentials.")
    args = parser.parse_args()

    try:
        if args.status:
            print_json(authorization_status())
            return 0

        if args.complete:
            result = complete_authorization()
            print_json(result)
            return 0 if result.get("status") == "authorized" else 3

        print_json(start_authorization())
        return 0
    except AidsoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
