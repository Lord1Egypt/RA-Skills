"""Skiplagged data source — free REST API for flight prices.

Best for: flight prices (especially Chinese domestic airlines),
route-based search with full price coverage.

Does NOT provide: real-time flight tracking, aircraft type, delay info.

Key characteristics:
- 100% price coverage for Chinese domestic routes
- Covers 25+ Chinese airlines
- No authentication required
- Returns prices in USD cents (converted to dollars)
- ISO 8601 timestamps with timezone offsets
"""

import logging
from datetime import datetime

from curl_cffi import requests as cf_requests

from airport_manager import airport_manager

logger = logging.getLogger("flyclaw.skiplagged")

BASE_URL = "https://skiplagged.com/api/search.php"


class _TransientError(Exception):
    """Transient error (timeout, connection reset) — worth retrying."""
    pass


class SkiplaggedSource:
    """Skiplagged flight search data source."""

    def __init__(self, timeout: int = 15, retry: int = 3,
                 mcp_enabled: bool = False, mcp_url: str = "",
                 retry_delay: float = 0.5, retry_backoff: float = 2.0):
        self.timeout = timeout
        self.max_retries = retry
        self.mcp_enabled = mcp_enabled
        self.mcp_url = mcp_url
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff

    def query_by_flight(self, flight_number: str) -> list[dict]:
        """Skiplagged does not support flight number queries."""
        return []

    def query_by_route(
        self, origin: str, destination: str, date: str,
        *, adults: int = 1, stops: int | str = 0,
        cabin: str = "economy", limit: int | None = None,
        timeout: int | None = None,
        return_date: str | None = None,
    ) -> list[dict]:
        """Query flights by route.

        Args:
            origin: IATA code (e.g. "KMG")
            destination: IATA code (e.g. "NKG")
            date: Travel date YYYY-MM-DD
            adults: Number of passengers (unused by SK API but kept for interface)
            stops: Max stops filter (0=nonstop, 1, 2, "any")
            cabin: Cabin class (economy/business/first via fare_class param)
            limit: Max results to return
            timeout: Override instance timeout
            return_date: Return date YYYY-MM-DD for round-trip queries

        Returns:
            List of FlyClaw standard record dicts.
        """
        effective_timeout = timeout if timeout is not None else self.timeout

        # MCP path (if enabled)
        if self.mcp_enabled and self.mcp_url:
            try:
                mcp_results = self._query_via_mcp(
                    origin.upper(), destination.upper(), date,
                    cabin=cabin, stops=stops, limit=limit,
                    timeout=effective_timeout,
                )
                if mcp_results:
                    return mcp_results
            except Exception as e:
                logger.warning("SK MCP failed, falling back to REST: %s", e)

        # REST path (with retry + fare_class)
        try:
            data = self._fetch_with_retry(
                origin.upper(), destination.upper(), date,
                effective_timeout, cabin=cabin,
                return_date=return_date,
            )
        except (_TransientError, Exception) as e:
            logger.warning("Skiplagged request failed: %s", e)
            return []

        if not data:
            return []

        return self._parse_response(data, stops=stops, limit=limit, cabin=cabin)

    def _fetch_with_retry(
        self, origin: str, destination: str, date: str,
        total_timeout: int, *, cabin: str = "economy",
        return_date: str | None = None,
    ) -> dict | None:
        """Fetch with smart retry on empty responses and transient errors.

        Retry triggers:
        - HTTP 200 + empty flights dict (server-side soft throttle)
        - Transient network errors (timeout, connection reset, DNS)

        No-retry (fail fast):
        - HTTP 4xx/5xx (permanent error)
        - JSON parse error (permanent)
        """
        import time as _time

        attempts = self.max_retries + 1
        per_attempt = max(3, total_timeout // attempts)
        best_data = None

        for attempt in range(attempts):
            t0 = _time.time()
            try:
                data = self._fetch(origin, destination, date, per_attempt,
                                   cabin=cabin, return_date=return_date)
            except _TransientError as e:
                elapsed = _time.time() - t0
                logger.info(
                    "SK %s→%s: attempt=%d/%d status=transient "
                    "flights=0 time=%.1fs error=%s",
                    origin, destination, attempt + 1, attempts, elapsed, e,
                )
                if attempt < attempts - 1:
                    delay = self.retry_delay * (self.retry_backoff ** attempt)
                    _time.sleep(delay)
                continue

            if data is None:
                # HTTP error or JSON parse error → permanent, no retry
                return best_data

            flights = data.get("flights", {})
            elapsed = _time.time() - t0

            if flights:
                logger.info(
                    "SK %s→%s: attempt=%d/%d status=ok "
                    "flights=%d time=%.1fs",
                    origin, destination, attempt + 1, attempts,
                    len(flights), elapsed,
                )
                if best_data and best_data.get("flights"):
                    best_data["flights"].update(flights)
                    best_data.setdefault("airlines", {}).update(
                        data.get("airlines", {})
                    )
                    return best_data
                return data

            # Empty flights → retry
            logger.info(
                "SK %s→%s: attempt=%d/%d status=empty "
                "flights=0 time=%.1fs",
                origin, destination, attempt + 1, attempts, elapsed,
            )
            if attempt < attempts - 1:
                delay = self.retry_delay * (self.retry_backoff ** attempt)
                _time.sleep(delay)

            if best_data is None:
                best_data = data

        return best_data

    def _fetch(
        self, origin: str, destination: str, date: str,
        timeout: int, *, cabin: str = "economy",
        return_date: str | None = None,
    ) -> dict | None:
        """Fetch data from Skiplagged API."""
        session = cf_requests.Session()
        params = {
            "from": origin,
            "to": destination,
            "depart": date,
            "sort": "cost",
        }
        if return_date:
            params["return"] = return_date
        # fare_class: REST API supports economy/business/first only
        # Map premium → economy (SK has no premium economy tier)
        _SK_CABIN_MAP = {"economy": "economy", "business": "business",
                         "first": "first", "premium": "economy"}
        effective_cabin = _SK_CABIN_MAP.get(cabin, "economy")
        if effective_cabin and effective_cabin != "economy":
            params["fare_class"] = effective_cabin

        try:
            resp = session.get(
                BASE_URL,
                params=params,
                impersonate="chrome",
                timeout=timeout,
            )
        except Exception as e:
            # Network errors (timeout, connection reset, DNS) are transient
            raise _TransientError(str(e))

        if resp.status_code != 200:
            logger.warning("Skiplagged returned HTTP %d", resp.status_code)
            return None

        try:
            return resp.json()
        except Exception as e:
            logger.warning("Skiplagged JSON parse error: %s", e)
            return None

    def _query_via_mcp(
        self, origin: str, destination: str, date: str,
        *, cabin: str = "economy", stops: int | str = 0,
        limit: int | None = None, timeout: int = 15,
    ) -> list[dict]:
        """Query via MCP interface (optional, requires mcp package)."""
        try:
            from sources.skiplagged_mcp import SkiplaggedMCPClient
        except ImportError:
            logger.info("MCP client not available (mcp package not installed)")
            return []

        client = SkiplaggedMCPClient(url=self.mcp_url, timeout=timeout)
        return client.search_flights(
            origin, destination, date,
            cabin=cabin, stops=stops, limit=limit,
        )

    def _parse_response(
        self, data: dict, *, stops: int | str = 0, limit: int | None = None,
        cabin: str = "economy",
    ) -> list[dict]:
        """Parse Skiplagged API response into standard records."""
        airlines = data.get("airlines", {})
        flights = data.get("flights", {})

        if not flights:
            return []

        records = []
        for fid, flight_data in flights.items():
            try:
                record = self._parse_flight(flight_data, airlines, cabin=cabin)
            except Exception as e:
                logger.debug("Skipping Skiplagged entry %s: %s", fid, e)
                continue

            if record is None:
                continue

            # Client-side stops filter
            rec_stops = record.get("stops", 0)
            if stops != "any" and rec_stops > int(stops):
                continue

            records.append(record)

        # Sort by price (cheapest first)
        records.sort(key=lambda r: r.get("price") or float("inf"))

        return records[:limit] if limit is not None else records

    def _parse_flight(self, flight_data: list, airlines: dict,
                      *, cabin: str = "economy") -> dict | None:
        """Parse a single flight entry.

        flight_data = [legs, price_cents, unknown, token]
        legs = [[flight_num, origin, dep_iso, dest, arr_iso], ...]
        """
        if not isinstance(flight_data, list) or len(flight_data) < 2:
            return None

        legs = flight_data[0]
        price_cents = flight_data[1]

        if not isinstance(legs, list) or not legs:
            return None

        first_seg = legs[0]
        last_seg = legs[-1]

        if not isinstance(first_seg, list) or len(first_seg) < 5:
            return None
        if not isinstance(last_seg, list) or len(last_seg) < 5:
            return None

        flight_number = first_seg[0] or ""
        origin_iata = first_seg[1] or ""
        dep_iso = first_seg[2] or ""
        destination_iata = last_seg[3] or ""
        arr_iso = last_seg[4] or ""

        # Strip timezone offset for consistency with GF format
        scheduled_departure = _strip_tz_offset(dep_iso)
        scheduled_arrival = _strip_tz_offset(arr_iso)

        # Price: cents to dollars
        price = price_cents / 100.0 if isinstance(price_cents, (int, float)) else None

        # Airline name from code
        airline_code = _extract_airline_code(flight_number)
        airline_name = airlines.get(airline_code, airline_code)

        # Stops
        num_stops = len(legs) - 1

        # Duration in minutes
        duration_minutes = _calc_duration_minutes(dep_iso, arr_iso)

        return {
            "flight_number": flight_number,
            "airline": airline_name,
            "origin_iata": origin_iata,
            "origin_city": airport_manager.get_display_name(origin_iata),
            "destination_iata": destination_iata,
            "destination_city": airport_manager.get_display_name(destination_iata),
            "scheduled_departure": scheduled_departure,
            "scheduled_arrival": scheduled_arrival,
            "actual_departure": None,
            "actual_arrival": None,
            "status": "",
            "aircraft_type": "",
            "delay_minutes": None,
            "price": price,
            "stops": num_stops,
            "duration_minutes": duration_minutes,
            "cabin_class": cabin,
            "source": "skiplagged",
        }


def _strip_tz_offset(iso_str: str) -> str | None:
    """Strip timezone offset from ISO 8601 string.

    '2026-03-22T08:15:00+08:00' -> '2026-03-22T08:15:00'
    """
    if not iso_str:
        return None
    # Handle '+HH:MM' or '-HH:MM' at end
    if len(iso_str) >= 6 and iso_str[-6] in ("+", "-") and iso_str[-3] == ":":
        return iso_str[:-6]
    # Handle 'Z' suffix
    if iso_str.endswith("Z"):
        return iso_str[:-1]
    return iso_str


def _extract_airline_code(flight_number: str) -> str:
    """Extract airline IATA code from flight number.

    'MU2716' -> 'MU', '3U8801' -> '3U'
    """
    if not flight_number:
        return ""
    # Handle codes like '3U' (digit + letter)
    if len(flight_number) >= 2 and flight_number[0].isdigit() and flight_number[1].isalpha():
        return flight_number[:2]
    # Standard 2-letter code
    code = ""
    for ch in flight_number:
        if ch.isalpha():
            code += ch
        else:
            break
    return code[:2] if len(code) >= 2 else code


def _calc_duration_minutes(dep_iso: str, arr_iso: str) -> int | None:
    """Calculate flight duration in minutes from ISO 8601 timestamps."""
    if not dep_iso or not arr_iso:
        return None
    try:
        dep = datetime.fromisoformat(dep_iso)
        arr = datetime.fromisoformat(arr_iso)
        delta = arr - dep
        minutes = int(delta.total_seconds() / 60)
        return minutes if minutes > 0 else None
    except (ValueError, TypeError):
        return None
