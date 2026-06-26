#!/usr/bin/env python3
import argparse
import json
import sqlite3
import subprocess
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from _fitbit_common import db, fitbit_get, get_config, load_tokens, utc_now_iso

CONTRACT_PATH = Path(__file__).resolve().parent.parent / "references" / "capability_contract.json"
from fitbit_sync import backfill, sync_day
from training_correlation import (
    HEALTH_DB_PATH as TRAINING_HEALTH_DB_PATH,
    correlation_summary as training_correlation_summary,
    health_window as training_health_window,
    status as training_status,
    sync_calendar as training_sync_calendar,
    _connect as training_connect,
)


SUPPORTED_METRICS = {
    "steps",
    "distance_km",
    "calories_out",
    "floors",
    "active_zone_minutes",
    "resting_hr",
    "hrv_rmssd",
    "sleep_minutes",
    "sleep_efficiency",
    "sleep_score",
    "data_quality",
    "updated_at",
}

DEFAULT_METRICS = ["hrv_rmssd", "resting_hr", "sleep_minutes", "data_quality"]

# Broad Fitbit endpoint catalog for discovery + direct access.
HEALTH_DB_PATH = Path(__file__).resolve().parent.parent / "assets" / "health_unified.sqlite3"

ENDPOINT_CATALOG = {
    "activity_steps": {
        "path_template": "activities/steps/date/{date}/1d.json",
        "scope": "activity",
        "kind": "daily",
    },
    "activity_distance": {
        "path_template": "activities/distance/date/{date}/1d.json",
        "scope": "activity",
        "kind": "daily",
    },
    "activity_floors": {
        "path_template": "activities/floors/date/{date}/1d.json",
        "scope": "activity",
        "kind": "daily",
    },
    "activity_calories": {
        "path_template": "activities/calories/date/{date}/1d.json",
        "scope": "activity",
        "kind": "daily",
    },
    "activity_azm": {
        "path_template": "activities/active-zone-minutes/date/{date}/1d.json",
        "scope": "activity",
        "kind": "daily",
    },
    "heart_daily": {
        "path_template": "activities/heart/date/{date}/1d.json",
        "scope": "heartrate",
        "kind": "daily",
    },
    "hrv_daily": {
        "path_template": "hrv/date/{date}.json",
        "scope": "heartrate",
        "kind": "daily",
    },
    "sleep_daily": {
        "path_template": "sleep/date/{date}.json",
        "scope": "sleep",
        "kind": "daily",
    },
    "weight_daily": {
        "path_template": "body/log/weight/date/{date}.json",
        "scope": "weight",
        "kind": "daily",
    },
    "foods_daily": {
        "path_template": "foods/log/date/{date}.json",
        "scope": "nutrition",
        "kind": "daily",
    },
    "profile": {
        "path_template": "profile.json",
        "scope": "profile",
        "kind": "singleton",
    },
}


def _print(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, separators=(",", ":")))


def _metrics_arg(value: str) -> List[str]:
    if not value or value == "*":
        return sorted(SUPPORTED_METRICS)
    out = [v.strip() for v in value.split(",") if v.strip()]
    invalid = [m for m in out if m not in SUPPORTED_METRICS]
    if invalid:
        raise ValueError(f"unsupported metrics: {','.join(invalid)}")
    return out


def _default_range(days: int) -> Tuple[str, str]:
    d1 = date.today()
    d0 = d1 - timedelta(days=max(days - 1, 0))
    return d0.isoformat(), d1.isoformat()


def _safe_get(cfg, path: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        return fitbit_get(cfg, path), None
    except Exception as e:
        return None, str(e)


def _sample_keys(payload: Any, limit: int = 12) -> List[str]:
    if isinstance(payload, dict):
        return sorted(list(payload.keys()))[:limit]
    if isinstance(payload, list):
        if payload and isinstance(payload[0], dict):
            return sorted(list(payload[0].keys()))[:limit]
        return ["<list>"]
    return [type(payload).__name__]


def classify_error(error_text: str) -> str:
    e = (error_text or "").lower()
    if "429" in e or "rate limited" in e:
        return "rate_limited"
    if "insufficient scope" in e or "missing scope" in e:
        return "missing_scope"
    if "404" in e:
        return "device_unsupported_or_not_found"
    if "empty" in e or "no data" in e:
        return "no_data"
    return "error"


def capability_matrix() -> None:
    cfg = get_config()
    token = load_tokens(cfg)
    granted = set((token.get("scope") or "").split())
    configured = set((cfg.scopes or "").split())

    contract = json.loads(CONTRACT_PATH.read_text())
    rows = []
    for item in contract.get("domains", []):
        scope = item["required_scope"]
        has_scope = scope in granted if granted else scope in configured
        rows.append(
            {
                "domain": item["domain"],
                "path": item["path"],
                "required_scope": scope,
                "token_has_scope": has_scope,
                "inspire3_expected": item.get("inspire3_expected", "conditional"),
                "data_available": "unknown_without_fetch",
                "blocked_reason": None if has_scope else "missing_scope",
                "notes": item.get("notes", ""),
            }
        )

    _print(
        {
            "ok": True,
            "mode": "docs_first_static_contract",
            "source": contract.get("source", {}),
            "granted_scopes": sorted(granted),
            "configured_scopes": sorted(configured),
            "rows": rows,
        }
    )


def _is_nonempty_payload(payload: Dict[str, Any]) -> bool:
    # Heuristic: if any leaf scalar is non-zero/non-empty, consider endpoint populated.
    stack = [payload]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
        else:
            if cur not in (None, "", 0, 0.0, False, "0", "0.0"):
                return True
    return False


def tool_schema() -> None:
    _print(
        {
            "ok": True,
            "tool": "fitbit_tools",
            "commands": [
                "schema",
                "auth-status",
                "catalog",
                "capability-matrix",
                "discover-capabilities",
                "fetch-endpoint",
                "fetch-day",
                "fetch-range",
                "fetch-latest",
                "store-sync-day",
                "store-sync-range",
                "quality-flags",
                "unified-status",
                "unified-fetch-latest",
                "training-sync-calendar",
                "training-health-status",
                "training-health-window",
                "training-health-correlation",
            ],
            "supported_metrics": sorted(SUPPORTED_METRICS),
            "default_metrics": DEFAULT_METRICS,
            "endpoint_catalog": sorted(list(ENDPOINT_CATALOG.keys())),
            "output": "compact_json",
        }
    )


def auth_status() -> None:
    cfg = get_config()
    tokens = load_tokens(cfg)
    exp = tokens.get("expires_at")
    now_ts = __import__("time").time()
    status = "missing"
    seconds = None
    if exp:
        seconds = int(float(exp) - now_ts)
        status = "valid" if seconds > 0 else "expired"
    _print(
        {
            "ok": True,
            "token_status": status,
            "seconds_to_expiry": seconds,
            "has_refresh_token": bool(tokens.get("refresh_token")),
            "granted_scopes": (tokens.get("scope") or "").split(),
            "configured_scopes": cfg.scopes.split(),
            "at": utc_now_iso(),
        }
    )


def catalog() -> None:
    _print({"ok": True, "catalog": ENDPOINT_CATALOG})


def discover_capabilities(days: int, sleep_ms: int, stop_on_429: bool) -> None:
    cfg = get_config()
    start, end = _default_range(days)
    d0 = date.fromisoformat(start)

    summary = {
        "ok": True,
        "range": {"start": start, "end": end, "days": days},
        "throttle_ms": sleep_ms,
        "stop_on_429": stop_on_429,
        "scopes": cfg.scopes.split(),
        "results": {},
    }

    for name, spec in ENDPOINT_CATALOG.items():
        kind = spec["kind"]
        entry = {
            "scope": spec["scope"],
            "kind": kind,
            "supported": True,
            "populated_days": 0,
            "empty_days": 0,
            "errors": 0,
            "sample_keys": [],
            "last_error": None,
        }

        if kind == "singleton":
            payload, err = _safe_get(cfg, spec["path_template"])
            if err:
                entry["supported"] = False
                entry["errors"] = 1
                entry["last_error"] = err
            else:
                entry["sample_keys"] = _sample_keys(payload)
                entry["populated_days"] = 1 if _is_nonempty_payload(payload) else 0
                entry["empty_days"] = 0 if entry["populated_days"] else 1
            summary["results"][name] = entry
            if sleep_ms > 0:
                time.sleep(sleep_ms / 1000.0)
            continue

        for i in range(days):
            d = (d0 + timedelta(days=i)).isoformat()
            path = spec["path_template"].format(date=d)
            payload, err = _safe_get(cfg, path)
            if err:
                entry["errors"] += 1
                entry["last_error"] = err
                entry["last_error_class"] = classify_error(err)
                if stop_on_429 and "429" in err:
                    break
            else:
                if not entry["sample_keys"]:
                    entry["sample_keys"] = _sample_keys(payload)
                if _is_nonempty_payload(payload):
                    entry["populated_days"] += 1
                else:
                    entry["empty_days"] += 1
            if sleep_ms > 0:
                time.sleep(sleep_ms / 1000.0)

        if entry["errors"] == days:
            entry["supported"] = False
        summary["results"][name] = entry

    _print(summary)


def fetch_endpoint(path: str, params_json: str, normalize: bool) -> None:
    cfg = get_config()
    params = None
    if params_json:
        params = json.loads(params_json)
        if not isinstance(params, dict):
            raise ValueError("params_json must decode to an object")

    payload = fitbit_get(cfg, path, params=params)
    if normalize and isinstance(payload, dict):
        _print({"ok": True, "path": path, "params": params or {}, "sample_keys": _sample_keys(payload), "payload": payload})
        return
    _print({"ok": True, "path": path, "params": params or {}, "payload": payload})


def fetch_day(day: str, raw: bool) -> None:
    cfg = get_config()
    payload = {
        "steps": fitbit_get(cfg, f"activities/steps/date/{day}/1d.json"),
        "distance": fitbit_get(cfg, f"activities/distance/date/{day}/1d.json"),
        "floors": fitbit_get(cfg, f"activities/floors/date/{day}/1d.json"),
        "calories": fitbit_get(cfg, f"activities/calories/date/{day}/1d.json"),
        "active_zone_minutes": fitbit_get(cfg, f"activities/active-zone-minutes/date/{day}/1d.json"),
        "sleep": fitbit_get(cfg, f"sleep/date/{day}.json"),
        "heart": fitbit_get(cfg, f"activities/heart/date/{day}/1d.json"),
        "hrv": fitbit_get(cfg, f"hrv/date/{day}.json"),
    }
    if raw:
        _print({"ok": True, "date": day, "source": "fitbit_api", "raw": payload})
        return

    def _v(d, *keys, default=None):
        cur = d
        for k in keys:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            elif isinstance(cur, list) and isinstance(k, int) and len(cur) > k:
                cur = cur[k]
            else:
                return default
        return cur

    def _first_value(d, list_key):
        items = _v(d, list_key, default=[])
        if isinstance(items, list) and items:
            first = items[0]
            if isinstance(first, dict):
                return first.get("value")
        return None

    def _to_int(value, default=0):
        try:
            if value in (None, ""):
                return default
            return int(float(value))
        except Exception:
            return default

    def _to_float(value, default=0.0):
        try:
            if value in (None, ""):
                return default
            return float(value)
        except Exception:
            return default

    azm_raw = _first_value(payload["active_zone_minutes"], "activities-active-zone-minutes")
    sleep_entry = _v(payload["sleep"], "sleep", 0, default={}) or {}

    normalized = {
        "date": day,
        "steps": _to_int(_first_value(payload["steps"], "activities-steps"), default=0),
        "distance_km": _to_float(_first_value(payload["distance"], "activities-distance"), default=0.0),
        "floors": _to_int(_first_value(payload["floors"], "activities-floors"), default=0),
        "calories_out": _to_int(_first_value(payload["calories"], "activities-calories"), default=0),
        "active_zone_minutes": _to_int(azm_raw.get("activeZoneMinutes") if isinstance(azm_raw, dict) else azm_raw, default=0),
        "sleep_minutes": _v(payload["sleep"], "summary", "totalMinutesAsleep"),
        "sleep_efficiency": sleep_entry.get("efficiency") or _v(payload["sleep"], "summary", "efficiency"),
        "sleep_score": sleep_entry.get("sleepScore") or _v(payload["sleep"], "summary", "sleepScore"),
        "resting_hr": _v(payload["heart"], "activities-heart", 0, "value", "restingHeartRate"),
        "hrv_rmssd": _v(payload["hrv"], "hrv", 0, "value", "dailyRmssd"),
    }
    _print({"ok": True, "date": day, "source": "fitbit_api", "normalized": normalized})


def fetch_range(start: str, end: str, metrics: List[str], ensure_fresh: bool) -> None:
    if ensure_fresh:
        backfill(start, end, emit_text=False)

    cfg = get_config()
    conn = db(cfg)
    conn.row_factory = sqlite3.Row
    cols = ["date"] + metrics
    query = f"SELECT {', '.join(cols)} FROM daily_metrics WHERE date BETWEEN ? AND ? ORDER BY date ASC"
    rows = [dict(r) for r in conn.execute(query, (start, end)).fetchall()]
    _print(
        {
            "ok": True,
            "source": "local_cache",
            "freshened": ensure_fresh,
            "start": start,
            "end": end,
            "metrics": metrics,
            "rows": rows,
        }
    )


def fetch_latest(days: int, metrics: List[str], ensure_fresh: bool) -> None:
    start, end = _default_range(days)
    if ensure_fresh:
        backfill(start, end, emit_text=False)

    cfg = get_config()
    conn = db(cfg)
    conn.row_factory = sqlite3.Row
    cols = ["date"] + metrics
    query = f"SELECT {', '.join(cols)} FROM daily_metrics ORDER BY date DESC LIMIT ?"
    rows = [dict(r) for r in conn.execute(query, (days,)).fetchall()]
    _print({"ok": True, "source": "local_cache", "freshened": ensure_fresh, "days": days, "metrics": metrics, "rows": rows})


def store_sync_day(day: str) -> None:
    result = sync_day(day, emit_text=False)
    _print({"ok": True, "operation": "store.sync-day", "result": result})


def store_sync_range(start: str, end: str) -> None:
    results = backfill(start, end, emit_text=False)
    _print({"ok": True, "operation": "store.sync-range", "start": start, "end": end, "results": results})


def quality_flags(start: str, end: str) -> None:
    cfg = get_config()
    conn = db(cfg)
    conn.row_factory = sqlite3.Row
    rows = [
        dict(r)
        for r in conn.execute(
            "SELECT date, level, flag, message, created_at FROM quality_flags WHERE date BETWEEN ? AND ? ORDER BY created_at DESC",
            (start, end),
        ).fetchall()
    ]
    _print({"ok": True, "source": "local_cache", "start": start, "end": end, "rows": rows})


def unified_status() -> None:
    conn = sqlite3.connect(str(HEALTH_DB_PATH))
    sources = [
        {"source": r[0], "count": r[1]} for r in conn.execute(
            "SELECT source, COUNT(*) FROM daily_health_summary GROUP BY source ORDER BY source"
        ).fetchall()
    ]
    date_range = conn.execute(
        "SELECT MIN(date), MAX(date) FROM daily_health_summary"
    ).fetchone()
    raw = conn.execute("SELECT COUNT(*) FROM apple_health_records").fetchone()[0]
    _print({
        "ok": True,
        "db": str(HEALTH_DB_PATH),
        "daily_sources": sources,
        "daily_range": {"start": date_range[0], "end": date_range[1]},
        "apple_raw_records": raw,
    })


def unified_fetch_latest(days: int, source: str) -> None:
    conn = sqlite3.connect(str(HEALTH_DB_PATH))
    conn.row_factory = sqlite3.Row

    if source == "best":
        query = """
        WITH ranked AS (
          SELECT *,
                 CASE WHEN source='fitbit' THEN 2 WHEN source='apple_health' THEN 1 ELSE 0 END AS pri,
                 ROW_NUMBER() OVER (PARTITION BY date ORDER BY CASE WHEN source='fitbit' THEN 2 WHEN source='apple_health' THEN 1 ELSE 0 END DESC, ingested_at DESC) AS rn
          FROM daily_health_summary
        )
        SELECT date, source, steps, resting_hr, hrv_rmssd, sleep_minutes, data_quality, ingested_at
        FROM ranked
        WHERE rn = 1
        ORDER BY date DESC
        LIMIT ?
        """
        rows = [dict(r) for r in conn.execute(query, (days,)).fetchall()]
    else:
        rows = [
            dict(r)
            for r in conn.execute(
                """
                SELECT date, source, steps, resting_hr, hrv_rmssd, sleep_minutes, data_quality, ingested_at
                FROM daily_health_summary
                WHERE source = ?
                ORDER BY date DESC
                LIMIT ?
                """,
                (source, days),
            ).fetchall()
        ]

    _print({"ok": True, "source": source, "days": days, "rows": rows})


def training_fetch_calendar(calendar_id: str, out_path: str, start: str, end: str, account: Optional[str]) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "gog",
        "calendar",
        "events",
        calendar_id,
        "--json",
        "--results-only",
        "--no-input",
        "--all-pages",
        "--from",
        start,
        "--to",
        end,
    ]
    if account:
        cmd.extend(["--account", account])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "gog calendar fetch failed")

    payload = json.loads(proc.stdout or "{}")
    events = payload.get("events") if isinstance(payload, dict) else payload
    if not isinstance(events, list):
        raise RuntimeError("unexpected gog calendar payload shape")

    out.write_text(json.dumps({"events": events}, ensure_ascii=False, indent=2))
    _print(
        {
            "ok": True,
            "operation": "training-fetch-calendar",
            "calendar_id": calendar_id,
            "account": account,
            "from": start,
            "to": end,
            "out": str(out),
            "events": len(events),
            "first": events[0].get("start", {}) if events else None,
            "last": events[-1].get("start", {}) if events else None,
        }
    )



def training_sync(json_path: str, title_prefixes: List[str], calendar_filter: Optional[str], start: Optional[str], end: Optional[str], reset: bool) -> None:
    conn = training_connect(TRAINING_HEALTH_DB_PATH)
    try:
        result = training_sync_calendar(
            conn,
            Path(json_path),
            title_prefixes,
            calendar_filter,
            start,
            end,
            reset,
        )
    finally:
        conn.close()
    _print(result)


def training_health_status(source: str) -> None:
    conn = training_connect(TRAINING_HEALTH_DB_PATH)
    try:
        result = training_status(conn, source)
    finally:
        conn.close()
    _print(result)


def training_window(days: int, source: str) -> None:
    conn = training_connect(TRAINING_HEALTH_DB_PATH)
    try:
        result = training_health_window(conn, days, source)
    finally:
        conn.close()
    _print(result)


def training_correlation(days: int, source: str) -> None:
    conn = training_connect(TRAINING_HEALTH_DB_PATH)
    try:
        result = training_correlation_summary(conn, days, source)
    finally:
        conn.close()
    _print(result)


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("schema")
    sub.add_parser("auth-status")
    sub.add_parser("catalog")
    sub.add_parser("capability-matrix")

    dc = sub.add_parser("discover-capabilities")
    dc.add_argument("--days", type=int, default=7)
    dc.add_argument("--sleep-ms", type=int, default=350, help="Delay between API calls to reduce 429s")
    dc.add_argument("--stop-on-429", action="store_true", help="Stop probing each endpoint after first 429")

    fe = sub.add_parser("fetch-endpoint")
    fe.add_argument("--path", required=True, help="Fitbit API path under /1/user/-/ e.g. sleep/date/2026-03-15.json")
    fe.add_argument("--params-json", default="", help='Optional JSON object for query params, e.g. {"sort":"asc"}')
    fe.add_argument("--normalize", action="store_true", help="Include sample_keys alongside payload")

    fday = sub.add_parser("fetch-day")
    fday.add_argument("--date", default=date.today().isoformat())
    fday.add_argument("--raw", action="store_true")

    fr = sub.add_parser("fetch-range")
    fr.add_argument("--start", required=True)
    fr.add_argument("--end", required=True)
    fr.add_argument("--metrics", default=",".join(DEFAULT_METRICS))
    fr.add_argument("--ensure-fresh", action="store_true")

    fl = sub.add_parser("fetch-latest")
    fl.add_argument("--days", type=int, default=5)
    fl.add_argument("--metrics", default=",".join(DEFAULT_METRICS))
    fl.add_argument("--ensure-fresh", action="store_true")

    ssd = sub.add_parser("store-sync-day")
    ssd.add_argument("--date", default=date.today().isoformat())

    ssr = sub.add_parser("store-sync-range")
    ssr.add_argument("--start", required=True)
    ssr.add_argument("--end", required=True)

    qf = sub.add_parser("quality-flags")
    qf.add_argument("--start", required=False)
    qf.add_argument("--end", required=False)
    qf.add_argument("--days", type=int, default=7)

    sub.add_parser("unified-status")

    ufl = sub.add_parser("unified-fetch-latest")
    ufl.add_argument("--days", type=int, default=14)
    ufl.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    tfc = sub.add_parser("training-fetch-calendar")
    tfc.add_argument("--calendar-id", required=True)
    tfc.add_argument("--out", required=True)
    tfc.add_argument("--from", dest="from_", required=True)
    tfc.add_argument("--to", required=True)
    tfc.add_argument("--account")

    tsc = sub.add_parser("training-sync-calendar")
    tsc.add_argument("--json", required=True)
    tsc.add_argument("--title-prefix", action="append", default=["Training —", "Training -", "Workout Log —"])
    tsc.add_argument("--calendar-filter")
    tsc.add_argument("--start")
    tsc.add_argument("--end")
    tsc.add_argument("--reset", action="store_true")

    ths = sub.add_parser("training-health-status")
    ths.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    thw = sub.add_parser("training-health-window")
    thw.add_argument("--days", type=int, default=28)
    thw.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    thc = sub.add_parser("training-health-correlation")
    thc.add_argument("--days", type=int, default=90)
    thc.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    args = p.parse_args()

    try:
        if args.cmd == "schema":
            tool_schema()
        elif args.cmd == "auth-status":
            auth_status()
        elif args.cmd == "catalog":
            catalog()
        elif args.cmd == "capability-matrix":
            capability_matrix()
        elif args.cmd == "discover-capabilities":
            discover_capabilities(args.days, args.sleep_ms, args.stop_on_429)
        elif args.cmd == "fetch-endpoint":
            fetch_endpoint(args.path, args.params_json, args.normalize)
        elif args.cmd == "fetch-day":
            fetch_day(args.date, args.raw)
        elif args.cmd == "fetch-range":
            fetch_range(args.start, args.end, _metrics_arg(args.metrics), args.ensure_fresh)
        elif args.cmd == "fetch-latest":
            fetch_latest(args.days, _metrics_arg(args.metrics), args.ensure_fresh)
        elif args.cmd == "store-sync-day":
            store_sync_day(args.date)
        elif args.cmd == "store-sync-range":
            store_sync_range(args.start, args.end)
        elif args.cmd == "quality-flags":
            start, end = args.start, args.end
            if not start or not end:
                start, end = _default_range(args.days)
            quality_flags(start, end)
        elif args.cmd == "unified-status":
            unified_status()
        elif args.cmd == "unified-fetch-latest":
            unified_fetch_latest(args.days, args.source)
        elif args.cmd == "training-fetch-calendar":
            training_fetch_calendar(args.calendar_id, args.out, args.from_, args.to, args.account)
        elif args.cmd == "training-sync-calendar":
            training_sync(args.json, args.title_prefix, args.calendar_filter, args.start, args.end, args.reset)
        elif args.cmd == "training-health-status":
            training_health_status(args.source)
        elif args.cmd == "training-health-window":
            training_window(args.days, args.source)
        elif args.cmd == "training-health-correlation":
            training_correlation(args.days, args.source)
    except Exception as e:
        _print({"ok": False, "error": str(e), "cmd": args.cmd})
        raise SystemExit(2)


if __name__ == "__main__":
    main()
