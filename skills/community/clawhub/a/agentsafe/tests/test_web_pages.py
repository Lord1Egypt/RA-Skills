"""Public web pages (/ , /terms, /privacy, /refund) and the access-log
middleware (visitor IP + time, 30-day retention per PRIVACY_POLICY.md).
"""

import json
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from httpx import ASGITransport
from starlette.middleware import Middleware as StarletteMiddleware

from agentsafe.config import Settings
from agentsafe.server import build_server
from agentsafe.web.access_log import ACCESS_LOG_RETENTION_DAYS, AccessLogMiddleware, AccessLogStore
from agentsafe.web.pages import legal_html, legal_markdown


def _settings(**kw) -> Settings:
    base = {
        "INFURA_ETH_ENDPOINT": "https://rpc.test",
        "ETHERSCAN_API_KEY": "k",
        "GITHUB_TOKEN": "ghp-t",
        "GITHUB_REPO": "owner/repo",
        "LLM_PROVIDERS_JSON": json.dumps(
            [
                {
                    "name": "p",
                    "base_url": "https://l.test",
                    "api_key": "k",
                    "model": "m",
                    "rpm_limit": 60,
                }
            ]
        ),
        "TASK_STORE": "memory",
        "PAYMENTS_ENABLED": False,
    }
    base.update(kw)
    return Settings(_env_file=None, **base)


def _http_client(server, *, store: AccessLogStore | None = None, **kw):
    middleware = [StarletteMiddleware(AccessLogMiddleware, store=store)] if store else None
    app = server.http_app(middleware=middleware, **kw)
    return httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")


class TestPublicPages:
    async def test_index_served_at_root(self):
        server = build_server(_settings())
        async with _http_client(server) as client:
            r = await client.get("/")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert "agentSAFE" in r.text
        # pricing table: every tier price
        for price in ("$0.50", "$2.50", "$5.00", "$25.00"):
            assert price in r.text
        # enterprise CTA + legal footer links
        assert "https://tally.so/r/laby7B" in r.text
        assert 'href="/terms"' in r.text
        assert 'href="/privacy"' in r.text
        assert 'href="/refund"' in r.text
        # Claude config JSON present
        assert '"mcpServers"' in r.text
        assert '"agentsafe"' in r.text

    @pytest.mark.parametrize(
        ("path", "marker", "has_table"),
        [
            ("/terms", "Terms of Service", True),
            ("/terms", "non-refundable", True),
            ("/privacy", "Privacy Policy", True),
            ("/privacy", "30 days", True),
            ("/refund", "Refund Policy", False),
            ("/refund", "full refund", False),
        ],
    )
    async def test_legal_pages_rendered(self, path, marker, has_table):
        server = build_server(_settings())
        async with _http_client(server) as client:
            r = await client.get(path)
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert ("<table" in r.text) is has_table  # tables render when present
        assert marker in r.text

    async def test_legal_pages_cross_link_each_other(self):
        server = build_server(_settings())
        async with _http_client(server) as client:
            r = await client.get("/privacy")
        for link in ('href="/terms"', 'href="/privacy"', 'href="/refund"'):
            assert link in r.text


class TestAccessLogStore:
    def test_log_and_purge_30_day_retention(self, tmp_path):
        store = AccessLogStore(str(tmp_path / "access.db"))
        now = datetime.now(UTC)
        store.log("1.2.3.4", "GET", "/", when=now - timedelta(days=29))
        store.log("5.6.7.8", "GET", "/terms", when=now - timedelta(days=31))
        assert store.count() == 2
        removed = store.purge()
        assert removed == 1  # only the 31-day-old entry exceeds retention
        assert store.count() == 1
        assert ACCESS_LOG_RETENTION_DAYS == 30

    async def test_middleware_records_ip_path_and_time(self, tmp_path):
        store = AccessLogStore(str(tmp_path / "access.db"))
        server = build_server(_settings())
        async with _http_client(server, store=store) as client:
            r = await client.get("/", headers={"X-Forwarded-For": "203.0.113.9"})
        assert r.status_code == 200
        entries = store.entries()
        assert len(entries) == 1
        assert entries[0]["ip"] == "203.0.113.9"  # X-Forwarded-For honored
        assert entries[0]["path"] == "/"
        # timestamp parses as UTC ISO-8601
        datetime.fromisoformat(entries[0]["ts"])

    async def test_middleware_logs_transport_peer_without_proxy_header(self, tmp_path):
        store = AccessLogStore(str(tmp_path / "access.db"))
        server = build_server(_settings())
        async with _http_client(server, store=store) as client:
            await client.get("/terms")
        assert store.count() == 1
        assert store.entries()[0]["path"] == "/terms"


class TestLegalContentIntegrity:
    """The served pages come from the repository Markdown files; the key
    public commitments must be present in the raw source."""

    def test_privacy_states_30_day_ip_retention(self):
        raw = legal_markdown("privacy")
        assert "30 days" in raw
        assert "PDPO" in raw
        assert "anti-DDoS" in raw

    def test_terms_state_ai_disclaimer_and_tally_link(self):
        raw = legal_markdown("terms")
        assert "AI-assisted" in raw
        assert "not a substitute for a professional security audit" in raw
        assert "https://tally.so/r/laby7B" in raw

    def test_rendered_pages_have_rendered_headings(self):
        for slug in ("terms", "privacy", "refund"):
            html = legal_html(slug)
            assert "<h1" in html, slug  # markdown heading rendered (BOM-safe)
