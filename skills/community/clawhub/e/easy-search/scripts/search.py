#!/usr/bin/env python3
"""
Easy Search - A simple web search tool with no API key required.
Version 5.0.0 - Enhanced with more engines, snippet extraction, time filter and interactive mode

Features:
- Uses duckduckgo_search library for better stability (when available)
- Auto-detects best available search engine with health caching
- Automatic failover between engines
- Supports multiple search engines: DuckDuckGo, Bing, Google, Baidu, Sogou, 360, Brave, Yandex
- Snippet extraction for better result previews
- Time filtering (day/week/month/year)
- Interactive mode for continuous searching
- Proxy support via environment variables
- Result caching
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Try to import duckduckgo_search
try:
    from duckduckgo_search import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False

# Try to import requests for better HTTP handling
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ============================================================================
# Configuration
# ============================================================================

VERSION = "1.1.0"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

CACHE_DIR = Path.home() / ".easysearch_cache"
CACHE_TTL = 3600  # 1 hour

# Engine health cache
ENGINE_HEALTH_CACHE = {
    "last_check": 0,
    "ttl": 300,  # 5 minutes
    "data": {},
    "best_engine": None
}

# Engine priorities (higher = preferred)
# Adjusted based on reliability and snippet quality
ENGINE_PRIORITY = {
    "duckduckgo": 100,  # Most stable with DDGS library, good snippets
    "startpage": 95,    # Privacy-focused, good HTML parsing
    "bing": 90,         # Good global coverage, decent snippets
    "sogou": 85,        # Good for Chinese content
    "brave": 80,        # Privacy-focused, growing index
    "google": 70,       # Best results but often blocked
    "so360": 60,        # Chinese alternative
    "yandex": 50,       # Russian engine, works in some regions
    "baidu": 40,        # Chinese engine, strong anti-crawl
}

# Time filter URL parameters
TIME_FILTERS = {
    "day": {"google": "&tbs=qdr:d", "bing": "&filters=ex1:\"ez1\"", "baidu": "&lm=1"},
    "week": {"google": "&tbs=qdr:w", "bing": "&filters=ex1:\"ez2\"", "baidu": "&lm=7"},
    "month": {"google": "&tbs=qdr:m", "bing": "&filters=ex1:\"ez3\"", "baidu": "&lm=30"},
    "year": {"google": "&tbs=qdr:y", "bing": "&filters=ex1:\"ez4\"", "baidu": "&lm=365"},
}

# HTML-based search engine configurations with snippet patterns
ENGINES = {
    "google": {
        "name": "Google",
        "url_template": "https://www.google.com/search?q={query}&num={num}",
        "result_patterns": [
            # Title and URL
            (r'<h3[^>]*><a[^>]*href="([^"]+)"[^>]*>([^<]+)</a></h3>', "title_url"),
            (r'<a[^>]*href="(/url\?q=[^"]+)"[^>]*>([^<]+)</a>', "google_redirect"),
        ],
        "snippet_patterns": [
            r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>',
            r'<span[^>]*class="[^"]*aCOpRe[^"]*"[^>]*>(.*?)</span>',
        ],
    },
    "bing": {
        "name": "Bing",
        "url_template": "https://www.bing.com/search?q={query}&count={num}",
        "result_patterns": [
            (r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>([^<]+)</a></h2>', "title_url"),
        ],
        "snippet_patterns": [
            r'<p[^>]*class="b_lineclamp[^"]*"[^>]*>(.*?)</p>',
            r'<div[^>]*class="b_caption"[^>]*>.*?<p>(.*?)</p>',
        ],
        "result_container": r'<li[^>]*class="b_algo"[^>]*>(.*?)</li>',
    },
    "duckduckgo": {
        "name": "DuckDuckGo",
        "url_template": "https://duckduckgo.com/html/?q={query}",
        "result_patterns": [
            (r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', "title_url"),
        ],
        "snippet_patterns": [
            r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>',
        ],
        "result_container": r'<div[^>]*class="result[^"]*"[^>]*>(.*?)</div>',
    },
    "baidu": {
        "name": "Baidu",
        "url_template": "https://www.baidu.com/s?wd={query}&rn={num}",
        "result_patterns": [
            (r'<h3[^>]*class=[\'"][^\'"]*[tT][^\'"]*[\'"][^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', "baidu_link"),
        ],
        "snippet_patterns": [
            r'<span[^>]*class="[^"]*content-right[^"]*"[^>]*>(.*?)</span>',
            r'<div[^>]*class="[^"]*c-abstract[^"]*"[^>]*>(.*?)</div>',
        ],
    },
    "startpage": {
        "name": "Startpage",
        "url_template": "https://www.startpage.com/do/search?q={query}",
        "result_patterns": [
            # Startpage: find title in h2, then look for external URL before it
            (r'<h2[^>]*class="wgl-title[^"]*"[^>]*>([^<]+)</h2>', "title_with_context"),
        ],
        "snippet_patterns": [
            r'<p[^>]*class="wgl-description[^"]*"[^>]*>(.*?)</p>',
        ],
        # URL pattern to search before title
        "url_pattern": r'href="(https://[^"]+)"',
        "url_filter": ["startpage", "proxy", "app.startpage"],  # URLs containing these are filtered out
    },
    "sogou": {
        "name": "Sogou",
        "url_template": "https://www.sogou.com/web?query={query}&num={num}",
        "result_patterns": [
            (r'<h3[^>]*><a[^>]*href="([^"]+)"[^>]*target="_blank"[^>]*>([^<]+)</a>', "title_url"),
            (r'<a[^>]*class="[^"]*vr-title[^"]*"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', "title_url"),
        ],
        "snippet_patterns": [
            r'<p[^>]*class="[^"]*str-text-info[^"]*"[^>]*>(.*?)</p>',
            r'<div[^>]*class="[^"]*str_text_info[^"]*"[^>]*>(.*?)</div>',
        ],
    },
    "so360": {
        "name": "360 Search",
        "url_template": "https://www.so.com/s?q={query}&pn=0&rn={num}",
        "result_patterns": [
            (r'<h3[^>]*><a[^>]*href="([^"]+)"[^>]*>([^<]+)</a></h3>', "title_url"),
        ],
        "snippet_patterns": [
            r'<p[^>]*class="[^"]*desc[^"]*"[^>]*>(.*?)</p>',
        ],
    },
    "brave": {
        "name": "Brave Search",
        "url_template": "https://search.brave.com/search?q={query}",
        "result_patterns": [
            (r'<a[^>]*class="[^"]*result-header[^"]*"[^>]*href="([^"]+)"[^>]*>.*?<span[^>]*>([^<]+)</span>', "title_url"),
            (r'<cite[^>]*>([^<]+)</cite>.*?<a[^>]*href="([^"]+)"', "reverse"),
        ],
        "snippet_patterns": [
            r'<p[^>]*class="[^"]*snippet[^"]*"[^>]*>(.*?)</p>',
        ],
    },
    "yandex": {
        "name": "Yandex",
        "url_template": "https://yandex.com/search/?text={query}&numdoc={num}",
        "result_patterns": [
            (r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*target="_blank"[^>]*>([^<]+)</a>', "title_url"),
        ],
        "snippet_patterns": [
            r'<span[^>]*class="[^"]*extended-text[^"]*"[^>]*>(.*?)</span>',
        ],
    },
}


# ============================================================================
# Proxy Detection
# ============================================================================

def get_proxy_url() -> Optional[str]:
    """Get proxy URL from environment variables."""
    return (os.environ.get("ALL_PROXY") or
            os.environ.get("HTTPS_PROXY") or
            os.environ.get("HTTP_PROXY") or
            os.environ.get("https_proxy") or
            os.environ.get("http_proxy"))


def has_working_proxy() -> bool:
    """Check if a working proxy is configured."""
    proxy = get_proxy_url()
    return bool(proxy)


# ============================================================================
# URL Cleaning
# ============================================================================

def clean_url(url: str, engine: str = "") -> str:
    """Clean and normalize URLs from search results."""
    if not url:
        return url

    original_url = url

    try:
        # Decode HTML entities first
        url = url.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        url = url.replace('&quot;', '"').replace('&#39;', "'")

        # DuckDuckGo redirect
        if "duckduckgo.com/l/" in url and "uddg=" in url:
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if "uddg" in params:
                url = urllib.parse.unquote(params["uddg"][0])

        # Baidu redirect
        elif "baidu.com/baidu.php" in url or "baidu.com/link?" in url:
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if "url" in params:
                url = urllib.parse.unquote(params["url"][0])

        # Sogou redirect
        elif "sogou.com/link?" in url:
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if "url" in params:
                url = urllib.parse.unquote(params["url"][0])

        # Google redirect
        elif url.startswith("/url?q=") or "/url?q=" in url:
            match = re.search(r'[?&]q=([^&]+)', url)
            if match:
                url = urllib.parse.unquote(match.group(1))

        # Protocol-relative URL
        elif url.startswith("//"):
            url = "https:" + url

        # Remove tracking parameters
        url = re.sub(r'[?&](utm_\w+|referrerpolicy|fbclid|gclid|msclkid|sessionid|__mk_|cvid|pcvid)=[^&]*', '', url)
        url = re.sub(r'[?&]$', '', url)

        # Ensure scheme
        if not url.startswith(("http://", "https://")):
            if re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9]*\.', url):
                url = "https://" + url
            else:
                return original_url

        return url.strip()

    except Exception:
        return original_url


def clean_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode common entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ============================================================================
# Search Implementation: duckduckgo_search library
# ============================================================================

def search_with_ddgs(
    query: str,
    max_results: int = 5,
    proxy: Optional[str] = None,
    timeout: int = 30,
    time_filter: Optional[str] = None,
    max_retries: int = 2
) -> Tuple[List[Dict], Optional[str]]:
    """
    Search using duckduckgo_search library with retry support.
    Returns (results, error_message).
    """
    if not HAS_DDGS:
        return [], "duckduckgo_search library not installed"

    results = []
    last_error = None

    for attempt in range(max_retries):
        try:
            kwargs = {"timeout": timeout}
            if proxy:
                kwargs["proxies"] = proxy

            with DDGS(**kwargs) as ddgs:
                # Build search parameters
                search_params = {"keywords": query, "max_results": max_results}

                # Time filter for DDGS
                if time_filter:
                    timelimit_map = {"day": "d", "week": "w", "month": "m", "year": "y"}
                    if time_filter in timelimit_map:
                        search_params["timelimit"] = timelimit_map[time_filter]

                for r in ddgs.text(**search_params):
                    results.append({
                        "title": r.get("title", "No title"),
                        "url": r.get("href", r.get("url", "")),
                        "snippet": r.get("body", r.get("snippet", "")),
                    })

            if results:
                return results, None

        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
                continue

    return [], last_error or "No results found"


# ============================================================================
# Search Implementation: HTML scraping (fallback)
# ============================================================================

def fetch_html(url: str, timeout: int = 15) -> Tuple[Optional[str], Optional[str]]:
    """Fetch HTML content using urllib or requests."""
    proxy = get_proxy_url()
    user_agent = random.choice(USER_AGENTS)

    # Try with requests first (better proxy support)
    if HAS_REQUESTS:
        try:
            proxies = None
            if proxy:
                proxies = {"http": proxy, "https": proxy}

            resp = requests.get(
                url,
                headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"},
                timeout=timeout,
                proxies=proxies,
                allow_redirects=True
            )
            if resp.status_code == 200:
                return resp.text, None
        except Exception:
            pass

    # Fallback to urllib
    try:
        handlers = []
        if proxy:
            handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))

        opener = urllib.request.build_opener(*handlers) if handlers else urllib.request.build_opener()

        req = urllib.request.Request(
            url,
            headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"}
        )

        with opener.open(req, timeout=timeout) as resp:
            html = resp.read()
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
                try:
                    return html.decode(encoding), None
                except:
                    continue
            return html.decode('utf-8', errors='replace'), None

    except Exception as e:
        return None, str(e)


def extract_snippet(html: str, engine: str) -> str:
    """Extract snippet text from HTML using engine-specific patterns."""
    if engine not in ENGINES:
        return ""

    config = ENGINES[engine]
    for pattern in config.get("snippet_patterns", []):
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            return clean_html(match.group(1))

    return ""


def parse_html_results(html: str, engine: str, max_results: int) -> List[Dict]:
    """Parse search results from HTML with snippet extraction."""
    if engine not in ENGINES:
        return []

    results = []
    seen_urls = set()

    # Check for blocked indicators
    blocked_indicators = ["百度安全验证", "captcha", "验证码", "access denied", "blocked", "请输入验证码"]
    for indicator in blocked_indicators:
        if indicator.lower() in html.lower():
            return []  # Engine blocked us

    config = ENGINES[engine]

    # Try to parse results by container first (more accurate snippet matching)
    container_pattern = config.get("result_container")
    if container_pattern:
        containers = re.findall(container_pattern, html, re.IGNORECASE | re.DOTALL)
        for container in containers:
            if len(results) >= max_results:
                break

            # Extract title and URL
            for pattern, pattern_type in config["result_patterns"]:
                match = re.search(pattern, container, re.IGNORECASE | re.DOTALL)
                if match:
                    if pattern_type in ("title_url", "google_redirect", "baidu_link"):
                        url = clean_url(match.group(1), engine)
                        title = clean_html(match.group(2))
                    elif pattern_type == "reverse":
                        title = clean_html(match.group(1))
                        url = clean_url(match.group(2), engine)
                    else:
                        continue

                    if not url or url.startswith("#") or url.startswith("javascript:"):
                        continue

                    url_key = url.split("?")[0]
                    if url_key in seen_urls:
                        continue
                    seen_urls.add(url_key)

                    # Extract snippet from container
                    snippet = extract_snippet(container, engine)

                    results.append({
                        "title": title or "No title",
                        "url": url,
                        "snippet": snippet
                    })
                    break

    # Fallback: parse results individually
    if not results:
        # Special handling for engines with separate title and URL patterns (like Startpage)
        titles = []
        urls = []
        has_separate_patterns = False
        has_context_pattern = False

        for pattern, pattern_type in config["result_patterns"]:
            if pattern_type == "title_with_context":
                # Find titles and search for URLs before each title
                has_context_pattern = True
                title_matches = list(re.finditer(pattern, html, re.IGNORECASE | re.DOTALL))
                url_pattern = config.get("url_pattern", r'href="(https://[^"]+)"')
                url_filters = config.get("url_filter", [])

                for title_match in title_matches:
                    title = clean_html(title_match.group(1))
                    # Search for URL in window before title
                    start = max(0, title_match.start() - 2000)
                    window = html[start:title_match.end()]

                    url_matches = re.findall(url_pattern, window)
                    # Filter out internal URLs
                    external_urls = [u for u in url_matches if not any(f in u.lower() for f in url_filters)]

                    if external_urls:
                        url = clean_url(external_urls[-1], engine)  # Use the last URL (closest to title)
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            results.append({
                                "title": title or "No title",
                                "url": url,
                                "snippet": ""
                            })
                            if len(results) >= max_results:
                                break

            elif pattern_type == "title_only":
                titles = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                has_separate_patterns = True
            elif pattern_type == "url_only":
                urls = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                has_separate_patterns = True

        if has_context_pattern:
            pass  # Already handled above
        elif has_separate_patterns and titles and urls:
            # Match titles with URLs (they should be in order)
            for i, title in enumerate(titles):
                if len(results) >= max_results:
                    break
                if i < len(urls):
                    url = clean_url(urls[i], engine)
                    if url and not url.startswith("#") and not url.startswith("javascript:"):
                        url_key = url.split("?")[0]
                        if url_key not in seen_urls:
                            seen_urls.add(url_key)
                            results.append({
                                "title": clean_html(title) or "No title",
                                "url": url,
                                "snippet": ""
                            })

        # Standard pattern matching
        if not results:
            for pattern, pattern_type in config["result_patterns"]:
                if pattern_type in ("title_only", "url_only"):
                    continue  # Skip these, already handled above

                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)

            for match in matches:
                if len(results) >= max_results:
                    break

                if pattern_type in ("title_url", "google_redirect", "baidu_link"):
                    url, title = match[0], match[1]
                elif pattern_type == "reverse":
                    title, url = match[0], match[1]
                else:
                    continue

                url = clean_url(url, engine)

                if not url or url.startswith("#") or url.startswith("javascript:"):
                    continue

                url_key = url.split("?")[0]
                if url_key in seen_urls:
                    continue
                seen_urls.add(url_key)

                results.append({
                    "title": clean_html(title) if title else "No title",
                    "url": url.strip(),
                    "snippet": ""  # Snippet extraction not available in fallback mode
                })

    return results


def search_with_html(
    query: str,
    engine: str,
    max_results: int = 5,
    timeout: int = 15,
    time_filter: Optional[str] = None
) -> Tuple[List[Dict], Optional[str]]:
    """
    Search by scraping HTML (fallback method).
    Returns (results, error_message).
    """
    if engine not in ENGINES:
        return [], f"Unknown engine: {engine}"

    config = ENGINES[engine]

    # Build URL with time filter
    url = config["url_template"].format(
        query=urllib.parse.quote_plus(query),
        num=max_results + 5
    )

    # Add time filter if supported
    if time_filter and time_filter in TIME_FILTERS:
        if engine in TIME_FILTERS[time_filter]:
            url += TIME_FILTERS[time_filter][engine]

    html, error = fetch_html(url, timeout)
    if html is None:
        return [], error

    results = parse_html_results(html, engine, max_results)
    return results, None


# ============================================================================
# Caching
# ============================================================================

def get_cache_key(query: str, engine: str, time_filter: Optional[str] = None) -> str:
    key = f"{query}:{engine}:{time_filter or 'all'}"
    return hashlib.md5(key.encode()).hexdigest()


def get_cached_result(query: str, engine: str, time_filter: Optional[str] = None) -> Optional[Dict]:
    try:
        cache_file = CACHE_DIR / f"{get_cache_key(query, engine, time_filter)}.json"
        if cache_file.exists():
            if time.time() - cache_file.stat().st_mtime < CACHE_TTL:
                return json.loads(cache_file.read_text())
    except:
        pass
    return None


def save_to_cache(query: str, engine: str, result: Dict, time_filter: Optional[str] = None):
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{get_cache_key(query, engine, time_filter)}.json"
        cache_file.write_text(json.dumps(result, ensure_ascii=False))
    except:
        pass


# ============================================================================
# Engine Health Check with Caching
# ============================================================================

def check_engine_health(engine: str, timeout: int = 10) -> Tuple[bool, float, str]:
    """
    Check if a search engine is working.
    Returns (is_healthy, response_time, method_used).
    """
    start_time = time.time()

    # Special handling for DuckDuckGo with library
    if engine == "duckduckgo" and HAS_DDGS:
        results, error = search_with_ddgs("test", max_results=1, timeout=timeout)
        response_time = time.time() - start_time
        if results:
            return True, response_time, "ddgs"
        return False, response_time, f"ddgs_error: {error}"[:50]

    # HTML-based check for other engines
    results, error = search_with_html("test", engine, max_results=1, timeout=timeout)
    response_time = time.time() - start_time

    if results:
        return True, response_time, "html"

    return False, response_time, f"html_error: {error}"[:50] if error else "no results"


def get_best_available_engine(timeout: int = 10, force_refresh: bool = False) -> Tuple[str, Dict]:
    """
    Find the best available search engine with caching.
    Returns (best_engine, health_status).
    """
    import threading

    # Check cache
    current_time = time.time()
    if not force_refresh and (current_time - ENGINE_HEALTH_CACHE["last_check"] < ENGINE_HEALTH_CACHE["ttl"]):
        return ENGINE_HEALTH_CACHE["best_engine"] or "bing", ENGINE_HEALTH_CACHE["data"]

    health_status = {}
    lock = threading.Lock()

    def check(e: str):
        is_healthy, response_time, method = check_engine_health(e, timeout)
        with lock:
            health_status[e] = {
                "healthy": is_healthy,
                "response_time": response_time,
                "method": method
            }

    # Check all engines in parallel
    threads = [threading.Thread(target=check, args=(e,), daemon=True) for e in ENGINES.keys()]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=timeout + 5)

    # Find best engine by priority
    best_engine = None
    best_score = -1

    for engine, status in health_status.items():
        if status["healthy"]:
            score = ENGINE_PRIORITY.get(engine, 0)
            if score > best_score:
                best_score = score
                best_engine = engine

    if best_engine is None:
        best_engine = "bing"  # Default fallback

    # Update cache
    ENGINE_HEALTH_CACHE["last_check"] = current_time
    ENGINE_HEALTH_CACHE["data"] = health_status
    ENGINE_HEALTH_CACHE["best_engine"] = best_engine

    return best_engine, health_status


# ============================================================================
# Main Search Function with Auto-Selection
# ============================================================================

def search(
    query: str,
    engine: str = "auto",
    max_results: int = 5,
    timeout: int = 30,
    use_cache: bool = True,
    auto_fallback: bool = True,
    time_filter: Optional[str] = None
) -> Dict:
    """
    Perform web search with automatic engine selection and failover.

    Args:
        query: Search query
        engine: Engine to use ("auto" or specific engine name)
        max_results: Maximum number of results
        timeout: Request timeout
        use_cache: Use cached results
        auto_fallback: Auto-switch to other engines on failure
        time_filter: Time filter (day/week/month/year)

    Returns:
        Dict with query, engine, results, and metadata
    """
    original_engine = engine

    # Auto-select best engine
    if engine == "auto":
        engine, health = get_best_available_engine(timeout=timeout // 2)
        print(f"[Auto-selected engine: {engine}]", file=sys.stderr)

    # Check cache
    if use_cache:
        cached = get_cached_result(query, engine, time_filter)
        if cached:
            cached["cached"] = True
            return cached

    # Try primary engine
    results = []
    error = None
    method = "unknown"

    # Try DuckDuckGo with library first
    if engine == "duckduckgo" and HAS_DDGS:
        proxy = get_proxy_url()
        results, error = search_with_ddgs(query, max_results, proxy, timeout, time_filter=time_filter)
        method = "duckduckgo_search library"
        if results:
            print(f"[Used: duckduckgo_search library]", file=sys.stderr)

    # Fallback to HTML scraping
    if not results and engine in ENGINES:
        results, error = search_with_html(query, engine, max_results, timeout, time_filter=time_filter)
        method = "HTML scraping"

    # Auto-fallback to other engines
    if not results and auto_fallback:
        print(f"[Primary engine failed, trying alternatives...]", file=sys.stderr)

        # Order by priority
        fallback_order = sorted(
            ENGINES.keys(),
            key=lambda x: ENGINE_PRIORITY.get(x, 0),
            reverse=True
        )

        for fallback_engine in fallback_order:
            if fallback_engine == engine:
                continue

            if fallback_engine == "duckduckgo" and HAS_DDGS:
                proxy = get_proxy_url()
                results, error = search_with_ddgs(query, max_results, proxy, timeout, time_filter=time_filter)
            elif fallback_engine in ENGINES:
                results, error = search_with_html(query, fallback_engine, max_results, timeout, time_filter=time_filter)

            if results:
                engine = fallback_engine
                print(f"[Fallback to: {engine}]", file=sys.stderr)
                break

    # Build result
    result = {
        "query": query,
        "engine": engine,
        "method": method,
        "results": results[:max_results],
        "total": len(results[:max_results])
    }

    if time_filter:
        result["time_filter"] = time_filter

    if not results:
        result["error"] = error or "No results found"
        result["engine"] = original_engine if original_engine != "auto" else engine

        # Add network diagnostic hints
        if not get_proxy_url():
            result["hint"] = "No proxy configured. If search fails, try setting ALL_PROXY environment variable."
        elif "timeout" in str(error).lower() or "connection" in str(error).lower():
            result["hint"] = "Network issue detected. Check your proxy settings (ALL_PROXY)."

    # Save to cache
    if use_cache and results:
        save_to_cache(query, engine, result, time_filter)

    return result


# ============================================================================
# Output Formatting
# ============================================================================

def format_markdown(results: Dict) -> str:
    lines = [f"## Search Results: {results.get('query', 'Unknown')}", ""]

    if "error" in results:
        lines.append(f"**Error**: {results['error']}")
        if "hint" in results:
            lines.append(f"")
            lines.append(f"**Hint**: {results['hint']}")
        return "\n".join(lines)

    lines.append(f"Engine: **{results.get('engine', 'Unknown').upper()}**")
    if results.get("method"):
        lines.append(f"Method: _{results['method']}_")
    if results.get("time_filter"):
        lines.append(f"Time: _{results['time_filter']}_")
    lines.append("")

    for i, item in enumerate(results.get("results", []), 1):
        title = item.get("title", "No title")
        url = item.get("url", "#")
        snippet = item.get("snippet", "")

        lines.append(f"{i}. [{title}]({url})")
        if snippet:
            # Truncate long snippets
            snippet_text = snippet[:200] + "..." if len(snippet) > 200 else snippet
            lines.append(f"   > {snippet_text}")
        lines.append("")

    if results.get("cached"):
        lines.append("_(from cache)_")

    return "\n".join(lines)


def format_csv(results: Dict) -> str:
    import io
    import csv

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Title", "URL", "Snippet", "Engine"])

    for item in results.get("results", []):
        snippet = item.get("snippet", "")
        writer.writerow([
            item.get("title", ""),
            item.get("url", ""),
            snippet[:150] if snippet else "",
            results.get("engine", "")
        ])

    return output.getvalue()


def format_simple(results: Dict) -> str:
    """Simple format for quick reading."""
    lines = []
    for i, item in enumerate(results.get("results", []), 1):
        title = item.get("title", "No title")
        url = item.get("url", "#")
        lines.append(f"{i}. {title}")
        lines.append(f"   {url}")
        if item.get("snippet"):
            lines.append(f"   {item['snippet'][:100]}...")
        lines.append("")
    return "\n".join(lines)


# ============================================================================
# Interactive Mode
# ============================================================================

def interactive_mode(default_engine: str = "auto", default_format: str = "md"):
    """Run interactive search mode."""
    print("=" * 50)
    print("  Easy Search Interactive Mode")
    print("  Type your query to search, or use commands:")
    print("  :engine <name>  - Change engine")
    print("  :format <fmt>   - Change format (json/md/csv/simple)")
    print("  :check          - Check engine health")
    print("  :help           - Show help")
    print("  :quit / :exit   - Exit")
    print("=" * 50)
    print()

    engine = default_engine
    fmt = default_format

    while True:
        try:
            user_input = input(f"[{engine}]> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith(":"):
            cmd = user_input.lower()

            if cmd in (":quit", ":exit", ":q"):
                print("Goodbye!")
                break

            elif cmd == ":help":
                print("\nCommands:")
                print("  :engine <name>  - Change search engine")
                print("                    Options: auto, duckduckgo, bing, google, baidu, sogou, so360, brave, yandex")
                print("  :format <fmt>   - Change output format")
                print("                    Options: json, md, csv, simple")
                print("  :check          - Check which engines are available")
                print("  :help           - Show this help")
                print("  :quit           - Exit interactive mode")
                print()

            elif cmd.startswith(":engine "):
                new_engine = user_input[8:].strip()
                if new_engine in list(ENGINES.keys()) + ["auto"]:
                    engine = new_engine
                    print(f"Engine set to: {engine}")
                else:
                    print(f"Unknown engine. Options: auto, {', '.join(ENGINES.keys())}")

            elif cmd.startswith(":format "):
                new_fmt = user_input[8:].strip()
                if new_fmt in ["json", "md", "csv", "simple"]:
                    fmt = new_fmt
                    print(f"Format set to: {fmt}")
                else:
                    print("Unknown format. Options: json, md, csv, simple")

            elif cmd == ":check":
                print("Checking engines...")
                best, health = get_best_available_engine(force_refresh=True)
                for eng, status in sorted(health.items(), key=lambda x: x[1]["response_time"]):
                    status_str = "OK" if status["healthy"] else "FAIL"
                    time_str = f"{status['response_time']:.2f}s"
                    print(f"  {eng:12} {status_str:4}  {time_str:>6}")
                print(f"\nBest engine: {best}")

            else:
                print(f"Unknown command: {cmd}")
                print("Type :help for available commands")

            continue

        # Perform search
        result = search(user_input, engine=engine)

        # Output result
        if fmt == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif fmt == "md":
            print(format_markdown(result))
        elif fmt == "csv":
            print(format_csv(result))
        else:
            print(format_simple(result))

        print()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"Easy web search v{VERSION} - No API key required",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s Python tutorial
  %(prog)s -q "AI news" --engine auto
  %(prog)s "React hooks" --engine duckduckgo --format md
  %(prog)s -q "latest news" --time day
  %(prog)s --interactive
  %(prog)s --check-engines

Engine Options:
  auto        - Auto-select best available engine (default)
  duckduckgo  - Use DuckDuckGo (preferred, uses library if available)
  bing        - Use Bing
  google      - Use Google
  baidu       - Use Baidu (Chinese content)
  sogou       - Use Sogou (Chinese content)
  so360       - Use 360 Search (Chinese content)
  brave       - Use Brave Search
  yandex      - Use Yandex

Time Filter Options:
  day         - Results from last 24 hours
  week        - Results from last week
  month       - Results from last month
  year        - Results from last year

Output Formats:
  json        - JSON format (default)
  md          - Markdown format
  csv         - CSV format
  simple      - Simple text format
        """
    )

    parser.add_argument("query", nargs="?", help="Search query (can be positional)")
    parser.add_argument("--query", "-q", help="Search query (alternative flag)")
    parser.add_argument("--engine", "-e", default="auto",
                        choices=["auto"] + list(ENGINES.keys()),
                        help="Search engine (default: auto)")
    parser.add_argument("--results", "-r", type=int, default=5,
                        help="Number of results (default: 5)")
    parser.add_argument("--format", "-f", default="json",
                        choices=["json", "md", "csv", "simple"],
                        help="Output format (default: json)")
    parser.add_argument("--time", "-t", dest="time_filter",
                        choices=["day", "week", "month", "year"],
                        help="Time filter for results")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Request timeout (default: 30)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Disable caching")
    parser.add_argument("--no-fallback", action="store_true",
                        help="Disable automatic engine fallback")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Clear result cache")
    parser.add_argument("--check-engines", action="store_true",
                        help="Check which engines are available")
    parser.add_argument("--diagnose", action="store_true",
                        help="Run network diagnostics")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Start interactive mode")
    parser.add_argument("--version", "-v", action="version",
                        version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    # Handle cache clearing
    if args.clear_cache:
        try:
            import shutil
            if CACHE_DIR.exists():
                shutil.rmtree(CACHE_DIR)
            print("Cache cleared.")
        except Exception as e:
            print(f"Error clearing cache: {e}")
        return

    # Handle engine health check
    if args.check_engines:
        print("Checking search engines...")
        print()
        best, health = get_best_available_engine(force_refresh=True)
        for engine, status in sorted(health.items(), key=lambda x: x[1]["response_time"]):
            status_str = "OK" if status["healthy"] else "FAIL"
            time_str = f"{status['response_time']:.2f}s" if status["response_time"] else "N/A"
            method = status.get("method", "unknown")
            print(f"  {engine:12} {status_str:4}  {time_str:>6}  ({method})")
        print()
        print(f"Best engine: {best}")
        # Add proxy hint if all engines fail
        healthy_count = sum(1 for s in health.values() if s["healthy"])
        if healthy_count == 0 and not get_proxy_url():
            print()
            print("All engines failed. Consider setting a proxy:")
            print("  export ALL_PROXY='http://127.0.0.1:7890'")
        return

    # Handle network diagnostics
    if args.diagnose:
        print("=" * 50)
        print("  Easy Search Network Diagnostics")
        print("=" * 50)
        print()

        # Check proxy
        proxy = get_proxy_url()
        print(f"Proxy: {proxy if proxy else 'Not configured'}")
        print()

        # Check dependencies
        print("Dependencies:")
        print(f"  duckduckgo_search: {'Installed' if HAS_DDGS else 'Not installed'}")
        print(f"  requests: {'Installed' if HAS_REQUESTS else 'Not installed'}")
        print()

        # Test connectivity
        print("Network connectivity:")
        test_urls = [
            ("Bing", "https://www.bing.com"),
            ("Google", "https://www.google.com"),
            ("DuckDuckGo", "https://duckduckgo.com"),
        ]

        import socket
        socket.setdefaulttimeout(5)

        for name, url in test_urls:
            try:
                if HAS_REQUESTS:
                    resp = requests.get(url, timeout=5, headers={"User-Agent": USER_AGENTS[0]})
                    status = f"OK ({resp.status_code})"
                else:
                    import urllib.request
                    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENTS[0]})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        status = f"OK ({resp.status})"
            except Exception as e:
                status = f"FAIL ({str(e)[:30]})"
            print(f"  {name:15} {status}")

        print()

        # Recommendations
        print("Recommendations:")
        if not proxy:
            print("  - No proxy configured. If connectivity fails, try:")
            print("    export ALL_PROXY='http://127.0.0.1:7890'")
        if not HAS_DDGS:
            print("  - Install duckduckgo_search for better stability:")
            print("    pip install duckduckgo-search")
        if not HAS_REQUESTS:
            print("  - Install requests for better HTTP handling:")
            print("    pip install requests")

        return

    # Handle interactive mode
    if args.interactive:
        interactive_mode(default_engine=args.engine, default_format=args.format)
        return

    # Get query from positional or flag argument
    query = args.query or args.q

    # Require query for search
    if not query:
        parser.error("Query is required for search (positional or --query/-q)")

    # Perform search
    result = search(
        query,
        engine=args.engine,
        max_results=args.results,
        timeout=args.timeout,
        use_cache=not args.no_cache,
        auto_fallback=not args.no_fallback,
        time_filter=args.time_filter
    )

    # Output
    if args.format == "md":
        print(format_markdown(result))
    elif args.format == "csv":
        print(format_csv(result))
    elif args.format == "simple":
        print(format_simple(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()