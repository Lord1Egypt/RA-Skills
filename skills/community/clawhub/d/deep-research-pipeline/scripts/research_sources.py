"""Research Source Adapters — Multi-source search for the Researcher Agent.

Provides source adapters that search different information sources:
- WebSearchSource: Free web search via DuckDuckGo Lite + content fetching
- GitHubSource: GitHub public API (repos, code, issues)
- DocSource: Direct documentation URL fetching and extraction

Each adapter has a search(query, limit) → list[dict] method returning results
with {title, url, content, source_type, relevance_score}.

All adapters use urllib.request for HTTP. GitHub API works without auth for
public repos (60 req/hr unauthenticated). Web search uses DuckDuckGo Lite.

Usage:
    from research_sources import WebSearchSource, GitHubSource, DocSource

    web = WebSearchSource()
    results = web.search("OpenClaw skills system", limit=5)

    gh = GitHubSource()
    results = gh.search("openclaw", limit=5)

    doc = DocSource()
    results = doc.search("https://docs.python.org/3/", limit=3)
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from typing import Optional
from xml.etree import ElementTree

from llm_client import call_llm as _call_glm

# ─── Shared helpers ───────────────────────────────────────────────────────────

def _fetch_url(url: str, max_chars: int = 30000, timeout: int = 15) -> Optional[str]:
    """Fetch a URL and return text content. Returns None on failure."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text" not in content_type and "json" not in content_type:
                return None
            return resp.read(max_chars).decode(errors="replace")
    except Exception:
        return None


def _extract_text(html_content: str) -> str:
    """Rough HTML-to-text extraction: strip tags, decode entities, normalize whitespace."""
    # Remove script and style blocks
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Decode HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _content_hash(content: str) -> str:
    """SHA256 hash of content for deduplication."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _normalize_url(url: str) -> str:
    """Normalize URL for dedup (strip trailing slash, fragment, lowercase host)."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname.lower() if parsed.hostname else ""
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{host}{path}"


# ─── Base Source ──────────────────────────────────────────────────────────────


class BaseSource:
    """Base class for research source adapters."""

    source_type: str = "base"

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search for results matching query.

        Returns list of dicts with:
            - title: str
            - url: str
            - content: str (main body text)
            - source_type: str
            - relevance_score: float (0.0-1.0)
        """
        raise NotImplementedError


# ─── WebSearchSource ──────────────────────────────────────────────────────────


class WebSearchSource(BaseSource):
    """Web search via DuckDuckGo Lite HTML endpoint (free, no API key).

    Falls back to generating search URLs if DuckDuckGo is blocked.
    Fetches full content from top result URLs.
    """

    source_type = "web"

    # DuckDuckGo Lite endpoint
    DDG_LITE = "https://lite.duckduckgo.com/lite/"
    # DuckDuckGo HTML endpoint (more reliable for scraping)
    DDG_HTML = "https://html.duckduckgo.com/html/"

    def __init__(self, fetch_content: bool = True):
        """Args:
            fetch_content: If True, fetch full content from result URLs.
        """
        self.fetch_content = fetch_content

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search DuckDuckGo and return results with content."""
        # Try DuckDuckGo HTML endpoint first
        results = self._search_ddg_html(query, limit)
        if not results:
            # Fallback to lite endpoint
            results = self._search_ddg_lite(query, limit)

        if self.fetch_content:
            results = self._fetch_results_content(results)

        # Add metadata
        for r in results:
            r["source_type"] = self.source_type
            r["content_hash"] = _content_hash(r.get("content", ""))

        return results

    def _search_ddg_html(self, query: str, limit: int) -> list[dict]:
        """Search via DuckDuckGo HTML endpoint."""
        try:
            form_data = urllib.parse.urlencode({"q": query}).encode()
            req = urllib.request.Request(
                self.DDG_HTML,
                data=form_data,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                html_content = resp.read(100000).decode(errors="replace")

            return self._parse_ddg_html(html_content, limit)
        except Exception:
            return []

    def _parse_ddg_html(self, html_content: str, limit: int) -> list[dict]:
        """Parse DuckDuckGo HTML search results."""
        results = []

        # DuckDuckGo HTML wraps results in <a class="result__a"> with href
        # and snippets in <a class="result__snippet">
        # Links are redirect URLs: https://duckduckgo.com/l/?uddg=ENCODED_URL
        for match in re.finditer(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            html_content,
            re.DOTALL,
        ):
            raw_href = html.unescape(match.group(1))
            title = _extract_text(match.group(2))

            # Extract real URL from DDG redirect
            real_url = self._extract_ddg_url(raw_href)
            if not real_url:
                continue

            results.append({"title": title.strip(), "url": real_url, "content": ""})

            if len(results) >= limit:
                break

        # Also try to extract snippets
        snippet_matches = re.findall(
            r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
            html_content,
            re.DOTALL,
        )
        for i, snippet in enumerate(snippet_matches):
            if i < len(results):
                results[i]["snippet"] = _extract_text(snippet)

        return results

    def _extract_ddg_url(self, href: str) -> Optional[str]:
        """Extract real URL from DuckDuckGo redirect URL."""
        parsed = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(parsed.query)

        # DDG uses uddg parameter for the real URL
        if "uddg" in params:
            return params["uddg"][0]

        # If it's already a direct URL
        if href.startswith("http"):
            return href

        return None

    def _search_ddg_lite(self, query: str, limit: int) -> list[dict]:
        """Search via DuckDuckGo Lite endpoint (simpler parsing)."""
        try:
            form_data = urllib.parse.urlencode({"q": query}).encode()
            req = urllib.request.Request(
                self.DDG_LITE,
                data=form_data,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                html_content = resp.read(100000).decode(errors="replace")

            return self._parse_ddg_lite(html_content, limit)
        except Exception:
            return []

    def _parse_ddg_lite(self, html_content: str, limit: int) -> list[dict]:
        """Parse DuckDuckGo Lite search results (table-based layout)."""
        results = []

        # DDG Lite uses tables with class="result-link"
        for match in re.finditer(
            r'<a[^>]+class="result-link"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            html_content,
            re.DOTALL,
        ):
            raw_href = html.unescape(match.group(1))
            title = _extract_text(match.group(2))
            real_url = self._extract_ddg_url(raw_href)
            if not real_url:
                continue
            results.append({"title": title.strip(), "url": real_url, "content": ""})
            if len(results) >= limit:
                break

        # Extract snippets from table cells
        snippet_cells = re.findall(
            r'<td[^>]+class="result-snippet"[^>]*>(.*?)</td>',
            html_content,
            re.DOTALL,
        )
        for i, snippet in enumerate(snippet_cells):
            if i < len(results):
                results[i]["snippet"] = _extract_text(snippet)

        return results

    def _fetch_results_content(self, results: list[dict]) -> list[dict]:
        """Fetch full content from result URLs."""
        for r in results:
            url = r.get("url", "")
            if not url or url.startswith("https://duckduckgo.com"):
                continue
            content = _fetch_url(url)
            if content:
                r["content"] = _extract_text(content)[:8000]
            elif "snippet" in r:
                r["content"] = r["snippet"]
        return results


# ─── GitHubSource ─────────────────────────────────────────────────────────────


class GitHubSource(BaseSource):
    """GitHub search via public REST API.

    Searches repositories and code. No auth required for public repos
    (60 requests/hour limit). Set GITHUB_TOKEN env var for higher limits.

    Usage:
        gh = GitHubSource()
        repos = gh.search("openclaw", limit=5)
        code = gh.search_code("SKILL.md openclaw", limit=5)
    """

    source_type = "github"
    API_BASE = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search GitHub repositories and code."""
        repos = self._search_repos(query, limit)
        code = self._search_code(query, max(1, limit - len(repos)))
        return repos + code

    def search_repos(self, query: str, limit: int = 5) -> list[dict]:
        """Search only repositories."""
        return self._search_repos(query, limit)

    def search_code(self, query: str, limit: int = 5) -> list[dict]:
        """Search only code."""
        return self._search_code(query, limit)

    def _api_request(self, path: str, params: dict = None) -> Optional[dict]:
        """Make a GitHub API request."""
        url = f"{self.API_BASE}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        headers = {
            "User-Agent": "ResearchBot/1.0",
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"GitHub API rate limit hit. Set GITHUB_TOKEN for higher limits.", file=sys.stderr)
            return None
        except Exception:
            return None

    def _search_repos(self, query: str, limit: int) -> list[dict]:
        """Search GitHub repositories."""
        data = self._api_request("/search/repositories", {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit,
        })

        if not data or "items" not in data:
            return []

        results = []
        for item in data["items"][:limit]:
            results.append({
                "title": item.get("full_name", ""),
                "url": item.get("html_url", ""),
                "content": item.get("description", "") or "",
                "source_type": self.source_type,
                "relevance_score": 0.5,  # Default, can be re-scored later
                "metadata": {
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language", ""),
                    "updated": item.get("updated_at", ""),
                    "topics": item.get("topics", []),
                    "forks": item.get("forks_count", 0),
                },
                "content_hash": _content_hash(item.get("description", "")),
            })
        return results

    def _search_code(self, query: str, limit: int) -> list[dict]:
        """Search GitHub code."""
        data = self._api_request("/search/code", {
            "q": query,
            "per_page": limit,
        })

        if not data or "items" not in data:
            return []

        results = []
        for item in data["items"][:limit]:
            # Fetch the file content if it's small
            raw_url = item.get("html_url", "").replace(
                "github.com", "raw.githubusercontent.com"
            ).replace("/blob/", "/")

            content = ""
            if raw_url:
                fetched = _fetch_url(raw_url, max_chars=5000)
                if fetched:
                    content = fetched[:5000]

            results.append({
                "title": f"{item.get('name', '')} in {item.get('repository', {}).get('full_name', '')}",
                "url": item.get("html_url", ""),
                "content": content,
                "source_type": self.source_type,
                "relevance_score": 0.5,
                "metadata": {
                    "repo": item.get("repository", {}).get("full_name", ""),
                    "path": item.get("path", ""),
                },
                "content_hash": _content_hash(content),
            })
        return results


# ─── DocSource ────────────────────────────────────────────────────────────────


class DocSource(BaseSource):
    """Documentation source — fetches and extracts content from documentation URLs.

    Can be used with specific URLs or auto-discover docs for known projects.

    Usage:
        doc = DocSource()
        # Direct URL fetch
        results = doc.search("https://docs.python.org/3/library/urllib.html", limit=1)

        # Auto-discover docs for a topic
        results = doc.discover_docs("python urllib", limit=3)
    """

    source_type = "docs"

    # Common documentation URL patterns
    DOC_PATTERNS = {
        "python": ["https://docs.python.org/3/"],
        "react": ["https://react.dev/reference"],
        "node": ["https://nodejs.org/docs/latest/api/"],
        "rust": ["https://doc.rust-lang.org/"],
        "go": ["https://pkg.go.dev/"],
        "docker": ["https://docs.docker.com/"],
        "kubernetes": ["https://kubernetes.io/docs/"],
        "fastapi": ["https://fastapi.tiangolo.com/"],
        "django": ["https://docs.djangoproject.com/"],
        "postgres": ["https://www.postgresql.org/docs/current/"],
    }

    def __init__(self, fetch_content: bool = True):
        self.fetch_content = fetch_content

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Fetch documentation from a URL or search for relevant docs.

        If query looks like a URL, fetch it directly.
        Otherwise, try to discover relevant documentation pages.
        """
        # If query is a URL, fetch directly
        if query.startswith("http://") or query.startswith("https://"):
            return self._fetch_doc_page(query)

        # Try to discover docs for known projects
        results = self._discover_from_known_patterns(query, limit)

        if not results:
            # Fallback: use DuckDuckGo with site:docs restriction
            results = self._search_docs_ddg(query, limit)

        return results

    def discover_docs(self, query: str, limit: int = 5) -> list[dict]:
        """Discover documentation pages for a topic."""
        return self.search(query, limit)

    def _fetch_doc_page(self, url: str) -> list[dict]:
        """Fetch a single documentation page."""
        content = _fetch_url(url, max_chars=40000)
        if not content:
            return []

        text = _extract_text(content)[:15000]
        # Try to extract a title from the page
        title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else url

        # Try to extract h1 as a better title
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            h1_text = _extract_text(h1_match.group(1)).strip()
            if len(h1_text) > 3 and len(h1_text) < 200:
                title = h1_text

        return [{
            "title": title,
            "url": url,
            "content": text,
            "source_type": self.source_type,
            "relevance_score": 0.7,  # Direct doc fetch gets a boost
            "content_hash": _content_hash(text),
        }]

    def _discover_from_known_patterns(self, query: str, limit: int) -> list[dict]:
        """Try to find documentation for known projects based on query keywords."""
        results = []
        query_lower = query.lower()

        for project, base_urls in self.DOC_PATTERNS.items():
            if project in query_lower:
                for base_url in base_urls:
                    content = _fetch_url(base_url, max_chars=20000)
                    if content:
                        text = _extract_text(content)[:10000]
                        results.append({
                            "title": f"{project.capitalize()} Documentation",
                            "url": base_url,
                            "content": text,
                            "source_type": self.source_type,
                            "relevance_score": 0.6,
                            "content_hash": _content_hash(text),
                        })
                    if len(results) >= limit:
                        return results

        return results

    def _search_docs_ddg(self, query: str, limit: int) -> list[dict]:
        """Search DuckDuckGo for documentation pages (site-restricted)."""
        # Build doc-focused search queries
        doc_queries = [
            f"{query} documentation",
            f"{query} docs guide",
            f"{query} official documentation",
        ]

        results = []
        seen_urls = set()

        for dq in doc_queries[:2]:  # Limit to 2 sub-queries
            try:
                form_data = urllib.parse.urlencode({"q": dq}).encode()
                req = urllib.request.Request(
                    WebSearchSource.DDG_HTML,
                    data=form_data,
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    html_content = resp.read(50000).decode(errors="replace")

                web_source = WebSearchSource(fetch_content=False)
                ddg_results = web_source._parse_ddg_html(html_content, limit)

                for r in ddg_results:
                    url = r.get("url", "")
                    norm_url = _normalize_url(url)
                    if norm_url in seen_urls:
                        continue
                    seen_urls.add(norm_url)

                    # Filter for likely doc pages
                    doc_indicators = [
                        "/docs/", "/doc/", "/documentation", "docs.",
                        "/reference", "/api/", "/guide", "/tutorial",
                        "readthedocs.io", "devdocs.io",
                    ]
                    is_doc = any(ind in url.lower() for ind in doc_indicators)

                    # Fetch content for likely doc pages
                    if is_doc and self.fetch_content:
                        content = _fetch_url(url, max_chars=30000)
                        if content:
                            r["content"] = _extract_text(content)[:12000]
                            r["source_type"] = self.source_type
                            r["relevance_score"] = 0.6
                            r["content_hash"] = _content_hash(r["content"])
                            results.append(r)
                            if len(results) >= limit:
                                return results

            except Exception:
                continue

        return results


# ─── Relevance Scorer ─────────────────────────────────────────────────────────


def score_results(
    results: list[dict],
    topic: str,
    use_llm: bool = True,
) -> list[dict]:
    """Score results by relevance to the original research topic.

    If use_llm=True and an LLM is configured, uses the shared client for intelligent scoring.
    Otherwise falls back to keyword-based scoring.

    Returns results sorted by relevance_score descending.
    """
    if not results:
        return []

    if use_llm:
        return _score_with_llm(results, topic)
    else:
        return _score_keyword(results, topic)


def _score_with_llm(results: list[dict], topic: str) -> list[dict]:
    """Score results using GLM for semantic relevance."""
    # Batch results to avoid context overflow (max ~8 results per batch)
    BATCH_SIZE = 8
    all_scored = []

    for i in range(0, len(results), BATCH_SIZE):
        batch = results[i : i + BATCH_SIZE]
        scored = _score_batch_llm(batch, topic, offset=i)
        all_scored.extend(scored)

    all_scored.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    return all_scored


def _score_batch_llm(batch: list[dict], topic: str, offset: int = 0) -> list[dict]:
    """Score a batch of results using GLM."""
    system = (
        "You are a research relevance scorer. Score each search result's "
        "relevance to the research topic on a scale of 0.0 to 1.0.\n\n"
        "Scoring:\n"
        "- 1.0: Directly answers or is essential for the topic\n"
        "- 0.8: Highly relevant supporting information\n"
        "- 0.6: Somewhat relevant but tangential\n"
        "- 0.4: Loosely related\n"
        "- 0.2: Barely related\n"
        "- 0.0: Irrelevant\n\n"
        "Output ONLY JSON array: [{\"index\": N, \"score\": 0.X, \"reason\": \"...\"}]"
    )

    numbered = []
    for i, r in enumerate(batch):
        content_preview = (r.get("content") or "")[:500]
        numbered.append(
            f"[{i}] {r.get('title', 'Untitled')} ({r.get('url', 'unknown')})\n"
            f"{content_preview}"
        )

    prompt = (
        f"Research topic: {topic}\n\n"
        f"Results to score:\n{chr(10).join(numbered)}\n\n"
        "Score each result."
    )

    try:
        response = _call_glm(prompt, system, max_tokens=2048, temperature=0.1)
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        scores = json.loads(response)
        if not isinstance(scores, list):
            scores = [scores]

        score_map = {s.get("index", 0): s for s in scores}

        result = []
        for i, r in enumerate(batch):
            merged = {**r}
            if i in score_map:
                merged["relevance_score"] = float(score_map[i].get("score", 0.5))
                merged["relevance_reason"] = score_map[i].get("reason", "")
            else:
                merged["relevance_score"] = 0.5
            result.append(merged)

        return result

    except Exception:
        # Fallback to keyword scoring
        return _score_keyword(batch, topic)


def _score_keyword(results: list[dict], topic: str) -> list[dict]:
    """Simple keyword-based relevance scoring (fallback)."""
    topic_words = set(topic.lower().split())
    # Remove common stop words
    stop_words = {"a", "an", "the", "is", "are", "was", "were", "be", "been",
                  "being", "have", "has", "had", "do", "does", "did", "will",
                  "would", "could", "should", "may", "might", "can", "shall",
                  "how", "what", "when", "where", "which", "who", "why", "in",
                  "on", "at", "to", "for", "of", "with", "by", "from", "and",
                  "or", "but", "not", "this", "that", "it"}
    topic_words -= stop_words

    scored = []
    for r in results:
        text = f"{r.get('title', '')} {r.get('content', '')}".lower()
        words = set(text.split())

        if not topic_words:
            score = 0.5
        else:
            overlap = len(topic_words & words)
            score = min(1.0, overlap / max(1, len(topic_words)) * 1.5)
            # Boost if title matches
            title_words = set(r.get("title", "").lower().split())
            title_overlap = len(topic_words & title_words)
            score = min(1.0, score + title_overlap * 0.1)

        scored.append({**r, "relevance_score": round(score, 2)})

    scored.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    return scored


# ─── Deduplication ────────────────────────────────────────────────────────────


def deduplicate_results(results: list[dict]) -> list[dict]:
    """Deduplicate results by URL and content hash.

    Keeps the result with higher relevance_score when duplicates found.
    """
    seen_urls = set()
    seen_hashes = set()
    unique = []

    for r in sorted(results, key=lambda x: x.get("relevance_score", 0), reverse=True):
        url = _normalize_url(r.get("url", ""))
        content_hash = r.get("content_hash", "")

        if url and url in seen_urls:
            continue
        if content_hash and content_hash in seen_hashes:
            continue

        if url:
            seen_urls.add(url)
        if content_hash:
            seen_hashes.add(content_hash)

        unique.append(r)

    return unique


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Research source adapters")
    sub = parser.add_subparsers(dest="command")

    # Web search
    wp = sub.add_parser("web")
    wp.add_argument("query")
    wp.add_argument("--limit", "-n", type=int, default=5)
    wp.add_argument("--no-fetch", action="store_true", help="Skip content fetching")

    # GitHub search
    gp = sub.add_parser("github")
    gp.add_argument("query")
    gp.add_argument("--limit", "-n", type=int, default=5)
    gp.add_argument("--repos-only", action="store_true")
    gp.add_argument("--code-only", action="store_true")

    # Docs search
    dp = sub.add_parser("docs")
    dp.add_argument("query")
    dp.add_argument("--limit", "-n", type=int, default=3)

    # Score results
    sp = sub.add_parser("score")
    sp.add_argument("topic")
    sp.add_argument("--input", "-i", help="JSON file with results (or stdin)")
    sp.add_argument("--stdin", action="store_true")

    args = parser.parse_args()

    if args.command == "web":
        source = WebSearchSource(fetch_content=not args.no_fetch)
        results = source.search(args.query, args.limit)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.command == "github":
        source = GitHubSource()
        if args.code_only:
            results = source.search_code(args.query, args.limit)
        elif args.repos_only:
            results = source.search_repos(args.query, args.limit)
        else:
            results = source.search(args.query, args.limit)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.command == "docs":
        source = DocSource()
        results = source.search(args.query, args.limit)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.command == "score":
        if args.stdin or not args.input:
            data = json.load(sys.stdin)
        else:
            with open(args.input) as f:
                data = json.load(f)
        scored = score_results(data, args.topic)
        print(json.dumps(scored, indent=2, ensure_ascii=False))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
