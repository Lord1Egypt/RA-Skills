from __future__ import annotations

import csv
import difflib
import io
import json
import os
import re
import unicodedata
import urllib.parse
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:
    from pypinyin import lazy_pinyin
except ImportError:  # a clear runtime error is raised only for Chinese input
    lazy_pinyin = None

try:
    from rapidfuzz import fuzz, process
except ImportError:
    fuzz = None
    process = None

try:
    from .common import cache_dir, fetch_bytes, read_json_cache, write_json_atomic
except ImportError:
    from common import cache_dir, fetch_bytes, read_json_cache, write_json_atomic


UNLOCODE_URL = os.getenv(
    "UNLOCODE_CSV_URL",
    "https://raw.githubusercontent.com/datasets/un-locode/main/data/code-list.csv",
)
WPI_QUERY_URL = os.getenv(
    "WPI_QUERY_URL",
    "https://services9.arcgis.com/j1CY4yzWfwptbTWN/arcgis/rest/services/"
    "WorldPortIndex_WFL1/FeatureServer/0/query",
)
PORT_CATALOG_TTL_SECONDS = 30 * 24 * 60 * 60

COUNTRY_HINTS = {
    "china": "CN",
    "pr china": "CN",
    "中国": "CN",
    "vietnam": "VN",
    "viet nam": "VN",
    "越南": "VN",
    "korea": "KR",
    "south korea": "KR",
    "韩国": "KR",
    "japan": "JP",
    "日本": "JP",
    "singapore": "SG",
    "新加坡": "SG",
    "indonesia": "ID",
    "印尼": "ID",
    "malaysia": "MY",
    "马来西亚": "MY",
    "philippines": "PH",
    "菲律宾": "PH",
    "cambodia": "KH",
    "柬埔寨": "KH",
    "thailand": "TH",
    "泰国": "TH",
    "hong kong": "HK",
    "香港": "HK",
    "macao": "MO",
    "macau": "MO",
    "澳门": "MO",
    "taiwan": "TW",
    "台湾": "TW",
}

NOISE_WORDS = {
    "port",
    "pt",
    "harbour",
    "harbor",
    "terminal",
    "anchorage",
    "gangkou",
    "matou",
    "china",
    "prc",
}

@dataclass(frozen=True)
class Port:
    locode: str
    name: str
    country: str
    latitude: float
    longitude: float

    def to_dict(self) -> dict:
        return asdict(self)


MANUAL_PORTS = {
    "TWKHH": Port("TWKHH", "Kaohsiung", "TW", 22.6163, 120.2850),
    "TWKEL": Port("TWKEL", "Keelung", "TW", 25.1283, 121.7419),
    "TWTXG": Port("TWTXG", "Taichung", "TW", 24.2534, 120.5017),
}

MANUAL_ALIASES = {
    "香港": "HKHKG",
    "香港港": "HKHKG",
    "澳门": "MOMFM",
    "澳门港": "MOMFM",
    "高雄": "TWKHH",
    "高雄港": "TWKHH",
    "基隆": "TWKEL",
    "基隆港": "TWKEL",
    "台中": "TWTXG",
    "台中港": "TWTXG",
}


def _coordinate(part: str, degree_digits: int) -> float:
    degrees = int(part[:degree_digits])
    minutes = int(part[degree_digits : degree_digits + 2])
    direction = part[-1]
    value = degrees + minutes / 60
    return -value if direction in {"S", "W"} else value


def parse_coordinates(raw: str) -> tuple[float, float] | None:
    match = re.fullmatch(r"(\d{4}[NS])\s+(\d{5}[EW])", (raw or "").strip())
    if not match:
        return None
    return _coordinate(match.group(1), 2), _coordinate(match.group(2), 3)


def _catalog_path() -> Path:
    return cache_dir() / "unlocode_ports.json"


def build_catalog(force_refresh: bool = False) -> list[Port]:
    path = _catalog_path()
    if not force_refresh:
        cached = read_json_cache(path, PORT_CATALOG_TTL_SECONDS)
        if cached:
            return [Port(**item) for item in cached]

    raw = fetch_bytes(UNLOCODE_URL, timeout=60).decode("utf-8-sig", "replace")
    ports: list[Port] = []
    missing_coordinates: list[tuple[str, str, str]] = []
    for row in csv.DictReader(io.StringIO(raw)):
        function = row.get("Function", "")
        coordinates = parse_coordinates(row.get("Coordinates", ""))
        if not function.startswith("1"):
            continue
        country = (row.get("Country") or "").upper()
        location = (row.get("Location") or "").upper()
        name = row.get("NameWoDiacritics") or row.get("Name") or ""
        if not country or not location or not name:
            continue
        if not coordinates:
            missing_coordinates.append((country + location, name, country))
            continue
        ports.append(
            Port(
                locode=country + location,
                name=name,
                country=country,
                latitude=coordinates[0],
                longitude=coordinates[1],
            )
        )

    # Supplement UN/LOCODE with World Port Index coordinates. This covers
    # valid maritime ports whose UN/LOCODE coordinate is blank.
    offset = 0
    while True:
        query = urllib.parse.urlencode(
            {
                "where": "1=1",
                "outFields": (
                    "OBJECTID,INDEX_NO,PORT_NAME,COUNTRY,LATITUDE,LONGITUDE"
                ),
                "returnGeometry": "false",
                "orderByFields": "OBJECTID",
                "resultOffset": offset,
                "resultRecordCount": 2000,
                "f": "json",
            }
        )
        page = json.loads(
            fetch_bytes(f"{WPI_QUERY_URL}?{query}", timeout=60).decode(
                "utf-8",
                "replace",
            )
        )
        features = page.get("features", [])
        for feature in features:
            attributes = feature.get("attributes", {})
            name = str(attributes.get("PORT_NAME") or "").strip()
            country = str(attributes.get("COUNTRY") or "").strip().upper()
            latitude = attributes.get("LATITUDE")
            longitude = attributes.get("LONGITUDE")
            object_id = attributes.get("OBJECTID")
            if (
                not name
                or len(country) != 2
                or latitude is None
                or longitude is None
            ):
                continue
            ports.append(
                Port(
                    locode=f"WPI{object_id}",
                    name=name,
                    country=country,
                    latitude=float(latitude),
                    longitude=float(longitude),
                )
            )
        if not features or len(features) < 2000:
            break
        offset += len(features)

    # UN/LOCODE intentionally has blank coordinates for some valid ports.
    # Reuse coordinates only when a same-country, coordinated port name is an
    # unambiguous exact/containment alias (for example CNZOS Zhoushan and the
    # coordinated Majistan/Zhoushan entry).
    def simple_name(value: str) -> str:
        folded = unicodedata.normalize("NFKD", value).casefold()
        folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
        return "".join(re.findall(r"[a-z0-9]+", folded))

    by_country: dict[str, list[tuple[str, Port]]] = {}
    for port in ports:
        by_country.setdefault(port.country, []).append((simple_name(port.name), port))
    for locode, name, country in missing_coordinates:
        needle = simple_name(name)
        if not needle:
            continue
        candidates = [
            port
            for normalized, port in by_country.get(country, [])
            if needle == normalized or needle in normalized or normalized in needle
        ]
        unique_coordinates = {
            (port.latitude, port.longitude) for port in candidates
        }
        if len(unique_coordinates) == 1 and candidates:
            source = candidates[0]
            ports.append(
                Port(
                    locode=locode,
                    name=name,
                    country=country,
                    latitude=source.latitude,
                    longitude=source.longitude,
                )
            )
    known = {port.locode for port in ports}
    ports.extend(
        port for locode, port in MANUAL_PORTS.items() if locode not in known
    )
    write_json_atomic(path, [port.to_dict() for port in ports])
    return ports


def _country_hint(value: str) -> str | None:
    folded = unicodedata.normalize("NFKC", value).casefold()
    for label, code in COUNTRY_HINTS.items():
        if label.casefold() in folded:
            return code
    return None


def _romanize(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    normalized = re.sub(r"^(?:中国|国内)\s*", "", normalized)
    folded = normalized.casefold().strip()
    for label in sorted(COUNTRY_HINTS, key=len, reverse=True):
        suffix = label.casefold()
        if folded != suffix and (
            folded.endswith(", " + suffix)
            or folded.endswith("," + suffix)
            or folded.endswith(" " + suffix)
        ):
            normalized = normalized[: len(normalized) - len(label)].rstrip(" ,")
            folded = normalized.casefold().strip()
            break
    normalized = re.sub(r"(?:港口|港|码头)$", " ", normalized)
    if re.search(r"[\u3400-\u9fff]", normalized):
        if lazy_pinyin is None:
            raise RuntimeError(
                "中文港口名称需要 pypinyin，请先安装 requirements.txt"
            )
        normalized = " ".join(lazy_pinyin(normalized))
    normalized = unicodedata.normalize("NFKD", normalized)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    normalized = normalized.casefold()
    normalized = re.sub(r"港口|港|码头", " ", normalized)
    words = re.findall(r"[a-z0-9]+", normalized)
    words = [word for word in words if word not in NOISE_WORDS]
    return "".join(words)


def _is_locode(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z]{2}[A-Za-z0-9]{3}", value.strip()))


class PortResolver:
    def __init__(self, ports: Iterable[Port] | None = None):
        self.ports = list(ports) if ports is not None else build_catalog()
        known = {port.locode for port in self.ports}
        self.ports.extend(
            port
            for locode, port in MANUAL_PORTS.items()
            if locode not in known
        )
        self.by_locode = {port.locode: port for port in self.ports}
        self.by_name: dict[str, list[Port]] = {}
        self.normalized_names: dict[str, str] = {}
        self._query_cache: dict[str, Port] = {}
        self._field_cache: dict[str, list[Port]] = {}
        for port in self.ports:
            normalized = _romanize(port.name)
            if normalized:
                self.by_name.setdefault(normalized, []).append(port)
                self.normalized_names[port.locode] = normalized
        self.choice_names = list(self.by_name)
        self.choice_names_by_country: dict[str, list[str]] = {}
        self.choice_names_by_initial: dict[str, list[str]] = {}
        self.choice_names_by_country_initial: dict[tuple[str, str], list[str]] = {}
        for normalized, ports_for_name in self.by_name.items():
            initial = normalized[:1]
            self.choice_names_by_initial.setdefault(initial, []).append(normalized)
            for country in {port.country for port in ports_for_name}:
                self.choice_names_by_country.setdefault(country, []).append(normalized)
                self.choice_names_by_country_initial.setdefault(
                    (country, initial),
                    [],
                ).append(normalized)

    def resolve(
        self,
        query: str,
        allow_fuzzy: bool = True,
        fuzzy_cutoff: float = 0.78,
    ) -> Port:
        value = (query or "").strip()
        if not value:
            raise ValueError("港口不能为空")
        cached = self._query_cache.get(value.casefold())
        if cached:
            return cached
        alias_locode = MANUAL_ALIASES.get(value)
        if alias_locode:
            port = self.by_locode.get(alias_locode) or MANUAL_PORTS.get(alias_locode)
            if port:
                self._query_cache[value.casefold()] = port
                return port
        if _is_locode(value):
            port = self.by_locode.get(value.upper())
            if not port:
                raise ValueError(f"未找到 UN/LOCODE: {value.upper()}")
            self._query_cache[value.casefold()] = port
            return port

        country_hint = _country_hint(value)
        normalized = _romanize(value)
        if not normalized:
            raise ValueError(f"无法识别港口: {query}")

        exact = self.by_name.get(normalized, [])
        if country_hint:
            exact = [port for port in exact if port.country == country_hint]
        if len(exact) == 1:
            self._query_cache[value.casefold()] = exact[0]
            return exact[0]
        dedicated_ports = [
            port
            for port in exact
            if re.search(r"(?:\bport\b|\bpt\b)", port.name, re.I)
        ]
        if dedicated_ports:
            dedicated_ports.sort(
                key=lambda port: (
                    port.locode.startswith("WPI"),
                    port.locode,
                )
            )
            self._query_cache[value.casefold()] = dedicated_ports[0]
            return dedicated_ports[0]
        if exact and len({(p.country, p.latitude, p.longitude) for p in exact}) == 1:
            self._query_cache[value.casefold()] = exact[0]
            return exact[0]
        if not allow_fuzzy:
            raise ValueError(f"无法精确识别港口: {query}")

        candidates: list[tuple[float, Port]] = []
        if process is not None and fuzz is not None:
            if fuzzy_cutoff >= 0.9:
                initial = normalized[:1]
                choices = (
                    self.choice_names_by_country_initial.get(
                        (country_hint, initial),
                        [],
                    )
                    if country_hint
                    else self.choice_names_by_initial.get(initial, [])
                )
                min_length = max(2, int(len(normalized) * 0.45))
                max_length = max(5, int(len(normalized) * 1.8))
                choices = [
                    name
                    for name in choices
                    if min_length <= len(name) <= max_length
                ]
            else:
                choices = (
                    self.choice_names_by_country.get(country_hint, [])
                    if country_hint
                    else self.choice_names
                )
            fuzzy_matches = process.extract(
                normalized,
                choices,
                scorer=fuzz.WRatio,
                score_cutoff=fuzzy_cutoff * 100,
                limit=4,
            )
            for name, score, _ in fuzzy_matches:
                for port in self.by_name.get(name, []):
                    if not country_hint or port.country == country_hint:
                        candidates.append((score / 100, port))
        else:
            for port in self.ports:
                if country_hint and port.country != country_hint:
                    continue
                name = self.normalized_names.get(port.locode, "")
                if not name:
                    continue
                ratio = difflib.SequenceMatcher(None, normalized, name).ratio()
                if normalized in name or name in normalized:
                    ratio = max(
                        ratio,
                        min(len(normalized), len(name))
                        / max(len(normalized), len(name))
                        + 0.12,
                    )
                if ratio >= fuzzy_cutoff:
                    candidates.append((ratio, port))

        candidates.sort(key=lambda item: (-item[0], item[1].locode))
        if not candidates:
            raise ValueError(f"无法识别港口: {query}")
        best_score, best_port = candidates[0]
        if len(candidates) > 1:
            second_score, second_port = candidates[1]
            if best_score - second_score < 0.025 and best_port.country != second_port.country:
                raise ValueError(
                    f"港口名称有歧义: {query}，请提供国家或 UN/LOCODE"
                )
        self._query_cache[value.casefold()] = best_port
        return best_port

    def resolve_field(self, value: str) -> list[Port]:
        """Resolve one or more alternative ports in a cargo field."""
        raw = (value or "").strip()
        if not raw:
            return []
        field_key = raw.casefold()
        if field_key in self._field_cache:
            return self._field_cache[field_key]
        cleaned = re.sub(
            r"^\s*(?:load(?:ing)?\s+port|discharge\s+port)\s*:\s*",
            "",
            raw,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"^\s*\d+\s*(?:sb|sp)(?:\s+\d+\s*(?:sb|sp))*\s*", "", cleaned, flags=re.I)
        attempts = [cleaned]
        parts = re.split(
            r"\s+(?:or|and/or|chopt)\s+|[/、;；]|\s+或\s+",
            cleaned,
            flags=re.IGNORECASE,
        )
        attempts.extend(part.strip(" ,.") for part in parts if part.strip(" ,."))
        for part in list(parts):
            comma_head = part.split(",", 1)[0].strip()
            if comma_head:
                attempts.append(comma_head)
        resolved: list[Port] = []
        seen: set[str] = set()
        for attempt in attempts:
            try:
                port = self.resolve(attempt, allow_fuzzy=False)
            except (ValueError, RuntimeError):
                continue
            if port.locode not in seen:
                seen.add(port.locode)
                resolved.append(port)
        if not resolved and process is not None:
            for attempt in attempts:
                try:
                    port = self.resolve(
                        attempt,
                        allow_fuzzy=True,
                        fuzzy_cutoff=0.92,
                    )
                except (ValueError, RuntimeError):
                    continue
                if port.locode not in seen:
                    seen.add(port.locode)
                    resolved.append(port)
        self._field_cache[field_key] = resolved
        return resolved


def describe_resolution(query: str) -> str:
    resolver = PortResolver()
    return json.dumps(resolver.resolve(query).to_dict(), ensure_ascii=False)
