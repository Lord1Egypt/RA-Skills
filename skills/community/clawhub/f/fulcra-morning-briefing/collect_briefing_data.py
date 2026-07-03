#!/usr/bin/env python3
"""Collect Fulcra context for a morning briefing.

This script outputs structured JSON for an agent to turn into a tone-calibrated
morning briefing. It can use a local Fulcra context service when explicitly
configured, and otherwise falls back to direct Fulcra CLI JSON commands.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def add_fulcra_context_to_path() -> None:
    candidates: list[Path] = []
    if os.environ.get("FULCRA_CONTEXT_SCRIPTS"):
        candidates.append(Path(os.environ["FULCRA_CONTEXT_SCRIPTS"]))

    here = Path(__file__).resolve()
    candidates.extend(
        [
            here.parents[1] / "fulcra-context" / "scripts",
            here.parents[2] / "fulcra-context" / "scripts",
            Path.cwd() / "skills" / "fulcra-context" / "scripts",
        ]
    )

    for candidate in candidates:
        if (candidate / "fulcra_data_service.py").exists():
            sys.path.insert(0, str(candidate))
            return


def load_api() -> tuple[Any | None, str | None]:
    add_fulcra_context_to_path()
    try:
        from fulcra_data_service import get_service
    except ImportError:
        return CliFulcraApi(), None

    return get_service(), None


def parse_fulcra_output(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        items = []
        for line in text.splitlines():
            line = line.strip()
            if line:
                items.append(json.loads(line))
        return items


def run_fulcra_json(*args: str, timeout: int = 30) -> Any:
    result = subprocess.run(
        ["uv", "tool", "run", "fulcra-api", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"fulcra-api {' '.join(args)} failed")
    text = result.stdout.strip()
    return parse_fulcra_output(text)


class CliFulcraApi:
    """Small CLI-backed subset used when no host service is configured."""

    def get_metric_samples(self, start: str, end: str, metric_name: str) -> list[dict[str, Any]]:
        payload = run_fulcra_json("get-records", metric_name, start, end)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            records = payload.get("records") or payload.get("data") or payload.get("items")
            if isinstance(records, list):
                return records
        return []

    def get_calendar_events(self, start: str, end: str) -> list[dict[str, Any]]:
        payload = run_fulcra_json("calendar-events", start, end)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            events = payload.get("events") or payload.get("data") or payload.get("items")
            if isinstance(events, list):
                return events
        return []


def get_data_updates(hours: int) -> dict[str, Any]:
    try:
        payload = run_fulcra_json("data-updates", f"{hours} hours")
        if not isinstance(payload, dict):
            return {"available": False, "reason": "unexpected output"}
        data_types = payload.get("data_types") or {}
        file_changes = payload.get("file_changes") or []
        if not isinstance(data_types, dict):
            data_types = {}
        if not isinstance(file_changes, list):
            file_changes = []
        return {
            "available": True,
            "window_hours": hours,
            "changed_types": sorted(str(key) for key in data_types.keys()),
            "file_changes_count": len(file_changes),
        }
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def get_sleep(api: Any, lookback_hours: int = 14) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=lookback_hours)).isoformat()
    end = now.isoformat()

    try:
        samples = api.get_metric_samples(start, end, "SleepStage")
        if not samples:
            return {"available": False, "reason": "no data"}

        stage_names = {0: "InBed", 1: "Asleep", 2: "Awake", 3: "Core", 4: "Deep", 5: "REM"}
        stage_minutes: dict[str, float] = {}

        for sample in samples:
            start_dt = datetime.fromisoformat(sample["start_date"].replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(sample["end_date"].replace("Z", "+00:00"))
            minutes = (end_dt - start_dt).total_seconds() / 60
            stage = stage_names.get(sample.get("value", -1), f"Unknown({sample.get('value')})")
            stage_minutes[stage] = stage_minutes.get(stage, 0) + minutes

        sleep_minutes = sum(value for key, value in stage_minutes.items() if key not in {"Awake", "InBed"})
        deep_pct = stage_minutes.get("Deep", 0) / max(sleep_minutes, 1) * 100
        rem_pct = stage_minutes.get("REM", 0) / max(sleep_minutes, 1) * 100

        if sleep_minutes < 360:
            quality = "poor"
        elif deep_pct < 10 or rem_pct < 15:
            quality = "fair"
        elif sleep_minutes >= 420 and deep_pct >= 15 and rem_pct >= 20:
            quality = "excellent"
        else:
            quality = "good"

        return {
            "available": True,
            "total_hours": round(sleep_minutes / 60, 1),
            "stages_minutes": {key: round(value, 0) for key, value in stage_minutes.items()},
            "quality": quality,
            "deep_pct": round(deep_pct, 1),
            "rem_pct": round(rem_pct, 1),
        }
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def get_metric_summary(api: Any, metric_name: str, hours: int) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    try:
        samples = api.get_metric_samples((now - timedelta(hours=hours)).isoformat(), now.isoformat(), metric_name)
        values = [sample["value"] for sample in samples or [] if "value" in sample]
        if not values:
            return {"available": False}
        return {
            "available": True,
            "avg": round(sum(values) / len(values), 1),
            "min": round(min(values), 1),
            "max": round(max(values), 1),
            "latest": round(values[-1], 1),
            "samples": len(values),
        }
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def get_steps(api: Any) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    try:
        samples = api.get_metric_samples((now - timedelta(hours=24)).isoformat(), now.isoformat(), "StepCount")
        if not samples:
            return {"available": False}
        return {"available": True, "total": round(sum(sample.get("value", 0) for sample in samples))}
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def get_calendar(api: Any) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    try:
        events = api.get_calendar_events(start.isoformat(), end.isoformat())
        formatted = [
            {
                "title": event.get("title", "Untitled"),
                "start": event.get("start_date") or event.get("start_time") or event.get("start", ""),
                "end": event.get("end_date") or event.get("end_time") or event.get("end", ""),
                "all_day": event.get("is_all_day", event.get("all_day", False)),
                "location": event.get("location", ""),
            }
            for event in events or []
        ]
        return {"available": True, "events": formatted, "count": len(formatted)}
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def get_weather(summary: str | None) -> dict[str, Any]:
    if not summary:
        return {
            "available": False,
            "reason": "not supplied; provide weather from a trusted host tool or user-approved source",
        }
    return {"available": True, "summary": summary}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect morning briefing data from Fulcra context")
    parser.add_argument("--weather-summary", help="Optional trusted weather summary to include without making a network request")
    parser.add_argument("--lookback", type=int, default=14, help="Hours to look back for sleep data")
    args = parser.parse_args()

    api, error = load_api()
    if error:
        print(json.dumps({"ok": False, "error": error}, indent=2))
        return 1

    briefing = {
        "ok": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "freshness": get_data_updates(args.lookback),
        "sleep": get_sleep(api, args.lookback),
        "heart_rate": get_metric_summary(api, "HeartRate", 10),
        "hrv": get_metric_summary(api, "HeartRateVariabilitySDNN", 12),
        "steps": get_steps(api),
        "calendar": get_calendar(api),
        "weather": get_weather(args.weather_summary),
    }
    print(json.dumps(briefing, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
