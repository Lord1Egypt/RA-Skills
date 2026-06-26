#!/usr/bin/env python3
"""Collect AI hotspot candidates from public RSS/Atom feeds.

The script intentionally performs collection and coarse filtering only.
An agent should still verify, rank, and summarize the final briefing.
"""

from __future__ import annotations

import argparse
import email.utils
import html
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable


GLOBAL_FEEDS = [
    "https://openai.com/news/rss.xml",
    "https://deepmind.google/blog/rss.xml",
    "https://blog.google/technology/ai/rss/",
    "https://huggingface.co/blog/feed.xml",
    "https://www.technologyreview.com/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/index.xml",
    "http://feeds.venturebeat.com/VentureBeat",
    "https://export.arxiv.org/rss/cs.AI",
    "https://export.arxiv.org/rss/cs.CL",
    "https://export.arxiv.org/rss/cs.LG",
]

CHINA_FEEDS = [
    "https://36kr.com/feed",
    "https://www.ifanr.com/feed",
    "https://www.infoq.cn/rss/",
    "https://www.leiphone.com/feed/categoryRss/name/ai",
    "https://www.leiphone.com/feed/categoryRss/name/robot",
    "https://www.leiphone.com/feed/categoryRss/name/chips",
    "https://news.google.com/rss/search?q=%E4%B8%AD%E5%9B%BD+AI+OR+%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD+OR+%E5%A4%A7%E6%A8%A1%E5%9E%8B&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=DeepSeek+OR+%E9%80%9A%E4%B9%89%E5%8D%83%E9%97%AE+OR+%E6%96%87%E5%BF%83%E4%B8%80%E8%A8%80+OR+%E8%85%BE%E8%AE%AF%E6%B7%B7%E5%85%83+OR+%E8%B1%86%E5%8C%85+OR+Kimi&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
]

KEYWORDS = [
    "ai",
    "artificial intelligence",
    "agent",
    "anthropic",
    "benchmark",
    "chatgpt",
    "claude",
    "copilot",
    "deepmind",
    "diffusion",
    "gpt",
    "gpu",
    "hugging face",
    "language model",
    "llm",
    "machine learning",
    "model",
    "multimodal",
    "openai",
    "reasoning",
    "robotics",
    "safety",
    "transformer",
    "人工智能",
    "大模型",
    "生成式",
    "智能体",
    "多模态",
    "推理",
    "开源模型",
    "具身智能",
    "机器人",
    "自动驾驶",
    "智算",
    "算力",
    "芯片",
    "备案",
    "监管",
    "deepseek",
    "通义",
    "千问",
    "文心",
    "混元",
    "豆包",
    "kimi",
    "智谱",
    "月之暗面",
    "minimax",
    "阶跃星辰",
    "百川",
    "商汤",
    "讯飞",
    "盘古",
    "魔搭",
]

CHINA_ENTITY_KEYWORDS = [
    "中国",
    "国产",
    "国内",
    "北京",
    "上海",
    "深圳",
    "杭州",
    "百度",
    "阿里",
    "腾讯",
    "字节",
    "华为",
    "科大讯飞",
    "商汤",
    "旷视",
    "云从",
    "寒武纪",
    "壁仞",
    "摩尔线程",
    "deepseek",
    "通义",
    "千问",
    "文心",
    "混元",
    "豆包",
    "kimi",
    "智谱",
    "月之暗面",
    "minimax",
    "阶跃星辰",
    "百川",
    "零一万物",
    "面壁智能",
    "稀宇",
    "可灵",
    "即梦",
    "魔搭",
    "备案",
    "工信部",
    "网信办",
]

CHINA_CORE_SUBJECT_KEYWORDS = [
    "百度",
    "阿里",
    "腾讯",
    "字节",
    "华为",
    "科大讯飞",
    "商汤",
    "寒武纪",
    "壁仞",
    "摩尔线程",
    "deepseek",
    "通义",
    "千问",
    "文心",
    "混元",
    "豆包",
    "kimi",
    "智谱",
    "月之暗面",
    "minimax",
    "阶跃星辰",
    "百川",
    "零一万物",
    "面壁智能",
    "可灵",
    "即梦",
    "魔搭",
    "工信部",
    "网信办",
]

CHINA_GEO_MARKET_KEYWORDS = [
    "中国",
    "国产",
    "国内",
    "北京",
    "上海",
    "深圳",
    "杭州",
    "港股",
    "科创板",
    "a股",
]

FOREIGN_AI_ORG_KEYWORDS = [
    "anthropic",
    "claude",
    "openai",
    "chatgpt",
    "google",
    "deepmind",
    "gemini",
    "meta",
    "llama",
    "microsoft",
    "copilot",
    "nvidia",
    "xai",
    "grok",
]


@dataclass
class Candidate:
    title: str
    link: str
    source: str
    region: str
    china_core_subject: bool
    published: str | None
    summary: str
    score: int


def fetch(url: str, timeout: int = 4, insecure: bool = False) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Codex AI hot news collector/1.0"},
    )
    context = ssl._create_unverified_context() if insecure else None
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        return response.read()


def text_of(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return html.unescape(re.sub(r"\s+", " ", node.text)).strip()


def parse_date(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(raw)
        if parsed is not None:
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        pass
    try:
        normalized = raw.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    return None


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def keyword_score(text: str) -> int:
    lowered = text.lower()
    return sum(1 for keyword in KEYWORDS if keyword in lowered)


def china_entity_score(text: str) -> int:
    lowered = text.lower()
    return min(5, sum(1 for keyword in CHINA_ENTITY_KEYWORDS if keyword.lower() in lowered))


def has_china_core_subject(text: str) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in CHINA_CORE_SUBJECT_KEYWORDS)


def has_china_market_context(text: str) -> bool:
    lowered = text.lower()
    if has_china_core_subject(text):
        return True
    if looks_like_foreign_only_ai_story(text):
        return False
    return any(keyword.lower() in lowered for keyword in CHINA_GEO_MARKET_KEYWORDS)


def looks_like_foreign_only_ai_story(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in FOREIGN_AI_ORG_KEYWORDS)


def score_candidate(text: str, region: str) -> int:
    score = keyword_score(text)
    if region != "china":
        return score
    if has_china_core_subject(text):
        score += china_entity_score(text)
    elif has_china_market_context(text):
        score += min(2, china_entity_score(text))
    elif looks_like_foreign_only_ai_story(text):
        score -= 12
    return max(0, score)


def source_name(feed_url: str) -> str:
    host = re.sub(r"^https?://", "", feed_url).split("/", 1)[0]
    return host.removeprefix("www.")


def iter_items(feed_url: str, payload: bytes, region: str) -> Iterable[Candidate]:
    root = ET.fromstring(payload)
    source = source_name(feed_url)

    if root.tag.lower().endswith("rss"):
        items = root.findall("./channel/item")
        for item in items:
            title = text_of(item.find("title"))
            link = text_of(item.find("link")) or text_of(item.find("guid"))
            summary = strip_tags(text_of(item.find("description")))
            published_raw = text_of(item.find("pubDate"))
            published = parse_date(published_raw)
            clipped_summary = summary[:500]
            searchable = f"{title} {clipped_summary}"
            score = score_candidate(searchable, region)
            china_core = region == "china" and has_china_core_subject(searchable)
            if score:
                yield Candidate(
                    title=title,
                    link=link,
                    source=source,
                    region=region,
                    china_core_subject=china_core,
                    published=published.isoformat() if published else None,
                    summary=clipped_summary,
                    score=score,
                )
        return

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = text_of(entry.find("atom:title", ns))
        link_node = entry.find("atom:link[@href]", ns) or entry.find("atom:link", ns)
        link = link_node.attrib.get("href", "") if link_node is not None else ""
        summary = strip_tags(text_of(entry.find("atom:summary", ns)))
        published_raw = text_of(entry.find("atom:published", ns)) or text_of(
            entry.find("atom:updated", ns)
        )
        published = parse_date(published_raw)
        clipped_summary = summary[:500]
        searchable = f"{title} {clipped_summary}"
        score = score_candidate(searchable, region)
        china_core = region == "china" and has_china_core_subject(searchable)
        if score:
            yield Candidate(
                title=title,
                link=link,
                source=source,
                region=region,
                china_core_subject=china_core,
                published=published.isoformat() if published else None,
                summary=clipped_summary,
                score=score,
            )


def published_dt(candidate: Candidate) -> datetime | None:
    if not candidate.published:
        return None
    try:
        return datetime.fromisoformat(candidate.published)
    except ValueError:
        return None


def unique_key(candidate: Candidate) -> str:
    title = re.sub(r"[^\w\u4e00-\u9fff ]+", "", candidate.title.lower())
    words = [word for word in title.split() if len(word) > 3]
    return " ".join(words[:10])


def selected_feeds(region_filter: str) -> list[tuple[str, str]]:
    feeds: list[tuple[str, str]] = []
    if region_filter in ("all", "global"):
        feeds.extend((feed, "global") for feed in GLOBAL_FEEDS)
    if region_filter in ("all", "china"):
        feeds.extend((feed, "china") for feed in CHINA_FEEDS)
    return feeds


def collect(
    hours: int,
    limit: int,
    insecure: bool,
    region_filter: str,
) -> tuple[list[Candidate], list[str]]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    candidates: list[Candidate] = []
    errors: list[str] = []

    for feed, region in selected_feeds(region_filter):
        try:
            payload = fetch(feed, insecure=insecure)
            for candidate in iter_items(feed, payload, region):
                published = published_dt(candidate)
                if published is None or published >= cutoff:
                    candidates.append(candidate)
        except (ET.ParseError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            errors.append(f"{feed}: {exc}")

    deduped: dict[str, Candidate] = {}
    for candidate in candidates:
        key = unique_key(candidate) or candidate.link or candidate.title
        current = deduped.get(key)
        if current is None or candidate.score > current.score:
            deduped[key] = candidate

    ranked = sorted(
        deduped.values(),
        key=lambda item: (
            item.china_core_subject,
            item.score,
            published_dt(item) or datetime.min.replace(tzinfo=timezone.utc),
        ),
        reverse=True,
    )
    return ranked[:limit], errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect AI hotspot candidates.")
    parser.add_argument("--hours", type=int, default=24, help="Freshness window in hours.")
    parser.add_argument("--limit", type=int, default=30, help="Maximum candidates to output.")
    parser.add_argument(
        "--region",
        choices=("all", "global", "china"),
        default="all",
        help="Feed region to collect.",
    )
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification only for local debugging.",
    )
    args = parser.parse_args()

    candidates, errors = collect(args.hours, args.limit, args.insecure, args.region)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_hours": args.hours,
        "candidates": [asdict(candidate) for candidate in candidates],
        "errors": errors,
    }
    data = json.dumps(payload, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(data + "\n")
    else:
        print(data)
    return 0 if candidates else 2


if __name__ == "__main__":
    sys.exit(main())
