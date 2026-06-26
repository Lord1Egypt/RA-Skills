"""Airport code resolver with Chinese/English/IATA input support.

Loads cache/airports.json and builds reverse lookup indices so that user
input in any form (IATA, Chinese city, English city, alias) resolves to
the correct IATA code.
"""

import json
import logging
import os
import re
import time

import requests

_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
_AIRPORTS_FILE = os.path.join(_PROJECT_DIR, "cache", "airports.json")
_INACTIVE_FILE = os.path.join(_PROJECT_DIR, "cache", "inactive_airports.json")

logger = logging.getLogger("flyclaw.airport")

# Default (primary international) airport for multi-airport cities.
_CITY_DEFAULT = {
    "上海": "PVG",
    "shanghai": "PVG",
    "北京": "PEK",
    "beijing": "PEK",
    "成都": "CTU",
    "chengdu": "CTU",
    "纽约": "JFK",
    "newyork": "JFK",
    "new york": "JFK",
    "伦敦": "LHR",
    "london": "LHR",
    "巴黎": "CDG",
    "paris": "CDG",
}


class AirportManager:
    """Resolve user input (Chinese/English/IATA) to IATA airport code."""

    def __init__(self, data_path: str = _AIRPORTS_FILE,
                 inactive_path: str = _INACTIVE_FILE):
        self._data_path = data_path
        self._airports: dict[str, dict] = {}
        # Lookup tables: lowercased key -> list of IATA codes
        self._iata_index: dict[str, str] = {}         # "pvg" -> "PVG"
        self._city_cn_index: dict[str, list[str]] = {} # "上海" -> ["PVG","SHA"]
        self._city_en_index: dict[str, list[str]] = {} # "shanghai" -> ["PVG","SHA"]
        self._alias_index: dict[str, str] = {}         # "浦东" -> "PVG"
        self._name_cn_index: dict[str, str] = {}       # partial Chinese names
        self._inactive_set: set[str] = set()           # inactive airport IATA codes
        self._load(data_path)
        self._load_inactive(inactive_path)

    def _load(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            self._airports = json.load(f)

        for iata, info in self._airports.items():
            # IATA index (case-insensitive)
            self._iata_index[iata.lower()] = iata

            # City CN index
            city_cn = info.get("city_cn", "")
            if city_cn:
                self._city_cn_index.setdefault(city_cn, []).append(iata)

            # City EN index (lowercased, with and without spaces)
            city_en = info.get("city_en", "")
            if city_en:
                key = city_en.lower()
                self._city_en_index.setdefault(key, []).append(iata)
                # Also index without spaces: "new york" -> "newyork"
                no_space = key.replace(" ", "")
                if no_space != key:
                    self._city_en_index.setdefault(no_space, []).append(iata)

            # Alias index
            for alias in info.get("aliases", []):
                self._alias_index[alias.lower()] = iata

            # Chinese airport name (partial match index)
            name_cn = info.get("name_cn", "")
            if name_cn:
                self._name_cn_index[name_cn] = iata

    def _load_inactive(self, path: str) -> None:
        """Load inactive airport codes from JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            airports = data.get("airports", {})
            self._inactive_set = {code.upper() for code in airports}
            logger.debug("Loaded %d inactive airports", len(self._inactive_set))
        except (OSError, json.JSONDecodeError) as e:
            logger.debug("Inactive airports file not loaded: %s", e)
            self._inactive_set = set()

    def is_active(self, code: str) -> bool:
        """Return True if airport has commercial passenger flights."""
        return code.upper() not in self._inactive_set

    def resolve_all(self, query: str, *, filter_inactive: bool = True) -> list[str]:
        """Resolve user input to all matching IATA codes.

        - IATA code (PVG) → ["PVG"] (exact match, never filtered)
        - Alias (浦东) → ["PVG"] (exact match, never filtered)
        - City name (上海) → ["PVG", "SHA"] (city-level, inactive filtered)
        - City name (Shanghai) → ["PVG", "SHA"]
        - Unknown → []

        When filter_inactive=True, city-level results exclude airports in
        the inactive list (closed, non-commercial, etc.).  If all airports
        would be filtered, returns the original unfiltered list as fallback.
        Direct IATA / alias matches are never filtered.
        """
        q = query.strip()
        if not q:
            return []

        q_lower = q.lower()
        q_nospace = re.sub(r"\s+", "", q_lower)

        # 1. Direct IATA match → single airport (never filter)
        if q_nospace in self._iata_index:
            return [self._iata_index[q_nospace]]

        # 2. Alias match → single airport (never filter)
        if q_lower in self._alias_index:
            return [self._alias_index[q_lower]]
        if q_nospace in self._alias_index:
            return [self._alias_index[q_nospace]]

        # 3. Chinese city name → all airports in that city
        if q in self._city_cn_index:
            return self._filter_inactive(self._city_cn_index[q], filter_inactive)

        # 4. English city name (with spaces) → all airports
        if q_lower in self._city_en_index:
            return self._filter_inactive(self._city_en_index[q_lower], filter_inactive)

        # 5. English city name (without spaces) → all airports
        if q_nospace in self._city_en_index:
            return self._filter_inactive(self._city_en_index[q_nospace], filter_inactive)

        # 6. Partial Chinese name match → single airport (never filter)
        for name, iata in self._name_cn_index.items():
            if q in name:
                return [iata]

        return []

    def _filter_inactive(self, codes: list[str], do_filter: bool) -> list[str]:
        """Filter inactive airports from a city-level result list.

        Returns the original list if filtering is disabled or would remove all.
        """
        if not do_filter or not self._inactive_set:
            return list(codes)
        filtered = [c for c in codes if c not in self._inactive_set]
        if not filtered:
            # Safety fallback: don't return empty
            return list(codes)
        return filtered

    def resolve(self, query: str) -> str | None:
        """Resolve user input to IATA code (backward compatible).

        Returns the primary airport for multi-airport cities via _CITY_DEFAULT.
        Returns None if unresolvable.
        """
        results = self.resolve_all(query)
        if not results:
            return None

        # For multi-airport cities, prefer the default primary airport
        q = query.strip()
        q_lower = q.lower()
        q_nospace = re.sub(r"\s+", "", q_lower)
        for key in (q, q_lower, q_nospace):
            if key in _CITY_DEFAULT:
                default = _CITY_DEFAULT[key]
                if default in results:
                    return default
        return results[0]

    def check_staleness(self, update_days: int) -> bool:
        """Check if airport data file is stale and needs updating.

        Returns True if the data file is older than *update_days* days.
        Returns False if update_days <= 0 (auto-update disabled) or file
        is still fresh.
        """
        if update_days <= 0:
            return False
        try:
            mtime = os.path.getmtime(self._data_path)
        except OSError:
            return True  # file missing → stale
        return (time.time() - mtime) >= update_days * 86400

    @staticmethod
    def _validate_airport_data(data: dict) -> bool:
        """Validate that *data* looks like a valid airports dict.

        Requirements:
        - Must be a dict with at least 10 entries
        - Keys must be 3-char uppercase (IATA format)
        - Values must contain name_cn, name_en, city_cn, city_en keys
          (values may be empty strings for airports without translations)
        """
        if not isinstance(data, dict) or len(data) < 10:
            return False
        required_fields = {"name_cn", "name_en", "city_cn", "city_en"}
        for key, val in data.items():
            if not (isinstance(key, str) and len(key) == 3 and key.isupper()):
                return False
            if not isinstance(val, dict):
                return False
            if not required_fields.issubset(val.keys()):
                return False
        return True

    def update_from_url(self, url: str) -> bool:
        """Download airport data from *url* and merge into existing data.

        - Empty URL → return False
        - Validates downloaded data structure
        - Merges: keeps existing entries, adds new entries, fills missing fields
        - Writes via atomic replace
        - Rebuilds indices on success
        - Any failure → logs warning, returns False, existing data untouched
        """
        if not url:
            return False
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            new_data = resp.json()
        except Exception as e:
            logger.warning("Failed to download airport data from %s: %s", url, e)
            return False

        if not self._validate_airport_data(new_data):
            logger.warning("Downloaded airport data failed validation")
            return False

        # Merge: preserve existing, add new, fill missing fields
        merged = self._airports.copy()
        for iata, info in new_data.items():
            if iata in merged:
                # Fill missing fields in existing entry
                for field, val in info.items():
                    if not merged[iata].get(field) and val:
                        merged[iata][field] = val
            else:
                merged[iata] = info

        # Atomic write via temp file + os.replace
        try:
            tmp_path = self._data_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self._data_path)
        except Exception as e:
            logger.warning("Failed to write airport data: %s", e)
            return False

        # Rebuild indices
        self._airports = {}
        self._iata_index = {}
        self._city_cn_index = {}
        self._city_en_index = {}
        self._alias_index = {}
        self._name_cn_index = {}
        self._load(self._data_path)

        logger.info("Airport data updated: %d entries", len(self._airports))
        return True

    def get_info(self, iata: str) -> dict | None:
        """Return full airport info dict, or None."""
        return self._airports.get(iata.upper())

    def get_display_name(self, iata: str) -> str:
        """Return display name like '上海浦东(PVG)'.

        Falls back to city_en when city_cn is empty.
        """
        info = self.get_info(iata)
        if not info:
            return iata
        city = info.get("city_cn", "") or info.get("city_en", "")
        # Use first alias as short name if available
        aliases = info.get("aliases", [])
        short = ""
        for a in aliases:
            if not a.isascii():
                short = a
                break
        name_part = f"{city}{short}" if short and short != city else city
        if not name_part:
            return iata
        return f"{name_part}({iata})"


# Module-level singleton
airport_manager = AirportManager()
