"""CyberLens API client for cloud-powered scanning."""

import asyncio
import os
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import httpx


DEFAULT_API_BASE = "https://api.cyberlensai.com/functions/v1/public-api-scan"


class CyberLensQuotaExceededError(RuntimeError):
    """Raised when the CyberLens public API reports exhausted scan quota."""

    def __init__(
        self,
        message: str,
        *,
        upgrade_url: Optional[str] = None,
        quota_type: Optional[str] = None,
        used: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> None:
        super().__init__(message)
        self.upgrade_url = upgrade_url
        self.quota_type = quota_type
        self.used = used
        self.limit = limit


def _resolve_api_base(api_base: Optional[str] = None) -> str:
    """Resolve and validate the CyberLens API base URL."""
    candidate = (api_base or os.environ.get("CYBERLENS_API_BASE_URL") or DEFAULT_API_BASE).strip()
    parsed = urlparse(candidate)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("CyberLens API base URL must be a valid https:// URL.")
    return candidate.rstrip("/")


class CyberLensAPIClient:
    """Async client for the CyberLens public scan API."""

    def __init__(self, api_key: str, timeout: float = 120.0, api_base: Optional[str] = None):
        self.api_key = api_key
        self.timeout = timeout
        self.api_base = _resolve_api_base(api_base)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
            },
        )
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    @staticmethod
    def _parse_error_payload(response: httpx.Response) -> Dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            payload = {}
        return payload if isinstance(payload, dict) else {}

    def _read_response_data(self, response: httpx.Response) -> Dict[str, Any]:
        payload = self._parse_error_payload(response)

        if response.status_code >= 400:
            error = payload.get("error")
            if isinstance(error, dict):
                message = error.get("message") or f"CyberLens API error ({response.status_code})"
                if response.status_code == 402 and error.get("code") == "QUOTA_EXCEEDED":
                    raise CyberLensQuotaExceededError(
                        message,
                        upgrade_url=error.get("upgrade_url"),
                        quota_type=error.get("quota_type"),
                        used=error.get("used"),
                        limit=error.get("limit"),
                    )
                raise RuntimeError(message)

            if isinstance(error, str):
                raise RuntimeError(error)

            response.raise_for_status()

        data = payload.get("data")
        if not isinstance(data, dict):
            raise RuntimeError("CyberLens API response did not include a data object.")
        return data

    async def start_scan(self, url: str) -> str:
        """Start a scan and return the scan ID."""
        response = await self._client.post(
            f"{self.api_base}/scan",
            json={"url": url},
        )
        data = self._read_response_data(response)
        return data["scan_id"]

    async def poll_scan(self, scan_id: str) -> Dict[str, Any]:
        """Poll for scan results with exponential backoff."""
        delay = 1.0
        max_delay = 30.0
        elapsed = 0.0

        while elapsed < self.timeout:
            await asyncio.sleep(delay)
            elapsed += delay

            response = await self._client.get(f"{self.api_base}/scan/{scan_id}")
            data = self._read_response_data(response)

            if data["status"] == "completed":
                return data
            if data["status"] == "failed":
                raise RuntimeError("Scan failed on the server.")

            delay = min(delay * 2, max_delay)

        raise TimeoutError("Scan timed out waiting for results.")

    async def scan(self, url: str) -> Dict[str, Any]:
        """Start a scan and wait for results."""
        scan_id = await self.start_scan(url)
        return await self.poll_scan(scan_id)

    async def get_quota(self) -> Dict[str, Any]:
        """Get current usage quota."""
        response = await self._client.get(f"{self.api_base}/quota")
        return self._read_response_data(response)
