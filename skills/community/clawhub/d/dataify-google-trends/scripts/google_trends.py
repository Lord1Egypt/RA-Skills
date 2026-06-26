#!/usr/bin/env python3
"""Call Dataify Scraper API Google Trends and print the raw response body."""

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
    "hl",
    "geo",
    "region",
    "data_type",
    "tz",
    "cat",
    "gprop",
    "date",
    "csv",
    "include_low_search_volume",
    "no_cache",
)

DISPLAY_FIELDS = ("Authorization", "engine", *FIELDS)

FIELD_DEFAULTS = {
    "Authorization": "无",
    "engine": "google_trends",
    "q": "无（必填）",
    "json": "1",
    "hl": "未设置",
    "geo": "未设置（全球）",
    "region": "取决于 geo",
    "data_type": "未设置",
    "tz": "420",
    "cat": "0",
    "gprop": "未设置（网页搜索）",
    "date": "未设置",
    "csv": "未设置",
    "include_low_search_volume": "未设置",
    "no_cache": "false",
}

FIELD_DESCRIPTIONS = {
    "Authorization": "Dataify API token 请求头；没有 token 时提示用户提供或去 https://dashboard.dataify.com/login?utm_source=skill 注册；展示时隐藏实际值。",
    "engine": "固定值：google_trends。",
    "q": "搜索查询内容；必须从用户要求中解析或向用户确认，不要使用示例值作为默认值。",
    "json": "输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。",
    "hl": "Google Trends 使用的语言代码，例如 en、zh-cn、es、fr。",
    "geo": "搜索发起的地理位置；未设置时表示全球。",
    "region": "区域粒度；仅部分区域类 data_type 使用：COUNTRY、REGION、DMA、CITY。",
    "data_type": "搜索类型：TIMESERIES、GEO_MAP、GEO_MAP_0、RELATED_TOPICS、RELATED_QUERIES。",
    "tz": "时区偏移量，单位分钟，范围 -1439 到 1439；文档默认 420。",
    "cat": "搜索类别；0 表示所有类别。",
    "gprop": "Google 属性：images、news、froogle、youtube；未设置表示网页搜索。",
    "date": "日期或日期范围表达式。",
    "csv": "设为 true 时检索 CSV 结果。",
    "include_low_search_volume": "设为 true 时包含低搜索量区域。",
    "no_cache": "设为 true 跳过 5 分钟缓存；false 使用缓存。",
}

COUNTRY_ALIASES = {
    "全球": "",
    "worldwide": "",
    "global": "",
    "no selection": "",
    "印度": "India",
    "india": "India",
    "美国": "United+States",
    "美國": "United+States",
    "united states": "United+States",
    "usa": "United+States",
    "us": "United+States",
    "巴西": "Brazil",
    "brazil": "Brazil",
    "印度尼西亚": "Indonesia",
    "indonesia": "Indonesia",
    "墨西哥": "Mexico",
    "mexico": "Mexico",
    "日本": "Japan",
    "japan": "Japan",
    "德国": "Germany",
    "德國": "Germany",
    "germany": "Germany",
    "法国": "France",
    "法國": "France",
    "france": "France",
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

REGION_ALIASES = {
    "国家/地区": "COUNTRY",
    "国家": "COUNTRY",
    "country": "COUNTRY",
    "country/region": "COUNTRY",
    "子区域": "REGION",
    "省": "REGION",
    "州": "REGION",
    "region": "REGION",
    "subregion": "REGION",
    "地铁": "DMA",
    "都会区": "DMA",
    "metro": "DMA",
    "dma": "DMA",
    "城市": "CITY",
    "city": "CITY",
}

DATA_TYPE_ALIASES = {
    "时间趋势分析": "TIMESERIES",
    "时间趋势": "TIMESERIES",
    "随时间": "TIMESERIES",
    "interest over time": "TIMESERIES",
    "time trend": "TIMESERIES",
    "timeseries": "TIMESERIES",
    "区域对比分析": "GEO_MAP",
    "区域对比": "GEO_MAP",
    "regional comparison": "GEO_MAP",
    "geo_map": "GEO_MAP",
    "区域兴趣分布": "GEO_MAP_0",
    "按区域的兴趣": "GEO_MAP_0",
    "interest by region": "GEO_MAP_0",
    "geo_map_0": "GEO_MAP_0",
    "相关主题推荐": "RELATED_TOPICS",
    "相关主题": "RELATED_TOPICS",
    "related topics": "RELATED_TOPICS",
    "related_topics": "RELATED_TOPICS",
    "相关查询推荐": "RELATED_QUERIES",
    "相关查询": "RELATED_QUERIES",
    "related queries": "RELATED_QUERIES",
    "related_queries": "RELATED_QUERIES",
}

CATEGORY_ALIASES = {
    "所有类别": "0",
    "all categories": "0",
    "艺术与娱乐": "3",
    "arts & entertainment": "3",
    "arts and entertainment": "3",
    "计算机与电子产品": "5",
    "computers & electronics": "5",
    "computers and electronics": "5",
    "金融": "7",
    "finance": "7",
    "游戏": "8",
    "games": "8",
    "家居与园艺": "11",
    "home & garden": "11",
    "home and garden": "11",
    "商业与工业": "12",
    "business & industrial": "12",
    "business and industrial": "12",
    "互联网与电信": "13",
    "internet & telecom": "13",
    "internet and telecom": "13",
    "人民与社会": "14",
    "people & society": "14",
    "people and society": "14",
    "新闻": "16",
    "news category": "16",
}

GPROP_ALIASES = {
    "网页搜索": "",
    "web search": "",
    "图像搜索": "images",
    "图片搜索": "images",
    "image search": "images",
    "images": "images",
    "新闻搜索": "news",
    "news search": "news",
    "google 购物": "froogle",
    "购物": "froogle",
    "shopping": "froogle",
    "froogle": "froogle",
    "youtube 搜索": "youtube",
    "youtube search": "youtube",
    "youtube": "youtube",
}

BOOLEAN_TRUE = {"1", "true", "yes", "y", "on", "enable", "enabled", "开启", "打开", "启用", "是", "需要"}
BOOLEAN_FALSE = {"0", "false", "no", "n", "off", "disable", "disabled", "关闭", "禁用", "否", "不需要"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Trends API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Trends fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the normalized form payload instead of calling API.")
    parser.add_argument("--preview-table", action="store_true", help="Print a Markdown confirmation table and do not call API.")

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
        if re.fullmatch(r"[a-z0-9_+\-/& ]+", label_lower):
            if re.search(rf"(?<![a-z0-9]){re.escape(label_lower)}(?![a-z0-9])", lowered):
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


def quote_lenient_json_value(match: re.Match[str]) -> str:
    prefix = match.group(1)
    value = match.group(2).strip()
    lowered = value.lower()
    if lowered in {"true", "false", "null"}:
        return f"{prefix}{lowered}"
    if re.fullmatch(r"-?\d+(?:\.\d+)?", value):
        return f"{prefix}{value}"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'{prefix}"{escaped}"'


def load_params_json(raw: str) -> dict[str, Any]:
    try:
        supplied = json_module.loads(raw)
    except json_module.JSONDecodeError as first_error:
        # PowerShell or copied examples may strip JSON quotes. Accept a small,
        # object-only lenient form such as {q:AI,json:2,csv:true}.
        repaired = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', raw.strip())
        repaired = re.sub(r'(:\s*)([^"\{\[\]\s,][^,}\]]*)', quote_lenient_json_value, repaired)
        try:
            supplied = json_module.loads(repaired)
        except json_module.JSONDecodeError as second_error:
            raise ValueError(f"--params-json is not valid JSON: {first_error}") from second_error

    if not isinstance(supplied, dict):
        raise ValueError("--params-json must be a JSON object")
    return supplied


def clean_query_text(query: str) -> str:
    query = re.sub(r"\s*(?:google\s+trends|trends|趋势|趨勢)\s*$", "", query.strip(), flags=re.IGNORECASE)
    return query.strip()


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return clean_query_text(quoted.group(1))

    patterns = (
        r"(?:搜索|查询|检索|抓取|采集|趋势|趨勢)\s*(.+?)(?:[，。；;]|$)",
        r"(?:search\s+)?google\s+trends\s+(?:for\s+)?(.+?)(?:\s+with\b|\s+in\b|\s+for\b|[,;.]|$)",
        r"(?:trends\s+for|search\s+trends\s+for|search\s+for)\s+(.+?)(?:\s+with\b|\s+in\b|\s+for\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query_text(match.group(1))
            if query:
                return query
    return None


def extract_timezone(text: str) -> str | None:
    match = re.search(r"\b(?:tz|timezone|时区|時區)\s*[:=]?\s*(-?\d{1,4})\b", text, flags=re.IGNORECASE)
    return match.group(1) if match else None


def extract_category_number(text: str) -> str | None:
    match = re.search(r"\b(?:cat|category|类别|分類|分类)\s*[:=]?\s*(\d+)\b", text, flags=re.IGNORECASE)
    return match.group(1) if match else None


def extract_date(text: str) -> str | None:
    quoted = re.search(r"(?:date|日期|时间范围|時間範圍)\s*[:=]\s*[\"'“‘](.+?)[\"'”’]", text, flags=re.IGNORECASE)
    if quoted:
        return quoted.group(1).strip()

    key_value = re.search(r"\bdate\s*[:=]\s*([^\n,;，；]+)", text, flags=re.IGNORECASE)
    if key_value:
        return key_value.group(1).strip()

    trend_expr = re.search(r"\b(today\s+\d+(?:-[ymd])?|now\s+\d+-[hd]|all|ytd)\b", text, flags=re.IGNORECASE)
    if trend_expr:
        return trend_expr.group(1).strip()

    range_expr = re.search(r"\b(\d{4}-\d{2}-\d{2}\s+\d{4}-\d{2}-\d{2})\b", text)
    if range_expr:
        return range_expr.group(1).strip()

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

    if "geo" not in params:
        geo = find_alias(text, COUNTRY_ALIASES)
        if geo is not None:
            params["geo"] = geo

    if "region" not in params:
        region = find_alias(text, REGION_ALIASES)
        if region:
            params["region"] = region

    if "data_type" not in params:
        data_type = find_alias(text, DATA_TYPE_ALIASES)
        if data_type:
            params["data_type"] = data_type

    if "cat" not in params:
        category = extract_category_number(text) or find_alias(text, CATEGORY_ALIASES)
        if category:
            params["cat"] = category

    if "gprop" not in params:
        gprop = find_alias(text, GPROP_ALIASES)
        if gprop is not None:
            params["gprop"] = gprop

    if "tz" not in params:
        timezone = extract_timezone(text)
        if timezone:
            params["tz"] = timezone

    if "date" not in params:
        date = extract_date(text)
        if date:
            params["date"] = date

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

    if "csv" not in params:
        if "csv" in lowered:
            params["csv"] = "true"

    if "include_low_search_volume" not in params:
        low_volume_markers = (
            "include_low_search_volume",
            "low search volume",
            "低搜索量",
            "低搜尋量",
        )
        if any(marker in lowered for marker in low_volume_markers):
            params["include_low_search_volume"] = "true"

    if "no_cache" not in params:
        if any(marker in lowered for marker in ("no_cache", "no cache", "bypass cache", "skip cache", "不走缓存", "跳过缓存", "繞過快取")):
            params["no_cache"] = "true"
        elif any(marker in lowered for marker in ("use cache", "使用缓存", "使用快取")):
            params["no_cache"] = "false"

    return params


def merge_params(args: argparse.Namespace) -> dict[str, str]:
    params: dict[str, str] = {}

    if args.request:
        params.update(parse_natural_request(args.request))

    if args.params_json:
        supplied = load_params_json(args.params_json)
        for key, value in supplied.items():
            if key in FIELDS or key == "engine":
                cleaned = clean_value(value)
                if cleaned is not None and key != "engine":
                    params[key] = cleaned

    for field in FIELDS:
        value = clean_value(getattr(args, field))
        if value is not None:
            params[field] = value

    return normalize_params(params)


def normalize_params(params: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {"engine": "google_trends"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q"):
        raise ValueError("Missing required query q. Parse q from the user request or ask the user what Trends query to search.")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))

    if "region" in normalized:
        normalized["region"] = normalized["region"].upper()

    if "data_type" in normalized:
        normalized["data_type"] = normalized["data_type"].upper()

    if "cat" not in normalized:
        normalized["cat"] = "0"

    if "tz" not in normalized:
        normalized["tz"] = "420"

    for boolean_field in ("csv", "include_low_search_volume", "no_cache"):
        if boolean_field in normalized:
            normalized[boolean_field] = normalize_boolean(normalized[boolean_field])

    return normalized


def get_authorization(token_arg: str | None) -> str | None:
    token = clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        return None
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_preview_table(params: dict[str, str], token_present: bool = False) -> str:
    rows = ["| 参数名 | 当前值 | 默认值 | 说明 |", "| --- | --- | --- | --- |"]
    for field in DISPLAY_FIELDS:
        if field == "Authorization":
            current = "已提供（不展示）" if token_present else "未提供"
        else:
            current = params.get(field, "未设置")
        rows.append(
            "| {field} | {current} | {default} | {description} |".format(
                field=markdown_escape(field),
                current=markdown_escape(current),
                default=markdown_escape(FIELD_DEFAULTS[field]),
                description=markdown_escape(FIELD_DESCRIPTIONS[field]),
            )
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
        token_present = bool(clean_value(args.token) or clean_value(os.environ.get("DATAIFY_API_TOKEN")))
        print(render_preview_table(params, token_present=token_present))
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
