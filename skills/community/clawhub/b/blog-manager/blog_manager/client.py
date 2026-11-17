"""HTTP client layer for the Blog System API v1.0.0.

All network communication goes through ``BlogClient`` so that command
modules stay thin. The API requires no authentication. Endpoints live
under ``/api`` (except ``/health`` which is at the root path).

The base URL is resolved **exclusively** from the ``BLOG_MANAGER_BASE_URL``
environment variable (or an explicit constructor argument for testing).
It is never hard-coded, never read from any config file, and never
falls back to any default. If the variable is unset or invalid a
``BlogConfigError`` is raised and the CLI exits with code 2.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

#: Environment variable that must contain the API base URL.
BASE_URL_ENV = "BLOG_MANAGER_BASE_URL"

#: Default request timeout in seconds.
DEFAULT_TIMEOUT = 30


class BlogConfigError(Exception):
    """Raised when ``BLOG_MANAGER_BASE_URL`` is missing or invalid."""


class BlogAPIError(Exception):
    """Raised when the API responds with an HTTP error (status >= 400)."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class BlogClient:
    """Reusable HTTP client for Blog System API v1.0.0.

    Usage::

        client = BlogClient()                 # reads env var
        client = BlogClient(base_url="...")   # explicit (testing)
        data = client.get("/api/articles")
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = self._resolve_base_url(base_url)
        self.session = session if session is not None else requests.Session()
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_base_url(base_url: Optional[str]) -> str:
        """Return a validated base URL from env or constructor arg."""
        raw = (base_url if base_url else os.environ.get(BASE_URL_ENV, "")).strip()
        url = raw.rstrip("/")
        if not url:
            raise BlogConfigError(
                f"{BASE_URL_ENV} is not set. "
                f"Export it first, e.g. export {BASE_URL_ENV}=http://host:port"
            )
        if not (url.startswith("http://") or url.startswith("https://")):
            raise BlogConfigError(
                f"{BASE_URL_ENV} must start with http:// or https:// (got {url!r})"
            )
        return url

    # ------------------------------------------------------------------
    # Generic request
    # ------------------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        resp = self.session.request(
            method,
            url,
            params=params,
            json=json,
            files=files,
            timeout=self.timeout,
        )
        try:
            body: Any = resp.json()
        except ValueError:
            body = {"raw": resp.text}
        if resp.status_code >= 400:
            if isinstance(body, dict):
                detail = body.get("detail") or body.get("message") or str(body)
            else:
                detail = str(body)
            raise BlogAPIError(resp.status_code, detail)
        return body

    # ------------------------------------------------------------------
    # Convenience verbs
    # ------------------------------------------------------------------

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
    ) -> Any:
        return self._request("POST", path, json=json, files=files)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PUT", path, json=json)

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("DELETE", path, params=params)
