#!/usr/bin/env python3
"""
Convert fetched AI news payloads into normalized source_item records
that are ready for Feishu Bitable ingestion.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from zoneinfo import ZoneInfo

BITABLE_FIELD_MAP_ZH = {
    "title": "标题",
    "canonical_url": "原文链接",
    "source": "来源",
    "source_type": "来源类型",
    "published_at": "发布时间",
    "original_time": "原始时间",
    "raw_text": "原文摘要",
    "hash_title": "标题哈希",
    "hash_text": "摘要哈希",
    "status": "处理状态",
    "notes": "备注",
    "window_key": "报道窗口键",
}


def get_report_window_key() -> str:
    """
    计算当前报道窗口键
    - 如果当前时间 >= 09:00，窗口是 今天09:00 - 明天09:00，窗口键 = 明天日期 + "-0900"
    - 如果当前时间 < 09:00，窗口是 昨天09:00 - 今天09:00，窗口键 = 今天日期 + "-0900"
    """
    now = datetime.now()
    current_hour = now.hour
    
    if current_hour >= 9:
        # 今天的窗口，明天为窗口结束时间
        from datetime import timedelta
        tomorrow = now + timedelta(days=1)
        window_date = tomorrow.strftime("%Y-%m-%d")
    else:
        # 昨天的窗口，今天为窗口结束时间
        window_date = now.strftime("%Y-%m-%d")
    
    return f"{window_date}-0900"


TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {
    "spm",
    "from",
    "fromid",
    "feature",
    "ref",
    "referer",
    "source",
    "sourceid",
    "sessionid",
}

ENTITY_KEYWORDS = {
    "OpenAI": ["openai", "gpt", "chatgpt", "sora"],
    "Anthropic": ["anthropic", "claude"],
    "Google": ["google", "gemini", "deepmind"],
    "Meta": ["meta", "llama"],
    "Microsoft": ["microsoft", "copilot", "azure ai"],
    "NVIDIA": ["nvidia", "h100", "h200", "blackwell"],
    "财联社": ["财联社", "cls"],
    "36氪": ["36氪", "36kr"],
    "Forrester": ["forrester"],
    "Steve Blank": ["steve blank"],
    "上海": ["上海"],
}

THEME_RULES = [
    ("算力", ["算力", "芯片", "gpu", "推理", "训练", "云", "算力券", "降价"]),
    ("应用", ["agent", "应用", "workflow", "工作流", "数字员工", "copilot"]),
    ("商业", ["成本", "roi", "付费", "采购", "营收", "价格"]),
    ("人才", ["岗位", "招聘", "人才", "组织", "培训"]),
    ("安全", ["合规", "监管", "安全", "隐私", "risk", "policy"]),
    ("资本", ["融资", "并购", "估值", "投资", "基金"]),
    ("基础设施", ["模型", "框架", "sdk", "api", "infra", "平台"]),
]

SOURCE_TYPE_RULES = {
    "OpenAI新闻": "announcement",
    "Anthropic新闻": "announcement",
    "Forrester博客": "blog",
    "SteveBlank": "blog",
    "财联社-AI": "news",
    "36氪-AI": "news",
    "CMSWire": "news",
    "CX Today": "news",
}
LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def sha1_text(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def normalize_timestamp(value: Optional[str]) -> str:
    if not value:
        return ""
    candidate = value.strip()
    if candidate.endswith("Z"):
        return candidate
    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except ValueError:
        return candidate


def normalize_original_time(value: Optional[str]) -> str:
    if not value:
        return ""
    candidate = value.strip()
    now_local = datetime.now(LOCAL_TZ)

    for fmt in (
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y.%m.%d",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H:%M:%S",
        "%b %d, %Y",
        "%b %d, %Y %H:%M",
        "%B %d, %Y",
        "%B %d, %Y %H:%M",
    ):
        try:
            dt = datetime.strptime(candidate, fmt)
            dt = dt.replace(tzinfo=LOCAL_TZ)
            return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        except ValueError:
            continue

    match = re.search(r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2})(?::(?P<second>\d{1,2}))?)?", candidate)
    if match:
        dt = datetime(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day")),
            int(match.group("hour") or 0),
            int(match.group("minute") or 0),
            int(match.group("second") or 0),
            tzinfo=LOCAL_TZ,
        )
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    match = re.search(r"(?P<month>\d{1,2})[/-](?P<day>\d{1,2})(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2})(?::(?P<second>\d{1,2}))?)?", candidate)
    if match:
        dt = datetime(
            now_local.year,
            int(match.group("month")),
            int(match.group("day")),
            int(match.group("hour") or 0),
            int(match.group("minute") or 0),
            int(match.group("second") or 0),
            tzinfo=LOCAL_TZ,
        )
        if dt - now_local > timedelta(days=2):
            dt = dt.replace(year=dt.year - 1)
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    return ""


def iso_to_epoch_ms(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    candidate = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LOCAL_TZ)
    return int(dt.timestamp() * 1000)


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    query_items = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        key_lower = key.lower()
        if key_lower in TRACKING_QUERY_KEYS:
            continue
        if any(key_lower.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES):
            continue
        query_items.append((key, value))

    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        path=parsed.path.rstrip("/") or parsed.path,
        query=urlencode(query_items),
        fragment="",
    )
    return urlunparse(normalized)


def guess_source_type(source: str) -> str:
    return SOURCE_TYPE_RULES.get(source, "news")


def extract_entities(*values: str) -> List[str]:
    haystack = " ".join(values).lower()
    entities = []
    for entity, keywords in ENTITY_KEYWORDS.items():
        if any(keyword.lower() in haystack for keyword in keywords):
            entities.append(entity)
    return entities


def guess_theme(*values: str) -> str:
    haystack = " ".join(values).lower()
    for theme, keywords in THEME_RULES:
        if any(keyword.lower() in haystack for keyword in keywords):
            return theme
    return ""


def build_event_key_guess(entities: Iterable[str], theme_guess: str, title: str, published_at: str) -> str:
    entity_part = "-".join(entity.lower().replace(" ", "_") for entity in entities[:2]) or "unknown"
    date_part = published_at[:10] if published_at else "unknown-date"
    title_part = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", title.lower()).strip("-")[:40]
    parts = [entity_part, theme_guess or "unknown-theme", date_part, title_part or "untitled"]
    return "--".join(parts)


def build_source_item(article: Dict[str, str], fetched_at: str) -> Dict[str, object]:
    title = clean_text(article.get("title"))
    raw_url = clean_text(article.get("url"))
    canonical_url = canonicalize_url(raw_url)
    source = clean_text(article.get("source"))
    original_time = clean_text(article.get("date"))
    published_at = normalize_timestamp(article.get("parsed_date"))
    if not published_at:
        published_at = normalize_original_time(original_time)
    author = clean_text(article.get("author"))
    raw_text = clean_text(article.get("summary"))
    entities = extract_entities(title, source, raw_url)
    theme_guess = guess_theme(title, source, raw_text or title)
    hash_title = sha1_text(title)[:16]
    hash_text = sha1_text(raw_text)[:16] if raw_text else ""
    event_key_guess = build_event_key_guess(entities, theme_guess, title, published_at)

    return {
        "title": title,
        "canonical_url": canonical_url,
        "source": source,
        "source_type": guess_source_type(source),
        "published_at": published_at,
        "original_time": original_time,
        "fetched_at": fetched_at,
        "raw_text": raw_text,
        "hash_title": hash_title,
        "hash_text": hash_text,
        "status": "new",
        "notes": "",
        "window_key": get_report_window_key(),
    }


def bitable_record(source_item: Dict[str, object]) -> Dict[str, object]:
    fields = {}
    for key, value in source_item.items():
        if value is None:
            continue
        if key == "fetched_at":
            # 飞书表可以直接使用“创建时间”字段，避免模型重复写入抓取时间。
            continue
        if key == "hash_text" and not value:
            continue
        field_name = BITABLE_FIELD_MAP_ZH.get(key, key)
        if key == "canonical_url":
            fields[field_name] = {
                "text": str(value),
                "link": str(value),
            }
        elif key == "published_at":
            epoch_ms = iso_to_epoch_ms(str(value))
            fields[field_name] = epoch_ms if epoch_ms is not None else value
        elif key == "title":
            fields[field_name] = [{"text": str(value), "type": "text"}]
        else:
            fields[field_name] = value
    return {"fields": fields}


def convert_payload(payload: Dict[str, object]) -> Dict[str, object]:
    fetched_at = normalize_timestamp(payload.get("fetched_at")) or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    articles = payload.get("articles") or []
    source_items = [build_source_item(article, fetched_at) for article in articles]

    return {
        "fetched_at": fetched_at,
        "total": len(source_items),
        "source_items": source_items,
        "bitable_records": [bitable_record(item) for item in source_items],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build normalized source_item records from fetched AI news JSON.")
    parser.add_argument("--input", help="Path to fetcher JSON payload. Reads stdin when omitted.")
    parser.add_argument(
        "--format",
        choices=("source_items", "bitable_records", "full"),
        default="full",
        help="Output only source items, only Feishu-style records, or the full payload.",
    )
    parser.add_argument(
        "--field-language",
        choices=("internal", "zh"),
        default="zh",
        help="Field names for bitable_records. `zh` matches the Chinese headers used in Feishu.",
    )
    return parser.parse_args()


def read_payload(path: Optional[str]) -> Dict[str, object]:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def main() -> int:
    args = parse_args()
    payload = read_payload(args.input)
    converted = convert_payload(payload)

    if args.field_language == "internal":
        converted["bitable_records"] = [{"fields": item} for item in converted["source_items"]]

    if args.format == "source_items":
        output = converted["source_items"]
    elif args.format == "bitable_records":
        output = converted["bitable_records"]
    else:
        output = converted

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
