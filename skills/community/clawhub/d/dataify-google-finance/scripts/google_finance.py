#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Finance and print the raw response body."""

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
    "window",
    "no_cache",
)

TABLE_FIELDS = (
    "engine",
    "q",
    "json",
    "hl",
    "window",
    "no_cache",
)

DEFAULTS = {
    "json": "1",
    "window": "1D",
    "no_cache": "false",
}

FIELD_METADATA = {
    "engine": {
        "default": "google_finance",
        "description": "Google 金融接口固定值：google_finance。",
    },
    "q": {
        "default": "无",
        "description": "想要搜索的查询内容，可以是股票、指数、共同基金、货币或期货。",
    },
    "json": {
        "default": "1",
        "description": "采集结果输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。",
    },
    "hl": {
        "default": "无",
        "description": "Google 金融要使用的语言代码，例如 en、es、fr。",
    },
    "window": {
        "default": "1D",
        "description": "图表时间范围：1D、5D、1M、6M、YTD、1Y、5Y、MAX。",
    },
    "no_cache": {
        "default": "false",
        "description": "是否跳过缓存：true=跳过缓存，false=使用缓存结果。",
    },
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

QUERY_STOPWORDS = {
    "json",
    "html",
    "light",
    "google",
    "finance",
    "googlefinance",
    "google_finance",
    "1d",
    "5d",
    "1m",
    "6m",
    "ytd",
    "1y",
    "5y",
    "max",
}


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Finance API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Finance fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the normalized payload instead of calling API.")
    parser.add_argument(
        "--preview-table",
        action="store_true",
        help="Print the pre-call Markdown parameter table instead of calling API.",
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


def normalize_window(value: Any) -> str:
    text = str(value).strip()
    compact = re.sub(r"[\s_-]+", "", text).lower()
    mapping = {
        "1d": "1D",
        "1day": "1D",
        "oneday": "1D",
        "一天": "1D",
        "1天": "1D",
        "1日": "1D",
        "5d": "5D",
        "5day": "5D",
        "5days": "5D",
        "fivedays": "5D",
        "五天": "5D",
        "5天": "5D",
        "5日": "5D",
        "1m": "1M",
        "1month": "1M",
        "onemonth": "1M",
        "一个月": "1M",
        "1个月": "1M",
        "1個月": "1M",
        "6m": "6M",
        "6month": "6M",
        "6months": "6M",
        "sixmonths": "6M",
        "六个月": "6M",
        "6个月": "6M",
        "6個月": "6M",
        "ytd": "YTD",
        "yeartodate": "YTD",
        "年初至今": "YTD",
        "1y": "1Y",
        "1year": "1Y",
        "oneyear": "1Y",
        "一年": "1Y",
        "1年": "1Y",
        "5y": "5Y",
        "5year": "5Y",
        "5years": "5Y",
        "fiveyears": "5Y",
        "五年": "5Y",
        "5年": "5Y",
        "max": "MAX",
        "maximum": "MAX",
        "最大": "MAX",
        "最大值": "MAX",
    }
    return mapping.get(compact, text.upper())


def find_alias(text: str, aliases: dict[str, str]) -> str | None:
    lowered = text.lower()
    for label, code in aliases.items():
        if re.search(rf"(?<![a-z0-9_]){re.escape(label.lower())}(?![a-z0-9_])", lowered):
            return code
    return None


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=：]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；。]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        value = raw_value.strip().strip("\"'")
        params[field.lower()] = value
    return params


def parse_params_json(value: str) -> dict[str, Any]:
    try:
        supplied = json_module.loads(value)
    except json_module.JSONDecodeError as original_exc:
        repaired = value.strip()
        repaired = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', repaired)
        repaired = re.sub(
            r":\s*([^{}\[\],\"'\s][^{}\[\],]*?)(\s*[,}])",
            lambda match: (
                f": {match.group(1).strip()}{match.group(2)}"
                if match.group(1).strip().lower() in {"true", "false", "null"}
                or re.fullmatch(r"-?\d+(?:\.\d+)?", match.group(1).strip())
                else f': "{match.group(1).strip()}"{match.group(2)}'
            ),
            repaired,
        )
        try:
            supplied = json_module.loads(repaired)
        except json_module.JSONDecodeError as repaired_exc:
            raise ValueError(f"--params-json 不是有效 JSON: {original_exc}") from repaired_exc
    if not isinstance(supplied, dict):
        raise ValueError("--params-json 必须是 JSON object")
    return supplied


def strip_query_noise(query: str) -> str:
    text = query.strip().strip("\"'“”‘’")
    text = re.sub(r"^(?:一下|关于|有关|的)\s*", "", text)
    text = re.sub(r"\s*(?:的)?(?:股票|股价|行情|金融数据|走势图|图表|价格)$", "", text)
    return text.strip()


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        query = strip_query_noise(quoted.group(1))
        if query:
            return query

    symbol_match = re.search(
        r"\b(?:NASDAQ|NYSE|NYSEARCA|AMEX|INDEXNASDAQ|INDEXNYSEGIS|INDEXSP|CURRENCY|MUTF|FUTURES?)[.:][A-Z0-9._-]+\b",
        text,
        flags=re.IGNORECASE,
    )
    if symbol_match:
        return symbol_match.group(0).upper()

    patterns = (
        r"(?:搜索|查找|查询|检索|获取|抓取|看一下)\s*(?:Google\s*金融|Google\s*Finance|金融|财经)?\s*(.+?)(?:[，。；;]|$)",
        r"(?:google\s*finance|finance\s*search|search\s+for|quote|price)\s+(?:for\s+)?(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = strip_query_noise(match.group(1))
            if query:
                return query

    uppercase_candidates = re.findall(r"\b[A-Z][A-Z0-9.]{0,9}\b", text)
    for candidate in uppercase_candidates:
        if candidate.lower() not in QUERY_STOPWORDS:
            return candidate

    return None


def parse_window(text: str) -> str | None:
    lowered = text.lower()
    ordered_markers = (
        (("年初至今", "ytd", "year to date"), "YTD"),
        (("最大值", "最大", "max", "maximum"), "MAX"),
        (("5年", "五年", "5 year", "5-year", "5y"), "5Y"),
        (("1年", "一年", "1 year", "1-year", "1y"), "1Y"),
        (("6个月", "6個月", "六个月", "6 month", "6-month", "6m"), "6M"),
        (("1个月", "1個月", "一个月", "1 month", "1-month", "1m"), "1M"),
        (("5天", "五天", "5 day", "5-day", "5d"), "5D"),
        (("1天", "一天", "1 day", "1-day", "1d"), "1D"),
    )
    for markers, value in ordered_markers:
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

    if "hl" not in params:
        language = find_alias(text, LANGUAGE_ALIASES)
        if language:
            params["hl"] = language

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

    if "window" not in params:
        window = parse_window(text)
        if window:
            params["window"] = window

    if "no_cache" not in params:
        true_markers = (
            "no_cache",
            "不使用缓存",
            "不走缓存",
            "跳过缓存",
            "绕过缓存",
            "bypass cache",
            "no cache",
        )
        false_markers = (
            "使用缓存",
            "走缓存",
            "use cache",
            "with cache",
        )
        if any(marker in lowered for marker in true_markers):
            params["no_cache"] = "true"
        elif any(marker in lowered for marker in false_markers):
            params["no_cache"] = "false"

    return params


def merge_params(args: argparse.Namespace) -> dict[str, str]:
    params: dict[str, str] = {}

    if args.request:
        params.update(parse_natural_request(args.request))

    if args.params_json:
        supplied = parse_params_json(args.params_json)
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
    normalized: dict[str, str] = {"engine": "google_finance"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    for field, default_value in DEFAULTS.items():
        normalized.setdefault(field, default_value)

    if not normalized.get("q"):
        raise ValueError("缺少必填搜索参数 q，请从用户需求中解析 q，或让用户提供要搜索的股票、指数、共同基金、货币或期货。")

    normalized["json"] = normalize_output_mode(normalized["json"])
    normalized["window"] = normalize_window(normalized["window"])
    normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

    if "hl" in normalized:
        language = find_alias(normalized["hl"], LANGUAGE_ALIASES)
        if language:
            normalized["hl"] = language

    return normalized


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def print_preview_table(params: dict[str, str]) -> None:
    print("| 参数名 | 当前值 | 默认值 | 说明 |")
    print("| --- | --- | --- | --- |")
    for field in TABLE_FIELDS:
        meta = FIELD_METADATA[field]
        current = params.get(field, "")
        print(
            "| "
            f"{markdown_escape(field)} | "
            f"{markdown_escape(current)} | "
            f"{markdown_escape(meta['default'])} | "
            f"{markdown_escape(meta['description'])} |"
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

    if args.preview_table:
        print_preview_table(params)
        return 0

    if args.dry_run:
        print(json_module.dumps(params, ensure_ascii=False, sort_keys=True))
        return 0

    authorization = get_authorization(args.token)
    if not authorization:
        print("缺少 Dataify API token，请提供 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。", file=sys.stderr)
        return 2

    return call_api(params, authorization, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
