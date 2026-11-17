"""api/index.py serverless entrypoint acceptance.

Reproduces the Vercel Python runtime condition: ASGI lifespan events are
NEVER emitted, so FastMCP's streamable-HTTP session manager must be started
by the entrypoint's bootstrap, not by a lifespan scope. Regression guard for
the production incident where every /mcp request returned HTTP 500
("Task group is not initialized").

Tests are hermetic: env vars are pinned before the module is imported so the
operator's real .env (PAYMENTS_ENABLED=true, live keys) can never leak in.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import importlib.util
import json
import sys
from pathlib import Path

import anyio
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "api" / "index.py"

_DUMMY_LLM = json.dumps(
    [
        {
            "name": "test-provider",
            "base_url": "https://llm.example/v1",
            "api_key": "sk-dummy",
            "model": "dummy-model",
            "rpm_limit": 5,
        }
    ]
)

_INIT_REQUEST = json.dumps(
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "vercel-probe", "version": "0.0.1"},
        },
    }
).encode()


def _http_scope(method: str, path: str, body: bytes = b"") -> dict:
    headers = [(b"host", b"agentsafe.example"), (b"content-type", b"application/json")]
    if body:
        headers.append((b"accept", b"application/json, text/event-stream"))
    return {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": method,
        "scheme": "https",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "root_path": "",
        "headers": headers,
        "client": ("203.0.113.7", 443),
        "server": ("agentsafe.example", 443),
    }


async def _call_asgi(app, scope: dict, body: bytes = b"") -> list[dict]:
    """Invoke the ASGI app the way Vercel's runtime does: no lifespan scope."""
    messages: list[dict] = []

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: dict) -> None:
        messages.append(message)

    await app(scope, receive, send)
    return messages


@pytest.fixture()
async def entry_module(monkeypatch):
    """Load api/index.py with a pinned, payments-disabled environment."""
    monkeypatch.setenv("PAYMENTS_ENABLED", "false")
    monkeypatch.setenv("TASK_STORE", "memory")
    monkeypatch.setenv("INFURA_ETH_ENDPOINT", "https://rpc.example/v3/dummy")
    monkeypatch.setenv("ETHERSCAN_API_KEY", "dummy-etherscan")
    monkeypatch.setenv("ETHERSCAN_BASE_URL", "https://etherscan.example/v2/api")
    monkeypatch.setenv("GITHUB_TOKEN", "ghp-dummy")
    monkeypatch.setenv("GITHUB_REPO", "owner/repo")
    monkeypatch.setenv("GITHUB_WORKFLOW_FILE", "docker-audit.yml")
    monkeypatch.setenv("GITHUB_REF", "main")
    monkeypatch.setenv("LLM_PROVIDERS_JSON", _DUMMY_LLM)

    spec = importlib.util.spec_from_file_location("api_index_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["api_index_under_test"] = module
    spec.loader.exec_module(module)
    try:
        yield module
    finally:
        # Close the bootstrap-held lifespan deterministically via the holder
        # task (aclose): the lifespan exits inside the task that entered it,
        # so anyio task groups and fastmcp ContextVar tokens unwind in the
        # correct context. Leaving it suspended would let loop
        # shutdown_asyncgens tear down the nested session-manager generators
        # from a foreign context and raise cross-context Token errors.
        bootstrap = getattr(module, "app", None)
        if bootstrap is not None and hasattr(bootstrap, "aclose"):
            with anyio.move_on_after(15):
                await bootstrap.aclose()
        sys.modules.pop("api_index_under_test", None)


class TestServerlessEntrypoint:
    async def test_initialize_without_lifespan_returns_200(self, entry_module):
        """THE Vercel regression: no lifespan scope ever arrives; /mcp must
        still serve. Before the bootstrap fix this returned 500 because the
        FastMCP session manager is only started inside the lifespan."""
        messages = await _call_asgi(
            entry_module.app,
            _http_scope("POST", "/mcp", _INIT_REQUEST),
            _INIT_REQUEST,
        )
        start = messages[0]
        assert start["type"] == "http.response.start"
        assert start["status"] == 200, f"messages={messages!r}"
        body = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
        payload = json.loads(body)
        assert payload["jsonrpc"] == "2.0"
        assert payload["id"] == 1
        assert payload["result"]["serverInfo"]["name"] == "agentSAFE"

    async def test_concurrent_first_requests_bootstrap_once(self, entry_module):
        """Two simultaneous cold-start requests must not double-enter the
        lifespan (guarded bootstrap) and both must succeed."""
        async with anyio.create_task_group() as tg:
            results: list[list[dict]] = [[], []]

            async def call(i: int):
                results[i] = await _call_asgi(
                    entry_module.app,
                    _http_scope("POST", "/mcp", _INIT_REQUEST),
                    _INIT_REQUEST,
                )

            tg.start_soon(call, 0)
            tg.start_soon(call, 1)
        for messages in results:
            assert messages[0]["status"] == 200, f"messages={messages!r}"

    async def test_landing_page_still_served(self, entry_module):
        """Custom routes pass through the bootstrap untouched."""
        messages = await _call_asgi(entry_module.app, _http_scope("GET", "/"))
        assert messages[0]["status"] == 200

    async def test_unknown_path_returns_404(self, entry_module):
        messages = await _call_asgi(entry_module.app, _http_scope("GET", "/nope"))
        assert messages[0]["status"] == 404

    async def test_without_bootstrap_lifespan_gap_breaks_mcp(self, entry_module):
        """Documents the root cause: the RAW FastMCP app (no bootstrap) 500s
        under the Vercel condition. If this ever starts passing, the
        bootstrap can be retired."""
        raw_app = entry_module.app._app  # unwrap the bootstrap middleware
        with pytest.raises(Exception):
            await _call_asgi(
                raw_app,
                _http_scope("POST", "/mcp", _INIT_REQUEST),
                _INIT_REQUEST,
            )


def _invoke_on_fresh_loop(app, scope: dict, body: bytes = b"") -> list[dict]:
    """Run one ASGI call on its OWN event loop in its OWN thread - exactly how
    a serverless runtime invokes a warm process between requests - then tear
    that loop down (holder cancelled inside its own context, asyncgens
    finalized, loop closed)."""
    def _worker():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(_call_asgi(app, scope, body))
        finally:
            state = getattr(app, "_state", None)
            task = getattr(state, "holder_task", None) if state is not None else None
            if task is not None and not task.done():
                task.cancel()
                try:
                    loop.run_until_complete(task)
                except BaseException:  # noqa: BLE001 - CancelledError expected
                    pass
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        return ex.submit(_worker).result(timeout=60)


class TestEventLoopRotation:
    """THE production regression (observed on Vercel): the Python runtime
    rotates event loops across invocations of the same warm process. A
    holder bound to a previous loop leaves the session manager's task group
    on a dead loop; /mcp then 500s with 'Internal Server Error' while landing
    pages keep working (static routes never touch the session manager).
    The bootstrap must rebuild the lifespan holder on the new loop."""

    async def test_mcp_survives_event_loop_rotation(self, entry_module):
        # Invocation 1 (loop A): landing page triggers the cold-start bootstrap.
        landing = _invoke_on_fresh_loop(
            entry_module.app, _http_scope("GET", "/")
        )
        assert landing[0]["status"] == 200

        # Invocation 2 (loop B): /mcp initialize on a DIFFERENT loop must be
        # rebuilt and served - not routed to loop A's dead session manager.
        messages = _invoke_on_fresh_loop(
            entry_module.app,
            _http_scope("POST", "/mcp", _INIT_REQUEST),
            _INIT_REQUEST,
        )
        assert messages[0]["status"] == 200, f"messages={messages!r}"
        body = b"".join(
            m.get("body", b"") for m in messages if m["type"] == "http.response.body"
        )
        payload = json.loads(body)
        assert payload["result"]["serverInfo"]["name"] == "agentSAFE"

    async def test_rotation_repeats_across_many_loops(self, entry_module):
        # Warm instance serving N invocations, each on a fresh loop.
        for i in range(3):
            messages = _invoke_on_fresh_loop(
                entry_module.app,
                _http_scope("POST", "/mcp", _INIT_REQUEST),
                _INIT_REQUEST,
            )
            assert messages[0]["status"] == 200, f"invocation {i}: {messages!r}"
