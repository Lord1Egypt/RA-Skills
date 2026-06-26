#!/usr/bin/env python3
"""Call the Dataify Bing News API after parsing natural-language requests."""

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
    "qft",
    "safeSearch",
    "no_cache",
}

DEFAULT_ENDPOINT = "https://scraperapi.dataify.com/request"

FIELD_DEFINITIONS = [
    {
        "name": "engine",
        "default": "bing_news",
        "description": "Bing 新闻接口标识。参数说明默认值为 bing_news。",
    },
    {
        "name": "q",
        "default": "pizza",
        "description": "新闻搜索关键词，可使用任意语言。参数说明默认值为 pizza。",
    },
    {
        "name": "json",
        "default": "1",
        "description": "采集结果输出格式：1 返回 JSON，2 返回 JSON+HTML，3 返回 HTML。参数说明默认 JSON，即 1。",
    },
    {
        "name": "mkt",
        "default": "",
        "description": "搜索结果界面显示语言，格式为 <语言代码>-<国家/地区代码>，例如 en-US。参数说明未给默认值。",
    },
    {
        "name": "cc",
        "default": "",
        "description": "按国家/地区用户习惯展示结果，使用两个字母的国家/地区代码。参数说明未给默认值。",
    },
    {
        "name": "first",
        "default": "1",
        "description": "自然结果偏移量。参数说明默认值为 1。",
    },
    {
        "name": "count",
        "default": "",
        "description": "每页结果数量建议值，实际返回数量可能不同。参数说明未给默认值。",
    },
    {
        "name": "qft",
        "default": "",
        "description": "按日期排序或过滤的 Bing 查询过滤字符串。参数说明未给默认值。",
    },
    {
        "name": "safeSearch",
        "default": "",
        "description": "成人内容过滤级别，可选 Off、Moderate、Strict。参数说明未给默认值。",
    },
    {
        "name": "no_cache",
        "default": "false",
        "description": "缓存行为：true 跳过缓存，false 使用缓存。参数说明默认 false。",
    },
]

DEFAULT_VALUES = {
    field["name"]: field["default"]
    for field in FIELD_DEFINITIONS
    if field["default"] != ""
}

COUNTRY_WORDS = {
    "china": "cn",
    "chinese": "cn",
    "中国": "cn",
    "国内": "cn",
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
    "korea": "kr",
    "south korea": "kr",
    "韩国": "kr",
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
    "简体中文": "zh-CN",
    "中国": "zh-CN",
    "english": "en-US",
    "us english": "en-US",
    "英文": "en-US",
    "英语": "en-US",
    "japanese": "ja-JP",
    "日文": "ja-JP",
    "日语": "ja-JP",
    "korean": "ko-KR",
    "韩文": "ko-KR",
    "韩语": "ko-KR",
    "french": "fr-FR",
    "法文": "fr-FR",
    "法语": "fr-FR",
    "german": "de-DE",
    "德文": "de-DE",
    "德语": "de-DE",
}


class MissingTokenError(ValueError):
    """Raised when Dataify authentication is unavailable."""


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def as_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def display_value(value: str | None) -> str:
    if value is None or value == "":
        return "(无)"
    return str(value)


def escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def build_parameter_rows(payload: dict[str, str]) -> list[dict[str, str]]:
    rows = []
    for field in FIELD_DEFINITIONS:
        name = field["name"]
        rows.append(
            {
                "参数名": name,
                "当前值": display_value(payload.get(name)),
                "默认值": display_value(field["default"]),
                "说明": field["description"],
            }
        )
    return rows


def format_parameter_table(payload: dict[str, str]) -> str:
    headers = ["参数名", "当前值", "默认值", "说明"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in build_parameter_rows(payload):
        lines.append(
            "| "
            + " | ".join(escape_markdown_cell(row[header]) for header in headers)
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
        "news": "q",
        "关键词": "q",
        "关键字": "q",
        "查询": "q",
        "搜索词": "q",
        "搜索": "q",
        "新闻": "q",
        "format": "json",
        "output": "json",
        "输出": "json",
        "格式": "json",
        "返回格式": "json",
        "market": "mkt",
        "language": "mkt",
        "locale": "mkt",
        "语言": "mkt",
        "市场": "mkt",
        "界面语言": "mkt",
        "country": "cc",
        "region": "cc",
        "地区": "cc",
        "国家": "cc",
        "offset": "first",
        "start": "first",
        "起始": "first",
        "开始": "first",
        "偏移": "first",
        "limit": "count",
        "size": "count",
        "number": "count",
        "count": "count",
        "数量": "count",
        "条数": "count",
        "结果数": "count",
        "date": "qft",
        "filter": "qft",
        "filters": "qft",
        "日期": "qft",
        "时间过滤": "qft",
        "排序": "qft",
        "safe": "safeSearch",
        "safe_search": "safeSearch",
        "safesearch": "safeSearch",
        "安全搜索": "safeSearch",
        "成人过滤": "safeSearch",
        "no_cache": "no_cache",
        "nocache": "no_cache",
        "cache": "no_cache",
        "缓存": "no_cache",
    }
    return aliases.get(lower_key, raw_key)


def parse_bool(value: str) -> str:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on", "skip", "bypass", "refresh", "fresh", "跳过", "不使用", "不要", "刷新", "开启"}:
        return "true"
    if text in {"0", "false", "no", "n", "off", "use", "cached", "使用", "关闭"}:
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
        "仅json": "1",
        "2": "2",
        "json+html": "2",
        "json + html": "2",
        "html+json": "2",
        "html + json": "2",
        "json和html": "2",
        "json html": "2",
        "3": "3",
        "html": "3",
        "html only": "3",
        "只要html": "3",
        "仅html": "3",
    }
    if text in mapping:
        return mapping[text]
    if "json" in text and "html" in text:
        return "2"
    if "html" in text and "json" not in text:
        return "3"
    if "json" in text:
        return "1"
    raise ValueError(f"Invalid json output format: {value!r}")


def normalize_safe_search(value: str) -> str:
    text = value.strip().lower()
    mapping = {
        "off": "Off",
        "false": "Off",
        "0": "Off",
        "none": "Off",
        "关闭": "Off",
        "不过滤": "Off",
        "不限制": "Off",
        "moderate": "Moderate",
        "medium": "Moderate",
        "中等": "Moderate",
        "适中": "Moderate",
        "strict": "Strict",
        "high": "Strict",
        "严格": "Strict",
        "强": "Strict",
    }
    if text in mapping:
        return mapping[text]
    for value_name in ("Off", "Moderate", "Strict"):
        if text == value_name.lower():
            return value_name
    raise ValueError("safeSearch must be Off, Moderate, or Strict")


def parse_key_value_pairs(prompt: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(r"([\w\u4e00-\u9fff-]+)\s*(?:=|:|：)\s*([^,，;\n]+)")
    for match in pattern.finditer(prompt):
        key = normalize_key(match.group(1))
        if key not in SUPPORTED_FIELDS:
            continue
        values[key] = strip_wrapping_quotes(match.group(2))
    return values


def remove_key_value_pairs(prompt: str) -> str:
    return re.sub(r"[\w\u4e00-\u9fff-]+\s*(?:=|:|：)\s*[^,，;\n]+", " ", prompt)


def clean_query_candidate(text: str) -> str:
    text = remove_key_value_pairs(text)
    replacements = [
        r"\b(?:search|find|fetch|get|look up|run)\b",
        r"\b(?:bing|news|bing news)\b",
        r"\b(?:for|about|on|with|in|from)\b",
        r"\b(?:return|output|format|json|html|and)\b",
        r"\b(?:safe search|strict|moderate|off|cache|cached|fresh|refresh|results?)\b",
        r"(?:搜索|查询|查找|查一下|搜一下|获取|抓取|运行|调用)",
        r"(?:必应|Bing|新闻|资讯)",
        r"(?:关于|有关|返回|输出|格式|结果|安全搜索|严格|中等|关闭|缓存|跳过缓存|不使用缓存)",
        r"(?:JSON|HTML|json|html)",
        r"\b(?:mkt|cc|first|count|qft|safeSearch|no_cache)\b",
        r"\d+\s*(?:条|个|篇|results?)",
    ]
    for pattern in replacements:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[，,。.;；、]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return strip_wrapping_quotes(text)


def parse_query(prompt: str) -> str | None:
    patterns = [
        r"(?:搜索|查询|查找|查一下|搜一下|获取|抓取)(?:\s*必应)?(?:\s*新闻|\s*资讯)?(?:\s*(?:关于|有关))?\s*([^,，。；;\n]+)",
        r"(?:search|find|fetch|get|look up|run)(?:\s+bing)?(?:\s+news)?(?:\s+(?:for|about|on))?\s+([^,;\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, flags=re.IGNORECASE)
        if match:
            candidate = clean_query_candidate(match.group(1))
            if candidate:
                return candidate

    candidate = clean_query_candidate(prompt)
    return candidate or None


def infer_output_format(prompt: str) -> str | None:
    lowered = prompt.lower()
    compact = re.sub(r"\s+", "", lowered)
    if "json+html" in compact or "html+json" in compact or ("json" in lowered and "html" in lowered) or "json和html" in compact:
        return "2"
    if re.search(r"(?:html only|only html|只要\s*html|仅\s*html|返回\s*html|html格式)", prompt, re.IGNORECASE):
        return "3"
    if re.search(r"(?:json only|only json|只要\s*json|仅\s*json|返回\s*json|json格式)", prompt, re.IGNORECASE):
        return "1"
    return None


def infer_no_cache(prompt: str) -> str | None:
    if re.search(r"(?:no[_ -]?cache|bypass cache|skip cache|fresh|refresh|跳过缓存|不使用缓存|不要缓存|刷新)", prompt, re.IGNORECASE):
        return "true"
    if re.search(r"(?:use cache|cached|使用缓存|走缓存)", prompt, re.IGNORECASE):
        return "false"
    return None


def infer_market(prompt: str) -> str | None:
    match = re.search(r"\b([a-z]{2})-([a-z]{2})\b", prompt, re.IGNORECASE)
    if match:
        return f"{match.group(1).lower()}-{match.group(2).upper()}"
    lowered = prompt.lower()
    for word, value in MARKET_WORDS.items():
        if word.lower() in lowered or word in prompt:
            return value
    return None


def infer_country(prompt: str) -> str | None:
    match = re.search(r"\bcc\s*(?:=|:)?\s*([a-z]{2})\b", prompt, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    lowered = prompt.lower()
    for word, value in COUNTRY_WORDS.items():
        if word.lower() in lowered or word in prompt:
            return value
    return None


def infer_first(prompt: str) -> str | None:
    patterns = [
        r"\bfirst\s*(?:=|:)?\s*(\d+)\b",
        r"\boffset\s*(?:=|:)?\s*(\d+)\b",
        r"\bstart\s*(?:=|:)?\s*(\d+)\b",
        r"(?:从第|第)\s*(\d+)\s*(?:条|个|篇)?\s*(?:开始|起)",
        r"(?:偏移|起始|开始)\s*(?:=|:|：)?\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def infer_count(prompt: str) -> str | None:
    patterns = [
        r"\bcount\s*(?:=|:)?\s*(\d+)\b",
        r"\blimit\s*(?:=|:)?\s*(\d+)\b",
        r"(\d+)\s*(?:条|个|篇)\s*(?:新闻|资讯|结果)?",
        r"(\d+)\s*results?\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def infer_qft(prompt: str) -> str | None:
    match = re.search(r"\bqft\s*(?:=|:)\s*([^,，;\n]+)", prompt, re.IGNORECASE)
    if match:
        return strip_wrapping_quotes(match.group(1))
    return None


def infer_safe_search(prompt: str) -> str | None:
    if re.search(r"(?:strict safe|safeSearch\s*[:=]\s*strict|严格)", prompt, re.IGNORECASE):
        return "Strict"
    if re.search(r"(?:moderate safe|safeSearch\s*[:=]\s*moderate|中等|适中)", prompt, re.IGNORECASE):
        return "Moderate"
    if re.search(r"(?:safeSearch\s*[:=]\s*off|turn off safe|disable safe|关闭安全|不过滤|不限制)", prompt, re.IGNORECASE):
        return "Off"
    return None


def extract_token(prompt: str) -> str | None:
    match = re.search(
        r"(?:DATAIFY_API_TOKEN|api[_ -]?token|token|令牌|密钥)\s*(?:=|:|：|是|为)\s*((?:Bearer\s+)?[A-Za-z0-9._~+/=-]+)",
        prompt,
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def parse_prompt(prompt: str) -> dict[str, str]:
    values = parse_key_value_pairs(prompt)

    if "q" not in values:
        query = parse_query(prompt)
        if query:
            values["q"] = query

    values.setdefault("engine", DEFAULT_VALUES["engine"])

    inference_steps = [
        ("json", infer_output_format),
        ("no_cache", infer_no_cache),
        ("mkt", infer_market),
        ("cc", infer_country),
        ("first", infer_first),
        ("count", infer_count),
        ("qft", infer_qft),
        ("safeSearch", infer_safe_search),
    ]
    for key, infer in inference_steps:
        if key not in values:
            value = infer(prompt)
            if value:
                values[key] = value

    return values


def apply_overrides(payload: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    for key in ["q", "json", "mkt", "cc", "first", "count", "qft", "safeSearch"]:
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

    for key, value in DEFAULT_VALUES.items():
        cleaned.setdefault(key, value)

    cleaned["engine"] = DEFAULT_VALUES["engine"]

    if not cleaned.get("q"):
        raise ValueError("Missing required field q. Provide --q or a prompt with a Bing news search query.")

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

    if "safeSearch" in cleaned:
        cleaned["safeSearch"] = normalize_safe_search(cleaned["safeSearch"])

    return cleaned


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.getenv("DATAIFY_API_TOKEN") or extract_token(args.prompt)
    if not token:
        raise MissingTokenError(
            "缺少 DATAIFY_API_TOKEN。请提供 Dataify API token，或访问 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"
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
        "User-Agent": "codex-bing-news-skill/1.0",
    }

    if body_format == "json":
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
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
    parser = argparse.ArgumentParser(description="Parse and call the Dataify Bing News API.")
    parser.add_argument("--prompt", default="", help="Natural-language user request to parse.")
    parser.add_argument("--q", help="News search query override.")
    parser.add_argument("--json", help="Output format: 1 JSON, 2 JSON plus HTML, 3 HTML.")
    parser.add_argument("--mkt", help="Market and language, such as zh-CN or en-US.")
    parser.add_argument("--cc", help="Two-letter country or region code.")
    parser.add_argument("--first", help="Result offset.")
    parser.add_argument("--count", help="Requested result count.")
    parser.add_argument("--qft", help="Bing qft date/filter string.")
    parser.add_argument("--safeSearch", "--safe-search", dest="safeSearch", help="Off, Moderate, or Strict.")
    parser.add_argument("--no-cache", "--no_cache", dest="no_cache", help="true to skip cache, false to use cache.")
    parser.add_argument("--field", action="append", help="Additional API field override as key=value.")
    parser.add_argument("--token", help="API token for this run. Bearer prefix is added when missing.")
    parser.add_argument("--body-format", choices=["form", "json"], default="form", help="POST body format.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds.")
    parser.add_argument("--preview", action="store_true", help="Print the full parameter confirmation table and skip network/auth checks.")
    parser.add_argument("--dry-run", action="store_true", help="Print parsed payload and skip network/auth checks.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    try:
        payload = parse_prompt(args.prompt)
        payload = apply_overrides(payload, args)
        payload = validate_payload(payload)

        if args.preview:
            print(format_parameter_table(payload))
            return 0

        if args.dry_run:
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
