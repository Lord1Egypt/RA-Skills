#!/usr/bin/env python3
"""Call the Dataify Bing Images API after parsing natural-language requests."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


SUPPORTED_FIELDS = {
    "engine",
    "q",
    "json",
    "mkt",
    "cc",
    "first",
    "count",
    "imagesize",
    "color2",
    "photo",
    "aspect",
    "face",
    "age",
    "license",
    "no_cache",
}

DEFAULT_ENDPOINT = "https://scraperapi.dataify.com/request"

FIELD_ORDER = [
    "engine",
    "q",
    "json",
    "mkt",
    "cc",
    "first",
    "count",
    "imagesize",
    "color2",
    "photo",
    "aspect",
    "face",
    "age",
    "license",
    "no_cache",
]

FIELD_SPECS = {
    "engine": {
        "default": "bing_images",
        "description": "接口引擎，固定为 bing_images。",
    },
    "q": {
        "default": None,
        "description": "搜索关键词，必填；可以是任意语言。",
    },
    "json": {
        "default": "1",
        "description": "采集结果输出格式：1 返回 JSON，2 返回 JSON 和 HTML，3 返回 HTML。",
    },
    "mkt": {
        "default": None,
        "description": "搜索结果界面显示语言，格式为 语言代码-国家/地区代码，例如 en-US。",
    },
    "cc": {
        "default": None,
        "description": "按国家或地区用户习惯展示搜索结果，使用两个字母的国家/地区代码，例如 us、ru、uk。",
    },
    "first": {
        "default": "1",
        "description": "控制自然结果的偏移量；默认值为 1。",
    },
    "count": {
        "default": None,
        "description": "控制每页结果数量；该值为建议值，可能无法完全反映实际返回数量。",
    },
    "imagesize": {
        "default": None,
        "description": "按图片尺寸过滤：small 小、medium 中、large 大、wallpaper 超大/壁纸。",
    },
    "color2": {
        "default": None,
        "description": "按图片颜色过滤：color 彩色、bw 黑白，或 FGcls_RED 等指定颜色。",
    },
    "photo": {
        "default": None,
        "description": "按图片类型过滤：photo 照片、clipart 剪贴画、linedrawing 线条画、animatedgif 动图、animatedgifhttps HTTPS 动图、transparent 透明、shopping 购物。",
    },
    "aspect": {
        "default": None,
        "description": "按图片布局过滤：square 方形、wide 宽图、tall 高图。",
    },
    "face": {
        "default": None,
        "description": "按人物类型过滤：face 仅面部、portrait 头肩肖像。",
    },
    "age": {
        "default": None,
        "description": "按日期过滤：lt1440 过去 24 小时、lt10080 过去一周、lt43200 过去一个月、lt525600 过去一年。",
    },
    "license": {
        "default": None,
        "description": "按使用许可过滤：Type-Any 所有 Creative Commons、L1 Public Domain、L2_L3_L4_L5_L6_L7 免费共享和使用、L2_L3_L4 免费共享和商业使用、L2_L3_L5_L6 免费修改共享和使用、L2_L3 免费修改共享和商业使用。",
    },
    "no_cache": {
        "default": "false",
        "description": "是否跳过缓存：true 跳过缓存，false 使用缓存；默认值为 false。",
    },
}

COUNTRY_WORDS = {
    "china": "cn",
    "chinese": "cn",
    "中国": "cn",
    "us": "us",
    "usa": "us",
    "united states": "us",
    "america": "us",
    "美国": "us",
    "uk": "uk",
    "united kingdom": "uk",
    "英国": "uk",
    "japan": "jp",
    "日本": "jp",
    "india": "in",
    "印度": "in",
    "france": "fr",
    "法国": "fr",
    "germany": "de",
    "德国": "de",
    "russia": "ru",
    "俄罗斯": "ru",
    "canada": "ca",
    "加拿大": "ca",
    "australia": "au",
    "澳大利亚": "au",
}

MARKET_WORDS = {
    "chinese": "zh-CN",
    "china": "zh-CN",
    "simplified chinese": "zh-CN",
    "中文": "zh-CN",
    "中国": "zh-CN",
    "english": "en-US",
    "us english": "en-US",
    "英文": "en-US",
    "英语": "en-US",
    "japanese": "ja-JP",
    "日文": "ja-JP",
    "日语": "ja-JP",
    "french": "fr-FR",
    "法文": "fr-FR",
    "法语": "fr-FR",
    "german": "de-DE",
    "德文": "de-DE",
    "德语": "de-DE",
}

COLOR_WORDS = {
    "color": "color",
    "colored": "color",
    "彩色": "color",
    "仅彩色": "color",
    "black and white": "bw",
    "black-white": "bw",
    "monochrome": "bw",
    "bw": "bw",
    "黑白": "bw",
    "red": "FGcls_RED",
    "红色": "FGcls_RED",
    "orange": "FGcls_ORGANGE",
    "橙色": "FGcls_ORGANGE",
    "yellow": "FGcls_YELLOW",
    "黄色": "FGcls_YELLOW",
    "green": "FGcls_GREEN",
    "绿色": "FGcls_GREEN",
    "teal": "FGcls_TEAL",
    "青色": "FGcls_TEAL",
    "blue": "FGcls_BLUE",
    "蓝色": "FGcls_BLUE",
    "purple": "FGcls_PURPLE",
    "紫色": "FGcls_PURPLE",
    "pink": "FGcls_PINK",
    "粉色": "FGcls_PINK",
    "brown": "FGcls_BROWN",
    "棕色": "FGcls_BROWN",
    "black": "FGcls_BLACK",
    "黑色": "FGcls_BLACK",
    "gray": "FGcls_GRAY",
    "grey": "FGcls_GRAY",
    "灰色": "FGcls_GRAY",
    "white": "FGcls_WHITE",
    "白色": "FGcls_WHITE",
}

PHOTO_WORDS = {
    "photo": "photo",
    "photos": "photo",
    "photograph": "photo",
    "照片": "photo",
    "clipart": "clipart",
    "clip art": "clipart",
    "剪贴画": "clipart",
    "linedrawing": "linedrawing",
    "line drawing": "linedrawing",
    "line art": "linedrawing",
    "线条画": "linedrawing",
    "线稿": "linedrawing",
    "animatedgif": "animatedgif",
    "animated gif": "animatedgif",
    "gif": "animatedgif",
    "动图": "animatedgif",
    "animatedgifhttps": "animatedgifhttps",
    "https gif": "animatedgifhttps",
    "https 动图": "animatedgifhttps",
    "transparent": "transparent",
    "透明": "transparent",
    "shopping": "shopping",
    "购物": "shopping",
    "商品": "shopping",
}


class MissingTokenError(ValueError):
    """Raised when Dataify authentication is unavailable."""


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def as_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def default_values() -> dict[str, str]:
    values: dict[str, str] = {}
    for key, spec in FIELD_SPECS.items():
        default = spec["default"]
        if default is not None:
            values[key] = str(default)
    return values


def display_value(value: str | None) -> str:
    return value if value not in {None, ""} else "-"


def markdown_table(payload: dict[str, str]) -> str:
    rows = ["| 参数名 | 当前值 | 默认值 | 说明 |", "|---|---|---|---|"]
    for key in FIELD_ORDER:
        spec = FIELD_SPECS[key]
        rows.append(
            f"| `{key}` | {display_value(payload.get(key))} | "
            f"{display_value(spec['default'])} | {spec['description']} |"
        )
    return "\n".join(rows)


def strip_wrapping_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    return value.strip("“”‘’")


def normalize_key(key: str) -> str:
    raw_key = key.strip()
    lower_key = raw_key.lower().replace("-", "_")
    aliases = {
        "query": "q",
        "keyword": "q",
        "keywords": "q",
        "search": "q",
        "关键词": "q",
        "关键字": "q",
        "查询": "q",
        "搜索词": "q",
        "format": "json",
        "output": "json",
        "输出": "json",
        "格式": "json",
        "market": "mkt",
        "市场": "mkt",
        "country": "cc",
        "国家": "cc",
        "地区": "cc",
        "offset": "first",
        "start": "first",
        "开始": "first",
        "起始": "first",
        "数量": "count",
        "结果数": "count",
        "size": "imagesize",
        "image_size": "imagesize",
        "imagesize": "imagesize",
        "尺寸": "imagesize",
        "大小": "imagesize",
        "color": "color2",
        "colour": "color2",
        "颜色": "color2",
        "image_type": "photo",
        "type": "photo",
        "kind": "photo",
        "类型": "photo",
        "图片类型": "photo",
        "layout": "aspect",
        "aspect": "aspect",
        "比例": "aspect",
        "布局": "aspect",
        "face_type": "face",
        "person": "face",
        "people": "face",
        "人物": "face",
        "人脸": "face",
        "time": "age",
        "date": "age",
        "freshness": "age",
        "时间": "age",
        "日期": "age",
        "license": "license",
        "licence": "license",
        "许可": "license",
        "授权": "license",
        "no_cache": "no_cache",
        "nocache": "no_cache",
        "cache": "no_cache",
        "缓存": "no_cache",
    }
    return aliases.get(lower_key, raw_key)


def parse_bool(value: str) -> str:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on", "skip", "bypass", "refresh", "fresh", "跳过", "不要", "不使用", "开启"}:
        return "true"
    if text in {"0", "false", "no", "n", "off", "use", "cached", "使用", "关闭"}:
        return "false"
    raise ValueError(f"Invalid boolean value for no_cache: {value!r}")


def normalize_json_format(value: str) -> str:
    text = value.strip().lower().replace("，", "+")
    text = re.sub(r"\s+", " ", text)
    mapping = {
        "1": "1",
        "json": "1",
        "json only": "1",
        "只要json": "1",
        "仅json": "1",
        "2": "2",
        "json+html": "2",
        "json + html": "2",
        "json and html": "2",
        "html+json": "2",
        "html + json": "2",
        "html and json": "2",
        "both": "2",
        "都要": "2",
        "3": "3",
        "html": "3",
        "html only": "3",
        "只要html": "3",
        "仅html": "3",
    }
    compact = text.replace(" ", "")
    if text in mapping:
        return mapping[text]
    if compact in mapping:
        return mapping[compact]
    if "json" in text and "html" in text:
        return "2"
    raise ValueError("json must be 1, 2, 3, JSON, HTML, or JSON+HTML")


def normalize_imagesize(value: str) -> str:
    text = value.strip().lower()
    compact = re.sub(r"\s+", "", text)
    mapping = {
        "small": "small",
        "小": "small",
        "小图": "small",
        "小尺寸": "small",
        "medium": "medium",
        "中": "medium",
        "中等": "medium",
        "中图": "medium",
        "large": "large",
        "big": "large",
        "大": "large",
        "大图": "large",
        "大尺寸": "large",
        "wallpaper": "wallpaper",
        "extra large": "wallpaper",
        "xlarge": "wallpaper",
        "超大": "wallpaper",
        "壁纸": "wallpaper",
    }
    if text in mapping:
        return mapping[text]
    if compact in mapping:
        return mapping[compact]
    raise ValueError("imagesize must be small, medium, large, or wallpaper")


def normalize_color2(value: str) -> str:
    text = value.strip()
    upper = text.upper()
    allowed = {
        "color",
        "bw",
        "FGcls_RED",
        "FGcls_ORGANGE",
        "FGcls_YELLOW",
        "FGcls_GREEN",
        "FGcls_TEAL",
        "FGcls_BLUE",
        "FGcls_PURPLE",
        "FGcls_PINK",
        "FGcls_BROWN",
        "FGcls_BLACK",
        "FGcls_GRAY",
        "FGcls_WHITE",
    }
    for allowed_value in allowed:
        if text == allowed_value:
            return allowed_value
        if upper == allowed_value.upper():
            return allowed_value
    lowered = text.lower()
    if lowered in COLOR_WORDS:
        return COLOR_WORDS[lowered]
    if text in COLOR_WORDS:
        return COLOR_WORDS[text]
    raise ValueError("color2 has an unsupported value")


def normalize_photo(value: str) -> str:
    text = value.strip().lower()
    allowed = {"photo", "clipart", "linedrawing", "animatedgif", "animatedgifhttps", "transparent", "shopping"}
    if text in allowed:
        return text
    compact = re.sub(r"[\s_-]+", "", text)
    compact_map = {
        "clipart": "clipart",
        "lineart": "linedrawing",
        "linedrawing": "linedrawing",
        "animatedgif": "animatedgif",
        "gif": "animatedgif",
        "httpsgif": "animatedgifhttps",
    }
    if compact in compact_map:
        return compact_map[compact]
    if text in PHOTO_WORDS:
        return PHOTO_WORDS[text]
    raise ValueError("photo must be photo, clipart, linedrawing, animatedgif, animatedgifhttps, transparent, or shopping")


def normalize_aspect(value: str) -> str:
    text = value.strip().lower()
    mapping = {
        "square": "square",
        "正方形": "square",
        "方形": "square",
        "wide": "wide",
        "horizontal": "wide",
        "landscape": "wide",
        "宽": "wide",
        "横向": "wide",
        "宽图": "wide",
        "tall": "tall",
        "vertical": "tall",
        "portrait": "tall",
        "高": "tall",
        "纵向": "tall",
        "竖图": "tall",
    }
    if text in mapping:
        return mapping[text]
    raise ValueError("aspect must be square, wide, or tall")


def normalize_face(value: str) -> str:
    text = value.strip().lower()
    mapping = {
        "face": "face",
        "faces": "face",
        "face only": "face",
        "only face": "face",
        "人脸": "face",
        "仅面部": "face",
        "面部": "face",
        "portrait": "portrait",
        "head shoulders": "portrait",
        "head and shoulders": "portrait",
        "头像": "portrait",
        "肖像": "portrait",
        "头肩": "portrait",
    }
    compact = re.sub(r"\s+", " ", text)
    if compact in mapping:
        return mapping[compact]
    raise ValueError("face must be face or portrait")


def normalize_age(value: str) -> str:
    text = value.strip().lower()
    compact = re.sub(r"\s+", "", text)
    mapping = {
        "lt1440": "lt1440",
        "past 24 hours": "lt1440",
        "last 24 hours": "lt1440",
        "today": "lt1440",
        "24小时": "lt1440",
        "过去24小时": "lt1440",
        "最近24小时": "lt1440",
        "今天": "lt1440",
        "lt10080": "lt10080",
        "past week": "lt10080",
        "last week": "lt10080",
        "this week": "lt10080",
        "一周": "lt10080",
        "过去一周": "lt10080",
        "最近一周": "lt10080",
        "lt43200": "lt43200",
        "past month": "lt43200",
        "last month": "lt43200",
        "this month": "lt43200",
        "一个月": "lt43200",
        "过去一个月": "lt43200",
        "最近一个月": "lt43200",
        "lt525600": "lt525600",
        "past year": "lt525600",
        "last year": "lt525600",
        "this year": "lt525600",
        "一年": "lt525600",
        "过去一年": "lt525600",
        "最近一年": "lt525600",
    }
    if text in mapping:
        return mapping[text]
    if compact in mapping:
        return mapping[compact]
    raise ValueError("age must be lt1440, lt10080, lt43200, or lt525600")


def normalize_license(value: str) -> str:
    text = value.strip().lower()
    compact = re.sub(r"[\s_-]+", "", text)
    allowed = {
        "Type-Any",
        "L1",
        "L2_L3_L4_L5_L6_L7",
        "L2_L3_L4",
        "L2_L3_L5_L6",
        "L2_L3",
    }
    for allowed_value in allowed:
        if value.strip() == allowed_value:
            return allowed_value
        if value.strip().upper() == allowed_value.upper():
            return allowed_value
    if "public domain" in text or "公有领域" in text or "公共领域" in text:
        return "L1"
    if "creative commons" in text or "cc license" in text or "知识共享" in text:
        return "Type-Any"
    if ("commercial" in text or "商业" in text) and ("modify" in text or "修改" in text or "改编" in text):
        return "L2_L3"
    if "commercial" in text or "商业" in text:
        return "L2_L3_L4"
    if "modify" in text or "修改" in text or "改编" in text:
        return "L2_L3_L5_L6"
    if compact in {"typeany", "allcreativecommons", "allcc"}:
        return "Type-Any"
    if compact in {"publicdomain"}:
        return "L1"
    if "free" in text or "免费" in text or "共享" in text:
        return "L2_L3_L4_L5_L6_L7"
    raise ValueError("license has an unsupported value")


def parse_key_value_pairs(prompt: str) -> dict[str, str]:
    values: dict[str, str] = {}
    key_pattern = (
        r"engine|q|query|keyword|keywords|search|关键词|关键字|查询|搜索词|"
        r"json|format|output|输出|格式|mkt|market|市场|cc|country|国家|地区|"
        r"first|offset|start|开始|起始|count|数量|结果数|"
        r"imagesize|image_size|size|尺寸|大小|color2|color|colour|颜色|"
        r"photo|image_type|type|kind|类型|图片类型|aspect|layout|比例|布局|"
        r"face|face_type|person|people|人物|人脸|age|date|time|freshness|时间|日期|"
        r"license|licence|许可|授权|no_cache|no-cache|nocache|cache|缓存"
    )
    pattern = re.compile(
        rf"(?P<key>{key_pattern})\s*(?:=|:|：)\s*(?P<value>\"[^\"]+\"|'[^']+'|[^,\n;，；]+)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(prompt):
        key = normalize_key(match.group("key"))
        values[key] = strip_wrapping_quotes(match.group("value"))
    return values


def parse_query(prompt: str) -> str | None:
    patterns = [
        r"(?:search|find|look up|query)\s+(?:bing\s+)?(?:images?|pictures?)?\s*(?:for\s+)?[\"'](?P<q>[^\"']+)[\"']",
        r"(?:search|find|look up|query)\s+(?:bing\s+)?(?:images?|pictures?)?\s*(?:for\s+)?(?P<q>.+?)(?:\s+(?:with|using|return|mkt=|cc=|first=|count=|size|image size|color|type|layout|aspect|face|date|license|json|html|cache)|$)",
        r"(?:搜索|查找|查询|找|抓取|爬取)(?:必应|Bing)?(?:图片|图像)?\s*[\"“'](?P<q>[^\"”']+)[\"”']",
        r"(?:搜索|查找|查询|找|抓取|爬取)(?:必应|Bing)?(?:图片|图像)?\s*(?P<q>.+?)(?:，|,|。|；|;|要求|返回|尺寸|大小|颜色|类型|布局|比例|人脸|人物|时间|日期|许可|授权|市场|国家|地区|数量|跳过缓存|不使用缓存|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            query = match.group("q").strip()
            query = re.split(
                r"\s*[,;，；]\s*(?=(?:small|medium|large|wallpaper|extra large|square|wide|tall|horizontal|vertical|"
                r"photo|photos|clipart|line drawing|line art|animated|gif|transparent|shopping|"
                r"red|orange|yellow|green|teal|blue|purple|pink|brown|black|gray|grey|white|"
                r"past|last|this|public domain|creative commons|free|commercial|modify|return|count|cc=|mkt=)\b|"
                r"(?:小图|中图|大图|壁纸|正方形|方形|横向|纵向|透明|照片|剪贴画|线条画|动图|"
                r"红色|橙色|黄色|绿色|青色|蓝色|紫色|粉色|棕色|黑色|灰色|白色|过去|最近|今天|返回|数量|美国|中国))",
                query,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip()
            query = re.sub(r"\s+", " ", query)
            query = re.sub(r"\s*(?:的)?(?:图片|图像|相关图片|结果)\s*$", "", query)
            return query.rstrip(".。 ，,")
    text = prompt.strip()
    if text and not parse_key_value_pairs(prompt):
        return text
    return None


def infer_output_format(prompt: str) -> str | None:
    text = prompt.lower()
    compact = re.sub(r"\s+", "", text)
    if re.search(r"(json\s*(\+|and)\s*html|html\s*(\+|and)\s*json|both)", text) or "json和html" in compact or "html和json" in compact or "都要" in compact:
        return "2"
    if re.search(r"(html only|return html|html format)", text) or "只要html" in compact or "返回html" in compact:
        return "3"
    if re.search(r"(json only|return json|json format)", text) or "只要json" in compact or "返回json" in compact:
        return "1"
    return None


def infer_no_cache(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(no_cache|no-cache|skip cache|bypass cache|refresh|fresh)", text) or any(word in prompt for word in ["实时", "刷新", "跳过缓存", "不要缓存", "不使用缓存"]):
        return "true"
    if re.search(r"(use cache|cached)", text) or "使用缓存" in prompt:
        return "false"
    return None


def infer_market(prompt: str) -> str | None:
    match = re.search(r"\b([a-z]{2}-[a-z]{2})\b", prompt, re.IGNORECASE)
    if match:
        language, country = match.group(1).split("-", 1)
        return f"{language.lower()}-{country.upper()}"
    text = prompt.lower()
    for word, mkt in MARKET_WORDS.items():
        if word in text or word in prompt:
            return mkt
    return None


def infer_country(prompt: str) -> str | None:
    text = prompt.lower()
    match = re.search(r"\bcc\s*(?:=|:)\s*([a-z]{2})\b", text)
    if match:
        return match.group(1).lower()
    for word, cc in COUNTRY_WORDS.items():
        if word in text or word in prompt:
            return cc
    return None


def infer_first(prompt: str) -> str | None:
    patterns = [
        r"\b(?:first|offset|start)\s*(?:=|:)?\s*(\d+)\b",
        r"(?:从第|偏移|起始|开始)\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def infer_count(prompt: str) -> str | None:
    patterns = [
        r"\b(?:count|limit|number of results|results)\s*(?:=|:)?\s*(\d+)\b",
        r"(?:返回|要|获取|数量)\s*(\d+)\s*(?:张|个|条|幅)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def infer_imagesize(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"\b(wallpaper|extra large|xlarge)\b", text) or any(word in prompt for word in ["壁纸", "超大"]):
        return "wallpaper"
    if re.search(r"\b(large|big)\s+(?:image|images|picture|pictures|photo|photos)\b", text) or any(word in prompt for word in ["大图", "大尺寸"]):
        return "large"
    if re.search(r"\bmedium\s+(?:image|images|picture|pictures|photo|photos)\b", text) or any(word in prompt for word in ["中图", "中等尺寸"]):
        return "medium"
    if re.search(r"\bsmall\s+(?:image|images|picture|pictures|photo|photos)\b", text) or any(word in prompt for word in ["小图", "小尺寸"]):
        return "small"
    return None


def infer_color2(prompt: str) -> str | None:
    text = prompt.lower()
    for word, value in sorted(COLOR_WORDS.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(rf"(?<![a-z0-9]){re.escape(word)}(?![a-z0-9])", text) or word in prompt:
            return value
    return None


def infer_photo(prompt: str) -> str | None:
    text = prompt.lower()
    for word, value in sorted(PHOTO_WORDS.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(rf"(?<![a-z0-9]){re.escape(word)}(?![a-z0-9])", text) or word in prompt:
            return value
    return None


def infer_aspect(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"\b(square)\b", text) or any(word in prompt for word in ["正方形", "方形"]):
        return "square"
    if re.search(r"\b(wide|horizontal|landscape)\b", text) or any(word in prompt for word in ["横向", "宽图", "宽屏"]):
        return "wide"
    if re.search(r"\b(tall|vertical|portrait)\b", text) or any(word in prompt for word in ["纵向", "竖图", "高图"]):
        return "tall"
    return None


def infer_face(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"\b(face|faces|face only|only face)\b", text) or any(word in prompt for word in ["人脸", "面部", "仅面部"]):
        return "face"
    if re.search(r"\b(portrait|head and shoulders|head shoulders)\b", text) or any(word in prompt for word in ["头像", "肖像", "头肩"]):
        return "portrait"
    return None


def infer_age(prompt: str) -> str | None:
    text = prompt.lower()
    compact = re.sub(r"\s+", "", prompt)
    if "lt1440" in text or re.search(r"(past|last)\s*24\s*hours?", text) or any(word in compact for word in ["过去24小时", "最近24小时", "今天"]):
        return "lt1440"
    if "lt10080" in text or re.search(r"(past|last|this)\s*week", text) or any(word in compact for word in ["过去一周", "最近一周", "近一周"]):
        return "lt10080"
    if "lt43200" in text or re.search(r"(past|last|this)\s*month", text) or any(word in compact for word in ["过去一个月", "最近一个月", "近一个月"]):
        return "lt43200"
    if "lt525600" in text or re.search(r"(past|last|this)\s*year", text) or any(word in compact for word in ["过去一年", "最近一年", "近一年"]):
        return "lt525600"
    return None


def infer_license(prompt: str) -> str | None:
    text = prompt.lower()
    if "public domain" in text or "公有领域" in prompt or "公共领域" in prompt:
        return "L1"
    if "creative commons" in text or "知识共享" in prompt:
        return "Type-Any"
    if ("commercial" in text or "商业" in prompt) and ("modify" in text or "修改" in prompt or "改编" in prompt):
        return "L2_L3"
    if "commercial" in text or "商业" in prompt:
        return "L2_L3_L4"
    if "modify" in text or "修改" in prompt or "改编" in prompt:
        return "L2_L3_L5_L6"
    if re.search(r"\bfree\b", text) or "免费" in prompt or "共享" in prompt:
        return "L2_L3_L4_L5_L6_L7"
    return None


def parse_prompt(prompt: str) -> dict[str, str]:
    values = default_values()
    values.update(parse_key_value_pairs(prompt))

    if "q" not in values:
        query = parse_query(prompt)
        if query:
            values["q"] = query

    inference_steps = [
        ("json", infer_output_format),
        ("no_cache", infer_no_cache),
        ("mkt", infer_market),
        ("cc", infer_country),
        ("first", infer_first),
        ("count", infer_count),
        ("imagesize", infer_imagesize),
        ("color2", infer_color2),
        ("photo", infer_photo),
        ("aspect", infer_aspect),
        ("face", infer_face),
        ("age", infer_age),
        ("license", infer_license),
    ]
    for key, infer in inference_steps:
        if key not in values:
            value = infer(prompt)
            if value:
                values[key] = value

    return values


def apply_overrides(payload: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    for key in ["q", "json", "mkt", "cc", "first", "count", "imagesize", "color2", "photo", "aspect", "face", "age", "license"]:
        value = getattr(args, key, None)
        if value is not None:
            payload[key] = value

    if args.no_cache is not None:
        payload["no_cache"] = parse_bool(args.no_cache)

    for item in args.field or []:
        if "=" not in item:
            raise ValueError(f"--field must be key=value, got {item!r}")
        key, value = item.split("=", 1)
        key = normalize_key(key)
        if key not in SUPPORTED_FIELDS:
            raise ValueError(f"Unsupported field {key!r}")
        payload[key] = value

    return payload


def validate_payload(payload: dict[str, str]) -> dict[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in payload.items():
        key = normalize_key(key)
        if key not in SUPPORTED_FIELDS:
            continue
        if value is None:
            continue
        value = str(value).strip()
        if value == "":
            continue
        cleaned[key] = value

    cleaned["engine"] = "bing_images"

    if not cleaned.get("q"):
        raise ValueError("Missing required field q. Provide --q or a prompt with an image search query.")

    if "json" in cleaned:
        cleaned["json"] = normalize_json_format(cleaned["json"])

    if "no_cache" in cleaned:
        cleaned["no_cache"] = parse_bool(cleaned["no_cache"])

    if "mkt" in cleaned:
        match = re.fullmatch(r"([a-z]{2})-([a-z]{2})", cleaned["mkt"], re.IGNORECASE)
        if not match:
            raise ValueError("mkt must look like en-US or zh-CN")
        cleaned["mkt"] = f"{match.group(1).lower()}-{match.group(2).upper()}"

    if "cc" in cleaned:
        if not re.fullmatch(r"[a-z]{2}", cleaned["cc"], re.IGNORECASE):
            raise ValueError("cc must be a two-letter country or region code")
        cleaned["cc"] = cleaned["cc"].lower()

    if "first" in cleaned:
        first = int(cleaned["first"])
        if first < 1:
            raise ValueError("first must be greater than or equal to 1")
        cleaned["first"] = str(first)

    if "count" in cleaned:
        count = int(cleaned["count"])
        if count < 1:
            raise ValueError("count must be greater than or equal to 1")
        cleaned["count"] = str(count)

    if "imagesize" in cleaned:
        cleaned["imagesize"] = normalize_imagesize(cleaned["imagesize"])

    if "color2" in cleaned:
        cleaned["color2"] = normalize_color2(cleaned["color2"])

    if "photo" in cleaned:
        cleaned["photo"] = normalize_photo(cleaned["photo"])

    if "aspect" in cleaned:
        cleaned["aspect"] = normalize_aspect(cleaned["aspect"])

    if "face" in cleaned:
        cleaned["face"] = normalize_face(cleaned["face"])

    if "age" in cleaned:
        cleaned["age"] = normalize_age(cleaned["age"])

    if "license" in cleaned:
        cleaned["license"] = normalize_license(cleaned["license"])

    return cleaned


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.getenv("DATAIFY_API_TOKEN")
    if not token:
        raise MissingTokenError(
            "缺少 DATAIFY_API_TOKEN。请输入 Dataify API token，或访问 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"
        )
    token = token.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def call_api(token: str, payload: dict[str, str], body_format: str, timeout: float) -> tuple[bool, str]:
    headers = {
        "Authorization": token,
        "Accept": "application/json, text/plain;q=0.9, */*;q=0.8",
        "User-Agent": "codex-bing-images-skill/1.0",
    }

    if body_format == "json":
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    else:
        data = urllib.parse.urlencode(payload).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    request = urllib.request.Request(DEFAULT_ENDPOINT, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            text = raw.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            return 200 <= response.status < 300, text
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        return False, text or f"HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return False, str(exc.reason)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="解析并调用 Dataify Bing Images API。")
    parser.add_argument("--prompt", default="", help="待解析的用户自然语言请求。")
    parser.add_argument("--q", help="覆盖搜索关键词。")
    parser.add_argument("--json", help="输出格式：1 JSON，2 JSON 和 HTML，3 HTML。")
    parser.add_argument("--mkt", help="市场和语言，例如 zh-CN 或 en-US。")
    parser.add_argument("--cc", help="两个字母的国家或地区代码。")
    parser.add_argument("--first", help="自然结果偏移量。")
    parser.add_argument("--count", help="请求的结果数量。")
    parser.add_argument("--imagesize", help="尺寸过滤：small、medium、large 或 wallpaper。")
    parser.add_argument("--color2", help="颜色过滤，例如 color、bw 或 FGcls_BLUE。")
    parser.add_argument("--photo", help="图片类型：photo、clipart、linedrawing、animatedgif、animatedgifhttps、transparent 或 shopping。")
    parser.add_argument("--aspect", help="布局过滤：square、wide 或 tall。")
    parser.add_argument("--face", help="人物过滤：face 或 portrait。")
    parser.add_argument("--age", help="日期过滤：lt1440、lt10080、lt43200 或 lt525600。")
    parser.add_argument("--license", help="使用许可过滤。")
    parser.add_argument("--no-cache", "--no_cache", dest="no_cache", help="true 跳过缓存，false 使用缓存。")
    parser.add_argument("--field", action="append", help="额外 API 字段覆盖，格式 key=value。")
    parser.add_argument("--token", help="本次运行使用的 API token；缺少 Bearer 前缀时会自动添加。")
    parser.add_argument("--body-format", choices=["form", "json"], default="form", help="POST 请求体格式。")
    parser.add_argument("--timeout", type=float, default=60.0, help="请求超时时间，单位秒。")
    parser.add_argument("--preview", action="store_true", help="输出完整请求参数表，并跳过网络和鉴权检查。")
    parser.add_argument("--confirmed", action="store_true", help="用户确认预览参数后，允许真实调用接口。")
    parser.add_argument("--dry-run", action="store_true", help="输出解析后的 payload，并跳过网络和鉴权检查。")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    try:
        payload = parse_prompt(args.prompt)
        payload = apply_overrides(payload, args)
        payload = validate_payload(payload)

        if args.preview:
            print(markdown_table(payload))
            return 0

        if args.dry_run:
            print(as_json({"ok": True, "dry_run": True, "payload": payload}))
            return 0

        if not args.confirmed:
            eprint("请先使用 --preview 展示完整请求参数表，并在用户确认后再使用 --confirmed 调用接口。")
            return 1

        token = resolve_token(args)
        ok, response_text = call_api(token, payload, args.body_format, args.timeout)
        sys.stdout.write(response_text)
        if response_text and not response_text.endswith("\n"):
            sys.stdout.write("\n")
        return 0 if ok else 2
    except MissingTokenError as exc:
        eprint(str(exc))
        return 1
    except Exception as exc:
        eprint(as_json({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
