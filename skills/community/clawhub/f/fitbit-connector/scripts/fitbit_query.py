#!/usr/bin/env python3
import argparse
import json
import sqlite3
from datetime import date

from _fitbit_common import get_config


def _fetch_day(conn, day: str):
    conn.row_factory = sqlite3.Row
    return conn.execute("SELECT * FROM daily_metrics WHERE date=?", (day,)).fetchone()


def _fetch_trend(conn, days: int):
    conn.row_factory = sqlite3.Row
    return conn.execute(
        """
        SELECT date, hrv_rmssd, readiness_state, readiness_confidence, data_quality
        FROM daily_metrics
        WHERE hrv_rmssd IS NOT NULL
        ORDER BY date DESC
        LIMIT ?
        """,
        (days,),
    ).fetchall()


def ask_day(conn, day: str, intent: str):
    row = _fetch_day(conn, day)
    if not row:
        print(json.dumps({"date": day, "intent": intent, "status": "no_data"}, separators=(",", ":")))
        return

    d = dict(row)
    reasons = json.loads(d.get("reasons_json") or "[]")
    base = {
        "date": d["date"],
        "readiness": d["readiness_state"],
        "confidence": d["readiness_confidence"],
        "rec": d["pp_recommendation"],
        "quality": d.get("data_quality", "unknown"),
    }

    if intent == "readiness":
        out = {**base, "reasons": reasons}
    elif intent == "sleep":
        out = {
            **base,
            "sleep_min": d.get("sleep_minutes"),
            "sleep_eff": d.get("sleep_efficiency"),
            "sleep_score": d.get("sleep_score"),
        }
    elif intent == "fatigue":
        out = {
            **base,
            "rhr": d.get("resting_hr"),
            "hrv": d.get("hrv_rmssd"),
            "azm": d.get("active_zone_minutes"),
        }
    else:
        out = {
            **base,
            "steps": d.get("steps"),
            "distance_km": d.get("distance_km"),
            "calories_out": d.get("calories_out"),
            "floors": d.get("floors"),
        }

    print(json.dumps(out, separators=(",", ":")))


def ask_hrv_trend(conn, days: int):
    rows = [dict(r) for r in _fetch_trend(conn, days)]
    if not rows:
        print(json.dumps({"intent": "hrv-trend", "days": days, "status": "no_data"}, separators=(",", ":")))
        return

    # rows are DESC by date
    hrv_vals = [r["hrv_rmssd"] for r in rows if r.get("hrv_rmssd") is not None]
    first = hrv_vals[-1] if len(hrv_vals) >= 2 else hrv_vals[0]
    last = hrv_vals[0]
    delta = round(last - first, 2)

    if delta >= 3:
        direction = "up"
    elif delta <= -3:
        direction = "down"
    else:
        direction = "flat"

    avg = round(sum(hrv_vals) / len(hrv_vals), 2)
    out = {
        "intent": "hrv-trend",
        "days": days,
        "samples": len(rows),
        "direction": direction,
        "delta": delta,
        "avg": avg,
        "latest": {
            "date": rows[0]["date"],
            "hrv": rows[0]["hrv_rmssd"],
            "readiness": rows[0]["readiness_state"],
            "confidence": rows[0]["readiness_confidence"],
            "quality": rows[0]["data_quality"],
        },
        "series": [{"date": r["date"], "hrv": r["hrv_rmssd"], "quality": r["data_quality"]} for r in rows],
    }
    print(json.dumps(out, separators=(",", ":")))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=False, default=date.today().isoformat())
    p.add_argument(
        "--intent",
        required=False,
        default="readiness",
        choices=["readiness", "sleep", "fatigue", "activity", "hrv-trend"],
    )
    p.add_argument("--days", type=int, default=5)
    args = p.parse_args()

    cfg = get_config()
    conn = sqlite3.connect(cfg.db_path)

    if args.intent == "hrv-trend":
        ask_hrv_trend(conn, args.days)
    else:
        ask_day(conn, args.date, args.intent)


if __name__ == "__main__":
    main()
