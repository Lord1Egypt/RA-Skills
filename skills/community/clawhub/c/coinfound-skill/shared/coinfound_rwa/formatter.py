from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

COMPACT_UNITS = (
    (1_000_000_000_000, "T"),
    (1_000_000_000, "B"),
    (1_000_000, "M"),
    (1_000, "K"),
)

TIME_KEYS = {
    "time",
    "reportdate",
    "inceptiondate",
}


def format_display_data(value: Any, field_name: str | None = None) -> Any:
    if isinstance(value, dict):
        return {key: format_display_data(item, key) for key, item in value.items()}
    if isinstance(value, list):
        return [format_display_data(item, field_name) for item in value]
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        if is_time_like(field_name, value):
            return format_timestamp(value)
        return format_number(value)
    return value


def format_number(value: int | float) -> str:
    absolute = abs(float(value))
    for threshold, unit in COMPACT_UNITS:
        if absolute >= threshold:
            return f"{trim_number(float(value) / threshold, 2)}{unit}"
    if float(value).is_integer():
        return str(int(value))
    return trim_number(float(value), 4)


def trim_number(value: float, digits: int) -> str:
    text = f"{value:.{digits}f}"
    if "." not in text:
        return text
    return text.rstrip("0").rstrip(".")


def is_time_like(field_name: str | None, value: int | float) -> bool:
    if not field_name:
        return False
    normalized = "".join(ch for ch in field_name.lower() if ch.isalnum())
    if normalized in TIME_KEYS or normalized.endswith("timestamp"):
        return True
    if normalized.endswith("time") or normalized.endswith("date"):
        return True
    return False


def format_timestamp(value: int | float) -> str:
    timestamp = float(value)
    if timestamp > 100_000_000_000:
        timestamp /= 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
