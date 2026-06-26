#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Videos and print the raw response body."""

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
    "location",
    "uule",
    "start",
    "tbs",
    "no_cache",
    "lr",
    "safe",
    "nfpr",
    "filter",
)

PARAMETER_SPECS = (
    ("Authorization", None, "Dataify API token in the Authorization header. Use --token or DATAIFY_API_TOKEN; Bearer prefix is optional."),
    ("engine", "google_videos", "Fixed body value for Google Videos."),
    ("q", None, "Required search query content."),
    ("json", "1", "Output format: 1 JSON, 2 JSON+HTML, 3 HTML, 4 Light JSON."),
    ("google_domain", "google.com", "Google domain to use."),
    ("gl", None, "Two-letter country or region code for Google search behavior."),
    ("hl", None, "Language code for Google search UI/results."),
    ("location", None, "Named geographic location to originate the search from."),
    ("uule", None, "Google encoded location. Do not use together with location."),
    ("start", None, "Result offset for pagination."),
    ("tbs", None, "Advanced Google search parameters for filters such as date, duration, quality, or source."),
    ("no_cache", "false", "Set true to bypass cached results; false allows cache use."),
    ("lr", None, "Restrict results to one or more languages, such as lang_fr or lang_fr|lang_de."),
    ("safe", None, "Safe search level. Use active to enable or off to disable when requested."),
    ("nfpr", "0", "Whether to exclude results from autocorrected queries. 1 excludes them, 0 includes them."),
    ("filter", "0", "Similar and omitted results filter. 0 enables filters, 1 disables them."),
)

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Videos API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Videos fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--preview-table",
        action="store_true",
        help="Print the complete Markdown parameter table instead of calling API.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized form payload as JSON instead of calling API.",
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


def find_alias_near_markers(text: str, aliases: dict[str, str], markers: tuple[str, ...]) -> str | None:
    lowered = text.lower()
    for marker in markers:
        marker_lower = marker.lower()
        position = lowered.find(marker_lower)
        if position == -1:
            continue
        window = text[position : position + 100]
        found = find_alias(window, aliases)
        if found:
            return found
    return None


def parse_page_start(text: str) -> str | None:
    patterns = (
        r"第\s*(\d+)\s*页",
        r"page\s*(\d+)",
        r"\b页码\s*[:=]?\s*(\d+)",
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
    return params


def clean_query_text(query: str) -> str:
    query = query.strip(" ：:，,。.;；")
    query = re.sub(r"^(?:for|about)\s+", "", query, flags=re.IGNORECASE)
    query = re.sub(r"\s*(?:视频|影片|videos?|google\s+videos?)\s*$", "", query, flags=re.IGNORECASE)
    return query.strip(" ：:，,。.;；")


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return clean_query_text(quoted.group(1))

    patterns = (
        r"(?:搜索|查找|查询|检索|抓取|采集)\s*(?:google\s*)?(?:视频|影片|videos?)?\s*(.+?)(?:[，。；;]|$)",
        r"(?:google\s+videos?|video\s+search|search\s+videos?\s+for|search\s+for)\s+(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query_text(match.group(1))
            if query:
                return query
    return None


def parse_output_mode(text: str) -> str | None:
    lowered = text.lower()
    checks = (
        (("json+html", "html+json", "返回json+html", "输出json+html"), "2"),
        (("light json", "lite json", "轻量json", "返回light json"), "4"),
        (("返回html", "输出html", "html格式", " as html", " html output"), "3"),
        (("返回json", "输出json", "json格式", " as json", " json output"), "1"),
    )
    for markers, mode in checks:
        if any(marker in lowered for marker in markers):
            return mode
    return None


def parse_language(text: str) -> str | None:
    language = find_alias_near_markers(
        text,
        LANGUAGE_ALIASES,
        ("hl", "语言", "语种", "界面语言", "language", "locale"),
    )
    if language:
        return language

    patterns = (
        r"\bin\s+([a-z][a-z -]{1,40}?)(?:\s+results?|\s+language|\s+locale|\s+no\s+cache|\s+page\b|[,;.]|$)",
        r"\b([a-z][a-z -]{1,40}?)\s+(?:results?|language|locale)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            found = find_alias(match.group(1), LANGUAGE_ALIASES)
            if found:
                return found
    return None


def parse_tbs(text: str) -> str | None:
    lowered = text.lower()
    checks = (
        (("过去一小时", "最近一小时", "past hour", "last hour"), "qdr:h"),
        (("过去一天", "最近一天", "24小时", "past day", "last day"), "qdr:d"),
        (("过去一周", "最近一周", "past week", "last week"), "qdr:w"),
        (("过去一月", "过去一个月", "最近一个月", "past month", "last month"), "qdr:m"),
        (("过去一年", "最近一年", "past year", "last year"), "qdr:y"),
    )
    for markers, value in checks:
        if any(marker in lowered for marker in markers):
            return value
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

    if "google_domain" not in params:
        domain_match = re.search(r"\bgoogle\.[a-z0-9.-]+\b", lowered)
        if domain_match:
            params["google_domain"] = domain_match.group(0)

    if "gl" not in params:
        country = find_alias_near_markers(
            text,
            COUNTRY_ALIASES,
            ("gl", "国家", "地区", "区域", "google地区", "google国家", "country", "region"),
        )
        if country:
            params["gl"] = country

    if "hl" not in params:
        language = parse_language(text)
        if language:
            params["hl"] = language

    if "start" not in params:
        start = parse_page_start(text)
        if start:
            params["start"] = start

    if "json" not in params:
        output_mode = parse_output_mode(text)
        if output_mode:
            params["json"] = output_mode

    if "tbs" not in params:
        tbs = parse_tbs(text)
        if tbs:
            params["tbs"] = tbs

    if "no_cache" not in params:
        if any(marker in lowered for marker in ("no_cache", "no cache", "bypass cache", "不使用缓存", "跳过缓存", "绕过缓存")):
            params["no_cache"] = "true"
        elif any(marker in lowered for marker in ("use cache", "使用缓存", "走缓存")):
            params["no_cache"] = "false"

    if "safe" not in params:
        if any(marker in lowered for marker in ("safe off", "关闭安全", "安全搜索关闭", "成人")):
            params["safe"] = "off"
        elif any(marker in lowered for marker in ("safe on", "开启安全", "安全搜索开启")):
            params["safe"] = "active"

    if "nfpr" not in params:
        if any(marker in lowered for marker in ("排除自动纠正", "不要自动纠正", "exclude autocorrect", "nfpr")):
            params["nfpr"] = "1"
        elif any(marker in lowered for marker in ("包含自动纠正", "允许自动纠正", "include autocorrect")):
            params["nfpr"] = "0"

    if "filter" not in params:
        if any(marker in lowered for marker in ("关闭相似结果", "禁用省略结果", "disable similar", "disable omitted")):
            params["filter"] = "1"
        elif any(marker in lowered for marker in ("开启相似结果", "启用省略结果", "enable similar", "enable omitted")):
            params["filter"] = "0"

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
    normalized: dict[str, str] = {"engine": "google_videos"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q"):
        raise ValueError("Missing required query q. Parse q from the user request or ask the user what videos to search.")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))
    normalized.setdefault("google_domain", "google.com")
    normalized.setdefault("no_cache", "false")
    normalized.setdefault("nfpr", "0")
    normalized.setdefault("filter", "0")

    if "no_cache" in normalized:
        normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

    if "safe" in normalized:
        safe = normalized["safe"].strip().lower()
        normalized["safe"] = "active" if safe in {"active", "on", "true", "1", "开启", "打开"} else "off"

    for field in ("nfpr", "filter"):
        if field in normalized:
            value = normalized[field].strip().lower()
            if value in BOOLEAN_TRUE:
                normalized[field] = "1"
            elif value in BOOLEAN_FALSE:
                normalized[field] = "0"

    if normalized.get("uule"):
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


def mask_authorization(token_arg: str | None) -> str:
    token = get_authorization(token_arg)
    if not token:
        return "missing"
    bare = re.sub(r"^bearer\s+", "", token, flags=re.IGNORECASE)
    if len(bare) <= 8:
        return "provided (***)"
    return f"provided ({bare[:4]}...{bare[-4:]})"


def markdown_cell(value: Any) -> str:
    if value is None:
        return "none"
    text = str(value)
    if not text:
        return "none"
    return text.replace("|", "\\|").replace("\n", " ")


def build_parameter_table(params: dict[str, str], token_arg: str | None) -> str:
    rows = ["| Parameter | Current value | Default value | Description |", "|---|---|---|---|"]
    for name, default, description in PARAMETER_SPECS:
        if name == "Authorization":
            current = mask_authorization(token_arg)
        else:
            current = params.get(name, "")
        rows.append(
            "| "
            + " | ".join(
                (
                    markdown_cell(name),
                    markdown_cell(current),
                    markdown_cell(default),
                    markdown_cell(description),
                )
            )
            + " |"
        )
    return "\n".join(rows)


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

    if args.preview_table:
        print(build_parameter_table(params, args.token))
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
