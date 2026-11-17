#!/usr/bin/env python3
"""Collect Fulcra context for a morning briefing.

This script outputs structured JSON for an agent to turn into a
tone-calibrated morning briefing. It prefers an explicitly configured local
Fulcra service, then falls back to direct Fulcra CLI calls.
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

    for candidate in candidates:
        if (candidate / "fulcra_data_service.py").exists():
            sys.path.insert(0, str(candidate))
            return


def parse_json_output(output: str) -> Any:
    output = output.strip()
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        values = []
        for line in output.splitlines():
            line = line.strip()
            if line:
                values.append(json.loads(line))
        return values


def run_fulcra_json(*args: str) -> Any:
    command = os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api").split()
    result = subprocess.run(
        [*command, *args],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "Fulcra CLI command failed").strip()
        raise RuntimeError(message)
    return parse_json_output(result.stdout)


def range_to_window(start: str, end: str) -> str:
    start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    hours = max(1, round((end_dt - start_dt).total_seconds() / 3600))
    return f"{hours} hours"


class CliFulcraService:
    def get_metric_samples(self, start: str, end: str, metric_name: str) -> list[dict[str, Any]]:
        data = run_fulcra_json("get-records", metric_name, range_to_window(start, end))
        return data if isinstance(data, list) else data.get("records", [])

    def get_calendar_events(self, start: str, end: str) -> list[dict[str, Any]]:
        data = run_fulcra_json("calendar-events", range_to_window(start, end))
        return data if isinstance(data, list) else data.get("events", [])


def load_api() -> tuple[Any | None, str | None]:
    add_fulcra_context_to_path()
    try:
        from fulcra_data_service import get_service
    except ImportError:
        try:
            run_fulcra_json("user-info")
        except Exception as exc:
            return None, f"Fulcra CLI unavailable or unauthenticated: {exc}"
        return CliFulcraService(), None

    return get_service(), None


def get_sleep(api: Any, lookback_hours: int = 14) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=lookback_hours)).isoformat()
    end = now.isoformat()

    try:
        samples = api.get_metric_samples(start, end, "SleepStage")
        if not samples:
            return {"available": False, "reason": "no data"}

        stage_names = {2: "Awake", 3: "Core", 4: "Deep", 5: "REM"}
        stage_minutes: dict[str, float] = {}

        for sample in samples:
            start_dt = datetime.fromisoformat(sample["start_date"].replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(sample["end_date"].replace("Z", "+00:00"))
            minutes = (end_dt - start_dt).total_seconds() / 60
            stage = stage_names.get(sample.get("value", -1), f"Unknown({sample.get('value')})")
            stage_minutes[stage] = stage_minutes.get(stage, 0) + minutes

        sleep_minutes = sum(value for key, value in stage_minutes.items() if key != "Awake")
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
        try:
            scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))
            from fulcra_calendar_utils import is_real_meeting
        except ImportError:
            is_real_meeting = lambda event: bool(event.get("attendees") or event.get("participants"))

        def format_event(event: dict[str, Any]) -> dict[str, Any]:
            return {
                "title": event.get("title", "Untitled"),
                "start": event.get("start_date") or event.get("start_time") or event.get("start", ""),
                "end": event.get("end_date") or event.get("end_time") or event.get("end", ""),
                "all_day": event.get("is_all_day", event.get("all_day", False)),
                "location": event.get("location", ""),
            }

        formatted = [
            format_event(event)
            for event in events or []
        ]
        real_events = [
            format_event(event)
            for event in events or []
            if is_real_meeting(event)
        ]
        return {
            "available": True,
            "events": formatted,
            "count": len(formatted),
            "real_events": real_events,
            "real_count": len(real_events),
        }
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def summarize_data_updates(window: str) -> dict[str, Any]:
    """Return a compact freshness summary without raw private update records."""
    try:
        data = run_fulcra_json("data-updates", window)
    except Exception as exc:
        return {"available": False, "reason": str(exc)}

    if not isinstance(data, dict):
        return {"available": True, "window": window, "changed_data_types": [], "file_change_count": 0}

    data_types = data.get("data_types") or {}
    if isinstance(data_types, dict):
        changed = sorted(str(name) for name, value in data_types.items() if value)
    elif isinstance(data_types, list):
        changed = sorted(str(item) for item in data_types)
    else:
        changed = []

    file_changes = data.get("file_changes") or []
    if isinstance(file_changes, dict):
        file_change_count = sum(len(value) for value in file_changes.values() if isinstance(value, list))
    elif isinstance(file_changes, list):
        file_change_count = len(file_changes)
    else:
        file_change_count = 0

    return {
        "available": True,
        "window": window,
        "changed_data_types": changed,
        "file_change_count": file_change_count,
    }


def get_weather(location: str) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["curl", "-s", f"wttr.in/{location}?format=%l:+%c+%t+%h+%w"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return {"available": True, "summary": result.stdout.strip(), "location": location.replace("+", " ")}
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect morning briefing data from Fulcra context and weather")
    parser.add_argument("--location", default="New+York", help="Weather location, for example New+York or London")
    parser.add_argument("--lookback", type=int, default=14, help="Hours to look back for sleep data")
    args = parser.parse_args()

    api, error = load_api()
    if error:
        print(json.dumps({"ok": False, "error": error}, indent=2))
        return 1

    briefing = {
        "ok": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "freshness": summarize_data_updates(f"{args.lookback} hours"),
        "sleep": get_sleep(api, args.lookback),
        "heart_rate": get_metric_summary(api, "HeartRate", 10),
        "hrv": get_metric_summary(api, "HeartRateVariabilitySDNN", 12),
        "steps": get_steps(api),
        "calendar": get_calendar(api),
        "weather": get_weather(args.location),
    }
    print(json.dumps(briefing, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
