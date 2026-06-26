"""
Drop-in replacement for httpx.AsyncClient using curl_cffi to bypass Cloudflare.

Provides the subset of httpx.AsyncClient API that twikit actually uses:
- request(method, url, headers=, json=, data=, params=, content=, **kwargs)
- cookies (get/set/clear/update/iterate/jar)
- stream(method, url, ...) context manager (for media downloads)

All requests use curl_cffi's Chrome TLS impersonation to avoid Cloudflare 403.
"""

from __future__ import annotations

import json as _json
import logging
from contextlib import asynccontextmanager
from http.cookiejar import CookieJar
from typing import Any, AsyncIterator

from curl_cffi.requests import AsyncSession, Response as CurlResponse, Cookies as CurlCookies

log = logging.getLogger("curl_httpx_shim")


class _CookieJarAdapter:
    """Makes curl_cffi's cookies look like httpx's Cookies to twikit."""

    def __init__(self, session: AsyncSession):
        self._session = session

    # ---------- iteration / dict-like ----------
    def __iter__(self):
        for name, value in self._session.cookies.items():
            yield name

    def items(self):
        return list(self._session.cookies.items())

    def __len__(self):
        return len(self._session.cookies)

    # ---------- twikit calls dict(self.http.cookies) ----------
    def keys(self):
        return [name for name, _ in self._session.cookies.items()]

    def values(self):
        return [value for _, value in self._session.cookies.items()]

    def __getitem__(self, name: str):
        return self._session.cookies.get(name)

    # ---------- twikit uses .get(name) ----------
    def get(self, name: str, default=None):
        val = self._session.cookies.get(name)
        return val if val is not None else default

    # ---------- twikit calls .clear() ----------
    def clear(self):
        self._session.cookies.clear()

    # ---------- twikit calls .update(dict) ----------
    def update(self, other):
        if isinstance(other, dict):
            for k, v in other.items():
                self._session.cookies.set(k, v, domain=".x.com")
        elif hasattr(other, 'items'):
            for k, v in other.items():
                self._session.cookies.set(k, v, domain=".x.com")

    # ---------- jar property — twikit iterates .jar for cookie objects ----------
    @property
    def jar(self):
        """Return lightweight cookie-like objects with .name and .value."""
        return [
            _SimpleCookie(name, value)
            for name, value in self._session.cookies.items()
        ]


class _SimpleCookie:
    """Minimal cookie object with .name and .value for twikit iteration."""
    __slots__ = ('name', 'value')

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class _StreamResponse:
    """Wraps a curl_cffi response to provide httpx-like stream interface."""

    def __init__(self, response: CurlResponse):
        self._response = response

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def headers(self):
        return self._response.headers

    async def aiter_bytes(self, chunk_size: int = 4096) -> AsyncIterator[bytes]:
        content = self._response.content
        for i in range(0, len(content), chunk_size):
            yield content[i:i + chunk_size]

    async def aread(self) -> bytes:
        return self._response.content

    async def aclose(self):
        pass


class CurlAsyncClient:
    """
    Drop-in replacement for httpx.AsyncClient that uses curl_cffi
    with Chrome TLS impersonation.
    """

    def __init__(self, proxy: str | None = None, **kwargs):
        self._impersonate = kwargs.pop("impersonate", "chrome")
        # Filter out kwargs that curl_cffi doesn't understand
        self._session = AsyncSession(
            impersonate=self._impersonate,
            proxy=proxy,
        )
        self._cookies = _CookieJarAdapter(self._session)
        # _mounts stub for twikit proxy property access
        self._mounts = {}
        log.info("CurlAsyncClient initialized (impersonate=%s)", self._impersonate)

    # ---------- cookies property ----------
    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        """twikit assigns self.http.cookies = list(cookies.items())"""
        self._session.cookies.clear()
        if isinstance(value, list):
            for name, val in value:
                self._session.cookies.set(name, val, domain=".x.com")
        elif isinstance(value, dict):
            for name, val in value.items():
                self._session.cookies.set(name, val, domain=".x.com")

    def _dedup_cookies(self):
        """Merge dupes: keep .x.com, copy unique .twitter.com to .x.com, remove .twitter.com."""
        try:
            jar = self._session.cookies.jar
            xcom = {}
            twitter = {}
            for cookie in jar:
                d = getattr(cookie, 'domain', '')
                if '.x.com' in d:
                    xcom[cookie.name] = cookie.value
                elif '.twitter.com' in d:
                    twitter[cookie.name] = cookie.value
            if not twitter:
                return
            for name, val in twitter.items():
                if name not in xcom:
                    self._session.cookies.set(name, val, domain=".x.com")
            for name in list(twitter.keys()):
                try:
                    jar.clear(".twitter.com", "/", name)
                except KeyError:
                    pass
        except Exception:
            pass

    # ---------- request ----------
    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict | None = None,
        json: Any = None,
        data: Any = None,
        params: dict | None = None,
        content: bytes | None = None,
        timeout: float | None = None,
        **kwargs
    ) -> CurlResponse:
        self._dedup_cookies()
        kw: dict[str, Any] = {
            "headers": headers or {},
            "params": params,
            "timeout": timeout if timeout is not None else 30,
        }
        if json is not None:
            kw["json"] = json
        if data is not None:
            kw["data"] = data
        if content is not None:
            kw["content"] = content

        resp = await self._session.request(method, url, **kw)
        self._dedup_cookies()
        return resp

    async def get(self, url: str, **kwargs) -> CurlResponse:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> CurlResponse:
        return await self.request("POST", url, **kwargs)

    # ---------- stream context manager ----------
    @asynccontextmanager
    async def stream(self, method: str, url: str, **kwargs):
        """Provide httpx-like streaming interface (used for media downloads)."""
        resp = await self.request(method, url, **kwargs)
        try:
            yield _StreamResponse(resp)
        finally:
            pass

    # ---------- lifecycle ----------
    async def aclose(self):
        await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.aclose()
