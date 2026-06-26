"""httpx AsyncClient factory.

[INPUT]: SDKConfig
[OUTPUT]: create_user_service_client(), create_molt_message_client()
[POS]: Provides pre-configured HTTP clients

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

import os
import ssl
from pathlib import Path
from urllib.parse import urlparse

import httpx

from utils.config import SDKConfig


def _resolve_verify(base_url: str) -> bool | ssl.SSLContext:
    """Resolve TLS verification settings for the given service URL.

    Priority:
      1. AWIKI_CA_BUNDLE / E2E_CA_BUNDLE environment variable
      2. Auto-detect mkcert root CA for local *.test domains on macOS
      3. Default system/Certifi verification
    """
    for env_name in ("AWIKI_CA_BUNDLE", "E2E_CA_BUNDLE", "SSL_CERT_FILE"):
        candidate = os.environ.get(env_name, "").strip()
        if candidate and Path(candidate).is_file():
            return ssl.create_default_context(cafile=candidate)

    host = (urlparse(base_url).hostname or "").lower()
    if host.endswith(".test") or host == "localhost":
        mkcert_root = (
            Path.home()
            / "Library"
            / "Application Support"
            / "mkcert"
            / "rootCA.pem"
        )
        if mkcert_root.is_file():
            return ssl.create_default_context(cafile=str(mkcert_root))

    return True


def create_user_service_client(config: SDKConfig) -> httpx.AsyncClient:
    """Create an async HTTP client for user-service."""
    return httpx.AsyncClient(
        base_url=config.user_service_url,
        timeout=30.0,
        trust_env=False,
        verify=_resolve_verify(config.user_service_url),
    )


def create_molt_message_client(config: SDKConfig) -> httpx.AsyncClient:
    """Create an async HTTP client for molt-message."""
    return httpx.AsyncClient(
        base_url=config.molt_message_url,
        timeout=30.0,
        trust_env=False,
        verify=_resolve_verify(config.molt_message_url),
    )


__all__ = ["create_molt_message_client", "create_user_service_client"]
