"""Jina API client for enhanced reading and web search."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

import requests

from datapulse.core.retry import CircuitBreaker, retry
from datapulse.core.security import get_secret

logger = logging.getLogger("datapulse.jina_client")


@dataclass
class JinaReadOptions:
    """Options for Jina Reader API."""

    response_format: str = "markdown"  # markdown | html | text | screenshot
    target_selector: str = ""  # CSS selector for targeted extraction
    wait_for_selector: str = ""  # Wait for element before extraction
    no_cache: bool = False  # Bypass Jina cache
    with_generated_alt: bool = False  # VLM image descriptions
    cookie: str = ""  # Cookie passthrough
    use_post: bool = False  # POST mode for SPA hash routes


@dataclass
class JinaSearchOptions:
    """Options for Jina Search API."""

    sites: list[str] = field(default_factory=list)  # Restrict to domains
    limit: int = 5  # Max results


@dataclass
class JinaReadResult:
    """Result from Jina Reader API."""

    url: str
    content: str
    status_code: int


@dataclass
class JinaSearchResult:
    """Single search result from Jina Search API."""

    title: str
    url: str
    description: str
    content: str


class JinaBlockedByPolicyError(RuntimeError):
    """Raised when Jina returns policy/legal blocking statuses (e.g., 451)."""

    def __init__(self, message: str, status_code: int, response: requests.Response):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


def _extract_jina_error_hint(response: requests.Response) -> str:
    text = (response.text or "").strip()
    if text:
        return text[:512]
    if body := response.headers.get("Link"):
        return body[:512]
    return f"HTTP {response.status_code} {response.reason}"


class JinaAPIClient:
    """Unified client for Jina Reader and Search APIs."""

    READ_API = "https://r.jina.ai/"
    SEARCH_API = "https://s.jina.ai/"

    def __init__(
        self,
        api_key: str | None = None,
        proxy_url: str = "",
        timeout: int = 30,
    ):
        self.api_key = get_secret("JINA_API_KEY") if api_key is None else api_key
        self.proxy_url = proxy_url
        self.timeout = timeout
        self._read_cb = CircuitBreaker(failure_threshold=5, recovery_timeout=60.0, name="jina_read")
        self._search_cb = CircuitBreaker(failure_threshold=5, recovery_timeout=60.0, name="jina_search")

    def read(self, url: str, *, options: JinaReadOptions | None = None) -> JinaReadResult:
        """Read a URL via Jina Reader API."""
        opts = options or JinaReadOptions()
        return self._read_cb.call(self._do_read, url, opts)

    @retry(max_attempts=2, base_delay=1.0, retryable=(requests.RequestException,))
    def _do_read(self, url: str, opts: JinaReadOptions) -> JinaReadResult:
        headers = self._build_read_headers(opts)

        if opts.use_post:
            resp = requests.post(
                self.READ_API,
                headers=headers,
                json={"url": url},
                timeout=self.timeout,
            )
        else:
            resp = requests.get(
                f"{self.READ_API}{url}",
                headers=headers,
                timeout=self.timeout,
            )

        self._raise_for_status_if_blocked(resp, "read")
        resp.raise_for_status()
        return JinaReadResult(
            url=url,
            content=resp.text or "",
            status_code=resp.status_code,
        )

    def _build_read_headers(self, opts: JinaReadOptions) -> dict[str, str]:
        headers: dict[str, str] = {
            "Accept": "application/json",
            "X-Respond-With": opts.response_format,
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if opts.target_selector:
            headers["X-Target-Selector"] = opts.target_selector
        if opts.wait_for_selector:
            headers["X-Wait-For-Selector"] = opts.wait_for_selector
        if opts.no_cache:
            headers["X-No-Cache"] = "true"
        if opts.with_generated_alt:
            headers["X-With-Generated-Alt"] = "true"
        if opts.cookie:
            headers["X-Set-Cookie"] = opts.cookie
        if self.proxy_url:
            headers["X-Proxy-URL"] = self.proxy_url
        return headers

    def search(self, query: str, *, options: JinaSearchOptions | None = None) -> list[JinaSearchResult]:
        """Search the web via Jina Search API. Requires API key."""
        if not self.api_key:
            raise ValueError("Jina API key required for search. Set JINA_API_KEY or pass api_key.")
        opts = options or JinaSearchOptions()
        return self._search_cb.call(self._do_search, query, opts)

    def _do_search(self, query: str, opts: JinaSearchOptions) -> list[JinaSearchResult]:
        search_query = query
        if opts.sites:
            site_clauses = " ".join(f"site:{s}" for s in opts.sites)
            search_query = f"{query} {site_clauses}"

        headers: dict[str, str] = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        resp = requests.get(
            f"{self.SEARCH_API}{search_query}",
            headers=headers,
            timeout=self.timeout,
        )

        self._raise_for_status_if_blocked(resp, "search")
        resp.raise_for_status()
        return self._parse_search_results(resp.text, limit=opts.limit)

    @staticmethod
    def _raise_for_status_if_blocked(response: requests.Response, context: str) -> None:
        if response.status_code in {403, 451}:
            hint = _extract_jina_error_hint(response)
            message = (
                f"Jina {context} blocked by policy ({response.status_code}): {hint}"
            )
            logger.info(message)
            raise JinaBlockedByPolicyError(message, response.status_code, response)

    @staticmethod
    def _parse_search_results(text: str, limit: int = 5) -> list[JinaSearchResult]:
        """Parse Jina search markdown response into structured results."""
        if not text.strip():
            return []

        results: list[JinaSearchResult] = []
        # Split by separator (---) between results
        blocks = re.split(r"\n---\n", text)

        for block in blocks:
            if len(results) >= limit:
                break
            block = block.strip()
            if not block:
                continue

            title = ""
            url = ""
            description = ""
            content = ""

            title_match = re.search(r"^Title:\s*(.+)$", block, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()

            url_match = re.search(r"^URL Source:\s*(.+)$", block, re.MULTILINE)
            if url_match:
                url = url_match.group(1).strip()

            desc_match = re.search(r"^Description:\s*(.+)$", block, re.MULTILINE)
            if desc_match:
                description = desc_match.group(1).strip()

            content_match = re.search(r"Markdown Content:\n(.+)", block, re.DOTALL)
            if content_match:
                content = content_match.group(1).strip()

            if url:  # At minimum need a URL
                results.append(JinaSearchResult(
                    title=title,
                    url=url,
                    description=description,
                    content=content,
                ))

        return results
