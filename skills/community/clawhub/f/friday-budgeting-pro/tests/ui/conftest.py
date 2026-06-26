"""
tests/ui/conftest.py — Playwright fixtures + skip guard.

All tests in this package are skipped cleanly when Playwright is not
installed, and activate the moment you run:

    pip install playwright
    playwright install chromium

Design notes
────────────
• Skip guards live in pytest_collection_modifyitems (not at module level) so
  that conftest.py loads without error regardless of whether playwright or
  chromium is available.  This is the correct pattern for pytest ≥ 7.
• Fixtures raise pytest.skip() themselves when called without the runtime
  deps, providing a belt-and-suspenders fallback.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.request
from contextlib import closing
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Runtime availability probes (run once at import time — fast checks only)
# ---------------------------------------------------------------------------

try:
    import playwright  # noqa: F401

    _PLAYWRIGHT_INSTALLED = True
except ImportError:
    _PLAYWRIGHT_INSTALLED = False


def _chromium_available() -> bool:
    """Return True only when the chromium binary can actually be launched."""
    if not _PLAYWRIGHT_INSTALLED:
        return False
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
                browser.close()
                return True
            except Exception:
                return False
    except Exception:
        return False


# Evaluated once; cached so collection is fast.
_CHROMIUM_AVAILABLE: bool | None = None  # lazy


def _ensure_chromium_checked() -> bool:
    global _CHROMIUM_AVAILABLE
    if _CHROMIUM_AVAILABLE is None:
        _CHROMIUM_AVAILABLE = _chromium_available()
    return _CHROMIUM_AVAILABLE


def _skip_reason() -> str | None:
    """Return a skip reason string, or None if tests should run."""
    if not _PLAYWRIGHT_INSTALLED:
        return (
            "Playwright not installed. Run: pip install playwright && playwright install chromium"
        )
    if not _ensure_chromium_checked():
        return "Chromium binary not installed. Run: playwright install chromium"
    return None


# ---------------------------------------------------------------------------
# pytest hook: add skip markers to all ui/ items when deps are absent
# ---------------------------------------------------------------------------


def pytest_collection_modifyitems(items: list) -> None:  # type: ignore[type-arg]
    reason = _skip_reason()
    if reason is None:
        return
    skip_mark = pytest.mark.skip(reason=reason)
    for item in items:
        # Only touch items that live under tests/ui/
        if "tests/ui" in str(getattr(item, "fspath", "")):
            item.add_marker(skip_mark)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# Session-scoped server fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def server_url(tmp_path_factory):
    """Start the UI server in a subprocess on a free port, yield URL, clean up.

    Uses tests/ui/_server_runner.py so that server.paths.DB_PATH is patched
    to a fresh temp database before ui.server is imported in the subprocess.
    """
    reason = _skip_reason()
    if reason:
        pytest.skip(reason)

    port = _find_free_port()
    app_dir = tmp_path_factory.mktemp("ui_app")

    env = os.environ.copy()
    env["FRIDAY_BP_APP_DIR"] = str(app_dir)
    env["FRIDAY_BP_UI_PORT"] = str(port)
    env.setdefault("PLAID_CLIENT_ID", "test-client-id")
    env.setdefault("PLAID_SECRET", "test-secret")

    repo_root = Path(__file__).parent.parent.parent
    runner_module = "tests.ui._server_runner"

    proc = subprocess.Popen(
        [sys.executable, "-m", runner_module],
        env=env,
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{url}/healthz", timeout=0.5)
            break
        except Exception:
            if proc.poll() is not None:
                _, err = proc.communicate()
                raise RuntimeError(f"Server process exited early:\n{err.decode()[:1000]}")
            time.sleep(0.25)
    else:
        proc.kill()
        _, err = proc.communicate()
        raise RuntimeError(f"Server failed to start within 15s: {err.decode()[:500]}")

    yield url

    proc.kill()
    proc.wait(timeout=5)


# ---------------------------------------------------------------------------
# Per-test browser fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def browser_context(server_url):  # noqa: ARG001 — ensures server is up
    reason = _skip_reason()
    if reason:
        pytest.skip(reason)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    pg = browser_context.new_page()
    yield pg
    pg.close()
