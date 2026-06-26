"""
tests/test_classifier_validation.py — Tests for issue #42.

Validates:
  - safe_classify happy-path passes entry through
  - safe_classify with unknown line_item_id → fallback stub (source="llm-rejected")
  - safe_classify with malformed JSON → fallback stub
  - safe_classify with fallback_to_review=False + bad output → raises ValueError
  - classify_with_llm with ledger_id mismatch → raises ValueError
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from server.classifier import classify_with_llm, safe_classify
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Constants / helpers
# ---------------------------------------------------------------------------

LEDGER_ID = "ledger-val"
LEDGER_ID_2 = "ledger-other"
LINE_ITEM_ID = "li-food"
TXN_ID = "txn-val-1"


def seed(conn) -> None:
    """Minimal seed: two ledgers + one line_item each."""
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (LEDGER_ID, "Food"))
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (LEDGER_ID_2, "Transport"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        (LINE_ITEM_ID, LEDGER_ID, "Groceries"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-transit", LEDGER_ID_2, "Transit"),
    )
    # FK chain for transactions
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_access_token_encrypted) VALUES (?, ?)",
        ("conn-val", "placeholder"),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id) VALUES (?, ?)",
        ("acct-val", "conn-val"),
    )
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def make_txn(amount: float = 30.00) -> dict:
    return {
        "id": TXN_ID,
        "merchant": "Loblaws",
        "amount": amount,
        "date": "2025-06-01",
        "bank_account_id": "acct-val",
    }


def llm_json(**kwargs) -> str:
    payload = {
        "line_item_id": LINE_ITEM_ID,
        "confidence": 0.85,
        "reasoning": "Loblaws is a grocery store.",
    }
    payload.update(kwargs)
    return json.dumps(payload)


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def db(tmp_path):
    db_path = tmp_path / "val_test.db"
    init_db(db_path)
    conn = get_db(db_path)
    seed(conn)
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# Tests — safe_classify happy path
# ---------------------------------------------------------------------------


def test_safe_classify_valid_output_passes_through(db):
    """safe_classify with valid LLM output returns the entry unchanged."""
    mock_chat = MagicMock(return_value=llm_json())

    with patch("server.llm.chat", mock_chat):
        result = safe_classify(db, make_txn())

    # Source is set by classify_with_llm; no rejection should occur
    assert result["transaction_id"] == TXN_ID
    assert result["line_item_id"] == LINE_ITEM_ID
    assert result["ledger_id"] == LEDGER_ID
    assert result["source"] in (
        "llm",
        "llm-needs-review",
    ), f"Expected 'llm' or 'llm-needs-review', got {result['source']!r}"
    assert "rejection_reason" not in result


# ---------------------------------------------------------------------------
# Tests — safe_classify fallback paths
# ---------------------------------------------------------------------------


def test_safe_classify_unknown_line_item_id_returns_rejected(db):
    """Unknown line_item_id → fallback stub with source='llm-rejected'."""
    bad_response = llm_json(line_item_id="li-does-not-exist")
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        result = safe_classify(db, make_txn(), fallback_to_review=True)

    assert result["source"] == "llm-rejected"
    assert result["line_item_id"] is None
    assert result["ledger_id"] is None
    assert result["confidence"] == 0.0
    assert result["reviewed"] == 0
    assert result["transaction_id"] == TXN_ID
    assert result["amount"] == 30.00
    assert (
        "unknown line_item_id" in result["rejection_reason"].lower()
        or "does not exist" in result["rejection_reason"].lower()
    ), f"rejection_reason should mention unknown id, got: {result['rejection_reason']!r}"


def test_safe_classify_malformed_json_returns_rejected(db):
    """Malformed LLM JSON → fallback stub with source='llm-rejected'."""
    mock_chat = MagicMock(return_value="this is not json {{{{")

    with patch("server.llm.chat", mock_chat):
        result = safe_classify(db, make_txn(), fallback_to_review=True)

    assert result["source"] == "llm-rejected"
    assert result["line_item_id"] is None
    assert result["ledger_id"] is None
    assert isinstance(result["rejection_reason"], str)
    assert len(result["rejection_reason"]) > 0


def test_safe_classify_fallback_false_reraises(db):
    """With fallback_to_review=False, ValueError should propagate."""
    bad_response = llm_json(line_item_id="li-ghost")
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError):
            safe_classify(db, make_txn(), fallback_to_review=False)


# ---------------------------------------------------------------------------
# Tests — classify_with_llm ledger_id mismatch
# ---------------------------------------------------------------------------


def test_classify_with_llm_ledger_id_mismatch_raises(db):
    """LLM returning a ledger_id that doesn't match the DB lookup → ValueError."""
    # LINE_ITEM_ID belongs to LEDGER_ID ("ledger-val"), but we tell the LLM
    # to return LEDGER_ID_2 ("ledger-other") — that should be rejected.
    bad_response = llm_json(
        line_item_id=LINE_ITEM_ID,
        ledger_id=LEDGER_ID_2,
    )
    mock_chat = MagicMock(return_value=bad_response)

    with patch("server.llm.chat", mock_chat):
        with pytest.raises(ValueError, match="ledger_id mismatch"):
            classify_with_llm(db, make_txn())


def test_classify_with_llm_correct_ledger_id_passes(db):
    """LLM returning the correct ledger_id alongside line_item_id → no error."""
    good_response = llm_json(
        line_item_id=LINE_ITEM_ID,
        ledger_id=LEDGER_ID,  # matches what's in the DB
    )
    mock_chat = MagicMock(return_value=good_response)

    with patch("server.llm.chat", mock_chat):
        result = classify_with_llm(db, make_txn())

    assert result["ledger_id"] == LEDGER_ID
    assert result["line_item_id"] == LINE_ITEM_ID
