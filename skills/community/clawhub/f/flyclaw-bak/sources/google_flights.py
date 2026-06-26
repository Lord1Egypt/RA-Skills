"""Google Flights data source with fallback strategy.

Level 1: fli library (Python wrapper for Google Flights)
Level 2: SerpAPI (requires API key in config.yaml)
"""

import logging
from datetime import datetime, date as date_type

import requests

import config as cfg
from airport_manager import airport_manager
from route_cache import route_cache

logger = logging.getLogger("flyclaw.google_flights")

# Lazy imports for optional dependencies
_fli_available = None


def _check_fli():
    global _fli_available
    if _fli_available is None:
        try:
            from fli.search import SearchFlights  # noqa: F401
            _fli_available = True
        except ImportError:
            _fli_available = False
    return _fli_available


def _format_city(iata: str) -> str:
    """Get display name for an IATA code."""
    return airport_manager.get_display_name(iata) if iata else ""


# Mapping from user-facing cabin names to fli SeatType enum values.
# Imported lazily (fli might not be installed), so we store the int values.
_CABIN_MAP = {
    "economy": 1,       # SeatType.ECONOMY
    "premium": 2,       # SeatType.PREMIUM_ECONOMY
    "business": 3,      # SeatType.BUSINESS
    "first": 4,         # SeatType.FIRST
}

_SORT_MAP = {
    "cheapest": 2,      # SortBy.CHEAPEST
    "fastest": 5,       # SortBy.DURATION
    "departure": 3,     # SortBy.DEPARTURE_TIME
    "arrival": 4,       # SortBy.ARRIVAL_TIME
}


class GoogleFlightsSource:
    """Google Flights data source with multi-level fallback."""

    def __init__(self, timeout: int = 15, serpapi_key: str = "",
                 retry: int = 3,
                 retry_delay: float = 0.5, retry_backoff: float = 2.0):
        self.timeout = timeout
        self.serpapi_key = serpapi_key
        self.max_retries = retry
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff

    def query_by_flight(self, flight_number: str) -> list[dict]:
        """Query by flight number using route cache.

        Looks up the flight's route in the cache, then delegates to
        query_by_route.  Returns empty if route is unknown.
        """
        route = route_cache.get(flight_number)
        if not route:
            logger.info(
                "Google Flights: no cached route for %s, skipping",
                flight_number,
            )
            return []

        today = date_type.today().isoformat()
        results = self.query_by_route(
            route["origin"], route["destination"], today
        )

        fn_upper = flight_number.strip().upper()
        matched = [
            r for r in results
            if r.get("flight_number", "").upper() == fn_upper
        ]
        return matched if matched else results

    def query_by_route(
        self, origin: str | list[str], destination: str | list[str], date: str,
        *, return_date: str | None = None, adults: int = 1,
        children: int = 0, infants: int = 0,
        cabin: str = "economy", stops: int | str = 0,
        sort: str | None = None, limit: int | None = None,
    ) -> list[dict]:
        """Search flights by route. Tries fli library first, then SerpAPI.

        origin/destination can be a single IATA code or a list of codes
        for multi-airport city searches.
        """
        kw = dict(return_date=return_date, adults=adults, children=children,
                  infants=infants, cabin=cabin, stops=stops,
                  sort=sort, limit=limit)

        # Level 1: fli library
        if _check_fli():
            results = self._query_via_fli(origin, destination, date, **kw)
            if results:
                return results
            logger.info("fli library returned no results, trying next level")

        # Level 2: SerpAPI
        if self.serpapi_key:
            results = self._query_via_serpapi(origin, destination, date, **kw)
            if results:
                return results
            logger.info("SerpAPI returned no results")

        logger.info("Google Flights: no results from any level")
        return []

    def _query_via_fli(
        self, origin: str | list[str], destination: str | list[str], date: str,
        *, return_date: str | None = None, adults: int = 1,
        children: int = 0, infants: int = 0,
        cabin: str = "economy", stops: int | str = 0,
        sort: str | None = None, limit: int | None = None,
    ) -> list[dict]:
        """Level 1: fli Python library with smart retry on empty results."""
        import time as _time

        attempts = self.max_retries + 1
        for attempt in range(attempts):
            results = self._query_via_fli_single(
                origin, destination, date,
                return_date=return_date, adults=adults,
                children=children, infants=infants,
                cabin=cabin, stops=stops, sort=sort, limit=limit,
            )
            if results:
                return results
            if attempt < attempts - 1:
                delay = self.retry_delay * (self.retry_backoff ** attempt)
                logger.info(
                    "fli empty response attempt %d, retrying in %.1fs...",
                    attempt + 1, delay,
                )
                _time.sleep(delay)
        return []

    def _query_via_fli_single(
        self, origin: str | list[str], destination: str | list[str], date: str,
        *, return_date: str | None = None, adults: int = 1,
        children: int = 0, infants: int = 0,
        cabin: str = "economy", stops: int | str = 0,
        sort: str | None = None, limit: int | None = None,
    ) -> list[dict]:
        """Single fli query attempt (no retry).

        origin/destination can be str or list[str] for multi-airport queries.
        """
        try:
            from fli.models.google_flights.base import Airport as FliAirport
            from fli.models.google_flights.flights import (
                FlightSearchFilters,
                FlightSegment,
                PassengerInfo,
            )
            from fli.search import SearchFlights
        except ImportError:
            return []

        # Normalize to lists
        origins = origin if isinstance(origin, list) else [origin]
        dests = destination if isinstance(destination, list) else [destination]

        # Build multi-airport departure/arrival lists
        dep_airports = []
        for o in origins:
            try:
                dep_airports.append([FliAirport[o.upper()], 0])
            except KeyError:
                logger.warning("Airport code not in fli enum: %s", o)

        arr_airports = []
        for d in dests:
            try:
                arr_airports.append([FliAirport[d.upper()], 0])
            except KeyError:
                logger.warning("Airport code not in fli enum: %s", d)

        if not dep_airports or not arr_airports:
            return []

        try:
            from fli.models.google_flights.base import MaxStops, SortBy
            from fli.models import SeatType, TripType

            outbound_seg = FlightSegment(
                departure_airport=dep_airports,
                arrival_airport=arr_airports,
                travel_date=date,
            )
            segments = [outbound_seg]

            is_round_trip = return_date is not None
            if is_round_trip:
                return_seg = FlightSegment(
                    departure_airport=arr_airports,
                    arrival_airport=dep_airports,
                    travel_date=return_date,
                )
                segments.append(return_seg)

            seat_val = _CABIN_MAP.get(cabin, 1)
            seat_type = SeatType(seat_val)
            _STOPS_MAP = {
                0: MaxStops.NON_STOP,
                1: MaxStops.ONE_STOP_OR_FEWER,
                2: MaxStops.TWO_OR_FEWER_STOPS,
                "any": MaxStops.ANY,
            }
            stops_enum = _STOPS_MAP.get(stops, MaxStops.NON_STOP)
            sort_val = _SORT_MAP.get(sort, 0)
            sort_by = SortBy(sort_val)

            fli_trip_type = TripType.ROUND_TRIP if is_round_trip else TripType.ONE_WAY
            # fli top_n: use limit if set, otherwise 200 as practical max
            fli_top_n = limit if limit is not None else 200
            if is_round_trip:
                fli_top_n = min(fli_top_n, 5)

            filters = FlightSearchFilters(
                passenger_info=PassengerInfo(
                    adults=adults, children=children,
                    infants_in_seat=infants,
                ),
                flight_segments=segments,
                seat_type=seat_type,
                stops=stops_enum,
                sort_by=sort_by,
                trip_type=fli_trip_type,
            )
            sf = SearchFlights()
            raw_results = sf.search(filters, top_n=fli_top_n)
        except Exception as e:
            logger.warning("fli search failed: %s", e)
            return []

        if not raw_results:
            return []

        # Primary airports for display fallback
        primary_origin = origins[0].upper()
        primary_dest = dests[0].upper()

        results = []
        for r in raw_results:
            if limit is not None and len(results) >= limit:
                break
            try:
                if is_round_trip and isinstance(r, tuple) and len(r) == 2:
                    parsed = self._parse_fli_round_trip(
                        r[0], r[1], primary_origin, primary_dest, cabin
                    )
                else:
                    parsed = self._parse_fli_result(r, primary_origin, primary_dest)
                    parsed["trip_type"] = "one_way"
                    parsed["cabin_class"] = cabin
                results.append(parsed)
            except Exception as e:
                logger.debug("Skipping fli result: %s", e)
        return results

    def _parse_fli_result(self, result, origin: str, dest: str) -> dict:
        """Convert fli FlightResult to standard schema.

        origin/dest are fallback values; actual airports are extracted
        from leg data when available.
        """
        legs = result.legs
        if not legs:
            return self._empty_record(origin, dest)

        first_leg = legs[0]
        last_leg = legs[-1]

        flight_number = ""
        airline = ""
        if first_leg.airline:
            airline = first_leg.airline.value or ""
        if first_leg.flight_number:
            # Construct full flight number from airline code + number
            airline_code = first_leg.airline.name if first_leg.airline else ""
            flight_number = f"{airline_code}{first_leg.flight_number}"

        dep_dt = first_leg.departure_datetime
        arr_dt = last_leg.arrival_datetime

        # Extract actual origin/dest from legs when available
        actual_origin = origin
        actual_dest = dest
        if hasattr(first_leg, 'departure_airport') and first_leg.departure_airport:
            dep_ap = first_leg.departure_airport
            if hasattr(dep_ap, 'name'):
                actual_origin = dep_ap.name
        if hasattr(last_leg, 'arrival_airport') and last_leg.arrival_airport:
            arr_ap = last_leg.arrival_airport
            if hasattr(arr_ap, 'name'):
                actual_dest = arr_ap.name

        return {
            "flight_number": flight_number,
            "airline": airline,
            "origin_iata": actual_origin,
            "origin_city": _format_city(actual_origin),
            "destination_iata": actual_dest,
            "destination_city": _format_city(actual_dest),
            "scheduled_departure": dep_dt.isoformat() if dep_dt else None,
            "scheduled_arrival": arr_dt.isoformat() if arr_dt else None,
            "actual_departure": None,
            "actual_arrival": None,
            "status": "",
            "aircraft_type": "",
            "delay_minutes": None,
            "price": result.price,
            "stops": result.stops,
            "duration_minutes": result.duration,
            "source": "google_flights",
        }

    def _parse_fli_round_trip(
        self, outbound, inbound, origin: str, dest: str, cabin: str
    ) -> dict:
        """Convert a fli round-trip pair to standard schema."""
        record = self._parse_fli_result(outbound, origin, dest)
        record["trip_type"] = "round_trip"
        record["cabin_class"] = cabin

        # Return flight info
        ret_legs = inbound.legs
        if ret_legs:
            first_ret = ret_legs[0]
            last_ret = ret_legs[-1]
            ret_fn = ""
            ret_airline = ""
            if first_ret.airline:
                ret_airline = first_ret.airline.value or ""
                airline_code = first_ret.airline.name if first_ret.airline else ""
                if first_ret.flight_number:
                    ret_fn = f"{airline_code}{first_ret.flight_number}"

            ret_dep = first_ret.departure_datetime
            ret_arr = last_ret.arrival_datetime

            record["return_flight_number"] = ret_fn
            record["return_airline"] = ret_airline
            record["return_departure"] = ret_dep.isoformat() if ret_dep else None
            record["return_arrival"] = ret_arr.isoformat() if ret_arr else None
            record["return_stops"] = inbound.stops
            record["return_duration_minutes"] = inbound.duration
        else:
            record["return_flight_number"] = ""
            record["return_airline"] = ""
            record["return_departure"] = None
            record["return_arrival"] = None
            record["return_stops"] = None
            record["return_duration_minutes"] = None

        # Price is the total for the pair
        record["price"] = outbound.price

        return record

    def _query_via_serpapi(
        self, origin: str | list[str], destination: str | list[str], date: str,
        *, return_date: str | None = None, adults: int = 1,
        children: int = 0, infants: int = 0,
        cabin: str = "economy", stops: int | str = 0,
        sort: str | None = None, limit: int | None = None,
    ) -> list[dict]:
        """Level 2: SerpAPI Google Flights endpoint.

        Multi-airport: comma-separated IATA codes for departure_id/arrival_id.
        """
        _SERPAPI_CABIN = {
            "economy": "1", "premium": "2", "business": "3", "first": "4",
        }
        # Normalize to lists then join with comma for SerpAPI
        origins = origin if isinstance(origin, list) else [origin]
        dests = destination if isinstance(destination, list) else [destination]
        dep_id = ",".join(o.upper() for o in origins)
        arr_id = ",".join(d.upper() for d in dests)

        is_round_trip = return_date is not None
        try:
            params = {
                "engine": "google_flights",
                "departure_id": dep_id,
                "arrival_id": arr_id,
                "outbound_date": date,
                "type": "1" if is_round_trip else "2",
                "currency": "USD",
                "hl": "en",
                "api_key": self.serpapi_key,
                "adults": str(adults),
                "travel_class": _SERPAPI_CABIN.get(cabin, "1"),
            }
            if is_round_trip:
                params["return_date"] = return_date
            if children > 0:
                params["children"] = str(children)
            if infants > 0:
                params["infants_in_seat"] = str(infants)
            if stops != "any":
                params["stops"] = str(stops)
            resp = requests.get(
                "https://serpapi.com/search",
                params=params,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.warning("SerpAPI request failed: %s", e)
            return []

        best = data.get("best_flights", [])
        other = data.get("other_flights", [])
        all_flights = best + other
        if limit is not None:
            all_flights = all_flights[:limit]

        trip_type_str = "round_trip" if is_round_trip else "one_way"
        primary_origin = origins[0].upper()
        primary_dest = dests[0].upper()
        results = []
        for flight in all_flights:
            try:
                parsed = self._parse_serpapi_result(
                    flight, primary_origin, primary_dest
                )
                parsed["trip_type"] = trip_type_str
                parsed["cabin_class"] = cabin
                results.append(parsed)
            except Exception as e:
                logger.debug("Skipping SerpAPI result: %s", e)
        return results

    def _parse_serpapi_result(
        self, flight: dict, origin: str, dest: str
    ) -> dict:
        """Convert SerpAPI flight result to standard schema."""
        legs = flight.get("flights", [])
        first = legs[0] if legs else {}
        last = legs[-1] if legs else {}

        dep_airport = first.get("departure_airport", {})
        arr_airport = last.get("arrival_airport", {})

        return {
            "flight_number": first.get("flight_number", ""),
            "airline": first.get("airline", ""),
            "origin_iata": dep_airport.get("id", origin),
            "origin_city": _format_city(dep_airport.get("id", origin)),
            "destination_iata": arr_airport.get("id", dest),
            "destination_city": _format_city(arr_airport.get("id", dest)),
            "scheduled_departure": dep_airport.get("time"),
            "scheduled_arrival": arr_airport.get("time"),
            "actual_departure": None,
            "actual_arrival": None,
            "status": "",
            "aircraft_type": first.get("airplane", ""),
            "delay_minutes": None,
            "price": flight.get("price"),
            "stops": len(flight.get("layovers", [])),
            "duration_minutes": flight.get("total_duration"),
            "source": "google_flights",
        }

    @staticmethod
    def _empty_record(origin: str, dest: str) -> dict:
        return {
            "flight_number": "",
            "airline": "",
            "origin_iata": origin,
            "origin_city": _format_city(origin),
            "destination_iata": dest,
            "destination_city": _format_city(dest),
            "scheduled_departure": None,
            "scheduled_arrival": None,
            "actual_departure": None,
            "actual_arrival": None,
            "status": "",
            "aircraft_type": "",
            "delay_minutes": None,
            "price": None,
            "source": "google_flights",
        }
