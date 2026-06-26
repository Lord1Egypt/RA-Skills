#!/usr/bin/env python3
"""Call Dataify Scraper API Google Images and print the raw response body."""

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
    "google_domain",
    "gl",
    "hl",
    "cr",
    "lr",
    "location",
    "uule",
    "lat",
    "lon",
    "radius",
    "start",
    "tbm",
    "ludocid",
    "lsig",
    "kgmid",
    "si",
    "ibp",
    "uds",
    "tbs",
    "safe",
    "nfpr",
    "filter",
    "device",
    "render_js",
    "no_cache",
    "ai_overview",
)

REQUEST_FIELDS = ("engine",) + FIELDS

FIELD_METADATA = {
    "engine": ("google_images", "固定值：Google Images 引擎。"),
    "q": ("", "定义搜索的查询内容；必填。"),
    "json": ("1", "定义采集结果的输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。"),
    "google_domain": ("google.com", "定义要使用的 Google 域名。"),
    "gl": ("", "定义 Google 搜索使用的国家/地区，两位国家/地区代码。"),
    "hl": ("", "定义 Google 搜索使用的语言代码。"),
    "cr": ("", "限制搜索结果所在国家/地区，格式如 countryFR，可用 | 分隔多个值。"),
    "lr": ("", "限制搜索结果语言，格式如 lang_fr，可用 | 分隔多个值。"),
    "location": ("", "定义搜索发起的地理位置；不能与 uule、lat、lon 一起使用。"),
    "uule": ("", "Google 编码位置；不能与 location、lat、lon、radius 一起使用。"),
    "lat": ("", "搜索起点的 GPS 纬度；使用 lon 时必须同时提供。"),
    "lon": ("", "搜索起点的 GPS 经度；使用 lat 时必须同时提供。"),
    "radius": ("", "搜索结果偏向范围，单位为米；桌面端 1-199，平板/移动端 1-1000。"),
    "start": ("0", "结果偏移量，用于分页；0 为第一页，10 为第二页，20 为第三页。"),
    "tbm": ("", "搜索类型；Google Images 可使用 isch，但未指定时不作为默认值传入。"),
    "ludocid": ("", "地点的 Google CID。"),
    "lsig": ("", "用于强制显示知识图谱地图视图等场景的签名参数。"),
    "kgmid": ("", "Google Knowledge Graph MID。"),
    "si": ("", "Google 搜索缓存搜索参数。"),
    "ibp": ("", "负责渲染某些元素布局和扩展的参数。"),
    "uds": ("", "Google 搜索过滤参数。"),
    "tbs": ("", "高级搜索参数，可表达图片尺寸、颜色、类型、日期等过滤。"),
    "safe": ("", "成人内容过滤级别；可设为 active 或 off。"),
    "nfpr": ("0", "是否排除自动更正查询的结果；0 包含，1 排除。"),
    "filter": ("1", "类似结果和省略结果过滤器；1 禁用，0 启用。"),
    "device": ("desktop", "获取结果的设备类型：desktop、tablet 或 mobile。"),
    "render_js": ("", "是否使用浏览器执行页面脚本并返回渲染后的 HTML，true 或 false。"),
    "no_cache": ("false", "是否跳过缓存；true 跳过缓存，false 使用缓存结果。"),
    "ai_overview": ("", "是否获取 Google 搜索结果中的 AI Overview 内容，true 或 false。"),
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
    "ca": "ca",
    "澳大利亚": "au",
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
        description="Call Dataify Google Images API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Images fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized form payload instead of calling API.",
    )
    parser.add_argument(
        "--params-table",
        action="store_true",
        help="Print a Markdown parameter table and do not call API.",
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
        r"page\s*(\d+)",
        r"第\s*(\d+)\s*頁",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            page = max(int(match.group(1)), 1)
            return str((page - 1) * 10)

    match = re.search(r"\bstart\s*[:=]\s*(\d+)\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def parse_radius(text: str) -> str | None:
    match = re.search(r"(?:radius|半径|范围)\s*[:=]?\s*(\d+)", text, flags=re.IGNORECASE)
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


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        params[field.lower()] = raw_value.strip().strip("\"'")
    return params


def clean_query_text(query: str) -> str:
    query = query.strip()
    query = re.sub(r"\s*(?:图片|圖像|图像|images?|google\s+images?)\s*$", "", query, flags=re.IGNORECASE)
    return query.strip()


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return clean_query_text(quoted.group(1))

    patterns = (
        r"(?:搜索|查找|查询|检索|抓取|采集|找|搜)\s*(?:google\s*)?(?:图片|图像|images?)?\s*(.+?)(?:[，。；;]|$)",
        r"(?:google\s+images|image\s+search|search\s+images?\s+for|search\s+for)\s+(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query_text(match.group(1))
            if query:
                return query
    return None


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))
    params.update({k: v for k, v in parse_coordinates(text).items() if k not in params})

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

    if "radius" not in params:
        radius = parse_radius(text)
        if radius:
            params["radius"] = radius

    if "device" not in params:
        if any(word in lowered for word in ("mobile", "手机", "移动端", "移动")):
            params["device"] = "mobile"
        elif any(word in lowered for word in ("tablet", "平板")):
            params["device"] = "tablet"
        elif any(word in lowered for word in ("desktop", "桌面", "电脑")):
            params["device"] = "desktop"

    if "safe" not in params:
        if any(word in lowered for word in ("safe off", "关闭安全", "安全搜索关闭", "成人")):
            params["safe"] = "off"
        elif any(word in lowered for word in ("safe on", "开启安全", "安全搜索开启")):
            params["safe"] = "active"

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

    boolean_markers = {
        "render_js": ("render_js", "渲染js", "渲染 javascript", "render javascript"),
        "no_cache": ("no_cache", "不走缓存", "跳过缓存", "绕过缓存", "bypass cache", "no cache"),
        "ai_overview": ("ai_overview", "ai overview", "ai 概览", "ai概览"),
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
    normalized: dict[str, str] = {"engine": "google_images"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q"):
        raise ValueError("Missing required query q. Parse q from the user request or ask the user what images to search.")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))

    normalized.setdefault("google_domain", "google.com")
    normalized.setdefault("start", "0")
    normalized.setdefault("nfpr", "0")
    normalized.setdefault("filter", "1")
    normalized.setdefault("device", "desktop")
    normalized.setdefault("no_cache", "false")

    if "safe" in normalized:
        safe = normalized["safe"].strip().lower()
        normalized["safe"] = "active" if safe in {"active", "on", "true", "1", "开启", "打开"} else "off"

    if "device" in normalized:
        device = normalized["device"].strip().lower()
        if device in {"desktop", "tablet", "mobile"}:
            normalized["device"] = device

    for field in ("render_js", "no_cache", "ai_overview"):
        if field in normalized:
            normalized[field] = normalize_boolean(normalized[field])

    for field in ("nfpr", "filter"):
        if field in normalized:
            value = normalized[field].strip().lower()
            if value in BOOLEAN_TRUE:
                normalized[field] = "1"
            elif value in BOOLEAN_FALSE:
                normalized[field] = "0"

    if bool(normalized.get("lat")) != bool(normalized.get("lon")):
        raise ValueError("lat and lon must be supplied together.")

    if normalized.get("uule"):
        for field in ("location", "lat", "lon", "radius"):
            normalized.pop(field, None)
    elif normalized.get("location"):
        for field in ("lat", "lon"):
            normalized.pop(field, None)

    if normalized.get("radius") and not (normalized.get("lat") and normalized.get("lon")):
        normalized.pop("radius", None)

    return normalized


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def print_params_table(params: dict[str, str]) -> None:
    print("| 参数名 | 当前值 | 默认值 | 说明 |")
    print("| --- | --- | --- | --- |")
    for field in REQUEST_FIELDS:
        default, description = FIELD_METADATA[field]
        current = params.get(field, "")
        print(
            "| "
            + " | ".join(
                (
                    markdown_escape(field),
                    markdown_escape(current),
                    markdown_escape(default),
                    markdown_escape(description),
                )
            )
            + " |"
        )


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

    if args.params_table:
        print_params_table(params)
        return 0

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
