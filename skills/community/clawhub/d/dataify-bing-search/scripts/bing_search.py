#!/usr/bin/env python3
"""Call the Dataify Bing Search API after parsing natural-language requests."""

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
    "location",
    "lat",
    "lon",
    "mkt",
    "cc",
    "first",
    "safeSearch",
    "filters",
    "no_cache",
}

DEFAULT_ENDPOINT = "https://scraperapi.dataify.com/request"


FIELD_SPECS = [
    {
        "name": "engine",
        "default": "bing",
        "description": "Bing搜索；参数说明中的默认值为 bing。",
    },
    {
        "name": "q",
        "default": "pizza",
        "description": "搜索关键词，可以是任意语言；参数说明中的默认值为 pizza。",
    },
    {
        "name": "json",
        "default": "1",
        "description": "输出格式：1 返回 JSON，2 返回 JSON+HTML，3 返回 HTML；参数说明中的默认值为 JSON。",
    },
    {
        "name": "location",
        "default": None,
        "description": "搜索发起的地理位置；参数说明未给默认值。",
    },
    {
        "name": "lat",
        "default": None,
        "description": "搜索起点 GPS 纬度；参数说明未给默认值。",
    },
    {
        "name": "lon",
        "default": None,
        "description": "搜索起点 GPS 经度；参数说明未给默认值。",
    },
    {
        "name": "mkt",
        "default": None,
        "description": "搜索结果界面显示语言，格式为 <语言代码>-<国家/地区代码>；参数说明未给默认值。",
    },
    {
        "name": "cc",
        "default": None,
        "description": "按国家/地区用户习惯展示结果的两字母国家/地区代码；参数说明未给默认值。",
    },
    {
        "name": "first",
        "default": "1",
        "description": "自然结果偏移量；参数说明中的默认值为 1。",
    },
    {
        "name": "safeSearch",
        "default": None,
        "description": "成人内容过滤级别，可为 Off、Moderate、Strict；参数说明未给默认值。",
    },
    {
        "name": "filters",
        "default": None,
        "description": "高级过滤选项，例如日期范围或显示过滤器；参数说明未给默认值。",
    },
    {
        "name": "no_cache",
        "default": "false",
        "description": "true 跳过缓存，false 使用缓存；参数说明中的默认值为 false。",
    },
]


COUNTRY_WORDS = {
    "china": "cn",
    "chinese": "cn",
    "us": "us",
    "usa": "us",
    "united states": "us",
    "america": "us",
    "uk": "uk",
    "united kingdom": "uk",
    "japan": "jp",
    "india": "in",
    "france": "fr",
    "germany": "de",
    "russia": "ru",
    "canada": "ca",
    "australia": "au",
}


MARKET_WORDS = {
    "chinese": "zh-CN",
    "china": "zh-CN",
    "simplified chinese": "zh-CN",
    "english": "en-US",
    "us english": "en-US",
    "japanese": "ja-JP",
    "french": "fr-FR",
    "german": "de-DE",
}


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def as_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def default_payload() -> dict[str, str]:
    return {
        spec["name"]: spec["default"]
        for spec in FIELD_SPECS
        if spec["default"] is not None
    }


def format_value(value: str | None) -> str:
    if value is None or value == "":
        return "无"
    return value


def markdown_param_table(payload: dict[str, str]) -> str:
    lines = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "|---|---|---|---|",
    ]
    for spec in FIELD_SPECS:
        name = spec["name"]
        lines.append(
            f"| `{name}` | {format_value(payload.get(name))} | "
            f"{format_value(spec['default'])} | {spec['description']} |"
        )
    return "\n".join(lines)


def normalize_key(key: str) -> str:
    raw_key = key.strip()
    lower_key = raw_key.lower()
    aliases = {
        "query": "q",
        "keyword": "q",
        "keywords": "q",
        "format": "json",
        "output": "json",
        "market": "mkt",
        "country": "cc",
        "safe": "safeSearch",
        "safesearch": "safeSearch",
        "safe_search": "safeSearch",
        "no-cache": "no_cache",
        "nocache": "no_cache",
    }
    if raw_key == "safeSearch":
        return "safeSearch"
    return aliases.get(lower_key, raw_key)


def parse_bool(value: str) -> str:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on", "skip", "bypass", "refresh"}:
        return "true"
    if text in {"0", "false", "no", "n", "off", "use"}:
        return "false"
    raise ValueError(f"Invalid boolean value for no_cache: {value!r}")


def normalize_json_format(value: str) -> str:
    text = value.strip().lower()
    mapping = {
        "1": "1",
        "json": "1",
        "json only": "1",
        "2": "2",
        "json+html": "2",
        "json and html": "2",
        "html+json": "2",
        "both": "2",
        "3": "3",
        "html": "3",
        "html only": "3",
    }
    if text in mapping:
        return mapping[text]
    raise ValueError("json must be 1, 2, 3, JSON, HTML, or JSON+HTML")


def normalize_safe_search(value: str) -> str:
    text = value.strip().lower()
    mapping = {
        "off": "Off",
        "none": "Off",
        "false": "Off",
        "moderate": "Moderate",
        "medium": "Moderate",
        "strict": "Strict",
        "high": "Strict",
        "on": "Strict",
        "true": "Strict",
    }
    if text in mapping:
        return mapping[text]
    raise ValueError("safeSearch must be Off, Moderate, or Strict")


def strip_wrapping_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    return value


def parse_key_value_pairs(prompt: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(
        r"(?P<key>engine|q|query|json|format|output|location|lat|lon|mkt|market|cc|country|first|safeSearch|safe_search|safe|filters|no_cache|no-cache|nocache)"
        r"\s*(?:=|:)\s*"
        r"(?P<value>\"[^\"]+\"|'[^']+'|[^,\n;]+)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(prompt):
        key = normalize_key(match.group("key"))
        values[key] = strip_wrapping_quotes(match.group("value"))
    return values


def parse_query(prompt: str) -> str | None:
    patterns = [
        r"(?:search|find|look up|query)\s+(?:bing\s+)?(?:for\s+)?[\"'](?P<q>[^\"']+)[\"']",
        r"(?:search|find|look up|query)\s+(?:bing\s+)?(?:for\s+)?(?P<q>.+?)(?:\s+(?:from|near|location|in|with|using|return|mkt=|cc=|safe|json|html|lat=|lon=|first=)|$)",
        r"(?:搜索|查找|查询|搜一下|检索|抓取|爬取)(?:必应|bing)?[\"'“”]?(?P<q>[^\"'“”，,。]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            query = match.group("q").strip()
            query = re.sub(r"\s+", " ", query)
            query = re.sub(r"\s*(?:的)?(?:相关)?(?:内容|信息|资料|结果)\s*$", "", query)
            return query.rstrip(".,;，。； ")
    text = prompt.strip()
    if text and not parse_key_value_pairs(prompt):
        return text
    return None


def infer_output_format(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(json\s*(\+|and)\s*html|html\s*(\+|and)\s*json|both)", text):
        return "2"
    if re.search(r"(html only|return html|html format|只要\s*html|返回\s*html)", text):
        return "3"
    if re.search(r"(json only|return json|json format|只要\s*json|返回\s*json)", text):
        return "1"
    return None


def infer_safe_search(prompt: str) -> str | None:
    text = prompt.lower()
    if "safesearch" not in text and "safe search" not in text and "安全搜索" not in prompt:
        return None
    if re.search(r"(strict|high|on|严格|开启)", text):
        return "Strict"
    if re.search(r"(moderate|medium|中等|适中)", text):
        return "Moderate"
    if re.search(r"(off|none|关闭|不要|不启用)", text):
        return "Off"
    return None


def infer_no_cache(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(no_cache|no-cache|skip cache|bypass cache|refresh|fresh|实时|刷新|跳过缓存|不要缓存)", text):
        return "true"
    if re.search(r"(use cache|cached|使用缓存)", text):
        return "false"
    return None


def infer_location(prompt: str) -> str | None:
    patterns = [
        r"\b(?:location|from|near)\b\s*[:=]?\s*([A-Za-z][A-Za-z ._-]{1,40})",
        r"(?:位置|地点|地区)\s*[:=：]?\s*([\u4e00-\u9fffA-Za-z ._-]{1,40})",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            value = match.group(1).strip(" ,.;")
            value = re.split(r"\s+(?:mkt|cc|first|safe|json|html|lat|lon)\s*[=:]?", value, maxsplit=1, flags=re.IGNORECASE)[0]
            if value and not re.fullmatch(r"[a-z]{2}-[a-z]{2}", value, re.IGNORECASE):
                return value
    return None


def infer_market(prompt: str) -> str | None:
    match = re.search(r"\b([a-z]{2}-[a-z]{2})\b", prompt, re.IGNORECASE)
    if match:
        language, country = match.group(1).split("-", 1)
        return f"{language.lower()}-{country.upper()}"
    text = prompt.lower()
    for word, mkt in MARKET_WORDS.items():
        if word in text:
            return mkt
    return None


def infer_country(prompt: str) -> str | None:
    text = prompt.lower()
    match = re.search(r"\bcc\s*(?:=|:)\s*([a-z]{2})\b", text)
    if match:
        return match.group(1).lower()
    for word, cc in COUNTRY_WORDS.items():
        if word in text:
            return cc
    return None


def infer_lat_lon(prompt: str) -> tuple[str | None, str | None]:
    lat = None
    lon = None
    lat_match = re.search(r"\blat(?:itude)?\s*(?:=|:)?\s*(-?\d+(?:\.\d+)?)", prompt, re.IGNORECASE)
    lon_match = re.search(r"\b(?:lon|lng|longitude)\s*(?:=|:)?\s*(-?\d+(?:\.\d+)?)", prompt, re.IGNORECASE)
    if lat_match:
        lat = lat_match.group(1)
    if lon_match:
        lon = lon_match.group(1)
    return lat, lon


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


def parse_prompt(prompt: str) -> dict[str, str]:
    values = default_payload()
    values.update(parse_key_value_pairs(prompt))

    if "q" not in values:
        query = parse_query(prompt)
        if query:
            values["q"] = query
    else:
        query = parse_query(prompt)
        if query and values.get("q") == "pizza":
            values["q"] = query

    values["engine"] = "bing"

    inferred_json = infer_output_format(prompt)
    if inferred_json and "json" not in values:
        values["json"] = inferred_json

    inferred_safe = infer_safe_search(prompt)
    if inferred_safe and "safeSearch" not in values:
        values["safeSearch"] = inferred_safe

    inferred_no_cache = infer_no_cache(prompt)
    if inferred_no_cache and "no_cache" not in values:
        values["no_cache"] = inferred_no_cache

    inferred_location = infer_location(prompt)
    if inferred_location and "location" not in values:
        values["location"] = inferred_location

    inferred_market = infer_market(prompt)
    if inferred_market and "mkt" not in values:
        values["mkt"] = inferred_market

    inferred_country = infer_country(prompt)
    if inferred_country and "cc" not in values:
        values["cc"] = inferred_country

    lat, lon = infer_lat_lon(prompt)
    if lat and "lat" not in values:
        values["lat"] = lat
    if lon and "lon" not in values:
        values["lon"] = lon

    first = infer_first(prompt)
    if first and "first" not in values:
        values["first"] = first

    return values


def apply_overrides(payload: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    for key in ["q", "json", "location", "lat", "lon", "mkt", "cc", "first", "safeSearch", "filters"]:
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

    cleaned["engine"] = "bing"

    if not cleaned.get("q"):
        raise ValueError("Missing required field q. Provide --q or a prompt with a search query.")

    if "json" in cleaned:
        cleaned["json"] = normalize_json_format(cleaned["json"])
    else:
        cleaned["json"] = "1"

    if "safeSearch" in cleaned:
        cleaned["safeSearch"] = normalize_safe_search(cleaned["safeSearch"])

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

    for key, low, high in [("lat", -90.0, 90.0), ("lon", -180.0, 180.0)]:
        if key in cleaned:
            number = float(cleaned[key])
            if number < low or number > high:
                raise ValueError(f"{key} must be between {low:g} and {high:g}")

    return cleaned


def resolve_url(args: argparse.Namespace) -> str:
    if args.url:
        return args.url
    return DEFAULT_ENDPOINT


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.getenv("DATAIFY_API_TOKEN")
    if not token:
        raise ValueError(
            "缺少 DATAIFY_API_TOKEN。请提供 --token，或设置 DATAIFY_API_TOKEN，"
            "或访问 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"
        )
    token = token.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def call_api(url: str, token: str, payload: dict[str, str], body_format: str, timeout: float) -> tuple[bool, str]:
    headers = {
        "Authorization": token,
        "Accept": "application/json, text/plain;q=0.9, */*;q=0.8",
        "User-Agent": "codex-bing-search-skill/1.0",
    }

    if body_format == "json":
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    else:
        data = urllib.parse.urlencode(payload).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
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
    parser = argparse.ArgumentParser(description="Parse and call the Dataify Bing Search API.")
    parser.add_argument("--prompt", default="", help="Natural-language user request to parse.")
    parser.add_argument("--q", help="Search query override.")
    parser.add_argument("--json", help="Output format: 1 JSON, 2 JSON plus HTML, 3 HTML.")
    parser.add_argument("--location", help="Named geographic search origin.")
    parser.add_argument("--lat", help="GPS latitude.")
    parser.add_argument("--lon", help="GPS longitude.")
    parser.add_argument("--mkt", help="Market and language, such as zh-CN or en-US.")
    parser.add_argument("--cc", help="Two-letter country or region code.")
    parser.add_argument("--first", help="Organic result offset.")
    parser.add_argument("--safeSearch", help="Safe search level: Off, Moderate, or Strict.")
    parser.add_argument("--filters", help="Advanced Bing filter string.")
    parser.add_argument("--no-cache", dest="no_cache", help="true to skip cache, false to use cache.")
    parser.add_argument("--field", action="append", help="Additional API field override as key=value.")
    parser.add_argument("--url", help="Full API endpoint override. Defaults to the hard-coded Dataify endpoint.")
    parser.add_argument("--token", help="API token for this run. Bearer prefix is added when missing.")
    parser.add_argument("--body-format", choices=["form", "json"], default="form", help="POST body format.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print parsed payload and skip network/auth checks.")
    parser.add_argument("--show-params", action="store_true", help="Print the full request parameter table and exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    try:
        payload = parse_prompt(args.prompt)
        payload = apply_overrides(payload, args)
        payload = validate_payload(payload)

        result: dict[str, Any] = {
            "ok": True,
            "dry_run": bool(args.dry_run),
            "payload": payload,
        }

        if args.show_params:
            print(markdown_param_table(payload))
            return 0

        if args.dry_run:
            print(as_json(result))
            return 0

        url = resolve_url(args)
        token = resolve_token(args)
        ok, response_text = call_api(url, token, payload, args.body_format, args.timeout)
        sys.stdout.write(response_text)
        if response_text and not response_text.endswith("\n"):
            sys.stdout.write("\n")
        return 0 if ok else 2
    except Exception as exc:
        error = {
            "ok": False,
            "error": str(exc),
        }
        eprint(as_json(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
