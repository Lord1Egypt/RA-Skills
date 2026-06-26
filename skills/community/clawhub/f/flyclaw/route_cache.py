"""Flight route cache for indirect flight-number lookups.

Maintains a mapping of flight_number → {origin, destination, last_seen}
so that sources which only support route queries (e.g. Google Flights)
can participate in flight-number lookups by first resolving the route
from the cache.

Cache file: cache/flight_routes.json
"""

import json
import logging
import os
import time

import config as cfg

logger = logging.getLogger("flyclaw.route_cache")

_DEFAULT_TTL = 30 * 86400  # 30 days in seconds


class RouteCache:
    """In-memory + on-disk route cache."""

    def __init__(
        self,
        cache_path: str | None = None,
        ttl: int = _DEFAULT_TTL,
    ):
        self.cache_path = cache_path or os.path.join(
            cfg.PROJECT_DIR, cfg.DEFAULTS["cache"]["dir"], "flight_routes.json"
        )
        self.ttl = ttl
        self._data: dict[str, dict] = {}
        self._dirty = False
        self._load()

    def _load(self):
        """Load cache from disk."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Route cache load failed: %s", e)
                self._data = {}

    def get(self, flight_number: str) -> dict | None:
        """Look up route for a flight number.

        Returns {"origin": "PEK", "destination": "JFK"} or None if
        missing or expired.
        """
        fn = flight_number.strip().upper()
        entry = self._data.get(fn)
        if not entry:
            return None
        if time.time() - entry.get("last_seen", 0) > self.ttl:
            return None
        return {"origin": entry["origin"], "destination": entry["destination"]}

    def update(self, flight_number: str, origin: str, destination: str):
        """Update a single route entry."""
        fn = flight_number.strip().upper()
        if not fn or not origin or not destination:
            return
        self._data[fn] = {
            "origin": origin.upper(),
            "destination": destination.upper(),
            "last_seen": int(time.time()),
        }
        self._dirty = True

    def update_from_records(self, records: list[dict]):
        """Batch-update cache from query result records."""
        for rec in records:
            fn = rec.get("flight_number", "")
            origin = rec.get("origin_iata", "")
            dest = rec.get("destination_iata", "")
            if fn and origin and dest:
                self.update(fn, origin, dest)

    def save(self):
        """Write cache to disk (atomic via temp file)."""
        if not self._dirty:
            return
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        tmp = self.cache_path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.cache_path)
            self._dirty = False
            logger.debug("Route cache saved (%d entries)", len(self._data))
        except OSError as e:
            logger.warning("Route cache save failed: %s", e)


# Module-level singleton
route_cache = RouteCache()
