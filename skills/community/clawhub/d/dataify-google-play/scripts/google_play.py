#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Play and print the raw response body."""

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
    "apps_category",
    "next_page_token",
    "section_page_token",
    "chart",
    "see_more_token",
    "store_device",
    "age",
    "no_cache",
)

DISPLAY_FIELDS = ("engine",) + FIELDS

DEFAULTS = {
    "engine": "google_play",
    "q": "",
    "json": "1",
    "hl": "",
    "gl": "us",
    "apps_category": "",
    "next_page_token": "",
    "section_page_token": "",
    "chart": "",
    "see_more_token": "",
    "store_device": "phone",
    "age": "",
    "no_cache": "false",
}

FIELD_DESCRIPTIONS = {
    "engine": "固定值，Dataify Google Play 引擎。",
    "q": "要在 Google Play 应用商店中搜索的查询内容。",
    "json": "输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。",
    "hl": "Google Play 使用的语言代码，例如 en、zh-cn、ja、fr。",
    "gl": "Google Play 使用的国家/地区代码；接口文档默认 us。",
    "apps_category": "应用商店类别，例如 PRODUCTIVITY、FINANCE、FAMILY。",
    "next_page_token": "下一页令牌；不要与 section_page_token、see_more_token、chart 同用。",
    "section_page_token": "版块分页令牌；不要与 next_page_token、see_more_token、chart 同用。",
    "chart": "热门排行榜参数；最多可返回 50 条结果，不要与分页/查看更多令牌同用。",
    "see_more_token": "查看更多令牌；不要与 section_page_token、next_page_token、chart 同用。",
    "store_device": "用于排序/浏览结果的设备；不能与 apps_category 或 q 同用。",
    "age": "年龄段子类别；仅在 apps_category=FAMILY 时使用。",
    "no_cache": "true 跳过缓存，false 使用默认 5 分钟缓存。",
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
    "韩国": "kr",
    "韓國": "kr",
    "south korea": "kr",
    "korea": "kr",
    "kr": "kr",
    "印度": "in",
    "india": "in",
    "in": "in",
    "巴西": "br",
    "brazil": "br",
    "br": "br",
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
    "韩文": "ko",
    "韩语": "ko",
    "korean": "ko",
    "ko": "ko",
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
}

BOOLEAN_TRUE = {"1", "true", "yes", "y", "on", "enable", "enabled", "开启", "打开", "启用", "是", "需要", "跳过", "不走"}
BOOLEAN_FALSE = {"0", "false", "no", "n", "off", "disable", "disabled", "关闭", "禁用", "否", "不需要", "使用"}

CATEGORY_ALIASES = {
    "wear os": "ANDROID_WEAR",
    "wear": "ANDROID_WEAR",
    "手表应用": "ANDROID_WEAR",
    "艺术": "ART_AND_DESIGN",
    "art": "ART_AND_DESIGN",
    "design": "ART_AND_DESIGN",
    "车辆": "AUTO_AND_VEHICLES",
    "汽车": "AUTO_AND_VEHICLES",
    "auto": "AUTO_AND_VEHICLES",
    "vehicles": "AUTO_AND_VEHICLES",
    "美容": "BEAUTY",
    "beauty": "BEAUTY",
    "图书": "BOOKS_AND_REFERENCE",
    "书籍": "BOOKS_AND_REFERENCE",
    "books": "BOOKS_AND_REFERENCE",
    "reference": "BOOKS_AND_REFERENCE",
    "商务": "BUSINESS",
    "商业": "BUSINESS",
    "business": "BUSINESS",
    "漫画": "COMICS",
    "comics": "COMICS",
    "通信": "COMMUNICATION",
    "通讯": "COMMUNICATION",
    "communication": "COMMUNICATION",
    "dating": "DATING",
    "约会": "DATING",
    "教育": "EDUCATION",
    "education": "EDUCATION",
    "娱乐": "ENTERTAINMENT",
    "entertainment": "ENTERTAINMENT",
    "活动": "EVENTS",
    "events": "EVENTS",
    "金融": "FINANCE",
    "财经": "FINANCE",
    "finance": "FINANCE",
    "餐饮": "FOOD_AND_DRINK",
    "美食": "FOOD_AND_DRINK",
    "food": "FOOD_AND_DRINK",
    "drink": "FOOD_AND_DRINK",
    "健康": "HEALTH_AND_FITNESS",
    "健身": "HEALTH_AND_FITNESS",
    "fitness": "HEALTH_AND_FITNESS",
    "health": "HEALTH_AND_FITNESS",
    "家居": "HOUSE_AND_HOME",
    "house": "HOUSE_AND_HOME",
    "home": "HOUSE_AND_HOME",
    "库": "LIBRARIES_AND_DEMO",
    "demo": "LIBRARIES_AND_DEMO",
    "libraries": "LIBRARIES_AND_DEMO",
    "生活": "LIFESTYLE",
    "lifestyle": "LIFESTYLE",
    "地图": "MAPS_AND_NAVIGATION",
    "导航": "MAPS_AND_NAVIGATION",
    "maps": "MAPS_AND_NAVIGATION",
    "navigation": "MAPS_AND_NAVIGATION",
    "医疗": "MEDICAL",
    "medical": "MEDICAL",
    "音乐": "MUSIC_AND_AUDIO",
    "音频": "MUSIC_AND_AUDIO",
    "music": "MUSIC_AND_AUDIO",
    "audio": "MUSIC_AND_AUDIO",
    "新闻": "NEWS_AND_MAGAZINES",
    "杂志": "NEWS_AND_MAGAZINES",
    "news": "NEWS_AND_MAGAZINES",
    "magazines": "NEWS_AND_MAGAZINES",
    "育儿": "PARENTING",
    "parenting": "PARENTING",
    "个性化": "PERSONALIZATION",
    "personalization": "PERSONALIZATION",
    "摄影": "PHOTOGRAPHY",
    "拍照": "PHOTOGRAPHY",
    "photography": "PHOTOGRAPHY",
    "效率": "PRODUCTIVITY",
    "办公": "PRODUCTIVITY",
    "生产力": "PRODUCTIVITY",
    "productivity": "PRODUCTIVITY",
    "购物": "SHOPPING",
    "shopping": "SHOPPING",
    "社交": "SOCIAL",
    "social": "SOCIAL",
    "体育": "SPORTS",
    "sports": "SPORTS",
    "工具": "TOOLS",
    "tools": "TOOLS",
    "旅行": "TRAVEL_AND_LOCAL",
    "旅游": "TRAVEL_AND_LOCAL",
    "travel": "TRAVEL_AND_LOCAL",
    "local": "TRAVEL_AND_LOCAL",
    "视频": "VIDEO_PLAYERS",
    "播放器": "VIDEO_PLAYERS",
    "video": "VIDEO_PLAYERS",
    "watch faces": "WATCH_FACE",
    "表盘": "WATCH_FACE",
    "天气": "WEATHER",
    "weather": "WEATHER",
    "儿童": "FAMILY",
    "孩子": "FAMILY",
    "kids": "FAMILY",
    "family": "FAMILY",
    "家庭": "FAMILY",
}

DEVICE_ALIASES = {
    "手机": "phone",
    "phone": "phone",
    "mobile": "phone",
    "平板": "tablet",
    "tablet": "tablet",
    "电视": "tv",
    "tv": "tv",
    "chromebook": "chromebook",
    "手表": "watch",
    "watch": "watch",
    "车载": "car",
    "汽车": "car",
    "car": "car",
}

AGE_ALIASES = {
    "5岁以下": "AGE_RANGE1",
    "5 岁以下": "AGE_RANGE1",
    "五岁以下": "AGE_RANGE1",
    "under 5": "AGE_RANGE1",
    "5 and under": "AGE_RANGE1",
    "6-8": "AGE_RANGE2",
    "6 到 8": "AGE_RANGE2",
    "6至8": "AGE_RANGE2",
    "6 to 8": "AGE_RANGE2",
    "9-12": "AGE_RANGE3",
    "9 到 12": "AGE_RANGE3",
    "9至12": "AGE_RANGE3",
    "9 to 12": "AGE_RANGE3",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Play API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Play fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the confirmation table instead of calling API.")
    parser.add_argument(
        "--dry-run-json",
        action="store_true",
        help="Print normalized payload JSON instead of the confirmation table.",
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


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“‘](.+?)[\"'”’]", text)
    if quoted:
        return quoted.group(1).strip()

    patterns = (
        r"(?:搜索|查找|查询|检索|搜一下)\s*(.+?)(?:[，,。；;]|$)",
        r"(?:search\s+for|google\s+play\s+search|google\s+play)\s+(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            if query:
                return cleanup_query(query)
    return None


def cleanup_query(query: str) -> str:
    query = re.sub(r"\b(?:on|in|from)\s+google\s+play\b", "", query, flags=re.IGNORECASE).strip()
    query = re.sub(r"(?:在)?\s*Google\s*Play\s*(?:应用商店|商店)?(?:上|中|里)?", "", query, flags=re.IGNORECASE).strip()
    country_words = r"(?:美国|美國|日本|英国|英國|法国|法國|德国|德國|韩国|韓國|中国|中國|印度|加拿大|澳大利亚|澳洲)"
    query = re.sub(rf"^{country_words}(?:地区|區|区)?(?:的)?", "", query).strip()
    query = re.sub(rf"{country_words}(?:地区|區|区)?(?:的)?$", "", query).strip()
    return query


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))
    lowered = text.lower()

    if "q" not in params:
        query = extract_query(text)
        if query:
            params["q"] = query

    if "gl" not in params:
        country = find_alias(text, COUNTRY_ALIASES)
        if country:
            params["gl"] = country

    if "hl" not in params:
        language = find_alias(text, LANGUAGE_ALIASES)
        if language:
            params["hl"] = language

    if "apps_category" not in params:
        category = find_alias(text, CATEGORY_ALIASES)
        if category:
            params["apps_category"] = category

    if "store_device" not in params:
        device = find_alias(text, DEVICE_ALIASES)
        if device:
            params["store_device"] = device

    if "age" not in params:
        age = find_alias(text, AGE_ALIASES)
        if age:
            params["age"] = age

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

    token_fields = {
        "next_page_token": ("next_page_token", "下一页令牌", "next page token"),
        "section_page_token": ("section_page_token", "版块页面令牌", "版块分页令牌", "section page token"),
        "see_more_token": ("see_more_token", "查看更多令牌", "see more token"),
    }
    for field, markers in token_fields.items():
        if field not in params:
            for marker in markers:
                pattern = rf"{re.escape(marker)}\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if match:
                    params[field] = match.group(1).strip().strip("\"'")
                    break

    if "chart" not in params and any(marker in lowered for marker in ("chart", "排行榜", "热门榜", "热门排行", "top chart", "popular ranking")):
        params["chart"] = "topselling_free"

    if "no_cache" not in params and any(marker in lowered for marker in ("no_cache", "不走缓存", "跳过缓存", "绕过缓存", "bypass cache", "no cache")):
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
    normalized: dict[str, str] = {"engine": "google_play"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    if not normalized.get("q") and not normalized.get("store_device"):
        raise ValueError("缺少搜索关键词 q，请从用户需求中解析 q，或让用户提供要搜索的 Google Play 内容。")

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))

    if "no_cache" in normalized:
        normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

    if "apps_category" in normalized:
        category = normalized["apps_category"].strip()
        normalized["apps_category"] = CATEGORY_ALIASES.get(category.lower(), category.upper())

    if "store_device" in normalized:
        device = normalized["store_device"].strip()
        normalized["store_device"] = DEVICE_ALIASES.get(device.lower(), device.lower())

    if "age" in normalized:
        age = normalized["age"].strip()
        normalized["age"] = AGE_ALIASES.get(age.lower(), age.upper())

    conflicting_tokens = [field for field in ("next_page_token", "section_page_token", "see_more_token", "chart") if normalized.get(field)]
    if len(conflicting_tokens) > 1:
        raise ValueError(
            "参数冲突：next_page_token、section_page_token、see_more_token、chart 不能同时使用，请只保留一个。"
        )

    if normalized.get("store_device") and (normalized.get("apps_category") or normalized.get("q")):
        raise ValueError("参数冲突：store_device 不能与 apps_category 或 q 一起使用。")

    if normalized.get("age") and normalized.get("apps_category") != "FAMILY":
        raise ValueError("参数冲突：age 仅在 apps_category=FAMILY 时使用。")

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


def print_confirmation_table(params: dict[str, str]) -> None:
    print("| 参数名 | 当前值 | 默认值 | 说明 |")
    print("| --- | --- | --- | --- |")
    for field in DISPLAY_FIELDS:
        current = params.get(field, "")
        default = DEFAULTS.get(field, "")
        description = FIELD_DESCRIPTIONS[field]
        print(
            f"| `{field}` | {markdown_escape(current)} | {markdown_escape(default)} | {markdown_escape(description)} |"
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

    if args.dry_run_json:
        print(json_module.dumps(params, ensure_ascii=False, sort_keys=True))
        return 0

    if args.dry_run:
        print_confirmation_table(params)
        return 0

    authorization = get_authorization(args.token)
    if not authorization:
        print("缺少 Dataify API token，请提供 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。", file=sys.stderr)
        return 2

    return call_api(params, authorization, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
