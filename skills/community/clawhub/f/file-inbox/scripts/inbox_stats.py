#!/usr/bin/env python3
"""
inbox_stats.py — Show inbox statistics.

Usage:
  python3 inbox_stats.py [--inbox DIR]
"""

import argparse
import json
import os
from collections import Counter
from pathlib import Path


def find_workspace_root(start: Path) -> Path:
    current = start.resolve()
    for _ in range(10):
        if (current / "skills").is_dir() or (current / "inbox").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return Path.cwd()


def get_dir_size(path: Path) -> int:
    total = 0
    for f in path.rglob("*"):
        if f.is_file() and f.name != ".meta.json":
            total += f.stat().st_size
    return total


def human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def parse_index_rows(index_path: Path) -> list[dict]:
    if not index_path.exists():
        return []
    rows = []
    in_table = False
    for line in index_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("| ID |"):
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            parts = [p.strip() for p in stripped.strip("|").split("|")]
            if len(parts) >= 7:
                rows.append({
                    "direction": "in" if "in" in parts[1] else "out",
                    "type": parts[3],
                    "tags": parts[4],
                    "date": parts[6],
                })
        elif in_table and stripped and not stripped.startswith("|"):
            in_table = False
    return rows


def main():
    parser = argparse.ArgumentParser(description="Show inbox statistics")
    parser.add_argument("--inbox", default="inbox")
    args = parser.parse_args()

    workspace = find_workspace_root(Path(__file__))
    inbox_root = workspace / args.inbox

    if not inbox_root.exists():
        print("Inbox not initialized. Run init_inbox.sh first.")
        return

    meta_path = inbox_root / ".meta.json"
    index_path = inbox_root / "INDEX.md"

    # Meta stats
    if meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)
    else:
        meta = {"total": 0, "inbound": 0, "outbound": 0, "lastUpdated": "N/A"}

    # Parse index for detailed stats
    rows = parse_index_rows(index_path)

    # Type breakdown
    type_counter = Counter(r["type"] for r in rows)
    tag_counter = Counter()
    for r in rows:
        for tag in r["tags"].split():
            tag = tag.strip()
            if tag:
                tag_counter[tag] += 1

    # Storage size
    inbound_size = get_dir_size(inbox_root / "inbound") if (inbox_root / "inbound").exists() else 0
    outbound_size = get_dir_size(inbox_root / "outbound") if (inbox_root / "outbound").exists() else 0
    total_size = inbound_size + outbound_size

    # Recent activity (last 7 entries)
    recent = rows[:7]

    # Output
    print("=" * 50)
    print("📁 File Inbox Statistics")
    print("=" * 50)
    print(f"Total files:    {meta['total']}")
    print(f"  Inbound:      {meta['inbound']}")
    print(f"  Outbound:     {meta['outbound']}")
    print(f"Last updated:   {meta.get('lastUpdated', 'N/A')}")
    print(f"Storage:        {human_size(total_size)}")
    print(f"  Inbound:      {human_size(inbound_size)}")
    print(f"  Outbound:     {human_size(outbound_size)}")

    if type_counter:
        print(f"\n📊 By File Type:")
        for ftype, count in type_counter.most_common(10):
            print(f"  {ftype:12s}  {count}")

    if tag_counter:
        print(f"\n🏷️  Top Tags:")
        for tag, count in tag_counter.most_common(10):
            print(f"  {tag:16s}  {count}")

    if recent:
        print(f"\n🕐 Recent Activity:")
        for r in recent:
            icon = "⬇️" if r["direction"] == "in" else "⬆️"
            print(f"  {icon} {r['date']}  {r['type']}")

    print()


if __name__ == "__main__":
    main()
