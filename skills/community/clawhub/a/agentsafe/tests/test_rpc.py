"""Phase 2 tests: RPC client (respx-mocked; no real network, no real keys)."""

import httpx
import pytest
import respx

from agentsafe.rpc import (
    EthRpcClient,
    RpcPermanentError,
    RpcTransientError,
)

ADDR = "0x" + "ab" * 20
ENDPOINT = "https://rpc.test/v3/key"


def _rpc_result(code: str) -> dict:
    return {"jsonrpc": "2.0", "id": 1, "result": code}


async def _nosleep(_: float) -> None:
    return None


def _client(**kw) -> EthRpcClient:
    kw.setdefault("sleeper", _nosleep)
    return EthRpcClient(ENDPOINT, **kw)


class TestRpcHappyPath:
    @respx.mock
    async def test_contract_code(self):
        code = "0x6080" + "ff" * 100
        respx.post(ENDPOINT).mock(return_value=httpx.Response(200, json=_rpc_result(code)))
        c = _client()
        assert await c.get_code(ADDR) == code
        assert await c.is_contract(ADDR) is True
        assert await c.get_code_size(ADDR) == 102  # (4 + 200 hex chars) / 2

    @respx.mock
    async def test_eoa_returns_0x_not_an_error(self):
        respx.post(ENDPOINT).mock(return_value=httpx.Response(200, json=_rpc_result("0x")))
        c = _client()
        assert await c.get_code(ADDR) == "0x"
        assert await c.is_contract(ADDR) is False
        assert await c.get_code_size(ADDR) == 0

    @respx.mock
    async def test_mixed_case_address_normalized_before_request(self):
        mixed = "0xAbCdEf" + "11" * 17
        route = respx.post(ENDPOINT).mock(
            return_value=httpx.Response(200, json=_rpc_result("0x6080"))
        )
        c = _client()
        await c.get_code(mixed)
        sent = route.calls.last.request.read()
        assert mixed.lower() in sent.decode()  # lowercase on the wire

    @respx.mock
    async def test_uppercase_0x_prefix_normalized(self):
        route = respx.post(ENDPOINT).mock(
            return_value=httpx.Response(200, json=_rpc_result("0x6080"))
        )
        await _client().get_code("0X" + "ab" * 20)
        assert route.called

    async def test_invalid_address_rejected_without_http(self):
        c = _client()
        with pytest.raises(ValueError, match="invalid EVM address"):
            await c.get_code("0x123")

    async def test_invalid_endpoint_rejected(self):
        with pytest.raises(ValueError):
            EthRpcClient("ftp://nope")


class TestRpcRetries:
    @respx.mock
    async def test_429_then_success(self):
        route = respx.post(ENDPOINT)
        route.side_effect = [
            httpx.Response(429, json={}),
            httpx.Response(200, json=_rpc_result("0x6080")),
        ]
        c = _client(max_retries=2)
        assert await c.get_code(ADDR) == "0x6080"
        assert route.call_count == 2

    @respx.mock
    async def test_429_retries_exhausted(self):
        route = respx.post(ENDPOINT).mock(return_value=httpx.Response(429, json={}))
        c = _client(max_retries=2)
        with pytest.raises(RpcTransientError, match="giving up"):
            await c.get_code(ADDR)
        assert route.call_count == 3  # initial + 2 retries

    @respx.mock
    async def test_timeout_then_success(self):
        route = respx.post(ENDPOINT)
        route.side_effect = [
            httpx.ConnectTimeout("t/o"),
            httpx.Response(200, json=_rpc_result("0x6080")),
        ]
        c = _client(max_retries=1)
        assert await c.get_code(ADDR) == "0x6080"

    @respx.mock
    async def test_backoff_sleeps_called(self):
        respx.post(ENDPOINT).mock(return_value=httpx.Response(503, json={}))
        sleeps: list[float] = []

        async def recorder(d: float) -> None:
            sleeps.append(d)

        c = EthRpcClient(ENDPOINT, max_retries=2, backoff_base=0.5, sleeper=recorder)
        with pytest.raises(RpcTransientError):
            await c.get_code(ADDR)
        assert sleeps == [0.5, 1.0]  # exponential, capped

    @respx.mock
    async def test_jsonrpc_error_is_permanent_no_retry(self):
        route = respx.post(ENDPOINT).mock(
            return_value=httpx.Response(
                200,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "error": {"code": -32000, "message": "execution reverted"},
                },
            )
        )
        c = _client(max_retries=5)
        with pytest.raises(RpcPermanentError, match="execution reverted"):
            await c.get_code(ADDR)
        assert route.call_count == 1  # JSON-RPC errors are never retried

    @respx.mock
    async def test_non_hex_result_rejected(self):
        respx.post(ENDPOINT).mock(return_value=httpx.Response(200, json=_rpc_result("deadbeef")))
        c = _client()
        with pytest.raises(RpcPermanentError, match="non-hex"):
            await c.get_code(ADDR)

    @respx.mock
    async def test_http_404_permanent(self):
        respx.post(ENDPOINT).mock(return_value=httpx.Response(404, text="not found"))
        c = _client(max_retries=5)
        with pytest.raises(RpcPermanentError, match="404"):
            await c.get_code(ADDR)
