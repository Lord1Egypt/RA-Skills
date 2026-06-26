#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from market_data import fetch_tencent_quotes, format_markdown_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch Tencent quote snapshots for A-share watchlists.")
    parser.add_argument("symbols", nargs="+", help="Symbols such as sz300502 sh688981 sh600938")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    quotes = fetch_tencent_quotes(args.symbols)

    if args.format == "json":
        print(json.dumps(quotes, ensure_ascii=False, indent=2))
        return

    columns = [
        ("Name", "name"),
        ("Code", "code"),
        ("Price", "price"),
        ("Chg%", "change_pct"),
        ("High", "high"),
        ("Low", "low"),
        ("Amount(100m)", "amount_100m"),
    ]
    print(format_markdown_table(quotes, columns))


if __name__ == "__main__":
    main()
