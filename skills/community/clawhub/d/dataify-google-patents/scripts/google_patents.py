#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Dataify Scraper API Google Patents and print the raw response body."""

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

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

FIELDS = (
    "q",
    "json",
    "page",
    "num",
    "sort",
    "clustered",
    "dups",
    "patents",
    "scholar",
    "before",
    "after",
    "inventor",
    "assignee",
    "country",
    "language",
    "status",
    "type",
    "litigation",
    "no_cache",
)

DEFAULTS = {
    "json": "1",
    "page": "0",
    "dups": "family",
    "patents": "true",
    "scholar": "false",
    "no_cache": "false",
}

DISPLAY_DEFAULTS = {
    "Authorization": "",
    "engine": "google_patents",
    "q": "",
    "json": "1",
    "page": "0",
    "num": "",
    "sort": "省略（默认按相关性排序）",
    "clustered": "",
    "dups": "family",
    "patents": "true",
    "scholar": "false",
    "before": "",
    "after": "",
    "inventor": "",
    "assignee": "",
    "country": "",
    "language": "",
    "status": "",
    "type": "",
    "litigation": "",
    "no_cache": "false",
}

FIELD_DESCRIPTIONS = {
    "Authorization": "Dataify API token；没有 token 时提示用户提供，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。",
    "engine": "Google Patents 固定引擎值。",
    "q": "要搜索的专利查询内容；可用分号分隔多个搜索表达式。",
    "json": "输出格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。",
    "page": "页码；0 为第一页，1 为第二页，依次类推。",
    "num": "每页结果数量；最小 10，最大 100。",
    "sort": "排序方式；new=最新，old=最旧；省略时默认按相关性排序。",
    "clustered": "结果分组方式；true 表示按分类分组。",
    "dups": "去重方式；family=按家族去重，language=按公布/公开去重。",
    "patents": "是否包含 Google Patents 结果；默认 true。",
    "scholar": "是否包含 Google Scholar 结果；默认 false。",
    "before": "最大日期过滤；格式为 priority:YYYYMMDD、filing:YYYYMMDD 或 publication:YYYYMMDD。",
    "after": "最小日期过滤；格式为 priority:YYYYMMDD、filing:YYYYMMDD 或 publication:YYYYMMDD。",
    "inventor": "发明人过滤；多个发明人可用逗号分隔，名称含逗号时用括号包裹。",
    "assignee": "受让人/申请人/权利人过滤；多个名称可用逗号分隔，名称含逗号时用括号包裹。",
    "country": "按国家/地区代码过滤；多个代码用逗号分隔。",
    "language": "按语言过滤；多个语言用逗号分隔。",
    "status": "状态过滤；GRANT=授权专利，APPLICATION=专利申请。",
    "type": "类型过滤；PATENT=专利，DESIGN=外观设计。",
    "litigation": "诉讼状态过滤；YES=有相关诉讼，NO=无已知诉讼。",
    "no_cache": "是否跳过缓存；true=跳过缓存，false=使用缓存。",
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
    "包含",
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
    "不包含",
    "排除",
}

COUNTRY_ALIASES = {
    "united states": "US",
    "usa": "US",
    "u.s.": "US",
    "us": "US",
    "美国": "US",
    "china": "CN",
    "cn": "CN",
    "中国": "CN",
    "japan": "JP",
    "jp": "JP",
    "日本": "JP",
    "korea": "KR",
    "south korea": "KR",
    "kr": "KR",
    "韩国": "KR",
    "germany": "DE",
    "de": "DE",
    "德国": "DE",
    "france": "FR",
    "fr": "FR",
    "法国": "FR",
    "united kingdom": "GB",
    "uk": "GB",
    "gb": "GB",
    "英国": "GB",
    "europe": "EP",
    "european": "EP",
    "ep": "EP",
    "欧洲": "EP",
    "world": "WO",
    "wipo": "WO",
    "wo": "WO",
    "国际": "WO",
}

LANGUAGE_ALIASES = {
    "english": "ENGLISH",
    "en": "ENGLISH",
    "英文": "ENGLISH",
    "英语": "ENGLISH",
    "chinese": "CHINESE",
    "zh": "CHINESE",
    "中文": "CHINESE",
    "汉语": "CHINESE",
    "japanese": "JAPANESE",
    "ja": "JAPANESE",
    "日文": "JAPANESE",
    "日语": "JAPANESE",
    "korean": "KOREAN",
    "ko": "KOREAN",
    "韩文": "KOREAN",
    "韩语": "KOREAN",
    "german": "GERMAN",
    "de": "GERMAN",
    "德文": "GERMAN",
    "德语": "GERMAN",
    "french": "FRENCH",
    "fr": "FRENCH",
    "法文": "FRENCH",
    "法语": "FRENCH",
    "spanish": "SPANISH",
    "es": "SPANISH",
    "西班牙文": "SPANISH",
    "西班牙语": "SPANISH",
}

DATE_TYPE_ALIASES = {
    "priority": "priority",
    "prior": "priority",
    "优先权": "priority",
    "filing": "filing",
    "filed": "filing",
    "申请": "filing",
    "publication": "publication",
    "published": "publication",
    "公开": "publication",
    "公布": "publication",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Dataify Google Patents API and print the raw response body."
    )
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--params-json", help="JSON object containing Dataify Google Patents fields.")
    parser.add_argument("--request", help="Natural-language request to parse as a fallback.")
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print the normalized payload instead of calling API.")
    parser.add_argument("--print-table", action="store_true", help="Print the full parameter review table and exit.")

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


def normalize_sort(value: Any) -> str | None:
    text = str(value).strip().lower()
    if text in {"new", "newest", "latest", "recent", "最新", "最近"}:
        return "new"
    if text in {"old", "oldest", "earliest", "最旧", "最早"}:
        return "old"
    if text in {"relevance", "relevant", "相关性", "默认"}:
        return None
    return str(value).strip()


def normalize_dups(value: Any) -> str:
    text = str(value).strip().lower()
    if text in {"family", "families", "家族", "按家族"}:
        return "family"
    if text in {"publication", "publications", "language", "公布", "公开", "按公布", "按公开"}:
        return "language"
    return str(value).strip()


def normalize_choice(value: Any, mapping: dict[str, str]) -> str:
    text = str(value).strip()
    return mapping.get(text.lower(), mapping.get(text.upper(), text.upper()))


def normalize_country(value: Any) -> str:
    parts = split_multi_value(str(value))
    normalized: list[str] = []
    for part in parts:
        lowered = part.lower()
        normalized.append(COUNTRY_ALIASES.get(lowered, part.upper() if re.fullmatch(r"[A-Za-z]{2,3}", part) else part))
    return ",".join(normalized)


def normalize_language(value: Any) -> str:
    parts = split_multi_value(str(value))
    normalized: list[str] = []
    for part in parts:
        lowered = part.lower()
        normalized.append(LANGUAGE_ALIASES.get(lowered, part))
    return ",".join(normalized)


def split_multi_value(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,，;；]", value) if part.strip()]


def normalize_date_string(value: str) -> str:
    compact = re.sub(r"[-/.\s]", "", value.strip())
    return compact if re.fullmatch(r"\d{8}", compact) else value.strip()


def normalize_date_filter(value: Any) -> str:
    text = str(value).strip()
    if ":" not in text:
        return normalize_date_string(text)
    kind, raw_date = text.split(":", 1)
    normalized_kind = DATE_TYPE_ALIASES.get(kind.strip().lower(), kind.strip())
    return f"{normalized_kind}:{normalize_date_string(raw_date)}"


def find_alias(text: str, aliases: dict[str, str]) -> str | None:
    lowered = text.lower()
    for label, code in aliases.items():
        if label.lower() in lowered:
            return code
    return None


def parse_key_value_fields(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    field_pattern = "|".join(re.escape(field) for field in FIELDS)
    pattern = rf"(?:^|[\s,;，；])({field_pattern})\s*[:=：]\s*(\"[^\"]*\"|'[^']*'|[^,;，；\n]+)"
    for field, raw_value in re.findall(pattern, text, flags=re.IGNORECASE):
        value = raw_value.strip().strip("\"'")
        params[field.lower()] = value
    return params


def extract_query(text: str) -> str | None:
    quoted = re.search(r"[\"'“”‘’](.+?)[\"'“”‘’]", text)
    if quoted:
        return quoted.group(1).strip()

    patterns = (
        r"(?:搜索|查找|查询|检索)(?:\s*Google)?(?:\s*专利)?\s*[:：]?\s*(.+?)(?:[，。；;]|$)",
        r"(?:search\s+(?:google\s+)?patents?\s+for|google\s+patents?\s+for|patents?\s+for|search\s+for)\s+(.+?)(?:\s+(?:with|as|in|before|after|from|by)\b|[,;.]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            query = re.sub(r"^(?:关于|有关)\s*", "", query)
            if query:
                return query
    return None


def extract_page(text: str) -> str | None:
    patterns = (
        r"第\s*(\d+)\s*页",
        r"page\s*(\d+)",
        r"第\s*(\d+)\s*頁",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            page = max(int(match.group(1)), 1)
            return str(page - 1)
    return None


def extract_num(text: str) -> str | None:
    patterns = (
        r"(?:每页|每頁|返回|数量|數量|条数|條數|num|results?)\s*[:=：]?\s*(\d{1,3})",
        r"(\d{1,3})\s*(?:条|條|results?)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_named_filter(text: str, labels: tuple[str, ...]) -> str | None:
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = rf"(?:{label_pattern})\s*[:=：]?\s*(\"[^\"]*\"|'[^']*'|[^,;，；。\n]+)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def extract_date_filter(text: str, direction: str) -> str | None:
    direction_words = (
        ("before", "之前", "以前", "早于", "截止", "最大日期")
        if direction == "before"
        else ("after", "之后", "以后", "晚于", "起始", "最小日期")
    )
    date_type_pattern = r"priority|prior|filing|filed|publication|published|优先权|申请|公开|公布"
    date_pattern = r"\d{4}[-/.]?\d{2}[-/.]?\d{2}|\d{8}"
    direction_pattern = "|".join(re.escape(word) for word in direction_words)

    patterns = (
        rf"({date_type_pattern})\s*(?:date|日期)?\s*(?:{direction_pattern})\s*[:=：]?\s*({date_pattern})",
        rf"(?:{direction_pattern})\s*({date_type_pattern})\s*(?:date|日期)?\s*[:=：]?\s*({date_pattern})",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            kind, raw_date = match.group(1), match.group(2)
            return normalize_date_filter(f"{kind}:{raw_date}")
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

    if "page" not in params:
        page = extract_page(text)
        if page:
            params["page"] = page

    if "num" not in params:
        num = extract_num(text)
        if num:
            params["num"] = num

    if "sort" not in params:
        if any(marker in lowered for marker in ("newest", "latest", "recent", "最新", "最近")):
            params["sort"] = "new"
        elif any(marker in lowered for marker in ("oldest", "earliest", "最旧", "最早")):
            params["sort"] = "old"

    if "clustered" not in params and any(marker in lowered for marker in ("clustered", "grouped", "分组", "分組")):
        params["clustered"] = "true"

    if "dups" not in params:
        if any(marker in lowered for marker in ("family dedupe", "family duplicates", "家族去重", "按家族")):
            params["dups"] = "family"
        elif any(marker in lowered for marker in ("publication dedupe", "publication duplicates", "公开去重", "公布去重", "按公开", "按公布")):
            params["dups"] = "language"

    if "patents" not in params:
        if any(marker in lowered for marker in ("exclude patents", "without patents", "不包含专利", "排除专利")):
            params["patents"] = "false"
        elif any(marker in lowered for marker in ("include patents", "包含专利", "专利结果")):
            params["patents"] = "true"

    if "scholar" not in params:
        if any(marker in lowered for marker in ("exclude scholar", "without scholar", "不包含学术", "排除学术")):
            params["scholar"] = "false"
        elif any(marker in lowered for marker in ("include scholar", "google scholar", "scholar", "包含学术", "学术结果")):
            params["scholar"] = "true"

    if "before" not in params:
        before = extract_date_filter(text, "before")
        if before:
            params["before"] = before

    if "after" not in params:
        after = extract_date_filter(text, "after")
        if after:
            params["after"] = after

    if "inventor" not in params:
        inventor = extract_named_filter(text, ("inventor", "发明人", "發明人"))
        if inventor:
            params["inventor"] = inventor

    if "assignee" not in params:
        assignee = extract_named_filter(text, ("assignee", "applicant", "owner", "受让人", "受讓人", "申请人", "申請人", "权利人", "權利人"))
        if assignee:
            params["assignee"] = assignee

    if "country" not in params:
        country = extract_named_filter(text, ("country", "countries", "国家", "國家", "地区", "地區"))
        if country:
            params["country"] = country
        else:
            alias = find_alias(text, COUNTRY_ALIASES)
            if alias:
                params["country"] = alias

    if "language" not in params:
        language = extract_named_filter(text, ("language", "languages", "语言", "語言"))
        if language:
            params["language"] = language

    if "status" not in params:
        if any(marker in lowered for marker in ("granted", "grant", "授权", "授權", "已授权", "已授權")):
            params["status"] = "GRANT"
        elif any(marker in lowered for marker in ("application", "applications", "申请", "申請")):
            params["status"] = "APPLICATION"

    if "type" not in params:
        if any(marker in lowered for marker in ("design", "外观设计", "外觀設計")):
            params["type"] = "DESIGN"
        elif any(marker in lowered for marker in ("patent type", "专利类型", "專利類型")):
            params["type"] = "PATENT"

    if "litigation" not in params:
        if any(marker in lowered for marker in ("without litigation", "no litigation", "无诉讼", "無訴訟", "没有诉讼", "沒有訴訟")):
            params["litigation"] = "NO"
        elif any(marker in lowered for marker in ("with litigation", "litigation", "有诉讼", "有訴訟")):
            params["litigation"] = "YES"

    if "no_cache" not in params:
        if any(marker in lowered for marker in ("no_cache", "no cache", "bypass cache", "跳过缓存", "跳過緩存", "不使用缓存", "不使用緩存")):
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
            normalized_key = str(key).strip()
            if normalized_key in FIELDS:
                cleaned = clean_value(value)
                if cleaned is not None:
                    params[normalized_key] = cleaned

    for field in FIELDS:
        value = clean_value(getattr(args, field))
        if value is not None:
            params[field] = value

    return normalize_params(params)


def normalize_params(params: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {"engine": "google_patents"}

    for field in FIELDS:
        value = clean_value(params.get(field))
        if value is not None:
            normalized[field] = value

    for field, default_value in DEFAULTS.items():
        normalized.setdefault(field, default_value)

    normalized["json"] = normalize_output_mode(normalized["json"])
    normalized["page"] = str(normalized["page"]).strip()
    normalized["dups"] = normalize_dups(normalized["dups"])
    normalized["patents"] = normalize_boolean(normalized["patents"])
    normalized["scholar"] = normalize_boolean(normalized["scholar"])
    normalized["no_cache"] = normalize_boolean(normalized["no_cache"])

    if "sort" in normalized:
        sort = normalize_sort(normalized["sort"])
        if sort is None:
            normalized.pop("sort", None)
        else:
            normalized["sort"] = sort

    if "clustered" in normalized:
        normalized["clustered"] = normalize_boolean(normalized["clustered"])

    if "before" in normalized:
        normalized["before"] = normalize_date_filter(normalized["before"])
    if "after" in normalized:
        normalized["after"] = normalize_date_filter(normalized["after"])
    if "country" in normalized:
        normalized["country"] = normalize_country(normalized["country"])
    if "language" in normalized:
        normalized["language"] = normalize_language(normalized["language"])
    if "status" in normalized:
        normalized["status"] = normalize_choice(
            normalized["status"],
            {
                "grant": "GRANT",
                "granted": "GRANT",
                "授权": "GRANT",
                "授權": "GRANT",
                "application": "APPLICATION",
                "applications": "APPLICATION",
                "申请": "APPLICATION",
                "申請": "APPLICATION",
            },
        )
    if "type" in normalized:
        normalized["type"] = normalize_choice(
            normalized["type"],
            {
                "patent": "PATENT",
                "专利": "PATENT",
                "專利": "PATENT",
                "design": "DESIGN",
                "外观设计": "DESIGN",
                "外觀設計": "DESIGN",
            },
        )
    if "litigation" in normalized:
        normalized["litigation"] = normalize_choice(
            normalized["litigation"],
            {
                "yes": "YES",
                "true": "YES",
                "有": "YES",
                "有诉讼": "YES",
                "有訴訟": "YES",
                "no": "NO",
                "false": "NO",
                "无": "NO",
                "無": "NO",
                "无诉讼": "NO",
                "無訴訟": "NO",
            },
        )

    return normalized


def has_search_criteria(params: dict[str, str]) -> bool:
    criteria_fields = {
        "q",
        "sort",
        "clustered",
        "before",
        "after",
        "inventor",
        "assignee",
        "country",
        "language",
        "status",
        "type",
        "litigation",
    }
    return any(clean_value(params.get(field)) for field in criteria_fields)


def get_authorization(token_arg: str | None) -> str | None:
    token = clean_value(token_arg) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        return None
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    os.environ["DATAIFY_API_TOKEN"] = token
    return token


def token_status(token_arg: str | None) -> str:
    return "已提供（已隐藏）" if get_authorization(token_arg) else "未提供"


def escape_markdown(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r", " ").replace("\n", " ").strip()
    return text.replace("|", "\\|")


def print_parameter_table(params: dict[str, str], token_arg: str | None) -> None:
    rows = ["| 参数名 | 当前值 | 默认值 | 说明 |", "| --- | --- | --- | --- |"]
    all_fields = ("Authorization", "engine", *FIELDS)
    for field in all_fields:
        if field == "Authorization":
            current_value = token_status(token_arg)
        elif field == "sort" and "sort" not in params:
            current_value = "省略（默认按相关性排序）"
        else:
            current_value = params.get(field, "")
        rows.append(
            "| {field} | {current} | {default} | {description} |".format(
                field=escape_markdown(field),
                current=escape_markdown(current_value),
                default=escape_markdown(DISPLAY_DEFAULTS.get(field, "")),
                description=escape_markdown(FIELD_DESCRIPTIONS.get(field, "")),
            )
        )
    print("\n".join(rows))


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

    if args.print_table:
        print_parameter_table(params, args.token)
        return 0

    if args.dry_run:
        print(json_module.dumps(params, ensure_ascii=False, sort_keys=True))
        return 0

    if not has_search_criteria(params):
        print("缺少 Google Patents 搜索条件，请提供 q 或至少一个筛选字段。", file=sys.stderr)
        return 2

    authorization = get_authorization(args.token)
    if not authorization:
        print("缺少 Dataify API token，请提供 token，或前往 https://dashboard.dataify.com/login?utm_source=skill 注册获取。", file=sys.stderr)
        return 2

    return call_api(params, authorization, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
