#!/usr/bin/env python3
"""Query live heart rate events from the live_events table.

Usage examples:
  python scripts/query_live_hr.py --window-minutes 60
  python scripts/query_live_hr.py --session-id <uuid> --window-minutes 30
  python scripts/query_live_hr.py --device-id A1B2C3D4 --window-minutes 10
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


_repo_root = Path(__file__).resolve().parent.parent
_load_dotenv(_repo_root / ".env")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query live HR events from live_events table")
    parser.add_argument(
        "--db",
        default=os.environ.get("AHB_DB_PATH", "db/health.db"),
        help="Path to SQLite database (default: AHB_DB_PATH env or db/health.db)",
    )
    parser.add_argument(
        "--window-minutes",
        type=int,
        default=60,
        help="How many minutes back to query (default: 60)",
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="Filter to a specific session UUID",
    )
    parser.add_argument(
        "--device-id",
        default=None,
        help="Filter to a specific device ID",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Max number of events to return (default: 500)",
    )
    return parser.parse_args()


def _hr_zone(bpm: float) -> str:
    if bpm < 60:
        return "resting"
    if bpm < 100:
        return "normal"
    if bpm < 140:
        return "elevated"
    return "high"


def main() -> None:
    args = parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    now = int(time.time())
    since = now - args.window_minutes * 60

    # Build query with optional filters
    clauses = ["ts >= ?"]
    params: list[object] = [since]

    if args.session_id:
        clauses.append("session_id = ?")
        params.append(args.session_id)
    if args.device_id:
        clauses.append("device_id = ?")
        params.append(args.device_id)

    where = " AND ".join(clauses)
    sql = f"""
        SELECT session_id, seq, ts, value, unit,
               source_kind, source_vendor, device_id, source_device_name,
               received_at
        FROM live_events
        WHERE {where}
        ORDER BY ts DESC
        LIMIT ?
    """
    params.append(args.limit)

    rows = conn.execute(sql, params).fetchall()

    events = [dict(row) for row in rows]
    values = [float(e["value"]) for e in events]

    # Compute summary stats
    summary: dict[str, object] = {
        "count": len(values),
        "latest_bpm": values[0] if values else None,
        "min_bpm": min(values) if values else None,
        "max_bpm": max(values) if values else None,
        "avg_bpm": round(statistics.fmean(values), 1) if values else None,
        "median_bpm": round(statistics.median(values), 1) if values else None,
        "stddev_bpm": round(statistics.pstdev(values), 2) if len(values) >= 2 else None,
        "latest_zone": _hr_zone(values[0]) if values else None,
        "window_minutes": args.window_minutes,
        "session_id_filter": args.session_id,
        "device_id_filter": args.device_id,
    }

    # Collect unique sessions seen in the window
    sessions_seen = sorted({e["session_id"] for e in events})

    # Build per-session summaries
    session_summaries = []
    for sid in sessions_seen:
        s_events = [e for e in events if e["session_id"] == sid]
        s_values = [float(e["value"]) for e in s_events]
        s_ts = [e["ts"] for e in s_events]
        session_summaries.append({
            "session_id": sid,
            "event_count": len(s_values),
            "start_ts": min(s_ts) if s_ts else None,
            "end_ts": max(s_ts) if s_ts else None,
            "device_name": s_events[0]["source_device_name"] if s_events else None,
            "device_id": s_events[0]["device_id"] if s_events else None,
            "avg_bpm": round(statistics.fmean(s_values), 1) if s_values else None,
            "min_bpm": min(s_values) if s_values else None,
            "max_bpm": max(s_values) if s_values else None,
        })

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "sessions": session_summaries,
        "events": events,
    }

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
