from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from pathlib import Path


CHINESE_TIME_WINDOW_PATTERN = re.compile(
    r"^\s*"
    r"(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})点(?:((?:\d{1,2}))分?)?"
    r"\s*到\s*"
    r"(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})点(?:((?:\d{1,2}))分?)?"
    r"\s*$"
)
ISO_TIME_WINDOW_PATTERN = re.compile(
    r"^\s*"
    r"(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?"
    r"\s+to\s+"
    r"(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?"
    r"\s*$",
    re.IGNORECASE,
)


def build_daily_report_window(*, now: datetime | None = None, end_hour: int = 8) -> tuple[datetime, datetime]:
    current = now or datetime.now()
    end = datetime.combine(current.date(), time(hour=end_hour))
    start = datetime.combine(current.date() - timedelta(days=1), time.min)
    return start, end


def format_chinese_time_window(start: datetime, end: datetime) -> str:
    def format_one(value: datetime) -> str:
        if value.minute:
            return f"{value.year}年{value.month}月{value.day}日{value.hour}点{value.minute}分"
        return f"{value.year}年{value.month}月{value.day}日{value.hour}点"

    return f"{format_one(start)}到{format_one(end)}"


def default_daily_report_window_text(*, now: datetime | None = None, end_hour: int = 8) -> str:
    start, end = build_daily_report_window(now=now, end_hour=end_hour)
    return format_chinese_time_window(start, end)


def parse_time_window(value: str) -> tuple[datetime, datetime]:
    match = CHINESE_TIME_WINDOW_PATTERN.match(value)
    if match:
        groups = match.groups()
        start = datetime(
            year=int(groups[0]),
            month=int(groups[1]),
            day=int(groups[2]),
            hour=int(groups[3]),
            minute=int(groups[4] or 0),
        )
        end = datetime(
            year=int(groups[5]),
            month=int(groups[6]),
            day=int(groups[7]),
            hour=int(groups[8]),
            minute=int(groups[9] or 0),
        )
        if end < start:
            raise ValueError("The time window end cannot be earlier than the start.")
        return start, end

    match = ISO_TIME_WINDOW_PATTERN.match(value)
    if match:
        groups = match.groups()
        start = datetime(
            year=int(groups[0]),
            month=int(groups[1]),
            day=int(groups[2]),
            hour=int(groups[3]),
            minute=int(groups[4]),
            second=int(groups[5] or 0),
        )
        end = datetime(
            year=int(groups[6]),
            month=int(groups[7]),
            day=int(groups[8]),
            hour=int(groups[9]),
            minute=int(groups[10]),
            second=int(groups[11] or 0),
        )
        if end < start:
            raise ValueError("The time window end cannot be earlier than the start.")
        return start, end

    raise ValueError(
        "Invalid time window format. Use '2026年3月15日0点到2026年3月16日8点' "
        "or '2026-03-15 00:00 to 2026-03-16 08:00'."
    )


def parse_record_datetime(value: str) -> datetime | None:
    cleaned = (value or "").strip()
    if not cleaned:
        return None

    try:
        dt = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        return None

    if dt.tzinfo is not None:
        return dt.astimezone().replace(tzinfo=None)
    return dt


def in_time_window(value: str, start: datetime, end: datetime) -> bool:
    dt = parse_record_datetime(value)
    if dt is None:
        return False
    return start <= dt <= end


def target_date_strings_from_window(start: datetime, end: datetime, *, prefix: str = "") -> list[str]:
    dates: list[str] = []
    current: date = start.date()
    end_date = end.date()
    while current <= end_date:
        date_text = current.isoformat()
        dates.append(f"{prefix}{date_text}" if prefix else date_text)
        current += timedelta(days=1)
    return dates


def existing_paths_from_stems(base_dir: Path, stems: list[str], suffix: str = ".jsonl") -> list[Path]:
    paths: list[Path] = []
    for stem in stems:
        path = base_dir / f"{stem}{suffix}"
        if path.exists():
            paths.append(path)
    return paths
