from __future__ import annotations

import os
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from constants import API_KEY_ENV_VAR, DEFAULT_RANGE_DAYS


def parse_iso_date(value: str) -> date:
    """Parse a YYYY-MM-DD string into a date."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid date '{value}'. Use YYYY-MM-DD format.") from exc


def resolve_date_range(args: list[str]) -> tuple[date, date]:
    """Resolve CLI args into an inclusive start/end date range."""
    today = datetime.now(UTC).date()

    if not args:
        return today, today + timedelta(days=DEFAULT_RANGE_DAYS)
    if len(args) == 1:
        start_date = parse_iso_date(args[0])
        return start_date, start_date + timedelta(days=DEFAULT_RANGE_DAYS)
    if len(args) == 2:
        start_date = parse_iso_date(args[0])
        end_date = parse_iso_date(args[1])
        if end_date < start_date:
            raise ValueError("End date must be on or after the start date.")
        return start_date, end_date

    raise ValueError(
        "Usage: economic-calendar-pro [START_DATE] [END_DATE]\n"
        "Examples:\n"
        "  economic-calendar-pro\n"
        "  economic-calendar-pro 2026-03-10\n"
        "  economic-calendar-pro 2026-03-10 2026-03-24"
    )


def parse_event_datetime(value: str | None) -> datetime | None:
    """Parse the TradingEconomics event timestamp."""
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_unix_millis(value) -> datetime | None:
    """Parse a unix-millis timestamp into a UTC datetime."""
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=UTC)
    except (TypeError, ValueError, OSError):
        return None


def format_day_header(value: date) -> str:
    """Format a day header for grouped output."""
    return value.strftime("%A, %Y-%m-%d")


def format_event_time(event_dt: datetime | None, date_span: str | None) -> str:
    """Format an event timestamp in UTC or all-day form."""
    if date_span == "1":
        return "All day"
    if event_dt is None:
        return "Unknown"

    if event_dt.tzinfo is None:
        event_dt = event_dt.replace(tzinfo=UTC)
    else:
        event_dt = event_dt.astimezone(UTC)

    return event_dt.strftime("%H:%M UTC")


def format_importance(value) -> str:
    """Convert numeric importance into a readable label."""
    try:
        importance = int(value)
    except (TypeError, ValueError):
        return "Unknown"

    return {
        1: "Low",
        2: "Medium",
        3: "High",
    }.get(importance, str(importance))


def repo_root() -> Path:
    """Return the repository root from this skill file."""
    return Path(__file__).resolve().parents[3]


def _strip_wrapping_quotes(value: str) -> str:
    """Remove matching wrapping quotes from a dotenv value."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def load_env_file_if_present() -> bool:
    """Load a nearby .env file without overriding existing environment values."""
    candidates = []
    seen = set()

    for base in (Path.cwd(), repo_root()):
        for candidate in (base / ".env",):
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            candidates.append(candidate)

    loaded = False
    for candidate in candidates:
        if not candidate.is_file():
            continue

        for raw_line in candidate.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = _strip_wrapping_quotes(value.strip())
            if key:
                os.environ.setdefault(key, value)

        loaded = True

    return loaded


def get_api_key() -> tuple[str, str, bool]:
    """Return the configured API key, auth source, and dotenv load status."""
    loaded_env_file = load_env_file_if_present()
    api_key = os.environ.get(API_KEY_ENV_VAR, "").strip()

    if api_key:
        return api_key, API_KEY_ENV_VAR, loaded_env_file

    return "", "", loaded_env_file
