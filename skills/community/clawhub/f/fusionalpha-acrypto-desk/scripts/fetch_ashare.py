"""CLI helper to fetch A-share JSON."""

import sys

sys.dont_write_bytecode = True

import argparse
import json

from fetch_samples import fetch_ashare, to_jsonable


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch A-share JSON for the skill")
    parser.add_argument("--code", default="600519", help="A-share code, e.g., 600519")
    args = parser.parse_args()

    payload = fetch_ashare(args.code)
    print(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
