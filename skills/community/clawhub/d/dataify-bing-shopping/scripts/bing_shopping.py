#!/usr/bin/env python3
"""Call the Dataify Bing Shopping API after parsing natural-language requests."""

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
    "efirst",
    "filters",
    "no_cache",
}

DEFAULT_ENDPOINT = "https://scraperapi.dataify.com/request"

FIELD_ORDER = [
    "engine",
    "q",
    "json",
    "mkt",
    "cc",
    "efirst",
    "filters",
    "no_cache",
]

FIELD_DEFAULTS: dict[str, str | None] = {
    "engine": "bing_shopping",
    "q": None,
    "json": "1",
    "mkt": None,
    "cc": None,
    "efirst": None,
    "filters": None,
    "no_cache": "false",
}

FIELD_DESCRIPTIONS = {
    "engine": "Bing Shopping 引擎，固定为 bing_shopping。",
    "q": "购物搜索关键词，来自用户请求。必填；不要把示例关键词当作默认值。",
    "json": "输出格式：1 返回 JSON，2 返回 JSON 和 HTML，3 返回 HTML。",
    "mkt": "界面显示语言和市场，格式为 语言-国家/地区，例如 zh-CN 或 en-US。",
    "cc": "两位国家/地区代码，用于按指定地区展示购物结果。",
    "efirst": "购物结果偏移量。",
    "filters": "高级 Bing 过滤字符串，可从 Bing 搜索 URL 复制或按需要构造。",
    "no_cache": "缓存行为：true 跳过缓存；false 在可用时使用缓存结果。",
}


COUNTRY_WORDS = {
    "us": "us",
    "usa": "us",
    "united states": "us",
    "america": "us",
    "american": "us",
    "美国": "us",
    "cn": "cn",
    "china": "cn",
    "chinese": "cn",
    "中国": "cn",
    "uk": "uk",
    "gb": "uk",
    "united kingdom": "uk",
    "britain": "uk",
    "英国": "uk",
    "jp": "jp",
    "japan": "jp",
    "japanese": "jp",
    "日本": "jp",
    "in": "in",
    "india": "in",
    "印度": "in",
    "de": "de",
    "germany": "de",
    "german": "de",
    "德国": "de",
    "fr": "fr",
    "france": "fr",
    "french": "fr",
    "法国": "fr",
    "ca": "ca",
    "canada": "ca",
    "加拿大": "ca",
    "au": "au",
    "australia": "au",
    "澳大利亚": "au",
    "ru": "ru",
    "russia": "ru",
    "俄罗斯": "ru",
}


MARKET_WORDS = {
    "zh-cn": "zh-CN",
    "simplified chinese": "zh-CN",
    "chinese": "zh-CN",
    "china": "zh-CN",
    "中文": "zh-CN",
    "中国": "zh-CN",
    "en-us": "en-US",
    "english": "en-US",
    "us english": "en-US",
    "美国英语": "en-US",
    "ja-jp": "ja-JP",
    "japanese": "ja-JP",
    "日本语": "ja-JP",
    "fr-fr": "fr-FR",
    "french": "fr-FR",
    "de-de": "de-DE",
    "german": "de-DE",
}


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def as_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def normalize_key(key: str) -> str:
    raw_key = key.strip()
    lower_key = raw_key.lower().replace("-", "_")
    aliases = {
        "query": "q",
        "keyword": "q",
        "keywords": "q",
        "search": "q",
        "product": "q",
        "format": "json",
        "output": "json",
        "market": "mkt",
        "locale": "mkt",
        "language": "mkt",
        "lang": "mkt",
        "country": "cc",
        "region": "cc",
        "offset": "efirst",
        "first": "efirst",
        "start": "efirst",
        "shopping_offset": "efirst",
        "filter": "filters",
        "no_cache": "no_cache",
        "nocache": "no_cache",
    }
    return aliases.get(lower_key, raw_key)


def strip_wrapping_quotes(value: str) -> str:
    value = value.strip()
    quote_pairs = {
        '"': '"',
        "'": "'",
        "“": "”",
        "‘": "’",
        "「": "」",
        "『": "』",
    }
    if len(value) >= 2 and value[0] in quote_pairs and value[-1] == quote_pairs[value[0]]:
        return value[1:-1].strip()
    return value


def parse_bool(value: str) -> str:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on", "skip", "bypass", "refresh", "fresh"}:
        return "true"
    if text in {"0", "false", "no", "n", "off", "use", "cached"}:
        return "false"
    raise ValueError(f"Invalid boolean value for no_cache: {value!r}")


def display_value(value: str | None) -> str:
    if value is None or value == "":
        return ""
    return str(value)


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def build_parameter_table(payload: dict[str, str]) -> str:
    rows = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "|---|---|---|---|",
    ]
    for key in FIELD_ORDER:
        current = display_value(payload.get(key))
        default = display_value(FIELD_DEFAULTS.get(key))
        description = FIELD_DESCRIPTIONS[key]
        rows.append(
            "| "
            + " | ".join(
                markdown_escape(item)
                for item in [key, current, default, description]
            )
            + " |"
        )
    return "\n".join(rows)


def normalize_json_format(value: str) -> str:
    text = re.sub(r"\s+", "", value.strip().lower())
    mapping = {
        "1": "1",
        "json": "1",
        "jsononly": "1",
        "只要json": "1",
        "只返回json": "1",
        "返回json": "1",
        "2": "2",
        "json+html": "2",
        "html+json": "2",
        "jsonandhtml": "2",
        "htmlandjson": "2",
        "json和html": "2",
        "html和json": "2",
        "both": "2",
        "全部": "2",
        "都要": "2",
        "3": "3",
        "html": "3",
        "htmlonly": "3",
        "只要html": "3",
        "只返回html": "3",
        "返回html": "3",
    }
    if text in mapping:
        return mapping[text]
    raise ValueError("json must be 1, 2, 3, JSON, HTML, or JSON+HTML")


def parse_key_value_pairs(prompt: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(
        r"(?P<key>engine|q|query|keyword|keywords|search|product|json|format|output|mkt|market|locale|language|lang|cc|country|region|efirst|offset|first|start|shopping_offset|filters|filter|no_cache|no-cache|nocache)"
        r"\s*(?:=|:|：)\s*"
        r"(?P<value>\"[^\"]+\"|'[^']+'|“[^”]+”|‘[^’]+’|[^,\n;，；]+)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(prompt):
        key = normalize_key(match.group("key"))
        values[key] = strip_wrapping_quotes(match.group("value"))
    return values


def trim_query(query: str) -> str:
    query = re.sub(r"\s+", " ", query).strip()
    query = re.sub(r"\s*(?:的)?(?:商品|购物结果|产品|结果|信息|资料)\s*$", "", query)
    query = re.split(
        r"\s+(?:in|from|for|with|using|return|output)\b|[,，;；]\s*(?:mkt|cc|json|efirst|filters|no_cache)\s*(?:=|:|：)",
        query,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    query = re.split(r"(?:，|,)?\s*(?:返回|输出|使用|市场|国家|地区|偏移|过滤|筛选|缓存)", query, maxsplit=1)[0]
    return query.strip(" .。")


def parse_query(prompt: str) -> str | None:
    patterns = [
        r"(?:bing\s+shopping|shopping)\s+(?:search|find|look up|query|shop)\s+(?:for\s+)?[\"“](?P<q>[^\"”]+)[\"”]",
        r"(?:search|find|look up|query|shop)\s+(?:bing\s+shopping\s+)?(?:for\s+)?[\"“](?P<q>[^\"”]+)[\"”]",
        r"(?:bing\s+shopping|shopping)\s+(?:search|find|look up|query|shop)\s+(?:for\s+)?(?P<q>.+?)(?:\s+(?:in|from|with|using|return|output|mkt=|cc=|json=|efirst=|filters=|no_cache=)|$)",
        r"(?:search|find|look up|query|shop)\s+(?:bing\s+shopping\s+)?(?:for\s+)?(?P<q>.+?)(?:\s+(?:in|from|with|using|return|output|mkt=|cc=|json=|efirst=|filters=|no_cache=)|$)",
        r"(?:搜索|查找|查询|搜一下|搜|抓取|爬取)(?:必应购物|Bing购物|bing shopping|购物)?[\"“']?(?P<q>[^\"”'，,。；;]+)",
        r"(?:在)?(?:必应购物|Bing购物|bing shopping)\s*(?:搜索|查找|查询|搜一下|搜)?[\"“']?(?P<q>[^\"”'，,。；;]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            query = trim_query(match.group("q"))
            if query:
                return query

    text = prompt.strip()
    if text and not parse_key_value_pairs(prompt):
        return trim_query(text)
    return None


def infer_output_format(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(json\s*(\+|and|和)\s*html|html\s*(\+|and|和)\s*json|both|都要|全部)", text):
        return "2"
    if re.search(r"(html only|return html|html format|只要\s*html|只返回\s*html|返回\s*html|输出\s*html)", text):
        return "3"
    if re.search(r"(json only|return json|json format|只要\s*json|只返回\s*json|返回\s*json|输出\s*json)", text):
        return "1"
    return None


def infer_no_cache(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(no_cache|no-cache|skip cache|bypass cache|refresh|fresh|实时|刷新|跳过缓存|不要缓存|不使用缓存)", text):
        return "true"
    if re.search(r"(use cache|cached|使用缓存|走缓存)", text):
        return "false"
    return None


def normalize_market(value: str) -> str:
    text = value.strip()
    lower_text = text.lower()
    if lower_text in MARKET_WORDS:
        return MARKET_WORDS[lower_text]
    match = re.fullmatch(r"([a-z]{2})-([a-z]{2})", text, re.IGNORECASE)
    if not match:
        raise ValueError("mkt must look like en-US or zh-CN")
    return f"{match.group(1).lower()}-{match.group(2).upper()}"


def infer_market(prompt: str) -> str | None:
    explicit = re.search(r"\b(?:mkt|market|locale|language|lang)\s*(?:=|:|：)?\s*([a-z]{2}-[a-z]{2})\b", prompt, re.IGNORECASE)
    if explicit:
        return normalize_market(explicit.group(1))

    match = re.search(r"\b([a-z]{2}-[a-z]{2})\b", prompt, re.IGNORECASE)
    if match:
        return normalize_market(match.group(1))

    text = prompt.lower()
    if re.search(r"(market|locale|language|lang|语言|市场|界面)", text):
        for word, mkt in MARKET_WORDS.items():
            if word in text:
                return mkt
    return None


def normalize_country(value: str) -> str:
    text = value.strip().lower()
    if text in COUNTRY_WORDS:
        return COUNTRY_WORDS[text]
    if not re.fullmatch(r"[a-z]{2}", text, re.IGNORECASE):
        raise ValueError("cc must be a two-letter country or region code")
    return text


def infer_country(prompt: str) -> str | None:
    explicit = re.search(r"\b(?:cc|country|region)\s*(?:=|:|：)?\s*([a-z]{2})\b", prompt, re.IGNORECASE)
    if explicit:
        return normalize_country(explicit.group(1))

    text = prompt.lower()
    country_context = re.search(r"(country|region|国家|地区|本地|当地|\bin\b|\bfrom\b)", text)
    if country_context:
        for word, cc in COUNTRY_WORDS.items():
            if word in text:
                return cc
    return None


def infer_efirst(prompt: str) -> str | None:
    patterns = [
        r"\b(?:efirst|offset|first|start)\s*(?:=|:|：)?\s*(\d+)\b",
        r"(?:偏移|跳过前|从第)\s*(\d+)\s*(?:个|条|项)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def parse_prompt(prompt: str) -> dict[str, str]:
    values = parse_key_value_pairs(prompt)

    if "q" not in values:
        query = parse_query(prompt)
        if query:
            values["q"] = query

    values.setdefault("engine", "bing_shopping")

    inferred_json = infer_output_format(prompt)
    if inferred_json and "json" not in values:
        values["json"] = inferred_json

    inferred_market = infer_market(prompt)
    if inferred_market and "mkt" not in values:
        values["mkt"] = inferred_market

    inferred_country = infer_country(prompt)
    if inferred_country and "cc" not in values:
        values["cc"] = inferred_country

    inferred_efirst = infer_efirst(prompt)
    if inferred_efirst and "efirst" not in values:
        values["efirst"] = inferred_efirst

    inferred_no_cache = infer_no_cache(prompt)
    if inferred_no_cache and "no_cache" not in values:
        values["no_cache"] = inferred_no_cache

    return values


def apply_overrides(payload: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    for key in ["q", "json", "mkt", "cc", "efirst", "filters"]:
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

    cleaned["engine"] = "bing_shopping"

    if not cleaned.get("q"):
        raise ValueError("Missing required field q. Provide --q or a prompt with a Bing Shopping query.")

    if "json" in cleaned:
        cleaned["json"] = normalize_json_format(cleaned["json"])
    else:
        cleaned["json"] = "1"

    if "mkt" in cleaned:
        cleaned["mkt"] = normalize_market(cleaned["mkt"])

    if "cc" in cleaned:
        cleaned["cc"] = normalize_country(cleaned["cc"])

    if "efirst" in cleaned:
        efirst = int(cleaned["efirst"])
        if efirst < 0:
            raise ValueError("efirst must be greater than or equal to 0")
        cleaned["efirst"] = str(efirst)

    if "no_cache" in cleaned:
        cleaned["no_cache"] = parse_bool(cleaned["no_cache"])
    elif FIELD_DEFAULTS["no_cache"] is not None:
        cleaned["no_cache"] = FIELD_DEFAULTS["no_cache"]

    return cleaned


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.getenv("DATAIFY_API_TOKEN")
    if not token:
        raise ValueError(
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
        "User-Agent": "codex-bing-shopping-skill/1.0",
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
    parser = argparse.ArgumentParser(description="Parse and call the Dataify Bing Shopping API.")
    parser.add_argument("--prompt", default="", help="Natural-language user request to parse.")
    parser.add_argument("--q", help="Bing Shopping query override.")
    parser.add_argument("--json", help="Output format: 1 JSON, 2 JSON plus HTML, 3 HTML. Defaults to 1.")
    parser.add_argument("--mkt", help="Market and language. No default; pass only when requested.")
    parser.add_argument("--cc", help="Two-letter country or region code. No default; pass only when requested.")
    parser.add_argument("--efirst", help="Shopping result offset. No default; pass only when requested.")
    parser.add_argument("--filters", help="Advanced Bing filter string. No default; pass only when requested.")
    parser.add_argument("--no-cache", dest="no_cache", help="true to skip cache, false to use cache. No default.")
    parser.add_argument("--field", action="append", help="Additional API field override as key=value.")
    parser.add_argument("--token", help="API token for this run. Bearer prefix is added when missing.")
    parser.add_argument("--body-format", choices=["form", "json"], default="form", help="POST body format.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print parsed payload and skip network/auth checks.")
    parser.add_argument("--preview-table", action="store_true", help="Print the full request parameter table and skip network/auth checks.")
    parser.add_argument("--confirmed", action="store_true", help="Confirm the user has reviewed the parameter table before a live API call.")
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

        if args.dry_run:
            print(as_json(result))
            return 0

        if args.preview_table:
            print(build_parameter_table(payload))
            return 0

        if not args.confirmed:
            raise ValueError(
                "Live API call requires --confirmed. Show the parameter table to the user first, "
                "ask whether they want to modify it, and call again with --confirmed only after confirmation."
            )

        token = resolve_token(args)
        ok, response_text = call_api(token, payload, args.body_format, args.timeout)
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
