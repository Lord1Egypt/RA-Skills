"""Ethereum Mainnet JSON-RPC 2.0 client.

- httpx.AsyncClient, connect/read timeouts, bounded exponential backoff.
- Transient errors only (timeout, transport error, HTTP 429/5xx) are retried.
- JSON-RPC level errors and invalid responses are permanent (no blind retry).
- An EOA ("0x" / empty code) is a VALID result, not an error.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import httpx

from agentsafe.schemas import normalize_address

logger = logging.getLogger("agentSAFE.rpc")

_TRANSIENT_HTTP = {429, 500, 502, 503, 504}


class RpcError(RuntimeError):
    """Base RPC failure. `transient` hints whether a retry could ever help."""


class RpcTransientError(RpcError):
    pass


class RpcPermanentError(RpcError):
    pass


class EthRpcClient:
    """Minimal eth_getCode client. Mainnet only; no arbitrary methods exposed."""

    def __init__(
        self,
        endpoint: str,
        *,
        timeout_seconds: float = 20.0,
        max_retries: int = 3,
        backoff_base: float = 0.5,
        backoff_cap: float = 8.0,
        client: httpx.AsyncClient | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        if not endpoint or not endpoint.startswith(("http://", "https://")):
            raise ValueError("RPC endpoint must be an http(s) URL")
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self._endpoint = endpoint
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._backoff_cap = backoff_cap
        self._sleeper = sleeper or asyncio.sleep
        self._client = client or httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_seconds, connect=timeout_seconds),
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_code(self, address: str) -> str:
        """Return runtime bytecode as 0x-hex. EOAs return "0x" (valid)."""
        addr = normalize_address(address)
        result = await self._call("eth_getCode", [addr, "latest"])
        if not isinstance(result, str) or not result.startswith("0x"):
            raise RpcPermanentError(f"eth_getCode returned non-hex result for {addr}")
        return result

    @staticmethod
    def code_size(code: str) -> int:
        """Byte length of 0x-hex bytecode; 0 for EOAs."""
        if not code or len(code) < 2:
            return 0
        return (len(code) - 2) // 2

    async def get_code_size(self, address: str) -> int:
        return self.code_size(await self.get_code(address))

    async def is_contract(self, address: str) -> bool:
        return await self.get_code_size(address) > 0

    async def _call(self, method: str, params: list[Any]) -> Any:
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        attempt = 0
        while True:
            transient: RpcTransientError | None = None
            try:
                resp = await self._client.post(self._endpoint, json=payload)
                if resp.status_code in _TRANSIENT_HTTP:
                    transient = RpcTransientError(f"HTTP {resp.status_code} from RPC")
                elif resp.status_code != 200:
                    raise RpcPermanentError(f"HTTP {resp.status_code} from RPC")
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                transient = RpcTransientError(f"transport error: {exc}")

            if transient is None:
                data = self._parse_jsonrpc(resp, method)
                return data["result"]

            if attempt >= self._max_retries:
                raise RpcTransientError(
                    f"{method}: giving up after {attempt + 1} attempts ({transient})"
                ) from transient
            delay = min(self._backoff_base * (2**attempt), self._backoff_cap)
            logger.debug(
                "rpc %s transient error, retry %d/%d in %.1fs",
                method,
                attempt + 1,
                self._max_retries,
                delay,
            )
            await self._sleeper(delay)
            attempt += 1

    @staticmethod
    def _parse_jsonrpc(resp: httpx.Response, method: str) -> dict[str, Any]:
        try:
            data = resp.json()
        except ValueError as exc:
            raise RpcPermanentError(f"{method}: non-JSON response from RPC") from exc
        if not isinstance(data, dict) or "error" in data:
            err = data.get("error") if isinstance(data, dict) else None
            msg = err.get("message") if isinstance(err, dict) else str(err)
            raise RpcPermanentError(f"{method}: JSON-RPC error: {msg}")
        if "result" not in data:
            raise RpcPermanentError(f"{method}: JSON-RPC response missing 'result'")
        return data
