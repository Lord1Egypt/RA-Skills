"""CLI helper to fetch CryptoPanic news JSON."""

import sys

sys.dont_write_bytecode = True

import argparse
import json
import os

from fetch_samples import fetch_cryptopanic, to_jsonable


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch CryptoPanic news JSON for the skill"
    )
    parser.add_argument("--base", default="BTC", help="base symbol, e.g., BTC")
    parser.add_argument("--kind", choices=["news", "media"], default="news")
    parser.add_argument("--limit", type=int, default=5, help="max items")
    parser.add_argument("--token", help="CryptoPanic token (optional if env set)")
    args = parser.parse_args()

    token = args.token or os.getenv("CRYPTOPANIC_TOKEN")
    if not token:
        print(
            json.dumps(
                {
                    "error": "missing CryptoPanic token",
                    "hint": "set CRYPTOPANIC_TOKEN or pass --token",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    try:
        payload = fetch_cryptopanic(token, args.base, kind=args.kind, limit=args.limit)
        print(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(
            json.dumps(
                to_jsonable({"error": str(exc)}),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
