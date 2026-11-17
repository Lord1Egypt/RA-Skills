"""External metadata providers used by Zotero enrichment."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Mapping
from typing import Any
from urllib.parse import quote

import httpx


class ProviderError(RuntimeError):
    """Raised when an external metadata provider cannot satisfy a request."""


class _JSONProvider:
    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        user_agent: str,
        max_retries: int = 2,
        min_interval_seconds: float = 0.0,
    ) -> None:
        self.client = client
        self.user_agent = user_agent
        self.max_retries = max_retries
        self.min_interval_seconds = max(0.0, min_interval_seconds)
        self._request_lock = asyncio.Lock()
        self._last_request_at = 0.0

    async def _get_json(
        self,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                if self.min_interval_seconds:
                    async with self._request_lock:
                        remaining = self.min_interval_seconds - (
                            time.monotonic() - self._last_request_at
                        )
                        if remaining > 0:
                            await asyncio.sleep(remaining)
                        response = await self.client.get(
                            url,
                            params=dict(params or {}),
                            headers={
                                "User-Agent": self.user_agent,
                                "Accept": "application/json",
                            },
                        )
                        self._last_request_at = time.monotonic()
                else:
                    response = await self.client.get(
                        url,
                        params=dict(params or {}),
                        headers={
                            "User-Agent": self.user_agent,
                            "Accept": "application/json",
                        },
                    )
                if response.status_code == 404:
                    return {}
                if (
                    response.status_code == 429 or response.status_code >= 500
                ) and attempt < self.max_retries:
                    retry_after = response.headers.get("Retry-After")
                    try:
                        delay = (
                            float(retry_after) if retry_after else 0.5 * (2**attempt)
                        )
                    except ValueError:
                        delay = 0.5 * (2**attempt)
                    await asyncio.sleep(min(delay, 5.0))
                    continue
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    raise ProviderError(f"Expected an object response from {url}")
                return payload
            except (httpx.HTTPError, ValueError, ProviderError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                    continue
        raise ProviderError(f"Request failed for {url}: {last_error}") from last_error


class CrossrefProvider(_JSONProvider):
    """Resolve and search publisher DOI metadata through Crossref."""

    base_url = "https://api.crossref.org"

    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        mailto: str = "",
        user_agent: str = "llm-wiki/1.5.2",
    ) -> None:
        super().__init__(client, user_agent=user_agent, min_interval_seconds=0.25)
        self.mailto = mailto.strip()

    def _params(self, values: Mapping[str, Any] | None = None) -> dict[str, Any]:
        params = dict(values or {})
        if self.mailto:
            params["mailto"] = self.mailto
        return params

    async def get_work(self, doi: str) -> dict[str, Any]:
        payload = await self._get_json(
            f"{self.base_url}/works/{quote(doi, safe='')}",
            params=self._params(),
        )
        message = payload.get("message")
        return dict(message) if isinstance(message, Mapping) else {}

    async def search_works(
        self,
        title: str,
        *,
        author: str = "",
        rows: int = 5,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "query.bibliographic": title,
            "rows": max(1, min(rows, 10)),
        }
        if author:
            params["query.author"] = author
        payload = await self._get_json(
            f"{self.base_url}/works",
            params=self._params(params),
        )
        message = payload.get("message")
        items = message.get("items") if isinstance(message, Mapping) else None
        return [dict(item) for item in items or [] if isinstance(item, Mapping)]


class OpenAlexProvider(_JSONProvider):
    """Fetch citation counts and open journal metrics from OpenAlex."""

    base_url = "https://api.openalex.org"

    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        api_key: str = "",
        mailto: str = "",
        user_agent: str = "llm-wiki/1.5.2",
    ) -> None:
        super().__init__(client, user_agent=user_agent)
        self.api_key = api_key.strip()
        self.mailto = mailto.strip()

    def _params(self, values: Mapping[str, Any] | None = None) -> dict[str, Any]:
        params = dict(values or {})
        if self.api_key:
            params["api_key"] = self.api_key
        if self.mailto:
            params["mailto"] = self.mailto
        return params

    async def get_work_by_doi(self, doi: str) -> dict[str, Any]:
        identifier = quote(f"https://doi.org/{doi}", safe="")
        return await self._get_json(
            f"{self.base_url}/works/{identifier}",
            params=self._params(),
        )

    async def search_works(
        self, title: str, *, per_page: int = 5
    ) -> list[dict[str, Any]]:
        payload = await self._get_json(
            f"{self.base_url}/works",
            params=self._params(
                {"search": title, "per-page": max(1, min(per_page, 10))}
            ),
        )
        results = payload.get("results")
        return [dict(item) for item in results or [] if isinstance(item, Mapping)]

    async def get_source(self, source_id: str) -> dict[str, Any]:
        identifier = source_id.rsplit("/", 1)[-1]
        return await self._get_json(
            f"{self.base_url}/sources/{quote(identifier, safe='')}",
            params=self._params(),
        )
