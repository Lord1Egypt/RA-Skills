"""Date and numeric coercion helpers used across many scripts."""

from __future__ import annotations

from datetime import datetime, timezone


def parse_date(value: str | None) -> datetime | None:
    """Parse common AC v3 timestamp shapes into a timezone-aware datetime.

    Accepts ISO 8601 (with or without trailing Z), `YYYY-MM-DD HH:MM:SS`,
    and bare `YYYY-MM-DD`. Naive results are coerced to UTC. Returns None
    on any unrecognized input.
    """
    if not value:
        return None
    # try permissive ISO 8601 first via fromisoformat
    try:
        s = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value.replace("Z", "+0000"), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def safe_int(value, default: int = 0) -> int:
    """Coerce loose API values to int; returns `default` on failure."""
    try:
        return int(float(value or default))
    except (ValueError, TypeError):
        return default


def safe_float(value, default: float = 0.0) -> float:
    """Coerce loose API values to float; returns `default` on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
