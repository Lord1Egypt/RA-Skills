import json
from unittest.mock import MagicMock, patch, call

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FAKE_RESULTS = json.dumps([
    {
        "title": "Chase Sapphire Preferred Review",
        "link": "https://creditcards.chase.com/sapphire-preferred",
        "snippet": "Earn 3x on dining, 2x on travel. $95 annual fee. 60,000 point welcome bonus.",
    },
    {
        "title": "Chase Sapphire Preferred — NerdWallet",
        "link": "https://www.nerdwallet.com/reviews/credit-cards/chase-sapphire-preferred",
        "snippet": "Our top pick for travel rewards. High earn rate on dining and travel.",
    },
])


def _make_mock_wrapper(return_value: str = FAKE_RESULTS):
    wrapper = MagicMock()
    wrapper.run.return_value = return_value
    wrapper._search.return_value = json.loads(return_value)
    return wrapper


def _make_tools(wrapper=None, recent_wrapper=None):
    """Build tools with injected mock wrappers."""
    if wrapper is None:
        wrapper = _make_mock_wrapper()
    if recent_wrapper is None:
        recent_wrapper = _make_mock_wrapper()

    with patch("tools.credit_card_tools.build_brave_wrapper") as mock_build:
        mock_build.side_effect = [wrapper, recent_wrapper]
        from tools.credit_card_tools import build_tools
        return build_tools("fake-key"), wrapper, recent_wrapper


# ---------------------------------------------------------------------------
# Tool existence checks
# ---------------------------------------------------------------------------

def test_build_tools_returns_nine_tools():
    tools, _, _ = _make_tools()
    assert len(tools) == 9


def test_all_tool_names_present():
    tools, _, _ = _make_tools()
    names = {t.name for t in tools}
    expected = {
        "search_card_full_report",
        "search_card_earning_rates",
        "search_transfer_partners",
        "search_statement_credits",
        "calculate_first_year_roi",
        "compare_cards",
        "analyze_wallet",
        "search_recent_changes",
        "recommend_cards_for_profile",
    }
    assert names == expected


# ---------------------------------------------------------------------------
# Individual tool behaviour
# ---------------------------------------------------------------------------

def _get_tool(tools, name):
    return next(t for t in tools if t.name == name)


def test_search_card_full_report_returns_string():
    tools, wrapper, _ = _make_tools()
    result = _get_tool(tools, "search_card_full_report").run("Chase Sapphire Preferred")
    assert isinstance(result, str)
    assert len(result) > 0


def test_search_card_earning_rates_returns_string():
    tools, wrapper, _ = _make_tools()
    result = _get_tool(tools, "search_card_earning_rates").run(
        {"card_name": "Chase Sapphire Preferred", "category": "dining"}
    )
    assert isinstance(result, str)


def test_search_transfer_partners_returns_string():
    tools, wrapper, _ = _make_tools()
    result = _get_tool(tools, "search_transfer_partners").run("Capital One Venture X")
    assert isinstance(result, str)


def test_search_statement_credits_returns_string():
    tools, wrapper, _ = _make_tools()
    result = _get_tool(tools, "search_statement_credits").run("Amex Platinum")
    assert isinstance(result, str)


def test_compare_cards_calls_wrapper_twice():
    tools, wrapper, _ = _make_tools()
    _get_tool(tools, "compare_cards").run({"card_a": "Chase Sapphire Preferred", "card_b": "Amex Gold"})
    assert wrapper._search.call_count == 2 or wrapper.run.call_count == 2


def test_compare_cards_result_contains_both_card_names():
    tools, _, _ = _make_tools()
    result = _get_tool(tools, "compare_cards").run(
        {"card_a": "Chase Sapphire Preferred", "card_b": "Amex Gold"}
    )
    assert "Chase Sapphire Preferred" in result
    assert "Amex Gold" in result


def test_analyze_wallet_returns_string():
    tools, _, _ = _make_tools()
    result = _get_tool(tools, "analyze_wallet").run(
        {"cards_owned": "Chase Sapphire Preferred, Amex Blue Cash Preferred"}
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_analyze_wallet_searches_each_card():
    tools, wrapper, _ = _make_tools()
    _get_tool(tools, "analyze_wallet").run(
        {"cards_owned": "Chase Sapphire Preferred, Amex Gold, Capital One Venture X"}
    )
    # Should make one search per card (3 cards)
    total_calls = wrapper._search.call_count + wrapper.run.call_count
    assert total_calls == 3


def test_search_recent_changes_uses_recent_wrapper():
    tools, main_wrapper, recent_wrapper = _make_tools()
    _get_tool(tools, "search_recent_changes").run("Amex Gold")
    # recent_wrapper should have been called, not main_wrapper
    assert recent_wrapper._search.called or recent_wrapper.run.called


def test_calculate_first_year_roi_contains_spend_summary():
    tools, _, _ = _make_tools()
    result = _get_tool(tools, "calculate_first_year_roi").run({
        "card_name": "Chase Sapphire Preferred",
        "monthly_spend_travel": 500,
        "monthly_spend_dining": 300,
        "monthly_spend_other": 1000,
    })
    assert "$6,000" in result or "6,000" in result  # annual travel = $6k
    assert "3,600" in result or "$3,600" in result  # annual dining = $3.6k


def test_recommend_cards_for_profile_returns_string():
    tools, _, _ = _make_tools()
    result = _get_tool(tools, "recommend_cards_for_profile").run({
        "spending_profile": "high dining and travel",
        "preferences": "no annual fee",
    })
    assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Integration smoke test (skipped without BRAVE_API_KEY)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_integration_search_card_full_report():
    import os
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        pytest.skip("BRAVE_API_KEY not set")

    from tools.credit_card_tools import build_tools
    tools = build_tools(api_key)
    tool = next(t for t in tools if t.name == "search_card_full_report")
    result = tool.run("Chase Sapphire Preferred")

    assert isinstance(result, str)
    assert len(result) > 50
    assert any(kw in result.lower() for kw in ["annual", "fee", "points", "reward"])
