#!/usr/bin/env python3
import argparse
import json
import urllib.parse
import urllib.request

HOST = "cryptexai-buy-sell-signals.p.rapidapi.com"
BASE = f"https://{HOST}"


def call(path: str, api_key: str):
    req = urllib.request.Request(
        f"{BASE}{path}",
        headers={
            "X-RapidAPI-Host": HOST,
            "X-RapidAPI-Key": api_key,
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", required=True)
    ap.add_argument("--symbols", action="store_true", help="Fetch symbol list")
    ap.add_argument("--signal", metavar="SYMBOL", help="Fetch signals for one symbol")
    args = ap.parse_args()

    if args.symbols:
        print(json.dumps(call("/getSymbols", args.api_key), indent=2, ensure_ascii=False))
        return

    if args.signal:
        q = urllib.parse.urlencode({"symbol": args.signal})
        print(json.dumps(call(f"/getSignalsForSymbol?{q}", args.api_key), indent=2, ensure_ascii=False))
        return

    ap.error("Use --symbols or --signal <SYMBOL>")


if __name__ == "__main__":
    main()
