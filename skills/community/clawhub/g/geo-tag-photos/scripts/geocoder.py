"""Nominatim-backed geocoder with on-disk cache and OSM-compliant rate limiting."""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Callable

import requests


USER_AGENT = "geo-tag-photos/1.0.0 (https://github.com/ucsdzehualiu/my_openclaw_skill)"
MIN_REQUEST_INTERVAL = 1.1
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
MAX_RETRIES = 3
RETRY_BACKOFF = (2.0, 4.0)  # seconds; sleeps before retry attempts 2 and 3


class GeocodeError(Exception):
    """Raised when Nominatim consistently fails after retries."""


_WS = re.compile(r"\s+")


def _canonical_key(landmark: str, city: str, country: str) -> str:
    parts = [_WS.sub(" ", x.strip().lower()) for x in (landmark, city, country)]
    return "|".join(parts)


class Geocoder:
    def __init__(
        self,
        cache_path: Path,
        *,
        session: requests.Session | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
        monotonic_fn: Callable[[], float] = time.monotonic,
    ):
        self.cache_path = Path(cache_path)
        self.session = session
        self._sleep = sleep_fn
        self._monotonic = monotonic_fn
        self._last_request_t: float | None = None
        self.cache: dict[str, list[float] | None] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        if self.cache_path.exists():
            try:
                self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except Exception:
                self.cache = {}

    def save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.cache_path.with_suffix(self.cache_path.suffix + ".tmp")
        tmp.write_text(json.dumps(self.cache, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.cache_path)

    def _wait_for_slot(self) -> None:
        if self._last_request_t is None:
            self._last_request_t = self._monotonic()
            return
        elapsed = self._monotonic() - self._last_request_t
        remaining = MIN_REQUEST_INTERVAL - elapsed
        if remaining > 0:
            self._sleep(remaining)
        self._last_request_t = self._monotonic()

    def _query_nominatim(self, q: str) -> list[float] | None:
        last_err: Exception | None = None
        for attempt in range(MAX_RETRIES):
            self._wait_for_slot()
            try:
                getter = (self.session.get if self.session else requests.get)
                resp = getter(
                    NOMINATIM_URL,
                    params={"q": q, "format": "json", "limit": 1},
                    headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
                    timeout=20,
                )
            except requests.RequestException as e:
                last_err = e
            else:
                status = getattr(resp, "status_code", 0)
                if 200 <= status < 300:
                    data = resp.json()
                    if not data:
                        return None
                    item = data[0]
                    return [float(item["lat"]), float(item["lon"])]
                if 400 <= status < 500 and status != 429:
                    raise GeocodeError(f"client error {status} from Nominatim")
                last_err = GeocodeError(f"server status {status}")
            # backoff before retry (only on attempts that aren't the last)
            if attempt < MAX_RETRIES - 1:
                self._sleep(RETRY_BACKOFF[attempt] if attempt < len(RETRY_BACKOFF) else RETRY_BACKOFF[-1])
        raise GeocodeError(f"failed after {MAX_RETRIES} attempts: {last_err}")

    def geocode(self, landmark: str, city: str, country: str) -> tuple[float, float] | None:
        key = _canonical_key(landmark, city, country)
        if key in self.cache:
            cached = self.cache[key]
            return tuple(cached) if cached else None
        q = f"{landmark.strip()}, {city.strip()}, {country.strip()}"
        result = self._query_nominatim(q)
        self.cache[key] = result
        return tuple(result) if result else None
