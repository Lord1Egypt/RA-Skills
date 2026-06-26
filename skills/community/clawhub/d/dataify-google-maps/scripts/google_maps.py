#!/usr/bin/env python3
"""Call Dataify Scraper API Google Maps and print the raw response body."""

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
TOKEN_MISSING_MESSAGE = "缺少 Dataify API token，请提供 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"

FIELDS = (
    "q",
    "json",
    "ll",
    "location",
    "lat",
    "lon",
    "z",
    "m",
    "nearby",
    "google_domain",
    "hl",
    "gl",
    "start",
    "type",
    "data",
    "place_id",
    "data_cid",
    "no_cache",
)

COUNTRY_ALIASES = {
    "美国": "us",
    "美國": "us",
    "united states": "us",
    "usa": "us",
    "us": "us",
    "中国": "cn",
    "中國": "cn",
    "china": "cn",
    "cn": "cn",
    "日本": "jp",
    "japan": "jp",
    "jp": "jp",
    "英国": "uk",
    "英國": "uk",
    "united kingdom": "uk",
    "uk": "uk",
    "法国": "fr",
    "法國": "fr",
    "france": "fr",
    "fr": "fr",
    "德国": "de",
    "德國": "de",
    "germany": "de",
    "de": "de",
    "加拿大": "ca",
    "canada": "ca",
    "ca": "ca",
    "澳大利亚": "au",
    "澳洲": "au",
    "australia": "au",
    "au": "au",
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

BOOLEAN_TRUE = {
    "1",
    "true",
    "yes",
    "y",
    "on",
    "enable",
    "enabled",
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
    "关闭",
    "禁用",
    "否",
    "不需要",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Maps API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Maps fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized form payload instead of calling API.",
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


def normalize_boolean(value: Any) -> str:
    text = str(value).strip().lower()
    if text in BOOLEAN_TRUE:
        return "true"
    if text in BOOLEAN_FALSE:
        return "false"
    return str(value).strip()


def normalize_output_mode(value: Any) -> str:
    text = str(value).strip().lower()
    compact = re.sub(r"[\s_-]+", "", text)
    if compact in {"1", "json"}:
        return "1"
    if compact in {"2", "json+html", "jsonhtml", "html+json", "htmljson"}:
        return "2"
    if compact in {"3", "html"}:
        return "3"
    if compact in {"4", "lightjson", "litejson"}:
        return "4"
    return str(value).strip()


def find_alias(text: str, aliases: dict[str, str]) -> str | None:
    lowered = text.lower()
    for label, code in aliases.items():
        label_lower = label.lower()
        if re.fullmatch(r"[a-z]{2,3}(?:-[a-z0-9]+)?", label_lower):
            if re.search(rf"\b{re.escape(label_lower)}\b", lowered):
                return code
        elif label_lower in lowered:
            return code
    return None


def parse_page_start(text: str) -> str | None:
    patterns = (
        r"第\s*(\d+)\s*页",
        r"第\s*(\d+)\s*頁",
        r"page\s*(\d+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            page = max(int(match.group(1)), 1)
            return str((page - 1) * 20)

    match = re.search(r"\bstart\s*[:=]\s*(\d+)\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def parse_coordinates(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    lat_match = re.search(r"\b(?:lat|latitude|纬度)\s*[:=]\s*(-?\d+(?:\.\d+)?)", text, flags=re.IGNORECASE)
    lon_match = re.search(r"\b(?:lon|lng|longitude|经度)\s*[:=]\s*(-?\d+(?:\.\d+)?)", text, flags=re.IGNORECASE)
    if lat_match:
        params["lat"] = lat_match.group(1)
    if lon_match:
        params["lon"] = lon_match.group(1)
    return params


def parse_ll(text: str) -> str | None:
    match = re.search(r"@-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*\d+(?:z|m)\b", text)
    if match:
        return re.sub(r"\s+", "", match.group(0))
    return None


def parse_scale(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    z_match = re.search(r"\b(?:z|zoom|缩放|缩放级别)\s*[:=]?\s*(\d+)\b", text, flags=re.IGNORECASE)
    m_match = re.search(r"\b(?:m|height|map\s*height|地图高度)\s*[:=]?\s*(\d+)\b", text, flags=re.IGNORECASE)
    if z_match:
        params["z"] = z_match.group(1)
    if m_match:
        params["m"] = m_match.group(1)
    return params


def parse_identifier_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    place_id_match = re.search(r"\bplace[_\s-]?id\s*[:=]\s*([^\s,;，；]+)", text, flags=re.IGNORECASE)
    data_cid_match = re.search(r"\b(?:data[_\s-]?cid|cid)\s*[:=]\s*([^\s,;，；]+)", text, flags=re.IGNORECASE)
    if place_id_match:
        params["place_id"] = place_id_match.group(1).strip("\"'")
    if data_cid_match:
        params["data_cid"] = data_cid_match.group(1).strip("\"'")
    return params


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        params[field.lower()] = raw_value.strip().strip("\"'")
    return params


def clean_query_text(query: str) -> str:
    query = query.strip()
    query = re.sub(r"\s*(?:google\s*maps?|谷歌地图|地图|maps?)\s*$", "", query, flags=re.IGNORECASE)
    query = re.sub(r"\s*(?:返回|输出)\s*(?:json\+html|html\+json|light\s*json|json|html)\s*$", "", query, flags=re.IGNORECASE)
    return query.strip()


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        query = clean_query_text(quoted.group(1))
        if query:
            return query

    patterns = (
        r"(?:搜索|查找|查询|检索|抓取|采集|找|搜)\s*(?:google\s*)?(?:maps?|谷歌地图|地图)?\s*(.+?)(?:[，。；;]|$)",
        r"(?:google\s+maps|maps)\s+(?:search\s+for|search|find)\s+(.+?)(?:\s+with\b|\s+using\b|[,;.]|$)",
        r"(?:search\s+for|find)\s+(.+?)\s+(?:on|in)\s+(?:google\s+maps|maps)(?:[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query_text(match.group(1))
            if query:
                return query

    if not re.search(r"\b(?:token|authorization|engine|json|ll|lat|lon|z|m|hl|gl|start|type|place_id|data_cid)\b", text, flags=re.IGNORECASE):
        query = clean_query_text(text)
        if query:
            return query

    return None


def parse_explicit_location(text: str) -> str | None:
    patterns = (
        r"\blocation\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^,;，；]+)",
        r"(?:搜索起点|地图起点|以)\s*(.+?)\s*(?:为搜索起点|为地图起点|作为搜索起点)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().strip("\"'")
    return None


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))
    params.update({k: v for k, v in parse_identifier_fields(text).items() if k not in params})
    params.update({k: v for k, v in parse_coordinates(text).items() if k not in params})
    params.update({k: v for k, v in parse_scale(text).items() if k not in params})

    if "ll" not in params:
        ll = parse_ll(text)
        if ll:
            params["ll"] = ll

    if "location" not in params:
        location = parse_explicit_location(text)
        if location:
            params["location"] = location

    if "q" not in params:
        query = extract_query(text)
        if query:
            params["q"] = query

    lowered = text.lower()

    if "google." in lowered and "google_domain" not in params:
        domain_match = re.search(r"\bgoogle\.[a-z0-9.-]+\b", lowered)
        if domain_match:
            params["google_domain"] = domain_match.group(0)

    if "gl" not in params:
        country = find_alias(text, COUNTRY_ALIASES)
        if country:
            params["gl"] = country

    if "hl" not in params:
        language = find_alias(text, LANGUAGE_ALIASES)
        if language:
            params["hl"] = language

    if "start" not in params:
        start = parse_page_start(text)
        if start:
            params["start"] = start

    if "json" not in params:
        output_checks = (
            ("json+html", "2"),
            ("html+json", "2"),
            ("light json", "4"),
            ("lite json", "4"),
            ("html", "3"),
            ("json", "1"),
        )
        for marker, mode in output_checks:
            if marker in lowered:
                params["json"] = mode
                break

    if "type" not in params:
        if any(marker in lowered for marker in ("place details", "地点详情", "地點詳情", "详情", "詳情")):
            params["type"] = "place"
        elif any(marker in lowered for marker in ("search results", "搜索列表", "结果列表", "結果列表")):
            params["type"] = "search"

    boolean_markers = {
        "nearby": ("nearby", "near me", "附近", "周边", "周邊", "离我近", "離我近"),
        "no_cache": ("no_cache", "不走缓存", "跳过缓存", "绕过缓存", "bypass cache", "no cache"),
    }
    for field, markers in boolean_markers.items():
        if field not in params and any(marker in lowered for marker in markers):
            params[field] = "true"

    return params


def merge_params(args: argparse.Namespace) -> dict[str, str]:
    params: dict[str, str] = {}

    if args.request:
        params.update(parse_natural_request(args.request))

    if args.params_json:
        try:
            supplied = json_module.loads(args.params_json)
        except json_module.JSONDecodeError as exc:
            raise ValueError(f"--params-json is not valid JSON: {exc}") from exc
        if not isinstance(supplied, dict):
            raise ValueError("--params-json must be a JSON object")
        for key, value in supplied.items():
            if key in FIELDS:
                cleaned = clean_value(value)
                if cleaned is not None:
                    params[key] = cleaned

    for field in FIELDS:
        value = clean_value(getattr(args, field))
        if value is not None:
            params[field] = value

    return normalize_params(params)


def normalize_params(params: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {"engine": "google_maps"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q"):
        raise ValueError("Missing required q. Parse q from the user request or ask the user what to search on Google Maps.")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))
    normalized.setdefault("google_domain", "google.com")
    normalized.setdefault("start", "0")
    normalized.setdefault("no_cache", "false")

    for field in ("nearby", "no_cache"):
        if field in normalized:
            normalized[field] = normalize_boolean(normalized[field])

    if normalized.get("place_id") and normalized.get("data_cid"):
        raise ValueError("place_id and data_cid cannot be used together.")

    if bool(normalized.get("lat")) != bool(normalized.get("lon")):
        raise ValueError("lat and lon must be supplied together.")

    if normalized.get("z") and normalized.get("m"):
        raise ValueError("Use either z or m, not both.")

    if normalized.get("ll"):
        for field in ("location", "lat", "lon", "z", "m"):
            normalized.pop(field, None)
    else:
        has_origin = bool(normalized.get("location") or (normalized.get("lat") and normalized.get("lon")))
        if has_origin and not (normalized.get("z") or normalized.get("m")):
            raise ValueError("location or lat/lon requires one of z or m.")
        if normalized.get("location"):
            for field in ("lat", "lon"):
                normalized.pop(field, None)

    if normalized.get("nearby") == "true":
        has_nearby_origin = bool(
            normalized.get("ll")
            or normalized.get("location")
            or (normalized.get("lat") and normalized.get("lon"))
        )
        if not has_nearby_origin:
            raise ValueError("nearby=true requires ll, location, or lat/lon as a Maps origin.")

    if "type" in normalized:
        search_type = normalized["type"].strip().lower()
        if search_type in {"search", "place"}:
            normalized["type"] = search_type

    return normalized


def get_authorization(token_arg: str | None) -> str | None:
    token = clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        return None
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def call_api(params: dict[str, str], authorization: str, timeout: float) -> int:
    body = urllib.parse.urlencode(params).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": authorization,
            "Content-Type": "application/x-www-form-urlencoded",
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
        print(f"Request to Dataify API failed: {exc.reason}", file=sys.stderr)
        return 1


def main() -> int:
    args = parse_args()

    try:
        params = merge_params(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.dry_run:
        print(json_module.dumps(params, ensure_ascii=False, sort_keys=True))
        return 0

    authorization = get_authorization(args.token)
    if not authorization:
        print(TOKEN_MISSING_MESSAGE, file=sys.stderr)
        return 2

    return call_api(params, authorization, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
