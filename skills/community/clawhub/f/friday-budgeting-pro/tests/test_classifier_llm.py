"""
tests/test_classifier_llm.py — Tests for Tier 2 LLM classifier (issue #19).

Uses a fresh tmp_path SQLite database initialised with the real schema.
server.llm.chat is patched so no real API calls are made.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from server.classifier import classify_with_llm
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

LEDGER_ID = "ledger-test"
LINE_ITEM_ID = "li-groceries"
TXN_ID = "txn-42"


def seed(conn) -> None:
    """Seed ledger, line_items, hints, and reviewed transaction_entries."""
    # Ledger + line items
    conn.execute(
        "INSERT INTO ledgers (id, name) VALUES (?, ?)",
        (LEDGER_ID, "Household"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        (LINE_ITEM_ID, LEDGER_ID, "Groceries"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-dining", LEDGER_ID, "Dining Out"),
    )

    # Classification hints
    conn.execute(
        "INSERT INTO classification_hints (id, text) VALUES (?, ?)",
        ("hint-1", "Supermarkets and grocery stores go under Groceries."),
    )
    conn.execute(
        "INSERT INTO classification_hints (id, text) VALUES (?, ?)",
        ("hint-2", "Restaurants and cafes go under Dining Out."),
    )

    # Seed the FK chain: bank_connections → bank_accounts → transactions
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_access_token_encrypted) VALUES (?, ?)",
        ("conn-x", "encrypted-token-placeholder"),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id) VALUES (?, ?)",
        ("acct-x", "conn-x"),
    )

    # Two reviewed historical entries for the same merchant
    for i, txn_id in enumerate(("txn-hist-1", "txn-hist-2")):
        conn.execute(
            "INSERT INTO transactions (id, bank_account_id, date, merchant, amount)"
            " VALUES (?, ?, ?, ?, ?)",
            (txn_id, "acct-x", f"2025-01-0{i + 1}", "Whole Foods Market", 55.00 + i),
        )
        conn.execute(
            "INSERT INTO transaction_entries"
            " (id, transaction_id, ledger_id, line_item_id, amount, source, confidence, reviewed)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                f"te-hist-{i}",
                txn_id,
                LEDGER_ID,
                LINE_ITEM_ID,
                55.00 + i,
                "manual",
                1.0,
                1,
            ),
        )

    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def make_txn(merchant: str = "Whole Foods Market", amount: float = 42.50) -> dict:
    return {
        "id": TXN_ID,
        "merchant": merchant,
        "amount": amount,
        "date": "2025-03-15",
        "bank_account_id": "acct-x",
    }


def valid_llm_response(line_item_id: str = LINE_ITEM_ID) -> str:
    return json.dumps(
        {
            "line_item_id": line_item_id,
            "confidence": 0.87,
            "reasoning": "Whole Foods is a supermarket.",
        }
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    conn = get_db(db_path)
    seed(conn)
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_classify_with_llm_returns_correct_entry(db):
    """classify_with_llm returns expected dict when LLM gives valid JSON."""
    mock_chat = MagicMock(return_value=valid_llm_response())

    with patch("server.llm.chat", mock_chat):
        result = classify_with_llm(db, make_txn())

    assert result["transaction_id"] == TXN_ID
    assert result["line_item_id"] == LINE_ITEM_ID
    assert result["ledger_id"] == LEDGER_ID
    assert result["amount"] == 42.50
    assert result["source"] == "llm"
    assert result["confidence"] == pytest.approx(0.87)
    assert result["reviewed"] == 0


def test_prompt_contains_ledger_tree(db):
    """The messages passed to chat include the full ledger tree."""
    mock_chat = MagicMock(return_value=valid_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_llm(db, make_txn())

    # Reconstruct prompt from call args
    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)

    assert "Household" in full_prompt, "Ledger name should appear in prompt"
    assert "Groceries" in full_prompt, "Line item name should appear in prompt"
    assert LINE_ITEM_ID in full_prompt, "Line item id should appear in prompt"


def test_prompt_contains_hints(db):
    """The messages passed to chat include classification hints."""
    mock_chat = MagicMock(return_value=valid_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_llm(db, make_txn())

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)

    assert "Supermarkets and grocery stores" in full_prompt
    assert "Restaurants and cafes" in full_prompt


def test_prompt_contains_recent_similar_transactions(db):
    """The messages passed to chat include recent reviewed txns for merchant."""
    mock_chat = MagicMock(return_value=valid_llm_response())

    with patch("server.llm.chat", mock_chat):
        classify_with_llm(db, make_txn())

    messages = mock_chat.call_args[0][0]
    full_prompt = " ".join(m["content"] for m in messages)

    # Both historical entries share the same merchant; at least one date should appear
    assert "Whole Foods Market" in full_prompt
    assert "2025-01-01" in full_prompt or "2025-01-02" in full_prompt


def test_malformed_json_raises(db):
    """classify_with_llm raises ValueError when LLM returns non-JSON."""
    mock_chat = MagicMock(return_value="not valid json at all")

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="non-JSON"):
            classify_with_llm(db, make_txn())


def test_unknown_line_item_id_raises(db):
    """classify_with_llm raises ValueError when LLM returns unknown line_item_id."""
    bad_response = json.dumps(
        {
            "line_item_id": "li-does-not-exist",
            "confidence": 0.5,
            "reasoning": "I guessed.",
        }
    )
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="does not exist"):
            classify_with_llm(db, make_txn())


def test_missing_line_item_id_key_raises(db):
    """classify_with_llm raises ValueError when 'line_item_id' key is absent."""
    bad_response = json.dumps({"confidence": 0.9, "reasoning": "oops"})
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="missing 'line_item_id'"):
            classify_with_llm(db, make_txn())
