#!/usr/bin/env python3
"""Query locally stored CLS snapshot history."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from storage import dedupe_by_id_keep_latest, load_snapshots

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


def main():
    parser = argparse.ArgumentParser(description="Query local CLS snapshot history")
    parser.add_argument("query_type", choices=["telegraph", "red", "hot"])
    parser.add_argument("--hours", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--min-reading", type=int, default=10000)
    args = parser.parse_args()

    rows = dedupe_by_id_keep_latest(load_snapshots())
    cutoff = int((datetime.now(SHANGHAI_TZ) - timedelta(hours=args.hours)).timestamp())
    rows = [row for row in rows if int(row.get("ctime") or 0) >= cutoff]

    if args.query_type == "red":
        rows = [row for row in rows if row.get("level") in {"A", "B"}]
    elif args.query_type == "hot":
        rows = [row for row in rows if int(row.get("reading_num") or 0) >= args.min_reading]
        rows = sorted(rows, key=lambda x: int(x.get("reading_num") or 0), reverse=True)

    rows = rows[: args.limit]
    print(json.dumps({"query_type": args.query_type, "count": len(rows), "items": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
