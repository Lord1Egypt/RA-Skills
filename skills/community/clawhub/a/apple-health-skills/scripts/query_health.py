#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import sqlite3
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    """Parse a simple KEY=VALUE .env file and set missing env vars."""
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


# Load .env from repo root so the script works without manually exporting vars.
_repo_root = Path(__file__).resolve().parent.parent
_load_dotenv(_repo_root / ".env")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query Apple Health Bridge SQLite data")
    parser.add_argument(
        "--db",
        default=os.environ.get("AHB_DB_PATH", "db/health.db"),
        help="Path to SQLite database (default: AHB_DB_PATH env or db/health.db)",
    )
    parser.add_argument(
        "--user-id",
        default=os.environ.get("AHB_USER_ID", ""),
        help="User identifier (default: AHB_USER_ID env var)",
    )
    parser.add_argument("--types", default="heart_rate,glucose,sleep_stage")
    parser.add_argument("--window-hours", type=int, default=24)
    parser.add_argument("--sleep-nights", type=int, default=7)
    parser.add_argument(
        "--include-features",
        action="store_true",
        default=True,
        help="Include daily and rolling feature summaries (default: true)",
    )
    return parser.parse_args()


def _safe_mean(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 3) if values else None


def _safe_median(values: list[float]) -> float | None:
    return round(statistics.median(values), 3) if values else None


def _safe_stddev(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    return round(statistics.pstdev(values), 3)


def _build_sleep_features(sleep_rows: list[sqlite3.Row], now_ts: int) -> dict[str, object]:
    nights: dict[str, dict[str, object]] = {}
    for row in sleep_rows:
        start_ts = int(row["start_ts"])
        end_ts = int(row["end_ts"])
        date_key = datetime.fromtimestamp(start_ts, tz=timezone.utc).date().isoformat()
        night = nights.setdefault(
            date_key,
            {
                "night": date_key,
                "time_in_bed_minutes": 0,
                "total_sleep_minutes": 0,
                "stage_minutes": {"deep": 0, "rem": 0, "core": 0, "other": 0},
                "start_ts": start_ts,
                "end_ts": end_ts,
            },
        )
        minutes = max(0, (end_ts - start_ts) / 60)
        night["time_in_bed_minutes"] += minutes
        category = str(row["category"])
        if category.startswith("asleep"):
            night["total_sleep_minutes"] += minutes
            if category == "asleepDeep":
                night["stage_minutes"]["deep"] += minutes
            elif category == "asleepREM":
                night["stage_minutes"]["rem"] += minutes
            elif category in {"asleepCore", "asleepUnspecified"}:
                night["stage_minutes"]["core"] += minutes
            else:
                night["stage_minutes"]["other"] += minutes
        night["start_ts"] = min(int(night["start_ts"]), start_ts)
        night["end_ts"] = max(int(night["end_ts"]), end_ts)

    nightly = sorted(nights.values(), key=lambda item: item["night"], reverse=True)
    for night in nightly:
        tib = float(night["time_in_bed_minutes"])
        asleep = float(night["total_sleep_minutes"])
        night["time_in_bed_minutes"] = round(tib, 2)
        night["total_sleep_minutes"] = round(asleep, 2)
        night["sleep_efficiency"] = round((asleep / tib), 3) if tib > 0 else None
        for stage, value in night["stage_minutes"].items():
            night["stage_minutes"][stage] = round(float(value), 2)

    bedtimes = [int(n["start_ts"]) % 86400 for n in nightly]
    waketimes = [int(n["end_ts"]) % 86400 for n in nightly]
    sleep_consistency = {
        "bedtime_variance_minutes": round(math.sqrt(statistics.pvariance(bedtimes)) / 60, 2)
        if len(bedtimes) > 1
        else None,
        "waketime_variance_minutes": round(math.sqrt(statistics.pvariance(waketimes)) / 60, 2)
        if len(waketimes) > 1
        else None,
    }

    return {
        "recent_nights": nightly,
        "rolling": {
            "avg_total_sleep_minutes": _safe_mean([float(n["total_sleep_minutes"]) for n in nightly]),
            "avg_time_in_bed_minutes": _safe_mean([float(n["time_in_bed_minutes"]) for n in nightly]),
            "avg_sleep_efficiency": _safe_mean(
                [float(n["sleep_efficiency"]) for n in nightly if n["sleep_efficiency"] is not None]
            ),
            "sleep_consistency": sleep_consistency,
            "window_end_ts": now_ts,
        },
    }


def _build_heart_features(heart_rows: list[sqlite3.Row], hrv_rows: list[sqlite3.Row]) -> dict[str, object]:
    hr_values = [float(row["value"]) for row in heart_rows]
    resting_rows = [float(row["value"]) for row in heart_rows if str(row["type"]) == "resting_heart_rate"]
    hrv_values = [float(row["value"]) for row in hrv_rows]
    return {
        "median_hr": _safe_median(hr_values),
        "avg_hr": _safe_mean(hr_values),
        "resting_hr_avg": _safe_mean(resting_rows),
        "resting_hr_latest": resting_rows[0] if resting_rows else None,
        "hrv_avg": _safe_mean(hrv_values),
        "hrv_latest": hrv_values[0] if hrv_values else None,
        "samples": len(hr_values),
        "hrv_samples": len(hrv_values),
    }


def _build_glucose_features(glucose_rows: list[sqlite3.Row]) -> dict[str, object]:
    values = [float(row["value"]) for row in glucose_rows]
    overnight = [
        float(row["value"])
        for row in glucose_rows
        if datetime.fromtimestamp(int(row["ts"]), tz=timezone.utc).hour < 6
    ]
    low, high = 70.0, 180.0
    in_range = [v for v in values if low <= v <= high]
    spikes = [v for v in values if v > high]
    return {
        "mean": _safe_mean(values),
        "variability_stddev": _safe_stddev(values),
        "time_in_range_pct": round((len(in_range) / len(values)) * 100, 2) if values else None,
        "spike_count": len(spikes),
        "overnight_baseline_estimate": _safe_median(overnight),
        "samples": len(values),
        "target_range_mg_dL": [low, high],
    }


def main() -> None:
    args = parse_args()

    if not args.user_id:
        raise SystemExit(
            "ERROR: --user-id is required (or set AHB_USER_ID in .env / environment)."
        )

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    now = int(time.time())
    since = now - args.window_hours * 3600
    types = [t.strip() for t in args.types.split(",") if t.strip()]

    out: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_id": args.user_id,
        "window_hours": args.window_hours,
        "quantity": {},
        "sleep": [],
        "features": {},
    }

    for metric in types:
        rows = conn.execute(
            """
            SELECT ts, value, unit, source, device
            FROM quantity_samples
            WHERE user_id = ? AND type = ? AND ts >= ?
            ORDER BY ts DESC
            LIMIT 500
            """,
            (args.user_id, metric, since),
        ).fetchall()
        if rows:
            out["quantity"][metric] = [dict(row) for row in rows]

    sleep_since = now - args.sleep_nights * 86400
    sleep_rows = conn.execute(
        """
        SELECT start_ts, end_ts, category, source, device
        FROM category_samples
        WHERE user_id = ? AND type = 'sleep_stage' AND start_ts >= ?
        ORDER BY start_ts DESC
        LIMIT 1000
        """,
        (args.user_id, sleep_since),
    ).fetchall()
    out["sleep"] = [dict(row) for row in sleep_rows]

    if args.include_features:
        heart_rows = conn.execute(
            """
            SELECT ts, value, unit, source, device, type
            FROM quantity_samples
            WHERE user_id = ? AND type IN ('heart_rate', 'resting_heart_rate') AND ts >= ?
            ORDER BY ts DESC
            LIMIT 1000
            """,
            (args.user_id, since),
        ).fetchall()
        hrv_rows = conn.execute(
            """
            SELECT ts, value, unit, source, device, type
            FROM quantity_samples
            WHERE user_id = ? AND type = 'hrv' AND ts >= ?
            ORDER BY ts DESC
            LIMIT 1000
            """,
            (args.user_id, since),
        ).fetchall()
        glucose_rows = conn.execute(
            """
            SELECT ts, value, unit, source, device, type
            FROM quantity_samples
            WHERE user_id = ? AND type = 'glucose' AND ts >= ?
            ORDER BY ts DESC
            LIMIT 1000
            """,
            (args.user_id, since),
        ).fetchall()
        out["features"] = {
            "sleep": _build_sleep_features(sleep_rows, now),
            "heart": _build_heart_features(heart_rows, hrv_rows),
            "glucose": _build_glucose_features(glucose_rows),
        }

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
