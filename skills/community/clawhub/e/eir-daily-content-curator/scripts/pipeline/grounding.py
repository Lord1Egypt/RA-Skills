"""
External search API client.

Wraps a configurable search service that provides web search,
news search, and URL browsing with inline content.

Configuration (in settings.json under "search"):
  search_base_url: API base URL (e.g. "https://api.example.com/v3")
  search_api_key:  API key for authentication

The API is expected to expose:
  POST {base}/search/web   — web search with inline content
  POST {base}/search/news  — news search (recent articles)
  POST {base}/browse       — fetch URL content

Compatible providers include Brave, Tavily, or any service
implementing the same REST interface.
"""

import json
import urllib.request
from typing import Optional

from .config import load_settings

_settings_cache = None


def _get_grounding_config():
    global _settings_cache
    if _settings_cache is None:
        _settings_cache = load_settings().get("search", {})
    return (
        _settings_cache.get("search_base_url", "").rstrip("/"),
        _settings_cache.get("search_api_key", ""),
    )


def _is_available():
    base, key = _get_grounding_config()
    return bool(base and key)


def _post(endpoint, body, timeout=20):
    """POST JSON to grounding API endpoint, return parsed response."""
    base, key = _get_grounding_config()
    if not base or not key:
        raise RuntimeError("Search API not configured (set search_base_url + search_api_key in settings.json)")
    url = "%s/%s" % (base, endpoint.lstrip("/"))
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "x-apikey": key,
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search_web(query, max_results=10, language="en", region="US",
               content_format="passage", max_length=3000):
    """Web search with inline content.
    
    content_format: 'passage' (query-relevant extracts), 'text', 'html', 'markdown'
    Returns list of {url, title, content, publishedDate, language}.
    """
    body = {
        "query": query,
        "maxResults": max_results,
        "language": language,
        "region": region,
        "contentFormat": content_format,
        "maxLength": max_length,
    }
    resp = _post("search/web", body)
    results = []
    for r in resp.get("webResults", []):
        results.append({
            "url": r.get("url", ""),
            "title": r.get("title", ""),
            "content": r.get("content", ""),
            "publishedDate": r.get("lastUpdatedAt"),
            "language": r.get("language", ""),
            "source_api": "grounding_web",
        })
    return results


def search_news(query, max_results=10, language="en", region="US",
                max_length=5000):
    """News search — returns recent articles (typically last 14 days).
    
    Returns list of {url, title, content, snippet, publishedDate, source, thumbnail}.
    """
    body = {
        "query": query,
        "maxResults": max_results,
        "language": language,
        "region": region,
        "maxLength": max_length,
    }
    resp = _post("search/news", body)
    results = []
    for r in resp.get("newsResults", []):
        item = {
            "url": r.get("url", ""),
            "title": r.get("title", ""),
            "content": r.get("content", ""),
            "snippet": r.get("snippet", ""),
            "publishedDate": r.get("lastUpdatedAt"),
            "source_name": r.get("source", ""),
            "source_api": "grounding_news",
        }
        thumb = r.get("thumbnail")
        if thumb and thumb.get("url"):
            item["thumbnail"] = thumb
        results.append(item)
    return results


def browse_url(url, max_length=50000):
    """Fetch full content from a URL via grounding browse endpoint.
    
    Returns {url, title, content, publishedDate} or None on failure.
    """
    try:
        body = {"url": url, "maxLength": max_length}
        resp = _post("browse", body, timeout=30)
        content = resp.get("content", "")
        if not content or len(content) < 100:
            return None
        return {
            "url": resp.get("url", url),
            "title": resp.get("title", ""),
            "content": content,
            "publishedDate": resp.get("lastUpdatedAt"),
            "source_api": "grounding_browse",
        }
    except Exception as e:
        print("    ⚠️ Grounding browse failed for %s: %s" % (url[:60], e))
        return None


def is_available():
    """Check if grounding API is configured."""
    return _is_available()
