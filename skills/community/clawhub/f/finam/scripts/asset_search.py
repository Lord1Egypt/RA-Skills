#!/usr/bin/env python3
"""Search Finam instruments by ticker glob pattern or name substring."""

import argparse
import fnmatch
import sys
import urllib.parse

import httpx

import utils
from utils import BASE_URL, dprint, get_token


VALID_TYPES = {"EQUITIES", "FUTURES", "BONDS", "FUNDS", "SPREADS", "OTHER", "CURRENCIES", "OPTIONS", "SWAPS", "INDICES"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Search Finam instruments by ticker glob pattern and/or name substring.",
        epilog=(
            "examples:\n"
            "  asset_search.py 'SBER*'\n"
            "  asset_search.py 'NG*' --type FUTURES --active false\n"
            "  asset_search.py --name 'natural gas' --type FUTURES\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pattern", nargs="?", help="glob pattern matched against ticker and symbol (e.g. 'SBER*', 'NG*')")
    parser.add_argument("--name", metavar="QUERY", help="case-insensitive substring search on instrument name")
    parser.add_argument("--type", metavar="TYPE", choices=VALID_TYPES, type=str.upper, help=f"filter by type: {', '.join(sorted(VALID_TYPES))}")
    parser.add_argument("--active", metavar="true|false", default="true", choices=("true", "false"), help="include archived instruments (default: true)")
    parser.add_argument("--max", metavar="N", type=int, default=30_000, help="max assets to fetch via /assets/all when --active false (default: 30000)")
    parser.add_argument("--debug", action="store_true", help="verbose output")

    args = parser.parse_args()

    if args.pattern is None and args.name is None:
        parser.error("at least one of pattern or --name is required")

    if args.debug:
        utils.DEBUG = True

    return args.pattern, args.name.lower() if args.name else None, args.type, args.active == "true", args.max


def fetch_assets(token):
    url = f"{BASE_URL}/assets"
    try:
        with httpx.Client(http2=True) as client:
            resp = client.get(url, headers={"Authorization": token})
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        print(f"Error: HTTP {e.response.status_code} fetching assets", file=sys.stderr)
        sys.exit(1)
    assets = data.get("assets") or []
    dprint(f"  Fetched {len(assets)} assets")
    return assets


def fetch_assets_all(token, only_active, max_assets):
    assets = []
    cursor = ""
    with httpx.Client(http2=True) as client:
        while True:
            params = {"only_active": "true" if only_active else "false"}
            if cursor:
                params["cursor"] = cursor
            url = f"{BASE_URL}/assets/all?" + urllib.parse.urlencode(params)
            try:
                resp = client.get(url, headers={"Authorization": token})
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPStatusError as e:
                print(f"Error: HTTP {e.response.status_code} fetching assets", file=sys.stderr)
                sys.exit(1)

            batch = data.get("assets") or []
            assets.extend(batch)
            dprint(f"  Fetched {len(batch)} assets (total: {len(assets)})")

            if max_assets and len(assets) >= max_assets:
                assets = assets[:max_assets]
                break

            next_cursor = data.get("next_cursor", "")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor

    return assets


def main():
    pattern, name_query, type_filter, only_active, max_assets = parse_args()

    token = get_token()

    if not only_active:
        dprint(f"Fetching all assets (only_active=false, max={max_assets})...")
        assets = fetch_assets_all(token, only_active=False, max_assets=max_assets)
    else:
        dprint("Fetching active assets...")
        assets = fetch_assets(token)
    dprint(f"Total assets fetched: {len(assets)}")

    matches = []
    for a in assets:
        if type_filter and a.get("type", "").upper() != type_filter:
            continue
        ticker_match = pattern and (
            fnmatch.fnmatch(a.get("ticker", ""), pattern)
            or fnmatch.fnmatch(a.get("symbol", ""), pattern)
        )
        name_match = name_query and name_query in a.get("name", "").lower()
        if pattern and name_query and ticker_match and name_match:
            matches.append(a)
        elif pattern and not name_query and ticker_match:
            matches.append(a)
        elif name_query and not pattern and name_match:
            matches.append(a)

    parts = []
    if pattern:
        parts.append(f"'{pattern}'")
    if name_query:
        parts.append(f"name='{name_query}'")
    if type_filter:
        parts.append(f"type={type_filter}")
    filter_desc = " ".join(parts)

    if not matches:
        print(f"No instruments found matching {filter_desc}.")
        return

    print(f"\nFound {len(matches)} instrument(s) matching {filter_desc}:\n")
    header = f"{'Ticker':<16}{'Symbol':<20}{'MIC':<10}{'Type':<16}{'Name'}"
    print(header)
    print("\u2500" * (len(header) + 20))
    for a in matches:
        archived = " [archived]" if a.get("is_archived") else ""
        print(
            f"{a.get('ticker', ''):<16}"
            f"{a.get('symbol', ''):<20}"
            f"{a.get('mic', ''):<10}"
            f"{a.get('type', ''):<16}"
            f"{a.get('name', '')}{archived}"
        )


if __name__ == "__main__":
    main()