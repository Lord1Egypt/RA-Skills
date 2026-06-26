"""Local message transport daemon over localhost TCP.

[INPUT]: asyncio stream server/client, settings.json transport config, one async
         message RPC handler callable, optional local availability probes
[OUTPUT]: LocalMessageDaemon server plus helpers for CLI tools to call or probe
          the localhost daemon with caller credential context
[POS]: Local transport layer for WebSocket receive mode, ensuring all message CLI
       traffic goes through one local daemon that owns the single remote WSS link.

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from utils.config import SDKConfig

DEFAULT_LOCAL_DAEMON_HOST = "127.0.0.1"
DEFAULT_LOCAL_DAEMON_PORT = 18790
_REQUEST_TIMEOUT_SECONDS = 20.0


@dataclass(frozen=True, slots=True)
class LocalDaemonSettings:
    """Resolved local daemon connection settings."""

    host: str = DEFAULT_LOCAL_DAEMON_HOST
    port: int = DEFAULT_LOCAL_DAEMON_PORT
    token: str = ""


def load_local_daemon_settings(
    config: SDKConfig | None = None,
) -> LocalDaemonSettings:
    """Load local daemon settings from settings.json."""
    resolved = config or SDKConfig.load()
    settings_path = resolved.data_dir / "config" / "settings.json"
    data: dict[str, Any] = {}
    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    transport = data.get("message_transport", {})
    host = transport.get("local_daemon_host", DEFAULT_LOCAL_DAEMON_HOST)
    port_raw = transport.get("local_daemon_port", DEFAULT_LOCAL_DAEMON_PORT)
    token = transport.get("local_daemon_token", "")
    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        port = DEFAULT_LOCAL_DAEMON_PORT
    if not isinstance(host, str) or not host:
        host = DEFAULT_LOCAL_DAEMON_HOST
    if not isinstance(token, str):
        token = ""
    return LocalDaemonSettings(host=host, port=port, token=token)


async def call_local_daemon(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    credential_name: str = "default",
    config: SDKConfig | None = None,
    timeout: float = _REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Call one local daemon RPC method and return its result."""
    settings = load_local_daemon_settings(config)
    if not settings.token:
        raise RuntimeError(
            "Local message daemon token is missing; run `python scripts/setup_realtime.py --receive-mode websocket` first"
        )

    async def _round_trip() -> dict[str, Any]:
        reader, writer = await asyncio.open_connection(settings.host, settings.port)
        try:
            payload = {
                "token": settings.token,
                "method": method,
                "params": params or {},
                "credential_name": credential_name,
            }
            writer.write((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))
            await writer.drain()
            line = await reader.readline()
            if not line:
                raise RuntimeError("Local message daemon closed the connection unexpectedly")
            response = json.loads(line.decode("utf-8"))
            if not response.get("ok", False):
                error = response.get("error", {})
                raise RuntimeError(str(error.get("message") or "Local message daemon request failed"))
            result = response.get("result", {})
            return result if isinstance(result, dict) else {"result": result}
        finally:
            writer.close()
            await writer.wait_closed()

    try:
        return await asyncio.wait_for(_round_trip(), timeout=timeout)
    except asyncio.TimeoutError as exc:
        raise RuntimeError(
            "Local message daemon request timed out while waiting for a credential WebSocket session"
        ) from exc
    except OSError as exc:
        raise RuntimeError(
            "Local message daemon is unavailable; make sure `ws_listener` is running in websocket mode"
        ) from exc


def is_local_daemon_available(
    *,
    config: SDKConfig | None = None,
    timeout: float = 0.2,
) -> bool:
    """Return whether the localhost message daemon TCP port is reachable."""
    settings = load_local_daemon_settings(config)
    try:
        with socket.create_connection(
            (settings.host, settings.port),
            timeout=timeout,
        ):
            return True
    except OSError:
        return False


class LocalMessageDaemon:
    """Local TCP daemon that proxies message RPC calls to one async handler."""

    def __init__(
        self,
        settings: LocalDaemonSettings,
        handler: Callable[[str, dict[str, Any], str], Awaitable[dict[str, Any]]],
    ) -> None:
        self._settings = settings
        self._handler = handler
        self._server: asyncio.AbstractServer | None = None

    async def start(self) -> None:
        """Start the local daemon server."""
        self._server = await asyncio.start_server(
            self._handle_client,
            host=self._settings.host,
            port=self._settings.port,
            reuse_address=True,
        )

    async def close(self) -> None:
        """Stop the local daemon server."""
        if self._server is None:
            return
        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """Handle one single-request local daemon connection."""
        try:
            line = await asyncio.wait_for(reader.readline(), timeout=_REQUEST_TIMEOUT_SECONDS)
            if not line:
                return
            try:
                request = json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                await self._write_response(
                    writer,
                    ok=False,
                    error={"message": "Invalid local daemon JSON request"},
                )
                return

            if request.get("token") != self._settings.token:
                await self._write_response(
                    writer,
                    ok=False,
                    error={"message": "Unauthorized local daemon request"},
                )
                return

            method = request.get("method")
            params = request.get("params", {})
            credential_name = request.get("credential_name", "default")
            if not isinstance(method, str) or not method:
                await self._write_response(
                    writer,
                    ok=False,
                    error={"message": "Local daemon request missing method"},
                )
                return
            if not isinstance(params, dict):
                await self._write_response(
                    writer,
                    ok=False,
                    error={"message": "Local daemon params must be an object"},
                )
                return
            if not isinstance(credential_name, str) or not credential_name:
                credential_name = "default"

            result = await self._handler(method, params, credential_name)
            await self._write_response(writer, ok=True, result=result)
        except Exception as exc:  # noqa: BLE001
            await self._write_response(
                writer,
                ok=False,
                error={"message": str(exc)},
            )
        finally:
            writer.close()
            await writer.wait_closed()

    @staticmethod
    async def _write_response(
        writer: asyncio.StreamWriter,
        *,
        ok: bool,
        result: dict[str, Any] | None = None,
        error: dict[str, Any] | None = None,
    ) -> None:
        """Write one response frame to the local client."""
        payload = {"ok": ok}
        if ok:
            payload["result"] = result or {}
        else:
            payload["error"] = error or {"message": "Unknown local daemon error"}
        writer.write((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))
        await writer.drain()


__all__ = [
    "DEFAULT_LOCAL_DAEMON_HOST",
    "DEFAULT_LOCAL_DAEMON_PORT",
    "LocalDaemonSettings",
    "LocalMessageDaemon",
    "call_local_daemon",
    "is_local_daemon_available",
    "load_local_daemon_settings",
]
