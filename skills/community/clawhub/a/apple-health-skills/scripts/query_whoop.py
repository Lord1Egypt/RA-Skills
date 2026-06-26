#!/usr/bin/env python3
"""Query Whoop data from the local SQLite database.

Usage
-----
    python scripts/query_whoop.py [--window-days 7] [--db db/health.db]

Outputs JSON consumed by the OpenClaw whoop-query skill.
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
    parser = argparse.ArgumentParser(description="Query Whoop data from local SQLite")
    parser.add_argument(
        "--db",
        default=os.environ.get("AHB_DB_PATH", "db/health.db"),
        help="Path to SQLite database",
    )
    parser.add_argument(
        "--user-id",
        default=os.environ.get("AHB_USER_ID", ""),
        help="User identifier (default: AHB_USER_ID)",
    )
    parser.add_argument(
        "--window-days",
        type=int,
        default=7,
        help="How many days of data to include (default: 7)",
    )
    return parser.parse_args()


def _safe_mean(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 3) if values else None


def _safe_median(values: list[float]) -> float | None:
    return round(statistics.median(values), 3) if values else None


def _ts_to_iso(ts: int | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def main() -> None:
    args = parse_args()
    if not args.user_id:
        raise SystemExit(
            "ERROR: --user-id is required (or set AHB_USER_ID in .env / environment)."
        )

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    now = int(time.time())
    since = now - args.window_days * 86400

    # ── Recoveries ────────────────────────────────────────────────────────────
    recovery_rows = conn.execute(
        """
        SELECT ts, recovery_score, resting_heart_rate, hrv_rmssd_milli,
               spo2_percentage, skin_temp_celsius
        FROM whoop_recoveries
        WHERE user_id = ? AND ts >= ?
        ORDER BY ts DESC
        """,
        (args.user_id, since),
    ).fetchall()

    recoveries = [dict(row) for row in recovery_rows]
    for r in recoveries:
        r["date"] = _ts_to_iso(r["ts"])

    recovery_scores = [r["recovery_score"] for r in recoveries if r["recovery_score"] is not None]
    hrv_values = [r["hrv_rmssd_milli"] for r in recoveries if r["hrv_rmssd_milli"] is not None]
    rhr_values = [r["resting_heart_rate"] for r in recoveries if r["resting_heart_rate"] is not None]

    recovery_features = {
        "avg_recovery_score": _safe_mean(recovery_scores),
        "latest_recovery_score": recovery_scores[0] if recovery_scores else None,
        "avg_hrv_rmssd": _safe_mean(hrv_values),
        "latest_hrv_rmssd": hrv_values[0] if hrv_values else None,
        "avg_resting_hr": _safe_mean(rhr_values),
        "latest_resting_hr": rhr_values[0] if rhr_values else None,
        "samples": len(recoveries),
    }

    # ── Sleeps ────────────────────────────────────────────────────────────────
    sleep_rows = conn.execute(
        """
        SELECT id, start_ts, end_ts, nap, performance_percentage,
               respiratory_rate, total_in_bed_minutes, total_sleep_minutes,
               stage_sws_minutes, stage_rem_minutes, stage_wake_minutes
        FROM whoop_sleeps
        WHERE user_id = ? AND start_ts >= ? AND nap = 0
        ORDER BY start_ts DESC
        """,
        (args.user_id, since),
    ).fetchall()

    sleeps = []
    for row in sleep_rows:
        d = dict(row)
        d["start_date"] = _ts_to_iso(d["start_ts"])
        d["end_date"] = _ts_to_iso(d["end_ts"])
        if d["total_in_bed_minutes"] and d["total_sleep_minutes"]:
            d["sleep_efficiency"] = round(d["total_sleep_minutes"] / d["total_in_bed_minutes"], 3)
        else:
            d["sleep_efficiency"] = None
        sleeps.append(d)

    perf_values = [s["performance_percentage"] for s in sleeps if s["performance_percentage"] is not None]
    sleep_mins = [s["total_sleep_minutes"] for s in sleeps if s["total_sleep_minutes"] is not None]
    sws_mins = [s["stage_sws_minutes"] for s in sleeps if s["stage_sws_minutes"] is not None]
    rem_mins = [s["stage_rem_minutes"] for s in sleeps if s["stage_rem_minutes"] is not None]
    resp_values = [s["respiratory_rate"] for s in sleeps if s["respiratory_rate"] is not None]

    sleep_features = {
        "avg_performance_pct": _safe_mean(perf_values),
        "latest_performance_pct": perf_values[0] if perf_values else None,
        "avg_total_sleep_minutes": _safe_mean(sleep_mins),
        "avg_sws_minutes": _safe_mean(sws_mins),
        "avg_rem_minutes": _safe_mean(rem_mins),
        "avg_respiratory_rate": _safe_mean(resp_values),
        "nights": len(sleeps),
    }

    # ── Cycles (daily strain) ─────────────────────────────────────────────────
    cycle_rows = conn.execute(
        """
        SELECT id, start_ts, end_ts, strain, kilojoule,
               average_heart_rate, max_heart_rate
        FROM whoop_cycles
        WHERE user_id = ? AND start_ts >= ?
        ORDER BY start_ts DESC
        """,
        (args.user_id, since),
    ).fetchall()

    cycles = []
    for row in cycle_rows:
        d = dict(row)
        d["date"] = _ts_to_iso(d["start_ts"])
        cycles.append(d)

    strain_values = [c["strain"] for c in cycles if c["strain"] is not None]
    strain_features = {
        "avg_strain": _safe_mean(strain_values),
        "latest_strain": strain_values[0] if strain_values else None,
        "max_strain": max(strain_values) if strain_values else None,
        "days": len(cycles),
    }

    # ── Workouts ──────────────────────────────────────────────────────────────
    workout_rows = conn.execute(
        """
        SELECT id, start_ts, end_ts, sport_name, strain, average_heart_rate,
               max_heart_rate, kilojoule,
               zone_zero_minutes, zone_one_minutes, zone_two_minutes,
               zone_three_minutes, zone_four_minutes, zone_five_minutes
        FROM whoop_workouts
        WHERE user_id = ? AND start_ts >= ?
        ORDER BY start_ts DESC
        """,
        (args.user_id, since),
    ).fetchall()

    workouts = []
    for row in workout_rows:
        d = dict(row)
        d["start_date"] = _ts_to_iso(d["start_ts"])
        d["end_date"] = _ts_to_iso(d["end_ts"])
        workouts.append(d)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_id": args.user_id,
        "window_days": args.window_days,
        "recoveries": recoveries,
        "sleeps": sleeps,
        "cycles": cycles,
        "workouts": workouts,
        "features": {
            "recovery": recovery_features,
            "sleep": sleep_features,
            "strain": strain_features,
        },
    }

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
