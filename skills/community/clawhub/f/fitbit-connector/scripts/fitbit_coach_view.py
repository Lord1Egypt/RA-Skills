#!/usr/bin/env python3
import argparse
import json
import sqlite3
from datetime import date

from _fitbit_common import get_config


def summary(day: str):
    cfg = get_config()
    conn = sqlite3.connect(cfg.db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM daily_metrics WHERE date=?", (day,)).fetchone()
    if not row:
        print(json.dumps({"date": day, "status": "no_data"}, indent=2))
        return

    flags = conn.execute(
        "SELECT level, flag, message FROM quality_flags WHERE date=? ORDER BY id DESC LIMIT 10", (day,)
    ).fetchall()

    out = dict(row)
    out["reasons_json"] = json.loads(out.get("reasons_json") or "[]")
    out["quality_flags"] = [{"level": f[0], "flag": f[1], "message": f[2]} for f in flags]
    print(json.dumps(out, indent=2))


def trend(days: int):
    cfg = get_config()
    conn = sqlite3.connect(cfg.db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT date, readiness_state, readiness_confidence, pp_recommendation, data_quality,
               sleep_minutes, resting_hr, hrv_rmssd
        FROM daily_metrics
        ORDER BY date DESC
        LIMIT ?
        """,
        (days,),
    ).fetchall()
    print(json.dumps([dict(r) for r in rows], indent=2))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("summary")
    s.add_argument("--date", required=False)
    t = sub.add_parser("trend")
    t.add_argument("--days", type=int, default=7)
    args = p.parse_args()

    if args.cmd == "summary":
        summary(args.date or date.today().isoformat())
    elif args.cmd == "trend":
        trend(args.days)


if __name__ == "__main__":
    main()
