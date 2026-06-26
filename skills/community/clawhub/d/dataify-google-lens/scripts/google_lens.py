#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Lens and print the raw response body."""

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
    "url",
    "json",
    "hl",
    "country",
    "type",
    "q",
    "safe",
    "no_cache",
)

FIELD_INFO = {
    "engine": {
        "default": "google_lens",
        "description": "固定值，表示调用 Google Lens。",
    },
    "url": {
        "default": "无",
        "description": "要执行 Google Lens 搜索的图片 URL。",
    },
    "json": {
        "default": "1",
        "description": "输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。",
    },
    "hl": {
        "default": "无",
        "description": "Google Lens 使用的语言代码，例如 en、zh-cn、ja；示例不是默认值。",
    },
    "country": {
        "default": "无",
        "description": "Google Lens 使用的两位国家或地区代码，例如 us、fr、de；示例不是默认值。",
    },
    "type": {
        "default": "all",
        "description": "搜索类型：all、products、about_this_image、exact_matches、visual_matches。",
    },
    "q": {
        "default": "无",
        "description": "附加搜索查询，仅适用于 all、visual_matches 或 products。",
    },
    "safe": {
        "default": "无",
        "description": "成人内容过滤级别：active 或 off。",
    },
    "no_cache": {
        "default": "false",
        "description": "是否绕过缓存：true 或 false。",
    },
}

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
    "gb": "gb",
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
    "澳大利亞": "au",
    "australia": "au",
    "au": "au",
    "韩国": "kr",
    "韓國": "kr",
    "south korea": "kr",
    "korea": "kr",
    "kr": "kr",
    "新加坡": "sg",
    "singapore": "sg",
    "sg": "sg",
    "香港": "hk",
    "hong kong": "hk",
    "hk": "hk",
    "台湾": "tw",
    "台灣": "tw",
    "taiwan": "tw",
    "tw": "tw",
}

LANGUAGE_ALIASES = {
    "中文": "zh-cn",
    "简体中文": "zh-cn",
    "簡體中文": "zh-cn",
    "繁体中文": "zh-tw",
    "繁體中文": "zh-tw",
    "英语": "en",
    "英文": "en",
    "english": "en",
    "en": "en",
    "日语": "ja",
    "日文": "ja",
    "japanese": "ja",
    "ja": "ja",
    "韩语": "ko",
    "韓語": "ko",
    "korean": "ko",
    "ko": "ko",
    "法语": "fr",
    "法文": "fr",
    "french": "fr",
    "fr": "fr",
    "德语": "de",
    "德文": "de",
    "german": "de",
    "de": "de",
    "西班牙语": "es",
    "spanish": "es",
    "es": "es",
}

TYPE_ALIASES = {
    "all": "all",
    "全部": "all",
    "所有": "all",
    "products": "products",
    "product": "products",
    "商品": "products",
    "产品": "products",
    "產品": "products",
    "about_this_image": "about_this_image",
    "about this image": "about_this_image",
    "关于此图片": "about_this_image",
    "關於此圖片": "about_this_image",
    "图片信息": "about_this_image",
    "exact_matches": "exact_matches",
    "exact matches": "exact_matches",
    "exact match": "exact_matches",
    "完全匹配": "exact_matches",
    "精确匹配": "exact_matches",
    "精準匹配": "exact_matches",
    "visual_matches": "visual_matches",
    "visual matches": "visual_matches",
    "visual match": "visual_matches",
    "similar images": "visual_matches",
    "similar image": "visual_matches",
    "相似图片": "visual_matches",
    "相似圖片": "visual_matches",
    "视觉匹配": "visual_matches",
    "視覺匹配": "visual_matches",
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
    "開啟",
    "打开",
    "啟用",
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
    "關閉",
    "禁用",
    "否",
    "不需要",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Lens API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Lens fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the full Markdown parameter table instead of calling API.",
    )
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


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        params[field.lower()] = raw_value.strip().strip("\"'")
    return params


def extract_url(text: str) -> str | None:
    match = re.search(r"https?://[^\s'\"<>，；,]+", text)
    if match:
        return match.group(0).rstrip(").]")
    return None


def extract_query(text: str) -> str | None:
    patterns = (
        r"\bq\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)",
        r"(?:关键词|關鍵詞|查询|查詢|query|keyword)\s*[:=：]?\s*(\"[^\"]*\"|'[^']*'|[^,;，；]+)",
        r"(?:with|for|关于|關於|包含)\s+[\"']([^\"']+)[\"']",
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

    if "url" not in params:
        image_url = extract_url(text)
        if image_url:
            params["url"] = image_url

    if "q" not in params:
        query = extract_query(text)
        if query:
            params["q"] = query

    lowered = text.lower()

    if "country" not in params:
        country = find_alias(text, COUNTRY_ALIASES)
        if country:
            params["country"] = country

    if "hl" not in params:
        language = find_alias(text, LANGUAGE_ALIASES)
        if language:
            params["hl"] = language

    if "type" not in params:
        lens_type = find_alias(text, TYPE_ALIASES)
        if lens_type:
            params["type"] = lens_type

    if "safe" not in params:
        if any(marker in lowered for marker in ("safe off", "关闭安全", "關閉安全", "安全搜索关闭", "成人内容不过滤")):
            params["safe"] = "off"
        elif any(marker in lowered for marker in ("safe on", "开启安全", "開啟安全", "安全搜索开启", "过滤成人")):
            params["safe"] = "active"

    if "json" not in params:
        output_checks = (
            ("json+html", "2"),
            ("html+json", "2"),
            ("light json", "4"),
            ("lite json", "4"),
            ("html", "3"),
            ("json", "1"),
            ("轻量 json", "4"),
            ("輕量 json", "4"),
        )
        for marker, mode in output_checks:
            if marker in lowered:
                params["json"] = mode
                break

    if "no_cache" not in params:
        no_cache_true = ("no_cache", "no cache", "bypass cache", "skip cache", "不使用缓存", "不用缓存", "跳过缓存", "繞過快取")
        no_cache_false = ("use cache", "使用缓存", "使用快取")
        if any(marker in lowered for marker in no_cache_true):
            params["no_cache"] = "true"
        elif any(marker in lowered for marker in no_cache_false):
            params["no_cache"] = "false"

    return params


def merge_params(args: argparse.Namespace, validate_required: bool) -> dict[str, str]:
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

    return normalize_params(params, validate_required=validate_required)


def normalize_params(params: dict[str, Any], validate_required: bool) -> dict[str, str]:
    normalized: dict[str, str] = {"engine": "google_lens"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))
    normalized["type"] = normalize_lens_type(normalized.get("type", "all"))
    normalized["no_cache"] = normalize_boolean(normalized.get("no_cache", "false"))

    if "safe" in normalized:
        safe = normalized["safe"].strip().lower()
        if safe in {"active", "on", "true", "1", "开启", "開啟", "打开", "啟用", "启用"}:
            normalized["safe"] = "active"
        elif safe in {"off", "false", "0", "关闭", "關閉", "禁用"}:
            normalized["safe"] = "off"

    for field in ("hl", "country"):
        if field in normalized:
            normalized[field] = normalized[field].strip().lower()

    if validate_required and not normalized.get("url"):
        raise ValueError("Missing required image url. Parse url from the user request or ask the user for the image URL.")

    return normalized


def normalize_lens_type(value: Any) -> str:
    text = str(value).strip()
    alias = find_alias(text, TYPE_ALIASES)
    return alias or text


def get_authorization(token_arg: str | None) -> str | None:
    token = clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        return None
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def escape_table_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", " ").replace("\r", " ").replace("|", "\\|")
    return text if text else "未设置"


def preview_table(params: dict[str, str]) -> str:
    rows = [
        ("engine", params.get("engine")),
        ("url", params.get("url")),
        ("json", params.get("json")),
        ("hl", params.get("hl")),
        ("country", params.get("country")),
        ("type", params.get("type")),
        ("q", params.get("q")),
        ("safe", params.get("safe")),
        ("no_cache", params.get("no_cache")),
    ]

    lines = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for name, current in rows:
        info = FIELD_INFO[name]
        lines.append(
            f"| `{name}` | {escape_table_cell(current)} | {escape_table_cell(info['default'])} | {escape_table_cell(info['description'])} |"
        )
    return "\n".join(lines)


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
        params = merge_params(args, validate_required=not args.preview)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.preview:
        print(preview_table(params))
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
