#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Local and print the raw response body."""

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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

FIELDS = (
    "q",
    "json",
    "google_domain",
    "gl",
    "hl",
    "location",
    "uule",
    "start",
    "ludocid",
    "tbs",
    "no_cache",
)

PARAMETER_INFO = (
    ("Authorization", "header", "string", "yes", None, "Dataify API token. If it lacks the Bearer prefix, the script adds it."),
    ("engine", "body", "string", "yes", "google_local", "Fixed engine value for Google Local."),
    ("q", "body", "string", "yes", None, "Search query content."),
    ("json", "body", "string", "yes", "1", "Output format: 1=JSON, 2=JSON+HTML, 3=HTML, 4=Light JSON."),
    ("google_domain", "body", "string", "no", "google.com", "Google domain to use."),
    ("gl", "body", "string", "no", None, "Two-letter Google country/region code."),
    ("hl", "body", "string", "no", None, "Google language code."),
    ("location", "body", "string", "no", None, "Geographic location where the search originates."),
    ("uule", "body", "string", "no", None, "Google encoded location. Do not use together with location."),
    ("start", "body", "string", "no", None, "Result offset for pagination."),
    ("ludocid", "body", "string", "no", None, "Google place CID/customer identifier."),
    ("tbs", "body", "string", "no", None, "Advanced search parameter not represented by q."),
    ("no_cache", "body", "string", "no", "false", "true bypasses cache; false uses cached results when available."),
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
    "印度": "in",
    "india": "in",
    "in": "in",
    "巴西": "br",
    "brazil": "br",
    "br": "br",
    "墨西哥": "mx",
    "mexico": "mx",
    "mx": "mx",
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
    "葡萄牙语": "pt",
    "portuguese": "pt",
    "pt": "pt",
    "韩文": "ko",
    "韩语": "ko",
    "korean": "ko",
    "ko": "ko",
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
        description="Call Dataify Google Local API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Local fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized form payload instead of calling API.",
    )
    parser.add_argument(
        "--describe-params",
        action="store_true",
        help="Print documented parameters, descriptions, and real defaults.",
    )
    parser.add_argument(
        "--preview-params",
        action="store_true",
        help="Print every documented parameter with current value, default, source, and description.",
    )
    parser.add_argument(
        "--preview-format",
        choices=("json", "markdown"),
        default="json",
        help="Format for --preview-params output.",
    )

    for field in FIELDS:
        parser.add_argument(f"--{field}", dest=field)

    return parser.parse_args()


def print_parameter_description() -> None:
    rows = [
        {
            "field": field,
            "location": location,
            "type": value_type,
            "required": required,
            "default": default,
            "description": description,
        }
        for field, location, value_type, required, default, description in PARAMETER_INFO
    ]
    print(json_module.dumps(rows, ensure_ascii=False, indent=2))


def build_parameter_preview(params: dict[str, str], token_arg: str | None) -> list[dict[str, str | None]]:
    token_available = bool(clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN")))
    rows = []
    for field, location, value_type, required, default, description in PARAMETER_INFO:
        if field == "Authorization":
            value = "(provided)" if token_available else None
            source = "user/env" if token_available else "unset"
        elif field == "engine":
            value = params.get("engine")
            source = "fixed"
        else:
            value = params.get(field)
            if value is None:
                source = "unset"
            elif default is not None and value == default:
                source = "default"
            else:
                source = "user/parsed"

        rows.append(
            {
                "field": field,
                "location": location,
                "type": value_type,
                "required": required,
                "value": value,
                "source": source,
                "default": default,
                "description": description,
            }
        )
    return rows


def markdown_cell(value: Any) -> str:
    if value is None:
        return "未赋值"
    text = str(value)
    text = text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")
    return text


def print_parameter_preview(params: dict[str, str], token_arg: str | None, output_format: str) -> None:
    rows = build_parameter_preview(params, token_arg)
    if output_format == "markdown":
        print("| 参数 | 位置 | 类型 | 必填 | 当前值 | 来源 | 默认值 | 说明 |")
        print("|---|---|---|---:|---|---|---|---|")
        for row in rows:
            print(
                "| "
                + " | ".join(
                    markdown_cell(row[key])
                    for key in ("field", "location", "type", "required", "value", "source", "default", "description")
                )
                + " |"
            )
        return

    print(json_module.dumps(rows, ensure_ascii=False, indent=2))


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
        params[field.lower()] = raw_value.strip().strip("\"'")

    shorthand_pattern = rf"\b({field_pattern})\b\s+(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(shorthand_pattern, text, flags=re.IGNORECASE):
        key = field.lower()
        if key not in params:
            params[key] = raw_value.strip().strip("\"'")
    return params


def parse_loose_params_object(text: str) -> dict[str, str]:
    stripped = text.strip()
    if not (stripped.startswith("{") and stripped.endswith("}")):
        raise ValueError("--params-json 必须是 JSON object")

    inner = stripped[1:-1].strip()
    if not inner:
        return {}

    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"(?:^|,)\s*\"?({field_pattern})\"?\s*:\s*(.*?)(?=,\s*\"?(?:{field_pattern})\"?\s*:|$)"
    for field, raw_value in re.findall(pattern, inner, flags=re.IGNORECASE):
        value = raw_value.strip().strip("\"'")
        if value:
            params[field.lower()] = value

    if not params:
        raise ValueError("--params-json 必须是 JSON object")
    return params


def parse_params_json_arg(text: str) -> dict[str, Any]:
    try:
        supplied = json_module.loads(text)
    except json_module.JSONDecodeError:
        supplied = parse_loose_params_object(text)

    if not isinstance(supplied, dict):
        raise ValueError("--params-json 必须是 JSON object")
    return supplied


def parse_ludocid(text: str) -> str | None:
    patterns = (
        r"\bludocid\s*[:=]\s*([^\s,;，；]+)",
        r"\b(?:google\s*)?(?:cid|客户标识符|客戶標識符)\s*[:=]\s*([^\s,;，；]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().strip("\"'")
    return None


def parse_explicit_location(text: str) -> str | None:
    patterns = (
        r"\blocation\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^,;，；]+)",
        r"\bin\s+(.+?)\s+(?:with|using)\b",
        r"(?:搜索位置|搜索地点|搜索地點|位置|地点|地點|地区|地區)\s*[:=：]\s*(.+?)(?:[，,。；;]|$)",
        r"(?:在|位于|位於)\s*(.+?)\s*(?:搜索|查找|查询|搜尋|搜|找)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip().strip("\"'")
            if value:
                return value
    return None


def clean_query_text(query: str) -> str:
    query = query.strip()
    query = re.sub(r"\s*(?:google\s*)?(?:local|本地|本地搜索|local\s*search)\s*$", "", query, flags=re.IGNORECASE)
    query = re.sub(r"\s*(?:返回|输出|輸出)\s*(?:json\+html|html\+json|light\s*json|json|html)\s*$", "", query, flags=re.IGNORECASE)
    return query.strip()


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        query = clean_query_text(quoted.group(1))
        if query:
            return query

    patterns = (
        r"(?:搜索|查找|查询|检索|抓取|采集|搜一下|搜|找)\s*(?:google\s*)?(?:local|本地|本地搜索)?\s*(.+?)(?:[，。；;]|$)",
        r"(?:search\s+for|find)\s+(.+?)\s+in\s+.+?(?:\s+with\b|\s+using\b|[,;.]|$)",
        r"(?:search\s+for|find)\s+(.+?)(?:\s+with\b|\s+using\b|[,;.]|$)",
        r"(?:google\s+local|local\s+search)\s+(?:search\s+for|search|find)\s+(.+?)(?:\s+with\b|\s+using\b|[,;.]|$)",
        r"(?:search\s+for|find)\s+(.+?)\s+(?:on|in)\s+(?:google\s+local|local\s+search)(?:[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query_text(match.group(1))
            if query:
                return query

    if not re.search(
        r"\b(?:token|authorization|engine|json|google_domain|gl|hl|location|uule|start|ludocid|cid|tbs|no_cache)\b",
        text,
        flags=re.IGNORECASE,
    ):
        query = clean_query_text(text)
        if query:
            return query

    return None


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))

    if "ludocid" not in params:
        ludocid = parse_ludocid(text)
        if ludocid:
            params["ludocid"] = ludocid

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

    if "no_cache" not in params:
        if any(marker in lowered for marker in ("不走缓存", "跳过缓存", "绕过缓存", "bypass cache", "no cache", "no_cache")):
            params["no_cache"] = "true"
        elif any(marker in lowered for marker in ("使用缓存", "走缓存", "use cache")):
            params["no_cache"] = "false"

    return params


def merge_params(args: argparse.Namespace) -> dict[str, str]:
    params: dict[str, str] = {}

    if args.request:
        params.update(parse_natural_request(args.request))

    if args.params_json:
        supplied = parse_params_json_arg(args.params_json)
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
    normalized: dict[str, str] = {"engine": "google_local"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q"):
        raise ValueError("缺少搜索关键词 q，请从用户需求中解析 q，或让用户提供要搜索的内容。")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))
    normalized.setdefault("google_domain", "google.com")
    normalized.setdefault("no_cache", "false")

    if "no_cache" in normalized:
        normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

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

    if args.describe_params:
        print_parameter_description()
        return 0

    try:
        params = merge_params(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.preview_params:
        print_parameter_preview(params, args.token, args.preview_format)
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
