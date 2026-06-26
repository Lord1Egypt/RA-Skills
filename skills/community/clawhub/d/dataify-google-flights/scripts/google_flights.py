#!/usr/bin/env python3
"""Call Dataify Scraper API Google Flights and print the raw response body."""

from __future__ import annotations

import argparse
import json as json_module
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


API_URL = "https://scraperapi.dataify.com/request"

FIELDS = (
    "departure_id",
    "arrival_id",
    "json",
    "gl",
    "hl",
    "currency",
    "type",
    "outbound_date",
    "return_date",
    "travel_class",
    "multi_city_json",
    "show_hidden",
    "exclude_basic",
    "deep_search",
    "adults",
    "children",
    "infants_in_seat",
    "infants_on_lap",
    "sort_by",
    "stops",
    "exclude_airlines",
    "include_airlines",
    "bags",
    "max_price",
    "outbound_times",
    "return_times",
    "emissions",
    "layover_duration",
    "exclude_conns",
    "max_duration",
    "departure_token",
    "no_cache",
)

DEFAULTS = {
    "engine": "google_flights",
    "json": "1",
    "currency": "USD",
    "type": "1",
    "travel_class": "1",
    "show_hidden": "false",
    "exclude_basic": "false",
    "deep_search": "false",
    "adults": "1",
    "children": "0",
    "infants_in_seat": "0",
    "infants_on_lap": "0",
    "sort_by": "1",
    "stops": "0",
    "bags": "0",
    "no_cache": "false",
}

BOOLEAN_FIELDS = {"show_hidden", "exclude_basic", "deep_search", "no_cache"}
BOOLEAN_TRUE = {
    "1",
    "true",
    "yes",
    "y",
    "on",
    "enable",
    "enabled",
    "open",
    "开启",
    "打开",
    "启用",
    "是",
    "需要",
}
BOOLEAN_FALSE = {
    "0",
    "false",
    "no",
    "n",
    "off",
    "disable",
    "disabled",
    "close",
    "关闭",
    "禁用",
    "否",
    "不需要",
}

OUTPUT_MODE_ALIASES = {
    "1": "1",
    "json": "1",
    "2": "2",
    "jsonhtml": "2",
    "htmljson": "2",
    "json+html": "2",
    "html+json": "2",
    "3": "3",
    "html": "3",
    "4": "4",
    "lightjson": "4",
    "litejson": "4",
}

TYPE_ALIASES = {
    "1": "1",
    "roundtrip": "1",
    "round": "1",
    "returntrip": "1",
    "往返": "1",
    "返程": "1",
    "2": "2",
    "oneway": "2",
    "single": "2",
    "singletrip": "2",
    "单程": "2",
    "3": "3",
    "multicity": "3",
    "multi-city": "3",
    "多城市": "3",
}

TRAVEL_CLASS_ALIASES = {
    "1": "1",
    "economy": "1",
    "经济舱": "1",
    "经济": "1",
    "2": "2",
    "premiumeconomy": "2",
    "premium": "2",
    "高级经济舱": "2",
    "超经": "2",
    "3": "3",
    "business": "3",
    "businessclass": "3",
    "商务舱": "3",
    "商务": "3",
    "4": "4",
    "first": "4",
    "firstclass": "4",
    "头等舱": "4",
    "头等": "4",
}

SORT_BY_ALIASES = {
    "1": "1",
    "best": "1",
    "popular": "1",
    "recommended": "1",
    "热门": "1",
    "推荐": "1",
    "最佳": "1",
    "2": "2",
    "price": "2",
    "cheapest": "2",
    "价格": "2",
    "最便宜": "2",
    "3": "3",
    "departuretime": "3",
    "departtime": "3",
    "起飞时间": "3",
    "出发时间": "3",
    "4": "4",
    "arrivaltime": "4",
    "到达时间": "4",
    "5": "5",
    "duration": "5",
    "flightduration": "5",
    "飞行时长": "5",
    "时长": "5",
    "6": "6",
    "emissions": "6",
    "carbon": "6",
    "排放": "6",
}

STOPS_ALIASES = {
    "0": "0",
    "any": "0",
    "anystops": "0",
    "不限中转": "0",
    "任意经停": "0",
    "1": "1",
    "nonstop": "1",
    "direct": "1",
    "直飞": "1",
    "无中转": "1",
    "2": "2",
    "onestop": "2",
    "1stop": "2",
    "oneorless": "2",
    "最多一次中转": "2",
    "经停1次或更少": "2",
    "3": "3",
    "twostops": "3",
    "2stops": "3",
    "twoorless": "3",
    "最多两次中转": "3",
    "经停2次或更少": "3",
}

COUNTRY_ALIASES = {
    "美国": "us",
    "united states": "us",
    "usa": "us",
    "us": "us",
    "中国": "cn",
    "china": "cn",
    "cn": "cn",
    "日本": "jp",
    "japan": "jp",
    "jp": "jp",
    "英国": "uk",
    "united kingdom": "uk",
    "uk": "uk",
    "法国": "fr",
    "france": "fr",
    "fr": "fr",
    "德国": "de",
    "germany": "de",
    "de": "de",
    "加拿大": "ca",
    "canada": "ca",
    "澳大利亚": "au",
    "australia": "au",
}

LANGUAGE_ALIASES = {
    "中文": "zh-cn",
    "简体中文": "zh-cn",
    "繁体中文": "zh-tw",
    "英文": "en",
    "英语": "en",
    "english": "en",
    "en": "en",
    "日文": "ja",
    "日语": "ja",
    "japanese": "ja",
    "ja": "ja",
    "法文": "fr",
    "法语": "fr",
    "french": "fr",
    "fr": "fr",
    "德文": "de",
    "德语": "de",
    "german": "de",
    "de": "de",
    "西班牙语": "es",
    "spanish": "es",
    "es": "es",
}

PARAMETER_CATALOG = {
    "required": [
        {"name": "Authorization", "default": None, "description": "Dataify API token，放在 Authorization 请求头中。"},
        {"name": "engine", "default": "google_flights", "description": "固定引擎值，Google Flights 必须使用 google_flights。"},
        {"name": "json", "default": "1", "description": "返回格式：1 表示 JSON，2 表示 JSON+HTML，3 表示 HTML，4 表示轻量 JSON。"},
    ],
    "flight_inputs": [
        {"name": "departure_id", "default": None, "description": "出发机场代码或 Google kgmid；可用逗号分隔多个值。"},
        {"name": "arrival_id", "default": None, "description": "到达机场代码或 Google kgmid；可用逗号分隔多个值。"},
        {"name": "outbound_date", "default": None, "description": "出发日期，格式为 YYYY-MM-DD；未指定时不传该参数。"},
        {"name": "return_date", "default": None, "description": "返程日期，格式为 YYYY-MM-DD；未指定时不传该参数。"},
        {"name": "multi_city_json", "default": None, "description": "多城市航班信息，type=3 时使用，值为航段对象组成的 JSON 字符串。"},
        {"name": "departure_token", "default": None, "description": "从上一轮出发航班结果中获得的 token，用于选择航班并获取返程或下一段航班。"},
    ],
    "optional": [
        {"name": "gl", "default": None, "description": "Google Flights 使用的国家或地区代码，例如 us、uk、fr、cn。"},
        {"name": "hl", "default": None, "description": "Google Flights 使用的语言代码，例如 en、zh-cn、ja、fr。"},
        {"name": "currency", "default": "USD", "description": "返回价格使用的货币，默认 USD。"},
        {"name": "type", "default": "1", "description": "航班类型：1 往返，2 单程，3 多城市；默认 1。"},
        {"name": "travel_class", "default": "1", "description": "舱位：1 经济舱，2 高级经济舱，3 商务舱，4 头等舱；默认 1。"},
        {"name": "show_hidden", "default": "false", "description": "是否包含隐藏航班结果；默认 false。"},
        {"name": "exclude_basic", "default": "false", "description": "是否排除基础经济舱票价；默认 false。该过滤通常只适用于美国国内航班。"},
        {"name": "deep_search", "default": "false", "description": "是否启用深度搜索；默认 false。深度搜索可能结果更完整，但响应更慢。"},
        {"name": "adults", "default": "1", "description": "成人乘客数量；默认 1。"},
        {"name": "children", "default": "0", "description": "儿童乘客数量；默认 0。"},
        {"name": "infants_in_seat", "default": "0", "description": "占座婴儿数量；默认 0。"},
        {"name": "infants_on_lap", "default": "0", "description": "不占座婴儿数量；默认 0。"},
        {"name": "sort_by", "default": "1", "description": "排序方式：1 最佳/热门，2 价格，3 出发时间，4 到达时间，5 飞行时长，6 排放量；默认 1。"},
        {"name": "stops", "default": "0", "description": "经停过滤：0 任意经停次数，1 仅直飞，2 最多 1 次经停，3 最多 2 次经停；默认 0。"},
        {"name": "exclude_airlines", "default": None, "description": "要排除的航空公司代码，多个代码用逗号分隔；不能与 include_airlines 同时使用。"},
        {"name": "include_airlines", "default": None, "description": "要包含的航空公司代码，多个代码用逗号分隔；不能与 exclude_airlines 同时使用。"},
        {"name": "bags", "default": "0", "description": "随身行李数量；默认 0。"},
        {"name": "max_price", "default": None, "description": "最高票价；未指定时不限制。"},
        {"name": "outbound_times", "default": None, "description": "出发航段时间范围，使用两个或四个逗号分隔的小时数字。"},
        {"name": "return_times", "default": None, "description": "返程航段时间范围，使用两个或四个逗号分隔的小时数字。"},
        {"name": "emissions", "default": None, "description": "排放过滤；值为 1 时仅返回低排放航班。"},
        {"name": "layover_duration", "default": None, "description": "中转时长范围，单位分钟，格式为 min,max。"},
        {"name": "exclude_conns", "default": None, "description": "要排除的中转机场代码，多个代码用逗号分隔。"},
        {"name": "max_duration", "default": None, "description": "最长总飞行时长，单位分钟。"},
        {"name": "no_cache", "default": "false", "description": "是否跳过缓存；true 表示跳过缓存，false 表示使用缓存；默认 false。"},
    ],
}


def iter_parameter_items() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for section in ("required", "flight_inputs", "optional"):
        for item in PARAMETER_CATALOG[section]:
            if item["name"] != "Authorization":
                items.append(item)
    return items


def build_parameter_table(params: dict[str, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in iter_parameter_items():
        name = item["name"]
        default = item.get("default")
        rows.append(
            {
                "参数名": name,
                "当前值": params.get(name, ""),
                "默认值": "" if default is None else str(default),
                "说明": item["description"],
            }
        )
    return rows


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def format_parameter_table(rows: list[dict[str, str]]) -> str:
    headers = ("参数名", "当前值", "默认值", "说明")
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Flights API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Flights fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print normalized parameters and catalog instead of calling API.")
    parser.add_argument(
        "--dry-run-format",
        choices=("json", "markdown"),
        default="json",
        help="Dry-run output format. Use markdown for the pre-call parameter table.",
    )

    for field in FIELDS:
        parser.add_argument(f"--{field}", dest=field)

    return parser.parse_args()


def clean_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).strip()
    return text if text else None


def compact_text(value: Any) -> str:
    return re.sub(r"[\s_\-+]+", "", str(value).strip().lower())


def normalize_boolean(value: Any) -> str:
    text = str(value).strip().lower()
    if text in BOOLEAN_TRUE:
        return "true"
    if text in BOOLEAN_FALSE:
        return "false"
    return str(value).strip()


def normalize_choice(value: Any, aliases: dict[str, str]) -> str:
    text = str(value).strip()
    lowered = text.lower()
    compact = compact_text(text)
    if lowered in aliases:
        return aliases[lowered]
    if compact in aliases:
        return aliases[compact]
    if text in aliases:
        return aliases[text]
    return text


def normalize_output_mode(value: Any) -> str:
    return normalize_choice(value, OUTPUT_MODE_ALIASES)


def normalize_date(value: Any) -> str:
    text = str(value).strip()
    match = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", text)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return text


def normalize_location_id(value: str) -> str:
    text = value.strip()
    return text.lower() if text.startswith("/") else text.upper()


def normalize_location_ids(value: str) -> str:
    return ",".join(normalize_location_id(part) for part in value.split(","))


def find_alias(text: str, aliases: dict[str, str]) -> str | None:
    lowered = text.lower()
    for label, code in aliases.items():
        if label.lower() in lowered:
            return code
    return None


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        value = raw_value.strip().strip("\"'")
        params[field.lower()] = value
    return params


def parse_route(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    airport = r"([A-Z]{3}|/[a-zA-Z0-9_]+)"
    patterns = (
        rf"(?:from|depart(?:ing)? from)\s+{airport}\s+(?:to|->)\s+{airport}",
        rf"从\s*{airport}\s*(?:到|至|飞往|->)\s*{airport}",
        rf"\b{airport}\s*(?:to|->|到|至|飞往)\s*{airport}\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["departure_id"] = normalize_location_id(match.group(1))
            params["arrival_id"] = normalize_location_id(match.group(2))
            return params

    codes = re.findall(r"\b[A-Z]{3}\b", text)
    if len(codes) >= 2:
        params["departure_id"] = normalize_location_id(codes[0])
        params["arrival_id"] = normalize_location_id(codes[1])
    return params


def parse_dates(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    dates = re.findall(r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b", text)
    normalized = [normalize_date(date) for date in dates]
    if normalized:
        params["outbound_date"] = normalized[0]
    if len(normalized) > 1:
        params["return_date"] = normalized[1]
    return params


def parse_count(text: str, labels: tuple[str, ...]) -> str | None:
    label_pattern = "|".join(re.escape(label) for label in labels)
    patterns = (
        rf"(\d+)\s*(?:{label_pattern})",
        rf"(?:{label_pattern})\s*[:=]?\s*(\d+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def parse_price(text: str) -> str | None:
    patterns = (
        r"(?:max(?:imum)? price|under|below|no more than)\s*[:=]?\s*\$?\s*(\d+(?:\.\d+)?)",
        r"(?:最高|不超过|低于|预算)\s*[:=]?\s*(\d+(?:\.\d+)?)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))

    for key, value in parse_route(text).items():
        params.setdefault(key, value)
    for key, value in parse_dates(text).items():
        params.setdefault(key, value)

    lowered = text.lower()

    if "type" not in params:
        if any(marker in lowered for marker in ("multi-city", "multicity", "多城市")):
            params["type"] = "3"
        elif any(marker in lowered for marker in ("one-way", "one way", "single trip", "单程")):
            params["type"] = "2"
        elif any(marker in lowered for marker in ("round trip", "roundtrip", "return trip", "往返")):
            params["type"] = "1"

    if "travel_class" not in params:
        for marker, value in TRAVEL_CLASS_ALIASES.items():
            if marker and marker in lowered:
                params["travel_class"] = value
                break

    if "sort_by" not in params:
        for marker, value in SORT_BY_ALIASES.items():
            if marker and marker in lowered:
                params["sort_by"] = value
                break

    if "stops" not in params:
        if any(marker in lowered for marker in ("nonstop", "direct", "直飞", "无中转")):
            params["stops"] = "1"
        elif any(marker in lowered for marker in ("one stop", "1 stop", "最多一次中转")):
            params["stops"] = "2"
        elif any(marker in lowered for marker in ("two stops", "2 stops", "最多两次中转")):
            params["stops"] = "3"

    if "gl" not in params:
        country = find_alias(text, COUNTRY_ALIASES)
        if country:
            params["gl"] = country

    if "hl" not in params:
        language = find_alias(text, LANGUAGE_ALIASES)
        if language:
            params["hl"] = language

    currency_match = re.search(r"\b(USD|CNY|RMB|EUR|JPY|GBP|AUD|CAD|HKD|SGD)\b", text, flags=re.IGNORECASE)
    if currency_match and "currency" not in params:
        currency = currency_match.group(1).upper()
        params["currency"] = "CNY" if currency == "RMB" else currency

    passenger_fields = {
        "adults": ("adult", "adults", "成人", "大人"),
        "children": ("child", "children", "kids", "儿童", "小孩"),
        "infants_in_seat": ("infant in seat", "infants in seat", "占座婴儿"),
        "infants_on_lap": ("infant on lap", "infants on lap", "lap infant", "不占座婴儿", "抱婴"),
        "bags": ("bag", "bags", "carry-on", "随身行李", "行李"),
    }
    for field, labels in passenger_fields.items():
        if field not in params:
            count = parse_count(text, labels)
            if count is not None:
                params[field] = count

    if "max_price" not in params:
        price = parse_price(text)
        if price is not None:
            params["max_price"] = price

    if "emissions" not in params and any(marker in lowered for marker in ("low emission", "低排放", "低碳")):
        params["emissions"] = "1"

    boolean_markers = {
        "show_hidden": ("show hidden", "include hidden", "隐藏航班"),
        "exclude_basic": ("exclude basic", "no basic economy", "排除基础经济舱"),
        "deep_search": ("deep search", "深度搜索"),
        "no_cache": ("no cache", "bypass cache", "跳过缓存", "不走缓存", "不用缓存"),
    }
    for field, markers in boolean_markers.items():
        if field not in params and any(marker in lowered for marker in markers):
            params[field] = "true"

    output_checks = (
        ("json+html", "2"),
        ("html+json", "2"),
        ("light json", "4"),
        ("lite json", "4"),
        ("html", "3"),
        ("json", "1"),
    )
    if "json" not in params:
        for marker, mode in output_checks:
            if marker in lowered:
                params["json"] = mode
                break

    return params


def merge_params(args: argparse.Namespace) -> dict[str, str]:
    params: dict[str, str] = {}

    if args.request:
        params.update(parse_natural_request(args.request))

    if args.params_json:
        try:
            supplied = json_module.loads(args.params_json)
        except json_module.JSONDecodeError as exc:
            raise ValueError(f"--params-json 不是有效 JSON: {exc}") from exc
        if not isinstance(supplied, dict):
            raise ValueError("--params-json 必须是 JSON object")
        for key, value in supplied.items():
            normalized_key = str(key).strip()
            if normalized_key == "engine":
                continue
            if normalized_key in FIELDS:
                cleaned = clean_value(value)
                if cleaned is not None:
                    params[normalized_key] = cleaned

    for field in FIELDS:
        value = clean_value(getattr(args, field))
        if value is not None:
            params[field] = value

    return normalize_params(params)


def normalize_params(params: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = dict(DEFAULTS)

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    normalized["engine"] = "google_flights"
    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))
    normalized["type"] = normalize_choice(normalized.get("type", "1"), TYPE_ALIASES)
    normalized["travel_class"] = normalize_choice(normalized.get("travel_class", "1"), TRAVEL_CLASS_ALIASES)
    normalized["sort_by"] = normalize_choice(normalized.get("sort_by", "1"), SORT_BY_ALIASES)
    normalized["stops"] = normalize_choice(normalized.get("stops", "0"), STOPS_ALIASES)

    for field in BOOLEAN_FIELDS:
        if field in normalized:
            normalized[field] = normalize_boolean(normalized[field])

    for field in ("outbound_date", "return_date"):
        if field in normalized:
            normalized[field] = normalize_date(normalized[field])

    if "gl" in normalized:
        normalized["gl"] = COUNTRY_ALIASES.get(normalized["gl"].lower(), normalized["gl"].lower())

    if "hl" in normalized:
        normalized["hl"] = LANGUAGE_ALIASES.get(normalized["hl"].lower(), normalized["hl"].lower())

    if "currency" in normalized:
        normalized["currency"] = normalized["currency"].upper()

    for field in ("departure_id", "arrival_id"):
        if field in normalized:
            normalized[field] = normalize_location_ids(normalized[field])

    for field in ("exclude_airlines", "include_airlines", "exclude_conns"):
        if field in normalized:
            normalized[field] = normalized[field].upper()

    return normalized


def validate_date(field: str, params: dict[str, str], errors: list[str]) -> None:
    value = params.get(field)
    if value and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        errors.append(f"{field} 必须使用 YYYY-MM-DD 格式")


def validate_params(params: dict[str, str]) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    errors: list[str] = []

    if params.get("include_airlines") and params.get("exclude_airlines"):
        errors.append("include_airlines 和 exclude_airlines 不能同时使用")

    if params.get("type") not in {"1", "2", "3"}:
        errors.append("type 必须是 1、2 或 3")

    if params.get("json") not in {"1", "2", "3", "4"}:
        errors.append("json 必须是 1、2、3 或 4")

    if params.get("travel_class") not in {"1", "2", "3", "4"}:
        errors.append("travel_class 必须是 1、2、3 或 4")

    if params.get("sort_by") not in {"1", "2", "3", "4", "5", "6"}:
        errors.append("sort_by 必须是 1、2、3、4、5 或 6")

    if params.get("stops") not in {"0", "1", "2", "3"}:
        errors.append("stops 必须是 0、1、2 或 3")

    validate_date("outbound_date", params, errors)
    validate_date("return_date", params, errors)

    if not params.get("departure_token") and params.get("type", "1") == "3" and not params.get("multi_city_json"):
        missing.append("multi_city_json")

    try:
        passengers_with_bag_allowance = (
            int(params.get("adults", "0"))
            + int(params.get("children", "0"))
            + int(params.get("infants_in_seat", "0"))
        )
        if int(params.get("bags", "0")) > passengers_with_bag_allowance:
            errors.append("bags 不应超过成人、儿童和占座婴儿的总人数")
    except ValueError:
        errors.append("乘客数量和 bags 必须是整数")

    return missing, errors


def token_status(token_arg: str | None) -> str:
    if clean_value(token_arg):
        return "provided_by_argument"
    if clean_value(os.environ.get("DATAIFY_API_TOKEN")):
        return "from_DATAIFY_API_TOKEN"
    return "missing"


def get_authorization(token_arg: str | None) -> str | None:
    token = clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        return None
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def build_dry_run(params: dict[str, str]) -> dict[str, Any]:
    missing, errors = validate_params(params)
    return {
        "api_url": API_URL,
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded; charset=utf-8",
        "parameter_table": build_parameter_table(params),
        "documented_defaults": DEFAULTS,
        "mapped_payload": params,
        "missing_parameters": missing,
        "validation_errors": errors,
    }


def call_api(params: dict[str, str], authorization: str, timeout: float) -> int:
    body = urllib.parse.urlencode(params).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": authorization,
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept": "*/*",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            sys.stdout.buffer.write(response.read())
            return 0
    except urllib.error.HTTPError as exc:
        error_body = exc.read()
        if error_body:
            sys.stdout.buffer.write(error_body)
        else:
            print(f"HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"请求 Dataify API 失败: {exc.reason}", file=sys.stderr)
        return 1


def main() -> int:
    configure_stdio()
    args = parse_args()

    try:
        params = merge_params(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.dry_run:
        preview = build_dry_run(params)
        if args.dry_run_format == "markdown":
            print(format_parameter_table(preview["parameter_table"]))
        else:
            print(json_module.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    missing, errors = validate_params(params)
    if missing or errors:
        if missing:
            print("缺少参数: " + ", ".join(missing), file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 2

    authorization = get_authorization(args.token)
    if not authorization:
        print("缺少 Dataify API token，请提供 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。", file=sys.stderr)
        return 2

    return call_api(params, authorization, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
