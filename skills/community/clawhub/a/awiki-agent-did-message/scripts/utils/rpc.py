"""JSON-RPC 2.0 client helper functions.

[INPUT]: httpx.AsyncClient, endpoint path, method name, params, DIDWbaAuthHeader
[OUTPUT]: rpc_call() helper, authenticated_rpc_call() with 401 retry, JsonRpcError exception class
[POS]: Provides unified JSON-RPC call wrappers for auth.py and external callers

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

from typing import Any

import httpx


class JsonRpcError(Exception):
    """JSON-RPC error response exception."""

    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"JSON-RPC error {code}: {message}")


async def rpc_call(
    client: httpx.AsyncClient,
    endpoint: str,
    method: str,
    params: dict | None = None,
    request_id: int | str = 1,
) -> Any:
    """Send a JSON-RPC 2.0 request and return the result.

    Args:
        client: httpx async client.
        endpoint: RPC endpoint path (e.g., "/did-auth/rpc").
        method: RPC method name (e.g., "register").
        params: Method parameters.
        request_id: Request ID.

    Returns:
        Value of the JSON-RPC result field.

    Raises:
        JsonRpcError: When the server returns a JSON-RPC error.
        httpx.HTTPStatusError: On HTTP layer errors.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": request_id,
    }
    resp = await client.post(endpoint, json=payload)
    resp.raise_for_status()
    body = resp.json()
    if body.get("error") is not None:
        error = body["error"]
        raise JsonRpcError(
            error["code"],
            error["message"],
            error.get("data"),
        )
    return body["result"]


__all__ = [
    "JsonRpcError",
    "rpc_call",
    "authenticated_rpc_call",
]


async def authenticated_rpc_call(
    client: httpx.AsyncClient,
    endpoint: str,
    method: str,
    params: dict | None = None,
    request_id: int | str = 1,
    *,
    auth: Any = None,
    credential_name: str = "default",
) -> Any:
    """JSON-RPC 2.0 request with automatic 401 retry.

    Uses DIDWbaAuthHeader to manage authentication headers and token caching.
    On 401, automatically clears the expired token and regenerates DIDWba auth header to retry.

    Args:
        client: httpx async client (with base_url set).
        endpoint: RPC endpoint path.
        method: RPC method name.
        params: Method parameters.
        request_id: Request ID.
        auth: DIDWbaAuthHeader instance.
        credential_name: Credential name (for persisting new JWT).

    Returns:
        Value of the JSON-RPC result field.

    Raises:
        JsonRpcError: When the server returns a JSON-RPC error.
        httpx.HTTPStatusError: On HTTP layer errors (non-401).
    """
    server_url = str(client.base_url)
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": request_id,
    }

    # Get authentication headers
    auth_headers = auth.get_auth_header(server_url)
    resp = await client.post(endpoint, json=payload, headers=auth_headers)

    # 401 -> clear expired token -> re-authenticate -> retry
    if resp.status_code == 401:
        auth.clear_token(server_url)
        auth_headers = auth.get_auth_header(server_url, force_new=True)
        resp = await client.post(endpoint, json=payload, headers=auth_headers)

    resp.raise_for_status()

    # Success: cache new token from response headers
    # Note: httpx response header keys are lowercase, DIDWbaAuthHeader.update_token() expects "Authorization"
    auth_header_value = resp.headers.get("authorization", "")
    new_token = auth.update_token(server_url, {"Authorization": auth_header_value})
    if new_token:
        from credential_store import update_jwt
        update_jwt(credential_name, new_token)

    body = resp.json()
    if body.get("error") is not None:
        error = body["error"]
        raise JsonRpcError(
            error["code"],
            error["message"],
            error.get("data"),
        )
    return body["result"]
