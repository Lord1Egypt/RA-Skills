#!/usr/bin/env python3
"""Collect everything the morning briefing needs, as one JSON blob.

The agent composes the briefing (tone-calibrated to how the user slept + how they said
they feel); this script just gathers the inputs deterministically so the agent isn't
making five separate tool calls. All sources are best-effort -- any missing one comes
back as available:false and the briefing simply skips it.

  collect [--location "New+York"] [--days-open-loops 1]

Gathers:
  - sleep        : last night's sleep summary (shared concierge_cli)
  - calendar     : today's events (count, first start, titles)
  - heart_rate   : overnight/recent HR summary (context, optional)
  - subjective   : most recent Morning Check-In (how they said they feel)
  - open_loops   : action_items + open_loops from the latest Evening Debrief
  - weather      : current conditions via wttr.in (no key needed)

Auth: Fulcra via fulcra-api CLI. No tokens printed.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concierge_bootstrap  # noqa: F401

import concierge_cli as cli  # noqa: E402
import fulcra_read  # noqa: E402


def get_subjective() -> dict:
    try:
        events = fulcra_read.read_annotation_events("Morning Check-In", days=1)
    except Exception as exc:
        return {"available": False, "reason": str(exc)[:200]}
    if events and isinstance(events[-1].get("data"), dict):
        return {"available": True, **events[-1]["data"]}
    return {"available": bool(events)}


def get_open_loops(days: float) -> dict:
    try:
        events = fulcra_read.read_annotation_events("Evening Debrief", days=days)
    except Exception as exc:
        return {"available": False, "reason": str(exc)[:200]}
    if not events:
        return {"available": False, "reason": "No recent evening debrief."}
    last = events[-1].get("data") or {}
    return {
        "available": True,
        "from_date": last.get("date"),
        "action_items": last.get("action_items") or [],
        "open_loops": last.get("open_loops") or [],
    }


def get_weather(location: str) -> dict:
    url = f"https://wttr.in/{urllib.parse.quote(location)}?format=%l:+%c+%t+%h+%w"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return {"available": True, "summary": resp.read().decode().strip(),
                    "location": location.replace("+", " ")}
    except Exception as exc:
        return {"available": False, "reason": str(exc)[:200]}


def main() -> int:
    p = argparse.ArgumentParser(description="Collect morning briefing context")
    p.add_argument("--location", default="", help="Weather location, e.g. New+York. Omit to skip weather.")
    p.add_argument("--days-open-loops", type=float, default=1.5)
    args = p.parse_args()

    now = datetime.now().astimezone()
    briefing = {
        "ok": True,
        "generated_at": now.isoformat(),
        "weekday": now.strftime("%A"),
        "sleep": cli.sleep_summary(now),
        "calendar": cli.today_calendar(now),
        "heart_rate": cli.metric_samples("HeartRate", now - timedelta(hours=10), now),
        "subjective": get_subjective(),
        "open_loops": get_open_loops(args.days_open_loops),
        "weather": get_weather(args.location) if args.location else {"available": False, "reason": "no --location"},
    }
    print(json.dumps(briefing, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
