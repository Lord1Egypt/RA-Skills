"""Shared errors, credentials, and config for the adidas Click skill.

adidas Click is a **B2B ordering portal** with no public API, so this skill's
only surface is the browser (Playwright). This module holds the pieces that do
not depend on captured HTML: the error hierarchy (mirrored on the SanMar skill
so the CLI layer can map exceptions to a stable JSON error model) and the
portal credentials / base URL.

Credentials are never hardcoded. They come from the ``ADIDAS_CLICK_*``
environment variables or inline in a tool's stdin JSON.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Default base URL for the adidas Click B2B portal. Override with
# ADIDAS_CLICK_BASE_URL (or inline `base_url`) for a region-specific host.
DEFAULT_BASE_URL = "https://b2bportal.adidas-group.com"


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class AdidasError(Exception):
    """Base class for adidas Click skill errors."""

    surface = "adidas_click"
    operation = ""
    retryable = False

    def to_dict(self) -> dict[str, object]:
        return {
            "status": "error",
            "surface": self.surface,
            "operation": self.operation,
            "message": str(self),
            "retryable": self.retryable,
        }


class AdidasConfigError(AdidasError):
    """Missing or invalid configuration (credentials, base URL)."""


class AdidasTransportError(AdidasError):
    """Network / browser-launch / navigation failure."""

    retryable = True


class AdidasAPIError(AdidasError):
    """The portal rejected an action or a page did not match expectations."""


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdidasClickCredentials:
    """Login for the adidas Click B2B portal (browser surface)."""

    username: str
    password: str
    base_url: str = DEFAULT_BASE_URL


def credentials_from_env() -> AdidasClickCredentials:
    """Load portal credentials from ``ADIDAS_CLICK_*`` env vars.

    Raises :class:`AdidasConfigError` (the agent's cue to ask the user) when
    username or password is missing.
    """

    username = os.getenv("ADIDAS_CLICK_USERNAME", "").strip()
    password = os.getenv("ADIDAS_CLICK_PASSWORD", "").strip()
    base_url = os.getenv("ADIDAS_CLICK_BASE_URL", "").strip() or DEFAULT_BASE_URL

    missing = [
        name
        for name, value in (
            ("adidas_click_username", username),
            ("adidas_click_password", password),
        )
        if not value
    ]
    if missing:
        raise AdidasConfigError(
            "adidas Click credentials were not provided. Ask the user for "
            + ", ".join(missing)
            + " and supply them via ADIDAS_CLICK_USERNAME / "
            "ADIDAS_CLICK_PASSWORD, or as username / password in the tool's "
            "stdin JSON."
        )
    return AdidasClickCredentials(
        username=username, password=password, base_url=base_url
    )
