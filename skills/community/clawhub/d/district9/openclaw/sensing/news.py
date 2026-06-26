"""News sensor — RSS feed scanning for meme-worthy topics."""

import xml.etree.ElementTree as ET

import requests

from .base import BaseSensor, Signal

# Free RSS feeds with crypto/tech/meme content
RSS_FEEDS = [
    ("https://cointelegraph.com/rss", "CoinTelegraph"),
    ("https://cryptonews.com/news/feed/", "CryptoNews"),
]


class NewsSensor(BaseSensor):
    """Scans RSS news feeds for trending topics (no API key required)."""

    name = "news"

    def scan(self) -> list[Signal]:
        signals = []
        for url, source_name in RSS_FEEDS:
            signals.extend(self._parse_feed(url, source_name))
        # Sort by score, take top 5
        signals.sort(key=lambda s: s.score, reverse=True)
        return signals[:5]

    def _parse_feed(self, url: str, source_name: str) -> list[Signal]:
        try:
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "OpenClaw/0.1 (DISTRICT9 Agent)"
            })
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            signals = []
            items = root.findall(".//item")[:10]

            for item in items:
                title = item.findtext("title", "")
                desc = item.findtext("description", "")

                if not title:
                    continue

                # Simple relevance scoring based on meme-related keywords
                score = self._score_headline(title, desc)
                if score > 30:
                    signals.append(Signal(
                        source="news",
                        keyword=title[:80],
                        score=score,
                        context=f"[{source_name}] {title}. {desc[:200]}",
                    ))

            return signals
        except Exception:
            return []

    def _score_headline(self, title: str, desc: str) -> float:
        """Score a headline for meme potential."""
        text = (title + " " + desc).lower()

        score = 40.0  # base score for any news

        # High meme potential keywords
        high_keywords = [
            "meme", "viral", "elon", "trump", "doge", "shib",
            "ai", "robot", "moon", "pump", "100x", "whale",
            "hack", "rug", "scam", "crash", "bull", "bear",
            "billion", "trillion", "record", "all-time",
        ]
        for kw in high_keywords:
            if kw in text:
                score += 15

        # Medium meme potential
        medium_keywords = [
            "bitcoin", "ethereum", "solana", "bnb", "defi",
            "nft", "token", "crypto", "blockchain",
            "market", "trading", "price",
        ]
        for kw in medium_keywords:
            if kw in text:
                score += 5

        return min(score, 100.0)
