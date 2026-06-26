"""CLI helper to fetch crypto JSON."""

import sys

sys.dont_write_bytecode = True

import argparse
import json

from fetch_samples import fetch_crypto, to_jsonable


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch crypto JSON for the skill")
    parser.add_argument(
        "--symbol", default="BTC/USDT", help="crypto symbol, e.g., BTC/USDT"
    )
    args = parser.parse_args()

    payload = fetch_crypto(args.symbol)
    print(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
