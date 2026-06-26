#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call the Dataify DuckDuckGo Search API from natural-language input."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Iterable, Optional


API_URL = "https://scraperapi.dataify.com/request"

REGION_ALIASES = {
    "us": "us-en",
    "usa": "us-en",
    "united states": "us-en",
    "america": "us-en",
    "美国": "us-en",
    "美区": "us-en",
    "uk": "uk-en",
    "united kingdom": "uk-en",
    "britain": "uk-en",
    "england": "uk-en",
    "英国": "uk-en",
    "france": "fr-fr",
    "french": "fr-fr",
    "法国": "fr-fr",
    "germany": "de-de",
    "german": "de-de",
    "德国": "de-de",
    "japan": "jp-jp",
    "japanese": "jp-jp",
    "日本": "jp-jp",
    "korea": "kr-kr",
    "south korea": "kr-kr",
    "韩国": "kr-kr",
    "china": "cn-zh",
    "mainland china": "cn-zh",
    "中国": "cn-zh",
    "中国大陆": "cn-zh",
    "taiwan": "tw-tzh",
    "台湾": "tw-tzh",
    "hong kong": "hk-tzh",
    "香港": "hk-tzh",
    "canada": "ca-en",
    "加拿大": "ca-en",
    "australia": "au-en",
    "澳大利亚": "au-en",
}

PARAM_SPECS = [
    {
        "name": "engine",
        "default": "duckduckgo",
        "description": "DuckDuckGo 搜索引擎，固定为 duckduckgo。",
    },
    {
        "name": "q",
        "default": "",
        "description": "搜索关键词，必填；接口文档中的 pizza 是示例值，不作为默认值。",
    },
    {
        "name": "json",
        "default": "1",
        "description": "采集结果输出格式：1=JSON（默认），2=JSON+HTML，3=HTML，4=Light JSON。",
    },
    {
        "name": "kl",
        "default": "",
        "description": "DuckDuckGo 搜索地区代码，如 us-en、uk-en、fr-fr；未指定则不传。",
    },
    {
        "name": "search_assist",
        "default": "false",
        "description": "是否返回 DuckDuckGo AI 搜索辅助，默认 false；与 m 不能一起使用。",
    },
    {
        "name": "safe",
        "default": "-1",
        "description": "成人内容过滤级别：1=严格，-1=中等（默认），-2=关闭。",
    },
    {
        "name": "df",
        "default": "",
        "description": "日期过滤：d=过去一天，w=过去一周，m=过去一月，y=过去一年，或 YYYY-MM-DD..YYYY-MM-DD；未指定则不传。",
    },
    {
        "name": "start",
        "default": "0",
        "description": "结果偏移量；不使用偏移量时为 0 或留空，默认按 0 处理。",
    },
    {
        "name": "m",
        "default": "50",
        "description": "要返回的最大结果数量，默认 50，范围 1-50；与 search_assist 不能一起使用。",
    },
    {
        "name": "no_cache",
        "default": "false",
        "description": "是否跳过缓存：true=跳过缓存，false=使用缓存（默认）。",
    },
]
PARAM_ORDER = [spec["name"] for spec in PARAM_SPECS]


def strip_quotes(value: str) -> str:
    return value.strip().strip("\"'“”‘’")


def display_value(value: Optional[str]) -> str:
    return value if value not in (None, "") else "未指定"


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def apply_defaults(fields: Dict[str, str]) -> Dict[str, str]:
    with_defaults = {
        spec["name"]: spec["default"]
        for spec in PARAM_SPECS
        if spec["default"] != ""
    }
    with_defaults.update({key: value for key, value in fields.items() if value not in (None, "")})
    return normalize_conflicts(with_defaults)


def normalize_conflicts(fields: Dict[str, str]) -> Dict[str, str]:
    normalized = dict(fields)
    if normalized.get("search_assist") == "true":
        normalized.pop("m", None)
    return normalized


def request_body_from_fields(fields: Dict[str, str]) -> Dict[str, str]:
    body = {
        key: fields[key]
        for key in PARAM_ORDER
        if key in fields and fields[key] not in (None, "")
    }
    if body.get("search_assist") == "true":
        body.pop("m", None)
    elif body.get("search_assist") == "false" and "m" in body:
        body.pop("search_assist", None)
    return body


def build_preview_table(fields: Dict[str, str]) -> str:
    lines = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    spec_by_name = {spec["name"]: spec for spec in PARAM_SPECS}
    for name in PARAM_ORDER:
        spec = spec_by_name[name]
        current = display_value(fields.get(name))
        default = display_value(spec["default"])
        description = spec["description"]
        lines.append(
            f"| `{name}` | {escape_table_cell(current)} | {escape_table_cell(default)} | {escape_table_cell(description)} |"
        )
    return "\n".join(lines)


def find_assignment(text: str, names: Iterable[str]) -> Optional[str]:
    joined = "|".join(re.escape(name) for name in names)
    pattern = rf"(?:^|[\s,，;；])(?:{joined})\s*[:=]\s*(\"[^\"]+\"|'[^']+'|[^,，;；\n]+)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return strip_quotes(match.group(1))


def normalize_bool(value: str) -> Optional[str]:
    value = strip_quotes(value).strip().lower()
    value = re.split(r"\s+", value, maxsplit=1)[0]
    if value in {"true", "1", "yes", "y", "on", "开启", "打开", "是", "需要"}:
        return "true"
    if value in {"false", "0", "no", "n", "off", "关闭", "否", "不需要"}:
        return "false"
    return None


def normalize_json_format(value: str) -> Optional[str]:
    value = strip_quotes(value).lower().replace(" ", "")
    if value in {"1", "json"}:
        return "1"
    if value in {"2", "json+html", "jsonhtml", "html+json", "json和html"}:
        return "2"
    if value in {"3", "html"}:
        return "3"
    if value in {"4", "lightjson", "light-json", "轻量json", "轻量"}:
        return "4"
    return None


def normalize_safe(value: str) -> Optional[str]:
    value = strip_quotes(value).lower()
    value = re.split(r"\s+", value, maxsplit=1)[0]
    if value in {"1", "strict", "严格", "强", "high"}:
        return "1"
    if value in {"-1", "moderate", "medium", "中等", "默认", "适中"}:
        return "-1"
    if value in {"-2", "off", "none", "关闭", "关", "不过滤"}:
        return "-2"
    return None


def normalize_count(value: str) -> Optional[str]:
    match = re.search(r"\d+", value)
    if not match:
        return None
    count = max(1, min(50, int(match.group(0))))
    return str(count)


def normalize_integer(value: str) -> Optional[str]:
    match = re.search(r"\d+", value)
    return match.group(0) if match else None


def parse_region(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("kl", "region", "地区", "区域", "国家"))
    if assigned:
        assigned = strip_quotes(assigned).strip()
        compact = assigned.replace(" ", "")
        if re.fullmatch(r"[a-z]{2}-[a-z]{2,4}", compact, flags=re.IGNORECASE):
            return compact.lower()
        lowered = assigned.lower()
        if lowered in REGION_ALIASES:
            return REGION_ALIASES[lowered]
        if assigned in REGION_ALIASES:
            return REGION_ALIASES[assigned]

    lowered_text = text.lower()
    for alias, code in sorted(REGION_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias.isascii():
            if re.search(rf"(?<![a-z]){re.escape(alias)}(?![a-z])", lowered_text):
                return code
        elif alias in text:
            return code
    return None


def parse_json_format(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("json", "format", "输出格式", "返回格式"))
    if assigned:
        parsed = normalize_json_format(assigned)
        if parsed:
            return parsed

    lowered = text.lower()
    if re.search(r"light[- ]?json|轻量\s*json", lowered):
        return "4"
    has_json = re.search(r"\bjson\b|JSON", text, flags=re.IGNORECASE) is not None
    has_html = re.search(r"\bhtml\b|HTML", text, flags=re.IGNORECASE) is not None
    if has_json and has_html:
        return "2"
    if has_html and re.search(r"只要|仅|only|格式", text, flags=re.IGNORECASE):
        return "3"
    if has_json:
        return "1"
    return None


def parse_safe(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("safe", "安全过滤", "成人过滤"))
    if assigned:
        parsed = normalize_safe(assigned)
        if parsed:
            return parsed

    lowered = text.lower()
    if re.search(r"safe\s*(strict|1)|安全过滤.{0,4}严格|严格.{0,4}过滤", lowered):
        return "1"
    if re.search(r"safe\s*(moderate|-1)|安全过滤.{0,4}(中等|默认|适中)", lowered):
        return "-1"
    if re.search(r"safe\s*(off|-2)|关闭.{0,4}(安全|成人).{0,4}过滤|(安全|成人).{0,4}过滤.{0,4}关闭|不过滤成人", lowered):
        return "-2"
    return None


def parse_date_filter(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("df", "date", "日期", "时间范围", "时间过滤"))
    if assigned:
        assigned = strip_quotes(assigned)
        if re.fullmatch(r"[dwmy]", assigned, flags=re.IGNORECASE):
            return assigned.lower()
        range_match = re.search(r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}", assigned)
        if range_match:
            return range_match.group(0)

    range_match = re.search(r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}", text)
    if range_match:
        return range_match.group(0)

    lowered = text.lower()
    if re.search(r"past\s*day|last\s*day|最近\s*(1|一)?\s*天|过去\s*(1|一)?\s*天|今天", lowered):
        return "d"
    if re.search(r"past\s*week|last\s*week|最近\s*(7|七|一)?\s*(天|周|星期)|过去\s*(7|七|一)?\s*(天|周|星期)|一周内", lowered):
        return "w"
    if re.search(r"past\s*month|last\s*month|最近\s*(30|三十|一)?\s*(天|月)|过去\s*(30|三十|一)?\s*(天|月)|一月内", lowered):
        return "m"
    if re.search(r"past\s*year|last\s*year|最近\s*(1|一)?\s*年|过去\s*(1|一)?\s*年|一年内", lowered):
        return "y"
    return None


def parse_search_assist(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("search_assist", "search-assist", "搜索辅助", "ai搜索辅助", "ai 搜索辅助"))
    if assigned:
        parsed = normalize_bool(assigned)
        if parsed:
            return parsed

    lowered = text.lower()
    if re.search(r"(不要|不需要|不开启|关闭|禁用).{0,8}(搜索辅助|ai\s*搜索辅助|search\s*assist)", lowered):
        return "false"
    if re.search(r"(开启|打开|启用|需要|包含|返回).{0,8}(搜索辅助|ai\s*搜索辅助|search\s*assist)", lowered):
        return "true"
    if re.search(r"search[_ -]?assist|ai\s*搜索辅助", lowered):
        return "true"
    return None


def parse_no_cache(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("no_cache", "no-cache", "cache", "缓存"))
    if assigned:
        parsed = normalize_bool(assigned)
        if parsed:
            return parsed

    lowered = text.lower()
    if re.search(r"no[_ -]?cache|不用缓存|不使用缓存|跳过缓存|绕过缓存|关闭缓存|实时", lowered):
        return "true"
    if re.search(r"使用缓存|走缓存|启用缓存", lowered):
        return "false"
    return None


def parse_count(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("m", "count", "limit", "数量", "结果数"))
    if assigned:
        parsed = normalize_count(assigned)
        if parsed:
            return parsed

    patterns = (
        r"返回\s*(\d+)\s*(?:条|个)?(?:自然)?(?:搜索)?(?:结果)?",
        r"(?:前|top)\s*(\d+)\s*(?:条|个)?",
        r"(\d+)\s*(?:条|个)\s*(?:自然)?(?:搜索)?结果",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return normalize_count(match.group(1))
    return None


def parse_start(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("start", "offset", "偏移", "起始"))
    if assigned:
        parsed = normalize_integer(assigned)
        if parsed:
            return parsed

    patterns = (
        r"(?:从|跳过|偏移)\s*第?\s*(\d+)\s*(?:条|个)?",
        r"skip\s*(\d+)",
        r"offset\s*(\d+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def clean_query(candidate: str) -> str:
    candidate = strip_quotes(candidate)
    removals = (
        r"^(?:请|帮我|帮忙|给我|麻烦)?\s*(?:用|通过)?\s*(?:dataify|duckduckgo)?\s*(?:搜索|查询|检索|查找|搜一下)\s*",
        r"^(?:please\s+)?(?:search(?:\s+for)?|look\s+up|find)\s+",
        r"\b(?:through|via|using|use)\s+(?:dataify|duckduckgo)\b",
        r"\b(?:dataify|duckduckgo)\b",
        r"\b(?:in|region)\s+[a-z]{2}-[a-z]{2,4}\b",
        r"\b[a-z]{2}-[a-z]{2,4}\b",
        r"用\s*(?:dataify|duckduckgo)",
        r"通过\s*(?:dataify|duckduckgo)",
        r"返回\s*\d+\s*(?:条|个)?(?:自然)?(?:搜索)?结果?",
        r"(?:前|top)\s*\d+\s*(?:条|个)?",
        r"\d+\s*(?:条|个)\s*(?:自然)?(?:搜索)?结果",
        r"(?:json\s*\+\s*html|html\s*\+\s*json|light\s*json|轻量\s*json|json|html)\s*(?:格式|输出|返回)?",
        r"(?:过去|最近)\s*(?:\d+|一|七|三十)?\s*(?:天|周|星期|月|年)",
        r"(?:past|last)\s+(?:day|week|month|year)",
        r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}",
        r"(?:地区|区域|国家|region|kl)\s*[:=为是]?\s*[\w-]+",
        r"(?:安全过滤|成人过滤|safe)\s*[:=为是]?\s*(?:严格|中等|默认|适中|关闭|strict|moderate|off|-?1|-2)",
        r"(?:不使用|不用|跳过|绕过|关闭|使用|走|启用)?\s*缓存",
        r"(?:no[_ -]?cache|cache)\s*[:=]?\s*(?:true|false|1|0|yes|no|on|off)?",
        r"(?:开启|打开|启用|需要|包含|返回|不要|不需要|不开启|关闭|禁用)?\s*(?:ai\s*)?搜索辅助",
        r"search[_ -]?assist\s*[:=]?\s*(?:true|false|1|0|yes|no|on|off)?",
        r"(?:m|count|limit|start|offset|df|date|format)\s*[:=]\s*[^,，;；\s]+",
    )
    for pattern in removals:
        candidate = re.sub(pattern, " ", candidate, flags=re.IGNORECASE)
    candidate = re.sub(r"\s+", " ", candidate)
    return candidate.strip(" ,，;；。:：")


def parse_query(text: str) -> Optional[str]:
    assigned = find_assignment(text, ("q", "query", "keyword", "keywords", "关键词", "搜索词"))
    if assigned:
        query = clean_query(assigned)
        if query:
            return query

    patterns = (
        r"(?:搜索|查询|检索|查找|搜一下)\s*[\"“]?(.+?)(?:[\"”]?(?:[,，;；。]|\s+(?:返回|输出|地区|区域|国家|过去|最近|安全|开启|关闭|不用|不使用|跳过|使用缓存|no[_ -]?cache|json|html|top|\d+\s*(?:条|个))))",
        r"(?:search(?:\s+for)?|look\s+up|find)\s+[\"']?(.+?)(?:[\"']?(?:[,，;；.]|\s+(?:return|with|region|past|last|safe|no[_ -]?cache|json|html|top|\d+\s*results?)))",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query(match.group(1))
            if query:
                return query

    fallback = clean_query(text)
    if fallback:
        return fallback
    return None


def parse_request(text: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}

    query = parse_query(text)
    if query:
        fields["q"] = query

    parsers = {
        "json": parse_json_format,
        "kl": parse_region,
        "search_assist": parse_search_assist,
        "safe": parse_safe,
        "df": parse_date_filter,
        "start": parse_start,
        "m": parse_count,
        "no_cache": parse_no_cache,
    }
    for field, parser in parsers.items():
        value = parser(text)
        if value is not None:
            fields[field] = value

    return normalize_conflicts(fields)


def apply_explicit_args(fields: Dict[str, str], args: argparse.Namespace) -> Dict[str, str]:
    if args.q:
        fields["q"] = args.q
    if args.json_format:
        parsed = normalize_json_format(args.json_format)
        if not parsed:
            raise SystemExit("--json must be one of 1, 2, 3, 4, JSON, JSON+HTML, HTML, or Light JSON")
        fields["json"] = parsed
    if args.kl:
        fields["kl"] = args.kl.strip().lower()
    if args.search_assist:
        parsed = normalize_bool(args.search_assist)
        if not parsed:
            raise SystemExit("--search-assist must be true or false")
        fields["search_assist"] = parsed
    if args.safe:
        parsed = normalize_safe(args.safe)
        if not parsed:
            raise SystemExit("--safe must be 1, -1, -2, strict, moderate, or off")
        fields["safe"] = parsed
    if args.df:
        fields["df"] = args.df
    if args.start:
        parsed = normalize_integer(args.start)
        if not parsed:
            raise SystemExit("--start must contain an integer")
        fields["start"] = parsed
    if args.m:
        parsed = normalize_count(args.m)
        if not parsed:
            raise SystemExit("--m must contain an integer from 1 to 50")
        fields["m"] = parsed
    if args.no_cache:
        parsed = normalize_bool(args.no_cache)
        if not parsed:
            raise SystemExit("--no-cache must be true or false")
        fields["no_cache"] = parsed

    return normalize_conflicts(fields)


def get_token(args: argparse.Namespace) -> str:
    token = args.token or os.environ.get("DATAIFY_API_TOKEN")
    if not token and not args.no_prompt and sys.stdin.isatty():
        print(
            "未检测到 Dataify API token。请输入 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。",
            file=sys.stderr,
        )
        token = getpass.getpass("Dataify API token: ")

    if not token:
        raise SystemExit(
            "未检测到 Dataify API token。请提供 --token，设置 DATAIFY_API_TOKEN，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"
        )

    os.environ["DATAIFY_API_TOKEN"] = token
    if not re.match(r"^Bearer\s+", token, flags=re.IGNORECASE):
        token = f"Bearer {token}"
    return token


def post_request(body: Dict[str, str], token: str) -> int:
    payload = urllib.parse.urlencode(body).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": token,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            sys.stdout.buffer.write(response.read())
            return 0
    except urllib.error.HTTPError as exc:
        sys.stdout.buffer.write(exc.read())
        return 1
    except urllib.error.URLError as exc:
        raise SystemExit(f"请求 Dataify API 失败: {exc.reason}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Call Dataify DuckDuckGo Search API.")
    parser.add_argument("text", nargs="*", help="Natural-language request text.")
    parser.add_argument("--request", "-r", default="", help="Natural-language request text.")
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--q", help="Search query.")
    parser.add_argument("--json", dest="json_format", help="Output format: 1, 2, 3, 4, JSON, JSON+HTML, HTML, Light JSON.")
    parser.add_argument("--kl", help="DuckDuckGo region code, e.g. us-en.")
    parser.add_argument("--search-assist", help="Whether to return DuckDuckGo AI search assist: true or false.")
    parser.add_argument("--safe", help="Safe search level: 1 strict, -1 moderate, -2 off.")
    parser.add_argument("--df", help="Date filter: d, w, m, y, or YYYY-MM-DD..YYYY-MM-DD.")
    parser.add_argument("--start", help="Result offset.")
    parser.add_argument("--m", help="Maximum result count, 1 to 50.")
    parser.add_argument("--no-cache", dest="no_cache", help="Whether to skip cache: true or false.")
    parser.add_argument("--dry-run", action="store_true", help="Print the request body without calling the API.")
    parser.add_argument("--preview", action="store_true", help="Print a Markdown parameter table and do not call the API.")
    parser.add_argument("--confirmed", action="store_true", help="Confirm the displayed parameters and call the API.")
    parser.add_argument("--no-prompt", action="store_true", help="Do not prompt interactively for a token.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    request_text = args.request or " ".join(args.text)
    fields = parse_request(request_text)
    fields = apply_explicit_args(fields, args)
    fields = apply_defaults(fields)

    if not fields.get("q"):
        raise SystemExit("缺少搜索关键词 q。请告诉我要搜索什么。")

    if args.preview:
        print(build_preview_table(fields))
        return 0

    if args.dry_run:
        print(json.dumps(request_body_from_fields(fields), ensure_ascii=False, indent=2))
        return 0

    if not args.confirmed:
        raise SystemExit("调用接口前必须先向用户展示参数表并获得确认。确认后请添加 --confirmed 再调用。")

    token = get_token(args)
    return post_request(request_body_from_fields(fields), token)


if __name__ == "__main__":
    raise SystemExit(main())
