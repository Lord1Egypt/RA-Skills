#!/usr/bin/env python3
"""End-to-end client contract validation for `cue_api.capabilities()`.

Layer A: spin up the local backend process **via its actual route module**
to exercise the full client path —
url construction, query param serialization, ETag echo + If-None-Match
short-circuit, 4xx structured detail decoding, 304 → None convention.

This runs the real `/api/tools/capabilities` handler in-process and points
``cue_api`` at it via a ``CUE_API_BASE`` env override + a stub ``CUE_API_KEY``.

Use when:
- Touching cue_api.capabilities() signature/parsing
- Touching the backend tool_capabilities / tools-route contract
- Pre-merge gate: catches client/server schema drift before deploying

Run:
    python3 scripts/test_capabilities_client.py
"""

from __future__ import annotations

import os
import sys
import threading
import time
import unittest
import urllib.request
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

# Resolve the backend repo path from CUE_BACKEND_DIR (set it to your local
# backend checkout). This Layer-A test only runs where the backend is present;
# CI and contributors without it skip cleanly.
_backend_env = os.environ.get("CUE_BACKEND_DIR")
_BACKEND_DIR = Path(_backend_env) if _backend_env else None
if not _BACKEND_DIR or not _BACKEND_DIR.exists():
    print("[skip] backend repo not found — set CUE_BACKEND_DIR to run this test", file=sys.stderr)
    sys.exit(0)
sys.path.insert(0, str(_BACKEND_DIR))


def _start_minimal_backend() -> tuple[str, threading.Thread]:
    """Spin up FastAPI on a free port with only the tools router mounted.

    Reuses the same hermetic pattern as the backend's own
    tool-capabilities API test.
    """
    import socket

    try:
        import uvicorn
        from fastapi import FastAPI
    except ImportError as e:
        # codex r2 finding: 默认 sys.exit(0) 让 CI 误以为 contract 测了。
        # 改成默认 exit 2 = "未验证",CI 不会 false-pass。如要在 dev box
        # 跳过(deps 装不全的开发者),显式设 CUE_SKILL_TEST_SKIP_OK=1。
        if os.environ.get("CUE_SKILL_TEST_SKIP_OK") == "1":
            print(
                f"[skip-ok] uvicorn + fastapi missing ({e}) — "
                f"CUE_SKILL_TEST_SKIP_OK=1 set, exiting 0",
                file=sys.stderr,
            )
            sys.exit(0)
        print(
            f"[NOT VERIFIED] capabilities contract not exercised — "
            f"uvicorn + fastapi missing ({e}).\n"
            f"       install: pip install uvicorn fastapi (or run in the backend .venv)\n"
            f"       to silence in non-CI dev env: export CUE_SKILL_TEST_SKIP_OK=1",
            file=sys.stderr,
        )
        sys.exit(2)

    from src.api.routes.tools import router as tools_router  # noqa: E402

    app = FastAPI()
    app.include_router(tools_router)

    # Find a free port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    config = uvicorn.Config(
        app, host="127.0.0.1", port=port, log_level="error", access_log=False
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    # Wait for the server to come up — naive poll
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{base}/openapi.json", timeout=1).read()
            return base, thread
        except Exception:
            time.sleep(0.1)
    raise RuntimeError("minimal backend did not start in 5s")


# Spin up once for the suite
_BASE, _BACKEND_THREAD = _start_minimal_backend()

# Configure cue_api to point at the minimal backend (and bypass real auth —
# the minimal backend doesn't enforce auth_dependency at app-creation time
# since we only mounted the tools router).
# cue_api.DEFAULT_BASE 含 /api(prod 形态);minimal app 没自动加 /api 前缀,
# 本地 base 末尾补 /api 让 URL 命中 router 注册的 /api/tools/capabilities。
os.environ["CUE_API_BASE"] = _BASE + "/api"
os.environ["CUE_API_KEY"] = "sk-test-not-used-by-minimal-backend"

from cue_api import CueAPIError, capabilities  # noqa: E402


class Case1_BareGetAutoSummary(unittest.TestCase):
    """Bare GET (no q/category/fields) → server auto-summary; client gets
    empty tools[] but populated counts/categories/presets."""

    def test_bare_get_empty_tools(self) -> None:
        body = capabilities()
        self.assertIsNotNone(body)
        self.assertEqual(body["tools"], [])
        self.assertEqual(body["query"]["fields"], "summary")
        self.assertGreater(body["counts"]["returned_tools"], 0)
        self.assertGreater(body["counts"]["categories"], 0)
        self.assertGreater(body["counts"]["presets"], 0)


class Case2_FilteredAutoDefault(unittest.TestCase):
    """q= or category= flips to auto-default (tools[] populated)."""

    def test_q_filter_returns_tools(self) -> None:
        body = capabilities(q="公告")
        self.assertGreater(len(body["tools"]), 0)
        self.assertEqual(body["query"]["fields"], "default")
        for t in body["tools"]:
            self.assertIn(
                "公告",
                t["name"] + t["display_name"] + t["category"]
                + t["category_label"] + " ".join(t["triggers"]),
            )

    def test_category_filter_returns_tools(self) -> None:
        body = capabilities(category="disclosure_cn")
        self.assertGreater(len(body["tools"]), 0)
        for t in body["tools"]:
            self.assertEqual(t["category"], "disclosure_cn")


class Case3_ExplicitFullInventory(unittest.TestCase):
    """Explicit fields=default dumps full catalog even without filters."""

    def test_fields_default_explicit_dumps_all(self) -> None:
        body = capabilities(fields="default")
        # Should match catalog size
        self.assertEqual(
            body["counts"]["returned_tools"],
            body["source_counts"]["catalog_tools"],
        )
        self.assertGreater(len(body["tools"]), 100)


class Case4_ETagRoundTrip(unittest.TestCase):
    """Client echoes ETag → server 304 → client returns None."""

    def test_etag_304_returns_none(self) -> None:
        first = capabilities()
        self.assertIn("_etag", first, "server must emit ETag header")
        etag = first["_etag"]
        # Weak validator per RFC 7232 §2.3 (backend emits W/"...")
        self.assertTrue(etag.startswith('W/"'), f"expected weak ETag, got {etag!r}")

        second = capabilities(if_none_match=etag)
        self.assertIsNone(second, "matching ETag should return None (304)")

    def test_etag_changes_when_filter_changes(self) -> None:
        a = capabilities()
        b = capabilities(category="disclosure_cn")
        self.assertNotEqual(a["_etag"], b["_etag"])


class Case5_StructuredErrors(unittest.TestCase):
    """Backend 400s carry structured `detail` dict; client raises CueAPIError
    with the dict serialized in `detail`."""

    def test_unsupported_fields_400(self) -> None:
        with self.assertRaises(CueAPIError) as cm:
            capabilities(fields="bogus")
        self.assertEqual(cm.exception.status, 400)
        self.assertIn("unsupported_fields", cm.exception.detail)


class Case6_MaxTriggersCapApplied(unittest.TestCase):
    """Client max_triggers param flows through query string."""

    def test_max_triggers_2(self) -> None:
        body = capabilities(q="公告", max_triggers=2)
        self.assertEqual(body["query"]["fields"], "default")
        for t in body["tools"]:
            self.assertLessEqual(len(t["triggers"]), 2)


class Case7_NoSecretLikeFieldNames(unittest.TestCase):
    """Smoke: client never sees suspicious-looking keys in tool dicts."""

    def test_no_secret_keys(self) -> None:
        body = capabilities(fields="default")
        forbidden = ("api_key", "secret", "token", "password", "credential")
        for tool in body["tools"]:
            for k in tool:
                self.assertFalse(
                    any(f in k.lower() for f in forbidden),
                    f"suspicious key {k!r} in tool {tool['name']}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
