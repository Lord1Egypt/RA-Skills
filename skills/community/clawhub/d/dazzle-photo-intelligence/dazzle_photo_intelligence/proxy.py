"""Stdio MCP proxy that auto-runs the OAuth2 device flow when the keyring has no tokens.

OpenClaw (or any MCP-capable agent) launches this as a stdio MCP server. The proxy:

- when authenticated, forwards each JSON-RPC request to Dazzle's HTTPS /mcp endpoint with a
  fresh bearer token (refreshing under an OS file lock if needed).
- when not authenticated, exposes a single `dazzle_login_required` tool. Calling it starts the
  OAuth2 device authorization grant (RFC 8628) and returns the verification URL + user code as
  the tool result, which the agent surfaces to the user. There is no background polling: every
  subsequent JSON-RPC request (tools/list or tools/call) makes one /oauth2/token call to check
  whether the user has approved the device code, and once tokens land in the keyring real tools
  become available.

Concurrent proxies on the same host share ~/.cache/dazzle-photo-intelligence/pending.json under
refresh.lock, so a user only ever sees one device-flow URL across all running instances; any
process can drive the flow to completion on its next query.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import sys
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from dazzle_photo_intelligence import storage

logger = logging.getLogger(__name__)

DAZZLE_API_HOST = "https://api.dazzle.ai"
DEFAULT_CLIENT_ID = "openclaw-dazzle-skill"
DEFAULT_SCOPE = "query"
DEVICE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
LOGIN_REQUIRED_TOOL = "dazzle_login_required"

_REFRESH_GRACE = timedelta(minutes=2)
_HTTP_TIMEOUT = 60.0


# --- Filesystem helpers ---


def _cache_dir() -> Path:
    base = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
    target = base / "dazzle-photo-intelligence"
    target.mkdir(parents=True, exist_ok=True)
    return target


def _pending_path() -> Path:
    return _cache_dir() / "pending.json"


@contextlib.contextmanager
def _refresh_lock() -> Iterator[None]:
    """Cross-platform exclusive file lock guarding keyring writes and pending.json IO."""
    lock_path = _cache_dir() / "refresh.lock"
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        if sys.platform == "win32":
            import msvcrt

            msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


# --- Pending login cache ---


def _load_pending() -> dict[str, Any] | None:
    path = _pending_path()
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def _write_pending(data: dict[str, Any]) -> None:
    fd = os.open(_pending_path(), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(json.dumps(data))


def _delete_pending() -> None:
    with contextlib.suppress(FileNotFoundError):
        _pending_path().unlink()


def _is_pending_fresh(pending: dict[str, Any]) -> bool:
    expires_at = _parse_iso(pending.get("expires_at"))
    return expires_at is not None and datetime.now(UTC) < expires_at


# --- Token state ---


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def _access_token_is_fresh() -> bool:
    expires_at = _parse_iso(storage.get("expires_at"))
    if expires_at is None:
        return False
    return datetime.now(UTC) + _REFRESH_GRACE < expires_at


def _has_refresh_token() -> bool:
    return bool(storage.get("refresh_token"))


def _store_tokens(tokens: dict[str, Any], client_id: str) -> None:
    expires_at = datetime.now(UTC) + timedelta(seconds=int(tokens["expires_in"]))
    storage.set_("access_token", tokens["access_token"])
    storage.set_("refresh_token", tokens["refresh_token"])
    storage.set_("expires_at", expires_at.isoformat())
    storage.set_("client_id", client_id)


# --- Device flow primitives ---


async def _start_device_authorization(
    client: httpx.AsyncClient, host: str, client_id: str, scope: str
) -> dict[str, Any]:
    response = await client.post(
        f"{host}/oauth2/device_authorization",
        data={"client_id": client_id, "scope": scope},
        timeout=_HTTP_TIMEOUT,
    )
    if response.status_code != 200:
        raise RuntimeError(f"device_authorization_failed: HTTP {response.status_code}: {response.text}")
    return response.json()


async def _poll_device_token_once(
    client: httpx.AsyncClient, host: str, client_id: str, device_code: str
) -> tuple[dict[str, Any] | None, str]:
    response = await client.post(
        f"{host}/oauth2/token",
        data={"grant_type": DEVICE_GRANT_TYPE, "device_code": device_code, "client_id": client_id},
        timeout=_HTTP_TIMEOUT,
    )
    if response.status_code == 200:
        return response.json(), ""
    try:
        payload = response.json()
    except ValueError:
        payload = {}
    error = payload.get("error", "")
    return None, error or "invalid_grant"


# --- Refresh-token rotation ---


async def _refresh_access_token(client: httpx.AsyncClient, host: str, client_id: str) -> str | None:
    """Refresh the access token. Returns the new access token, or None if refresh failed.

    Storage writes happen under _refresh_lock so concurrent proxies can't corrupt the
    file-backed keyring. On a non-200 response, re-checks under the lock for a peer-rotated
    token before giving up — refresh tokens are one-time-use, so when multiple processes
    race on the same /oauth2/token call only one wins; without this peer-check the losers
    would return None and trigger spurious _clear_tokens() that would sign the user out.
    """
    refresh_token = storage.get("refresh_token")
    if not refresh_token:
        return None

    response = await client.post(
        f"{host}/oauth2/token",
        data={"grant_type": "refresh_token", "refresh_token": refresh_token, "client_id": client_id},
        timeout=_HTTP_TIMEOUT,
    )

    loop = asyncio.get_running_loop()

    if response.status_code != 200:

        def _peer_token_or_none() -> str | None:
            with _refresh_lock():
                if _access_token_is_fresh():
                    return storage.get("access_token")
                return None

        return await loop.run_in_executor(None, _peer_token_or_none)

    payload = response.json()

    def _store_or_use_peer() -> str:
        with _refresh_lock():
            if _access_token_is_fresh():
                return str(storage.get("access_token"))
            expires_at = datetime.now(UTC) + timedelta(seconds=int(payload["expires_in"]))
            storage.set_("access_token", payload["access_token"])
            storage.set_("refresh_token", payload["refresh_token"])
            storage.set_("expires_at", expires_at.isoformat())
            return str(payload["access_token"])

    return await loop.run_in_executor(None, _store_or_use_peer)


async def _ensure_access_token(client: httpx.AsyncClient, host: str, client_id: str) -> str | None:
    """Return a usable access token, refreshing or completing pending login if needed."""
    if _access_token_is_fresh():
        token = storage.get("access_token")
        if token:
            return token

    if not _has_refresh_token():
        await _complete_pending_if_ready(client, host, client_id)
        if not _has_refresh_token():
            return None

    loop = asyncio.get_running_loop()

    def _locked_refresh() -> tuple[str | None, bool]:
        with _refresh_lock():
            if _access_token_is_fresh():
                return storage.get("access_token"), False
            return None, True

    cached_token, needs_refresh = await loop.run_in_executor(None, _locked_refresh)
    if not needs_refresh:
        return cached_token

    return await _refresh_access_token(client, host, client_id)


async def _clear_tokens() -> None:
    loop = asyncio.get_running_loop()

    def _do_clear() -> None:
        with _refresh_lock():
            storage.clear_all()

    await loop.run_in_executor(None, _do_clear)


# --- JSON-RPC forwarding ---


async def _forward(
    client: httpx.AsyncClient,
    host: str,
    client_id: str,
    method: str,
    params: dict[str, Any] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"jsonrpc": "2.0", "method": method, "id": 1}
    if params is not None:
        body["params"] = params

    async def _post() -> httpx.Response:
        token = await _ensure_access_token(client, host, client_id)
        if not token:
            raise RuntimeError("not_signed_in")
        return await client.post(
            f"{host}/mcp",
            json=body,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=_HTTP_TIMEOUT,
        )

    response = await _post()
    if response.status_code == 401:
        new_token = await _refresh_access_token(client, host, client_id)
        if not new_token:
            await _clear_tokens()
            raise RuntimeError("not_signed_in")
        response = await _post()
        if response.status_code == 401:
            await _clear_tokens()
            raise RuntimeError("not_signed_in")

    response.raise_for_status()
    return response.json()


# --- Login coordinator + one-shot completion ---


class _LoginCoordinator:
    """In-process state for an in-flight device authorization grant."""

    def __init__(self) -> None:
        self.last_failure_reason: str | None = None


async def _complete_pending_if_ready(client: httpx.AsyncClient, host: str, client_id: str) -> str | None:
    """Single-shot check: if a fresh pending device flow exists, hit /oauth2/token once.

    On success, stores the tokens and clears pending. Returns a terminal failure reason
    (access_denied, expired_token, invalid_grant, ...) if the flow died, or None otherwise
    (no pending, still authorization_pending, slow_down, or another process won the race).
    """
    loop = asyncio.get_running_loop()

    def _peek() -> dict[str, Any] | None:
        with _refresh_lock():
            if _has_refresh_token():
                return None
            pending = _load_pending()
            if pending and _is_pending_fresh(pending):
                return pending
            if pending:
                _delete_pending()
            return None

    pending = await loop.run_in_executor(None, _peek)
    if pending is None:
        return None

    device_code = pending["device_code"]
    tokens, error = await _poll_device_token_once(client, host, client_id, device_code)

    if tokens is not None:

        def _store() -> None:
            with _refresh_lock():
                _store_tokens(tokens, client_id)
                _delete_pending()

        await loop.run_in_executor(None, _store)
        return None

    if error in ("authorization_pending", "slow_down"):
        return None

    def _check_or_clear() -> str | None:
        with _refresh_lock():
            if _has_refresh_token():
                return None
            current = _load_pending()
            if current and current.get("device_code") == device_code:
                _delete_pending()
            return error or "invalid_grant"

    return await loop.run_in_executor(None, _check_or_clear)


async def _ensure_login(
    coord: _LoginCoordinator,
    client: httpx.AsyncClient,
    host: str,
    client_id: str,
    scope: str,
) -> dict[str, Any]:
    """Drive the device flow forward by one step. Returns {status, pending?}."""
    loop = asyncio.get_running_loop()

    failure = await _complete_pending_if_ready(client, host, client_id)
    if failure is not None:
        coord.last_failure_reason = failure

    def _peek() -> tuple[str, dict[str, Any] | None]:
        with _refresh_lock():
            if _has_refresh_token():
                return "authenticated", None
            pending = _load_pending()
            if pending and _is_pending_fresh(pending):
                return "have_pending", pending
            if pending:
                _delete_pending()
            return "no_pending", None

    role, pending = await loop.run_in_executor(None, _peek)

    if role == "authenticated":
        return {"status": "authenticated"}

    if role == "have_pending" and pending is not None:
        return {"status": "pending", "pending": pending}

    flow = await _start_device_authorization(client, host, client_id, scope)
    expires_at = datetime.now(UTC) + timedelta(seconds=int(flow.get("expires_in", 900)))
    new_pending: dict[str, Any] = {
        "device_code": flow["device_code"],
        "user_code": flow["user_code"],
        "verification_uri": flow.get("verification_uri"),
        "verification_uri_complete": flow.get("verification_uri_complete") or flow.get("verification_uri"),
        "expires_at": expires_at.isoformat(),
        "interval": int(flow.get("interval", 5)),
    }

    def _persist() -> dict[str, Any]:
        with _refresh_lock():
            existing = _load_pending()
            if existing and _is_pending_fresh(existing):
                return existing
            _write_pending(new_pending)
            return new_pending

    final = await loop.run_in_executor(None, _persist)
    return {"status": "pending", "pending": final}


# --- MCP server wiring ---


def _format_login_message(pending: dict[str, Any], failure_prefix: str = "") -> str:
    url = pending.get("verification_uri_complete") or pending.get("verification_uri") or ""
    code = pending.get("user_code", "")
    body = (
        "Sign in to Dazzle to query your photos.\n\n"
        f"Open this URL in a browser: {url}\n"
        f"Confirm the code: {code}\n\n"
        "After approving, ask your question again."
    )
    return f"{failure_prefix}{body}" if failure_prefix else body


def _login_required_tool() -> Tool:
    return Tool(
        name=LOGIN_REQUIRED_TOOL,
        description=(
            "User must sign in to Dazzle. Call this tool to receive a sign-in URL to surface to "
            "the user. Real query tools become available after sign-in — re-list tools then."
        ),
        inputSchema={"type": "object", "properties": {}},
    )


def _consume_failure_prefix(coord: _LoginCoordinator) -> str:
    reason = coord.last_failure_reason
    if reason is None:
        return ""
    coord.last_failure_reason = None
    if reason == "access_denied":
        return "Previous sign-in was denied. "
    if reason == "expired_token":
        return "Previous sign-in code expired. "
    return f"Previous sign-in failed ({reason}). "


def _create_server(host: str, client_id: str, scope: str = DEFAULT_SCOPE) -> Server:
    server: Server = Server("dazzle-photo-intelligence")
    coord = _LoginCoordinator()

    @contextlib.asynccontextmanager
    async def _http_client() -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient() as client:
            yield client

    async def _serve_login(client: httpx.AsyncClient) -> str:
        result = await _ensure_login(coord, client, host, client_id, scope)
        if result["status"] == "authenticated":
            return "You're signed in to Dazzle. Re-list tools to see real query tools, then ask your question again."
        prefix = _consume_failure_prefix(coord)
        return _format_login_message(result["pending"], prefix)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        async with _http_client() as client:
            if not _has_refresh_token():
                await _complete_pending_if_ready(client, host, client_id)
                if not _has_refresh_token():
                    return [_login_required_tool()]
            try:
                result = await _forward(client, host, client_id, "tools/list", None)
            except RuntimeError as exc:
                if str(exc) == "not_signed_in":
                    return [_login_required_tool()]
                raise
            tools_payload = result.get("result", {}).get("tools", [])
            return [
                Tool(
                    name=t["name"],
                    description=t.get("description", ""),
                    inputSchema=t.get("inputSchema", {"type": "object", "properties": {}}),
                )
                for t in tools_payload
            ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        async with _http_client() as client:
            if name == LOGIN_REQUIRED_TOOL:
                return [TextContent(type="text", text=await _serve_login(client))]
            try:
                result = await _forward(client, host, client_id, "tools/call", {"name": name, "arguments": arguments})
            except RuntimeError as exc:
                if str(exc) == "not_signed_in":
                    return [TextContent(type="text", text=await _serve_login(client))]
                raise
            content_payload = result.get("result", {}).get("content", [])
            return [
                TextContent(type="text", text=item.get("text", json.dumps(item)))
                for item in content_payload
                if item.get("type") == "text"
            ] or [TextContent(type="text", text=json.dumps(result.get("result", {})))]

    return server


def main() -> None:
    try:
        storage.ensure_writable()
    except storage.StorageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)

    host = DAZZLE_API_HOST
    if not host.startswith("https://"):
        print(f"error: refusing non-HTTPS host {host!r}; bearer tokens must not travel in cleartext", file=sys.stderr)
        sys.exit(2)
    client_id = storage.get("client_id") or os.environ.get("DAZZLE_CLIENT_ID") or DEFAULT_CLIENT_ID
    scope = os.environ.get("DAZZLE_SCOPE", DEFAULT_SCOPE)

    async def run() -> None:
        server = _create_server(host, client_id, scope)
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
