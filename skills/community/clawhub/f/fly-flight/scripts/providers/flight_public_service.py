#!/usr/bin/env python3
"""Flight provider for querying China domestic flights from public Tongcheng pages."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "assets" / "data"
PUBLIC_PROVIDER_URL_TEMPLATE = "https://www.ly.com/flights/itinerary/oneway/{departure}-{arrival}?date={departure_date}"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
SORT_MODES = {"price", "departure", "arrival", "duration"}


def load_json(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


CITY_CODES = load_json(DATA_DIR / "domestic_city_codes.json")
AIRPORT_ALIASES = load_json(DATA_DIR / "airport_aliases.json")


@dataclass(frozen=True)
class Place:
    raw: str
    query: str
    code: str
    resolved_as: str


def canonicalize_place(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("地点不能为空")
    if len(cleaned) == 3 and cleaned.isalpha():
        return cleaned.upper()
    for suffix in ("特别行政区", "自治区", "自治州", "省", "市"):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
            break
    return cleaned.replace(" ", "")


def resolve_place(value: str) -> Place:
    normalized = canonicalize_place(value)
    if len(normalized) == 3 and normalized.isalpha():
        code = normalized.upper()
        return Place(raw=value, query=normalized, code=code, resolved_as="iata")
    if normalized in AIRPORT_ALIASES:
        code = AIRPORT_ALIASES[normalized]
        return Place(raw=value, query=normalized, code=code, resolved_as="airport")
    if normalized in CITY_CODES:
        code = CITY_CODES[normalized]
        return Place(raw=value, query=normalized, code=code, resolved_as="city")
    raise ValueError(f"无法识别地点“{value}”。请改用常见城市名、具体机场名，或直接提供三字码。")


def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期必须是 YYYY-MM-DD 格式") from exc
    return value


def fetch_html(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "ignore")


def extract_state_from_html(html: str) -> dict[str, Any]:
    script_path = ROOT / "scripts" / "extract_tongcheng_state.js"
    completed = subprocess.run(
        ["node", str(script_path)],
        input=html,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        error = completed.stderr.strip() or completed.stdout.strip() or "unknown extractor error"
        raise RuntimeError(f"公开页面解析失败: {error}")
    return json.loads(completed.stdout)


def parse_time_duration(value: str) -> str:
    if not value:
        return ""
    return value.replace("小时", "h").replace("分钟", "m")


def duration_minutes(value: str) -> int:
    if not value:
        return 10**9
    hours = 0
    minutes = 0
    if "h" in value:
        left, _, rest = value.partition("h")
        hours = int(left or 0)
        value = rest
    if "m" in value:
        minutes = int(value.replace("m", "") or 0)
    return hours * 60 + minutes


def time_sort_value(date_value: str | None, time_value: str | None) -> str:
    return f"{date_value or '9999-99-99'}T{time_value or '99:99'}"


def simplify_flight(item: dict[str, Any]) -> dict[str, Any]:
    ticket_price = item.get("flightPrice")
    if not ticket_price:
        prices = item.get("productPrices") or {}
        ticket_price = next(iter(prices.values()), None)

    return {
        "airline_code": item.get("airCompanyCode"),
        "airline_name": item.get("airCompanyName"),
        "flight_no": item.get("flightNo"),
        "equipment": item.get("equipmentName"),
        "is_codeshare": False,
        "departure_code": item.get("originAirportCode"),
        "departure_name": item.get("originAirportShortName") or item.get("oapname"),
        "departure_date": (item.get("flyOffTime") or "").split(" ")[0],
        "departure_time": item.get("flyOffOnlyTime"),
        "arrival_code": item.get("arriveAirportCode"),
        "arrival_name": item.get("arriveAirportShortName") or item.get("aapname"),
        "arrival_date": (item.get("arrivalTime") or "").split(" ")[0],
        "arrival_time": item.get("arrivalOnlyTime"),
        "duration": parse_time_duration(item.get("spantime", "")),
        "segments": int(item.get("stopNum", 0)) + 1,
        "ticket_price": ticket_price,
        "raw": item,
    }


def matches_airline(flight: dict[str, Any], airline: str | None) -> bool:
    if not airline:
        return True
    query = airline.strip().lower()
    return query in (flight.get("airline_code") or "").lower() or query in (
        flight.get("airline_name") or ""
    ).lower()


def filter_flights(
    flights: list[dict[str, Any]],
    *,
    direct_only: bool,
    preferred_departure_airport: str | None,
    preferred_arrival_airport: str | None,
    airline: str | None,
) -> list[dict[str, Any]]:
    departure_code = resolve_place(preferred_departure_airport).code if preferred_departure_airport else None
    arrival_code = resolve_place(preferred_arrival_airport).code if preferred_arrival_airport else None

    filtered = flights
    if direct_only:
        filtered = [flight for flight in filtered if int(flight.get("segments") or 0) <= 1]
    if departure_code:
        filtered = [flight for flight in filtered if flight.get("departure_code") == departure_code]
    if arrival_code:
        filtered = [flight for flight in filtered if flight.get("arrival_code") == arrival_code]
    if airline:
        filtered = [flight for flight in filtered if matches_airline(flight, airline)]
    return filtered


def sort_flights(flights: list[dict[str, Any]], sort_by: str) -> list[dict[str, Any]]:
    if sort_by == "departure":
        return sorted(
            flights,
            key=lambda item: (
                time_sort_value(item.get("departure_date"), item.get("departure_time")),
                item.get("ticket_price") is None,
                item.get("ticket_price", 0),
            ),
        )
    if sort_by == "arrival":
        return sorted(
            flights,
            key=lambda item: (
                time_sort_value(item.get("arrival_date"), item.get("arrival_time")),
                item.get("ticket_price") is None,
                item.get("ticket_price", 0),
            ),
        )
    if sort_by == "duration":
        return sorted(
            flights,
            key=lambda item: (
                duration_minutes(item.get("duration") or ""),
                item.get("ticket_price") is None,
                item.get("ticket_price", 0),
            ),
        )
    return sorted(flights, key=lambda item: (item.get("ticket_price") is None, item.get("ticket_price", 0)))


def normalize_leg_response(
    state_payload: dict[str, Any],
    origin: Place,
    destination: Place,
    departure_date: str,
    limit: int,
    *,
    sort_by: str,
    direct_only: bool,
    preferred_departure_airport: str | None,
    preferred_arrival_airport: str | None,
    airline: str | None,
) -> dict[str, Any]:
    flights = [simplify_flight(item) for item in (state_payload.get("flightLists") or [])]
    flights = [item for item in flights if item.get("flight_no")]
    flights = filter_flights(
        flights,
        direct_only=direct_only,
        preferred_departure_airport=preferred_departure_airport,
        preferred_arrival_airport=preferred_arrival_airport,
        airline=airline,
    )
    flights = sort_flights(flights, sort_by=sort_by)
    trimmed = flights[:limit]

    return {
        "provider_reference": state_payload.get("cid"),
        "route": {
            "from": {"input": origin.raw, "query": origin.query, "code": origin.code, "resolved_as": origin.resolved_as},
            "to": {"input": destination.raw, "query": destination.query, "code": destination.code, "resolved_as": destination.resolved_as},
            "date": departure_date,
        },
        "count": len(trimmed),
        "total_found": len(flights),
        "sort_by": sort_by,
        "filters": {
            "direct_only": direct_only,
            "preferred_departure_airport": preferred_departure_airport,
            "preferred_arrival_airport": preferred_arrival_airport,
            "airline": airline,
        },
        "options": trimmed,
    }


def fetch_state_payload(
    origin: Place,
    destination: Place,
    departure_date: str,
    *,
    timeout: int,
    sample_state: str | None,
) -> dict[str, Any]:
    if sample_state:
        with open(sample_state, "r", encoding="utf-8") as handle:
            return json.load(handle)
    url = PUBLIC_PROVIDER_URL_TEMPLATE.format(
        departure=quote(origin.code),
        arrival=quote(destination.code),
        departure_date=quote(departure_date),
    )
    html = fetch_html(url, timeout=timeout)
    return extract_state_from_html(html)


def build_search_namespace(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        origin=args.origin,
        destination=args.destination,
        date=args.date,
        return_date=args.return_date,
        limit=args.limit,
        timeout=args.timeout,
        sort_by=args.sort_by,
        return_sort_by=args.return_sort_by,
        direct_only=args.direct_only,
        airline=args.airline,
        preferred_departure_airport=args.preferred_departure_airport,
        preferred_arrival_airport=args.preferred_arrival_airport,
        return_preferred_departure_airport=args.return_preferred_departure_airport,
        return_preferred_arrival_airport=args.return_preferred_arrival_airport,
        sample_state=args.sample_state,
        return_sample_state=args.return_sample_state,
    )


def run_search(args: argparse.Namespace) -> dict[str, Any]:
    origin = resolve_place(args.origin)
    destination = resolve_place(args.destination)
    departure_date = validate_date(args.date)
    if args.sort_by not in SORT_MODES:
        raise ValueError(f"sort_by 仅支持 {', '.join(sorted(SORT_MODES))}")

    outbound_state = fetch_state_payload(
        origin,
        destination,
        departure_date,
        timeout=args.timeout,
        sample_state=args.sample_state,
    )
    outbound = normalize_leg_response(
        outbound_state,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        limit=args.limit,
        sort_by=args.sort_by,
        direct_only=args.direct_only,
        preferred_departure_airport=args.preferred_departure_airport,
        preferred_arrival_airport=args.preferred_arrival_airport,
        airline=args.airline,
    )

    payload: dict[str, Any] = {
        "mode": "flight",
        "provider": "tongcheng-public-page",
        "reason": "success",
        "trip_type": "round-trip" if args.return_date else "one-way",
        "outbound": outbound,
    }

    if args.return_date:
        return_date = validate_date(args.return_date)
        return_state = fetch_state_payload(
            destination,
            origin,
            return_date,
            timeout=args.timeout,
            sample_state=args.return_sample_state or args.sample_state,
        )
        payload["return"] = normalize_leg_response(
            return_state,
            origin=destination,
            destination=origin,
            departure_date=return_date,
            limit=args.limit,
            sort_by=args.return_sort_by or args.sort_by,
            direct_only=args.direct_only,
            preferred_departure_airport=args.return_preferred_departure_airport,
            preferred_arrival_airport=args.return_preferred_arrival_airport,
            airline=args.airline,
        )
    return payload
