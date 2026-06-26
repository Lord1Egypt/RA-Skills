#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Shopping and print the raw response body."""

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

BODY_FIELDS = (
    "q",
    "json",
    "google_domain",
    "gl",
    "hl",
    "location",
    "uule",
    "start",
    "shoprs",
    "min_price",
    "max_price",
    "sort_by",
    "free_shipping",
    "on_sale",
    "small_business",
    "no_cache",
)

BOOLEAN_FIELDS = ("free_shipping", "on_sale", "small_business", "no_cache")

FIELD_DEFINITIONS = (
    ("Authorization", "无", "Header。Dataify API token；可传原始 token 或 Bearer token，预览时只显示是否已提供。"),
    ("engine", "google_shopping", "Body。固定 Google Shopping 引擎值，始终发送 google_shopping。"),
    ("q", "无", "Body。购物搜索关键词；除非 shoprs 已完整表达搜索或过滤状态，否则必填。"),
    ("json", "1", "Body。输出格式：1 为 JSON，2 为 JSON+HTML，3 为 HTML，4 为 Light JSON。"),
    ("google_domain", "google.com", "Body。要使用的 Google 域名。"),
    ("gl", "空", "Body。Google 搜索使用的两位国家或地区代码。"),
    ("hl", "空", "Body。界面或搜索语言代码。"),
    ("location", "空", "Body。搜索发起的地理位置；不要和 uule 同时使用。"),
    ("uule", "空", "Body。Google 编码位置；如果提供该字段，将省略 location。"),
    ("start", "空", "Body。结果偏移量，用于分页。"),
    ("shoprs", "空", "Body。Google Shopping 原始过滤 token；多个过滤器用 || 连接。"),
    ("min_price", "空", "Body。价格范围下限。"),
    ("max_price", "空", "Body。价格范围上限。"),
    ("sort_by", "空", "Body。排序方式：1 为价格从低到高，2 为价格从高到低。"),
    ("free_shipping", "空", "Body。设为 true 时仅显示包邮商品。"),
    ("on_sale", "空", "Body。设为 true 时仅显示促销或折扣商品。"),
    ("small_business", "空", "Body。设为 true 时仅显示来自小企业的商品。"),
    ("no_cache", "false", "Body。设为 true 时跳过缓存；默认使用缓存。"),
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
        description="Call Dataify Google Shopping API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Shopping fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the normalized payload instead of calling API.")
    parser.add_argument("--table", action="store_true", help="Print the full Markdown parameter table instead of calling API.")

    for field in BODY_FIELDS:
        parser.add_argument(f"--{field}", dest=field)
        if "_" in field:
            parser.add_argument(f"--{field.replace('_', '-')}", dest=field)

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
        if label.lower() in lowered:
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
            return str((page - 1) * 10)

    match = re.search(r"\bstart\s*[:=]\s*(\d+)\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    aliases: dict[str, str] = {field: field for field in BODY_FIELDS}
    aliases.update({field.replace("_", "-"): field for field in BODY_FIELDS if "_" in field})
    aliases["engine"] = "engine"

    field_pattern = "|".join(re.escape(field) for field in sorted(aliases, key=len, reverse=True))
    pattern = rf"(?<!\w)({field_pattern})(?!\w)\s*[:=：]\s*(\"[^\"]*\"|'[^']*'|[^,;，；\n]+)"
    for raw_field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        field = aliases[raw_field.lower()]
        value = raw_value.strip().strip("\"'")
        params[field] = value
    return params


def cleanup_query(query: str) -> str:
    cleaned = query.strip()
    cleaned = re.sub(r"\bgoogle\s+shopping\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bgoogle\s+shopping\s+(?:上|里|中|in|on)\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:in|on)\s+(?:the\s+)?(?:united states|usa|us|china|japan|united kingdom|uk|france|germany|canada|australia)\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?:美国|美國|中国|中國|日本|英国|英國|法国|法國|德国|德國|加拿大|澳大利亚|澳洲)\s*(?:google\s*shopping)?\s*(?:上|里|中)?", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[$￥¥]?\s*[0-9]+(?:\.[0-9]+)?\s*(?:美元|元|usd|dollars)?\s*(?:以内|以下|以上|起|封顶)?", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?:under|below|less than|no more than|max|over|above|more than|at least|min)\s*[$￥¥]?\s*[0-9]+(?:\.[0-9]+)?", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?:包邮|免运费|免邮|free shipping|促销|折扣|特价|优惠|on sale|discount|deal)", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?:英文|英语|中文|简体中文|繁体中文|日文|日语|法文|法语|德文|德语|西班牙语|english|chinese|japanese|french|german|spanish)", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:return|返回)\s*(?:json\+html|html\+json|light json|lite json|json|html)\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip()
    cleaned = re.sub(r"^(?:的|之|for|of)\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip(" ，,。；;")


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        query = cleanup_query(quoted.group(1))
        return query or quoted.group(1).strip()

    patterns = (
        r"(?:搜索|查找|查询|搜|找|买|购买)\s*(?:google\s*shopping\s*)?(?:商品|产品|物品)?\s*[:：]?\s*(.+?)(?:[，,。；;]|$)",
        r"(?:search\s+for|shop\s+for|buy|google\s+shopping)\s+(.+?)(?:\s+with\b|\s+under\b|\s+over\b|\s+below\b|\s+above\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = cleanup_query(match.group(1))
            if query:
                return query
    return None


def parse_price_filters(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    number = r"([0-9]+(?:\.[0-9]+)?)"

    range_patterns = (
        rf"(?:between|from)\s*[$￥¥]?\s*{number}\s*(?:and|to|-)\s*[$￥¥]?\s*{number}",
        rf"[$￥¥]?\s*{number}\s*(?:到|至|-)\s*[$￥¥]?\s*{number}\s*(?:美元|元|usd|dollars)?",
    )
    for pattern in range_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["min_price"] = match.group(1)
            params["max_price"] = match.group(2)
            return params

    upper_patterns = (
        rf"(?:under|below|less than|no more than|max|低于|小于|不超过|以内|以下)\s*[$￥¥]?\s*{number}",
        rf"[$￥¥]?\s*{number}\s*(?:美元|元|usd|dollars)?\s*(?:以内|以下|封顶)",
    )
    for pattern in upper_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["max_price"] = match.group(1)
            break

    lower_patterns = (
        rf"(?:over|above|more than|at least|min|高于|大于|超过|至少)\s*[$￥¥]?\s*{number}",
        rf"[$￥¥]?\s*{number}\s*(?:美元|元|usd|dollars)?\s*(?:以上|起)",
    )
    for pattern in lower_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["min_price"] = match.group(1)
            break

    return params


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))

    if "q" not in params:
        query = extract_query(text)
        if query:
            params["q"] = query

    lowered = text.lower()

    if "google_domain" not in params:
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

    for field, value in parse_price_filters(text).items():
        params.setdefault(field, value)

    if "sort_by" not in params:
        if any(marker in lowered for marker in ("low to high", "lowest price", "price ascending", "价格从低到高", "低到高", "由低到高")):
            params["sort_by"] = "1"
        elif any(marker in lowered for marker in ("high to low", "highest price", "price descending", "价格从高到低", "高到低", "由高到低")):
            params["sort_by"] = "2"

    if "free_shipping" not in params and any(marker in lowered for marker in ("free shipping", "包邮", "免运费", "免邮")):
        params["free_shipping"] = "true"
    if "on_sale" not in params and any(marker in lowered for marker in ("on sale", "sale", "discount", "deal", "促销", "折扣", "特价", "优惠")):
        params["on_sale"] = "true"
    if "small_business" not in params and any(marker in lowered for marker in ("small business", "小企业", "小型企业", "小商家")):
        params["small_business"] = "true"
    if "no_cache" not in params and any(marker in lowered for marker in ("no cache", "bypass cache", "不走缓存", "跳过缓存", "绕过缓存")):
        params["no_cache"] = "true"

    output_checks = (
        ("json+html", "2"),
        ("html+json", "2"),
        ("light json", "4"),
        ("lite json", "4"),
        ("轻量 json", "4"),
        ("轻量json", "4"),
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
            canonical_key = key.replace("-", "_")
            if canonical_key in BODY_FIELDS or canonical_key == "engine":
                cleaned = clean_value(value)
                if cleaned is not None:
                    params[canonical_key] = cleaned

    for field in BODY_FIELDS:
        value = clean_value(getattr(args, field))
        if value is not None:
            params[field] = value

    return normalize_params(params)


def normalize_params(params: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {"engine": "google_shopping"}

    for field in BODY_FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q") and not normalized.get("shoprs"):
        raise ValueError("缺少购物搜索关键词 q，请从用户需求中解析 q，或让用户提供要搜索的商品。")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))
    normalized["google_domain"] = normalized.get("google_domain", "google.com")

    for field in BOOLEAN_FIELDS:
        if field in normalized:
            normalized[field] = normalize_boolean(normalized[field])

    if "sort_by" in normalized:
        sort_by = normalized["sort_by"].strip().lower()
        if sort_by in {"low_to_high", "low-to-high", "asc", "ascending", "price_asc", "价格从低到高", "低到高"}:
            normalized["sort_by"] = "1"
        elif sort_by in {"high_to_low", "high-to-low", "desc", "descending", "price_desc", "价格从高到低", "高到低"}:
            normalized["sort_by"] = "2"

    if normalized.get("uule") and normalized.get("location"):
        normalized.pop("location", None)

    return normalized


def get_authorization(token_arg: str | None) -> str | None:
    token = clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        return None
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def escape_table_cell(value: Any) -> str:
    text = str(value)
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    text = text.replace("\r", " ").replace("\n", " ")
    return text


def current_value_for_table(name: str, params: dict[str, str], authorization: str | None) -> str:
    if name == "Authorization":
        return "已提供" if authorization else "未提供"
    value = params.get(name)
    if value is None or value == "":
        return "（未设置）"
    return value


def print_parameter_table(params: dict[str, str], authorization: str | None) -> None:
    print("| 参数名 | 当前值 | 默认值 | 说明 |")
    print("|---|---|---|---|")
    for name, default, description in FIELD_DEFINITIONS:
        current = current_value_for_table(name, params, authorization)
        print(
            "| "
            + escape_table_cell(name)
            + " | "
            + escape_table_cell(current)
            + " | "
            + escape_table_cell(default)
            + " | "
            + escape_table_cell(description)
            + " |"
        )


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
        print(f"请求 Dataify API 失败: {exc.reason}", file=sys.stderr)
        return 1


def main() -> int:
    args = parse_args()

    try:
        params = merge_params(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    authorization = get_authorization(args.token)

    if args.table:
        print_parameter_table(params, authorization)
        return 0

    if args.dry_run:
        print(json_module.dumps(params, ensure_ascii=False, sort_keys=True))
        return 0

    if not authorization:
        print("缺少 Dataify API token，请提供 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。", file=sys.stderr)
        return 2

    return call_api(params, authorization, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
