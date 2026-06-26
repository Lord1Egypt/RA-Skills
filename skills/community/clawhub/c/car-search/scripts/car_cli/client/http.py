"""HTTP client wrapper with anti-detection headers, jitter delays, burst detection, and retry."""

import asyncio
import collections
import logging
import random
import time

import httpx

from car_cli.logging_config import get_logger

_log = get_logger("http")

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "sec-ch-ua": '"Chromium";v="145", "Google Chrome";v="145", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}

MAX_RETRIES = 3
BACKOFF_BASE = 10
BACKOFF_CAP = 60

BURST_WINDOW_SIZE = 12
BURST_SHORT_WINDOW = 15
BURST_SHORT_THRESHOLD = 3
BURST_SHORT_PENALTY = (1.2, 2.8)
BURST_LONG_WINDOW = 45
BURST_LONG_THRESHOLD = 6
BURST_LONG_PENALTY = (4.0, 7.0)


class HttpClient:
    """Async HTTP client with anti-detection, burst detection, and retry logic."""

    _base_delay_multiplier: float = 1.0

    def __init__(self, base_url: str = "", referer: str = "", extra_headers: dict[str, str] | None = None):
        self._request_history: collections.deque = collections.deque(maxlen=BURST_WINDOW_SIZE)
        headers = dict(DEFAULT_HEADERS)
        if referer:
            headers["Referer"] = referer
        if extra_headers:
            headers.update(extra_headers)
        self._client = httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
            timeout=httpx.Timeout(30.0),
            http2=False,
        )
        self._base_url = base_url

    async def _jitter_delay(self):
        if random.random() < 0.05:
            delay = random.uniform(2.0, 5.0)
        else:
            delay = max(0.1, random.gauss(1.0, 0.3))

        delay *= self._base_delay_multiplier

        now = time.monotonic()
        timestamps = list(self._request_history)

        if timestamps:
            recent_short = sum(1 for t in timestamps if now - t < BURST_SHORT_WINDOW)
            if recent_short >= BURST_SHORT_THRESHOLD:
                delay += random.uniform(*BURST_SHORT_PENALTY)

            recent_long = sum(1 for t in timestamps if now - t < BURST_LONG_WINDOW)
            if recent_long >= BURST_LONG_THRESHOLD:
                delay += random.uniform(*BURST_LONG_PENALTY)

        _log.debug(
            "jitter delay=%.2fs multiplier=%.2f",
            delay,
            self._base_delay_multiplier,
        )
        await asyncio.sleep(delay)
        self._request_history.append(time.monotonic())

    def set_referer(self, referer: str):
        self._client.headers["Referer"] = referer

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """GET with jitter delay, burst detection, and exponential backoff retry."""
        if not url.startswith("http"):
            url = self._base_url.rstrip("/") + "/" + url.lstrip("/")

        cookies = kwargs.get("cookies")
        _log.debug(
            "GET %s cookies=%s params=%s",
            url,
            "yes" if cookies else "no",
            {k: v for k, v in kwargs.items() if k not in ("cookies", "headers")},
        )

        await self._jitter_delay()

        last_exc = None
        t0 = time.perf_counter()
        for attempt in range(MAX_RETRIES):
            try:
                resp = await self._client.get(url, **kwargs)
                elapsed = time.perf_counter() - t0
                if resp.status_code == 429 or resp.status_code >= 500:
                    wait = min(BACKOFF_BASE * (2**attempt), BACKOFF_CAP)
                    _log.debug(
                        "response status=%s attempt=%s/%s wait=%.1fs elapsed=%.2fs",
                        resp.status_code,
                        attempt + 1,
                        MAX_RETRIES,
                        wait,
                        elapsed,
                    )
                    if resp.status_code == 429:
                        HttpClient._base_delay_multiplier = min(
                            HttpClient._base_delay_multiplier * 2, 8.0
                        )
                    await asyncio.sleep(wait)
                    last_exc = httpx.HTTPStatusError(
                        f"HTTP {resp.status_code}",
                        request=resp.request,
                        response=resp,
                    )
                    continue
                resp.raise_for_status()
                _log.debug(
                    "response status=%s bytes=%s elapsed=%.2fs final_url=%s",
                    resp.status_code,
                    len(resp.content),
                    elapsed,
                    str(resp.url),
                )
                if _log.isEnabledFor(logging.DEBUG) and resp.text:
                    preview = resp.text[:400].replace("\n", " ")
                    _log.debug("body preview: %s%s", preview, "…" if len(resp.text) > 400 else "")
                return resp
            except httpx.HTTPStatusError:
                raise
            except httpx.HTTPError as e:
                _log.debug("HTTPError attempt=%s: %s", attempt + 1, e)
                last_exc = e
                wait = min(BACKOFF_BASE * (2**attempt), BACKOFF_CAP)
                await asyncio.sleep(wait)

        _log.debug("GET failed after %s attempts: %s", MAX_RETRIES, last_exc)
        raise last_exc  # type: ignore[misc]

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """POST with jitter delay, burst detection, and exponential backoff retry."""
        if not url.startswith("http"):
            url = self._base_url.rstrip("/") + "/" + url.lstrip("/")

        _log.debug(
            "POST %s content_type=%s",
            url,
            kwargs.get("headers", {}).get("Content-Type", "auto"),
        )

        await self._jitter_delay()

        last_exc = None
        t0 = time.perf_counter()
        for attempt in range(MAX_RETRIES):
            try:
                resp = await self._client.post(url, **kwargs)
                elapsed = time.perf_counter() - t0
                if resp.status_code == 429 or resp.status_code >= 500:
                    wait = min(BACKOFF_BASE * (2**attempt), BACKOFF_CAP)
                    _log.debug(
                        "response status=%s attempt=%s/%s wait=%.1fs elapsed=%.2fs",
                        resp.status_code,
                        attempt + 1,
                        MAX_RETRIES,
                        wait,
                        elapsed,
                    )
                    if resp.status_code == 429:
                        HttpClient._base_delay_multiplier = min(
                            HttpClient._base_delay_multiplier * 2, 8.0
                        )
                    await asyncio.sleep(wait)
                    last_exc = httpx.HTTPStatusError(
                        f"HTTP {resp.status_code}",
                        request=resp.request,
                        response=resp,
                    )
                    continue
                resp.raise_for_status()
                _log.debug(
                    "response status=%s bytes=%s elapsed=%.2fs",
                    resp.status_code,
                    len(resp.content),
                    elapsed,
                )
                if _log.isEnabledFor(logging.DEBUG) and resp.text:
                    preview = resp.text[:400].replace("\n", " ")
                    _log.debug("body preview: %s%s", preview, "…" if len(resp.text) > 400 else "")
                return resp
            except httpx.HTTPStatusError:
                raise
            except httpx.HTTPError as e:
                _log.debug("HTTPError attempt=%s: %s", attempt + 1, e)
                last_exc = e
                wait = min(BACKOFF_BASE * (2**attempt), BACKOFF_CAP)
                await asyncio.sleep(wait)

        _log.debug("POST failed after %s attempts: %s", MAX_RETRIES, last_exc)
        raise last_exc  # type: ignore[misc]

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
