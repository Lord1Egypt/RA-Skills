"""Health check — 1 API operation.

Endpoint:
  GET /health   health_check
"""

from __future__ import annotations

from typing import Any, Tuple

from .client import BlogClient


def health_check(client: BlogClient) -> Tuple[Any, str]:
    return client.get("/health"), "health"
