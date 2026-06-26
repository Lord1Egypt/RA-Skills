#!/usr/bin/env python3
"""
Breaking News Event Trader — Monitors 20+ RSS feeds and trades Polymarket.

Uses fast keyword pre-filtering to find high-impact breaking news, matches
stories to active Polymarket markets, and trades when estimated price impact
exceeds 12%.

Author: Mibayy
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta

import feedparser
import requests
from simmer_sdk import SimmerClient

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILL_SLUG = "polymarket-news-events"
TRADE_SOURCE = "sdk:polymarket-news-events"

_client = None
def get_client():
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=os.environ.get("TRADING_VENUE", "sim")
        )
    return _client


def check_context(client, market_id, my_probability=None):
    """Check market context before trading (flip-flop, slippage, edge)."""
    try:
        params = {}
        if my_probability is not None:
            params["my_probability"] = my_probability
        ctx = client.get_market_context(market_id, **params)
        trading = ctx.get("trading", {})
        flip_flop = trading.get("flip_flop_warning")
        if flip_flop and "SEVERE" in flip_flop:
            return False, f"flip-flop: {flip_flop}"
        slippage = ctx.get("slippage", {})
        if slippage.get("slippage_pct", 0) > 0.15:
            return False, "slippage too high"
        edge = ctx.get("edge_analysis", {})
        if edge.get("recommendation") == "HOLD":
            return False, "edge below threshold"
        return True, "ok"
    except Exception:
        return True, "context unavailable"


IMPACT_THRESHOLD = float(os.environ.get('NEWS_IMPACT_THRESHOLD', '0.12'))
TRADE_SIZE_USD = float(os.environ.get('NEWS_TRADE_SIZE', '20.0'))
MAX_AGE_MINUTES = int(os.environ.get('NEWS_MAX_AGE_MINUTES', '30'))

# State file to avoid re-trading same story
STATE_FILE = "/tmp/polymarket_news_seen.json"

# ---------------------------------------------------------------------------
# RSS Feed Sources (tier 1 = most credible, tier 3 = niche)
# ---------------------------------------------------------------------------
RSS_FEEDS = {
    # Tier 1 — Wire services & major outlets
    "reuters_world": {"url": "https://feeds.reuters.com/reuters/worldNews", "tier": 1},
    "reuters_business": {"url": "https://feeds.reuters.com/reuters/businessNews", "tier": 1},
    "ap_top": {"url": "https://rsshub.app/apnews/topics/apf-topnews", "tier": 1},
    "bbc_world": {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "tier": 1},
    "bbc_business": {"url": "https://feeds.bbci.co.uk/news/business/rss.xml", "tier": 1},

    # Tier 2 — Financial & political
    "cnbc_top": {"url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", "tier": 2},
    "marketwatch": {"url": "https://feeds.marketwatch.com/marketwatch/topstories/", "tier": 2},
    "politico": {"url": "https://www.politico.com/rss/politicopicks.xml", "tier": 2},
    "axios": {"url": "https://api.axios.com/feed/", "tier": 2},
    "thehill": {"url": "https://thehill.com/feed/", "tier": 2},
    "ft": {"url": "https://www.ft.com/rss/home", "tier": 2},

    # Tier 3 — Crypto & tech
    "coindesk": {"url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "tier": 2},
    "cointelegraph": {"url": "https://cointelegraph.com/rss", "tier": 2},
    "techcrunch": {"url": "https://techcrunch.com/feed/", "tier": 3},
    "bloomberg_markets": {"url": "https://feeds.bloomberg.com/markets/news.rss", "tier": 1},
    "wsj_world": {"url": "https://feeds.wsj.com/rss/RSSWorldNews.xml", "tier": 1},

    # Additional
    "guardian_world": {"url": "https://www.theguardian.com/world/rss", "tier": 2},
    "nyt_world": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "tier": 1},
    "cnn_top": {"url": "http://rss.cnn.com/rss/edition.rss", "tier": 2},
    "aljazeera": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "tier": 2},
}

# ---------------------------------------------------------------------------
# Pre-filter keywords
# ---------------------------------------------------------------------------
REJECT_KEYWORDS = {
    "opinion", "editorial", "podcast", "review", "recipe", "lifestyle",
    "horoscope", "obituary", "crossword", "gallery", "photos", "video",
    "newsletter", "subscribe", "sponsored", "advertisement", "quiz",
}

ACCEPT_KEYWORDS = {
    "breaking", "passes", "signs", "signed", "ruling", "rules",
    "indicted", "arrested", "convicted", "sentenced", "impeach",
    "default", "crash", "surge", "plunge", "soar", "collapses",
    "declares", "sanctions", "tariff", "embargo", "war", "ceasefire",
    "resign", "fired", "appointed", "elected", "wins", "loses",
    "hack", "breach", "ban", "approved", "rejected", "veto",
    "rate cut", "rate hike", "inflation", "recession", "shutdown",
    "earthquake", "hurricane", "pandemic", "outbreak",
    "bitcoin", "ethereum", "crypto", "sec", "fed", "supreme court",
    "executive order", "legislation", "ballot",
}

# Market-matching keyword clusters
TOPIC_CLUSTERS = {
    "trump": ["trump", "donald trump", "president trump", "maga"],
    "biden": ["biden", "joe biden", "president biden"],
    "election": ["election", "ballot", "vote", "electoral", "primary"],
    "bitcoin": ["bitcoin", "btc", "crypto", "cryptocurrency"],
    "ethereum": ["ethereum", "eth", "ether"],
    "fed": ["federal reserve", "fed", "fomc", "interest rate", "rate cut", "rate hike"],
    "inflation": ["inflation", "cpi", "consumer price"],
    "recession": ["recession", "gdp", "economic contraction"],
    "ukraine": ["ukraine", "kyiv", "zelensky", "russia war"],
    "china": ["china", "beijing", "xi jinping", "taiwan"],
    "ai": ["artificial intelligence", "openai", "chatgpt", "ai regulation"],
    "supreme_court": ["supreme court", "scotus", "justice"],
    "congress": ["congress", "senate", "house passes", "legislation"],
    "oil": ["oil price", "crude oil", "opec", "petroleum"],
    "gold": ["gold price", "gold surges", "precious metals"],
}

log = logging.getLogger(SKILL_SLUG)


# ---------------------------------------------------------------------------
# State management (avoid re-trading same story)
# ---------------------------------------------------------------------------
def load_seen() -> set:
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            # Prune entries older than 24h
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
            return {k for k, v in data.items() if v > cutoff}
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_seen(seen: set):
    now = datetime.now(timezone.utc).isoformat()
    data = {h: now for h in seen}
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def story_hash(title: str, link: str) -> str:
    return hashlib.md5(f"{title}|{link}".encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# RSS fetching & filtering
# ---------------------------------------------------------------------------
def fetch_all_feeds() -> list:
    """Fetch and pre-filter stories from all RSS feeds."""
    stories = []
    now = datetime.now(timezone.utc)

    for name, config in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(config["url"])
        except Exception as e:
            log.debug("Feed %s failed: %s", name, e)
            continue

        for entry in feed.entries[:10]:  # latest 10 per feed
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            summary = entry.get("summary", "")[:300]

            if not title:
                continue

            # Parse publication time
            pub_time = None
            for time_field in ["published_parsed", "updated_parsed"]:
                t = entry.get(time_field)
                if t:
                    try:
                        pub_time = datetime(*t[:6], tzinfo=timezone.utc)
                    except Exception:
                        pass
                    break

            if pub_time and (now - pub_time).total_seconds() > MAX_AGE_MINUTES * 60:
                continue

            stories.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": name,
                "tier": config["tier"],
                "pub_time": pub_time,
                "hash": story_hash(title, link),
            })

    return stories


def pre_filter(story: dict) -> bool:
    """Fast accept/reject pre-filter."""
    text = f"{story['title']} {story['summary']}".lower()

    # Reject noise
    for kw in REJECT_KEYWORDS:
        if kw in text:
            return False

    # Accept high-signal stories
    for kw in ACCEPT_KEYWORDS:
        if kw in text:
            return True

    # Tier 1 sources get benefit of doubt
    if story["tier"] == 1:
        return True

    return False


# ---------------------------------------------------------------------------
# Impact estimation
# ---------------------------------------------------------------------------
def estimate_impact(story: dict, matched_topics: list) -> float:
    """Estimate price impact of a news story (0.0 - 1.0)."""
    text = f"{story['title']} {story['summary']}".lower()
    score = 0.0

    # Source credibility
    tier_scores = {1: 0.04, 2: 0.03, 3: 0.02}
    score += tier_scores.get(story["tier"], 0.01)

    # Keyword signal strength
    strong_words = [
        "breaking", "passes", "signs into law", "declares", "crash",
        "surge", "plunge", "indicted", "war", "default", "ban",
    ]
    for w in strong_words:
        if w in text:
            score += 0.03

    medium_words = [
        "ruling", "approved", "rejected", "sanctions", "tariff",
        "resign", "fired", "elected", "wins",
    ]
    for w in medium_words:
        if w in text:
            score += 0.02

    # Topic match quality
    score += len(matched_topics) * 0.02

    # Recency boost
    if story.get("pub_time"):
        age_min = (datetime.now(timezone.utc) - story["pub_time"]).total_seconds() / 60
        if age_min < 5:
            score += 0.04
        elif age_min < 15:
            score += 0.02

    return min(score, 0.50)


def match_topics(story: dict) -> list:
    """Match story to topic clusters."""
    text = f"{story['title']} {story['summary']}".lower()
    matched = []
    for topic, keywords in TOPIC_CLUSTERS.items():
        for kw in keywords:
            if kw in text:
                matched.append(topic)
                break
    return matched


# ---------------------------------------------------------------------------
# Market matching
# ---------------------------------------------------------------------------
def find_markets_for_topics(client: SimmerClient, topics: list, story: dict) -> list:
    """Find Polymarket markets relevant to matched topics."""
    found = []
    seen_ids = set()

    # Build search queries from topics and title words
    queries = list(topics)

    # Add key phrases from title
    title_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', story["title"])
    for phrase in title_words[:3]:
        if len(phrase) > 3:
            queries.append(phrase)

    for query in queries[:6]:  # cap searches
        try:
            markets = client.find_markets(query=query)
        except Exception:
            markets = []

        for m in (markets or []):
            mid = m.id
            if mid not in seen_ids:
                seen_ids.add(mid)
                found.append(m)

    return found


def score_market_relevance(market: dict, story: dict, topics: list) -> float:
    """Score how relevant a market is to a news story."""
    q = market.question.lower() if market.question else ""
    text = f"{story['title']} {story['summary']}".lower()
    score = 0.0

    # Check topic keyword overlap
    for topic in topics:
        for kw in TOPIC_CLUSTERS.get(topic, [topic]):
            if kw in q:
                score += 3.0
                break

    # Title word overlap
    title_tokens = set(re.findall(r'\b\w{4,}\b', story["title"].lower()))
    q_tokens = set(re.findall(r'\b\w{4,}\b', q))
    overlap = len(title_tokens & q_tokens)
    score += overlap * 2.0

    # Named entity overlap (capitalized words)
    entities = set(re.findall(r'\b[A-Z][a-z]{2,}\b', story["title"]))
    q_entities = set(re.findall(r'\b[A-Z][a-z]{2,}\b', market.question or ""))
    score += len(entities & q_entities) * 3.0

    return score


# ---------------------------------------------------------------------------
# Trade direction estimation
# ---------------------------------------------------------------------------
def estimate_direction(story: dict, market: dict) -> str:
    """Estimate whether news is positive (buy YES) or negative (sell YES)."""
    text = f"{story['title']} {story['summary']}".lower()

    positive_signals = [
        "passes", "approved", "wins", "surge", "soar", "rally",
        "signs", "breakthrough", "deal", "agrees", "record high",
        "elected", "ceasefire", "peace",
    ]
    negative_signals = [
        "crash", "plunge", "collapse", "default", "indicted",
        "arrested", "ban", "sanctions", "war", "reject", "veto",
        "resign", "fired", "fails", "loses", "shutdown",
    ]

    pos = sum(1 for w in positive_signals if w in text)
    neg = sum(1 for w in negative_signals if w in text)

    return "yes" if pos >= neg else "no"


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def run(live: bool = False, quiet: bool = False):
    """Main news scan and trade loop."""
    client = get_client()
    seen = load_seen()

    # Fetch all feeds
    log.info("Fetching %d RSS feeds...", len(RSS_FEEDS))
    stories = fetch_all_feeds()
    log.info("Fetched %d stories (within %d min window)", len(stories), MAX_AGE_MINUTES)

    # Filter out already-seen
    new_stories = [s for s in stories if s["hash"] not in seen]
    log.info("New stories: %d (filtered %d seen)", len(new_stories), len(stories) - len(new_stories))

    # Pre-filter
    filtered = [s for s in new_stories if pre_filter(s)]
    log.info("After pre-filter: %d stories", len(filtered))

    trades_made = 0
    stories_with_signals = 0

    for story in filtered:
        # Match topics
        topics = match_topics(story)
        if not topics:
            log.debug("No topic match: %s", story["title"][:60])
            seen.add(story["hash"])
            continue

        # Estimate impact
        impact = estimate_impact(story, topics)
        if impact < IMPACT_THRESHOLD:
            log.debug("Low impact (%.1f%%): %s", impact * 100, story["title"][:60])
            seen.add(story["hash"])
            continue

        log.info(
            "HIGH IMPACT (%.0f%%): [%s] %s — topics: %s",
            impact * 100, story["source"], story["title"][:80], ", ".join(topics),
        )
        stories_with_signals += 1

        # Find matching markets
        markets = find_markets_for_topics(client, topics, story)
        if not markets:
            log.info("  No matching Polymarket markets found")
            seen.add(story["hash"])
            continue

        # Score and rank markets by relevance
        scored = []
        for m in markets:
            rel_score = score_market_relevance(m, story, topics)
            if rel_score >= 3.0:
                scored.append((m, rel_score))

        scored.sort(key=lambda x: x[1], reverse=True)

        # Trade top match only
        if not scored:
            log.info("  No sufficiently relevant markets")
            seen.add(story["hash"])
            continue

        market, relevance = scored[0]
        market_id = market.id
        token_id = market.polymarket_token_id
        question = market.question

        if not token_id:
            seen.add(story["hash"])
            continue
        side = estimate_direction(story, market)

        reasoning = (
            f"Breaking news trade: '{story['title'][:100]}' "
            f"(source: {story['source']}, tier {story['tier']}). "
            f"Impact estimate: {impact:.0%}. Topics: {', '.join(topics)}. "
            f"Market relevance: {relevance:.1f}. "
        )

        log.info("  TRADE: %s %s (relevance=%.1f) — %s", side.upper(), question[:50], relevance, reasoning[:100])

        ok, reason = check_context(client, market_id)
        if not ok:
            log.warning("Skipping trade: %s", reason)
            continue

        if live:
            try:
                result = client.trade(
                    market_id=market_id,
                    side=side,
                    amount=TRADE_SIZE_USD,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                )
                log.info("  Order placed: %s", json.dumps(result, default=str)[:200])
                trades_made += 1
            except Exception as e:
                log.error("  Order failed: %s", e)
        else:
            log.info("  [DRY RUN] Would %s $%.0f on %s", side, TRADE_SIZE_USD, question[:50])
            trades_made += 1

        seen.add(story["hash"])
        time.sleep(0.3)

    # Save state
    save_seen(seen)

    if not quiet:
        print(f"\n{'='*60}")
        print(f"News Event Scan — {datetime.now(timezone.utc).isoformat()}")
        print(f"Feeds polled: {len(RSS_FEEDS)}")
        print(f"Stories fetched: {len(stories)} (new: {len(new_stories)})")
        print(f"After pre-filter: {len(filtered)}")
        print(f"High-impact stories: {stories_with_signals}")
        print(f"Trades: {trades_made}")
        print(f"Mode: {'LIVE' if live else 'DRY RUN'}")
        print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Breaking News Event Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--quiet", action="store_true", help="Suppress summary output")
    parser.add_argument("--debug", action="store_true", help="Debug logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else (logging.WARNING if args.quiet else logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")

    if not os.environ.get("SIMMER_API_KEY"):
        log.error("SIMMER_API_KEY not set")
        sys.exit(1)

    try:
        run(live=args.live, quiet=args.quiet)
    except KeyboardInterrupt:
        log.info("Interrupted")
    except Exception as e:
        log.error("Fatal: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
