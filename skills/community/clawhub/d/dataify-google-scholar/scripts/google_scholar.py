#!/usr/bin/env python3
"""Call Dataify Scraper API Google Scholar and print the raw response body."""

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
TOKEN_MISSING_MESSAGE = "缺少 Dataify API token，请提供 token，或者前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。"

FIELD_METADATA = (
    {
        "name": "engine",
        "default": "google_scholar",
        "description": "Google 学术接口固定值。",
    },
    {"name": "q", "default": "", "description": "搜索查询内容。"},
    {
        "name": "json",
        "default": "1",
        "description": "输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。",
    },
    {
        "name": "hl",
        "default": "",
        "description": "界面语言代码，例如 en、es、fr、zh-cn。",
    },
    {
        "name": "lr",
        "default": "",
        "description": "限制结果语言，格式为 lang_{语言代码}，多个语言用 | 分隔。",
    },
    {
        "name": "start",
        "default": "0",
        "description": "结果偏移量。0 为第一页，10 为第二页，20 为第三页。",
    },
    {
        "name": "num",
        "default": "10",
        "description": "返回的最大结果数量，范围 1 到 20。",
    },
    {
        "name": "cites",
        "default": "",
        "description": "文章唯一 ID，用于触发“被引”搜索；可与 q 同时使用。",
    },
    {
        "name": "as_ylo",
        "default": "",
        "description": "结果起始年份，可与 as_yhi 结合使用。",
    },
    {
        "name": "as_yhi",
        "default": "",
        "description": "结果结束年份，可与 as_ylo 结合使用。",
    },
    {
        "name": "scisbd",
        "default": "0",
        "description": "过去一年添加的文献和排序。0=相关性，1=仅摘要，2=全部内容。",
    },
    {
        "name": "cluster",
        "default": "",
        "description": "文章唯一 ID，用于触发“所有版本”搜索；不能与 q 或 cites 同用。",
    },
    {
        "name": "as_sdt",
        "default": "0",
        "description": "搜索类型或专利过滤器。0=排除专利，7=包含专利，4=美国法院判例法。",
    },
    {
        "name": "safe",
        "default": "",
        "description": "成人内容过滤级别，可为 active 或 off；文档未给出明确参数默认值。",
    },
    {
        "name": "filter",
        "default": "1",
        "description": "类似结果和省略结果过滤器。1=启用，0=禁用。",
    },
    {
        "name": "as_vis",
        "default": "0",
        "description": "是否排除引用。1=排除引用，0=包含引用。",
    },
    {
        "name": "as_rr",
        "default": "0",
        "description": "是否仅显示综述文章。1=仅综述，0=所有结果。",
    },
    {
        "name": "no_cache",
        "default": "false",
        "description": "是否跳过 5 分钟缓存。true=跳过缓存，false=使用缓存。",
    },
)

FIELDS = tuple(item["name"] for item in FIELD_METADATA if item["name"] != "engine")
DEFAULTS = {
    item["name"]: item["default"]
    for item in FIELD_METADATA
    if item["default"] != ""
}

LANGUAGE_ALIASES = {
    "中文": "zh-cn",
    "简体中文": "zh-cn",
    "简体": "zh-cn",
    "繁体中文": "zh-tw",
    "繁体": "zh-tw",
    "英语": "en",
    "英文": "en",
    "english": "en",
    "en": "en",
    "西班牙语": "es",
    "西语": "es",
    "spanish": "es",
    "es": "es",
    "法语": "fr",
    "法文": "fr",
    "french": "fr",
    "fr": "fr",
    "德语": "de",
    "德文": "de",
    "german": "de",
    "de": "de",
    "日语": "ja",
    "日文": "ja",
    "japanese": "ja",
    "ja": "ja",
    "韩语": "ko",
    "韩文": "ko",
    "korean": "ko",
    "ko": "ko",
    "俄语": "ru",
    "俄文": "ru",
    "russian": "ru",
    "ru": "ru",
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
        description="Call Dataify Google Scholar API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Google Scholar fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the full Markdown parameter table instead of calling the API.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized form payload instead of calling the API.",
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


def normalize_binary(value: Any) -> str:
    text = str(value).strip().lower()
    if text in BOOLEAN_TRUE:
        return "1"
    if text in BOOLEAN_FALSE:
        return "0"
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


def normalize_scisbd(value: Any) -> str:
    text = str(value).strip().lower()
    if text in {"0", "relevance", "relevant", "相关性", "按相关性"}:
        return "0"
    if text in {"1", "abstract", "abstracts", "summary", "summaries", "仅摘要", "摘要"}:
        return "1"
    if text in {"2", "all", "full", "full content", "全部", "全部内容"}:
        return "2"
    return str(value).strip()


def normalize_as_sdt(value: Any) -> str:
    text = str(value).strip().lower()
    if text in {"0", "exclude patents", "without patents", "排除专利", "不含专利"}:
        return "0"
    if text in {"7", "include patents", "with patents", "包含专利", "包括专利"}:
        return "7"
    if text in {"4", "case law", "us case law", "判例法", "美国法院判例法"}:
        return "4"
    return str(value).strip()


def find_languages(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for label, code in LANGUAGE_ALIASES.items():
        label_lower = label.lower()
        if re.fullmatch(r"[a-z]{2,3}(?:-[a-z0-9]+)?", label_lower):
            matched = re.search(rf"\b{re.escape(label_lower)}\b", lowered)
        else:
            matched = label_lower in lowered
        if matched and code not in found:
            found.append(code)
    return found


def find_first_language(text: str) -> str | None:
    languages = find_languages(text)
    return languages[0] if languages else None


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"\b({field_pattern})\b\s*[:=]\s*(\"[^\"]*\"|'[^']*'|[^\s,;，；]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        params[field.lower()] = raw_value.strip().strip("\"'")
    return params


def parse_page_start(text: str) -> str | None:
    patterns = (
        r"第\s*(\d+)\s*页",
        r"第\s*(\d+)\s*頁",
        r"page\s*(\d+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            page = max(int(match.group(1)), 1)
            return str((page - 1) * 10)

    match = re.search(r"\bstart\s*[:=]\s*(\d+)\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def parse_num(text: str) -> str | None:
    patterns = (
        r"返回\s*(\d+)\s*(?:条|篇|个|項|项|results?|papers?)?",
        r"取\s*(\d+)\s*(?:条|篇|个|項|项|results?|papers?)",
        r"\bnum\s*[:=]\s*(\d+)\b",
        r"\b(\d+)\s*(?:results?|papers?)\b",
        r"(\d+)\s*(?:条|篇)\s*(?:结果|文献|论文)?",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def parse_years(text: str) -> dict[str, str]:
    params: dict[str, str] = {}

    between = re.search(
        r"\b(19\d{2}|20\d{2})\b\s*(?:-|到|至|through|to|and)\s*\b(19\d{2}|20\d{2})\b",
        text,
        flags=re.IGNORECASE,
    )
    if between:
        params["as_ylo"] = between.group(1)
        params["as_yhi"] = between.group(2)
        return params

    lower_patterns = (
        r"(?:从|自|起始|开始|不早于)\s*(19\d{2}|20\d{2})",
        r"(19\d{2}|20\d{2})\s*年?\s*(?:以后|之后|以来|起)",
        r"(?:since|after|from)\s+(19\d{2}|20\d{2})",
    )
    for pattern in lower_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["as_ylo"] = match.group(1)
            break

    upper_patterns = (
        r"(?:到|至|截至|截止|结束|不晚于)\s*(19\d{2}|20\d{2})",
        r"(19\d{2}|20\d{2})\s*年?\s*(?:以前|之前|以前的)",
        r"(?:until|before|to)\s+(19\d{2}|20\d{2})",
    )
    for pattern in upper_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            params["as_yhi"] = match.group(1)
            break

    return params


def extract_id_after_markers(text: str, markers: tuple[str, ...]) -> str | None:
    for marker in markers:
        pattern = rf"{re.escape(marker)}\s*[:=：]?\s*([A-Za-z0-9_-]{{6,}})"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def clean_query_text(query: str) -> str:
    query = query.strip().strip("\"'“”‘’")
    stop_patterns = (
        r"\s*(?:返回|取)\s*\d+\s*(?:条|篇|个|results?|papers?).*$",
        r"\s*第\s*\d+\s*页.*$",
        r"\s*page\s*\d+.*$",
        r"\s*(?:从|自|到|至|截至|截止|since|after|before|until)\s*(?:19\d{2}|20\d{2}).*$",
        r"\s*(?:19\d{2}|20\d{2})\s*(?:-|到|至|through|to|and)\s*(?:19\d{2}|20\d{2}).*$",
    )
    for pattern in stop_patterns:
        query = re.sub(pattern, "", query, flags=re.IGNORECASE)
    return query.strip(" ，,;；。")


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"“”'‘’](.+?)[\"“”'‘’]", text)
    if quoted:
        query = clean_query_text(quoted.group(1))
        if query:
            return query

    patterns = (
        r"(?:搜索|查找|查询|检索|采集)\s*(?:Google\s*学术|谷歌学术|学术)?\s*(?:关于|论文|文献|文章)?\s*(.+?)(?:[，。；;,]|$)",
        r"(?:google\s+scholar|scholar|search\s+for|search)\s+(.+?)(?:\s+with\b|\s+in\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = clean_query_text(match.group(1))
            if query:
                return query
    return None


def parse_natural_request(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    if not text:
        return params

    params.update(parse_key_value_fields(text))
    params.update({key: value for key, value in parse_years(text).items() if key not in params})

    if "q" not in params:
        query = extract_query(text)
        if query:
            params["q"] = query

    lowered = text.lower()

    if "cites" not in params:
        cites = extract_id_after_markers(text, ("cites", "被引", "引用该文献", "引用文章"))
        if cites:
            params["cites"] = cites

    if "cluster" not in params:
        cluster = extract_id_after_markers(text, ("cluster", "所有版本", "全部版本", "all versions"))
        if cluster:
            params["cluster"] = cluster

    if "hl" not in params:
        if any(marker in lowered for marker in ("界面语言", "使用语言", "hl", "interface language")):
            language = find_first_language(text)
            if language:
                params["hl"] = language

    if "lr" not in params:
        if any(marker in lowered for marker in ("限制语言", "结果语言", "只搜索", "仅搜索", "lr", "language restrict")):
            languages = find_languages(text)
            if languages:
                params["lr"] = "|".join(f"lang_{code}" for code in languages)

    if "start" not in params:
        start = parse_page_start(text)
        if start:
            params["start"] = start

    if "num" not in params:
        num = parse_num(text)
        if num:
            params["num"] = num

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

    if "scisbd" not in params:
        if any(marker in lowered for marker in ("仅摘要", "只要摘要", "abstract")):
            params["scisbd"] = "1"
        elif any(marker in lowered for marker in ("全部内容", "full content", "all content")):
            params["scisbd"] = "2"
        elif any(marker in lowered for marker in ("过去一年", "按日期", "date sort", "sort by date")):
            params["scisbd"] = "1"

    if "as_sdt" not in params:
        if any(marker in lowered for marker in ("判例法", "case law", "美国法院")):
            params["as_sdt"] = "4"
        elif any(marker in lowered for marker in ("包含专利", "包括专利", "include patents", "with patents")):
            params["as_sdt"] = "7"
        elif any(marker in lowered for marker in ("排除专利", "不含专利", "exclude patents", "without patents")):
            params["as_sdt"] = "0"

    if "safe" not in params:
        if any(marker in lowered for marker in ("safe off", "关闭安全", "安全搜索关闭", "成人")):
            params["safe"] = "off"
        elif any(marker in lowered for marker in ("safe on", "开启安全", "安全搜索开启")):
            params["safe"] = "active"

    if "filter" not in params:
        if any(marker in lowered for marker in ("禁用类似结果", "禁用省略结果", "不过滤类似", "filter off")):
            params["filter"] = "0"
        elif any(marker in lowered for marker in ("启用类似结果", "启用省略结果", "filter on")):
            params["filter"] = "1"

    if "as_vis" not in params:
        if any(marker in lowered for marker in ("排除引用", "不包含引用", "exclude citations")):
            params["as_vis"] = "1"
        elif any(marker in lowered for marker in ("包含引用", "include citations")):
            params["as_vis"] = "0"

    if "as_rr" not in params:
        if any(marker in lowered for marker in ("综述文章", "review articles", "review only", "仅综述")):
            params["as_rr"] = "1"

    if "no_cache" not in params:
        if any(marker in lowered for marker in ("no_cache", "no cache", "bypass cache", "不走缓存", "跳过缓存", "绕过缓存")):
            params["no_cache"] = "true"
        elif any(marker in lowered for marker in ("use cache", "使用缓存", "走缓存")):
            params["no_cache"] = "false"

    return params


def merge_params(args: argparse.Namespace, *, validate: bool) -> dict[str, str]:
    params: dict[str, str] = {}

    if args.request:
        params.update(parse_natural_request(args.request))

    if args.params_json:
        try:
            supplied = json_module.loads(args.params_json)
        except json_module.JSONDecodeError as exc:
            raise ValueError(f"--params-json is not valid JSON: {exc}") from exc
        if not isinstance(supplied, dict):
            raise ValueError("--params-json must be a JSON object")
        for key, value in supplied.items():
            if key in FIELDS:
                cleaned = clean_value(value)
                if cleaned is not None:
                    params[key] = cleaned

    for field in FIELDS:
        value = clean_value(getattr(args, field))
        if value is not None:
            params[field] = value

    return normalize_params(params, validate=validate)


def normalize_params(params: dict[str, Any], *, validate: bool) -> dict[str, str]:
    normalized: dict[str, str] = {"engine": "google_scholar"}

    for field in FIELDS:
        if field in DEFAULTS:
            normalized[field] = DEFAULTS[field]

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    normalized["json"] = normalize_output_mode(normalized.get("json", "1"))

    if "no_cache" in normalized:
        normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

    for field in ("filter", "as_vis", "as_rr"):
        if field in normalized:
            normalized[field] = normalize_binary(normalized[field])

    if "safe" in normalized:
        safe = normalized["safe"].strip().lower()
        if safe in {"active", "on", "true", "1", "开启", "打开"}:
            normalized["safe"] = "active"
        elif safe in {"off", "false", "0", "关闭"}:
            normalized["safe"] = "off"

    if "scisbd" in normalized:
        normalized["scisbd"] = normalize_scisbd(normalized["scisbd"])

    if "as_sdt" in normalized:
        normalized["as_sdt"] = normalize_as_sdt(normalized["as_sdt"])

    if "num" in normalized:
        try:
            num = int(normalized["num"])
        except ValueError as exc:
            raise ValueError("num must be an integer from 1 to 20") from exc
        if not 1 <= num <= 20:
            raise ValueError("num must be from 1 to 20")
        normalized["num"] = str(num)

    if validate:
        if normalized.get("cluster") and (normalized.get("q") or normalized.get("cites")):
            raise ValueError("cluster cannot be combined with q or cites. Use cluster by itself.")
        if not (normalized.get("q") or normalized.get("cites") or normalized.get("cluster")):
            raise ValueError("Missing search condition. Provide q, cites, or cluster.")

    return normalized


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def build_preview_table(params: dict[str, str]) -> str:
    lines = ["| 参数名 | 当前值 | 默认值 | 说明 |", "| --- | --- | --- | --- |"]
    for item in FIELD_METADATA:
        name = item["name"]
        current_value = params.get(name, "")
        default_value = item["default"]
        description = item["description"]
        lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in (name, current_value, default_value, description)
            )
            + " |"
        )
    return "\n".join(lines)


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
        print(f"Request to Dataify API failed: {exc.reason}", file=sys.stderr)
        return 1


def main() -> int:
    args = parse_args()

    try:
        params = merge_params(args, validate=not args.preview)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.preview:
        print(build_preview_table(params))
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
