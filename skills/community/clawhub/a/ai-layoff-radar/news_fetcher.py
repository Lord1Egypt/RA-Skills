import logging
import re
from datetime import datetime, timezone
from typing import Dict, List
from urllib.parse import quote_plus

import feedparser
from bs4 import BeautifulSoup
from dateutil import parser as dtparser
from newspaper import Article


logger = logging.getLogger(__name__)


KEYWORDS = [
    "AI layoffs",
    "AI job cuts",
    "automation layoffs",
    "AI replaced workers",
    "AI efficiency layoffs",
    "AI cost reduction layoffs",
]

NEWS_SOURCES = [
    "techcrunch.com",
    "bloomberg.com",
    "reuters.com",
    "ft.com",
    "theverge.com",
    "wired.com",
]


def _google_news_query_url(query: str) -> str:
    encoded = quote_plus(query)
    return f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"


def _parse_date(raw_date: str) -> str:
    if not raw_date:
        return datetime.now(timezone.utc).isoformat()
    try:
        return dtparser.parse(raw_date).astimezone(timezone.utc).isoformat()
    except (ValueError, TypeError):
        return datetime.now(timezone.utc).isoformat()


def _extract_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception:
        logger.warning("Failed to parse full article text: %s", url)
        return ""


def clean_html(text: str) -> str:
    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")
    clean = soup.get_text(" ", strip=True)

    # remove urls
    clean = re.sub(r"http\S+", "", clean)

    # normalize whitespace
    clean = re.sub(r"\s+", " ", clean)

    return clean


def fetch_news(max_items_per_feed: int = 10) -> List[Dict]:
    """
    Fetch candidate layoff articles from:
    1) Google News RSS keyword queries
    2) Google News RSS queries constrained to target news domains
    """
    feeds = []
    seen_urls = set()
    articles: List[Dict] = []

    for keyword in KEYWORDS:
        feeds.append(_google_news_query_url(keyword))
        for domain in NEWS_SOURCES:
            feeds.append(_google_news_query_url(f'{keyword} site:{domain}'))

    logger.info("Fetching %d RSS feeds", len(feeds))

    for feed_url in feeds:
        parsed = feedparser.parse(feed_url)
        if not parsed.entries:
            continue

        for entry in parsed.entries[:max_items_per_feed]:
            url = entry.get("link", "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            title = clean_html((entry.get("title") or "").strip())
            summary = clean_html((entry.get("summary") or "").strip())
            published = _parse_date(entry.get("published") or entry.get("updated") or "")
            source = ""
            if isinstance(entry.get("source"), dict):
                source = (entry.get("source", {}).get("title") or "").strip()
            if not source:
                source = (parsed.feed.get("title") or "Unknown").strip()

            text = clean_html(_extract_text(url))

            articles.append(
                {
                    "title": title,
                    "summary": summary,
                    "text": text,
                    "url": url,
                    "published_at": published,
                    "source_name": source,
                }
            )

    logger.info("Fetched %d unique candidate articles", len(articles))
    return articles
