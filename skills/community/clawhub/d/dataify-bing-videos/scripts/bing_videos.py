#!/usr/bin/env python3
"""Call the Dataify Bing Videos API after parsing natural-language requests."""

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
    "setlang",
    "first",
    "length",
    "date",
    "resolution",
    "source_site",
    "price",
    "no_cache",
}

DEFAULT_ENDPOINT = "https://scraperapi.dataify.com/request"

FIELD_ORDER = [
    "engine",
    "q",
    "json",
    "mkt",
    "cc",
    "setlang",
    "first",
    "length",
    "date",
    "resolution",
    "source_site",
    "price",
    "no_cache",
]

FIELD_DEFAULTS = {
    "engine": "bing_videos",
    "q": "pizza",
    "json": "1",
    "mkt": "",
    "cc": "",
    "setlang": "",
    "first": "1",
    "length": "",
    "date": "",
    "resolution": "",
    "source_site": "",
    "price": "",
    "no_cache": "false",
}

FIELD_DESCRIPTIONS = {
    "engine": "Bing视频接口标识，固定为 bing_videos。",
    "q": "搜索关键词，字段说明中的默认值为 pizza；用户指定搜索词时优先使用用户值。",
    "json": "输出格式：1=JSON，2=JSON+HTML，3=HTML。",
    "mkt": "搜索结果界面显示语言和市场，格式为 语言-国家/地区，例如 en-US。",
    "cc": "按国家/地区用户习惯展示结果的两字母国家/地区代码，例如 us、ru、uk。",
    "setlang": "搜索使用的语言代码，通常为两字母代码，例如 en、zh、ja。",
    "first": "自然结果偏移量；说明中的默认值为 1。",
    "length": "按视频时长过滤：short 少于5分钟，medium 5-20分钟，long 超过20分钟。",
    "date": "按日期过滤：lt1440 过去24小时，lt10080 过去一周，lt43200 过去一个月，lt525600 过去一年。",
    "resolution": "按分辨率过滤：lowerthan_360p、360p、480p、720p、1080p。",
    "source_site": "按来源网站过滤，例如 dailymotion.com、vimeo.com、cnn.com。",
    "price": "按价格过滤：free 免费，paid 付费。",
    "no_cache": "是否跳过缓存；说明中的默认值为 false，true 表示跳过缓存。",
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

LANGUAGE_WORDS = {
    "chinese": "zh",
    "中文": "zh",
    "汉语": "zh",
    "english": "en",
    "英文": "en",
    "英语": "en",
    "japanese": "ja",
    "日文": "ja",
    "日语": "ja",
    "french": "fr",
    "法文": "fr",
    "法语": "fr",
    "german": "de",
    "德文": "de",
    "德语": "de",
    "spanish": "es",
    "西班牙语": "es",
}

SOURCE_SITES = {
    "dailymotion": "dailymotion.com",
    "dailymotion.com": "dailymotion.com",
    "vimeo": "vimeo.com",
    "vimeo.com": "vimeo.com",
    "metacafe": "metacafe.com",
    "metacafe.com": "metacafe.com",
    "hulu": "hulu.com",
    "hulu.com": "hulu.com",
    "vevo": "vevo.com",
    "vevo.com": "vevo.com",
    "myspace": "myspace.com",
    "myspace.com": "myspace.com",
    "mtv": "mtv.com",
    "mtv.com": "mtv.com",
    "cbs": "cbsnews.com",
    "cbs news": "cbsnews.com",
    "cbsnews.com": "cbsnews.com",
    "fox": "foxnews.com",
    "fox news": "foxnews.com",
    "foxnews.com": "foxnews.com",
    "cnn": "cnn.com",
    "cnn.com": "cnn.com",
    "msn": "msn.com",
    "msn.com": "msn.com",
}


class MissingTokenError(ValueError):
    """Raised when Dataify authentication is unavailable."""


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def as_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def format_parameter_table(payload: dict[str, str]) -> str:
    lines = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "|---|---|---|---|",
    ]
    for field in FIELD_ORDER:
        current_value = payload.get(field, "")
        default_value = FIELD_DEFAULTS.get(field, "")
        description = FIELD_DESCRIPTIONS[field]
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(field),
                    markdown_escape(current_value),
                    markdown_escape(default_value),
                    markdown_escape(description),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


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
        "lang": "setlang",
        "language": "setlang",
        "语言": "setlang",
        "offset": "first",
        "start": "first",
        "开始": "first",
        "偏移": "first",
        "duration": "length",
        "时长": "length",
        "time": "date",
        "period": "date",
        "时间": "date",
        "日期": "date",
        "quality": "resolution",
        "分辨率": "resolution",
        "清晰度": "resolution",
        "source": "source_site",
        "site": "source_site",
        "source_site": "source_site",
        "来源": "source_site",
        "网站": "source_site",
        "站点": "source_site",
        "cost": "price",
        "价格": "price",
        "no_cache": "no_cache",
        "nocache": "no_cache",
        "cache": "no_cache",
        "缓存": "no_cache",
    }
    return aliases.get(lower_key, raw_key)


def parse_bool(value: str) -> str:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on", "skip", "bypass", "refresh", "fresh", "跳过", "不要", "不使用"}:
        return "true"
    if text in {"0", "false", "no", "n", "off", "use", "cached", "使用"}:
        return "false"
    raise ValueError(f"Invalid boolean value for no_cache: {value!r}")


def normalize_json_format(value: str) -> str:
    text = value.strip().lower().replace("＋", "+")
    text = re.sub(r"\s+", " ", text)
    mapping = {
        "1": "1",
        "json": "1",
        "json only": "1",
        "只要json": "1",
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
    }
    compact = text.replace(" ", "")
    if text in mapping:
        return mapping[text]
    if compact in mapping:
        return mapping[compact]
    if "json" in text and "html" in text:
        return "2"
    raise ValueError("json must be 1, 2, 3, JSON, HTML, or JSON+HTML")


def normalize_length(value: str) -> str:
    text = value.strip().lower()
    if text in {"short", "短", "短视频"} or re.search(r"(under|less than|<)\s*5", text) or "少于 5" in text or "少于5" in text:
        return "short"
    if text in {"medium", "中", "中等", "中视频"} or re.search(r"5\s*[-~到至]\s*20", text):
        return "medium"
    if text in {"long", "长", "长视频"} or re.search(r"(over|more than|>)\s*20", text) or "超过 20" in text or "超过20" in text:
        return "long"
    raise ValueError("length must be short, medium, or long")


def normalize_date(value: str) -> str:
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
    raise ValueError("date must be lt1440, lt10080, lt43200, or lt525600")


def normalize_resolution(value: str) -> str:
    text = value.strip().lower().replace(" ", "")
    if text in {"lowerthan_360p", "below360p", "under360p", "低于360p", "小于360p"}:
        return "lowerthan_360p"
    for resolution in ["1080p", "720p", "480p", "360p"]:
        if resolution in text:
            return resolution
    if text in {"hd", "高清"}:
        return "720p"
    if text in {"fullhd", "fhd", "全高清"}:
        return "1080p"
    raise ValueError("resolution must be lowerthan_360p, 360p, 480p, 720p, or 1080p")


def normalize_source_site(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"^https?://", "", text)
    text = text.split("/", 1)[0].strip()
    if text in SOURCE_SITES:
        return SOURCE_SITES[text]
    if re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", text):
        return text
    raise ValueError("source_site must be a supported source name or a domain such as vimeo.com")


def normalize_price(value: str) -> str:
    text = value.strip().lower()
    if text in {"free", "gratis", "免费", "不要钱", "0"}:
        return "free"
    if text in {"paid", "pay", "付费", "收费"}:
        return "paid"
    raise ValueError("price must be free or paid")


def parse_key_value_pairs(prompt: str) -> dict[str, str]:
    values: dict[str, str] = {}
    key_pattern = (
        r"engine|q|query|keyword|keywords|search|json|format|output|mkt|market|cc|country|"
        r"setlang|lang|language|first|offset|start|length|duration|date|time|period|"
        r"resolution|quality|source_site|source-site|source|site|price|cost|no_cache|no-cache|nocache|cache|"
        r"关键词|关键字|查询|搜索词|输出|格式|市场|国家|地区|语言|开始|偏移|时长|时间|日期|"
        r"分辨率|清晰度|来源|网站|站点|价格|缓存"
    )
    pattern = re.compile(
        rf"(?P<key>{key_pattern})"
        r"\s*(?:=|:|：)\s*"
        r"(?P<value>\"[^\"]+\"|'[^']+'|[^,\n;，；。]+)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(prompt):
        key = normalize_key(match.group("key"))
        values[key] = strip_wrapping_quotes(match.group("value"))
    return values


def clean_query(query: str) -> str:
    query = strip_wrapping_quotes(query)
    query = re.sub(r"\s+", " ", query).strip(" ,.;，。；")
    query = re.sub(r"\s*(?:的)?(?:相关)?(?:视频|内容|信息|资料|结果)\s*$", "", query)
    return query.rstrip(". ")


def parse_query(prompt: str) -> str | None:
    patterns = [
        r"(?:search|find|look up|query|get|fetch|scrape|crawl)\s+(?:bing\s+)?(?:videos?\s+)?(?:for|about|of)?\s*[\"'](?P<q>[^\"']+)[\"']",
        r"(?:search|find|look up|query|get|fetch|scrape|crawl)\s+(?:bing\s+)?(?:videos?\s+)?(?:for|about|of)?\s*(?P<q>.+?)(?=\s+(?:from|on|site|source|with|using|return|mkt|cc|setlang|language|market|country|first|offset|json|html|short|medium|long|free|paid|past|last|today|resolution|no[_ -]?cache|skip cache|bypass cache)|$)",
        r"(?:搜索|查找|查询|搜一下|搜|检索|抓取|爬取)(?:必应|bing)?(?:视频)?(?:里)?(?:关于|有关|关键词为|关键字为)?[\"'“”]?(?P<q>.+?)(?=(?:，|,|。|；|;)?\s*(?:返回|输出|格式|JSON|HTML|短视频|中视频|长视频|过去|最近|近|今天|分辨率|清晰度|来源|网站|站点|免费|付费|跳过缓存|不要缓存|使用缓存|mkt|cc|setlang|first|json|length|date|resolution|source_site|price|no_cache)|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            query = clean_query(match.group("q"))
            if query:
                return query

    text = prompt.strip()
    if text and not parse_key_value_pairs(prompt):
        return clean_query(text)
    return None


def infer_output_format(prompt: str) -> str | None:
    text = prompt.lower().replace("＋", "+")
    compact = re.sub(r"\s+", "", text)
    if re.search(r"(json\s*(\+|and|和|与)\s*html|html\s*(\+|and|和|与)\s*json|both)", text) or "都要" in text:
        return "2"
    if re.search(r"(html only|return html|html format)", text) or "只要html" in compact or "返回html" in compact:
        return "3"
    if re.search(r"(json only|return json|json format)", text) or "只要json" in compact or "返回json" in compact:
        return "1"
    return None


def infer_no_cache(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(no_cache|no-cache|skip cache|bypass cache|refresh|fresh|实时|刷新|跳过缓存|不要缓存|不使用缓存)", text):
        return "true"
    if re.search(r"(use cache|cached|使用缓存)", text):
        return "false"
    return None


def infer_market(prompt: str) -> str | None:
    match = re.search(r"\b([a-z]{2})-([a-z]{2})\b", prompt, re.IGNORECASE)
    if match:
        language, country = match.group(1), match.group(2)
        return f"{language.lower()}-{country.upper()}"
    text = prompt.lower()
    for word, mkt in MARKET_WORDS.items():
        if word.lower() in text or word in prompt:
            return mkt
    return None


def infer_country(prompt: str) -> str | None:
    text = prompt.lower()
    match = re.search(r"\bcc\s*(?:=|:)\s*([a-z]{2})\b", text)
    if match:
        return match.group(1).lower()
    for word, cc in COUNTRY_WORDS.items():
        if word.lower() in text or word in prompt:
            return cc
    return None


def infer_setlang(prompt: str) -> str | None:
    text = prompt.lower()
    match = re.search(r"\bsetlang\s*(?:=|:)\s*([a-z]{2})\b", text)
    if match:
        return match.group(1).lower()
    for word, lang in LANGUAGE_WORDS.items():
        if word.lower() in text or word in prompt:
            return lang
    return None


def infer_first(prompt: str) -> str | None:
    patterns = [
        r"\bfirst\s*(?:=|:)?\s*(\d+)\b",
        r"\boffset\s*(?:=|:)?\s*(\d+)\b",
        r"(?:从第|第)\s*(\d+)\s*(?:条|个)?(?:开始)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def infer_length(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(short video|short videos|under\s*5|less than\s*5|<\s*5|短视频|少于\s*5|小于\s*5)", text):
        return "short"
    if re.search(r"(medium video|medium videos|5\s*[-~到至]\s*20|中视频|中等时长)", text):
        return "medium"
    if re.search(r"(long video|long videos|over\s*20|more than\s*20|>\s*20|长视频|超过\s*20|大于\s*20)", text):
        return "long"
    return None


def infer_date(prompt: str) -> str | None:
    text = prompt.lower()
    compact = re.sub(r"\s+", "", text)
    if "lt1440" in text or re.search(r"(past|last)\s*24\s*hours?", text) or any(word in compact for word in ["过去24小时", "最近24小时", "今天"]):
        return "lt1440"
    if "lt10080" in text or re.search(r"(past|last|this)\s*week", text) or any(word in compact for word in ["过去一周", "最近一周", "近一周"]):
        return "lt10080"
    if "lt43200" in text or re.search(r"(past|last|this)\s*month", text) or any(word in compact for word in ["过去一个月", "最近一个月", "近一个月"]):
        return "lt43200"
    if "lt525600" in text or re.search(r"(past|last|this)\s*year", text) or any(word in compact for word in ["过去一年", "最近一年", "近一年"]):
        return "lt525600"
    return None


def infer_resolution(prompt: str) -> str | None:
    text = prompt.lower().replace(" ", "")
    if any(word in text for word in ["lowerthan_360p", "below360p", "under360p", "低于360p", "小于360p"]):
        return "lowerthan_360p"
    for resolution in ["1080p", "720p", "480p", "360p"]:
        if resolution in text:
            return resolution
    if "fullhd" in text or "全高清" in text:
        return "1080p"
    if re.search(r"\bhd\b", prompt, re.IGNORECASE) or "高清" in prompt:
        return "720p"
    return None


def infer_source_site(prompt: str) -> str | None:
    text = prompt.lower()
    for name, domain in sorted(SOURCE_SITES.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(rf"(?<![a-z0-9.-]){re.escape(name)}(?![a-z0-9.-])", text):
            return domain
    return None


def infer_price(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"\bfree\b", text) or any(word in prompt for word in ["免费", "不要钱"]):
        return "free"
    if re.search(r"\bpaid\b|\bpay\b", text) or any(word in prompt for word in ["付费", "收费"]):
        return "paid"
    return None


def parse_prompt(prompt: str) -> dict[str, str]:
    values = parse_key_value_pairs(prompt)

    if "q" not in values:
        query = parse_query(prompt)
        if query:
            values["q"] = query

    values.setdefault("engine", "bing_videos")

    inference_steps = [
        ("json", infer_output_format),
        ("no_cache", infer_no_cache),
        ("mkt", infer_market),
        ("cc", infer_country),
        ("setlang", infer_setlang),
        ("first", infer_first),
        ("length", infer_length),
        ("date", infer_date),
        ("resolution", infer_resolution),
        ("source_site", infer_source_site),
        ("price", infer_price),
    ]
    for key, infer in inference_steps:
        if key not in values:
            value = infer(prompt)
            if value:
                values[key] = value

    return values


def apply_overrides(payload: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    for key in ["q", "json", "mkt", "cc", "setlang", "first", "length", "date", "resolution", "source_site", "price"]:
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

    cleaned["engine"] = "bing_videos"

    if not cleaned.get("q"):
        cleaned["q"] = "pizza"

    if "json" in cleaned:
        cleaned["json"] = normalize_json_format(cleaned["json"])
    else:
        cleaned["json"] = "1"

    if "no_cache" in cleaned:
        cleaned["no_cache"] = parse_bool(cleaned["no_cache"])
    else:
        cleaned["no_cache"] = "false"

    if "mkt" in cleaned:
        match = re.fullmatch(r"([a-z]{2})-([a-z]{2})", cleaned["mkt"], re.IGNORECASE)
        if not match:
            raise ValueError("mkt must look like en-US or zh-CN")
        cleaned["mkt"] = f"{match.group(1).lower()}-{match.group(2).upper()}"

    if "cc" in cleaned:
        if not re.fullmatch(r"[a-z]{2}", cleaned["cc"], re.IGNORECASE):
            raise ValueError("cc must be a two-letter country or region code")
        cleaned["cc"] = cleaned["cc"].lower()

    if "setlang" in cleaned:
        if not re.fullmatch(r"[a-z]{2}", cleaned["setlang"], re.IGNORECASE):
            raise ValueError("setlang must be a two-letter language code")
        cleaned["setlang"] = cleaned["setlang"].lower()

    if "first" in cleaned:
        first = int(cleaned["first"])
        if first < 1:
            raise ValueError("first must be greater than or equal to 1")
        cleaned["first"] = str(first)
    else:
        cleaned["first"] = "1"

    if "length" in cleaned:
        cleaned["length"] = normalize_length(cleaned["length"])

    if "date" in cleaned:
        cleaned["date"] = normalize_date(cleaned["date"])

    if "resolution" in cleaned:
        cleaned["resolution"] = normalize_resolution(cleaned["resolution"])

    if "source_site" in cleaned:
        cleaned["source_site"] = normalize_source_site(cleaned["source_site"])

    if "price" in cleaned:
        cleaned["price"] = normalize_price(cleaned["price"])

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
        "User-Agent": "codex-bing-videos-skill/1.0",
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
    parser = argparse.ArgumentParser(description="Parse and call the Dataify Bing Videos API.")
    parser.add_argument("--prompt", default="", help="Natural-language user request to parse.")
    parser.add_argument("--q", help="Video search query override.")
    parser.add_argument("--json", help="Output format: 1 JSON, 2 JSON plus HTML, 3 HTML.")
    parser.add_argument("--mkt", help="Market and language, such as zh-CN or en-US.")
    parser.add_argument("--cc", help="Two-letter country or region code.")
    parser.add_argument("--setlang", help="Two-letter search language.")
    parser.add_argument("--first", help="Organic result offset. No default is sent.")
    parser.add_argument("--length", help="Duration filter: short, medium, or long.")
    parser.add_argument("--date", help="Date filter: lt1440, lt10080, lt43200, or lt525600.")
    parser.add_argument("--resolution", help="Resolution filter: lowerthan_360p, 360p, 480p, 720p, or 1080p.")
    parser.add_argument("--source-site", "--source_site", dest="source_site", help="Source site filter.")
    parser.add_argument("--price", help="Price filter: free or paid.")
    parser.add_argument("--no-cache", "--no_cache", dest="no_cache", help="true to skip cache, false to use cache.")
    parser.add_argument("--field", action="append", help="Additional API field override as key=value.")
    parser.add_argument("--token", help="API token for this run. Bearer prefix is added when missing.")
    parser.add_argument("--body-format", choices=["form", "json"], default="form", help="POST body format.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print parsed payload and skip network/auth checks.")
    parser.add_argument("--table", action="store_true", help="With --dry-run, print a Markdown parameter table.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    try:
        payload = parse_prompt(args.prompt)
        payload = apply_overrides(payload, args)
        payload = validate_payload(payload)

        if args.dry_run:
            if args.table:
                print(format_parameter_table(payload))
                return 0
            print(as_json({"ok": True, "dry_run": True, "payload": payload}))
            return 0

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
