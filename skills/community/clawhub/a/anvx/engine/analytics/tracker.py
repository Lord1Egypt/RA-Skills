"""Anonymised event tracker — fire-and-forget pings to analytics endpoint.

SECURITY: Event metadata must NEVER contain financial amounts, balances,
API keys, wallet addresses, or any PII. Only structural information
(counts, category names, event types) is permitted.
"""
import asyncio
import logging
import os
import uuid
from datetime import datetime
from typing import Any

import httpx

from engine.analytics.local_log import LocalEventLog

logger = logging.getLogger(__name__)

# Keys that must NEVER appear in metadata
_FORBIDDEN_KEYS = frozenset({
    "amount", "balance", "total", "spend", "revenue", "cost", "price",
    "api_key", "api_secret", "secret", "token", "password", "credential",
    "wallet", "address", "wallet_address",
    "email", "name", "phone", "ssn", "ip", "ip_address",
})


class EventTracker:
    """Non-blocking, anonymised analytics event tracker.

    When ANALYTICS_ENABLED=true and an ANALYTICS_ENDPOINT is configured,
    events are POSTed as JSON. Otherwise (or on failure), events are
    logged locally to a JSONL file.

    Events never delay the caller — sends are fire-and-forget.
    """

    def __init__(
        self,
        local_log: LocalEventLog | None = None,
    ) -> None:
        self._session_id = str(uuid.uuid4())
        self._local_log = local_log or LocalEventLog()
        self._client: httpx.AsyncClient | None = None
        self._pending_tasks: set[asyncio.Task[None]] = set()

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def analytics_enabled(self) -> bool:
        return os.getenv("ANALYTICS_ENABLED", "false").lower() == "true"

    @property
    def endpoint(self) -> str:
        return os.getenv("ANALYTICS_ENDPOINT", "")

    def track(
        self,
        event_type: str,
        event_category: str,
        surface: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record an analytics event (non-blocking).

        Args:
            event_type: e.g. "connector_sync", "anomaly_detected", "recommendation_viewed"
            event_category: e.g. "connector", "intelligence", "ui"
            surface: "openclaw" or "mcp"
            metadata: Structural info only — NEVER amounts, keys, or PII.
        """
        safe_metadata = _sanitise_metadata(metadata or {})

        event = {
            "event_type": event_type,
            "event_category": event_category,
            "surface": surface,
            "session_id": self._session_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": safe_metadata,
        }

        if self.analytics_enabled and self.endpoint:
            # Fire-and-forget async send
            try:
                loop = asyncio.get_running_loop()
                task = loop.create_task(self._send_remote(event))
                self._pending_tasks.add(task)
                task.add_done_callback(self._pending_tasks.discard)
            except RuntimeError:
                # No running loop — fall back to local
                self._local_log.write(event)
        else:
            self._local_log.write(event)

    async def _send_remote(self, event: dict[str, Any]) -> None:
        """POST event to analytics endpoint. Falls back to local log on failure."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=3.0)

        try:
            resp = await self._client.post(self.endpoint, json=event)
            resp.raise_for_status()
        except (httpx.HTTPError, httpx.TimeoutException) as exc:
            logger.debug("Analytics send failed (%s) — logging locally", exc)
            self._local_log.write(event)

    async def flush(self) -> None:
        """Wait for all pending sends to complete (for graceful shutdown)."""
        if self._pending_tasks:
            await asyncio.gather(*self._pending_tasks, return_exceptions=True)
            self._pending_tasks.clear()

    async def close(self) -> None:
        """Flush pending events and close the HTTP client."""
        await self.flush()
        if self._client is not None:
            await self._client.aclose()
            self._client = None


def _sanitise_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Strip any forbidden keys from metadata to prevent data leakage."""
    sanitised: dict[str, Any] = {}
    for key, value in metadata.items():
        key_lower = key.lower()
        if key_lower in _FORBIDDEN_KEYS:
            logger.warning("Stripped forbidden metadata key: %s", key)
            continue
        if isinstance(value, dict):
            value = _sanitise_metadata(value)
        sanitised[key] = value
    return sanitised
