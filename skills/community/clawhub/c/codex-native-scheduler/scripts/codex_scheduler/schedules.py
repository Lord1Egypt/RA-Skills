"""Semantic schedules shared by all native backends."""

from __future__ import annotations

import datetime as dt
import math
import time
from typing import Any

from .errors import SchedulerError
from .util import ceil_minute, iso, parse_at, parse_duration, parse_iso

WEEKDAYS = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def parse_clock(value: str) -> tuple[int, int]:
    parts = value.strip().split(":")
    if len(parts) != 2:
        raise SchedulerError("time must use HH:MM")
    try:
        hour, minute = (int(part) for part in parts)
    except ValueError as exc:
        raise SchedulerError("time must use HH:MM") from exc
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise SchedulerError("time must be between 00:00 and 23:59")
    return hour, minute


def make_schedule(
    *,
    at: str | None,
    every: str | None,
    daily_at: str | None,
    weekly_at: str | None,
    now: dt.datetime,
) -> dict[str, Any]:
    choices = [
        at is not None,
        every is not None,
        daily_at is not None,
        weekly_at is not None,
    ]
    if sum(choices) != 1:
        raise SchedulerError(
            "choose exactly one schedule: --at, --every, --daily-at, or --weekly-at"
        )
    if at is not None:
        return {"kind": "at", "at": iso(parse_at(at, now=now))}
    if every is not None:
        seconds = parse_duration(every)
        anchor = ceil_minute(now + dt.timedelta(seconds=seconds))
        return {"kind": "every", "seconds": seconds, "anchor": iso(anchor)}
    if daily_at is not None:
        hour, minute = parse_clock(daily_at)
        return {"kind": "daily", "hour": hour, "minute": minute}
    day_text, separator, clock_text = (weekly_at or "").partition("@")
    if not separator or day_text.lower() not in WEEKDAYS:
        raise SchedulerError("--weekly-at must use a value such as mon@09:30")
    hour, minute = parse_clock(clock_text)
    return {
        "kind": "weekly",
        "weekday": WEEKDAYS[day_text.lower()],
        "hour": hour,
        "minute": minute,
    }


def latest_due(schedule: dict[str, Any], now: dt.datetime) -> dt.datetime | None:
    kind = schedule["kind"]
    if kind == "at":
        target = parse_iso(schedule["at"]).astimezone(now.tzinfo)
        return target if target <= now else None
    if kind == "every":
        anchor = parse_iso(schedule["anchor"]).astimezone(now.tzinfo)
        if anchor > now:
            return None
        elapsed = (now - anchor).total_seconds()
        steps = math.floor(elapsed / int(schedule["seconds"]))
        return anchor + dt.timedelta(seconds=steps * int(schedule["seconds"]))
    if kind == "daily":
        for days_back in range(0, 8):
            date = now.date() - dt.timedelta(days=days_back)
            candidate = local_wall_time(
                date,
                int(schedule["hour"]),
                int(schedule["minute"]),
            )
            if candidate is not None and candidate <= now:
                return candidate
        return None
    if kind == "weekly":
        for days_back in range(0, 15):
            date = now.date() - dt.timedelta(days=days_back)
            if date.weekday() != int(schedule["weekday"]):
                continue
            candidate = local_wall_time(
                date,
                int(schedule["hour"]),
                int(schedule["minute"]),
            )
            if candidate is not None and candidate <= now:
                return candidate
        return None
    raise SchedulerError(f"unknown schedule kind: {kind}")


def next_due(schedule: dict[str, Any], now: dt.datetime) -> dt.datetime | None:
    kind = schedule["kind"]
    if kind == "at":
        target = parse_iso(schedule["at"]).astimezone(now.tzinfo)
        return target if target > now else None
    if kind == "every":
        anchor = parse_iso(schedule["anchor"]).astimezone(now.tzinfo)
        if anchor > now:
            return anchor
        elapsed = (now - anchor).total_seconds()
        steps = math.floor(elapsed / int(schedule["seconds"])) + 1
        return anchor + dt.timedelta(seconds=steps * int(schedule["seconds"]))
    if kind == "daily":
        for days_ahead in range(0, 8):
            date = now.date() + dt.timedelta(days=days_ahead)
            candidate = local_wall_time(
                date,
                int(schedule["hour"]),
                int(schedule["minute"]),
            )
            if candidate is not None and candidate > now:
                return candidate
        return None
    if kind == "weekly":
        for days_ahead in range(0, 15):
            date = now.date() + dt.timedelta(days=days_ahead)
            if date.weekday() != int(schedule["weekday"]):
                continue
            candidate = local_wall_time(
                date,
                int(schedule["hour"]),
                int(schedule["minute"]),
            )
            if candidate is not None and candidate > now:
                return candidate
        return None
    raise SchedulerError(f"unknown schedule kind: {kind}")


def occurrence_key(schedule: dict[str, Any], scheduled_for: dt.datetime) -> str:
    if schedule["kind"] in {"daily", "weekly"}:
        return scheduled_for.strftime("%Y-%m-%dT%H:%M")
    return scheduled_for.astimezone(dt.UTC).strftime("%Y-%m-%dT%H:%MZ")


def count_missed(
    schedule: dict[str, Any],
    previous: dt.datetime | None,
    current: dt.datetime,
) -> int:
    if previous is None:
        return 0
    kind = schedule["kind"]
    delta = (current - previous).total_seconds()
    if kind == "every":
        return max(0, int(delta // int(schedule["seconds"])) - 1)
    if kind == "daily":
        return max(0, (current.date() - previous.date()).days - 1)
    if kind == "weekly":
        days = (current.date() - previous.date()).days
        return max(0, days // 7 - 1)
    return 0


def local_wall_time(
    date: dt.date,
    hour: int,
    minute: int,
) -> dt.datetime | None:
    """Resolve a local wall time, returning None across a DST spring gap."""
    naive = dt.datetime.combine(date, dt.time(hour=hour, minute=minute))
    timestamp = time.mktime(naive.timetuple())
    localized = dt.datetime.fromtimestamp(timestamp).astimezone()
    if (
        localized.year,
        localized.month,
        localized.day,
        localized.hour,
        localized.minute,
    ) != (date.year, date.month, date.day, hour, minute):
        return None
    return localized
