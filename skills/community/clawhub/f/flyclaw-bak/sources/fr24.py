"""FlightRadar24 non-official API data source.

Queries the FR24 public flight list endpoint.  Best for international
flights: departure/arrival times, delay, aircraft, status.
"""

import logging
import time
from datetime import datetime, timezone

import requests

import config as cfg
from airport_manager import airport_manager

logger = logging.getLogger("flyclaw.fr24")

_HEADERS = {
    "User-Agent": cfg.USER_AGENT,
    "Origin": "https://www.flightradar24.com",
    "Referer": "https://www.flightradar24.com/",
    "Accept": "application/json",
}

_FLIGHT_LIST_URL = f"{cfg.FR24_API_BASE}/flight/list.json"


def _ts_to_iso(ts) -> str | None:
    """Convert unix timestamp to ISO-8601 string, or None."""
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat()
    except (ValueError, TypeError, OSError):
        return None


def _parse_flight(raw: dict) -> dict:
    """Normalise one FR24 flight record into the standard schema."""
    ident = raw.get("identification", {}) or {}
    number_info = ident.get("number", {}) or {}
    flight_number = number_info.get("default", "")

    airport = raw.get("airport", {}) or {}
    origin = airport.get("origin", {}) or {}
    dest = airport.get("destination", {}) or {}

    origin_iata = (origin.get("code") or {}).get("iata", "")
    dest_iata = (dest.get("code") or {}).get("iata", "")

    origin_city = (origin.get("position", {}).get("region", {}) or {}).get("city", "")
    dest_city = (dest.get("position", {}).get("region", {}) or {}).get("city", "")

    # Enrich with AirportManager display names
    origin_display = airport_manager.get_display_name(origin_iata) if origin_iata else origin_city
    dest_display = airport_manager.get_display_name(dest_iata) if dest_iata else dest_city

    time_info = raw.get("time", {}) or {}
    sched = time_info.get("scheduled", {}) or {}
    real = time_info.get("real", {}) or {}

    status_info = raw.get("status", {}) or {}
    status_text = status_info.get("text", "")

    aircraft_info = raw.get("aircraft", {}) or {}
    model = (aircraft_info.get("model") or {})
    aircraft_text = model.get("text") or model.get("code") or ""

    airline_info = raw.get("airline", {}) or {}
    airline_name = ""
    if airline_info:
        airline_name = airline_info.get("name", "") or ""

    # Calculate delay
    delay = None
    sched_dep = sched.get("departure")
    real_dep = real.get("departure")
    if sched_dep and real_dep:
        delay = (int(real_dep) - int(sched_dep)) // 60

    return {
        "flight_number": flight_number,
        "airline": airline_name,
        "origin_iata": origin_iata,
        "origin_city": origin_display,
        "destination_iata": dest_iata,
        "destination_city": dest_display,
        "scheduled_departure": _ts_to_iso(sched.get("departure")),
        "scheduled_arrival": _ts_to_iso(sched.get("arrival")),
        "actual_departure": _ts_to_iso(real.get("departure")),
        "actual_arrival": _ts_to_iso(real.get("arrival")),
        "status": status_text,
        "aircraft_type": aircraft_text,
        "delay_minutes": delay,
        "price": None,
        "source": "fr24",
    }


class FR24Source:
    """FlightRadar24 data source."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def query_by_flight(self, flight_number: str) -> list[dict]:
        """Query by flight number (e.g. 'CA981')."""
        params = {
            "query": flight_number.upper(),
            "fetchBy": "flight",
            "page": 1,
            "limit": 25,
        }
        return self._fetch(params)

    def query_by_route(
        self, origin: str, destination: str, date: str | None = None
    ) -> list[dict]:
        """Query by route. FR24 flight list API only supports flight/reg
        queries, not airport-based route queries. We return empty here;
        route search relies on Google Flights."""
        # FR24's public endpoint doesn't support airport-based route lookup.
        # Route queries are handled by Google Flights source.
        logger.debug("FR24 does not support route queries, skipping")
        return []

    def _fetch(self, params: dict) -> list[dict]:
        """Execute HTTP request and parse results."""
        try:
            logger.debug("FR24 request: %s", params)
            resp = requests.get(
                _FLIGHT_LIST_URL,
                headers=_HEADERS,
                params=params,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.warning("FR24 request failed: %s", e)
            return []
        except ValueError as e:
            logger.warning("FR24 JSON parse error: %s", e)
            return []

        try:
            items = data["result"]["response"]["data"]
            if not items:
                return []
        except (KeyError, TypeError):
            logger.warning("Unexpected FR24 response structure")
            return []

        results = []
        for item in items:
            try:
                results.append(_parse_flight(item))
            except Exception as e:
                logger.debug("Skipping malformed FR24 record: %s", e)
        return results
