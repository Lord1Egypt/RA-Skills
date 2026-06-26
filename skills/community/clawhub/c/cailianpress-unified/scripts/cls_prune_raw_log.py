#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path

from db import get_connection

RETENTION_DAYS = 30
SECONDS_PER_DAY = 86400


def main() -> None:
    now_ts = int(time.time())
    cutoff_ts = now_ts - RETENTION_DAYS * SECONDS_PER_DAY
    conn = get_connection()
    try:
        before_count = conn.execute("SELECT COUNT(*) FROM telegraph_raw_log").fetchone()[0]
        prune_count = conn.execute(
            "SELECT COUNT(*) FROM telegraph_raw_log WHERE captured_at < ?",
            (cutoff_ts,),
        ).fetchone()[0]
        conn.execute(
            "DELETE FROM telegraph_raw_log WHERE captured_at < ?",
            (cutoff_ts,),
        )
        conn.commit()
        after_count = conn.execute("SELECT COUNT(*) FROM telegraph_raw_log").fetchone()[0]
        print(json.dumps({
            "ok": True,
            "retention_days": RETENTION_DAYS,
            "cutoff_ts": cutoff_ts,
            "before_count": before_count,
            "deleted_count": prune_count,
            "after_count": after_count,
        }, ensure_ascii=False, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
