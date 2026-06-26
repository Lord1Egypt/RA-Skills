"""
tests/test_classifier_unified.py — Tests for the unified classify_transaction()
single-LLM-call classifier introduced by issue #205.

Verifies:
  - Single prompt contains rules + ledger tree + hints + recent entries +
    transfer-hint context + transaction details.
  - Returned dict has the unified shape (rule_id, line_item_id,
    classification_type, confidence, uncertain, reasoning).
  - Uncertain flag tracks the 0.7 confidence threshold.
  - Pre-fetched ledger_tree / hints overrides the DB-lookup path.
  - Bad LLM output raises ValueError.
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from server.classifier import (
    UNCERTAIN_THRESHOLD,
    _build_ledger_tree,
    _fetch_hints,
    classify_transaction,
)
from server.db import get_db, init_db

LEDGER_ID = "ledger-unified"
LI_GROCERIES = "li-groceries-u"
LI_DINING = "li-dining-u"
LI_INCOME = "li-income-u"


def _seed(conn) -> None:
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (LEDGER_ID, "Personal"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (LI_GROCERIES, LEDGER_ID, "Groceries", "expense"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (LI_DINING, LEDGER_ID, "Dining", "expense"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (LI_INCOME, LEDGER_ID, "Salary", "income"),
    )
    conn.execute(
        "INSERT INTO classification_hints (id, text) VALUES (?, ?)",
        ("h1", "Whole Foods is a grocery store."),
    )
    conn.commit()


@pytest.fixture()
def db(tmp_path):
    db_path = tmp_path / "unified.db"
    init_db(db_path)
    conn = get_db(db_path)
    _seed(conn)
    yield conn
    conn.close()


def _txn(**over):
    base = {
        "merchant": "Whole Foods Market",
        "amount": 42.50,
        "date": "2025-03-15",
        "account_name": "Chase Checking",
        "plaid_category": "Food and Drink, Groceries",
    }
    base.update(over)
    return base


def _rule(rid="r1", priority=10, rule_type="spending", line_item_id=None):
    return {
        "id": rid,
        "name": f"Rule {rid}",
        "description": "Test rule",
        "rule_type": rule_type,
        "line_item_id": line_item_id,
        "priority": priority,
        "enabled": True,
    }


def test_unified_returns_full_result_shape(db):
    fake = json.dumps(
        {
            "rule_id": "r1",
            "line_item_id": LI_GROCERIES,
            "classification_type": "spending",
            "confidence": 0.92,
            "reasoning": "Whole Foods is a grocery store.",
        }
    )
    with patch("server.llm.chat", return_value=fake):
        result = classify_transaction(
            db,
            _txn(),
            [_rule(rid="r1", line_item_id=LI_GROCERIES)],
        )

    assert result == {
        "rule_id": "r1",
        "line_item_id": LI_GROCERIES,
        "classification_type": "spending",
        "confidence": 0.92,
        "uncertain": False,
        "reasoning": "Whole Foods is a grocery store.",
    }


def test_unified_prompt_contains_all_sections(db):
    """The single LLM call must include rules + ledger tree + hints + txn."""
    fake = json.dumps(
        {
            "rule_id": None,
            "line_item_id": LI_GROCERIES,
            "classification_type": "spending",
            "confidence": 0.85,
            "reasoning": "ok",
        }
    )
    captured = {}

    def _spy(messages, **kw):
        captured["messages"] = messages
        return fake

    with patch("server.llm.chat", side_effect=_spy):
        classify_transaction(
            db,
            _txn(),
            [_rule(rid="r-1", line_item_id=LI_GROCERIES)],
        )

    assert "messages" in captured, "chat was not called"
    user_msg = captured["messages"][-1]["content"]
    # Each major section header must be present.
    assert "Classification Rules" in user_msg
    assert "Ledger Tree" in user_msg
    assert "Classification Hints" in user_msg
    assert "Recent Reviewed Entries" in user_msg
    assert "Additional Context" in user_msg
    assert "Transaction To Classify" in user_msg

    # Rule, ledger, hint, and transaction-specific tokens are embedded.
    assert "r-1" in user_msg
    assert "Personal" in user_msg
    assert LI_GROCERIES in user_msg
    assert "Whole Foods" in user_msg
    assert "Whole Foods is a grocery store." in user_msg
    assert "Chase Checking" in user_msg


def test_unified_uncertain_threshold(db):
    fake = json.dumps(
        {
            "rule_id": None,
            "line_item_id": LI_GROCERIES,
            "classification_type": "spending",
            "confidence": UNCERTAIN_THRESHOLD - 0.05,
            "reasoning": "unsure",
        }
    )
    with patch("server.llm.chat", return_value=fake):
        result = classify_transaction(db, _txn(), [])
    assert result["uncertain"] is True


def test_unified_transfer_hint_included(db):
    fake = json.dumps(
        {
            "rule_id": None,
            "line_item_id": LI_GROCERIES,
            "classification_type": "transfer",
            "confidence": 0.9,
            "reasoning": "transfer",
        }
    )
    captured = {}

    def _spy(messages, **kw):
        captured["messages"] = messages
        return fake

    with patch("server.llm.chat", side_effect=_spy):
        classify_transaction(
            db,
            _txn(),
            [],
            context={"possible_internal_transfer": True},
        )
    user_msg = captured["messages"][-1]["content"]
    assert "internal transfer" in user_msg.lower()


def test_unified_bad_json_raises(db):
    with patch("server.llm.chat", return_value="not json"):
        with pytest.raises(ValueError):
            classify_transaction(db, _txn(), [])


def test_unified_invalid_classification_type_raises(db):
    fake = json.dumps(
        {
            "rule_id": None,
            "line_item_id": None,
            "classification_type": "garbage",
            "confidence": 0.9,
            "reasoning": "x",
        }
    )
    with patch("server.llm.chat", return_value=fake):
        with pytest.raises(ValueError):
            classify_transaction(db, _txn(), [])


def test_prefetched_ledger_tree_and_hints_used(db):
    """Caller can pre-fetch ledger_tree + hints to amortize across many txns."""
    fake = json.dumps(
        {
            "rule_id": None,
            "line_item_id": LI_GROCERIES,
            "classification_type": "spending",
            "confidence": 0.9,
            "reasoning": "x",
        }
    )
    pre_tree = "  Ledger: Custom (id=cust)\n    - Custom item (id=ci-1)"
    pre_hints = ["Custom hint A", "Custom hint B"]
    captured = {}

    def _spy(messages, **kw):
        captured["messages"] = messages
        return fake

    with patch("server.llm.chat", side_effect=_spy):
        classify_transaction(
            db,
            _txn(),
            [],
            ledger_tree=pre_tree,
            hints=pre_hints,
        )
    user_msg = captured["messages"][-1]["content"]
    assert "Custom item" in user_msg
    assert "Custom hint A" in user_msg
    # The DB-side hint must NOT appear when caller pre-supplied hints.
    assert "Whole Foods is a grocery store." not in user_msg


def test_build_ledger_tree_helper(db):
    tree = _build_ledger_tree(db)
    assert "Personal" in tree
    assert "Groceries" in tree
    assert "Dining" in tree


def test_fetch_hints_helper(db):
    hints = _fetch_hints(db)
    assert hints == ["Whole Foods is a grocery store."]
