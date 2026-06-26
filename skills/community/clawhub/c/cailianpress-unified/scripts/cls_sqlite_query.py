#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time

from db import get_connection


def main():
    parser = argparse.ArgumentParser(description="Query CLS SQLite main view")
    parser.add_argument("query_type", choices=["telegraph", "red", "hot"])
    parser.add_argument("--hours", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--min-reading", type=int, default=10000)
    args = parser.parse_args()

    cutoff = int(time.time()) - args.hours * 3600
    where = ["ctime >= ?"]
    params = [cutoff]
    order_by = "ctime DESC"

    if args.query_type == "red":
        where.append("level IN ('A','B')")
    elif args.query_type == "hot":
        where.append("reading_num >= ?")
        params.append(args.min_reading)
        order_by = "reading_num DESC, ctime DESC"

    sql = f"""
        SELECT id, title, brief, content, level, is_red, telegraph_type, reading_num,
               ctime, modified_time, published_at, shareurl, category, type, sort_score,
               recommend, confirmed, jpush, share_num, comment_num, audio_url,
               first_seen_at, last_seen_at, seen_count, date_key, raw_json
        FROM v_telegraph_main
        WHERE {' AND '.join(where)}
        ORDER BY {order_by}
        LIMIT ?
    """
    params.append(args.limit)

    conn = get_connection()
    try:
        rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
        print(json.dumps({"query_type": args.query_type, "count": len(rows), "items": rows}, ensure_ascii=False, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
