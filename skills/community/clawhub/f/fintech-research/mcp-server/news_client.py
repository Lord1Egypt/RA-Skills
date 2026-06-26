"""
News aggregation: NewsAPI + RSS feeds — global financial news with sentiment.

Purpose: Aggregate financial news from multiple free sources and perform
          simple keyword-based sentiment analysis.

Network behavior:
  - NewsAPI: 1 HTTPS GET request per call to newsapi.org
  - RSS: 1-2 HTTPS GET requests per call to financial RSS feeds
  - 30-second connection timeout per request
  - Response size capped at 1MB
  - SSL certificate verification enabled
  - Optional API key from NEWS_API_KEY env var (free tier: 100 req/day)
  - No API key falls back to RSS-only mode

Free API key: https://newsapi.org/register
"""
import os
import re
import requests

try:
    import feedparser

    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

# Security: Predefined allowed domains
_NEWSAPI_DOMAIN = "newsapi.org"
_NEWSAPI_URL = f"https://{_NEWSAPI_DOMAIN}/v2/everything"

# RSS feeds from reputable financial news sources
_RSS_FEEDS = [
    ("Reuters", "https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best"),
    ("Financial Times", "https://www.ft.com/?format=rss"),
    ("Bloomberg Markets", "https://feeds.bloomberg.com/markets/news.rss"),
]

# Security: Response size cap
_MAX_RESPONSE_SIZE = 1024 * 1024

# Security: Query validation
_MAX_QUERY_LEN = 200
_QUERY_PATTERN = re.compile(r"^[\w\s\-.,;:!?'\"()/&@+$*=|<>]+$")

# Security: Request identity
_DEFAULT_HEADERS = {
    "User-Agent": (
        "FintechResearch-MCP/2.0 "
        "(https://github.com/fredtai/Fintech-research; "
        "news-aggregator)"
    ),
    "Accept": "application/json, application/rss+xml, text/xml, */*",
}

_session = requests.Session()
_session.headers.update(_DEFAULT_HEADERS)


def _validate_query(query: str) -> str:
    """Sanitize and validate search query."""
    if not query:
        return "financial markets"
    query = str(query).strip()
    if len(query) > _MAX_QUERY_LEN:
        query = query[:_MAX_QUERY_LEN]
    # Remove potentially dangerous characters
    query = re.sub(r"[<>&;`|$(){}[\]\\]", "", query)
    return query


def get_news(query, source="newsapi", limit=5):
    """
    Get financial news with sentiment scoring.

    Args:
        query: Search query string (e.g., "Tencent earnings")
        source: "newsapi" or "rss" (default: "newsapi")
        limit: Max articles (default: 5, max: 20)

    Returns:
        dict: {"articles": [...], "source": str}

    Security notes:
        - Query sanitized: length capped, special chars removed
        - Only HTTPS requests to newsapi.org or predefined RSS feeds
        - Response truncated at 1MB
        - Rate-limited by NewsAPI free tier (100 req/day)
    """
    query = _validate_query(query)
    limit = min(int(limit), 20)
    source = re.sub(r"[^a-zA-Z]", "", str(source))  # Sanitize source name

    try:
        if source == "newsapi":
            return _newsapi(query, limit)
        elif source == "rss":
            return _rss_feeds(query, limit)
        else:
            return _mock_news(query, limit)
    except Exception:
        return _mock_news(query, limit)


def _newsapi(query, limit):
    """Fetch from NewsAPI with rate limiting awareness."""
    key = os.environ.get("NEWS_API_KEY", "")
    if not key:
        # No API key: fall back to RSS mode
        return _rss_feeds(query, limit)

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": min(limit, 20),  # NewsAPI max is 100
        "language": "en",
        "apiKey": key,
    }

    resp = _session.get(
        _NEWSAPI_URL,
        params=params,
        timeout=30,
        verify=True,
        stream=True,
    )

    # Size limit
    content = b""
    for chunk in resp.iter_content(chunk_size=8192):
        content += chunk
        if len(content) > _MAX_RESPONSE_SIZE:
            return {"articles": [], "error": "Response exceeds size limit (1MB)"}

    resp.raise_for_status()
    data = resp.json()

    articles = []
    for article in data.get("articles", [])[:limit]:
        title = article.get("title", "")
        desc = article.get("description", "") or ""
        articles.append(
            {
                "title": title,
                "source": article.get("source", {}).get("name", "NewsAPI"),
                "published_at": article.get("publishedAt", ""),
                "url": article.get("url", ""),
                "sentiment_score": _sentiment(title + " " + desc),
            }
        )

    return {"articles": articles, "source": "newsapi.org", "count": len(articles)}


def _rss_feeds(query, limit):
    """Fetch from predefined RSS feeds."""
    if not HAS_FEEDPARSER:
        return _mock_news(query, limit)

    articles = []
    seen_titles = set()

    for source_name, feed_url in _RSS_FEEDS:
        if len(articles) >= limit:
            break
        try:
            resp = _session.get(feed_url, timeout=15, verify=True, stream=True)

            # Size limit for RSS
            content = b""
            for chunk in resp.iter_content(chunk_size=4096):
                content += chunk
                if len(content) > 512 * 1024:  # 512KB for RSS
                    break

            fp = feedparser.parse(content)
            for entry in fp.entries[:limit]:
                title = entry.get("title", "")
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                articles.append(
                    {
                        "title": title,
                        "source": source_name,
                        "published_at": entry.get("published", ""),
                        "url": entry.get("link", ""),
                        "sentiment_score": _sentiment(title),
                    }
                )
                if len(articles) >= limit:
                    break
        except Exception:
            continue

    if not articles:
        return _mock_news(query, limit)

    return {"articles": articles, "source": "RSS feeds", "count": len(articles)}


def _sentiment(text):
    """Simple keyword sentiment: -1 to +1."""
    positive = [
        "surge", "gain", "rise", "bull", "strong", "beat", "growth",
        "rally", "outperform", "upgrade", "boost", "jump", "soar",
        "positive", "exceed", "record", "high", "buy", "accumulate",
    ]
    negative = [
        "fall", "drop", "bear", "weak", "miss", "decline", "crash",
        "sell", "downgrade", "plunge", "slump", "loss", "tumble",
        "negative", "warning", "low", "reduce", "dump", "crisis",
    ]
    text_lower = text.lower()
    pos = sum(1 for w in positive if w in text_lower)
    neg = sum(1 for w in negative if w in text_lower)
    total = pos + neg
    return round((pos - neg) / total, 2) if total > 0 else 0.0


def _mock_news(query, limit):
    """Return mock news data for offline testing."""
    return {
        "articles": [
            {
                "title": f"Mock financial news for: {query}",
                "source": "Mock",
                "published_at": "2025-05-01T00:00:00Z",
                "url": "",
                "sentiment_score": 0.0,
                "mock": True,
            }
        ],
        "count": 1,
        "source": "mock",
        "mock": True,
    }
