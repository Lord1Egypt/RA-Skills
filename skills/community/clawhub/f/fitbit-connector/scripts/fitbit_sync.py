#!/usr/bin/env python3
import argparse
import json
from datetime import date, datetime, timedelta, timezone
from statistics import median
from typing import Any, Dict, List

from _fitbit_common import add_quality_flag, db, fitbit_get, get_config


def _get_or_none(dct, *path, default=None):
    cur = dct
    for p in path:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        elif isinstance(cur, list) and isinstance(p, int) and len(cur) > p:
            cur = cur[p]
        else:
            return default
    return cur


def _safe_get(cfg, endpoint, errors):
    try:
        return fitbit_get(cfg, endpoint)
    except Exception as e:
        errors.append({"endpoint": endpoint, "error": str(e)})
        return None


def _first_list_value(payload, list_key: str):
    items = _get_or_none(payload or {}, list_key, default=[])
    if isinstance(items, list) and items:
        first = items[0]
        if isinstance(first, dict):
            return first.get("value")
    return None


def _coerce_int(value, default=0):
    try:
        if value in (None, ""):
            return default
        return int(float(value))
    except Exception:
        return default


def _coerce_float(value, default=0.0):
    try:
        if value in (None, ""):
            return default
        return float(value)
    except Exception:
        return default


def _extract_active_zone_minutes(payload) -> int:
    value = _first_list_value(payload, "activities-active-zone-minutes")
    if isinstance(value, dict):
        return _coerce_int(value.get("activeZoneMinutes"), default=0)
    return _coerce_int(value, default=0)


def _extract_sleep_metrics(payload):
    summary = _get_or_none(payload or {}, "summary", default={}) or {}
    sleep_rows = _get_or_none(payload or {}, "sleep", default=[]) or []
    first_sleep = sleep_rows[0] if isinstance(sleep_rows, list) and sleep_rows else {}
    return (
        summary.get("totalMinutesAsleep"),
        first_sleep.get("efficiency") or summary.get("efficiency"),
        first_sleep.get("sleepScore") or summary.get("sleepScore"),
    )


def _extract_resting_hr(payload):
    return _get_or_none(payload or {}, "activities-heart", 0, "value", "restingHeartRate")


def _extract_hrv(payload):
    hrv_list = _get_or_none(payload or {}, "hrv", default=[])
    if hrv_list:
        return _get_or_none(hrv_list[0], "value", "dailyRmssd")
    return None


def _baseline(conn, metric_col):
    rows = conn.execute(
        f"SELECT {metric_col} FROM daily_metrics WHERE {metric_col} IS NOT NULL ORDER BY date DESC LIMIT 28"
    ).fetchall()
    vals = [r[0] for r in rows if r[0] is not None]
    if len(vals) < 7:
        return None
    return float(median(vals))


def _readiness(resting_hr, hrv, sleep_min, baseline_rhr, baseline_hrv, baseline_sleep):
    reasons = []
    state = "green"

    if sleep_min is not None:
        if baseline_sleep is not None and sleep_min < baseline_sleep - 90:
            state = "red"
            reasons.append("sleep_debt_vs_baseline")
        elif baseline_sleep is not None and sleep_min < baseline_sleep - 45:
            state = "amber" if state == "green" else state
            reasons.append("low_sleep_vs_baseline")
        elif baseline_sleep is None and sleep_min < 360:
            state = "red"
            reasons.append("sleep_debt_absolute")

    if resting_hr is not None:
        if baseline_rhr is not None and resting_hr >= baseline_rhr + 8:
            state = "red"
            reasons.append("elevated_rhr_vs_baseline")
        elif baseline_rhr is not None and resting_hr >= baseline_rhr + 4 and state == "green":
            state = "amber"
            reasons.append("moderate_rhr_vs_baseline")
        elif baseline_rhr is None and resting_hr >= 64:
            state = "red"
            reasons.append("elevated_rhr_absolute")

    if hrv is not None:
        if baseline_hrv is not None and hrv <= baseline_hrv * 0.75:
            state = "red"
            reasons.append("suppressed_hrv_vs_baseline")
        elif baseline_hrv is not None and hrv <= baseline_hrv * 0.9 and state == "green":
            state = "amber"
            reasons.append("moderate_hrv_vs_baseline")
        elif baseline_hrv is None and hrv < 24:
            state = "red"
            reasons.append("suppressed_hrv_absolute")

    available = sum(v is not None for v in [resting_hr, hrv, sleep_min])
    confidence = "high" if available == 3 else "medium" if available == 2 else "low"

    rec = {
        "green": "run_plan",
        "amber": "hold_load_or_reduce_volume",
        "red": "recovery_or_light_technique",
    }[state]
    return state, confidence, reasons, rec


def sync_day(day_str: str, emit_text: bool = True) -> Dict[str, Any]:
    cfg = get_config()
    conn = db(cfg)
    started = datetime.now(timezone.utc).isoformat()
    errors: List[Dict[str, str]] = []

    steps = _safe_get(cfg, f"activities/steps/date/{day_str}/1d.json", errors)
    dist = _safe_get(cfg, f"activities/distance/date/{day_str}/1d.json", errors)
    floors = _safe_get(cfg, f"activities/floors/date/{day_str}/1d.json", errors)
    cals = _safe_get(cfg, f"activities/calories/date/{day_str}/1d.json", errors)
    azm = _safe_get(cfg, f"activities/active-zone-minutes/date/{day_str}/1d.json", errors)
    sleep = _safe_get(cfg, f"sleep/date/{day_str}.json", errors)
    hr = _safe_get(cfg, f"activities/heart/date/{day_str}/1d.json", errors)
    hrv = _safe_get(cfg, f"hrv/date/{day_str}.json", errors)

    steps_v = _coerce_int(_first_list_value(steps, "activities-steps"), default=0)
    dist_v = _coerce_float(_first_list_value(dist, "activities-distance"), default=0.0)
    floors_v = _coerce_int(_first_list_value(floors, "activities-floors"), default=0)
    cals_v = _coerce_int(_first_list_value(cals, "activities-calories"), default=0)
    azm_v = _extract_active_zone_minutes(azm)

    sleep_min, sleep_eff, sleep_score = _extract_sleep_metrics(sleep)

    resting_hr = _extract_resting_hr(hr)
    hrv_v = _extract_hrv(hrv)

    baseline_rhr = _baseline(conn, "resting_hr")
    baseline_hrv = _baseline(conn, "hrv_rmssd")
    baseline_sleep = _baseline(conn, "sleep_minutes")

    state, conf, reasons, rec = _readiness(resting_hr, hrv_v, sleep_min, baseline_rhr, baseline_hrv, baseline_sleep)

    data_quality = "complete" if len(errors) == 0 else "partial"
    if len(errors) >= 4:
        data_quality = "degraded"

    updated_at = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO daily_metrics (
          date, steps, distance_km, calories_out, floors, active_zone_minutes,
          resting_hr, hrv_rmssd, sleep_minutes, sleep_efficiency, sleep_score,
          readiness_state, readiness_confidence, reasons_json, pp_recommendation, data_quality, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(date) DO UPDATE SET
          steps=excluded.steps,
          distance_km=excluded.distance_km,
          calories_out=excluded.calories_out,
          floors=excluded.floors,
          active_zone_minutes=excluded.active_zone_minutes,
          resting_hr=excluded.resting_hr,
          hrv_rmssd=excluded.hrv_rmssd,
          sleep_minutes=excluded.sleep_minutes,
          sleep_efficiency=excluded.sleep_efficiency,
          sleep_score=excluded.sleep_score,
          readiness_state=excluded.readiness_state,
          readiness_confidence=excluded.readiness_confidence,
          reasons_json=excluded.reasons_json,
          pp_recommendation=excluded.pp_recommendation,
          data_quality=excluded.data_quality,
          updated_at=excluded.updated_at
        """,
        (
            day_str,
            steps_v,
            dist_v,
            cals_v,
            floors_v,
            azm_v,
            resting_hr,
            hrv_v,
            sleep_min,
            sleep_eff,
            sleep_score,
            state,
            conf,
            json.dumps(reasons),
            rec,
            data_quality,
            updated_at,
        ),
    )

    for e in errors:
        add_quality_flag(conn, day_str, "warn", "endpoint_failed", f"{e['endpoint']}: {e['error']}")

    status = "ok" if not errors else "partial"
    details = {"errors": errors, "reasons": reasons, "data_quality": data_quality}
    conn.execute(
        "INSERT INTO sync_runs(started_at, finished_at, status, scope, requested_date, details_json) VALUES (?,?,?,?,?,?)",
        (
            started,
            datetime.now(timezone.utc).isoformat(),
            status,
            "sync-day",
            day_str,
            json.dumps(details),
        ),
    )
    conn.commit()

    result = {
        "date": day_str,
        "status": status,
        "quality": data_quality,
        "readiness": state,
        "confidence": conf,
        "errors": len(errors),
        "updated_at": updated_at,
    }
    if emit_text:
        print(f"Synced {day_str}: status={status}, quality={data_quality}, readiness={state}, confidence={conf}")
    return result


def backfill(start: str, end: str, emit_text: bool = True) -> List[Dict[str, Any]]:
    d0 = date.fromisoformat(start)
    d1 = date.fromisoformat(end)
    cur = d0
    out: List[Dict[str, Any]] = []
    while cur <= d1:
        out.append(sync_day(cur.isoformat(), emit_text=emit_text))
        cur += timedelta(days=1)
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync-day")
    s.add_argument("--date", required=False)
    b = sub.add_parser("backfill")
    b.add_argument("--start", required=True)
    b.add_argument("--end", required=True)
    args = p.parse_args()

    if args.cmd == "sync-day":
        sync_day(args.date or date.today().isoformat(), emit_text=True)
    else:
        backfill(args.start, args.end, emit_text=True)


if __name__ == "__main__":
    main()
