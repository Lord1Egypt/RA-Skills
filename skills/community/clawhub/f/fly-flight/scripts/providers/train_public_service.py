#!/usr/bin/env python3
"""Train provider for querying China high-speed rail from official 12306 public endpoints."""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import ssl
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import HTTPSHandler, HTTPCookieProcessor, Request, build_opener, urlopen


ROOT = Path(__file__).resolve().parent.parent.parent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
STATION_JS_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9367"
LEFT_TICKET_URL = "https://kyfw.12306.cn/otn/leftTicket/queryG"
LEFT_TICKET_INIT_URL = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
PUBLIC_PRICE_URL = "https://kyfw.12306.cn/otn/leftTicketPrice/queryAllPublicPrice"
TRAIN_SORT_MODES = {"price", "departure", "arrival", "duration"}
DEFAULT_SSL_CONTEXT = ssl._create_unverified_context()


@dataclass(frozen=True)
class Station:
    raw: str
    query: str
    code: str
    city: str
    resolved_as: str


STATION_CACHE: dict[str, Station] | None = None


def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期必须是 YYYY-MM-DD 格式") from exc
    return value


def fetch_text(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout, context=DEFAULT_SSL_CONTEXT) as response:
        return response.read().decode("utf-8", "ignore")


def fetch_json(url: str, params: dict[str, str], timeout: int) -> dict[str, Any]:
    query = urlencode(params)
    request = Request(f"{url}?{query}", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout, context=DEFAULT_SSL_CONTEXT) as response:
        return json.loads(response.read().decode("utf-8-sig", "ignore"))


def build_session_opener() -> Any:
    cookie_jar = http.cookiejar.CookieJar()
    return build_opener(
        HTTPCookieProcessor(cookie_jar),
        HTTPSHandler(context=DEFAULT_SSL_CONTEXT),
    )


def load_stations(timeout: int) -> dict[str, Station]:
    global STATION_CACHE
    if STATION_CACHE is not None:
        return STATION_CACHE

    raw = fetch_text(STATION_JS_URL, timeout)
    _, _, payload = raw.partition("'")
    payload, _, _ = payload.rpartition("'")
    stations: dict[str, Station] = {}
    parsed_stations: list[tuple[Station, str]] = []

    for item in payload.split("@"):
        if not item:
            continue
        parts = item.split("|")
        if len(parts) < 8:
            continue
        _, station_name, telecode, pinyin_full, pinyin_short, _, city_code, city_name, *_ = parts
        station = Station(
            raw=station_name,
            query=station_name,
            code=telecode,
            city=city_name or station_name,
            resolved_as="station",
        )
        parsed_stations.append((station, city_code))
        for key in {
            station_name,
            telecode.upper(),
            pinyin_full.lower(),
            pinyin_short.lower(),
        }:
            if key and key not in stations:
                stations[key] = station

    for station, city_code in parsed_stations:
        if station.raw == station.city:
            stations[station.city] = station
            if city_code:
                stations[city_code] = station

    STATION_CACHE = stations
    return stations


def resolve_station(value: str, timeout: int) -> Station:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("地点不能为空")
    if len(cleaned) == 3 and cleaned.isalpha():
        stations = load_stations(timeout)
        station = stations.get(cleaned.upper())
        if station:
            return Station(raw=value, query=cleaned.upper(), code=station.code, city=station.city, resolved_as="telecode")
        raise ValueError(f"无法识别车站代码“{value}”。")

    normalized = cleaned.replace(" ", "")
    stations = load_stations(timeout)
    for key in (normalized, normalized.lower()):
        station = stations.get(key)
        if station:
            resolved_as = "city" if key == station.city else "station"
            return Station(raw=value, query=normalized, code=station.code, city=station.city, resolved_as=resolved_as)
    raise ValueError(f"无法识别地点“{value}”。请使用常见城市名、具体车站名，或 12306 三字码。")


def fetch_left_ticket_payload(
    origin: Station,
    destination: Station,
    departure_date: str,
    *,
    timeout: int,
    sample_query: str | None,
) -> dict[str, Any]:
    if sample_query:
        with open(sample_query, "r", encoding="utf-8") as handle:
            return json.load(handle)
    opener = build_session_opener()
    init_request = Request(LEFT_TICKET_INIT_URL, headers={"User-Agent": USER_AGENT})
    opener.open(init_request, timeout=timeout).read()
    query = urlencode(
        {
            "leftTicketDTO.train_date": departure_date,
            "leftTicketDTO.from_station": origin.code,
            "leftTicketDTO.to_station": destination.code,
            "purpose_codes": "ADULT",
        }
    )
    request = Request(f"{LEFT_TICKET_URL}?{query}", headers={"User-Agent": USER_AGENT})
    with opener.open(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8-sig", "ignore"))


def fetch_price_payload(
    origin: Station,
    destination: Station,
    departure_date: str,
    *,
    timeout: int,
    sample_price: str | None,
) -> dict[str, Any]:
    if sample_price:
        with open(sample_price, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return fetch_json(
        PUBLIC_PRICE_URL,
        {
            "leftTicketDTO.train_date": departure_date,
            "leftTicketDTO.from_station": origin.code,
            "leftTicketDTO.to_station": destination.code,
            "purpose_codes": "ADULT",
            "randCode": "",
        },
        timeout,
    )


def parse_seat_price(value: str | None) -> int | None:
    if not value:
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return None
    return int(digits)


def format_price(value: int | None) -> float | None:
    if value is None:
        return None
    return round(value / 10.0, 1)


def duration_minutes(value: str | None) -> int:
    if not value or ":" not in value:
        return 10**9
    hours, minutes = value.split(":", 1)
    return int(hours) * 60 + int(minutes)


def time_sort_value(time_value: str | None) -> str:
    return time_value or "99:99"


def normalize_availability(value: str | None) -> str | None:
    if value in {"", None, "--"}:
        return None
    return value


def build_price_index(price_payload: dict[str, Any]) -> dict[tuple[str, str, str, str], dict[str, float | None]]:
    index: dict[tuple[str, str, str, str], dict[str, float | None]] = {}
    for item in price_payload.get("data") or []:
        dto = item.get("queryLeftNewDTO") or {}
        key = (
            dto.get("station_train_code") or "",
            dto.get("from_station_telecode") or "",
            dto.get("to_station_telecode") or "",
            dto.get("start_time") or "",
        )
        index[key] = {
            "business_class": format_price(parse_seat_price(dto.get("swz_price"))),
            "first_class": format_price(parse_seat_price(dto.get("zy_price"))),
            "second_class": format_price(parse_seat_price(dto.get("ze_price"))),
        }
    return index


def train_type_matches(train_code: str, train_type: str | None) -> bool:
    if not train_type:
        return True
    wanted = {item.strip().upper() for item in train_type.split(",") if item.strip()}
    return bool(wanted) and train_code[:1].upper() in wanted


def compute_display_price(seat_prices: dict[str, float | None], seat_type: str | None) -> float | None:
    if seat_type:
        return seat_prices.get(seat_type)
    prices = [price for price in seat_prices.values() if price is not None]
    if not prices:
        return None
    return min(prices)


def simplify_train(
    row: str,
    station_map: dict[str, str],
    price_index: dict[tuple[str, str, str, str], dict[str, float | None]],
    *,
    seat_type: str | None,
) -> dict[str, Any]:
    parts = row.split("|")
    key = (parts[3], parts[6], parts[7], parts[8])
    seat_prices = price_index.get(
        key,
        {"business_class": None, "first_class": None, "second_class": None},
    )
    seat_availability = {
        "second_class": normalize_availability(parts[30]),
        "first_class": normalize_availability(parts[31]),
        "business_class": normalize_availability(parts[32]),
    }

    return {
        "train_no": parts[3],
        "train_internal_no": parts[2],
        "train_type": (parts[3] or "")[:1],
        "train_class_name": "高速" if (parts[3] or "").startswith("G") else "动车",
        "bookable": parts[1] == "预订" and parts[11] == "Y",
        "departure_code": parts[6],
        "departure_name": station_map.get(parts[6], parts[6]),
        "arrival_code": parts[7],
        "arrival_name": station_map.get(parts[7], parts[7]),
        "start_station_code": parts[4],
        "start_station_name": station_map.get(parts[4], parts[4]),
        "end_station_code": parts[5],
        "end_station_name": station_map.get(parts[5], parts[5]),
        "departure_time": parts[8],
        "arrival_time": parts[9],
        "duration": parts[10],
        "seat_prices": seat_prices,
        "seat_availability": seat_availability,
        "ticket_price": compute_display_price(seat_prices, seat_type),
        "raw": parts,
    }


def filter_trains(
    trains: list[dict[str, Any]],
    *,
    train_type: str | None,
    preferred_departure_station: str | None,
    preferred_arrival_station: str | None,
    seat_type: str | None,
    timeout: int,
) -> list[dict[str, Any]]:
    departure_code = resolve_station(preferred_departure_station, timeout).code if preferred_departure_station else None
    arrival_code = resolve_station(preferred_arrival_station, timeout).code if preferred_arrival_station else None

    filtered = trains
    if train_type:
        filtered = [train for train in filtered if train_type_matches(train.get("train_no") or "", train_type)]
    if departure_code:
        filtered = [train for train in filtered if train.get("departure_code") == departure_code]
    if arrival_code:
        filtered = [train for train in filtered if train.get("arrival_code") == arrival_code]
    if seat_type:
        filtered = [train for train in filtered if train.get("seat_prices", {}).get(seat_type) is not None]
    return filtered


def sort_trains(trains: list[dict[str, Any]], sort_by: str) -> list[dict[str, Any]]:
    if sort_by == "departure":
        return sorted(
            trains,
            key=lambda item: (
                time_sort_value(item.get("departure_time")),
                item.get("ticket_price") is None,
                item.get("ticket_price") or 0,
            ),
        )
    if sort_by == "arrival":
        return sorted(
            trains,
            key=lambda item: (
                time_sort_value(item.get("arrival_time")),
                item.get("ticket_price") is None,
                item.get("ticket_price") or 0,
            ),
        )
    if sort_by == "duration":
        return sorted(
            trains,
            key=lambda item: (
                duration_minutes(item.get("duration")),
                item.get("ticket_price") is None,
                item.get("ticket_price") or 0,
            ),
        )
    return sorted(trains, key=lambda item: (item.get("ticket_price") is None, item.get("ticket_price") or 0))


def normalize_leg_response(
    query_payload: dict[str, Any],
    price_payload: dict[str, Any],
    origin: Station,
    destination: Station,
    departure_date: str,
    limit: int,
    *,
    sort_by: str,
    train_type: str | None,
    seat_type: str | None,
    preferred_departure_station: str | None,
    preferred_arrival_station: str | None,
    timeout: int,
) -> dict[str, Any]:
    station_map = query_payload.get("data", {}).get("map") or {}
    price_index = build_price_index(price_payload)
    rows = query_payload.get("data", {}).get("result") or []
    trains = [
        simplify_train(row, station_map, price_index, seat_type=seat_type)
        for row in rows
        if row.split("|")[3][:1] in {"G", "D", "C"}
    ]
    trains = filter_trains(
        trains,
        train_type=train_type,
        preferred_departure_station=preferred_departure_station,
        preferred_arrival_station=preferred_arrival_station,
        seat_type=seat_type,
        timeout=timeout,
    )
    trains = sort_trains(trains, sort_by)
    trimmed = trains[:limit]

    return {
        "route": {
            "from": {"input": origin.raw, "query": origin.query, "code": origin.code, "resolved_as": origin.resolved_as},
            "to": {"input": destination.raw, "query": destination.query, "code": destination.code, "resolved_as": destination.resolved_as},
            "date": departure_date,
        },
        "count": len(trimmed),
        "total_found": len(trains),
        "sort_by": sort_by,
        "filters": {
            "train_type": train_type,
            "seat_type": seat_type,
            "preferred_departure_station": preferred_departure_station,
            "preferred_arrival_station": preferred_arrival_station,
        },
        "options": trimmed,
    }


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
        train_type=args.train_type,
        seat_type=args.seat_type,
        preferred_departure_station=args.preferred_departure_station,
        preferred_arrival_station=args.preferred_arrival_station,
        return_preferred_departure_station=args.return_preferred_departure_station,
        return_preferred_arrival_station=args.return_preferred_arrival_station,
        sample_train_query=args.sample_train_query,
        sample_train_price=args.sample_train_price,
        return_sample_train_query=args.return_sample_train_query,
        return_sample_train_price=args.return_sample_train_price,
    )


def run_search(args: argparse.Namespace) -> dict[str, Any]:
    if args.sort_by not in TRAIN_SORT_MODES:
        raise ValueError(f"sort_by 仅支持 {', '.join(sorted(TRAIN_SORT_MODES))}")
    if args.seat_type and args.seat_type not in {"business_class", "first_class", "second_class"}:
        raise ValueError("seat_type 仅支持 business_class, first_class, second_class")

    origin = resolve_station(args.origin, args.timeout)
    destination = resolve_station(args.destination, args.timeout)
    departure_date = validate_date(args.date)

    outbound_query = fetch_left_ticket_payload(
        origin,
        destination,
        departure_date,
        timeout=args.timeout,
        sample_query=args.sample_train_query,
    )
    outbound_price = fetch_price_payload(
        origin,
        destination,
        departure_date,
        timeout=args.timeout,
        sample_price=args.sample_train_price,
    )
    outbound = normalize_leg_response(
        outbound_query,
        outbound_price,
        origin,
        destination,
        departure_date,
        args.limit,
        sort_by=args.sort_by,
        train_type=args.train_type,
        seat_type=args.seat_type,
        preferred_departure_station=args.preferred_departure_station,
        preferred_arrival_station=args.preferred_arrival_station,
        timeout=args.timeout,
    )

    payload: dict[str, Any] = {
        "mode": "train",
        "provider": "12306-public",
        "reason": "success",
        "trip_type": "round-trip" if args.return_date else "one-way",
        "outbound": outbound,
    }

    if args.return_date:
        return_date = validate_date(args.return_date)
        return_query = fetch_left_ticket_payload(
            destination,
            origin,
            return_date,
            timeout=args.timeout,
            sample_query=args.return_sample_train_query or args.sample_train_query,
        )
        return_price = fetch_price_payload(
            destination,
            origin,
            return_date,
            timeout=args.timeout,
            sample_price=args.return_sample_train_price or args.sample_train_price,
        )
        payload["return"] = normalize_leg_response(
            return_query,
            return_price,
            destination,
            origin,
            return_date,
            args.limit,
            sort_by=args.return_sort_by or args.sort_by,
            train_type=args.train_type,
            seat_type=args.seat_type,
            preferred_departure_station=args.return_preferred_departure_station,
            preferred_arrival_station=args.return_preferred_arrival_station,
            timeout=args.timeout,
        )
    return payload
