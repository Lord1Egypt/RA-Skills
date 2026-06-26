"""Airplanes.live ADS-B data source with ADSB.lol transparent fallback.

Queries the Airplanes.live free REST API for real-time aircraft position
data.  If Airplanes.live fails, automatically falls back to ADSB.lol
(identical API structure).

Best for: live tracking (altitude, speed, heading, position).
Does NOT provide: flight schedules, prices, or departure/arrival times.

API docs: https://airplanes.live
Rate limit: 1 request/second, no registration required.
"""

import logging

import requests

import config as cfg

logger = logging.getLogger("flyclaw.airplaneslive")


class AirplanesLiveSource:
    """Airplanes.live ADS-B data source with ADSB.lol fallback."""

    def __init__(self, timeout: int = 8):
        self.timeout = timeout

    def query_by_flight(self, flight_number: str) -> list[dict]:
        """Query by IATA flight number (e.g. 'CA981').

        Converts to ICAO callsign internally.  Tries Airplanes.live first,
        falls back to ADSB.lol on failure.  Returns empty list if the
        airline code is not in the mapping or the flight is not currently
        airborne.
        """
        callsign = cfg.iata_flight_to_icao_callsign(flight_number)
        if not callsign:
            logger.debug(
                "No ICAO callsign mapping for %s, skipping", flight_number
            )
            return []

        # Try primary: Airplanes.live
        results = self._try_api(
            cfg.AIRPLANESLIVE_API_BASE, callsign, flight_number
        )
        if results:
            return results

        # Fallback: ADSB.lol
        logger.info("Airplanes.live returned no results, trying ADSB.lol")
        results = self._try_api(
            cfg.ADSB_LOL_API_BASE, callsign, flight_number
        )
        return results

    def _try_api(
        self, base_url: str, callsign: str, flight_number: str
    ) -> list[dict]:
        """Try querying a single ADS-B API endpoint.

        Returns list of parsed records, or empty list on failure.
        """
        url = f"{base_url}/callsign/{callsign}"
        try:
            logger.debug("ADS-B request: %s", url)
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.warning("ADS-B request failed (%s): %s", base_url, e)
            return []
        except ValueError as e:
            logger.warning("ADS-B JSON parse error (%s): %s", base_url, e)
            return []

        aircraft_list = data.get("ac")
        if not aircraft_list:
            logger.info("ADS-B (%s): no aircraft found for %s", base_url, callsign)
            return []

        results = []
        for ac in aircraft_list:
            try:
                results.append(self._parse_aircraft(ac, flight_number))
            except Exception as e:
                logger.debug("Skipping malformed aircraft record: %s", e)
        return results

    def query_by_route(
        self, origin: str, destination: str, date: str | None = None
    ) -> list[dict]:
        """ADS-B data does not support route-based queries."""
        logger.debug("Airplanes.live does not support route queries, skipping")
        return []

    @staticmethod
    def _parse_aircraft(ac: dict, flight_number: str) -> dict:
        """Convert raw ADS-B aircraft record to standard schema."""
        return {
            "flight_number": flight_number.upper(),
            "airline": "",
            "origin_iata": "",
            "origin_city": "",
            "destination_iata": "",
            "destination_city": "",
            "scheduled_departure": None,
            "scheduled_arrival": None,
            "actual_departure": None,
            "actual_arrival": None,
            "status": "In Air",
            "aircraft_type": ac.get("t", ""),
            "delay_minutes": None,
            "price": None,
            "source": "airplanes_live",
            # ADS-B extended fields
            "altitude_ft": ac.get("alt_baro"),
            "ground_speed_kts": ac.get("gs"),
            "heading": ac.get("track"),
            "latitude": ac.get("lat"),
            "longitude": ac.get("lon"),
            "squawk": ac.get("squawk", ""),
            "hex_code": ac.get("hex", ""),
        }
