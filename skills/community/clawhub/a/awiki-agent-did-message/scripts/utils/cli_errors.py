"""Helpers for concise CLI error rendering.

[INPUT]: Exceptions raised by CLI entry points, logger instances, and
         user-facing validation messages
[OUTPUT]: format_cli_error(), exit_with_cli_error()
[POS]: Shared CLI helper that keeps terminal error output brief while
       preserving detailed traces in log files

[PROTOCOL]:
1. Update this header when logic changes
2. Check the containing folder's CLAUDE.md after updates
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Mapping
from typing import Any, NoReturn

import httpx

from utils.rpc import JsonRpcError

_MAX_ERROR_LENGTH = 240


def _normalize_message(message: str) -> str:
    """Collapse whitespace and trim overly long messages."""
    normalized = " ".join(message.split()).strip()
    if len(normalized) <= _MAX_ERROR_LENGTH:
        return normalized
    return f"{normalized[: _MAX_ERROR_LENGTH - 1].rstrip()}…"


def _extract_message(payload: Any) -> str | None:
    """Best-effort extraction of a human-readable message from a payload."""
    if isinstance(payload, str):
        return payload.strip() or None
    if not isinstance(payload, Mapping):
        return None

    for key in ("message", "detail", "error", "reason", "msg"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        nested = _extract_message(value)
        if nested:
            return nested

    for value in payload.values():
        nested = _extract_message(value)
        if nested:
            return nested
    return None


def _format_http_status_error(exc: httpx.HTTPStatusError) -> str:
    """Return a compact message for an HTTP status error."""
    response = exc.response
    if response is None:
        return _normalize_message(str(exc)) or "HTTP request failed"

    detail: str | None = None
    try:
        detail = _extract_message(response.json())
    except ValueError:
        text = response.text.strip()
        if text:
            detail = text

    if detail:
        return _normalize_message(detail)
    return f"HTTP {response.status_code}"


def format_cli_error(exc: BaseException) -> str:
    """Format an exception into a short CLI-friendly error message."""
    if isinstance(exc, JsonRpcError):
        return _normalize_message(exc.message) or "Request failed"
    if isinstance(exc, httpx.HTTPStatusError):
        return _format_http_status_error(exc)
    if isinstance(exc, httpx.RequestError):
        return _normalize_message(str(exc)) or "Network request failed"

    message = _normalize_message(str(exc))
    if message:
        return message
    return exc.__class__.__name__


def exit_with_cli_error(
    *,
    exc: BaseException,
    logger: logging.Logger,
    context: str,
    exit_code: int = 1,
    log_traceback: bool = True,
) -> NoReturn:
    """Log an exception and exit after printing a concise terminal message."""
    message = format_cli_error(exc)
    if log_traceback:
        logger.exception("%s: %s", context, message)
    else:
        logger.warning("%s: %s", context, message)

    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(exit_code) from exc
