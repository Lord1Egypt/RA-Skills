#!/usr/bin/env python3
"""Render normalized Fitbit daily JSON.

Usage:
  python3 scripts/fitbit_render.py day.json --format markdown --channel generic
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict


def style(channel: str, markdown: bool) -> Dict[str, Any]:
    c = (channel or "generic").lower()
    if not markdown or c == "telegram":
        return {"md": False, "bL": "", "bR": "", "bullet": "-"}
    if c in ("slack", "whatsapp"):
        return {"md": True, "bL": "*", "bR": "*", "bullet": "-"}
    return {"md": True, "bL": "**", "bR": "**", "bullet": "-"}


def fmt_minutes(mins: int) -> str:
    """Convert minutes to 'Xh Ym' format."""
    if mins is None:
        return "—"
    h = mins // 60
    m = mins % 60
    if h > 0 and m > 0:
        return f"{h}h {m}m"
    elif h > 0:
        return f"{h}h"
    else:
        return f"{m}m"


def render_sleep(sleep, st):
    """Render sleep section only."""
    lines = []
    if sleep.get("duration_minutes") is not None:
        sleep_info = fmt_minutes(sleep.get('duration_minutes'))
        if sleep.get("sleep_score"):
            sleep_info += f" (score {sleep.get('sleep_score')})"
        if sleep.get("efficiency"):
            sleep_info += f" | {sleep.get('efficiency')}% efficiency"
        lines.append(f"{st['bullet']} Sleep: {sleep_info}")

        stages = []
        if sleep.get("deep_minutes") is not None:
            stages.append(f"Deep: {fmt_minutes(sleep.get('deep_minutes'))}")
        if sleep.get("light_minutes") is not None:
            stages.append(f"Light: {fmt_minutes(sleep.get('light_minutes'))}")
        if sleep.get("rem_minutes") is not None:
            stages.append(f"REM: {fmt_minutes(sleep.get('rem_minutes'))}")
        if sleep.get("wake_minutes") is not None:
            stages.append(f"Wake: {fmt_minutes(sleep.get('wake_minutes'))}")
        if stages:
            lines.append(f"  {st['bullet']} Stages: {', '.join(stages)}")

    # Nap (if present)
    if sleep.get("nap_minutes") is not None:
        lines.append(f"{st['bullet']} Nap: {fmt_minutes(sleep.get('nap_minutes'))}")

    return lines


def render_activity(act, st):
    """Render activity section only."""
    lines = []
    if act.get("steps") is not None:
        lines.append(f"{st['bullet']} Steps: {act.get('steps'):,}")
    if act.get("calories_out") is not None:
        lines.append(f"{st['bullet']} Calories: {act.get('calories_out'):,} ({act.get('calories_bmr', 0):,} BMR)")
    if act.get("distance_km") is not None:
        lines.append(f"{st['bullet']} Distance: {act.get('distance_km')} km")
    if act.get("resting_heart_rate") is not None:
        lines.append(f"{st['bullet']} Resting HR: {act.get('resting_heart_rate')} bpm")

    active_mins = []
    if act.get("very_active_minutes") is not None and act.get("very_active_minutes", 0) > 0:
        active_mins.append(f"V. Active: {fmt_minutes(act.get('very_active_minutes'))}")
    if act.get("fairly_active_minutes") is not None and act.get("fairly_active_minutes", 0) > 0:
        active_mins.append(f"Fair: {fmt_minutes(act.get('fairly_active_minutes'))}")
    if act.get("lightly_active_minutes") is not None and act.get("lightly_active_minutes", 0) > 0:
        active_mins.append(f"Light: {fmt_minutes(act.get('lightly_active_minutes'))}")
    if act.get("sedentary_minutes") is not None and act.get("sedentary_minutes", 0) > 0:
        active_mins.append(f"Sedentary: {fmt_minutes(act.get('sedentary_minutes'))}")
    if active_mins:
        lines.append(f"  {st['bullet']} Active mins: {', '.join(active_mins)}")

    hr_zones = act.get("heart_rate_zones") or []
    if hr_zones:
        zone_info = []
        for zone in hr_zones:
            if isinstance(zone, dict) and zone.get("minutes", 0) > 0:
                zone_info.append(f"{zone.get('name')}: {fmt_minutes(zone.get('minutes'))}")
        if zone_info:
            lines.append(f"  {st['bullet']} HR Zones: {', '.join(zone_info)}")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--format", choices=["text", "markdown"], default="markdown")
    ap.add_argument("--channel", default="generic")
    ap.add_argument("--section", choices=["all", "sleep", "activity"], default="all",
                    help="Which section to render: all, sleep, or activity")
    args = ap.parse_args()

    doc = json.load(open(args.input, "r", encoding="utf-8"))
    st = style(args.channel, args.format == "markdown")

    date = doc.get("date") or "(unknown date)"
    sleep = doc.get("sleep") or {}
    act = doc.get("activity") or {}

    def b(s: str) -> str:
        return f"{st['bL']}{s}{st['bR']}" if st["md"] and st["bL"] else s

    lines = [b(f"Fitbit — {date}")]

    section = args.section.lower()

    if section in ("all", "sleep"):
        lines.extend(render_sleep(sleep, st))

    if section in ("all", "activity"):
        lines.extend(render_activity(act, st))

    if len(lines) == 1:
        lines.append(f"{st['bullet']} No data found for this day")

    print("\n".join(lines).strip() + "\n", end="")


if __name__ == "__main__":
    main()
