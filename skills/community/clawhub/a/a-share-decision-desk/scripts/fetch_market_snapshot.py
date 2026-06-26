#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from market_data import fetch_index_snapshot, fetch_sector_movers, format_markdown_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch A-share index and sector breadth snapshots.")
    parser.add_argument("--limit", type=int, default=10, help="Number of top and bottom sectors to return.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    indices = fetch_index_snapshot()
    leaders = fetch_sector_movers(limit=args.limit, rising=True)
    laggards = fetch_sector_movers(limit=args.limit, rising=False)

    if args.format == "json":
        payload = {"indices": indices, "leaders": leaders, "laggards": laggards}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print("## Indices")
    print(
        format_markdown_table(
            indices,
            [
                ("Name", "name"),
                ("Price", "price"),
                ("Chg%", "change_pct"),
                ("Up", "up_count"),
                ("Down", "down_count"),
            ],
        )
    )
    print("\n## Top Sectors")
    print(
        format_markdown_table(
            leaders,
            [
                ("Sector", "name"),
                ("Chg%", "change_pct"),
                ("Leader", "leader"),
                ("Up", "up_count"),
                ("Down", "down_count"),
            ],
        )
    )
    print("\n## Bottom Sectors")
    print(
        format_markdown_table(
            laggards,
            [
                ("Sector", "name"),
                ("Chg%", "change_pct"),
                ("Leader", "leader"),
                ("Up", "up_count"),
                ("Down", "down_count"),
            ],
        )
    )


if __name__ == "__main__":
    main()
