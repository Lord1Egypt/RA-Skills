"""Minimal live smoke tests for boss-cli.

These tests exercise a tiny set of high-signal commands against the
live Boss Zhipin API using your local saved cookies. They are skipped
by default and only run when explicitly requested::

    uv run pytest tests/test_smoke.py -v -m smoke

The suite intentionally stays small to reduce anti-bot invalidation
and keep release verification stable.
"""

from __future__ import annotations

import json
import re
import time

import pytest
from click.testing import CliRunner

from boss_cli.cli import cli

smoke = pytest.mark.smoke

runner = CliRunner()
_LAST_INVOKE_AT = 0.0
_SMOKE_INVOKE_DELAY_S = 1.2


def _throttle_live_requests() -> None:
    """Pace live API calls to reduce anti-bot invalidation during smoke tests."""
    global _LAST_INVOKE_AT
    elapsed = time.time() - _LAST_INVOKE_AT
    if _LAST_INVOKE_AT and elapsed < _SMOKE_INVOKE_DELAY_S:
        time.sleep(_SMOKE_INVOKE_DELAY_S - elapsed)
    _LAST_INVOKE_AT = time.time()


def _invoke(*args: str):
    """Run a CLI command and return result."""
    _throttle_live_requests()
    return runner.invoke(cli, list(args))


def _invoke_json(*args: str):
    """Run a CLI command with --json and return (result, parsed_data)."""
    _throttle_live_requests()
    result = runner.invoke(cli, [*args, "--json"])
    if result.exit_code != 0:
        return result, None
    try:
        data = json.loads(result.output)
    except json.JSONDecodeError:
        data = None
    return result, data


def _assert_ok_envelope(data: dict | None) -> dict:
    """Assert the command returned the standard success envelope."""
    assert data is not None
    assert data["ok"] is True
    assert "data" in data
    return data["data"]


@pytest.fixture(scope="module")
def live_auth_status() -> dict | None:
    """Fetch one shared status snapshot for the smoke session."""
    _invoke("login")
    result, data = _invoke_json("status")
    assert result.exit_code == 0
    return data


@pytest.fixture(scope="module")
def require_live_auth(live_auth_status: dict | None) -> None:
    """Skip auth-dependent smoke tests unless the session is truly usable."""
    if not live_auth_status or not live_auth_status.get("search_authenticated"):
        reason = ""
        if live_auth_status:
            reason = live_auth_status.get("reason", "")
        pytest.skip(f"Live auth unavailable: {reason or 'boss status 未通过'}")


@pytest.fixture(scope="module")
def require_recommend_auth(live_auth_status: dict | None) -> None:
    """Skip recommend smoke when only search auth is healthy."""
    if not live_auth_status or not live_auth_status.get("recommend_authenticated"):
        reason = ""
        if live_auth_status:
            reason = live_auth_status.get("reason", "")
        pytest.skip(f"Live recommend unavailable: {reason or 'boss recommend 未通过'}")


@smoke
class TestAuth:
    """Verify authentication is working e2e."""

    def test_status(self):
        result = _invoke("status")
        assert result.exit_code == 0
        assert "已登录" in result.output

    def test_status_json(self):
        result, data = _invoke_json("status")
        assert result.exit_code == 0
        assert data is not None
        assert data["authenticated"] is True
        assert data["cookie_count"] > 0


@smoke
@pytest.mark.usefixtures("require_live_auth")
class TestProfile:
    """Verify profile lookup with a structured response."""

    def test_me_json(self):
        result, data = _invoke_json("me")
        assert result.exit_code == 0
        payload = _assert_ok_envelope(data)
        # Must have at least one of these fields
        assert any(k in payload for k in ("name", "nickName", "account"))

@smoke
@pytest.mark.usefixtures("require_live_auth")
class TestSearch:
    """Verify job search on the live API."""

    def test_search_json(self):
        result, data = _invoke_json("search", "Python", "--city", "全国")
        assert result.exit_code == 0
        payload = _assert_ok_envelope(data)
        assert "jobList" in payload
        assert isinstance(payload.get("jobList", []), list)


@smoke
@pytest.mark.usefixtures("require_live_auth")
class TestRecommend:
    """Verify personalized recommendations on the live API."""

    @pytest.mark.usefixtures("require_recommend_auth")
    def test_recommend_json(self):
        result, data = _invoke_json("recommend")
        assert result.exit_code == 0
        payload = _assert_ok_envelope(data)
        assert isinstance(payload.get("jobList", []), list)


@smoke
class TestCities:
    """Verify local non-network command coverage remains intact."""

    def test_cities(self):
        result = _invoke("cities")
        assert result.exit_code == 0
        assert "北京" in result.output
        assert "上海" in result.output
        assert "杭州" in result.output
        assert "深圳" in result.output

    def test_cities_has_codes(self):
        result = _invoke("cities")
        # Should contain at least one city code (digits)
        assert re.search(r"\d{9}", result.output)
