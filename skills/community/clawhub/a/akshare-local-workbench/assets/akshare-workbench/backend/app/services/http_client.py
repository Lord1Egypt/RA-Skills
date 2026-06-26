from __future__ import annotations

import logging
import os
import random
import time
from typing import Callable
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

_PATCHED = False

_PROXY_MODE = os.environ.get("AKSHARE_PROXY_MODE", "auto").strip().lower()
_EASTMONEY_HTTP_RETRIES = int(os.environ.get("AKSHARE_EASTMONEY_HTTP_RETRIES", "2"))
_EASTMONEY_PAGE_DELAY_MIN = float(os.environ.get("AKSHARE_EASTMONEY_PAGE_DELAY_MIN", "6.0"))
_EASTMONEY_PAGE_DELAY_MAX = float(os.environ.get("AKSHARE_EASTMONEY_PAGE_DELAY_MAX", "10.0"))

_EASTMONEY_HOSTS = (
    "eastmoney.com",
    "push2.eastmoney.com",
    "push2his.eastmoney.com",
    "82.push2.eastmoney.com",
    "48.push2.eastmoney.com",
    "quote.eastmoney.com",
    "datacenter-web.eastmoney.com",
    "datacenter.eastmoney.com",
    "push2ex.eastmoney.com",
    "emweb.securities.eastmoney.com",
    "data.eastmoney.com",
    "pushhis.eastmoney.com",
)

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

_CURL_CFFI_AVAILABLE = False
try:
    from curl_cffi import requests as curl_requests
    _CURL_CFFI_AVAILABLE = True
except ImportError:
    curl_requests = None  # type: ignore[assignment]


def _is_transient_network_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(
        keyword in msg
        for keyword in (
            "connection aborted",
            "remote end closed",
            "remote disconnected",
            "forcibly closed",
            "connection reset",
            "connection refused",
            "proxyerror",
            "unable to connect to proxy",
            "max retries exceeded",
            "read timed out",
            "connect timeout",
        )
    )


def _is_eastmoney_url(url: str) -> bool:
    host = urlparse(url).hostname or ""
    return any(host == item or host.endswith("." + item) for item in _EASTMONEY_HOSTS)


def configure_session(session: requests.Session, *, use_proxy: bool | None = None) -> requests.Session:
    """Apply project-wide proxy rules to a requests session."""
    if use_proxy is None:
        use_proxy = _PROXY_MODE != "direct"
    session.trust_env = use_proxy
    session.headers.update(_BROWSER_HEADERS)
    if not use_proxy:
        session.proxies.update({"http": None, "https": None})
    return session


def _curl_cffi_get(
    url: str,
    params: dict | None,
    timeout: int,
) -> requests.Response:
    """Use curl_cffi with browser TLS fingerprint for eastmoney requests."""
    resp = curl_requests.get(
        url,
        params=params,
        timeout=timeout,
        impersonate="chrome131",
        headers={
            "Referer": "https://www.eastmoney.com/",
            "Origin": "https://www.eastmoney.com",
        },
    )
    resp.raise_for_status()
    wrapped = requests.Response()
    wrapped.status_code = resp.status_code
    wrapped._content = resp.content
    wrapped.headers.update(dict(resp.headers))
    wrapped.url = resp.url
    wrapped.encoding = resp.encoding or "utf-8"
    return wrapped


def _session_get(
    url: str,
    params: dict | None,
    timeout: int,
    *,
    use_proxy: bool,
) -> requests.Response:
    if _CURL_CFFI_AVAILABLE and _is_eastmoney_url(url):
        try:
            return _curl_cffi_get(url, params, timeout)
        except Exception as exc:
            if not _is_transient_network_error(exc):
                raise
            logger.warning("curl_cffi failed for eastmoney, falling back to requests: %s", exc)

    session = requests.Session()
    configure_session(session, use_proxy=use_proxy)
    if _is_eastmoney_url(url):
        session.headers.update({
            "Referer": "https://www.eastmoney.com/",
            "Origin": "https://www.eastmoney.com",
        })
    try:
        response = session.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response
    finally:
        session.close()


def request_with_retry(
    url: str,
    params: dict | None = None,
    timeout: int = 60,
    max_retries: int = 5,
    base_delay: float = 1.2,
    random_delay_range: tuple[float, float] = (0.8, 1.8),
) -> requests.Response:
    """Drop-in replacement for akshare.utils.request.request_with_retry."""
    last_exception: Exception | None = None
    is_eastmoney = _is_eastmoney_url(url)

    effective_retries = min(max_retries, _EASTMONEY_HTTP_RETRIES) if is_eastmoney else max_retries

    for attempt in range(effective_retries):
        proxy_attempts: list[bool]
        if _PROXY_MODE == "direct":
            proxy_attempts = [False]
        elif _PROXY_MODE == "system":
            proxy_attempts = [True]
        else:
            proxy_attempts = [True, False] if attempt >= 1 else [True]

        for use_proxy in proxy_attempts:
            try:
                return _session_get(url, params, timeout, use_proxy=use_proxy)
            except (requests.RequestException, ValueError) as exc:
                last_exception = exc
                if not _is_transient_network_error(exc):
                    raise
                mode = "proxy" if use_proxy else "direct"
                logger.warning(
                    "HTTP GET failed (%s, attempt %d/%d): %s",
                    mode,
                    attempt + 1,
                    effective_retries,
                    exc,
                )
                if _PROXY_MODE == "auto" and use_proxy and is_eastmoney:
                    continue
                break

        if attempt < effective_retries - 1:
            delay = base_delay * (2**attempt) + random.uniform(*random_delay_range)
            if last_exception and _is_transient_network_error(last_exception):
                delay *= 1.3
            if is_eastmoney:
                delay = max(delay, 3.0 + random.uniform(1.0, 2.5))
            time.sleep(delay)

    assert last_exception is not None
    raise last_exception


def patch_akshare_http() -> None:
    """Monkey-patch AKShare HTTP helpers once per process."""
    global _PATCHED
    if _PATCHED:
        return

    try:
        import akshare.utils.request as ak_request
        import akshare.utils.func as ak_func
    except ImportError:
        return

    ak_request.request_with_retry = request_with_retry  # type: ignore[assignment]

    def _stable_fetch_paginated_data(
        url: str,
        base_params: dict,
        timeout: int = 60,
    ):
        import math

        import pandas as pd

        params = base_params.copy()
        first = request_with_retry(url, params=params, timeout=timeout)
        data_json = first.json()
        per_page_num = len(data_json["data"]["diff"])
        total_page = math.ceil(data_json["data"]["total"] / per_page_num) if per_page_num else 1

        frames = [pd.DataFrame(data_json["data"]["diff"])]
        for page in range(2, total_page + 1):
            params["pn"] = page
            if _is_eastmoney_url(url):
                time.sleep(random.uniform(_EASTMONEY_PAGE_DELAY_MIN, _EASTMONEY_PAGE_DELAY_MAX))
            else:
                time.sleep(random.uniform(2.0, 4.0))
            resp = request_with_retry(url, params=params, timeout=timeout)
            frames.append(pd.DataFrame(resp.json()["data"]["diff"]))

        temp_df = pd.concat(frames, ignore_index=True)
        temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
        temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
        temp_df.reset_index(inplace=True)
        temp_df["index"] = temp_df["index"].astype(int) + 1
        return temp_df

    ak_func.fetch_paginated_data = _stable_fetch_paginated_data
    _PATCHED = True
    logger.info(
        "Patched AKShare HTTP client (proxy_mode=%s, curl_cffi=%s)",
        _PROXY_MODE,
        _CURL_CFFI_AVAILABLE,
    )


def with_rate_limit(source: str, fn: Callable[[], object]):
    """Run *fn* while holding the shared AKShare rate limiter."""
    from app.services.rate_limiter import rate_limiter

    rate_limiter.acquire(source)
    try:
        return fn()
    finally:
        rate_limiter.release()
