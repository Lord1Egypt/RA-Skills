"""
tests/test_classifier_v2.py — Tests for the Tier-1 v2 LLM classifier.

Covers classify_with_rules() from server.classifier (issue #170).

All tests mock server.llm.chat so no real API calls are made.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from server.classifier import classify_with_rules

# ---------------------------------------------------------------------------
# Helpers — canned LLM responses
# ---------------------------------------------------------------------------

INVESTMENT_RULE_ID = "rule-investment"
INVESTMENT_LINE_ITEM_ID = "li-invest"

PENDING_RULE_ID = "rule-pending"

SALARY_RULE_ID = "rule-salary"


def _llm_response(**kwargs) -> str:
    """Build a JSON string suitable as a mocked chat() return value."""
    defaults = {
        "rule_id": None,
        "line_item_id": None,
        "classification_type": "spending",
        "confidence": 0.9,
        "reasoning": "Test reasoning.",
    }
    defaults.update(kwargs)
    return json.dumps(defaults)


# ---------------------------------------------------------------------------
# Fixtures — sample rule list
# ---------------------------------------------------------------------------

DEFAULT_RULES = [
    {
        "id": PENDING_RULE_ID,
        "name": "Pending skip",
        "description": "Skip any transaction that is still pending",
        "rule_type": "skip",
        "line_item_id": None,
        "priority": 1,
        "is_default": True,
        "enabled": True,
    },
    {
        "id": "rule-transfer",
        "name": "Internal transfer",
        "description": "Same amount leaving one account and arriving at another within 3 days",
        "rule_type": "transfer",
        "line_item_id": None,
        "priority": 10,
        "is_default": True,
        "enabled": True,
    },
    {
        "id": INVESTMENT_RULE_ID,
        "name": "Investment contribution",
        "description": "Outflows to Wealthsimple, Questrade, or any investment platform",
        "rule_type": "transfer",
        "line_item_id": INVESTMENT_LINE_ITEM_ID,
        "priority": 20,
        "is_default": True,
        "enabled": True,
    },
    {
        "id": "rule-cc",
        "name": "Credit card payment",
        "description": "Payment from chequing that matches a credit card balance",
        "rule_type": "transfer",
        "line_item_id": None,
        "priority": 30,
        "is_default": True,
        "enabled": True,
    },
    {
        "id": SALARY_RULE_ID,
        "name": "Salary/payroll",
        "description": "Transactions tagged as payroll or salary by the bank",
        "rule_type": "income",
        "line_item_id": None,
        "priority": 40,
        "is_default": True,
        "enabled": True,
    },
    {
        "id": "rule-fees",
        "name": "Bank fees",
        "description": "Monthly account fees and bank charges",
        "rule_type": "spending",
        "line_item_id": None,
        "priority": 50,
        "is_default": True,
        "enabled": True,
    },
]

WEALTHSIMPLE_TXN = {
    "merchant": "Wealthsimple",
    "amount": 500.0,
    "date": "2026-05-20",
    "account_name": "RBC Chequing",
    "account_description": "Day-to-day chequing account",
    "plaid_category": "TRANSFER_OUT",
}


# ---------------------------------------------------------------------------
# Tests: basic matching
# ---------------------------------------------------------------------------


def test_classify_returns_correct_rule_id_for_match():
    """LLM returns a rule_id that matches → result carries that rule_id."""
    response = _llm_response(
        rule_id=INVESTMENT_RULE_ID,
        line_item_id=INVESTMENT_LINE_ITEM_ID,
        classification_type="transfer",
        confidence=0.95,
        reasoning="Wealthsimple is an investment platform.",
    )
    mock_chat = MagicMock(return_value=response)

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)

    assert result["rule_id"] == INVESTMENT_RULE_ID
    assert result["line_item_id"] == INVESTMENT_LINE_ITEM_ID
    assert result["classification_type"] == "transfer"
    assert result["confidence"] == pytest.approx(0.95)
    assert result["uncertain"] is False
    assert "Wealthsimple" in result["reasoning"] or result["reasoning"]


def test_classify_with_6_default_rules_matches_investment():
    """classify_with_rules with the default 6 rules picks Investment contribution."""
    response = _llm_response(
        rule_id=INVESTMENT_RULE_ID,
        line_item_id=INVESTMENT_LINE_ITEM_ID,
        classification_type="transfer",
        confidence=0.92,
        reasoning="Outflow to Wealthsimple is an investment contribution.",
    )
    mock_chat = MagicMock(return_value=response)

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)

    assert result["rule_id"] == INVESTMENT_RULE_ID
    assert result["classification_type"] == "transfer"
    assert result["uncertain"] is False


def test_prompt_contains_all_rules():
    """The prompt sent to the LLM includes all enabled rules by name."""
    mock_chat = MagicMock(return_value=_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)

    for rule in DEFAULT_RULES:
        assert rule["name"] in full_prompt, f"Rule '{rule['name']}' missing from prompt"


def test_prompt_contains_transaction_details():
    """Merchant, amount, and date appear in the LLM prompt."""
    mock_chat = MagicMock(return_value=_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)

    assert "Wealthsimple" in full_prompt
    assert "2026-05-20" in full_prompt
    assert "500" in full_prompt


# ---------------------------------------------------------------------------
# Tests: disabled / skip rules
# ---------------------------------------------------------------------------


def test_disabled_rule_excluded_from_prompt():
    """A rule with enabled=False must not appear in the prompt."""
    rules_with_disabled = [dict(r, enabled=(r["id"] != INVESTMENT_RULE_ID)) for r in DEFAULT_RULES]
    mock_chat = MagicMock(return_value=_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_rules(WEALTHSIMPLE_TXN, rules_with_disabled)

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)
    # The rule id should not appear in the prompt since it was disabled
    assert INVESTMENT_RULE_ID not in full_prompt


def test_pending_rule_returns_skip_classification_type():
    """When the LLM matches the pending-skip rule, classification_type is 'skip'."""
    response = _llm_response(
        rule_id=PENDING_RULE_ID,
        line_item_id=None,
        classification_type="skip",
        confidence=0.99,
        reasoning="Transaction is still pending.",
    )
    mock_chat = MagicMock(return_value=response)

    pending_txn = {
        "merchant": "Amazon",
        "amount": 29.99,
        "date": "2026-05-20",
        "plaid_category": "PENDING",
    }

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(pending_txn, DEFAULT_RULES)

    assert result["rule_id"] == PENDING_RULE_ID
    assert result["classification_type"] == "skip"


# ---------------------------------------------------------------------------
# Tests: no rule matches
# ---------------------------------------------------------------------------


def test_no_match_returns_none_rule_id():
    """When LLM finds no matching rule, rule_id is None and type is inferred."""
    response = _llm_response(
        rule_id=None,
        line_item_id=None,
        classification_type="spending",
        confidence=0.65,
        reasoning="No rule matched; inferred spending from negative amount.",
    )
    mock_chat = MagicMock(return_value=response)

    txn = {
        "merchant": "Tim Hortons",
        "amount": -4.50,
        "date": "2026-05-20",
        "plaid_category": "FOOD_AND_DRINK",
    }

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(txn, DEFAULT_RULES)

    assert result["rule_id"] is None
    assert result["classification_type"] == "spending"


# ---------------------------------------------------------------------------
# Tests: uncertain flag
# ---------------------------------------------------------------------------


def test_uncertain_true_when_confidence_below_threshold():
    """uncertain=True when LLM confidence < 0.7."""
    response = _llm_response(
        rule_id=None,
        line_item_id=None,
        classification_type="spending",
        confidence=0.5,
        reasoning="Not sure.",
    )
    mock_chat = MagicMock(return_value=response)

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)

    assert result["uncertain"] is True
    assert result["confidence"] == pytest.approx(0.5)


def test_uncertain_false_when_confidence_at_threshold():
    """uncertain=False when LLM confidence == 0.7 (boundary — not below)."""
    response = _llm_response(
        rule_id=INVESTMENT_RULE_ID,
        classification_type="transfer",
        confidence=0.7,
        reasoning="Boundary confidence.",
    )
    mock_chat = MagicMock(return_value=response)

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)

    assert result["uncertain"] is False


# ---------------------------------------------------------------------------
# Tests: context injection
# ---------------------------------------------------------------------------


def test_context_transfer_hint_appears_in_prompt():
    """possible_internal_transfer=True hint shows up in the LLM prompt."""
    mock_chat = MagicMock(return_value=_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_rules(
            WEALTHSIMPLE_TXN,
            DEFAULT_RULES,
            context={"possible_internal_transfer": True},
        )

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)
    assert "transfer" in full_prompt.lower() or "internal" in full_prompt.lower()


def test_context_recent_corrections_appear_in_prompt():
    """recent_corrections are included in the prompt."""
    corrections = [
        {
            "date": "2026-05-01",
            "from_line_item": "Groceries",
            "to_line_item": "Dining Out",
        }
    ]
    mock_chat = MagicMock(return_value=_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_rules(
            WEALTHSIMPLE_TXN,
            DEFAULT_RULES,
            context={"recent_corrections": corrections},
        )

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)
    assert "Groceries" in full_prompt or "Dining Out" in full_prompt


# ---------------------------------------------------------------------------
# Tests: error handling
# ---------------------------------------------------------------------------


def test_raises_on_non_json_response():
    """ValueError raised when LLM returns non-JSON."""
    mock_chat = MagicMock(return_value="not json at all")

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="non-JSON"):
            classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)


def test_raises_on_missing_required_keys():
    """ValueError raised when LLM JSON is missing required keys."""
    bad_response = json.dumps({"confidence": 0.9})
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="missing required keys"):
            classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)


def test_raises_on_invalid_classification_type():
    """ValueError raised when LLM returns an unrecognised classification_type."""
    bad_response = _llm_response(classification_type="unknown_type")
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="unknown classification_type"):
            classify_with_rules(WEALTHSIMPLE_TXN, DEFAULT_RULES)


# ---------------------------------------------------------------------------
# Tests: empty rules list
# ---------------------------------------------------------------------------


def test_empty_rules_list_still_calls_llm():
    """classify_with_rules works with an empty rules list (no rules enabled)."""
    response = _llm_response(
        rule_id=None,
        classification_type="spending",
        confidence=0.6,
        reasoning="No rules defined; inferred from context.",
    )
    mock_chat = MagicMock(return_value=response)

    with patch("server.llm.chat", mock_chat):
        result = classify_with_rules(WEALTHSIMPLE_TXN, [])

    assert mock_chat.called
    assert result["rule_id"] is None
    assert result["classification_type"] == "spending"
