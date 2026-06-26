#!/usr/bin/env python3
"""Fetch, score, and deduplicate crypto news from configured RSS sources."""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import math
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SOURCES_PATH = SKILL_DIR / "references" / "sources.yaml"
SCORING_PATH = SKILL_DIR / "references" / "scoring.yaml"

# Token fetch settings
TOKENS_TTL_HOURS = 24
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}"


@dataclass
class Article:
    source_id: str
    source_name: str
    source_weight: float
    category: str
    title: str
    url: str
    summary: str
    published_at: dt.datetime | None


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def save_yaml(path: Path, data: dict) -> None:
    """Save data to YAML file with preserving structure."""
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(data, handle, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2)


def fetch_tokens_from_coingecko(limit: int = 100, timeout: int = 15) -> dict[str, list[str]]:
    """Fetch top tokens from CoinGecko API (no API key required)."""
    url = COINGECKO_API_URL.format(limit=min(limit, 250))
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "FeedMob Coin News Collector/0.1"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))

    token_aliases: dict[str, list[str]] = {}
    for coin in data:
        symbol = coin.get("symbol", "").upper()
        name = coin.get("name", "").lower()
        if symbol and name:
            aliases = [name, symbol.lower()]
            # Remove duplicates while preserving order
            seen = set()
            unique_aliases = [a for a in aliases if not (a in seen or seen.add(a))]
            token_aliases[symbol] = unique_aliases

    return token_aliases


def is_tokens_fresh(scoring: dict, ttl_hours: int) -> bool:
    """Check if dynamic tokens in scoring.yaml are still fresh."""
    fetched_at_str = scoring.get("dynamic_tokens", {}).get("fetched_at")
    if not fetched_at_str:
        return False

    try:
        fetched_at = dt.datetime.fromisoformat(fetched_at_str)
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=dt.timezone.utc)
        age_hours = (dt.datetime.now(dt.timezone.utc) - fetched_at).total_seconds() / 3600
        return age_hours <= ttl_hours
    except (ValueError, TypeError):
        return False


def update_scoring_with_tokens(scoring: dict, tokens: dict[str, list[str]]) -> None:
    """Update scoring.yaml with new dynamic tokens."""
    scoring["dynamic_tokens"] = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "token_aliases": tokens
    }
    save_yaml(SCORING_PATH, scoring)


def get_token_aliases(args: argparse.Namespace, scoring: dict) -> dict[str, list[str]]:
    """Get token aliases: dynamic from CoinGecko (in YAML) + manual overrides (in YAML)."""
    # Manual tokens (higher priority, user-defined)
    manual_tokens = scoring.get("token_aliases", {})

    if args.no_dynamic_tokens:
        return manual_tokens

    # Check if dynamic tokens in YAML are fresh
    if is_tokens_fresh(scoring, TOKENS_TTL_HOURS):
        dynamic_tokens = scoring.get("dynamic_tokens", {}).get("token_aliases", {})
        return {**dynamic_tokens, **manual_tokens}

    # Fetch new tokens from CoinGecko and update scoring.yaml
    try:
        dynamic_tokens = fetch_tokens_from_coingecko(args.token_limit)
        update_scoring_with_tokens(scoring, dynamic_tokens)
        print(f"info: updated scoring.yaml with {len(dynamic_tokens)} tokens from CoinGecko", file=sys.stderr)
        return {**dynamic_tokens, **manual_tokens}
    except Exception as exc:
        print(f"warning: failed to fetch dynamic tokens: {exc}, using YAML only", file=sys.stderr)
        # Fall back to existing dynamic tokens if available
        existing_dynamic = scoring.get("dynamic_tokens", {}).get("token_aliases", {})
        return {**existing_dynamic, **manual_tokens}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="append", default=[])
    parser.add_argument("--topic", action="append", default=[])
    parser.add_argument("--days", type=int, help="Lookback window in days")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown", "md"], default="json",
                        help="Output format: json (default), markdown/md (with clickable links)")
    parser.add_argument("--token-limit", type=int, default=100,
                        help="Number of top tokens to fetch from CoinGecko (default: 100, max: 250)")
    parser.add_argument("--no-dynamic-tokens", action="store_true",
                        help="Disable dynamic token fetching, use only YAML config")
    return parser.parse_args()


def fetch_url(url: str, user_agent: str, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def strip_html(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except (TypeError, ValueError, IndexError):
        return None


def parse_feed(feed_bytes: bytes, source: dict) -> list[Article]:
    root = ET.fromstring(feed_bytes)
    articles: list[Article] = []
    for item in root.findall(".//item"):
        title = strip_html(item.findtext("title"))
        url = strip_html(item.findtext("link"))
        summary = strip_html(item.findtext("description"))
        published_at = parse_datetime(item.findtext("pubDate"))
        if not title or not url:
            continue
        articles.append(
            Article(
                source_id=source["id"],
                source_name=source["name"],
                source_weight=float(source.get("weight", 1.0)),
                category=source.get("category", "general"),
                title=title,
                url=url,
                summary=summary,
                published_at=published_at,
            )
        )
    return articles


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def recency_score(published_at: dt.datetime | None, half_life_hours: float) -> float:
    if not published_at:
        return 0.2
    age_hours = max((dt.datetime.now(dt.timezone.utc) - published_at).total_seconds() / 3600, 0)
    return math.exp(-math.log(2) * age_hours / half_life_hours)


def collect_matches(text: str, mapping: dict[str, list[str]]) -> list[str]:
    return [key for key, aliases in mapping.items() if any(alias in text for alias in aliases)]


def score_article(article: Article, scoring: dict, token_aliases: dict[str, list[str]]) -> tuple[float, list[str], list[str]]:
    full_text = normalize(f"{article.title} {article.summary}")
    title_text = normalize(article.title)
    token_matches = collect_matches(full_text, token_aliases)
    topic_matches = collect_matches(full_text, scoring["topic_keywords"])
    negative_hits = sum(1 for keyword in scoring["negative_keywords"] if keyword in full_text)

    weights = scoring["weights"]
    score = article.source_weight * weights["source_weight_multiplier"]
    score += len(token_matches) * weights["token_match"]
    score += len(topic_matches) * weights["topic_match"]
    if token_matches or topic_matches:
        if any(alias in title_text for aliases in list(token_aliases.values()) + list(scoring["topic_keywords"].values()) for alias in aliases):
            score += weights["title_keyword_bonus"]
    score += negative_hits * weights["negative_keyword_penalty"]
    score += recency_score(article.published_at, scoring["defaults"]["recency_half_life_hours"]) * 20
    return score, token_matches, topic_matches


def is_duplicate(left: str, right: str, threshold: float) -> bool:
    return SequenceMatcher(a=left, b=right).ratio() >= threshold


def format_output(articles: list[dict], fmt: str, pretty: bool) -> str:
    """Format articles for output."""
    if fmt == "json":
        return json.dumps(articles, ensure_ascii=False, indent=2 if pretty else None)

    # Markdown format with clickable links
    lines = ["# 📰 Coin News Digest\n"]
    for i, article in enumerate(articles, 1):
        title = article["title"]
        url = article["url"]
        source = article["source"]
        published = article.get("published_at", "")[:10] if article.get("published_at") else ""
        summary = article.get("summary", "")[:200] + "..." if len(article.get("summary", "")) > 200 else article.get("summary", "")
        tokens = ", ".join(article.get("matched_tokens", []))
        topics = ", ".join(article.get("matched_topics", []))

        lines.append(f"## {i}. [{title}]({url})")
        lines.append(f"**来源**: {source} | **时间**: {published} | **分数**: {article['score']}")
        if tokens:
            lines.append(f"**Token**: {tokens}")
        if topics:
            lines.append(f"**主题**: {topics}")
        lines.append(f"\n{summary}\n")
        lines.append("---\n")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    sources = load_yaml(SOURCES_PATH)
    scoring = load_yaml(SCORING_PATH)

    # Get token aliases (dynamic + static merge)
    token_aliases = get_token_aliases(args, scoring)

    all_articles: list[Article] = []
    for source in sources["sources"]:
        if not source.get("enabled", True):
            continue
        try:
            feed_bytes = fetch_url(
                source["url"],
                sources["defaults"]["user_agent"],
                int(sources["defaults"]["request_timeout_seconds"]),
            )
            all_articles.extend(parse_feed(feed_bytes, source)[: int(sources["defaults"]["max_articles_per_source"])])
        except Exception as exc:
            print(f"warning: failed to fetch {source['name']}: {exc}", file=sys.stderr)

    lookback_hours = args.hours
    if args.days is not None:
        lookback_hours = max(args.days, 0) * 24
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=lookback_hours)
    wanted_tokens = {token.upper() for token in args.token}
    wanted_topics = {topic.lower() for topic in args.topic}
    min_score = float(scoring["defaults"]["min_output_score"])
    duplicate_threshold = float(scoring["defaults"]["duplicate_title_similarity_threshold"])

    ranked = []
    seen_titles: list[str] = []
    for article in all_articles:
        if article.published_at and article.published_at < cutoff:
            continue
        score, token_matches, topic_matches = score_article(article, scoring, token_aliases)
        if wanted_tokens and not wanted_tokens.intersection(token_matches):
            continue
        if wanted_topics and not wanted_topics.intersection(topic_matches):
            continue
        if score < min_score:
            continue

        title_key = normalize(article.title)
        if any(is_duplicate(title_key, seen, duplicate_threshold) for seen in seen_titles):
            continue
        seen_titles.append(title_key)

        ranked.append(
            {
                "title": article.title,
                "url": article.url,
                "source": article.source_name,
                "source_id": article.source_id,
                "category": article.category,
                "published_at": article.published_at.isoformat() if article.published_at else None,
                "summary": article.summary,
                "score": round(score, 2),
                "matched_tokens": token_matches,
                "matched_topics": topic_matches,
                "duplicate_group_key": title_key,
            }
        )

    ranked.sort(key=lambda item: (item["score"], item["published_at"] or ""), reverse=True)
    result = ranked[: args.limit]

    if args.format in ("markdown", "md"):
        print(format_output(result, "markdown", args.pretty))
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
        if args.pretty:
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
