from __future__ import annotations

import csv
import io
import os
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from pypinyin import lazy_pinyin
from rapidfuzz import fuzz, process

try:
    from .common import cache_dir, fetch_bytes, read_json_cache, write_json_atomic
except ImportError:
    from common import cache_dir, fetch_bytes, read_json_cache, write_json_atomic


UNLOCODE_URL = os.getenv(
    "UNLOCODE_CSV_URL",
    "https://raw.githubusercontent.com/datasets/un-locode/main/data/code-list.csv",
)
PORT_CATALOG_TTL_SECONDS = 30 * 24 * 60 * 60
NOISE_WORDS = {
    "port", "pt", "harbour", "harbor", "terminal", "anchorage",
    "gangkou", "matou", "china", "prc",
}
COUNTRY_HINTS = {
    "中国": "CN", "china": "CN", "香港": "HK", "hong kong": "HK",
    "澳门": "MO", "macao": "MO", "macau": "MO", "台湾": "TW",
    "taiwan": "TW", "越南": "VN", "vietnam": "VN", "韩国": "KR",
    "korea": "KR", "日本": "JP", "japan": "JP", "新加坡": "SG",
    "singapore": "SG", "马来西亚": "MY", "malaysia": "MY",
    "菲律宾": "PH", "philippines": "PH", "印尼": "ID",
    "indonesia": "ID", "泰国": "TH", "thailand": "TH",
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
    "CNSWE": Port("CNSWE", "Shanwei", "CN", 22.7833, 115.3500),
    "CNNTG": Port("CNNTG", "Nantong", "CN", 32.0167, 120.8500),
    "CNZOS": Port("CNZOS", "Zhoushan", "CN", 30.0000, 122.1000),
    "CNSHG": Port("CNSHG", "Shanghai", "CN", 31.2333, 121.4833),
    "CNDLC": Port("CNDLC", "Dalian", "CN", 38.9167, 121.6000),
    "CNTAO": Port("CNTAO", "Qingdao", "CN", 36.0500, 120.3167),
    "CNNBG": Port("CNNBG", "Ningbo", "CN", 29.9167, 121.6667),
    "CNGZG": Port("CNGZG", "Guangzhou", "CN", 23.1333, 113.2333),
    "CNSTG": Port("CNSTG", "Shantou", "CN", 23.4167, 116.7667),
    "TWKHH": Port("TWKHH", "Kaohsiung", "TW", 22.6163, 120.2850),
    "TWKEL": Port("TWKEL", "Keelung", "TW", 25.1283, 121.7419),
    "TWTXG": Port("TWTXG", "Taichung", "TW", 24.2534, 120.5017),
}
MANUAL_ALIASES = {
    "汕尾": "CNSWE", "汕尾港": "CNSWE", "南通": "CNNTG",
    "南通港": "CNNTG", "舟山": "CNZOS", "舟山港": "CNZOS",
    "上海": "CNSHG", "上海港": "CNSHG", "大连": "CNDLC",
    "大连港": "CNDLC", "青岛": "CNTAO", "青岛港": "CNTAO",
    "宁波": "CNNBG", "宁波港": "CNNBG", "广州": "CNGZG",
    "广州港": "CNGZG", "汕头": "CNSTG", "汕头港": "CNSTG",
    "香港": "HKHKG", "香港港": "HKHKG", "澳门": "MOMFM",
    "澳门港": "MOMFM", "高雄": "TWKHH", "高雄港": "TWKHH",
    "基隆": "TWKEL", "基隆港": "TWKEL", "台中": "TWTXG",
    "台中港": "TWTXG",
}


def _coordinate(part: str, degree_digits: int) -> float:
    degrees = int(part[:degree_digits])
    minutes = int(part[degree_digits:degree_digits + 2])
    value = degrees + minutes / 60
    return -value if part[-1] in {"S", "W"} else value


def parse_coordinates(raw: str) -> tuple[float, float] | None:
    match = re.fullmatch(r"(\d{4}[NS])\s+(\d{5}[EW])", (raw or "").strip())
    if not match:
        return None
    return _coordinate(match.group(1), 2), _coordinate(match.group(2), 3)


def _romanize(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value or "")
    normalized = re.sub(r"^(?:中国|国内)\s*", "", normalized)
    normalized = re.sub(r"(?:港口|港|码头)$", "", normalized)
    if re.search(r"[\u3400-\u9fff]", normalized):
        normalized = " ".join(lazy_pinyin(normalized))
    normalized = unicodedata.normalize("NFKD", normalized)
    normalized = "".join(
        char for char in normalized if not unicodedata.combining(char)
    ).casefold()
    words = [
        word for word in re.findall(r"[a-z0-9]+", normalized)
        if word not in NOISE_WORDS
    ]
    return "".join(words)


def _country_hint(value: str) -> str | None:
    folded = unicodedata.normalize("NFKC", value).casefold()
    for label, code in COUNTRY_HINTS.items():
        if label.casefold() in folded:
            return code
    return None


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
    for row in csv.DictReader(io.StringIO(raw)):
        coordinates = parse_coordinates(row.get("Coordinates", ""))
        if not (row.get("Function") or "").startswith("1") or not coordinates:
            continue
        country = (row.get("Country") or "").upper()
        location = (row.get("Location") or "").upper()
        name = row.get("NameWoDiacritics") or row.get("Name") or ""
        if country and location and name:
            ports.append(
                Port(
                    country + location,
                    name,
                    country,
                    coordinates[0],
                    coordinates[1],
                )
            )
    known = {port.locode for port in ports}
    ports.extend(
        port for locode, port in MANUAL_PORTS.items() if locode not in known
    )
    write_json_atomic(path, [port.to_dict() for port in ports])
    return ports


class PortResolver:
    def __init__(self, ports: Iterable[Port] | None = None):
        self.ports = list(ports) if ports is not None else build_catalog()
        known = {port.locode for port in self.ports}
        self.ports.extend(
            port for locode, port in MANUAL_PORTS.items() if locode not in known
        )
        self.by_locode = {port.locode: port for port in self.ports}
        self.by_name: dict[str, list[Port]] = {}
        self.query_cache: dict[str, Port] = {}
        self.field_cache: dict[str, list[Port]] = {}
        for port in self.ports:
            name = _romanize(port.name)
            if name:
                self.by_name.setdefault(name, []).append(port)
        self.choice_names = list(self.by_name)

    def resolve(self, query: str, allow_fuzzy: bool = True) -> Port:
        value = (query or "").strip()
        if not value:
            raise ValueError("港口不能为空")
        if value.casefold() in self.query_cache:
            return self.query_cache[value.casefold()]
        alias = MANUAL_ALIASES.get(value)
        if alias and alias in self.by_locode:
            return self.by_locode[alias]
        if re.fullmatch(r"[A-Za-z]{2}[A-Za-z0-9]{3}", value):
            port = self.by_locode.get(value.upper())
            if not port:
                raise ValueError(f"未找到 UN/LOCODE: {value.upper()}")
            self.query_cache[value.casefold()] = port
            return port
        normalized = _romanize(value)
        country = _country_hint(value)
        exact = [
            port for port in self.by_name.get(normalized, [])
            if not country or port.country == country
        ]
        if exact:
            exact.sort(key=lambda port: (port.locode.startswith("WPI"), port.locode))
            self.query_cache[value.casefold()] = exact[0]
            return exact[0]
        if not allow_fuzzy or not normalized:
            raise ValueError(f"无法识别港口: {query}")
        choices = [
            name for name, ports in self.by_name.items()
            if not country or any(port.country == country for port in ports)
        ]
        matches = process.extract(
            normalized,
            choices,
            scorer=fuzz.WRatio,
            score_cutoff=88,
            limit=4,
        )
        candidates: list[tuple[float, Port]] = []
        for name, score, _ in matches:
            for port in self.by_name[name]:
                if not country or port.country == country:
                    candidates.append((score, port))
        candidates.sort(key=lambda item: (-item[0], item[1].locode))
        if not candidates:
            raise ValueError(f"无法识别港口: {query}")
        if (
            len(candidates) > 1
            and candidates[0][0] - candidates[1][0] < 2.5
            and candidates[0][1].country != candidates[1][1].country
        ):
            raise ValueError(f"港口名称有歧义: {query}，请提供国家或 UN/LOCODE")
        self.query_cache[value.casefold()] = candidates[0][1]
        return candidates[0][1]

    def resolve_field(self, value: str) -> list[Port]:
        raw = (value or "").strip()
        if not raw or re.search(
            r"(全国|中国沿海|国内沿海|不限|无限航区|全球|世界范围)",
            raw,
        ):
            return []
        if raw.casefold() in self.field_cache:
            return self.field_cache[raw.casefold()]
        cleaned = re.sub(r"^\s*(?:空船?|空港|open\s*)", "", raw, flags=re.I)
        parts = [cleaned]
        parts.extend(
            part.strip(" ,.")
            for part in re.split(
                r"[/、;；]|\s+(?:or|and/or|或)\s+",
                cleaned,
                flags=re.I,
            )
            if part.strip(" ,.")
        )
        resolved: list[Port] = []
        seen: set[str] = set()
        for part in parts:
            for candidate in (part, part.split(",", 1)[0].strip()):
                try:
                    port = self.resolve(candidate, allow_fuzzy=False)
                except ValueError:
                    continue
                if port.locode not in seen:
                    seen.add(port.locode)
                    resolved.append(port)
        self.field_cache[raw.casefold()] = resolved
        return resolved


def infer_trade(load_port: Port, discharge_port: Port) -> str:
    return (
        "domestic"
        if load_port.country == "CN" and discharge_port.country == "CN"
        else "international"
    )
