#!/usr/bin/env python3
"""Call Dataify Scraper API Google Search and print the raw response body."""

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
    "start",
    "tbs",
    "safe",
    "nfpr",
    "filter",
    "device",
    "render_js",
    "no_cache",
    "ai_overview",
)

DEFAULTS = {
    "json": "1",
    "google_domain": "google.com",
    "start": "0",
    "nfpr": "0",
    "filter": "1",
    "device": "desktop",
    "no_cache": "false",
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
    "法国": "fr",
    "法國": "fr",
    "france": "fr",
    "fr": "fr",
    "德国": "de",
    "德國": "de",
    "germany": "de",
    "de": "de",
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

BOOLEAN_TRUE = {"1", "true", "yes", "y", "on", "enable", "enabled", "开启", "打开", "启用", "是", "需要"}
BOOLEAN_FALSE = {"0", "false", "no", "n", "off", "disable", "disabled", "关闭", "禁用", "否", "不需要"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Search API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Search fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the normalized payload instead of calling API.")

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
        if label.lower() in lowered:
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


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        value = raw_value.strip().strip("\"'")
        params[field.lower()] = value
    return params


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return quoted.group(1).strip()

    patterns = (
        r"(?:搜索|查找|查询|检索|搜一下)\s*(.+?)(?:[，,。；;]|$)",
        r"(?:search\s+for|google\s+search|google)\s+(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            if query:
                return query
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

    if "device" not in params:
        if any(word in lowered for word in ("mobile", "手机", "移动端", "移動端")):
            params["device"] = "mobile"
        elif any(word in lowered for word in ("tablet", "平板")):
            params["device"] = "tablet"
        elif any(word in lowered for word in ("desktop", "桌面", "电脑", "電腦")):
            params["device"] = "desktop"

    if "safe" not in params:
        if any(word in lowered for word in ("safe off", "关闭安全", "安全搜索关闭", "成人")):
            params["safe"] = "off"
        elif any(word in lowered for word in ("safe on", "开启安全", "安全搜索开启")):
            params["safe"] = "active"

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
            raise ValueError(f"--params-json 不是有效 JSON: {exc}") from exc
        if not isinstance(supplied, dict):
            raise ValueError("--params-json 必须是 JSON object")
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
    normalized: dict[str, str] = {"engine": "google"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q"):
        raise ValueError("缺少搜索关键词 q，请从用户需求中解析 q，或让用户提供要搜索的内容。")

    for field, default_value in DEFAULTS.items():
        normalized.setdefault(field, default_value)

    normalized["json"] = normalize_output_mode(normalized["json"])

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
