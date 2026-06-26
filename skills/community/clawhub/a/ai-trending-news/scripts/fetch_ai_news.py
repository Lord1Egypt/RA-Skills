#!/usr/bin/env python3
"""Fetch and normalize AI news candidates from trusted public sources.

This script is intentionally dependency-light so it can run in a wide range of
agent environments. It uses only the Python standard library.

Outputs a JSON array of normalized items to stdout.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import Iterable, Optional

UA = "ai-trending-news-skill/1.0"

SOURCE_FEEDS = [
    {"source": "OpenAI", "kind": "rss", "url": "https://openai.com/news/rss.xml", "reputation": 100, "tier": 1},
    {"source": "Anthropic", "kind": "rss", "url": "https://www.anthropic.com/news/rss.xml", "reputation": 100, "tier": 1},
    {"source": "Google AI", "kind": "rss", "url": "https://blog.google/technology/ai/rss/", "reputation": 95, "tier": 1},
    {"source": "DeepMind", "kind": "rss", "url": "https://deepmind.google/discover/blog/rss.xml", "reputation": 95, "tier": 1},
    {"source": "Hugging Face", "kind": "rss", "url": "https://huggingface.co/blog/feed.xml", "reputation": 90, "tier": 1},
    {"source": "TechCrunch AI", "kind": "rss", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "reputation": 85, "tier": 2},
    {"source": "MIT Technology Review AI", "kind": "rss", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/", "reputation": 85, "tier": 2},
    {"source": "The Verge AI", "kind": "rss", "url": "https://www.theverge.com/artificial-intelligence/rss/index.xml", "reputation": 80, "tier": 2},
    {"source": "Ars Technica AI", "kind": "rss", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "reputation": 80, "tier": 2},
    {"source": "VentureBeat AI", "kind": "rss", "url": "https://venturebeat.com/category/ai/feed/", "reputation": 75, "tier": 2},
    {"source": "arXiv cs.AI", "kind": "rss", "url": "https://rss.arxiv.org/rss/cs.AI", "reputation": 75, "tier": 3},
    {"source": "arXiv cs.LG", "kind": "rss", "url": "https://rss.arxiv.org/rss/cs.LG", "reputation": 75, "tier": 3},
    {"source": "Hacker News", "kind": "hn", "url": "https://hn.algolia.com/api/v1/search?tags=story&query=AI", "reputation": 65, "tier": 4},
]

TITLE_CLEAN_RE = re.compile(r"\s+\|.*$|\s+-\s+.*$|\s+—\s+.*$")


@dataclass
class Item:
    title: str
    url: str
    source: str
    published_at: str
    summary: str = ""
    engagement: int = 0
    source_reputation: int = 0
    coverage: int = 0
    freshness: int = 0

    @property
    def dedupe_key(self) -> str:
        title = self.title.lower().strip()
        title = re.sub(r"[^a-z0-9]+", " ", title)
        return re.sub(r"\s+", " ", title).strip()

    def score(self, now: dt.datetime) -> float:
        published = parse_datetime(self.published_at)
        if not published:
            freshness_score = 20
        else:
            age_hours = max((now - published).total_seconds() / 3600.0, 0.0)
            if age_hours <= 6:
                freshness_score = 100
            elif age_hours <= 24:
                freshness_score = 80
            elif age_hours <= 72:
                freshness_score = 60
            elif age_hours <= 168:
                freshness_score = 40
            else:
                freshness_score = 20

        self.freshness = freshness_score
        return (
            freshness_score * 0.35
            + self.source_reputation * 0.30
            + self.coverage * 0.20
            + self.engagement * 0.15
        )


def http_get(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/xml, text/xml, application/rss+xml, application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_datetime(value: str) -> Optional[dt.datetime]:
    if not value:
        return None
    value = value.strip()
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return dt.datetime.fromisoformat(value)
    except ValueError:
        pass

    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
    ):
        try:
            parsed = dt.datetime.strptime(value, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            return parsed
        except ValueError:
            continue
    return None


def clean_title(title: str) -> str:
    title = html_unescape(title or "").strip()
    title = TITLE_CLEAN_RE.sub("", title)
    return re.sub(r"\s+", " ", title).strip()


def html_unescape(text: str) -> str:
    import html
    return html.unescape(text)


def read_rss(feed: dict, since: Optional[dt.datetime]) -> list[Item]:
    raw = http_get(feed["url"])
    root = ET.fromstring(raw)
    channel = root.find("channel")
    if channel is None:
        return []

    items: list[Item] = []
    for node in channel.findall("item"):
        title = clean_title((node.findtext("title") or "").strip())
        link = (node.findtext("link") or "").strip()
        pub = (node.findtext("pubDate") or node.findtext("published") or node.findtext("updated") or "").strip()
        summary = clean_title((node.findtext("description") or "").strip())
        published_at = parse_datetime(pub)
        if since and published_at and published_at < since:
            continue
        if not title or not link:
            continue
        items.append(
            Item(
                title=title,
                url=link,
                source=feed["source"],
                published_at=(published_at.isoformat() if published_at else ""),
                summary=summary,
                source_reputation=feed["reputation"],
            )
        )
    return items


def read_hn(feed: dict, since: Optional[dt.datetime]) -> list[Item]:
    payload = json.loads(http_get(feed["url"]))
    items: list[Item] = []
    for hit in payload.get("hits", []):
        title = clean_title(hit.get("title") or "")
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        created = parse_datetime(hit.get("created_at") or "")
        if since and created and created < since:
            continue
        if not title:
            continue
        points = int(hit.get("points") or 0)
        comments = int(hit.get("num_comments") or 0)
        engagement = min(100, points * 2 + comments)
        items.append(
            Item(
                title=title,
                url=url,
                source=feed["source"],
                published_at=(created.isoformat() if created else ""),
                summary=hit.get("story_text") or "",
                engagement=engagement,
                source_reputation=feed["reputation"],
            )
        )
    return items


def dedupe(items: Iterable[Item]) -> list[Item]:
    clusters: dict[str, Item] = {}
    for item in items:
        key = item.dedupe_key
        if key not in clusters:
            clusters[key] = item
            continue
        existing = clusters[key]
        # Keep the item with the better source reputation or richer summary.
        if item.source_reputation > existing.source_reputation:
            item.coverage = existing.coverage + 1
            clusters[key] = item
        else:
            existing.coverage += 1
            if len(item.summary or "") > len(existing.summary or ""):
                existing.summary = item.summary
            existing.engagement = max(existing.engagement, item.engagement)
    return list(clusters.values())


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch AI trending news candidates.")
    parser.add_argument("--hours", type=int, default=48, help="Lookback window in hours (default: 48)")
    parser.add_argument("--limit", type=int, default=50, help="Max items to return after scoring")
    args = parser.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = now - dt.timedelta(hours=max(args.hours, 1))

    all_items: list[Item] = []
    for feed in SOURCE_FEEDS:
        try:
            if feed["kind"] == "rss":
                all_items.extend(read_rss(feed, since))
            elif feed["kind"] == "hn":
                all_items.extend(read_hn(feed, since))
        except Exception as exc:
            print(f"[warn] failed to fetch {feed['source']}: {exc}", file=sys.stderr)

    merged = dedupe(all_items)
    ranked = sorted(merged, key=lambda item: item.score(now), reverse=True)

    output = []
    for item in ranked[: args.limit]:
        output.append(
            {
                **asdict(item),
                "score": round(item.score(now), 2),
                "published_at": item.published_at,
            }
        )

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
