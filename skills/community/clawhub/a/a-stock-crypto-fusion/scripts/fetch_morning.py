"""CLI helper to fetch morning-brief JSON inputs."""

import sys

sys.dont_write_bytecode = True

import argparse
import json

from fetch_samples import fetch_morning, to_jsonable


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch A-share morning briefing JSON")
    parser.add_argument("--date", help="target date YYYYMMDD (defaults to today)")
    parser.add_argument("--industries", type=int, default=10, help="top N industries")
    parser.add_argument(
        "--limitups", type=int, default=30, help="top N previous limit-ups"
    )
    parser.add_argument("--lhb", type=int, default=20, help="top N institutional LHB")
    parser.add_argument(
        "--breakfast", type=int, default=10, help="top N breakfast items"
    )
    args = parser.parse_args()

    payload = fetch_morning(
        date=args.date,
        top_n_industries=args.industries,
        top_n_limitups=args.limitups,
        top_n_lhb=args.lhb,
        top_n_breakfast=args.breakfast,
    )
    print(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
