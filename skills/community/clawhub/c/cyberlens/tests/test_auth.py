"""Tests for the CyberLens connect flow helpers."""

import pytest

from src import auth


class _MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class _MockAsyncClient:
    def __init__(self, response, calls, *args, **kwargs):
        self._response = response
        self._calls = calls

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json):
        self._calls["url"] = url
        self._calls["json"] = json
        return self._response


def test_resolve_callback_config_defaults_to_localhost(monkeypatch):
    monkeypatch.delenv("CYBERLENS_CONNECT_CALLBACK_URL", raising=False)
    monkeypatch.delenv("CYBERLENS_CONNECT_BIND_HOST", raising=False)
    monkeypatch.delenv("CYBERLENS_CONNECT_BIND_PORT", raising=False)
    monkeypatch.setattr(auth, "_find_open_port", lambda: 54321)

    bind_host, bind_port, callback_url = auth._resolve_callback_config()

    assert bind_host == "127.0.0.1"
    assert bind_port == 54321
    assert callback_url == "http://localhost:54321/callback"


def test_resolve_callback_config_uses_remote_callback(monkeypatch):
    monkeypatch.setenv(
        "CYBERLENS_CONNECT_CALLBACK_URL",
        "http://10.0.0.5:55432/callback",
    )
    monkeypatch.delenv("CYBERLENS_CONNECT_BIND_HOST", raising=False)
    monkeypatch.delenv("CYBERLENS_CONNECT_BIND_PORT", raising=False)

    bind_host, bind_port, callback_url = auth._resolve_callback_config()

    assert bind_host == "0.0.0.0"
    assert bind_port == 55432
    assert callback_url == "http://10.0.0.5:55432/callback"


def test_resolve_callback_config_supports_proxy_bind_override(monkeypatch):
    monkeypatch.setenv(
        "CYBERLENS_CONNECT_CALLBACK_URL",
        "https://openclaw.example.com/cyberlens/callback",
    )
    monkeypatch.setenv("CYBERLENS_CONNECT_BIND_HOST", "127.0.0.1")
    monkeypatch.setenv("CYBERLENS_CONNECT_BIND_PORT", "54321")

    bind_host, bind_port, callback_url = auth._resolve_callback_config()

    assert bind_host == "127.0.0.1"
    assert bind_port == 54321
    assert callback_url == "https://openclaw.example.com/cyberlens/callback"


def test_resolve_callback_config_requires_bind_port_when_callback_has_no_port(monkeypatch):
    monkeypatch.setenv(
        "CYBERLENS_CONNECT_CALLBACK_URL",
        "https://openclaw.example.com/cyberlens/callback",
    )
    monkeypatch.delenv("CYBERLENS_CONNECT_BIND_HOST", raising=False)
    monkeypatch.delenv("CYBERLENS_CONNECT_BIND_PORT", raising=False)

    with pytest.raises(ValueError, match="include a port"):
        auth._resolve_callback_config()


@pytest.mark.asyncio
async def test_exchange_connect_code_returns_full_key(monkeypatch):
    calls = {}

    def _client_factory(*args, **kwargs):
        return _MockAsyncClient(
            _MockResponse(200, {"fullKey": "clns_acct_test"}),
            calls,
            *args,
            **kwargs,
        )

    monkeypatch.setattr(auth.httpx, "AsyncClient", _client_factory)

    key = await auth._exchange_connect_code(
        "clcn_test",
        "https://api.cyberlensai.com/functions/v1/integration-connect/exchange",
    )

    assert key == "clns_acct_test"
    assert calls["url"] == "https://api.cyberlensai.com/functions/v1/integration-connect/exchange"
    assert calls["json"] == {"code": "clcn_test"}


@pytest.mark.asyncio
async def test_exchange_connect_code_raises_for_expired_code(monkeypatch):
    def _client_factory(*args, **kwargs):
        return _MockAsyncClient(
            _MockResponse(410, {"error": "Exchange code has expired."}),
            {},
            *args,
            **kwargs,
        )

    monkeypatch.setattr(auth.httpx, "AsyncClient", _client_factory)

    with pytest.raises(RuntimeError, match="expired"):
        await auth._exchange_connect_code(
            "clcn_test",
            "https://api.cyberlensai.com/functions/v1/integration-connect/exchange",
        )


@pytest.mark.asyncio
async def test_exchange_connect_code_rejects_untrusted_host():
    with pytest.raises(ValueError, match="untrusted exchange host"):
        await auth._exchange_connect_code(
            "clcn_test",
            "https://evil.example.com/functions/v1/integration-connect/exchange",
        )
