#!/usr/bin/env python3
"""
Normalize agent-reach list-page output into structured article records.

Accepted input:
1. JSON array/dict produced by an agent step
2. Lightweight markdown/text blocks with title/link/time/summary hints
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_summary(value: Optional[str], title: str) -> str:
    text = clean_text(value)
    if not text:
        return ""
    noise_patterns = (
        "advertisement",
        "recommended",
        "read more",
        "subscribe",
        "cookie",
        "相关阅读",
        "推荐阅读",
        "广告",
    )
    lowered = text.lower()
    if any(pattern in lowered for pattern in noise_patterns):
        return ""
    if clean_text(title) == text:
        return ""
    return text


def current_local_now() -> datetime:
    return datetime.now(LOCAL_TZ)


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=LOCAL_TZ)
    return value.astimezone(timezone.utc)


def adjust_yearless_candidate(candidate: datetime, now_local: datetime) -> datetime:
    if candidate.tzinfo is None:
        candidate = candidate.replace(tzinfo=LOCAL_TZ)
    if candidate - now_local > timedelta(days=2):
        candidate = candidate.replace(year=candidate.year - 1)
    return candidate


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None

    raw = clean_text(date_str)
    lowered = raw.lower()
    now_local = current_local_now()

    iso_candidate = raw.replace("Z", "+00:00")
    try:
        return normalize_datetime(datetime.fromisoformat(iso_candidate))
    except Exception:
        pass

    for fmt in (
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M",
        "%Y.%m.%d",
        "%Y.%m.%d %H:%M",
        "%B %d, %Y",
        "%B %d, %Y %H:%M",
        "%b %d, %Y",
        "%b %d, %Y %H:%M",
        "%d %B %Y",
        "%d %B %Y %H:%M",
        "%d %b %Y",
        "%d %b %Y %H:%M",
    ):
        try:
            return normalize_datetime(datetime.strptime(raw, fmt))
        except ValueError:
            continue

    # English month-day without year (e.g. "Mar 18", "March 18")
    en_month_day_patterns = (
        (r"^(?P<month_name>[A-Z][a-z]+)\s+(?P<day>\d{1,2})$", True),
    )
    for pattern, _ in en_month_day_patterns:
        match = re.match(pattern, raw)
        if not match:
            continue
        month_name = match.group("month_name")
        day = int(match.group("day"))
        for mfmt in ("%B", "%b"):
            try:
                month = datetime.strptime(month_name, mfmt).month
                candidate = datetime(now_local.year, month, day, tzinfo=LOCAL_TZ)
                candidate = adjust_yearless_candidate(candidate, now_local)
                return normalize_datetime(candidate)
            except ValueError:
                continue

    chinese_patterns = (
        (r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2}))?", True),
        (r"(?P<month>\d{1,2})月(?P<day>\d{1,2})日(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2}))?", False),
    )
    for pattern, has_year in chinese_patterns:
        match = re.search(pattern, raw)
        if not match:
            continue
        year = int(match.group("year")) if has_year else now_local.year
        month = int(match.group("month"))
        day = int(match.group("day"))
        hour = int(match.group("hour") or 0)
        minute = int(match.group("minute") or 0)
        try:
            candidate = datetime(year, month, day, hour, minute, tzinfo=LOCAL_TZ)
            if not has_year:
                candidate = adjust_yearless_candidate(candidate, now_local)
            return normalize_datetime(candidate)
        except ValueError:
            continue

    month_day_patterns = (
        r"(?P<month>\d{1,2})/(?P<day>\d{1,2})(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2}))?",
        r"(?P<month>\d{1,2})-(?P<day>\d{1,2})(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2}))?",
    )
    for pattern in month_day_patterns:
        match = re.search(pattern, raw)
        if not match:
            continue
        month = int(match.group("month"))
        day = int(match.group("day"))
        hour = int(match.group("hour") or 0)
        minute = int(match.group("minute") or 0)
        try:
            candidate = datetime(now_local.year, month, day, hour, minute, tzinfo=LOCAL_TZ)
            candidate = adjust_yearless_candidate(candidate, now_local)
            return normalize_datetime(candidate)
        except ValueError:
            continue

    relative_patterns = (
        (r"(\d+)\s*(分钟|mins?|minutes?)\s*(前|ago)?", "minutes"),
        (r"(\d+)\s*(小时|hours?|hrs?)\s*(前|ago)?", "hours"),
        (r"(\d+)\s*(天|days?)\s*(前|ago)?", "days"),
    )
    for pattern, unit in relative_patterns:
        match = re.search(pattern, lowered)
        if not match:
            continue
        amount = int(match.group(1))
        return normalize_datetime(now_local - timedelta(**{unit: amount}))

    relative_day_patterns = (
        (r"^(今天|today)(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2}))?$", 0),
        (r"^(昨天|yesterday)(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{1,2}))?$", 1),
    )
    for pattern, day_offset in relative_day_patterns:
        match = re.search(pattern, lowered)
        if not match:
            continue
        base = now_local - timedelta(days=day_offset)
        hour = int(match.group("hour") or base.hour)
        minute = int(match.group("minute") or base.minute)
        candidate = datetime(base.year, base.month, base.day, hour, minute, tzinfo=LOCAL_TZ)
        return normalize_datetime(candidate)
    return None


def article_from_mapping(item: Dict[str, object], default_source: str, fallback_to_now: bool = False) -> Optional[Dict[str, object]]:
    title = clean_text(item.get("title"))
    url = clean_text(item.get("url") or item.get("link"))
    original_time = clean_text(
        item.get("original_time")
        or item.get("date")
        or item.get("time")
        or item.get("published_at_raw")
    )
    summary = normalize_summary(item.get("summary") or item.get("excerpt") or item.get("description"), title)
    source = clean_text(item.get("source")) or default_source
    if not title or not url:
        return None
    if not original_time:
        if not fallback_to_now:
            return None
        original_time = "now"
    parsed_date = parse_date(original_time)
    if not parsed_date:
        if not fallback_to_now:
            return None
        parsed_date = normalize_datetime(current_local_now())
    return {
        "title": title,
        "url": url,
        "date": original_time,
        "summary": summary or None,
        "source": source,
        "parsed_date": parsed_date.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def parse_json_payload(raw: str, default_source: str, fallback_to_now: bool = False) -> Optional[List[Dict[str, object]]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None

    if isinstance(payload, dict):
        if isinstance(payload.get("articles"), list):
            items = payload["articles"]
        else:
            items = [payload]
    elif isinstance(payload, list):
        items = payload
    else:
        return None

    articles = []
    for item in items:
        if not isinstance(item, dict):
            continue
        article = article_from_mapping(item, default_source, fallback_to_now=fallback_to_now)
        if article:
            articles.append(article)
    return articles


_TIME_LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?)"
    r"|^(\d{1,2}月\d{1,2}日(?:\s+\d{1,2}:\d{2})?)"
    r"|^(\d+\s*(?:分钟|小时|天|hours?|mins?|minutes?|days?)\s*(?:前|ago)?)\s*$"
)
_HEADLINE_RE = re.compile(r"\*{0,2}【(.+?)】\*{0,2}")
_NOISE_URLS = re.compile(
    r"/(our|subject|download|vip|fm|invest|usercenter|seek-report|"
    r"information|live|video|topics|activity|station|policy|"
    r"newsflashes/catalog|account)"
)


_GITHUB_NAV_PATHS = re.compile(
    r"^https?://github\.com/(features|solutions|enterprise|team|security|resources|"
    r"login|signup|settings|marketplace|about|pricing|customer-stories|why-github|"
    r"explore|topics|collections|events|sponsors|readme|organizations|trending|"
    r"\.github|apps|codespaces|discussions|notifications|stars|watching|search|new|"
    r"site|docs|blog|changelog|skills|mcp|repositories)(/|$)",
    re.IGNORECASE,
)


def _is_article_url(url: str) -> bool:
    """Filter out navigation/noise URLs, keep article links."""
    if _NOISE_URLS.search(url):
        return False
    if re.search(r"/(detail|p|newsflashes)/\d+", url):
        return True
    if re.search(r"/news/|/blogs?/|/articles?/", url):
        return True
    # OpenAI /index/ article URLs
    if re.search(r"openai\.com/(index|zh-Hans-CN/index)/.+", url):
        return True
    # GitHub repo URLs (trending page items) — exclude known non-repo paths
    if re.match(r"https?://github\.com/[^/]+/[^/]+/?$", url):
        if not _GITHUB_NAV_PATHS.match(url):
            return True
    # Google DeepMind and Cloud blog post URLs
    if re.search(r"deepmind\.google/(discover/)?blog/.+", url):
        return True
    if re.search(r"cloud\.google\.com/blog/.+", url):
        return True
    return False


# Patterns to extract date + title from jina reader link text
# OpenAI: "标题 类别 2026年3月19日"
_OPENAI_LINK_RE = re.compile(
    r"^(.+?)\s+(?:安全|公司|产品|研究|工程|安全防护|政策|Education|Company|Product|Research|Engineering|Safety)\s+"
    r"(\d{4}年\d{1,2}月\d{1,2}日)$"
)
# Anthropic featured: "Category MonDD, YYYY #### Title Description"
_ANTHROPIC_FEATURED_RE = re.compile(
    r"^(?:Product|Announcements|Policy|Research|Company|Safety)\s+"
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4})\s+"
    r"#{1,4}\s+(.+?)(?:\s{2,}(.+))?$"
)
# Anthropic list: "MonDD, YYYY Category Title"
_ANTHROPIC_LIST_RE = re.compile(
    r"^((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4})\s+"
    r"(?:Product|Announcements|Policy|Research|Company|Safety)\s+(.+)$"
)


def _extract_headline_and_summary(link_text: str) -> tuple:
    """Extract headline from 【headline】 pattern or structured link text; rest is summary."""
    match = _HEADLINE_RE.search(link_text)
    if match:
        headline = clean_text(match.group(1))
        rest = link_text[:match.start()] + link_text[match.end():]
        rest = re.sub(r"^\*+|\*+$", "", rest).strip()
        summary = clean_text(rest)
        return headline, summary
    return clean_text(link_text), ""


def _extract_date_from_link_text(link_text: str) -> tuple:
    """Try to extract embedded date from link text for OpenAI/Anthropic patterns.

    Returns (title, date_str, summary) or (None, None, None) if no match.
    """
    # OpenAI pattern: "标题 类别 2026年3月19日"
    m = _OPENAI_LINK_RE.match(link_text.strip())
    if m:
        return clean_text(m.group(1)), clean_text(m.group(2)), ""

    # Anthropic featured: "Category Feb 17, 2026 #### Title Summary"
    m = _ANTHROPIC_FEATURED_RE.match(link_text.strip())
    if m:
        return clean_text(m.group(2)), clean_text(m.group(1)), clean_text(m.group(3) or "")

    # Anthropic list: "Mar 12, 2026 Announcements Title"
    m = _ANTHROPIC_LIST_RE.match(link_text.strip())
    if m:
        return clean_text(m.group(2)), clean_text(m.group(1)), ""

    # Google Cloud Blog pattern: "Category ### Title By Author • N-minute read"
    # or "#### Title" or "Category ##### Title By Author..."
    text = link_text.strip()
    # Strip "By Author • N-minute read" suffix
    text_no_author = re.sub(r"\s+By\s+[^•]+•\s+\d+-minute read$", "", text)
    # Strip heading markers
    text_no_heading = re.sub(r"#{1,6}\s+", "", text_no_author)
    # Strip known category prefixes
    _CLOUD_CATEGORIES = (
        "AI & Machine Learning", "Data Analytics", "Databases", "Compute",
        "Containers & Kubernetes", "Serverless", "Networking", "Infrastructure",
        "Security & Identity", "Application Modernization", "Chrome Enterprise",
        "Threat Intelligence", "Training and Certifications", "DevOps & SRE",
        "Google Cloud", "Workspace",
    )
    cleaned = text_no_heading.strip()
    for cat in _CLOUD_CATEGORIES:
        if cleaned.startswith(cat):
            cleaned = cleaned[len(cat):].strip()
            break
    if cleaned and len(cleaned) > 10 and cleaned != clean_text(link_text):
        return clean_text(cleaned), None, ""

    return None, None, None


def _detect_time(text: str) -> Optional[str]:
    """Check if a line is a standalone time indicator."""
    stripped = text.strip()
    match = _TIME_LINE_RE.match(stripped)
    if match:
        time_part = match.group(1) or match.group(2) or match.group(3)
        if time_part:
            return clean_text(time_part)
    return None


_AUTHOR_TIME_RE = re.compile(
    r"\]\([^)]*\)\s*(\d+\s*(?:分钟|小时|天|hours?|mins?|minutes?|days?)\s*(?:前|ago)?)\s*$"
)


def _extract_time_suffix(text: str) -> Optional[str]:
    """Extract relative time from author+time lines like '[Author](user_url)1小时前'."""
    match = _AUTHOR_TIME_RE.search(text)
    if match:
        return clean_text(match.group(1))
    return None


_INLINE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)\s*")


def parse_markdown_payload(raw: str, default_source: str, fallback_to_now: bool = False) -> List[Dict[str, object]]:
    articles = []
    current: Dict[str, str] = {}
    pending_time: Optional[str] = None
    url_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")

    def flush() -> None:
        nonlocal pending_time
        if not current:
            return
        article = article_from_mapping(current, default_source, fallback_to_now=fallback_to_now)
        if article:
            articles.append(article)
        current.clear()

    for line in raw.splitlines():
        text = clean_text(line)
        if not text:
            # Don't flush if we have a URL but no date yet — 36kr motif pattern:
            # title and summary are in separate paragraphs, time comes on author line.
            if current and "url" in current and "date" not in current:
                continue
            flush()
            continue

        # Detect standalone time lines (e.g. "2026-03-18 23:50 来自 第一财经", "1分钟前")
        detected_time = _detect_time(text)
        if detected_time:
            if current and "url" in current and "date" not in current:
                # Time AFTER a URL (36kr pattern): attach to current article
                current["date"] = detected_time
            else:
                # Time BEFORE a URL (cls.cn pattern): remember for next article
                pending_time = detected_time
            continue

        # Strip inline image markdown before searching for links (handles nested [![img](url) text](url))
        text_for_url = _INLINE_IMAGE_RE.sub("", text)
        url_match = url_pattern.search(text_for_url)
        if not url_match:
            url_match = url_pattern.search(text)
        if url_match:
            url = clean_text(url_match.group(2))
            if _is_article_url(url):
                if current.get("url") == url and "title" in current:
                    # Same URL as current article → this is the summary text (36kr motif pattern)
                    link_text = url_match.group(1)
                    summary_text = clean_text(link_text)
                    if summary_text and summary_text != current.get("title") and not current.get("summary"):
                        current["summary"] = summary_text
                else:
                    flush()
                    link_text = url_match.group(1)
                    # Try structured date extraction (OpenAI/Anthropic/Cloud Blog jina patterns)
                    ext_title, ext_date, ext_summary = _extract_date_from_link_text(link_text)
                    if ext_title:
                        current["title"] = ext_title
                        current["url"] = url
                        if ext_date:
                            current["date"] = ext_date
                        if ext_summary:
                            current["summary"] = ext_summary
                    else:
                        headline, summary = _extract_headline_and_summary(link_text)
                        current["title"] = headline
                        current["url"] = url
                        if summary:
                            current["summary"] = summary
                    if not current.get("date") and pending_time:
                        current["date"] = pending_time
                        pending_time = None
            else:
                # Not an article URL; check for time suffix (36kr author+time line pattern)
                time_suffix = _extract_time_suffix(text)
                if time_suffix and current and "url" in current and "date" not in current:
                    current["date"] = time_suffix
                    flush()
            continue

        if text.startswith("|") and text.endswith("|"):
            parts = [clean_text(part) for part in text.strip("|").split("|")]
            if len(parts) >= 4 and parts[0] not in {"标题", "---"}:
                flush()
                current["title"] = parts[0]
                current["url"] = parts[1]
                current["date"] = parts[2]
                current["summary"] = parts[3]
                flush()
            continue

        lowered = text.lower()
        if lowered.startswith("标题") or lowered.startswith("title"):
            current["title"] = clean_text(text.split(":", 1)[-1].split("：", 1)[-1])
        elif lowered.startswith("链接") or lowered.startswith("原文链接") or lowered.startswith("url") or lowered.startswith("link"):
            current["url"] = clean_text(text.split(":", 1)[-1].split("：", 1)[-1])
        elif lowered.startswith("时间") or lowered.startswith("发布时间") or lowered.startswith("原始时间") or lowered.startswith("date") or lowered.startswith("time"):
            current["date"] = clean_text(text.split(":", 1)[-1].split("：", 1)[-1])
        elif lowered.startswith("摘要") or lowered.startswith("summary") or lowered.startswith("导语"):
            current["summary"] = clean_text(text.split(":", 1)[-1].split("：", 1)[-1])
        elif current and "url" in current and "summary" not in current:
            # Body text after a URL match (e.g. 36kr flash body paragraphs)
            if len(text) > 20 and not text.startswith(("收藏", "阅 ", "评论", "分享", "微博", "微信", "![", "[](http")):
                current["summary"] = text

    flush()
    return articles


def parse_input(raw: str, default_source: str, fallback_to_now: bool = False) -> List[Dict[str, object]]:
    parsed = parse_json_payload(raw, default_source, fallback_to_now=fallback_to_now)
    if parsed is not None:
        return parsed
    return parse_markdown_payload(raw, default_source, fallback_to_now=fallback_to_now)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize agent-reach text into structured AI news records.")
    parser.add_argument("--input", help="Path to raw agent-reach output. Reads stdin when omitted.")
    parser.add_argument("--source", required=True, help="Default source name when input items do not include it.")
    parser.add_argument("--fallback-to-now", action="store_true", help="Use current time when no publish time is found (e.g. GitHub Trending).")
    return parser.parse_args()


def read_input(path: Optional[str]) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def main() -> int:
    args = parse_args()
    raw = read_input(args.input)
    articles = parse_input(raw, args.source, fallback_to_now=args.fallback_to_now)
    payload = {
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "articles": articles,
        "total": len(articles),
        "source_group": "public-web",
        "requested_sources": [args.source],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
