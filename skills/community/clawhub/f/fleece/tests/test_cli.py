"""
Tests for cli.py using typer.testing.CliRunner.

All Brave Search calls are mocked — no network required.
"""
import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from cli import app

runner = CliRunner()

FAKE_RESULT = "Chase Sapphire Preferred | $95 annual fee | 3x dining, 2x travel"


def _mock_search(monkeypatch, return_value: str = FAKE_RESULT):
    """Patch search_and_format and build_brave_wrapper for all CLI tests."""
    mock_wrapper = MagicMock()
    monkeypatch.setenv("BRAVE_API_KEY", "test-key")
    monkeypatch.setattr("tools.brave_client.build_brave_wrapper", lambda *a, **kw: mock_wrapper)
    monkeypatch.setattr("tools.brave_client.search_and_format", lambda *a, **kw: return_value)
    return mock_wrapper


# ---------------------------------------------------------------------------
# card
# ---------------------------------------------------------------------------

class TestCardCommand:
    def test_plain_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["card", "Chase Sapphire Preferred"])
        assert result.exit_code == 0
        assert FAKE_RESULT in result.output

    def test_json_output_shape(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["card", "Chase Sapphire Preferred", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["ok"] is True
        assert data["command"] == "card"
        assert data["result"] == FAKE_RESULT
        assert data["error"] is None

    def test_missing_api_key_exits_code_2(self, monkeypatch):
        monkeypatch.delenv("BRAVE_API_KEY", raising=False)
        monkeypatch.setattr("cli.load_dotenv", lambda: None)
        result = runner.invoke(app, ["card", "Chase Sapphire Preferred", "--no-dotenv"])
        assert result.exit_code == 2
        err = json.loads(result.output)
        assert err["ok"] is False

    def test_search_error_exits_code_1(self, monkeypatch):
        monkeypatch.setenv("BRAVE_API_KEY", "test-key")
        monkeypatch.setattr("tools.brave_client.build_brave_wrapper", lambda *a, **kw: MagicMock())
        monkeypatch.setattr("tools.brave_client.search_and_format", MagicMock(side_effect=Exception("HTTP 429")))
        result = runner.invoke(app, ["card", "Chase Sapphire Preferred"])
        assert result.exit_code == 1
        err = json.loads(result.output)
        assert err["ok"] is False
        assert "HTTP 429" in err["error"]

    def test_stdin_input(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["card", "-"], input="Amex Gold\n")
        assert result.exit_code == 0
        assert FAKE_RESULT in result.output


# ---------------------------------------------------------------------------
# rates
# ---------------------------------------------------------------------------

class TestRatesCommand:
    def test_plain_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["rates", "Amex Gold"])
        assert result.exit_code == 0
        assert FAKE_RESULT in result.output

    def test_with_category_flag(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["rates", "Amex Gold", "--category", "dining"])
        assert result.exit_code == 0

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["rates", "Amex Gold", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "rates"
        assert data["ok"] is True


# ---------------------------------------------------------------------------
# partners
# ---------------------------------------------------------------------------

class TestPartnersCommand:
    def test_plain_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["partners", "Capital One Venture X"])
        assert result.exit_code == 0

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["partners", "Capital One Venture X", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "partners"


# ---------------------------------------------------------------------------
# credits
# ---------------------------------------------------------------------------

class TestCreditsCommand:
    def test_plain_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["credits", "Amex Platinum"])
        assert result.exit_code == 0

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["credits", "Amex Platinum", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "credits"


# ---------------------------------------------------------------------------
# news
# ---------------------------------------------------------------------------

class TestNewsCommand:
    def test_uses_freshness_wrapper(self, monkeypatch):
        """news command should request freshness='pm'."""
        calls = []
        monkeypatch.setenv("BRAVE_API_KEY", "test-key")

        def capturing_build(key, freshness=None, **kw):
            calls.append(freshness)
            return MagicMock()

        monkeypatch.setattr("tools.brave_client.build_brave_wrapper", capturing_build)
        monkeypatch.setattr("tools.brave_client.search_and_format", lambda *a, **kw: FAKE_RESULT)
        result = runner.invoke(app, ["news", "Amex Gold"])
        assert result.exit_code == 0
        assert "pm" in calls

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["news", "Amex Gold", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "news"


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------

class TestCompareCommand:
    def test_output_contains_both_card_names(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["compare", "Amex Gold", "Chase Sapphire Preferred"])
        assert result.exit_code == 0
        assert "Amex Gold" in result.output
        assert "Chase Sapphire Preferred" in result.output

    def test_calls_search_twice(self, monkeypatch):
        monkeypatch.setenv("BRAVE_API_KEY", "test-key")
        monkeypatch.setattr("tools.brave_client.build_brave_wrapper", lambda *a, **kw: MagicMock())
        call_count = 0

        def counting_search(*a, **kw):
            nonlocal call_count
            call_count += 1
            return FAKE_RESULT

        monkeypatch.setattr("tools.brave_client.search_and_format", counting_search)
        runner.invoke(app, ["compare", "Amex Gold", "Chase Sapphire Preferred"])
        assert call_count == 2

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["compare", "Amex Gold", "Chase Sapphire Preferred", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "compare"
        assert data["ok"] is True


# ---------------------------------------------------------------------------
# wallet
# ---------------------------------------------------------------------------

class TestWalletCommand:
    def test_multiple_cards(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["wallet", "Amex Platinum", "Chase Freedom Unlimited"])
        assert result.exit_code == 0
        assert "Amex Platinum" in result.output
        assert "Chase Freedom Unlimited" in result.output

    def test_searches_each_card(self, monkeypatch):
        monkeypatch.setenv("BRAVE_API_KEY", "test-key")
        monkeypatch.setattr("tools.brave_client.build_brave_wrapper", lambda *a, **kw: MagicMock())
        call_count = 0

        def counting_search(*a, **kw):
            nonlocal call_count
            call_count += 1
            return FAKE_RESULT

        monkeypatch.setattr("tools.brave_client.search_and_format", counting_search)
        runner.invoke(app, ["wallet", "Card A", "Card B", "Card C"])
        assert call_count == 3

    def test_stdin_newline_delimited(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["wallet", "-"], input="Amex Gold\nChase Sapphire Preferred\n")
        assert result.exit_code == 0
        assert "Amex Gold" in result.output
        assert "Chase Sapphire Preferred" in result.output

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["wallet", "Amex Platinum", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "wallet"


# ---------------------------------------------------------------------------
# roi
# ---------------------------------------------------------------------------

class TestRoiCommand:
    def test_contains_spend_summary(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, [
            "roi", "Chase Sapphire Preferred",
            "--travel", "500", "--dining", "300", "--other", "1000",
        ])
        assert result.exit_code == 0
        assert "6,000" in result.output  # travel * 12
        assert "3,600" in result.output  # dining * 12

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["roi", "Chase Sapphire Preferred", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "roi"
        assert data["ok"] is True

    def test_defaults_zero_spend(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["roi", "Chase Sapphire Preferred"])
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# recommend
# ---------------------------------------------------------------------------

class TestRecommendCommand:
    def test_plain_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["recommend", "high dining and travel spend"])
        assert result.exit_code == 0

    def test_with_preferences(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["recommend", "high dining", "--preferences", "no annual fee"])
        assert result.exit_code == 0

    def test_json_output(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["recommend", "high dining", "--json"])
        data = json.loads(result.output)
        assert data["command"] == "recommend"

    def test_stdin_input(self, monkeypatch):
        _mock_search(monkeypatch)
        result = runner.invoke(app, ["recommend", "-"], input="heavy travel spender\n")
        assert result.exit_code == 0
