#!/usr/bin/env python3
"""Deterministically count characters for text with a hard limit."""

import argparse
import json
import sys
from typing import Dict, Union


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count characters in the provided text and compare against a limit."
    )
    parser.add_argument(
        "--limit",
        type=int,
        required=True,
        help="Maximum allowed character count.",
    )
    parser.add_argument(
        "--text",
        help="Text to count. If omitted, the script reads from stdin.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the result as a compact JSON object.",
    )
    return parser.parse_args()


def load_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    return sys.stdin.read()


def build_result(text: str, limit: int) -> Dict[str, Union[int, bool]]:
    chars = len(text)
    return {
        "chars": chars,
        "limit": limit,
        "remaining": limit - chars,
        "ok": chars <= limit,
    }


def main() -> int:
    args = parse_args()
    if args.limit < 0:
        print("limit must be non-negative", file=sys.stderr)
        return 2

    text = load_text(args)
    if args.text is None and text == "":
        print("no text provided via --text or stdin", file=sys.stderr)
        return 2

    result = build_result(text, args.limit)

    if args.json:
        print(json.dumps(result, separators=(",", ":")))
    else:
        print(f"chars={result['chars']}")
        print(f"limit={result['limit']}")
        print(f"remaining={result['remaining']}")
        print(f"ok={'true' if result['ok'] else 'false'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
