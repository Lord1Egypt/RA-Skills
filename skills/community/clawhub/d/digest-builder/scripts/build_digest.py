#!/usr/bin/env python3
"""Build a structured digest from FreshRSS items.

Pipeline stages:
1. URL exact deduplication
2. Similar-content clustering and deduplication
3. Article body fetch
4. Quality checks
5. Noise filtering
6. Summary generation
7. Initial ranking and document output
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


TRACKING_PARAMS = {
    "cmpid",
    "fbclid",
    "gclid",
    "igshid",
    "mkt_tok",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_src",
    "rss",
    "spm",
    "src",
    "source",
    "tag",
    "trk",
}

MARKETING_PATTERNS = [
    "扫码",
    "加群",
    "进群",
    "优惠",
    "折扣",
    "抽奖",
    "报名",
    "立即报名",
    "课程",
    "社群",
    "会员",
    "推广",
    "广告",
    "sponsored",
    "sign up",
    "subscribe",
    "newsletter",
    "promo",
    "discount",
    "webinar",
]

ACCESS_PATTERNS = [
    "enable javascript",
    "please enable javascript",
    "access denied",
    "forbidden",
    "登录后查看",
    "请登录",
    "subscribe to continue",
    "cookie policy",
]

LOW_SIGNAL_PATTERNS = [
    "comments",
    "求推荐",
    "求助",
    "bro-mode",
    "纯娱乐向",
    "摸鱼",
]

SOURCE_WEIGHTS = {
    "readhub": 1.40,
    "infoq": 1.32,
    "the new stack": 1.24,
    "techcrunch": 1.20,
    "stanford": 1.18,
    "slack engineering": 1.16,
    "cloudflare": 1.14,
    "hacker news": 1.02,
    "36kr": 1.05,
    "量子位": 1.05,
    "v2ex": 0.76,
}

TOPIC_RULES = {
    "AI": ["ai", "llm", "agent", "模型", "大模型", "openai", "anthropic", "claude", "gemini", "siri"],
    "安全": ["安全", "漏洞", "exploit", "breach", "supply chain", "secret", "风险", "scanner"],
    "开源": ["open source", "开源", "github", "release", "repo"],
    "基础设施": ["cloud", "kubernetes", "vault", "tracing", "otel", "infra", "platform", "数据湖"],
    "公司动态": ["融资", "ipo", "投资", "离职", "挖角", "软银", "meta", "apple", "华为", "openai"],
    "开发工具": ["skill", "copilot", "codex", "devops", "tool", "workflow", "ci/cd", "sdk"],
    "研究治理": ["research", "论文", "neurips", "治理", "study", "同行评审"],
}

RISK_RULES = {
    "security": ["安全", "漏洞", "attack", "exploit", "风险", "secret", "supply chain"],
    "governance": ["治理", "policy", "合规", "监管", "审查"],
    "availability": ["宕机", "incident", "latency", "故障", "稳定性"],
}


class BlockTextExtractor(HTMLParser):
    """Convert HTML into text blocks while ignoring obvious boilerplate tags."""

    BLOCK_TAGS = {
        "article",
        "blockquote",
        "br",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "tr",
        "ul",
    }
    SKIP_TAGS = {"head", "noscript", "script", "style", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {key.lower(): value or "" for key, value in attrs}
        lowered = tag.lower()
        if lowered in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if lowered in self.BLOCK_TAGS:
            self.parts.append("\n")
        if lowered == "title":
            self.in_title = True
        if lowered == "meta":
            name = attrs_map.get("name") or attrs_map.get("property") or ""
            content = attrs_map.get("content") or ""
            if name and content:
                self.meta[name.lower()] = content.strip()

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
            return
        if lowered in self.BLOCK_TAGS:
            self.parts.append("\n")
        if lowered == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.skip_depth > 0:
            return
        cleaned = collapse_ws(html.unescape(data))
        if not cleaned:
            return
        if self.in_title:
            self.title_parts.append(cleaned)
        self.parts.append(cleaned)


@dataclass
class Candidate:
    item_id: str
    title: str
    raw_url: str
    normalized_url: str
    source: str
    origin_feed: str
    origin_system: str
    published_at: str
    published_ts: int
    freshrss_categories: list[str]
    summary_html: str
    summary_text: str
    source_weight: float
    title_tokens: set[str]
    body_text: str = ""
    fetched_url: str = ""
    body_fetch_status: str = "pending"
    body_fetch_error: str = ""
    body_length: int = 0
    content_language: str = "unknown"
    content_title: str = ""
    meta_description: str = ""
    quality_score: int = 0
    quality_flags: list[str] | None = None
    noise_flags: list[str] | None = None
    filtered_reason: str = ""
    cluster_id: str = ""
    duplicate_item_ids: list[str] | None = None
    related_item_ids: list[str] | None = None
    topic_tags: list[str] | None = None
    risk_tags: list[str] | None = None
    actionability: str = "low"
    public_importance: int = 1
    personal_relevance: int = 1
    ranking_reason: str = ""
    summary: str = ""
    summary_zh: str = ""
    raw_excerpt: str = ""
    quality_passed: bool = True
    rank_score: float = 0.0

    def as_output(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "cluster_id": self.cluster_id,
            "title": self.title,
            "source": self.source,
            "published_at": self.published_at,
            "raw_url": self.raw_url,
            "normalized_url": self.normalized_url,
            "summary": self.summary,
            "summary_zh": self.summary_zh,
            "topic_tags": self.topic_tags or [],
            "risk_tags": self.risk_tags or [],
            "actionability": self.actionability,
            "public_importance": self.public_importance,
            "personal_relevance": self.personal_relevance,
            "ranking_reason": self.ranking_reason,
            "origin_system": self.origin_system,
            "origin_feed": self.origin_feed,
            "freshrss_categories": self.freshrss_categories,
            "quality_score": self.quality_score,
            "quality_flags": self.quality_flags or [],
            "noise_flags": self.noise_flags or [],
            "body_fetch_status": self.body_fetch_status,
            "fetched_url": self.fetched_url,
            "body_length": self.body_length,
            "duplicate_item_ids": self.duplicate_item_ids or [],
            "related_item_ids": self.related_item_ids or [],
            "content_language": self.content_language,
            "raw_excerpt": self.raw_excerpt,
            "rank_score": round(self.rank_score, 2),
        }


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_escape(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def canonical_link(item: dict[str, Any]) -> str:
    for key in ("canonical", "alternate"):
        values = item.get(key) or []
        if values and isinstance(values, list):
            first = values[0]
            if isinstance(first, dict) and first.get("href"):
                return str(first["href"])
    return ""


def parse_published(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().isoformat()


def normalize_url(url: str) -> str:
    if not url:
        return ""
    parsed = urllib.parse.urlsplit(url.strip())
    scheme = (parsed.scheme or "https").lower()
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        return url.strip()
    port = parsed.port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc = f"{host}:{port}"
    else:
        netloc = host
    path = parsed.path or "/"
    path = re.sub(r"/{2,}", "/", path)
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=False)
    filtered_pairs = []
    for key, value in query_pairs:
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in TRACKING_PARAMS:
            continue
        filtered_pairs.append((key, value))
    filtered_pairs.sort()
    query = urllib.parse.urlencode(filtered_pairs, doseq=True)
    return urllib.parse.urlunsplit((scheme, netloc, path, query, ""))


def normalized_title(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"https?://\S+", "", lowered)
    lowered = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", " ", lowered)
    return collapse_ws(lowered)


def build_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for token in re.findall(r"[a-z0-9]{2,}|[\u4e00-\u9fff]{2,}", text.lower()):
        if re.search(r"[\u4e00-\u9fff]", token):
            tokens.add(token)
            if len(token) <= 8:
                for index in range(len(token) - 1):
                    tokens.add(token[index : index + 2])
        else:
            if token.endswith("s") and len(token) > 4:
                token = token[:-1]
            tokens.add(token)
    return {token for token in tokens if token}


def detect_language(text: str) -> str:
    zh_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_count = len(re.findall(r"[A-Za-z]", text))
    if zh_count == 0 and latin_count == 0:
        return "unknown"
    if zh_count * 2 >= max(1, latin_count):
        return "zh"
    if latin_count * 2 >= max(1, zh_count):
        return "en"
    return "mixed"


def keyword_in_text(text: str, keyword: str) -> bool:
    if re.search(r"[\u4e00-\u9fff]", keyword):
        return keyword in text
    return re.search(rf"\b{re.escape(keyword.lower())}\b", text) is not None


def html_to_text(text: str) -> tuple[str, str, str]:
    parser = BlockTextExtractor()
    parser.feed(text)
    parser.close()
    joined = "\n".join(line.strip() for line in "".join(parser.parts).splitlines())
    lines: list[str] = []
    for line in joined.splitlines():
        line = collapse_ws(line)
        if not line:
            continue
        lowered = line.lower()
        if any(token in lowered for token in ("cookie", "privacy policy", "accept all", "advertisement")):
            continue
        lines.append(line)
    deduped: list[str] = []
    seen: set[str] = set()
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        deduped.append(line)
    body = "\n".join(deduped)
    title = collapse_ws(" ".join(parser.title_parts)) or collapse_ws(parser.meta.get("og:title", ""))
    description = collapse_ws(
        parser.meta.get("description", "")
        or parser.meta.get("og:description", "")
        or parser.meta.get("twitter:description", "")
    )
    return body, title, description


def clean_excerpt(text: str, limit: int = 280) -> str:
    cleaned = collapse_ws(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def item_source(item: dict[str, Any]) -> str:
    origin = item.get("origin") or {}
    return str(origin.get("title") or origin.get("streamId") or "Unknown")


def source_weight(source: str, url: str) -> float:
    lowered = source.lower()
    domain = urllib.parse.urlsplit(url).hostname or ""
    haystack = f"{lowered} {domain.lower()}"
    for key, value in SOURCE_WEIGHTS.items():
        if keyword_in_text(haystack, key):
            return value
    return 1.0


def parse_candidates(items: list[dict[str, Any]]) -> list[Candidate]:
    parsed: list[Candidate] = []
    for item in items:
        raw_url = canonical_link(item)
        normalized = normalize_url(raw_url)
        raw_summary = item.get("summary") or {}
        summary_html = raw_summary.get("content", "") if isinstance(raw_summary, dict) else ""
        summary_text = clean_excerpt(html_to_text(summary_html)[0], limit=1200)
        title = str(item.get("title") or "(Untitled)")
        published_ts = int(item.get("published") or 0)
        source = item_source(item)
        categories = [str(value) for value in item.get("categories") or []]
        parsed.append(
            Candidate(
                item_id=str(item.get("id") or ""),
                title=title,
                raw_url=raw_url,
                normalized_url=normalized or normalized_title(title),
                source=source,
                origin_feed=source,
                origin_system="freshrss",
                published_at=parse_published(published_ts) if published_ts else "",
                published_ts=published_ts,
                freshrss_categories=categories,
                summary_html=summary_html,
                summary_text=summary_text,
                source_weight=source_weight(source, raw_url),
                title_tokens=build_tokens(normalized_title(title)),
                raw_excerpt=clean_excerpt(summary_text or title, limit=220),
                quality_flags=[],
                noise_flags=[],
                duplicate_item_ids=[],
                related_item_ids=[],
                topic_tags=[],
                risk_tags=[],
            )
        )
    return parsed


def dedupe_exact_urls(candidates: list[Candidate]) -> tuple[list[Candidate], list[dict[str, Any]]]:
    buckets: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        key = candidate.normalized_url or normalized_title(candidate.title)
        buckets.setdefault(key, []).append(candidate)

    kept: list[Candidate] = []
    removed: list[dict[str, Any]] = []
    for key, grouped in buckets.items():
        grouped.sort(
            key=lambda item: (
                item.source_weight,
                len(item.summary_text),
                item.published_ts,
            ),
            reverse=True,
        )
        primary = grouped[0]
        primary.duplicate_item_ids = [item.item_id for item in grouped[1:]]
        kept.append(primary)
        for duplicate in grouped[1:]:
            removed.append(
                {
                    "item_id": duplicate.item_id,
                    "title": duplicate.title,
                    "source": duplicate.source,
                    "raw_url": duplicate.raw_url,
                    "normalized_url": key,
                    "reason": "exact_url_duplicate",
                    "kept_item_id": primary.item_id,
                }
            )
    return kept, removed


def fetch_url(url: str, timeout: int) -> tuple[str, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
            raise ValueError(f"Unsupported content type: {content_type}")
        payload = response.read(1_500_000).decode("utf-8", errors="replace")
        return payload, response.geturl(), content_type


def enrich_candidate(candidate: Candidate, timeout: int) -> Candidate:
    if not candidate.raw_url:
        candidate.body_fetch_status = "missing_url"
        candidate.body_fetch_error = "missing canonical url"
        candidate.body_text = candidate.summary_text
        candidate.body_length = len(candidate.body_text)
        candidate.content_language = detect_language(candidate.summary_text)
        return candidate

    try:
        html_text, final_url, _ = fetch_url(candidate.raw_url, timeout=timeout)
        body_text, content_title, description = html_to_text(html_text)
        host = urllib.parse.urlsplit(final_url or candidate.raw_url).hostname or ""
        if "github.com" in host and description:
            generic_markers = ("appearance settings", "github copilot", "sign in", "navigation menu")
            if not body_text or any(marker in body_text.lower() for marker in generic_markers):
                body_text = description
        candidate.body_text = body_text
        candidate.body_length = len(body_text)
        candidate.fetched_url = final_url
        candidate.content_title = content_title
        candidate.meta_description = description
        candidate.body_fetch_status = "fetched" if body_text else "empty_body"
        candidate.content_language = detect_language(
            "\n".join(part for part in (body_text[:4000], candidate.summary_text, candidate.title) if part)
        )
    except urllib.error.HTTPError as exc:
        candidate.body_fetch_status = "http_error"
        candidate.body_fetch_error = f"http_{exc.code}"
        candidate.body_text = candidate.summary_text
        candidate.body_length = len(candidate.body_text)
        candidate.content_language = detect_language(candidate.summary_text)
    except urllib.error.URLError as exc:
        candidate.body_fetch_status = "network_error"
        candidate.body_fetch_error = str(exc.reason)
        candidate.body_text = candidate.summary_text
        candidate.body_length = len(candidate.body_text)
        candidate.content_language = detect_language(candidate.summary_text)
    except Exception as exc:  # noqa: BLE001
        candidate.body_fetch_status = "fetch_error"
        candidate.body_fetch_error = str(exc)
        candidate.body_text = candidate.summary_text
        candidate.body_length = len(candidate.body_text)
        candidate.content_language = detect_language(candidate.summary_text)

    if not candidate.body_text:
        candidate.body_text = candidate.summary_text
        candidate.body_length = len(candidate.body_text)

    return candidate


def fetch_bodies(candidates: list[Candidate], timeout: int, concurrency: int) -> None:
    if not candidates:
        return
    workers = max(1, min(concurrency, len(candidates)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(enrich_candidate, candidate, timeout): candidate for candidate in candidates}
        for future in as_completed(futures):
            future.result()


def marketing_hits(text: str) -> int:
    lowered = text.lower()
    return sum(1 for pattern in MARKETING_PATTERNS if pattern.lower() in lowered)


def accessibility_hits(text: str) -> int:
    lowered = text.lower()
    return sum(1 for pattern in ACCESS_PATTERNS if pattern in lowered)


def quality_check(candidate: Candidate) -> None:
    score = 40.0
    flags: list[str] = []
    noise_flags: list[str] = []
    text = candidate.body_text or candidate.summary_text
    excerpt = text[:2400]
    body_length = len(text)
    url_host = urllib.parse.urlsplit(candidate.raw_url or candidate.fetched_url).hostname or ""

    if candidate.body_fetch_status == "fetched":
        score += 18
    elif candidate.body_fetch_status in {"network_error", "http_error", "fetch_error", "empty_body"}:
        flags.append("body_fetch_failed")
        score -= 14

    if body_length >= 4000:
        score += 20
    elif body_length >= 1800:
        score += 14
    elif body_length >= 800:
        score += 8
    elif body_length >= 240:
        score += 2
    else:
        flags.append("short_body")
        score -= 18

    if candidate.summary_text and len(candidate.summary_text) >= 80:
        score += 6
    else:
        flags.append("weak_feed_summary")
        score -= 4

    if candidate.content_language == "en":
        flags.append("needs_manual_translation")

    marketing = marketing_hits("\n".join([candidate.title, candidate.summary_text, excerpt[:1200]]))
    if marketing >= 4:
        noise_flags.append("marketing_heavy")
        score -= 30
    elif marketing >= 2:
        noise_flags.append("marketing_signal")
        score -= 12

    access_issues = accessibility_hits(excerpt)
    if access_issues >= 1 and body_length < 500:
        flags.append("body_access_limited")
        score -= 12

    title_lowered = candidate.title.lower()
    if any(pattern in title_lowered for pattern in LOW_SIGNAL_PATTERNS):
        noise_flags.append("low_signal_title")
        score -= 20

    if re.search(r"招聘|hiring|job[s]?\b|remote work|远程工作|兼职", title_lowered):
        noise_flags.append("recruitment_post")
        score -= 26

    if candidate.summary_text.lower() == "comments" and (body_length < 500 or "news.ycombinator.com" in url_host):
        noise_flags.append("comments_only")
        score -= 22

    if "v2ex" in candidate.source.lower() and body_length < 180:
        noise_flags.append("short_forum_post")
        score -= 16

    unique_ratio = len(set(excerpt.split())) / max(1, len(excerpt.split()))
    if unique_ratio < 0.35 and len(excerpt.split()) > 40:
        flags.append("repetitive_content")
        score -= 8

    candidate.quality_score = max(0, min(100, int(round(score))))
    candidate.quality_flags = flags
    candidate.noise_flags = noise_flags
    candidate.quality_passed = candidate.quality_score >= 35 and "marketing_heavy" not in noise_flags


def filter_noise(candidates: list[Candidate]) -> tuple[list[Candidate], list[dict[str, Any]]]:
    kept: list[Candidate] = []
    removed: list[dict[str, Any]] = []
    for candidate in candidates:
        reason = ""
        if not candidate.quality_passed:
            reason = "quality_below_threshold"
        elif "comments_only" in (candidate.noise_flags or []):
            reason = "comments_only"
        elif "marketing_heavy" in (candidate.noise_flags or []):
            reason = "marketing_heavy"
        elif "recruitment_post" in (candidate.noise_flags or []):
            reason = "recruitment_post"
        elif "short_forum_post" in (candidate.noise_flags or []) and candidate.quality_score < 48:
            reason = "short_forum_noise"

        if reason:
            candidate.filtered_reason = reason
            removed.append(
                {
                    "item_id": candidate.item_id,
                    "title": candidate.title,
                    "source": candidate.source,
                    "raw_url": candidate.raw_url,
                    "reason": reason,
                    "quality_score": candidate.quality_score,
                    "quality_flags": candidate.quality_flags or [],
                    "noise_flags": candidate.noise_flags or [],
                }
            )
            continue
        kept.append(candidate)
    return kept, removed


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    intersection = len(left & right)
    union = len(left | right)
    return intersection / union if union else 0.0


def build_similarity_tokens(candidate: Candidate) -> set[str]:
    combined = "\n".join(
        part
        for part in (
            normalized_title(candidate.title),
            candidate.summary_text[:500],
            candidate.body_text[:1200],
        )
        if part
    )
    return build_tokens(combined)


def similarity_score(left: Candidate, right: Candidate, left_tokens: set[str], right_tokens: set[str]) -> float:
    title_left = normalized_title(left.title)
    title_right = normalized_title(right.title)
    title_ratio = SequenceMatcher(None, title_left, title_right).ratio()
    token_ratio = jaccard_similarity(left_tokens, right_tokens)
    url_ratio = 1.0 if left.normalized_url == right.normalized_url else 0.0
    same_source_window = abs(left.published_ts - right.published_ts) <= 3 * 24 * 3600

    if url_ratio == 1.0:
        return 1.0
    if title_left and title_left == title_right:
        return 0.98
    if same_source_window and title_ratio >= 0.90:
        return 0.92
    if same_source_window and title_ratio >= 0.82 and token_ratio >= 0.45:
        return 0.86
    if same_source_window and title_ratio >= 0.60 and token_ratio >= 0.70:
        return token_ratio
    if same_source_window and title_ratio >= 0.72 and token_ratio >= 0.32:
        return 0.84
    return title_ratio * 0.6 + token_ratio * 0.4


def cluster_similar_candidates(candidates: list[Candidate]) -> tuple[list[Candidate], list[dict[str, Any]]]:
    if not candidates:
        return [], []

    tokens_map = {candidate.item_id: build_similarity_tokens(candidate) for candidate in candidates}
    parent = {candidate.item_id: candidate.item_id for candidate in candidates}

    def find(item_id: str) -> str:
        while parent[item_id] != item_id:
            parent[item_id] = parent[parent[item_id]]
            item_id = parent[item_id]
        return item_id

    def union(left_id: str, right_id: str) -> None:
        left_root = find(left_id)
        right_root = find(right_id)
        if left_root != right_root:
            parent[right_root] = left_root

    for index, left in enumerate(candidates):
        for right in candidates[index + 1 :]:
            similarity = similarity_score(left, right, tokens_map[left.item_id], tokens_map[right.item_id])
            if similarity >= 0.84:
                union(left.item_id, right.item_id)

    grouped: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        grouped.setdefault(find(candidate.item_id), []).append(candidate)

    kept: list[Candidate] = []
    removed: list[dict[str, Any]] = []
    cluster_number = 0
    for grouped_candidates in grouped.values():
        cluster_number += 1
        grouped_candidates.sort(
            key=lambda item: (
                item.quality_score,
                item.source_weight,
                item.body_length,
                len(item.summary_text),
            ),
            reverse=True,
        )
        primary = grouped_candidates[0]
        primary.cluster_id = f"cluster-{cluster_number:03d}"
        primary.related_item_ids = [item.item_id for item in grouped_candidates[1:]]
        kept.append(primary)
        for duplicate in grouped_candidates[1:]:
            removed.append(
                {
                    "item_id": duplicate.item_id,
                    "title": duplicate.title,
                    "source": duplicate.source,
                    "raw_url": duplicate.raw_url,
                    "reason": "similar_content_duplicate",
                    "kept_item_id": primary.item_id,
                    "cluster_id": primary.cluster_id,
                }
            )
    return kept, removed


def split_sentences(text: str) -> list[str]:
    normalized = re.sub(r"\n+", "\n", text)
    pieces = re.split(r"(?<=[。！？!?；;])\s+|(?<=[.?!])\s+(?=[A-Z0-9])|\n", normalized)
    sentences: list[str] = []
    for piece in pieces:
        cleaned = collapse_ws(piece)
        if len(cleaned) < 18:
            continue
        if len(cleaned) > 420:
            continue
        sentences.append(cleaned)
    return sentences


def score_sentence(sentence: str, title_tokens: set[str], index: int) -> float:
    sentence_tokens = build_tokens(sentence)
    overlap = len(sentence_tokens & title_tokens)
    numeric_bonus = 1.5 if re.search(r"\d", sentence) else 0.0
    keyword_bonus = 1.2 if re.search(r"风险|发布|推出|融资|漏洞|升级|supports|introduces|announced", sentence, re.I) else 0.0
    position_bonus = max(0.0, 3.0 - index * 0.35)
    length_penalty = 0.0 if len(sentence) <= 180 else -1.5
    return overlap * 2.4 + numeric_bonus + keyword_bonus + position_bonus + length_penalty


def choose_summary_sentences(candidate: Candidate, limit: int = 3) -> list[str]:
    source_text = candidate.body_text if len(candidate.body_text) >= 240 else candidate.summary_text
    sentences = split_sentences(source_text)
    if not sentences and candidate.summary_text:
        sentences = split_sentences(candidate.summary_text)
    if not sentences:
        fallback = collapse_ws(candidate.summary_text or candidate.title)
        return [fallback] if fallback else []

    scored = [
        (score_sentence(sentence, candidate.title_tokens, index), index, sentence)
        for index, sentence in enumerate(sentences[:40])
    ]
    scored.sort(reverse=True)
    chosen: list[str] = []
    chosen_tokens: list[set[str]] = []
    title_norm = normalized_title(candidate.title)
    for _, _, sentence in scored:
        if normalized_title(sentence) == title_norm and len(sentences) > 1:
            continue
        sentence_tokens = build_tokens(sentence)
        if any(jaccard_similarity(sentence_tokens, existing) >= 0.78 for existing in chosen_tokens):
            continue
        chosen.append(sentence)
        chosen_tokens.append(sentence_tokens)
        if len(chosen) >= limit:
            break
    return chosen or [sentences[0]]


def finalize_summary_text(title: str, sentences: list[str], max_chars: int = 220) -> str:
    cleaned_sentences: list[str] = []
    normalized = normalized_title(title)
    for sentence in sentences:
        current = collapse_ws(sentence)
        if not current:
            continue
        if normalized and normalized_title(current).startswith(normalized):
            current = current[len(title) :].strip(" ：:,-")
        if current and current not in cleaned_sentences:
            cleaned_sentences.append(current)

    parts: list[str] = []
    current_length = 0
    for sentence in cleaned_sentences:
        extra = len(sentence) + (1 if parts else 0)
        if current_length + extra > max_chars:
            break
        parts.append(sentence)
        current_length += extra

    summary = " ".join(parts).strip()
    return clean_excerpt(summary or " ".join(cleaned_sentences) or title, limit=max_chars)


def infer_topic_tags(candidate: Candidate) -> list[str]:
    haystack = "\n".join([candidate.title, candidate.summary_text, candidate.body_text[:1500]]).lower()
    tags = [tag for tag, keywords in TOPIC_RULES.items() if any(keyword_in_text(haystack, keyword.lower()) for keyword in keywords)]
    return tags or ["其他"]


def infer_risk_tags(candidate: Candidate) -> list[str]:
    haystack = "\n".join([candidate.title, candidate.summary_text, candidate.body_text[:1200]]).lower()
    return [tag for tag, keywords in RISK_RULES.items() if any(keyword_in_text(haystack, keyword.lower()) for keyword in keywords)]


def infer_actionability(candidate: Candidate) -> str:
    text = "\n".join([candidate.title, candidate.summary_text, candidate.body_text[:800]]).lower()
    if re.search(r"发布|上线|教程|实战|how to|guide|skill|workflow|release|sdk|api", text):
        return "high"
    if re.search(r"融资|离职|ipo|research|study|政策|趋势|治理", text):
        return "medium"
    return "low"


def infer_public_importance(candidate: Candidate) -> int:
    text = "\n".join([candidate.title, candidate.summary_text]).lower()
    score = 1
    if re.search(r"openai|anthropic|apple|meta|华为|软银|microsoft|google", text):
        score += 2
    if re.search(r"安全|漏洞|风险|attack|exploit|监管|policy|融资|ipo", text):
        score += 1
    if "Readhub" in candidate.source or "InfoQ" in candidate.source:
        score += 1
    return min(5, score)


def infer_personal_relevance(candidate: Candidate) -> int:
    text = "\n".join([candidate.title, candidate.summary_text, candidate.body_text[:800]]).lower()
    score = 1
    if re.search(r"agent|skill|workflow|devops|open source|开源|自动化|infra|tool|安全", text):
        score += 2
    if re.search(r"codex|claude|copilot|freshrss|知识库|笔记", text):
        score += 1
    return min(5, score)


def generate_summaries(candidate: Candidate) -> None:
    sentences = choose_summary_sentences(candidate)
    max_chars = 220 if candidate.content_language in {"zh", "mixed"} else 260
    candidate.summary = finalize_summary_text(candidate.title, sentences, max_chars=max_chars)
    if normalized_title(candidate.summary) == normalized_title(candidate.title) and candidate.summary_text:
        candidate.summary = clean_excerpt(candidate.summary_text, limit=max_chars)

    summary_language = detect_language(candidate.summary or candidate.summary_text)
    if summary_language in {"zh", "mixed"}:
        candidate.summary_zh = candidate.summary
        return

    if detect_language(candidate.summary_text) in {"zh", "mixed"}:
        candidate.summary_zh = finalize_summary_text(candidate.title, choose_summary_sentences(candidate, limit=2), max_chars=220)
        return

    wrapped = finalize_summary_text(candidate.title, sentences[:2], max_chars=160)
    candidate.summary_zh = (
        f"英文原文，主题是《{candidate.title}》。"
        f"核心信息主要集中在：{wrapped}"
    ).strip()
    if "needs_manual_translation" not in (candidate.quality_flags or []):
        (candidate.quality_flags or []).append("needs_manual_translation")


def rank_candidate(candidate: Candidate) -> None:
    candidate.topic_tags = infer_topic_tags(candidate)
    candidate.risk_tags = infer_risk_tags(candidate)
    candidate.actionability = infer_actionability(candidate)
    candidate.public_importance = infer_public_importance(candidate)
    candidate.personal_relevance = infer_personal_relevance(candidate)

    actionability_bonus = {"high": 8.0, "medium": 4.0, "low": 1.0}[candidate.actionability]
    risk_bonus = 4.0 if candidate.risk_tags else 0.0
    cluster_bonus = min(6.0, len(candidate.related_item_ids or []) * 1.2)
    source_bonus = candidate.source_weight * 10.0
    importance_bonus = candidate.public_importance * 5.0
    relevance_bonus = candidate.personal_relevance * 3.0
    length_bonus = min(6.0, math.log(max(candidate.body_length, 120), 10) * 2.5)
    candidate.rank_score = (
        candidate.quality_score
        + source_bonus
        + actionability_bonus
        + risk_bonus
        + cluster_bonus
        + importance_bonus
        + relevance_bonus
        + length_bonus
    )
    reason_parts = [
        f"quality={candidate.quality_score}",
        f"source_weight={candidate.source_weight:.2f}",
        f"public_importance={candidate.public_importance}",
        f"personal_relevance={candidate.personal_relevance}",
        f"actionability={candidate.actionability}",
    ]
    if candidate.related_item_ids:
        reason_parts.append(f"cluster_refs={len(candidate.related_item_ids)}")
    if candidate.risk_tags:
        reason_parts.append(f"risk={','.join(candidate.risk_tags)}")
    candidate.ranking_reason = "; ".join(reason_parts)


def build_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Digest | {result['window']['label']}",
        "",
        "## Overview",
        "",
        f"- Input items: `{result['stats']['input_items']}`",
        f"- After URL dedup: `{result['stats']['after_url_dedup']}`",
        f"- After noise filter: `{result['stats']['after_noise_filter']}`",
        f"- Final digest items: `{result['stats']['final_items']}`",
        "",
        "## Ranked Items",
        "",
    ]

    for index, item in enumerate(result["items"], start=1):
        lines.extend(
            [
                f"### {index}. {markdown_escape(item['title'])}",
                "",
                f"- Source: **{item['source']}**",
                f"- Published: `{item['published_at']}`",
                f"- Link: [{markdown_escape(item['title'])}]({item['raw_url']})" if item["raw_url"] else "- Link: N/A",
                f"- Score: **{item['rank_score']}**",
                f"- Topics: {', '.join(item['topic_tags']) or 'N/A'}",
                f"- Risks: {', '.join(item['risk_tags']) if item['risk_tags'] else 'None'}",
                f"- Actionability: **{item['actionability']}**",
                f"- Summary: {item['summary_zh'] or item['summary'] or 'N/A'}",
                f"- Ranking reason: `{item['ranking_reason']}`",
                "",
            ]
        )
        if item["duplicate_item_ids"] or item["related_item_ids"]:
            refs = item["duplicate_item_ids"] + item["related_item_ids"]
            lines.append(f"- Cluster refs: `{len(refs)}` related items")
            lines.append("")

    if result["filtered"]:
        lines.extend(["## Filtered Items", ""])
        for entry in result["filtered"][:30]:
            lines.append(f"- `{entry['reason']}` | {entry['source']} | {entry['title']}")
        lines.append("")
    return "\n".join(lines)


def build_result(
    input_payload: dict[str, Any],
    input_items: list[Candidate],
    url_dedup_removed: list[dict[str, Any]],
    filtered_removed: list[dict[str, Any]],
    similar_removed: list[dict[str, Any]],
    final_items: list[Candidate],
) -> dict[str, Any]:
    label = input_payload.get("target_date") or input_payload.get("label") or "unknown-window"
    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "window": {
            "label": label,
            "target_date": input_payload.get("target_date"),
            "timezone": input_payload.get("timezone"),
        },
        "stats": {
            "input_items": len(input_items),
            "after_url_dedup": len(input_items) - len(url_dedup_removed),
            "after_noise_filter": len(input_items) - len(url_dedup_removed) - len(filtered_removed),
            "final_items": len(final_items),
            "url_duplicates_removed": len(url_dedup_removed),
            "filtered_removed": len(filtered_removed),
            "similar_duplicates_removed": len(similar_removed),
        },
        "items": [candidate.as_output() for candidate in final_items],
        "filtered": filtered_removed + url_dedup_removed + similar_removed,
    }


def load_source_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items")
    if not isinstance(items, list):
        raise SystemExit("Source JSON missing items list")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a structured digest from FreshRSS items.")
    parser.add_argument("--source-json", required=True, help="Path to sliced or raw FreshRSS JSON.")
    parser.add_argument("--output-json", required=True, help="Structured digest JSON output.")
    parser.add_argument("--output-md", required=True, help="Structured digest Markdown output.")
    parser.add_argument("--timeout", type=int, default=8, help="Per-page fetch timeout in seconds.")
    parser.add_argument("--concurrency", type=int, default=8, help="Concurrent fetch workers.")
    args = parser.parse_args()

    source_json = Path(args.source_json)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)

    if not source_json.exists():
        raise SystemExit(f"Source JSON not found: {source_json}")

    input_payload = load_source_payload(source_json)
    raw_items = parse_candidates(input_payload["items"])

    url_deduped, url_removed = dedupe_exact_urls(raw_items)
    fetch_bodies(url_deduped, timeout=args.timeout, concurrency=args.concurrency)

    for candidate in url_deduped:
        quality_check(candidate)

    filtered_candidates, filtered_removed = filter_noise(url_deduped)
    clustered_candidates, similar_removed = cluster_similar_candidates(filtered_candidates)

    for candidate in clustered_candidates:
        generate_summaries(candidate)
        rank_candidate(candidate)

    clustered_candidates.sort(key=lambda item: item.rank_score, reverse=True)

    result = build_result(
        input_payload=input_payload,
        input_items=raw_items,
        url_dedup_removed=url_removed,
        filtered_removed=filtered_removed,
        similar_removed=similar_removed,
        final_items=clustered_candidates,
    )

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(build_markdown(result), encoding="utf-8")

    print(f"input_items={result['stats']['input_items']}")
    print(f"after_url_dedup={result['stats']['after_url_dedup']}")
    print(f"after_noise_filter={result['stats']['after_noise_filter']}")
    print(f"final_items={result['stats']['final_items']}")
    print(f"json={output_json}")
    print(f"md={output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
