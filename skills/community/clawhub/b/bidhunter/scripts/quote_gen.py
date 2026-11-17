#!/usr/bin/env python3
"""
quote_gen.py - Generate quote draft CSV from qualified announcements.
Only processes investable items.

Usage:
  python3 quote_gen.py <qual_file.jsonl> <date> <output_dir>
"""

import json
import sys
import os
import csv


def load_results(path):
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return results


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 quote_gen.py <qual_file.jsonl> <date> <output_dir>", file=sys.stderr)
        sys.exit(1)

    qual_path = sys.argv[1]
    date_str = sys.argv[2]
    output_dir = sys.argv[3]

    os.makedirs(output_dir, exist_ok=True)
    results = load_results(qual_path)

    investable = [r for r in results if r.get("verdict") == "investable"]

    if not investable:
        print("No investable items to generate quotes for.", file=sys.stderr)
        return

    output_file = os.path.join(output_dir, f"quote_draft_{date_str}.csv")

    with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "seq", "bid_id", "title", "source", "url",
            "publish_time", "assigned_entity", "matched_capabilities",
            "region", "is_priority", "quote_item", "unit", "qty",
            "unit_price", "total_price", "remark"
        ])

        for i, item in enumerate(investable, 1):
            caps = ", ".join(item.get("matched_capabilities", []))
            region_info = item.get("region_info", {})
            writer.writerow([
                i,
                item.get("id", ""),
                item.get("title", ""),
                item.get("source", ""),
                item.get("url", ""),
                item.get("publish_time", ""),
                item.get("assigned_entity", ""),
                caps,
                region_info.get("region", ""),
                "Y" if region_info.get("is_priority", False) else "",
                "", "", "", "", "",  # quote fields left blank for user to fill
                item.get("reason", "")
            ])

    print(f"Quote draft saved to: {output_file} ({len(investable)} items)", file=sys.stderr)


if __name__ == "__main__":
    main()
