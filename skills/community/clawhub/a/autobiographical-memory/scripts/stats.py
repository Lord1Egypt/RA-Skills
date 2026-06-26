#!/usr/bin/env python3
"""
Memory stats: show sizes, dates, coverage, and health of your memory files.

Usage:
    python3 stats.py [--memory-dir DIR]
"""

import argparse
import os
import re
import sys
from datetime import datetime, date
from pathlib import Path


def gather_stats(memory_dir: Path) -> dict:
    """Gather statistics from memory files."""
    stats = {
        "daily_files": [],
        "total_daily_size": 0,
        "memories_file": None,
        "memories_size": 0,
        "gaps": [],
        "monthly_counts": {},
    }

    for f in sorted(memory_dir.glob("*.md")):
        m = re.match(r"(\d{4}-\d{2})", f.stem)
        if f.stem == "README":
            continue
        if m:
            month_key = m.group(1)
            stats["monthly_counts"].setdefault(month_key, 0)
            stats["monthly_counts"][month_key] += 1
        # Check if it's a daily note (date format)
        dm = re.match(r"(\d{4}-\d{2}-\d{2})", f.stem)
        if dm:
            fdate = dm.group(1)
            fsize = f.stat().st_size
            stats["daily_files"].append({"date": fdate, "size": fsize, "path": f.name})
            stats["total_daily_size"] += fsize
            continue

        # MEMORY.md, USER.md, etc.
        if f.stem == "MEMORY":
            stats["memories_file"] = f
            stats["memories_size"] = f.stat().st_size

    return stats


def find_gaps(daily_files: list[dict]) -> list[str]:
    """Find notable gaps (>3 days) in daily note coverage."""
    if not daily_files:
        return []
    dates = sorted([d["date"] for d in daily_files])
    gaps = []
    for i in range(len(dates) - 1):
        d1 = date.fromisoformat(dates[i])
        d2 = date.fromisoformat(dates[i + 1])
        gap_days = (d2 - d1).days
        if gap_days > 3:
            gaps.append(f"{dates[i]} → {dates[i+1]} ({gap_days - 1} days missing)")
    return gaps


def print_report(stats: dict):
    """Print a formatted stats report."""
    print("=" * 50)
    print("📊 MEMORY STATS")
    print("=" * 50)

    # MEMORY.md
    if stats["memories_file"]:
        size_kb = stats["memories_size"] / 1024
        print(f"\n📝 MEMORY.md: {size_kb:.1f} KB")
    else:
        print("\n⚠️  MEMORY.md not found in this directory")

    # Daily notes
    daily = stats["daily_files"]
    print(f"\n📅 Daily note files: {len(daily)}")
    total_kb = stats["total_daily_size"] / 1024
    print(f"   Total size: {total_kb:.1f} KB")

    if daily:
        sizes = [d["size"] for d in daily]
        print(f"   Avg file size: {sum(sizes)/len(sizes)/1024:.1f} KB")
        print(f"   Largest: {max(sizes)/1024:.1f} KB ({max(daily, key=lambda x: x['size'])['path']})")

    # Monthly breakdown
    monthly = stats["monthly_counts"]
    if monthly:
        print(f"\n📆 Monthly coverage:")
        for month in sorted(monthly.keys()):
            count = monthly[month]
            bar = "█" * min(count, 20)
            print(f"   {month}: {count:2d} days {bar}")

    # Gaps
    gaps = stats.get("gaps", [])
    if gaps:
        print(f"\n⚠️  Notable gaps (>3 days):")
        for g in gaps:
            print(f"   {g}")
    else:
        print(f"\n✅ No significant gaps detected")

    # Coverage period
    if daily:
        dates = sorted([d["date"] for d in daily])
        print(f"\n📆 Coverage: {dates[0]} → {dates[-1]}")
        coverage_days = len(daily)
        total_days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days + 1
        pct = (coverage_days / total_days) * 100 if total_days > 0 else 0
        print(f"   Density: {coverage_days}/{total_days} days ({pct:.0f}%)")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Memory file statistics")
    parser.add_argument(
        "--memory-dir",
        type=str,
        default=None,
        help="Path to memory directory (default: <workspace>/memory)",
    )
    args = parser.parse_args()

    if args.memory_dir:
        memory_dir = Path(args.memory_dir)
    else:
        candidates = [
            Path.cwd() / "memory",
            Path.home() / ".openclaw" / "workspace" / "memory",
        ]
        memory_dir = None
        for c in candidates:
            if c.exists() and c.is_dir():
                memory_dir = c
                break

    if not memory_dir or not memory_dir.exists():
        print("Error: Could not find memory directory.", file=sys.stderr)
        print("Specify with --memory-dir or run from your workspace.", file=sys.stderr)
        sys.exit(1)

    stats = gather_stats(memory_dir)
    stats["gaps"] = find_gaps(stats["daily_files"])
    print_report(stats)


if __name__ == "__main__":
    main()
