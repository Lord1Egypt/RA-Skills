"""Date utilities for /depradar."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Optional


# ── Public helpers ──────────────────────────────────────────────────────────

def today_utc() -> str:
    """Return today's date as YYYY-MM-DD (UTC)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def days_ago(n: int) -> str:
    """Return the date N days ago as YYYY-MM-DD (UTC)."""
    return (datetime.now(timezone.utc) - timedelta(days=n)).strftime("%Y-%m-%d")


def days_since(date_str: str) -> Optional[int]:
    """Return how many days have elapsed since *date_str* (YYYY-MM-DD).

    Returns ``None`` if the string cannot be parsed.
    """
    parsed = _try_parse(date_str)
    if parsed is None:
        return None
    delta = datetime.now(timezone.utc) - parsed.replace(tzinfo=timezone.utc)
    return max(0, delta.days)


def is_within_days(date_str: str, days: int) -> Optional[bool]:
    """Return True if *date_str* falls within the last *days* days.

    Returns ``None`` if the date cannot be determined (treat as unknown).
    """
    n = days_since(date_str)
    if n is None:
        return None
    return n <= days


def parse_iso(date_str: str) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp (with or without timezone) into a UTC
    datetime object.  Returns ``None`` on failure.
    """
    return _try_parse(date_str)


def format_relative(date_str: str) -> str:
    """Return a human-readable relative string: '3 days ago', '2 months ago', etc."""
    n = days_since(date_str)
    if n is None:
        return "unknown date"
    if n == 0:
        return "today"
    if n == 1:
        return "1 day ago"
    if n < 7:
        return f"{n} days ago"
    if n < 14:
        return "1 week ago"
    if n < 30:
        return f"{n // 7} weeks ago"
    if n < 60:
        return "1 month ago"
    if n < 365:
        return f"{n // 30} months ago"
    return f"{n // 365} year{'s' if n >= 730 else ''} ago"


def recency_score(date_str: Optional[str]) -> int:
    """Return a 0-100 recency score. Higher = more recent.

    Scoring table:
      0–7 days   → 100
      8–14 days  → 85
      15–30 days → 65
      31–60 days → 40
      61–90 days → 25
      91+ days   → 10
      unknown    → 50
    """
    if not date_str:
        return 50
    n = days_since(date_str)
    if n is None:
        return 50
    if n <= 7:
        return 100
    if n <= 14:
        return 85
    if n <= 30:
        return 65
    if n <= 60:
        return 40
    if n <= 90:
        return 25
    return 10


# ── Internal ────────────────────────────────────────────────────────────────

_ISO_FORMATS = (
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
)

_FUZZY_PATTERN = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def _try_parse(s: str) -> Optional[datetime]:
    if not s:
        return None
    s = s.strip()
    # Strip fractional seconds that strptime can't handle uniformly
    s_clean = re.sub(r"\.\d+", "", s)
    for fmt in _ISO_FORMATS:
        try:
            dt = datetime.strptime(s_clean, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            pass
    # Last resort: grep for YYYY-MM-DD
    m = _FUZZY_PATTERN.search(s)
    if m:
        try:
            return datetime(
                int(m.group(1)), int(m.group(2)), int(m.group(3)),
                tzinfo=timezone.utc,
            )
        except ValueError:
            pass
    return None
