"""Etherscan V2 client + verified-source preservation.

Uses the current Etherscan V2 unified API:
    GET https://api.etherscan.io/v2/api?chainid=1&module=contract
        &action=getsourcecode&address=<addr>&apikey=<key>
(chainid=1 == Ethereum Mainnet; V1 module endpoints were retired in 2025.)

Multi-file contracts arrive as Etherscan's double-brace-escaped Standard JSON:
    SourceCode = "{{ \\"language\\": \\"Solidity\\", \\"sources\\": {..}, ... }}"
We MUST preserve file names, directory structure and settings - concatenating
files would break compilation and imports.

The API key is never logged. Rate-limit / auth / not-verified are distinct,
typed outcomes. Actual endpoint behavior must be re-verified at deploy time.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from pydantic import BaseModel, Field

from agentsafe.schemas import normalize_address

logger = logging.getLogger("agentSAFE.explorer")

ETHERSCAN_V2_BASE = "https://api.etherscan.io/v2/api"
ETH_MAINNET_CHAIN_ID = 1

_TRANSIENT_HTTP = {429, 500, 502, 503, 504}
_RATE_LIMIT_MARKERS = ("rate limit", "max rate", "too many requests")


class ExplorerError(RuntimeError):
    pass


class ExplorerRateLimitError(ExplorerError):
    """Quota exhausted - callers must back off, not hammer the endpoint."""


class ExplorerAuthError(ExplorerError):
    """Invalid/missing API key."""


class ContractNotVerifiedError(ExplorerError):
    """No verified source on Etherscan for this address."""


class SourceFile(BaseModel):
    path: str = Field(min_length=1)
    content: str


class SourceBundle(BaseModel):
    """Preserved multi-file project exactly as published by the explorer."""

    is_verified: bool
    contract_name: str = ""
    compiler_version: str = ""
    language: str = "Solidity"
    files: list[SourceFile] = Field(default_factory=list)
    settings: dict[str, Any] | None = None
    abi: str = ""
    optimization_used: bool | None = None
    runs: int | None = None
    evm_version: str | None = None
    is_proxy: bool = False
    implementation: str | None = None


def parse_source_code(raw: str) -> tuple[list[SourceFile], dict[str, Any] | None, str]:
    """Parse Etherscan's SourceCode field into files + settings + language.

    Handles: plain source, Standard JSON ``{...}``, and double-brace escaped
    Standard JSON ``{{...}}`` (multi-file). Never concatenates files.
    """
    s = (raw or "").strip()
    if not s:
        return [], None, "Solidity"

    std: dict[str, Any] | None = None
    if s.startswith("{{"):
        if not s.endswith("}}"):
            raise ExplorerError("multi-file SourceCode has unbalanced '{{ ... }}' wrapping")
        inner = s[1:-1]  # Etherscan escapes Standard JSON with an extra brace
        try:
            std = json.loads(inner)
        except json.JSONDecodeError as exc:
            raise ExplorerError(f"multi-file SourceCode is not valid Standard JSON: {exc}") from exc
    elif s.startswith("{") and s.endswith("}"):
        try:
            std = json.loads(s)
        except json.JSONDecodeError:
            std = None  # plain source that merely starts with '{'

    if std is not None and isinstance(std, dict) and "sources" in std:
        sources = std.get("sources")
        if not isinstance(sources, dict) or not sources:
            raise ExplorerError("Standard JSON 'sources' must be a non-empty object")
        files: list[SourceFile] = []
        for path, entry in sources.items():
            content = entry.get("content") if isinstance(entry, dict) else None
            if not isinstance(content, str):
                raise ExplorerError(f"source file {path!r} has no 'content'")
            files.append(SourceFile(path=path, content=content))
        settings = std.get("settings")
        language = str(std.get("language") or "Solidity")
        return files, settings if isinstance(settings, dict) else None, language

    # Plain single-file source
    return [SourceFile(path="contract.sol", content=raw)], None, "Solidity"


class EtherscanClient:
    """Etherscan V2 contract-source client (Ethereum Mainnet, chainid=1)."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = ETHERSCAN_V2_BASE,
        timeout_seconds: float = 20.0,
        max_retries: int = 3,
        backoff_base: float = 0.5,
        backoff_cap: float = 8.0,
        client: httpx.AsyncClient | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
        strict: bool = True,
    ) -> None:
        if strict:
            # Deferred (strict=False) mode is for cloud build-time inspection
            # only; the server lifespan re-validates config at runtime.
            if not api_key:
                raise ValueError("Etherscan API key is required")
            if not base_url.startswith(("http://", "https://")):
                raise ValueError("Etherscan base_url must be an http(s) URL")
        self._api_key = api_key
        self._base_url = base_url
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._backoff_cap = backoff_cap
        self._sleeper = sleeper or asyncio.sleep
        self._client = client or httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_seconds, connect=timeout_seconds),
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_verified_source(self, address: str) -> SourceBundle:
        """Fetch verification status + preserved source project for `address`.

        Raises ContractNotVerifiedError when no verified source exists.
        """
        addr = normalize_address(address)
        params = {
            "chainid": str(ETH_MAINNET_CHAIN_ID),
            "module": "contract",
            "action": "getsourcecode",
            "address": addr,
            "apikey": self._api_key,
        }
        data = await self._get(params, addr)
        result = data.get("result")
        if not isinstance(result, list) or not result:
            raise ContractNotVerifiedError(f"no source record for {addr}")
        rec = result[0]
        if not isinstance(rec, dict):
            raise ExplorerError(f"unexpected Etherscan result shape for {addr}")

        source_raw = rec.get("SourceCode") or ""
        contract_name = (rec.get("ContractName") or "").strip()
        if not source_raw.strip() or not contract_name:
            raise ContractNotVerifiedError(f"contract at {addr} is not verified")

        files, settings, language = parse_source_code(source_raw)
        if not files:
            raise ContractNotVerifiedError(f"empty verified source for {addr}")

        opt = rec.get("OptimizationUsed")
        runs = rec.get("Runs")
        impl = rec.get("Implementation")
        return SourceBundle(
            is_verified=True,
            contract_name=contract_name,
            compiler_version=(rec.get("CompilerVersion") or "").strip(),
            language=language,
            files=files,
            settings=settings,
            abi=rec.get("ABI") or "",
            optimization_used=None if opt in (None, "") else opt == "1",
            runs=None if runs in (None, "") else int(runs),
            evm_version=(rec.get("EVMVersion") or "").strip() or None,
            is_proxy=(rec.get("Proxy") or "") == "1",
            implementation=impl if impl else None,
        )

    async def _get(self, params: dict[str, str], addr: str) -> dict[str, Any]:
        attempt = 0
        while True:
            transient: ExplorerError | None = None
            try:
                resp = await self._client.get(self._base_url, params=params)
                if resp.status_code in _TRANSIENT_HTTP:
                    transient = ExplorerError(f"HTTP {resp.status_code} from Etherscan")
                elif resp.status_code != 200:
                    raise ExplorerError(f"HTTP {resp.status_code} from Etherscan")
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                transient = ExplorerError(f"transport error: {exc}")

            if transient is None:
                return self._parse_etherscan(resp, addr)

            if attempt >= self._max_retries:
                raise ExplorerRateLimitError(
                    f"Etherscan: giving up after {attempt + 1} attempts ({transient})"
                ) from transient
            delay = min(self._backoff_base * (2**attempt), self._backoff_cap)
            logger.debug(
                "etherscan %s transient error, retry %d/%d in %.1fs",
                addr,
                attempt + 1,
                self._max_retries,
                delay,
            )
            await self._sleeper(delay)
            attempt += 1

    @staticmethod
    def _parse_etherscan(resp: httpx.Response, addr: str) -> dict[str, Any]:
        try:
            data = resp.json()
        except ValueError as exc:
            raise ExplorerError("non-JSON response from Etherscan") from exc
        if not isinstance(data, dict):
            raise ExplorerError("unexpected Etherscan response shape")

        status = str(data.get("status", ""))
        message = str(data.get("message", ""))
        if status == "1":
            return data

        # Etherscan puts human-readable error text in EITHER message or result.
        result_field = data.get("result")
        combined = f"{message} {result_field if isinstance(result_field, str) else ''}".lower()
        if any(m in combined for m in _RATE_LIMIT_MARKERS):
            raise ExplorerRateLimitError(f"Etherscan rate limit: {message or result_field}")
        if "invalid api key" in combined or "missing api key" in combined:
            raise ExplorerAuthError("Etherscan rejected the API key")
        # status "0" with various messages: usually "NOTOK" / no data.
        raise ExplorerError(
            f"Etherscan API error for {addr}: status={status!r} message={message!r}"
        )
