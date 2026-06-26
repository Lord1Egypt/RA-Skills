#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Jobs and print the raw response body."""

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
    "google_domain",
    "gl",
    "hl",
    "location",
    "uule",
    "next_page_token",
    "chips",
    "lrad",
    "ltype",
    "uds",
    "no_cache",
)

DEFAULTS = {
    "json": "1",
    "google_domain": "google.com",
    "no_cache": "false",
}

PARAMETER_ORDER = ("engine",) + FIELDS

DEFAULT_DISPLAY = {
    "engine": "google_jobs",
    "q": "无默认值",
    "json": "1",
    "google_domain": "google.com",
    "gl": "无默认值",
    "hl": "无默认值",
    "location": "无默认值",
    "uule": "无默认值",
    "next_page_token": "无默认值",
    "chips": "无默认值",
    "lrad": "无默认值",
    "ltype": "无默认值",
    "uds": "无默认值",
    "no_cache": "false",
}

DESCRIPTIONS = {
    "engine": "Google Jobs 引擎，固定值 google_jobs。",
    "q": "职位搜索查询内容。",
    "json": "输出格式：1 返回 JSON，2 返回 JSON+HTML，3 返回 HTML，4 返回 Light JSON。",
    "google_domain": "请求使用的 Google 域名。",
    "gl": "Google 使用的国家/地区代码，通常为两位代码，如 us、uk、fr。",
    "hl": "Google Jobs 使用的语言代码，如 en、es、fr。",
    "location": "搜索发起的地理位置；不要与 uule 同时使用。",
    "uule": "Google 编码位置；不要与 location 同时使用。",
    "next_page_token": "用于检索下一页结果的令牌。",
    "chips": "Google Jobs 页面提取的额外查询或过滤条件令牌。",
    "lrad": "搜索半径，单位为公里。",
    "ltype": "居家办公过滤；文档说明该参数已被 Google 弃用，可接受 true 或 1。",
    "uds": "Google 提供的搜索过滤字符串。",
    "no_cache": "设置 true 可绕过缓存；设置 false 使用可用缓存结果。",
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
        description="Call Dataify Google Jobs API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Jobs fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the normalized payload instead of calling API.")
    parser.add_argument("--preview-table", action="store_true", help="Print the full request parameter table and exit.")

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


def markdown_escape(value: Any) -> str:
    text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def format_preview_table(params: dict[str, str]) -> str:
    rows = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for field in PARAMETER_ORDER:
        current_value = params.get(field, "")
        current_display = current_value if current_value != "" else "未设置"
        rows.append(
            "| {name} | {current} | {default} | {description} |".format(
                name=markdown_escape(field),
                current=markdown_escape(current_display),
                default=markdown_escape(DEFAULT_DISPLAY[field]),
                description=markdown_escape(DESCRIPTIONS[field]),
            )
        )
    return "\n".join(rows)


def find_alias(text: str, aliases: dict[str, str]) -> str | None:
    lowered = text.lower()
    for label, code in aliases.items():
        label_lower = label.lower()
        if label_lower.isascii():
            pattern = rf"(?<![a-z0-9]){re.escape(label_lower)}(?![a-z0-9])"
            if re.search(pattern, lowered):
                return code
        elif label_lower in lowered:
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


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return quoted.group(1).strip()

    patterns = (
        r"(?:搜索|查找|查询|检索|查看|看看|看一下|找)\s*(.+?)(?:[，。；;]|$)",
        r"(?:search\s+for|google\s+jobs|jobs\s+search|search|view|show)\s+(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            query = re.sub(r"^(?:一下|关于|有关)\s*", "", query)
            query = re.sub(r"(?:的)?(?:相关)?(?:工作|职位|岗位|招聘)$", "", query).strip()
            if query:
                return query
    return None


def extract_location(text: str) -> str | None:
    patterns = (
        r"(?:location|地点|位置|地区|城市)\s*[:=：]\s*(\"[^\"]*\"|'[^']*'|[^,，;；。]+)",
        r"\bin\s+([A-Z][A-Za-z .'-]+?)(?:\s+with\b|[,;.]|$)",
        r"(?:在|位于)\s*([^,，;；。]+?)(?:的)?(?:工作|职位|岗位|招聘)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip().strip("\"'")
            if value:
                return value
    return None


def extract_radius(text: str) -> str | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|公里|千米|kilometers?)", text, flags=re.IGNORECASE)
    return match.group(1) if match else None


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

    if "location" not in params and "uule" not in params:
        location = extract_location(text)
        if location:
            params["location"] = location

    if "lrad" not in params:
        radius = extract_radius(text)
        if radius:
            params["lrad"] = radius

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

    if "ltype" not in params and any(
        marker in lowered
        for marker in (
            "remote",
            "work from home",
            "wfh",
            "居家办公",
            "在家办公",
            "远程",
            "遠程",
        )
    ):
        params["ltype"] = "1"

    if "no_cache" not in params and any(
        marker in lowered
        for marker in (
            "no_cache",
            "不使用缓存",
            "不走缓存",
            "跳过缓存",
            "绕过缓存",
            "bypass cache",
            "no cache",
        )
    ):
        params["no_cache"] = "true"

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
    normalized: dict[str, str] = {"engine": "google_jobs"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    for field, default_value in DEFAULTS.items():
        normalized.setdefault(field, default_value)

    if not normalized.get("q"):
        raise ValueError("缺少必填搜索参数 q，请从用户需求中解析 q，或让用户提供要搜索的职位内容。")

    normalized["json"] = normalize_output_mode(normalized["json"])
    normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

    if "ltype" in normalized:
        ltype = normalized["ltype"].strip().lower()
        if ltype in BOOLEAN_TRUE:
            normalized["ltype"] = "1"
        elif ltype in BOOLEAN_FALSE:
            normalized["ltype"] = "false"

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

    if args.preview_table:
        print(format_preview_table(params))
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
