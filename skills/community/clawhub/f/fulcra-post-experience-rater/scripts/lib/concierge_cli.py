#!/usr/bin/env python3
"""Shared Fulcra CLI reads for the concierge skills.

Several skills need the same things from the `fulcra-api` CLI: run a command and parse
its NDJSON, read today's calendar, summarize last night's sleep. That logic was being
copied into each skill; it lives here once. The sleep math is ported verbatim from the
subjective-checkin skill (which mirrors the official fulcra-context sleep utility), so
all skills agree on what "last night's sleep" means.

Auth: the fulcra-api CLI (FULCRA_ACCESS_TOKEN or `fulcra auth login`). No tokens printed.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
from datetime import datetime, timedelta, timezone
from typing import Any

CLI_COMMAND = os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api")

# Authoritative SleepStage values (Fulcra catalog + fulcra-context sleep utils):
# 0 = in bed, 1 = asleep (unspecified), 2 = awake, 3 = core/light, 4 = deep, 5 = REM.
# Time asleep = stages 3 + 4 + 5; stage 2 is awake-in-bed.
SLEEP_STAGE_NAMES = {2: "awake", 3: "core", 4: "deep", 5: "rem"}


def run_cli(args: list[str]) -> tuple[int, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    cmd = [*shlex.split(CLI_COMMAND, posix=(os.name != "nt")), *args]
    try:
        proc = subprocess.run(cmd, env=env, text=True, capture_output=True, timeout=120)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, f"CLI invocation failed: {exc}"
    if proc.returncode != 0:
        return proc.returncode, (proc.stderr or proc.stdout or "").strip()
    return 0, proc.stdout


def parse_records(raw: str) -> list[Any]:
    """Fulcra CLI commands emit NDJSON (one JSON object per line). Tolerate a plain JSON
    array or a {"data": [...]} envelope too."""
    raw = (raw or "").strip()
    if not raw:
        return []
    try:
        val = json.loads(raw)
        if isinstance(val, list):
            return val
        if isinstance(val, dict):
            return val["data"] if isinstance(val.get("data"), list) else [val]
    except json.JSONDecodeError:
        pass
    rows: list[Any] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _parse_dt(ts: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except (ValueError, AttributeError, TypeError):
        return None


def _field(sample: dict[str, Any], *names: str) -> Any:
    for n in names:
        if sample.get(n) is not None:
            return sample[n]
    return None


def calendar_events(start: datetime, end: datetime) -> dict[str, Any]:
    """Today's (or any window's) calendar events: count + first start + titles."""
    rc, body = run_cli(["calendar-events", start.isoformat(), end.isoformat()])
    if rc != 0:
        return {"available": False, "reason": body[:300]}
    rows = [r for r in parse_records(body) if isinstance(r, dict)]
    titles = [r.get("title") or r.get("summary") or r.get("name") or "(untitled)" for r in rows]
    starts = [_field(r, "start_date", "start_time", "start") for r in rows]
    starts = [s for s in starts if s]
    return {"available": True, "event_count": len(rows), "titles": titles[:15],
            "first_start": min(starts) if starts else None}


def today_calendar(now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now().astimezone()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return calendar_events(day_start, day_start + timedelta(days=1))


def sleep_summary(now: datetime | None = None, lookback_hours: int = 30) -> dict[str, Any]:
    """Summarize the most recent sleep session from raw SleepStage samples. Groups samples
    into sessions (gaps > 60 min split), takes the latest, derives hours asleep, deep/REM %,
    efficiency, and a coarse poor/fair/good/excellent quality label."""
    now = now or datetime.now().astimezone()
    rc, body = run_cli(["get-records", "SleepStage", (now - timedelta(hours=lookback_hours)).isoformat(), now.isoformat()])
    if rc != 0:
        return {"available": False, "reason": body[:300]}

    samples: list[tuple[datetime, datetime, int]] = []
    for r in parse_records(body):
        if not isinstance(r, dict):
            continue
        sd = _parse_dt(_field(r, "start_date", "start_time", "start", "time"))
        ed = _parse_dt(_field(r, "end_date", "end_time", "end"))
        val = _field(r, "value", "sleep_stage")
        if sd and ed and val is not None:
            try:
                samples.append((sd, ed, int(val)))
            except (TypeError, ValueError):
                continue
    if not samples:
        return {"available": False, "reason": "No sleep stage data in the last ~30h."}

    samples.sort(key=lambda s: s[0])
    sessions: list[list[tuple[datetime, datetime, int]]] = [[samples[0]]]
    for s in samples[1:]:
        if (s[0] - sessions[-1][-1][1]).total_seconds() / 60 > 60:
            sessions.append([s])
        else:
            sessions[-1].append(s)
    session = sessions[-1]

    stage_min: dict[int, float] = {}
    s_start = s_end = None
    for sd, ed, val in session:
        if val in SLEEP_STAGE_NAMES:
            stage_min[val] = stage_min.get(val, 0.0) + (ed - sd).total_seconds() / 60
        s_start = sd if s_start is None or sd < s_start else s_start
        s_end = ed if s_end is None or ed > s_end else s_end

    asleep = stage_min.get(3, 0) + stage_min.get(4, 0) + stage_min.get(5, 0)
    awake = stage_min.get(2, 0)
    in_bed = asleep + awake
    if asleep < 30:
        return {"available": False, "reason": "Most recent sleep session too short to summarize."}
    deep_pct = round(stage_min.get(4, 0) / asleep * 100, 1)
    rem_pct = round(stage_min.get(5, 0) / asleep * 100, 1)
    if asleep < 360:
        quality = "poor"
    elif deep_pct < 10 or rem_pct < 15:
        quality = "fair"
    elif asleep >= 420 and deep_pct >= 15 and rem_pct >= 20:
        quality = "excellent"
    else:
        quality = "good"
    return {
        "available": True,
        "total_hours": round(asleep / 60, 1),
        "asleep_minutes": round(asleep),
        "stages_minutes": {SLEEP_STAGE_NAMES[k]: round(v) for k, v in stage_min.items()},
        "deep_pct": deep_pct,
        "rem_pct": rem_pct,
        "efficiency_pct": round(asleep / in_bed * 100, 1) if in_bed else None,
        "quality": quality,
        "bedtime": s_start.isoformat() if s_start else None,
        "wake": s_end.isoformat() if s_end else None,
    }


def metric_samples(metric: str, start: datetime, end: datetime) -> dict[str, Any]:
    """Summary stats (avg/min/max/latest) for a numeric metric, e.g. HeartRate."""
    rc, body = run_cli(["get-records", metric, start.isoformat(), end.isoformat()])
    if rc != 0:
        return {"available": False, "reason": body[:300]}
    vals = [_field(r, "value") for r in parse_records(body) if isinstance(r, dict)]
    vals = [float(v) for v in vals if isinstance(v, (int, float))]
    if not vals:
        return {"available": False, "reason": f"No {metric} samples."}
    return {"available": True, "avg": round(sum(vals) / len(vals), 1),
            "min": round(min(vals), 1), "max": round(max(vals), 1),
            "latest": round(vals[-1], 1), "samples": len(vals)}
