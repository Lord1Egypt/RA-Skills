from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, date, datetime, time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from constants import (
    API_BASE_URL,
    CALENDAR_COUNTRY_SCOPE,
    REQUEST_TIMEOUT_SECONDS,
    SITE_BASE_URL,
    USER_AGENT,
    YAHOO_CALENDAR_API_URL,
    YAHOO_FALLBACK_AUTH_SOURCE,
    YAHOO_LANG,
    YAHOO_MAX_COUNT_PER_DAY,
    YAHOO_REGION,
)
from utils import (
    format_day_header,
    format_event_time,
    format_importance,
    get_api_key,
    parse_event_datetime,
    parse_iso_date,
    parse_unix_millis,
)


def build_calendar_url(start_date: date, end_date: date, api_key: str) -> str:
    """Build the TradingEconomics calendar URL for a date range."""
    path = (
        f"/calendar/country/{CALENDAR_COUNTRY_SCOPE}/"
        f"{start_date.isoformat()}/{end_date.isoformat()}"
    )
    query = urlencode({"c": api_key, "f": "json"})
    return f"{API_BASE_URL}{path}?{query}"


def fetch_tradingeconomics_payload(
    start_date: date, end_date: date, api_key: str, loaded_env_file: bool
) -> tuple[list[dict] | None, dict | None]:
    """Fetch raw calendar items from TradingEconomics."""
    url = build_calendar_url(start_date, end_date, api_key)
    request = Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        message = f"TradingEconomics request failed with HTTP {exc.code}."
        if exc.code == 401:
            message += " Check TRADING_ECONOMICS_API_KEY."
        elif exc.code == 403:
            message += " The API key may be blocked or rate-limited."
        elif exc.code == 409:
            message += " TradingEconomics rejected the request due to throttling."
        return None, {
            "error": message,
            "auth_source": "TradingEconomics API",
            "source_type": "tradingeconomics",
            "loaded_env_file": loaded_env_file,
        }
    except URLError as exc:
        return None, {
            "error": f"Could not reach TradingEconomics: {exc.reason}",
            "auth_source": "TradingEconomics API",
            "source_type": "tradingeconomics",
            "loaded_env_file": loaded_env_file,
        }
    except json.JSONDecodeError as exc:
        return None, {
            "error": f"TradingEconomics returned invalid JSON: {exc}",
            "auth_source": "TradingEconomics API",
            "source_type": "tradingeconomics",
            "loaded_env_file": loaded_env_file,
        }

    if not isinstance(payload, list):
        return None, {
            "error": "TradingEconomics returned an unexpected payload.",
            "auth_source": "TradingEconomics API",
            "source_type": "tradingeconomics",
            "loaded_env_file": loaded_env_file,
        }

    return payload, {
        "auth_source": "TradingEconomics API",
        "source_type": "tradingeconomics",
        "loaded_env_file": loaded_env_file,
    }


def build_yahoo_calendar_url(start_date: date, end_date: date) -> str:
    """Build the Yahoo Finance economic calendar endpoint URL."""
    start_dt = datetime.combine(start_date, time.min, tzinfo=UTC)
    end_dt = datetime.combine(end_date, time.max, tzinfo=UTC)
    query = urlencode(
        {
            "countPerDay": str(YAHOO_MAX_COUNT_PER_DAY),
            "economicEventsHighImportanceOnly": "false",
            "economicEventsRegionFilter": "",
            "endDate": str(int(end_dt.timestamp() * 1000)),
            "modules": "economicEvents",
            "startDate": str(int(start_dt.timestamp() * 1000)),
            "lang": YAHOO_LANG,
            "region": YAHOO_REGION,
        }
    )
    return f"{YAHOO_CALENDAR_API_URL}?{query}"


def fetch_yahoo_payload(
    start_date: date, end_date: date, loaded_env_file: bool
) -> tuple[list[dict] | None, dict | None]:
    """Fetch Yahoo Finance calendar day groups for the date range."""
    url = build_yahoo_calendar_url(start_date, end_date)
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Language": f"{YAHOO_LANG},en;q=0.9",
        },
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        return None, {
            "error": f"Yahoo Finance fallback failed with HTTP {exc.code}.",
            "auth_source": YAHOO_FALLBACK_AUTH_SOURCE,
            "source_type": "yahoo",
            "loaded_env_file": loaded_env_file,
        }
    except URLError as exc:
        return None, {
            "error": f"Could not reach Yahoo Finance fallback: {exc.reason}",
            "auth_source": YAHOO_FALLBACK_AUTH_SOURCE,
            "source_type": "yahoo",
            "loaded_env_file": loaded_env_file,
        }
    except json.JSONDecodeError as exc:
        return None, {
            "error": f"Yahoo Finance fallback returned invalid JSON: {exc}",
            "auth_source": YAHOO_FALLBACK_AUTH_SOURCE,
            "source_type": "yahoo",
            "loaded_env_file": loaded_env_file,
        }

    day_groups = payload.get("finance", {}).get("result", {}).get("economicEvents")
    if not isinstance(day_groups, list):
        return None, {
            "error": "Yahoo Finance fallback returned an unexpected payload.",
            "auth_source": YAHOO_FALLBACK_AUTH_SOURCE,
            "source_type": "yahoo",
            "loaded_env_file": loaded_env_file,
        }

    return day_groups, {
        "auth_source": YAHOO_FALLBACK_AUTH_SOURCE,
        "source_type": "yahoo",
        "loaded_env_file": loaded_env_file,
    }


def normalize_tradingeconomics_event(item: dict) -> dict | None:
    """Normalize a TradingEconomics calendar row into a stable shape."""
    if not isinstance(item, dict):
        return None

    event_dt = parse_event_datetime(item.get("Date"))
    event_date = event_dt.date() if event_dt is not None else None
    relative_url = item.get("URL") or ""
    event_url = (
        f"{SITE_BASE_URL}{relative_url}"
        if relative_url.startswith("/")
        else relative_url
    )

    return {
        "calendar_id": item.get("CalendarId"),
        "date": event_date,
        "datetime": event_dt,
        "time_label": format_event_time(event_dt, item.get("DateSpan")),
        "country": item.get("Country") or "Unknown",
        "category": item.get("Category") or "Unknown",
        "event": item.get("Event") or item.get("Category") or "Unknown",
        "reference": item.get("Reference") or "",
        "actual": item.get("Actual") or "",
        "previous": item.get("Previous") or "",
        "forecast": item.get("Forecast") or "",
        "te_forecast": item.get("TEForecast") or "",
        "revised_from": item.get("Revised") or "",
        "importance": format_importance(item.get("Importance")),
        "importance_rank": _coerce_importance_rank(item.get("Importance")),
        "source": item.get("Source") or "",
        "url": event_url,
    }


def normalize_yahoo_event(day_date: date, record: dict) -> dict | None:
    """Normalize a Yahoo Finance calendar event into the shared output shape."""
    if not isinstance(record, dict):
        return None

    event_dt = parse_unix_millis(record.get("eventTime"))

    return {
        "calendar_id": None,
        "date": day_date,
        "datetime": event_dt,
        "time_label": format_event_time(event_dt, None),
        "country": record.get("countryCode") or "Unknown",
        "category": "Economic Event",
        "event": record.get("event") or "Unknown",
        "reference": record.get("period") or "",
        "actual": record.get("actual") or "",
        "previous": record.get("prior") or "",
        "forecast": "",
        "te_forecast": "",
        "revised_from": record.get("revisedFrom") or "",
        "importance": "",
        "importance_rank": 0,
        "source": "Yahoo Finance",
        "url": "",
    }


def _coerce_importance_rank(value) -> int:
    """Coerce importance into an integer for sorting."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def filter_and_sort_events(
    raw_events: list[dict], start_date: date, end_date: date
) -> tuple[list[dict], int]:
    """Normalize, filter, and sort fetched calendar events."""
    normalized = []
    out_of_range_count = 0

    for raw_event in raw_events:
        event = normalize_tradingeconomics_event(raw_event)
        if event is None or event["date"] is None:
            continue

        if start_date <= event["date"] <= end_date:
            normalized.append(event)
        else:
            out_of_range_count += 1

    normalized.sort(
        key=lambda item: (
            item["date"],
            item["datetime"] is None,
            item["datetime"] or item["date"],
            -item["importance_rank"],
            item["country"],
            item["event"],
        )
    )
    return normalized, out_of_range_count


def normalize_and_sort_yahoo_events(
    day_groups: list[dict], start_date: date, end_date: date
) -> tuple[list[dict], list[str]]:
    """Normalize and sort Yahoo Finance fallback events."""
    normalized = []
    truncated_days = []

    for day_group in day_groups:
        if not isinstance(day_group, dict):
            continue

        timestamp_string = day_group.get("timestampString")
        if not timestamp_string:
            continue

        try:
            day_date = parse_iso_date(timestamp_string)
        except ValueError:
            continue

        if not (start_date <= day_date <= end_date):
            continue

        count = day_group.get("count")
        total_count = day_group.get("totalCount")
        if count != total_count:
            truncated_days.append(
                f"{timestamp_string} ({count} returned / {total_count} total)"
            )

        records = day_group.get("records")
        if not isinstance(records, list):
            continue

        for record in records:
            event = normalize_yahoo_event(day_date, record)
            if event is not None:
                normalized.append(event)

    normalized.sort(
        key=lambda item: (
            item["date"],
            item["datetime"] is None,
            item["datetime"] or item["date"],
            item["country"],
            item["event"],
        )
    )
    return normalized, truncated_days


def build_yahoo_warning(auth_source: str, truncated_days: list[str]) -> str | None:
    """Describe Yahoo fallback limitations when richer fields are unavailable."""
    if auth_source != YAHOO_FALLBACK_AUTH_SOURCE:
        return None

    message = (
        "Yahoo Finance fallback is active, so country values are returned as codes and "
        "importance or market-expectation fields may be unavailable."
    )
    if truncated_days:
        message += (
            " Some days hit Yahoo's per-day limit of 100 events: "
            + ", ".join(truncated_days[:5])
            + ("." if len(truncated_days) <= 5 else ", ...")
        )
    return message


def get_economic_calendar(start_date: date, end_date: date) -> dict:
    """Fetch and prepare calendar data for the requested range."""
    api_key, auth_source, loaded_env_file = get_api_key()

    if api_key:
        raw_events, meta = fetch_tradingeconomics_payload(
            start_date, end_date, api_key, loaded_env_file
        )
    else:
        raw_events, meta = fetch_yahoo_payload(start_date, end_date, loaded_env_file)

    if raw_events is None:
        return meta or {"error": "Could not fetch economic calendar."}

    meta = meta or {
        "auth_source": auth_source or "unknown",
        "source_type": "unknown",
        "loaded_env_file": loaded_env_file,
    }

    truncated_days: list[str] = []
    if meta["source_type"] == "tradingeconomics":
        filtered_events, out_of_range_count = filter_and_sort_events(
            raw_events, start_date, end_date
        )
        if out_of_range_count > 0:
            truncated_days.append(
                f"TradingEconomics returned {out_of_range_count} out-of-range items that were filtered out"
            )
    else:
        filtered_events, truncated_days = normalize_and_sort_yahoo_events(
            raw_events, start_date, end_date
        )

    warning = build_yahoo_warning(meta["auth_source"], truncated_days)

    grouped_events = defaultdict(list)
    for event in filtered_events:
        grouped_events[event["date"]].append(event)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "events": filtered_events,
        "grouped_events": dict(grouped_events),
        "event_count": len(filtered_events),
        "day_count": len(grouped_events),
        "auth_source": meta["auth_source"],
        "loaded_env_file": meta["loaded_env_file"],
        "warning": warning,
    }


def format_event_details(event: dict) -> str:
    """Format the secondary metrics for a single calendar event."""
    fields = []

    if event["reference"]:
        fields.append(f"Ref: {event['reference']}")
    if event["actual"]:
        fields.append(f"Actual: {event['actual']}")
    if event["forecast"]:
        fields.append(f"Forecast: {event['forecast']}")
    elif event["te_forecast"]:
        fields.append(f"TE Forecast: {event['te_forecast']}")
    if event["previous"]:
        fields.append(f"Previous: {event['previous']}")
    if event.get("revised_from"):
        fields.append(f"Revised From: {event['revised_from']}")

    return " | ".join(fields)


def format_output(data: dict) -> str:
    """Format the calendar response into readable CLI output."""
    if "error" in data:
        return f"Error: {data['error']}"

    lines = [
        (
            "Economic Calendar: "
            f"{data['start_date'].isoformat()} to {data['end_date'].isoformat()}"
        ),
        (
            f"Auth: {data['auth_source']}"
            + (" (.env loaded)" if data.get("loaded_env_file") else "")
        ),
        f"Events: {data['event_count']} across {data['day_count']} day(s)",
    ]

    if data.get("warning"):
        lines.append(f"Warning: {data['warning']}")

    if not data["events"]:
        lines.append("No economic calendar events matched the requested date range.")
        return "\n".join(lines)

    for event_date in sorted(data["grouped_events"]):
        lines.extend(["", format_day_header(event_date)])
        for event in data["grouped_events"][event_date]:
            if event["importance"]:
                lines.append(
                    f"- {event['time_label']} | {event['country']} | {event['importance']} | {event['event']}"
                )
            else:
                lines.append(
                    f"- {event['time_label']} | {event['country']} | {event['event']}"
                )

            details = format_event_details(event)
            if details:
                lines.append(f"  {details}")

            if event["url"]:
                lines.append(f"  Link: {event['url']}")

    return "\n".join(lines)
