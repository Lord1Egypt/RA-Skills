#!/usr/bin/env python3
from __future__ import annotations

import json
from db import get_connection


def main():
    conn = get_connection()
    try:
        stats = {
            "telegraph_raw_main": conn.execute("SELECT COUNT(*) FROM telegraph_raw_main").fetchone()[0],
            "telegraph_raw_log": conn.execute("SELECT COUNT(*) FROM telegraph_raw_log").fetchone()[0],
            "telegraph_subjects": conn.execute("SELECT COUNT(*) FROM telegraph_subjects").fetchone()[0],
            "telegraph_stocks": conn.execute("SELECT COUNT(*) FROM telegraph_stocks").fetchone()[0],
            "telegraph_plates": conn.execute("SELECT COUNT(*) FROM telegraph_plates").fetchone()[0],
            "latest_ctime": conn.execute("SELECT MAX(ctime) FROM telegraph_raw_main").fetchone()[0],
            "latest_seen_at": conn.execute("SELECT MAX(last_seen_at) FROM telegraph_raw_main").fetchone()[0],
            "red_count": conn.execute("SELECT COUNT(*) FROM v_telegraph_main WHERE level IN ('A','B')").fetchone()[0],
        }
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    finally:
        conn.close()


if __name__ == '__main__':
    main()
