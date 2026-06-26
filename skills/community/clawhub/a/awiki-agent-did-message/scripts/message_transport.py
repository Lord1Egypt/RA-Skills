"""Message transport selection and RPC helpers.

[INPUT]: settings.json, credential_store, SDKConfig, HTTP RPC helpers, local
         daemon, listener recovery helpers
[OUTPUT]: receive-mode helpers plus credential-aware message RPC call helpers
          over HTTP or the local WebSocket-mode daemon with automatic HTTP
          fallback for WebSocket transport failures
[POS]: Shared transport abstraction for message-domain scripts, centralizing whether
       message RPC traffic should use direct HTTP JSON-RPC or the localhost daemon
       that owns the single remote WebSocket connection.

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from credential_store import create_authenticator
from listener_recovery import ensure_listener_runtime, note_listener_healthy
from message_daemon import call_local_daemon, load_local_daemon_settings
from utils.client import create_molt_message_client
from utils.config import SDKConfig
from utils.rpc import authenticated_rpc_call

MESSAGE_RPC = "/message/rpc"
RECEIVE_MODE_HTTP = "http"
RECEIVE_MODE_WEBSOCKET = "websocket"
_VALID_RECEIVE_MODES = {RECEIVE_MODE_HTTP, RECEIVE_MODE_WEBSOCKET}
_WEBSOCKET_FALLBACK_ERROR_MARKERS = (
    "Local message daemon token is missing",
    "Local message daemon request timed out",
    "Local message daemon is unavailable",
    "Remote WebSocket transport is not connected",
    "WebSocket not connected",
    "WebSocket reader failed",
    "WebSocket reader stopped",
    "WebSocket closed",
)
logger = logging.getLogger(__name__)


def load_receive_mode(config: SDKConfig | None = None) -> str:
    """Load the configured message receive mode.

    Defaults to HTTP mode when no explicit config is present to keep the
    non-realtime CLI flow available in fresh environments.
    """
    resolved = config or SDKConfig.load()
    settings_path = resolved.data_dir / "config" / "settings.json"
    if not settings_path.exists():
        return RECEIVE_MODE_HTTP
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return RECEIVE_MODE_HTTP
    mode = (
        data.get("message_transport", {}).get("receive_mode")
        or data.get("receive_mode")
        or RECEIVE_MODE_HTTP
    )
    if mode not in _VALID_RECEIVE_MODES:
        return RECEIVE_MODE_HTTP
    return mode


def is_websocket_mode(config: SDKConfig | None = None) -> bool:
    """Return whether the message domain is configured to use WebSocket mode."""
    return load_receive_mode(config) == RECEIVE_MODE_WEBSOCKET


async def http_message_rpc_call(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    credential_name: str = "default",
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Call one message RPC method over HTTP JSON-RPC."""
    resolved = config or SDKConfig.load()
    auth_result = create_authenticator(credential_name, resolved)
    if auth_result is None:
        raise RuntimeError(
            f"Credential '{credential_name}' unavailable; please create an identity first"
        )
    auth, _ = auth_result
    async with create_molt_message_client(resolved) as client:
        return await authenticated_rpc_call(
            client,
            MESSAGE_RPC,
            method,
            params=params,
            auth=auth,
            credential_name=credential_name,
        )


async def websocket_message_rpc_call(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    credential_name: str = "default",
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Call one message RPC method via the local WebSocket-mode daemon."""
    resolved = config or SDKConfig.load()
    return await call_local_daemon(
        method,
        params,
        credential_name=credential_name,
        config=resolved,
    )


async def message_rpc_call(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    credential_name: str = "default",
    config: SDKConfig | None = None,
    force_mode: str | None = None,
) -> dict[str, Any]:
    """Call one message RPC method using the configured transport mode."""
    resolved = config or SDKConfig.load()
    mode = force_mode or load_receive_mode(resolved)
    if mode == RECEIVE_MODE_WEBSOCKET:
        try:
            result = await websocket_message_rpc_call(
                method,
                params,
                credential_name=credential_name,
                config=resolved,
            )
            note_listener_healthy(credential_name, config=resolved)
            return result
        except Exception as exc:  # noqa: BLE001
            if not _should_fallback_to_http(exc):
                raise
            logger.warning(
                "WebSocket message RPC unavailable, falling back to HTTP "
                "credential=%s method=%s error=%s",
                credential_name,
                method,
                exc,
            )
            try:
                ensure_listener_runtime(credential_name, config=resolved)
            except Exception:  # noqa: BLE001
                logger.debug("Failed to run listener recovery after WebSocket RPC error", exc_info=True)
            return await http_message_rpc_call(
                method,
                params,
                credential_name=credential_name,
                config=resolved,
            )
    return await http_message_rpc_call(
        method,
        params,
        credential_name=credential_name,
        config=resolved,
    )


def _should_fallback_to_http(exc: BaseException) -> bool:
    """Return whether one WebSocket RPC failure should fall back to HTTP."""
    message = str(exc)
    if not message:
        return False
    if message.startswith("JSON-RPC error"):
        return False
    return any(marker in message for marker in _WEBSOCKET_FALLBACK_ERROR_MARKERS)


def write_receive_mode(
    mode: str,
    *,
    config: SDKConfig | None = None,
    extra_transport_fields: dict[str, Any] | None = None,
) -> Path:
    """Persist one receive mode into settings.json."""
    if mode not in _VALID_RECEIVE_MODES:
        raise ValueError(f"Unsupported receive mode: {mode}")
    resolved = config or SDKConfig.load()
    settings_path = resolved.data_dir / "config" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}
    transport = data.get("message_transport", {})
    transport["receive_mode"] = mode
    if extra_transport_fields:
        transport.update(extra_transport_fields)
    data["message_transport"] = transport
    settings_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return settings_path


__all__ = [
    "MESSAGE_RPC",
    "RECEIVE_MODE_HTTP",
    "RECEIVE_MODE_WEBSOCKET",
    "http_message_rpc_call",
    "is_websocket_mode",
    "load_receive_mode",
    "message_rpc_call",
    "websocket_message_rpc_call",
    "write_receive_mode",
    "load_local_daemon_settings",
]
