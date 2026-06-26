#!/usr/bin/env python3
"""Call Dataify Scraper API Google Hotels and print the raw response body."""

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
    "q",
    "json",
    "hl",
    "gl",
    "currency",
    "check_in_date",
    "check_out_date",
    "adults",
    "children",
    "children_ages",
    "sort_by",
    "min_price",
    "max_price",
    "property_types",
    "amenities",
    "rating",
    "brands",
    "hotel_class",
    "free_cancellation",
    "special_offers",
    "eco_certified",
    "vacation_rentals",
    "bedrooms",
    "bathrooms",
    "next_page_token",
    "no_cache",
    "property_token",
)

DEFAULTS = {
    "engine": "google_hotels",
    "json": "1",
    "currency": "USD",
    "adults": "2",
    "children": "0",
    "vacation_rentals": "false",
    "no_cache": "false",
}

BOOLEAN_FIELDS = {
    "free_cancellation",
    "special_offers",
    "eco_certified",
    "vacation_rentals",
    "no_cache",
}

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

SORT_BY_ALIASES = {
    "3": "3",
    "lowestprice": "3",
    "lowest": "3",
    "cheapest": "3",
    "priceasc": "3",
    "最低价格": "3",
    "价格最低": "3",
    "最便宜": "3",
    "8": "8",
    "highestrating": "8",
    "rating": "8",
    "bestrated": "8",
    "最高评分": "8",
    "评分最高": "8",
    "13": "13",
    "mostreviewed": "13",
    "reviews": "13",
    "reviewcount": "13",
    "评论最多": "13",
    "评价最多": "13",
}

RATING_ALIASES = {
    "7": "7",
    "3.5": "7",
    "3.5+": "7",
    "35+": "7",
    "8": "8",
    "4.0": "8",
    "4": "8",
    "4+": "8",
    "4.0+": "8",
    "40+": "8",
    "9": "9",
    "4.5": "9",
    "4.5+": "9",
    "45+": "9",
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
    "新加坡": "sg",
    "singapore": "sg",
    "韩国": "kr",
    "korea": "kr",
    "south korea": "kr",
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

PARAMETER_CATALOG = [
    {
        "name": "Authorization",
        "default": "",
        "description": "请求头中的 Dataify API token；缺失时提示用户提供，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。",
    },
    {"name": "engine", "default": "google_hotels", "description": "固定的 Dataify 引擎值。"},
    {"name": "q", "default": "", "description": "搜索查询或目的地；普通酒店搜索必填。"},
    {"name": "json", "default": "1", "description": "输出格式：1 JSON，2 JSON+HTML，3 HTML，4 Light JSON。"},
    {"name": "hl", "default": "", "description": "Google Hotels 使用的语言代码。"},
    {"name": "gl", "default": "", "description": "Google Hotels 使用的国家或地区代码。"},
    {"name": "currency", "default": "USD", "description": "返回价格使用的货币。"},
    {"name": "check_in_date", "default": "", "description": "入住日期，格式为 YYYY-MM-DD。"},
    {"name": "check_out_date", "default": "", "description": "退房日期，格式为 YYYY-MM-DD。"},
    {"name": "adults", "default": "2", "description": "成人数量。"},
    {"name": "children", "default": "0", "description": "儿童数量。"},
    {"name": "children_ages", "default": "", "description": "儿童年龄，多个年龄用逗号分隔；数量必须与 children 匹配。"},
    {"name": "sort_by", "default": "", "description": "排序方式；留空表示按相关性排序。可用值：3 最低价格，8 最高评分，13 评论最多。"},
    {"name": "min_price", "default": "", "description": "最低价格筛选。"},
    {"name": "max_price", "default": "", "description": "最高价格筛选。"},
    {"name": "property_types", "default": "", "description": "住宿类型 ID，多个值用逗号分隔。"},
    {"name": "amenities", "default": "", "description": "设施 ID，多个值用逗号分隔。"},
    {"name": "rating", "default": "", "description": "评分筛选：7 表示 3.5+，8 表示 4.0+，9 表示 4.5+。"},
    {"name": "brands", "default": "", "description": "酒店品牌筛选，多个值用逗号分隔。"},
    {"name": "hotel_class", "default": "", "description": "酒店星级筛选，多个星级可用逗号分隔。"},
    {"name": "free_cancellation", "default": "", "description": "设为 true 时显示可免费取消的结果；不适用于度假租赁。"},
    {"name": "special_offers", "default": "", "description": "设为 true 时显示有特惠的结果；不适用于度假租赁。"},
    {"name": "eco_certified", "default": "", "description": "设为 true 时显示获得生态认证的结果；不适用于度假租赁。"},
    {"name": "vacation_rentals", "default": "false", "description": "设为 true 时搜索度假租赁；false 时搜索酒店。"},
    {"name": "bedrooms", "default": "", "description": "最小卧室数量；适用于度假租赁。"},
    {"name": "bathrooms", "default": "", "description": "最小浴室数量；适用于度假租赁。"},
    {"name": "next_page_token", "default": "", "description": "用于获取下一页结果的分页 token。"},
    {"name": "no_cache", "default": "false", "description": "设为 true 时跳过缓存。"},
    {"name": "property_token", "default": "", "description": "用于获取酒店或住宿详情的 token。"},
]


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Hotels API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Hotels fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print a Markdown parameter table instead of calling API.")
    parser.add_argument("--dry-run-json", action="store_true", help="Print normalized dry-run metadata as JSON instead of Markdown.")

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


def parse_dates(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    explicit_patterns = {
        "check_in_date": (
            r"(?:check[_ -]?in|入住|到店)\s*[:=]?\s*(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})",
        ),
        "check_out_date": (
            r"(?:check[_ -]?out|退房|离店)\s*[:=]?\s*(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})",
        ),
    }
    for field, patterns in explicit_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                params[field] = normalize_date(match.group(1))
                break

    dates = [normalize_date(date) for date in re.findall(r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b", text)]
    if dates and "check_in_date" not in params:
        params["check_in_date"] = dates[0]
    if len(dates) > 1 and "check_out_date" not in params:
        params["check_out_date"] = dates[1]
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


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return quoted.group(1).strip()

    patterns = (
        r"(?:搜索|查询|找|查找)\s*(.+?)(?:酒店|住宿|旅馆|hotel|hotels)(?:[，。；;,.]|$)",
        r"(?:hotels?\s+(?:in|near)|stay\s+in)\s+(.+?)(?:\s+from\b|\s+for\b|[,;.]|$)",
        r"(?:google\s+hotels?|hotel\s+search)\s+(.+?)(?:\s+from\b|\s+for\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip(" 的在查找搜索")
            if query:
                return query
    return None


def parse_price_range(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    min_patterns = (
        r"(?:min(?:imum)? price|at least|from)\s*[:=]?\s*\$?\s*(\d+(?:\.\d+)?)",
        r"(?:最低价|价格下限|不少于|至少)\s*[:=]?\s*(\d+(?:\.\d+)?)",
    )
    max_patterns = (
        r"(?:max(?:imum)? price|under|below|up to|no more than)\s*[:=]?\s*\$?\s*(\d+(?:\.\d+)?)",
        r"(?:最高价|价格上限|不超过|低于|预算)\s*[:=]?\s*(\d+(?:\.\d+)?)",
    )
    for pattern in min_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["min_price"] = match.group(1)
            break
    for pattern in max_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["max_price"] = match.group(1)
            break
    range_match = re.search(r"(?:\$?\s*)?(\d+(?:\.\d+)?)\s*[-~到至]\s*(?:\$?\s*)?(\d+(?:\.\d+)?)", text)
    if range_match and ("price" in text.lower() or "价" in text):
        params.setdefault("min_price", range_match.group(1))
        params.setdefault("max_price", range_match.group(2))
    return params


def parse_hotel_class(text: str) -> str | None:
    values: list[str] = []
    for match in re.findall(r"([1-5])\s*(?:star|stars|星级|星)", text, flags=re.IGNORECASE):
        if match not in values:
            values.append(match)
    return ",".join(values) if values else None


def parse_children_ages(text: str) -> str | None:
    patterns = (
        r"(?:children[_ -]?ages|child ages|儿童年龄|小孩年龄)\s*[:=]?\s*([0-9,\s]+)",
        r"(?:ages|年龄)\s*[:=]?\s*([0-9,\s]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            values = [part for part in re.split(r"[\s,，]+", match.group(1).strip()) if part]
            if values:
                return ",".join(values)
    return None


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))

    if "q" not in params:
        query = extract_query(text)
        if query:
            params["q"] = query

    for key, value in parse_dates(text).items():
        params.setdefault(key, value)

    for key, value in parse_price_range(text).items():
        params.setdefault(key, value)

    lowered = text.lower()

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

    count_fields = {
        "adults": ("adult", "adults", "成人", "大人"),
        "children": ("child", "children", "kid", "kids", "儿童", "小孩", "孩子"),
        "bedrooms": ("bedroom", "bedrooms", "卧室", "房间"),
        "bathrooms": ("bathroom", "bathrooms", "浴室", "卫生间"),
    }
    for field, labels in count_fields.items():
        if field not in params:
            count = parse_count(text, labels)
            if count is not None:
                params[field] = count

    if "children_ages" not in params:
        ages = parse_children_ages(text)
        if ages:
            params["children_ages"] = ages

    if "sort_by" not in params:
        for marker, value in SORT_BY_ALIASES.items():
            if marker and marker in lowered:
                params["sort_by"] = value
                break

    if "rating" not in params:
        rating_match = re.search(r"([34](?:\.[05])?)\s*\+?\s*(?:rating|评分|分以上|\+)", text, flags=re.IGNORECASE)
        if rating_match:
            params["rating"] = normalize_choice(rating_match.group(1) + "+", RATING_ALIASES)

    if "hotel_class" not in params:
        hotel_class = parse_hotel_class(text)
        if hotel_class:
            params["hotel_class"] = hotel_class

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

    boolean_markers = {
        "free_cancellation": ("free cancellation", "免费取消", "可取消"),
        "special_offers": ("special offer", "special offers", "优惠", "特惠"),
        "eco_certified": ("eco certified", "eco-certified", "生态认证", "环保认证"),
        "vacation_rentals": ("vacation rental", "vacation rentals", "度假租赁", "民宿", "短租"),
        "no_cache": ("no cache", "bypass cache", "跳过缓存", "不走缓存", "不用缓存"),
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

    normalized["engine"] = "google_hotels"
    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))

    if "currency" in normalized:
        normalized["currency"] = normalized["currency"].upper()

    if "gl" in normalized:
        normalized["gl"] = COUNTRY_ALIASES.get(normalized["gl"].lower(), normalized["gl"].lower())

    if "hl" in normalized:
        normalized["hl"] = LANGUAGE_ALIASES.get(normalized["hl"].lower(), normalized["hl"].lower())

    for field in ("check_in_date", "check_out_date"):
        if field in normalized:
            normalized[field] = normalize_date(normalized[field])

    if "sort_by" in normalized:
        normalized["sort_by"] = normalize_choice(normalized["sort_by"], SORT_BY_ALIASES)

    if "rating" in normalized:
        normalized["rating"] = normalize_choice(normalized["rating"], RATING_ALIASES)

    for field in BOOLEAN_FIELDS:
        if field in normalized:
            normalized[field] = normalize_boolean(normalized[field])

    return normalized


def validate_params(params: dict[str, str]) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    errors: list[str] = []

    is_continuation = bool(params.get("property_token") or params.get("next_page_token"))
    if not is_continuation:
        for field in ("q", "check_in_date", "check_out_date"):
            if not params.get(field):
                missing.append(field)

    if params.get("json") not in {"1", "2", "3", "4"}:
        errors.append("json 必须是 1、2、3 或 4")

    if params.get("sort_by") and params["sort_by"] not in {"3", "8", "13"}:
        errors.append("sort_by 必须是 3、8 或 13")

    if params.get("rating") and params["rating"] not in {"7", "8", "9"}:
        errors.append("rating 必须是 7、8 或 9")

    for field in ("check_in_date", "check_out_date"):
        value = params.get(field)
        if value and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            errors.append(f"{field} 必须使用 YYYY-MM-DD 格式")

    try:
        children = int(params.get("children", "0"))
        ages = [age for age in params.get("children_ages", "").split(",") if age.strip()]
        if children > 0 and ages and len(ages) != children:
            errors.append("children_ages 的数量必须与 children 匹配")
    except ValueError:
        errors.append("children 必须是整数")

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


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", " ").replace("\r", " ")
    return text.replace("|", "\\|")


def build_parameter_rows(params: dict[str, str], token_arg: str | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry in PARAMETER_CATALOG:
        name = entry["name"]
        if name == "Authorization":
            current = token_status(token_arg)
        else:
            current = params.get(name, "")
        rows.append(
            {
                "参数名": name,
                "当前值": current,
                "默认值": entry["default"],
                "说明": entry["description"],
            }
        )
    return rows


def build_markdown_table(params: dict[str, str], token_arg: str | None) -> str:
    rows = build_parameter_rows(params, token_arg)
    lines = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {name} | {current} | {default} | {description} |".format(
                name=markdown_escape(row["参数名"]),
                current=markdown_escape(row["当前值"]),
                default=markdown_escape(row["默认值"]),
                description=markdown_escape(row["说明"]),
            )
        )
    return "\n".join(lines)


def build_dry_run(params: dict[str, str], token_arg: str | None) -> dict[str, Any]:
    missing, errors = validate_params(params)
    return {
        "api_url": API_URL,
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded; charset=utf-8",
        "authorization": token_status(token_arg),
        "parameter_table": build_parameter_rows(params, token_arg),
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

    if args.dry_run_json:
        print(json_module.dumps(build_dry_run(params, args.token), ensure_ascii=False, indent=2))
        return 0

    if args.dry_run:
        print(build_markdown_table(params, args.token))
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
