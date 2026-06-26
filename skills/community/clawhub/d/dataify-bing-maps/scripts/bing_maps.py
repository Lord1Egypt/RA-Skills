#!/usr/bin/env python3
"""Call the Dataify Bing Maps API after parsing natural-language requests."""

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
    "cp",
    "setlang",
    "place_id",
    "first",
    "count",
    "no_cache",
}

DEFAULT_ENDPOINT = "https://scraperapi.dataify.com/request"

PARAMETER_SPECS = [
    {
        "name": "engine",
        "default": "bing_maps",
        "description": "Bing Maps 引擎。默认值为 bing_maps。",
    },
    {
        "name": "q",
        "default": "",
        "description": "Bing Maps 搜索关键词。必填；无默认值。",
    },
    {
        "name": "json",
        "default": "1",
        "description": "输出格式：1 表示 JSON，2 表示 JSON+HTML，3 表示 HTML。默认值为 1。",
    },
    {
        "name": "cp",
        "default": "",
        "description": "查询中心点 GPS 坐标，格式为 纬度~经度。无默认值；示例值不是默认值。",
    },
    {
        "name": "setlang",
        "default": "",
        "description": "两位语言/地区值，例如 us、de、gb。无默认值。",
    },
    {
        "name": "place_id",
        "default": "",
        "description": "Bing Maps 地点唯一引用。无默认值。",
    },
    {
        "name": "first",
        "default": "0",
        "description": "本地结果偏移量。默认值为 0。",
    },
    {
        "name": "count",
        "default": "",
        "description": "每页建议返回结果数量，最大值为 30。无默认值，最大值不是默认值。",
    },
    {
        "name": "no_cache",
        "default": "false",
        "description": "true 表示跳过缓存，false 表示使用缓存。默认值为 false。",
    },
]

DEFAULT_VALUES = {
    spec["name"]: spec["default"]
    for spec in PARAMETER_SPECS
    if spec["default"] != ""
}


SETLANG_WORDS = {
    "us": "us",
    "usa": "us",
    "united states": "us",
    "america": "us",
    "美国": "us",
    "de": "de",
    "germany": "de",
    "德国": "de",
    "gb": "gb",
    "uk": "gb",
    "united kingdom": "gb",
    "英国": "gb",
    "china": "cn",
    "chinese": "cn",
    "中国": "cn",
    "中文": "cn",
    "japan": "jp",
    "japanese": "jp",
    "日本": "jp",
    "france": "fr",
    "french": "fr",
    "法国": "fr",
}


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def as_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def markdown_table(payload: dict[str, str]) -> str:
    lines = [
        "| 参数名 | 当前值 | 默认值 | 说明 |",
        "|---|---|---|---|",
    ]
    for spec in PARAMETER_SPECS:
        name = spec["name"]
        current = payload.get(name, "")
        default = spec["default"]
        description = spec["description"]
        lines.append(f"| `{name}` | {current or '（空）'} | {default or '（无）'} | {description} |")
    return "\n".join(lines)


def normalize_key(key: str) -> str:
    raw_key = key.strip()
    lower_key = raw_key.lower().replace("-", "_")
    aliases = {
        "query": "q",
        "keyword": "q",
        "keywords": "q",
        "search": "q",
        "format": "json",
        "output": "json",
        "coordinates": "cp",
        "coordinate": "cp",
        "gps": "cp",
        "center": "cp",
        "language": "setlang",
        "lang": "setlang",
        "region": "setlang",
        "country": "setlang",
        "cc": "setlang",
        "placeid": "place_id",
        "place_id": "place_id",
        "offset": "first",
        "limit": "count",
        "page_size": "count",
        "no_cache": "no_cache",
        "nocache": "no_cache",
    }
    return aliases.get(lower_key, raw_key)


def strip_wrapping_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    if len(value) >= 2 and value[0] in {"“", "‘"} and value[-1] in {"”", "’"}:
        return value[1:-1].strip()
    return value


def parse_bool(value: str) -> str:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on", "skip", "bypass", "refresh", "fresh"}:
        return "true"
    if text in {"0", "false", "no", "n", "off", "use", "cached"}:
        return "false"
    raise ValueError(f"Invalid boolean value for no_cache: {value!r}")


def normalize_json_format(value: str) -> str:
    text = value.strip().lower().replace(" ", "")
    mapping = {
        "1": "1",
        "json": "1",
        "jsononly": "1",
        "只要json": "1",
        "返回json": "1",
        "2": "2",
        "json+html": "2",
        "html+json": "2",
        "jsonandhtml": "2",
        "htmlandjson": "2",
        "both": "2",
        "全部": "2",
        "都要": "2",
        "3": "3",
        "html": "3",
        "htmlonly": "3",
        "只要html": "3",
        "返回html": "3",
    }
    if text in mapping:
        return mapping[text]
    raise ValueError("json must be 1, 2, 3, JSON, HTML, or JSON+HTML")


def parse_key_value_pairs(prompt: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(
        r"(?P<key>engine|q|query|keyword|keywords|search|json|format|output|cp|gps|coordinates|coordinate|center|setlang|lang|language|region|country|cc|place_id|placeid|first|offset|count|limit|page_size|no_cache|no-cache|nocache)"
        r"\s*(?:=|:|：)\s*"
        r"(?P<value>\"[^\"]+\"|'[^']+'|“[^”]+”|‘[^’]+’|[^,\n;，；]+)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(prompt):
        key = normalize_key(match.group("key"))
        values[key] = strip_wrapping_quotes(match.group("value"))
    return values


def clean_query_text(query: str) -> str:
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    query = re.sub(r"\s*(?:的)?(?:相关)?(?:地图|地点|商家|结果|信息|资料)\s*$", "", query)
    query = re.split(
        r"\s+(?:near|around|at|with|using|return)\b|[,，]\s*(?:cp|setlang|json|first|count|place_id|no_cache)\s*[=:：]",
        query,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    query = re.split(
        r"(?:\s|，|,)*(?:并|且|以及|和)?\s*(?:返回|输出|只要|需要|使用|坐标|语言|地区|每页|第|json\s*和\s*html|html\s*和\s*json|json\+html|html\+json)",
        query,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    return query.strip(" .。")


def parse_query(prompt: str) -> str | None:
    patterns = [
        r"(?:bing\s+maps?|maps?)\s+(?:search|find|look up|query)\s+(?:for\s+)?[\"'](?P<q>[^\"']+)[\"']",
        r"(?:search|find|look up|query)\s+(?:bing\s+maps?\s+)?(?:for\s+)?[\"'](?P<q>[^\"']+)[\"']",
        r"(?:bing\s+maps?|maps?)\s+(?:search|find|look up|query)\s+(?:for\s+)?(?P<q>.+?)(?:\s+(?:near|around|at|with|using|return|json|html|cp=|setlang=|place_id=|first=|count=)|$)",
        r"(?:search|find|look up|query)\s+(?:bing\s+maps?\s+)?(?:for\s+)?(?P<q>.+?)(?:\s+(?:near|around|at|with|using|return|json|html|cp=|setlang=|place_id=|first=|count=)|$)",
        r"(?:搜索|查找|查询|搜一下|检索|抓取|找)(?:必应地图|bing地图|bing maps?)?[\"'“”]?(?P<q>[^\"'“”，,。；;]+)",
        r"(?:在|用)(?:必应地图|bing地图|bing maps?)\s*(?:搜索|查找|查询|找)[\"'“”]?(?P<q>[^\"'“”，,。；;]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            query = clean_query_text(match.group("q"))
            if query:
                return query

    text = prompt.strip()
    if text and not parse_key_value_pairs(prompt):
        return text
    return None


def infer_output_format(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(json\s*(\+|and)\s*html|html\s*(\+|and)\s*json|both|json\s*和\s*html|html\s*和\s*json|都要|全部)", text):
        return "2"
    if re.search(r"(html only|return html|html format|只要\s*html|返回\s*html|输出\s*html)", text):
        return "3"
    if re.search(r"(json only|return json|json format|只要\s*json|返回\s*json|输出\s*json)", text):
        return "1"
    return None


def infer_no_cache(prompt: str) -> str | None:
    text = prompt.lower()
    if re.search(r"(no_cache|no-cache|skip cache|bypass cache|refresh|fresh|实时|刷新|跳过缓存|不要缓存|不使用缓存)", text):
        return "true"
    if re.search(r"(use cache|cached|使用缓存|走缓存)", text):
        return "false"
    return None


def normalize_cp(value: str) -> str:
    text = value.strip()
    coord_match = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:~|,|，|\s+)\s*(-?\d+(?:\.\d+)?)", text)
    if not coord_match:
        raise ValueError("cp must be in latitude~longitude form")
    lat = float(coord_match.group(1))
    lon = float(coord_match.group(2))
    if lat < -90 or lat > 90:
        raise ValueError("cp latitude must be between -90 and 90")
    if lon < -180 or lon > 180:
        raise ValueError("cp longitude must be between -180 and 180")
    return f"{coord_match.group(1)}~{coord_match.group(2)}"


def infer_cp(prompt: str) -> str | None:
    patterns = [
        r"\bcp\s*(?:=|:)\s*(-?\d+(?:\.\d+)?\s*(?:~|,|，)\s*-?\d+(?:\.\d+)?)",
        r"(?:gps|coordinates?|坐标|经纬度)\s*(?:=|:|：)?\s*(-?\d+(?:\.\d+)?\s*(?:~|,|，)\s*-?\d+(?:\.\d+)?)",
        r"\b(?:near|around|at)\s+(-?\d+(?:\.\d+)?\s*(?:~|,|，)\s*-?\d+(?:\.\d+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return normalize_cp(match.group(1))

    lat_match = re.search(r"\blat(?:itude)?\s*(?:=|:)?\s*(-?\d+(?:\.\d+)?)", prompt, re.IGNORECASE)
    lon_match = re.search(r"\b(?:lon|lng|longitude)\s*(?:=|:)?\s*(-?\d+(?:\.\d+)?)", prompt, re.IGNORECASE)
    if lat_match and lon_match:
        return normalize_cp(f"{lat_match.group(1)}~{lon_match.group(1)}")
    return None


def normalize_setlang(value: str) -> str:
    text = value.strip().lower()
    if text in SETLANG_WORDS:
        return SETLANG_WORDS[text]
    if re.fullmatch(r"[a-z]{2}", text):
        return text
    raise ValueError("setlang must be a two-letter value such as us, de, gb, cn, or jp")


def infer_setlang(prompt: str) -> str | None:
    explicit = re.search(r"\b(?:setlang|lang|language|region|country|cc)\s*(?:=|:)\s*([a-z]{2})\b", prompt, re.IGNORECASE)
    if explicit:
        return normalize_setlang(explicit.group(1))
    text = prompt.lower()
    for word, value in SETLANG_WORDS.items():
        if word in text:
            return value
    return None


def infer_place_id(prompt: str) -> str | None:
    match = re.search(r"\b(?:place_id|placeid|place id)\s*(?:=|:|：)\s*([A-Za-z0-9._~:-]+)", prompt, re.IGNORECASE)
    if match:
        return match.group(1)
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


def infer_count(prompt: str) -> str | None:
    patterns = [
        r"\bcount\s*(?:=|:)?\s*(\d+)\b",
        r"\blimit\s*(?:=|:)?\s*(\d+)\b",
        r"(?:每页|返回|取|要|显示)\s*(\d+)\s*(?:条|个|个结果|条结果)?",
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

    values.setdefault("engine", "bing_maps")

    inferred_json = infer_output_format(prompt)
    if inferred_json and "json" not in values:
        values["json"] = inferred_json

    inferred_cp = infer_cp(prompt)
    if inferred_cp and "cp" not in values:
        values["cp"] = inferred_cp

    inferred_setlang = infer_setlang(prompt)
    if inferred_setlang and "setlang" not in values:
        values["setlang"] = inferred_setlang

    inferred_place_id = infer_place_id(prompt)
    if inferred_place_id and "place_id" not in values:
        values["place_id"] = inferred_place_id

    inferred_first = infer_first(prompt)
    if inferred_first and "first" not in values:
        values["first"] = inferred_first

    inferred_count = infer_count(prompt)
    if inferred_count and "count" not in values:
        values["count"] = inferred_count

    inferred_no_cache = infer_no_cache(prompt)
    if inferred_no_cache and "no_cache" not in values:
        values["no_cache"] = inferred_no_cache

    return values


def apply_overrides(payload: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    for key in ["q", "json", "cp", "setlang", "first", "count"]:
        value = getattr(args, key, None)
        if value is not None:
            payload[key] = value

    if args.lat is not None or args.lon is not None:
        if args.lat is None or args.lon is None:
            raise ValueError("--lat and --lon must be provided together")
        payload["cp"] = f"{args.lat}~{args.lon}"

    if args.place_id is not None:
        payload["place_id"] = args.place_id

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

    cleaned["engine"] = DEFAULT_VALUES["engine"]

    if not cleaned.get("q"):
        raise ValueError("Missing required field q. Provide --q or a prompt with a Bing Maps query.")

    if "json" in cleaned:
        cleaned["json"] = normalize_json_format(cleaned["json"])
    else:
        cleaned["json"] = DEFAULT_VALUES["json"]

    if "cp" in cleaned:
        cleaned["cp"] = normalize_cp(cleaned["cp"])

    if "setlang" in cleaned:
        cleaned["setlang"] = normalize_setlang(cleaned["setlang"])

    if "first" in cleaned:
        first = int(cleaned["first"])
        if first < 0:
            raise ValueError("first must be greater than or equal to 0")
        cleaned["first"] = str(first)
    else:
        cleaned["first"] = DEFAULT_VALUES["first"]

    if "count" in cleaned:
        count = int(cleaned["count"])
        if count < 1 or count > 30:
            raise ValueError("count must be between 1 and 30")
        cleaned["count"] = str(count)

    if "no_cache" in cleaned:
        cleaned["no_cache"] = parse_bool(cleaned["no_cache"])
    else:
        cleaned["no_cache"] = DEFAULT_VALUES["no_cache"]

    return cleaned


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.getenv("DATAIFY_API_TOKEN")
    if not token:
        raise ValueError(
            "缺少 DATAIFY_API_TOKEN。请提供 --token，或设置 DATAIFY_API_TOKEN，"
            "或者访问 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"
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
        "User-Agent": "codex-bing-maps-skill/1.0",
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
    parser = argparse.ArgumentParser(description="Parse and call the Dataify Bing Maps API.")
    parser.add_argument("--prompt", default="", help="Natural-language user request to parse.")
    parser.add_argument("--q", help="Bing Maps query override.")
    parser.add_argument("--json", help="Output format: 1 JSON, 2 JSON plus HTML, 3 HTML. Defaults to 1.")
    parser.add_argument("--cp", help="GPS center as latitude~longitude. No default; pass only when requested.")
    parser.add_argument("--lat", help="GPS latitude; must be used with --lon.")
    parser.add_argument("--lon", help="GPS longitude; must be used with --lat.")
    parser.add_argument("--setlang", help="Two-letter language/region value, such as us, de, or gb. No default.")
    parser.add_argument("--place-id", dest="place_id", help="Bing Maps place ID. No default.")
    parser.add_argument("--first", help="Local result offset. No default.")
    parser.add_argument("--count", help="Suggested results per page, max 30. No default.")
    parser.add_argument("--no-cache", dest="no_cache", help="true to skip cache, false to use cache. No default.")
    parser.add_argument("--field", action="append", help="Additional API field override as key=value.")
    parser.add_argument("--token", help="API token for this run. Bearer prefix is added when missing.")
    parser.add_argument("--body-format", choices=["form", "json"], default="form", help="POST body format.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print parsed payload and skip network/auth checks.")
    parser.add_argument("--params-table", action="store_true", help="Print a Markdown parameter table and skip network/auth checks.")
    parser.add_argument("--confirmed", action="store_true", help="Required for live API calls after the user confirms the parameter table.")
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

        if args.params_table:
            print(markdown_table(payload))
            return 0

        if args.dry_run:
            print(as_json(result))
            return 0

        if not args.confirmed:
            print(markdown_table(payload))
            print("\n请确认以上参数是否需要修改。用户确认后，再添加 --confirmed 调用接口。")
            return 0

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
