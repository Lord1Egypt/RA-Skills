"""
tests/test_classifier_rules.py — Tests for Tier 1 rules engine (issue #18).

Uses a fresh tmp_path SQLite database initialised with the real schema.
"""

from __future__ import annotations

import sqlite3

import pytest

from server.classifier import apply_rules
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def seed(conn: sqlite3.Connection) -> dict:
    """Seed a minimal dataset and return the inserted ids."""
    conn.execute(
        "INSERT INTO ledgers (id, name) VALUES (?, ?)",
        ("ledger-1", "Household"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-food", "ledger-1", "Food & Drink"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-retail", "ledger-1", "Retail"),
    )
    conn.execute(
        "INSERT INTO routing_rules (id, merchant_pattern, line_item_id) VALUES (?, ?, ?)",
        ("rule-1", "Starbucks", "li-food"),
    )
    conn.execute(
        "INSERT INTO routing_rules (id, merchant_pattern, line_item_id) VALUES (?, ?, ?)",
        ("rule-2", "Amazon", "li-retail"),
    )
    conn.commit()
    return {"ledger_id": "ledger-1"}


def make_txn(merchant: str, amount: float = 10.00) -> dict:
    return {
        "id": "txn-1",
        "merchant": merchant,
        "amount": amount,
        "bank_account_id": "acct-1",
    }


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


def test_matching_rule_returns_entry(db):
    """apply_rules returns a populated entry dict when the merchant matches."""
    txn = make_txn("Starbucks Coffee", amount=5.50)
    result = apply_rules(db, txn)

    assert result is not None
    assert result["transaction_id"] == "txn-1"
    assert result["ledger_id"] == "ledger-1"
    assert result["line_item_id"] == "li-food"
    assert result["amount"] == 5.50
    assert result["source"] == "rule"
    assert result["confidence"] == 1.0
    assert result["reviewed"] == 0


def test_no_match_returns_none(db):
    """apply_rules returns None when no rule matches the merchant."""
    txn = make_txn("Whole Foods Market")
    result = apply_rules(db, txn)
    assert result is None


def test_case_insensitive_match(db):
    """Pattern 'Starbucks' should match merchant 'STARBUCKS COFFEE'."""
    txn = make_txn("STARBUCKS COFFEE")
    result = apply_rules(db, txn)
    assert result is not None
    assert result["line_item_id"] == "li-food"


def test_first_rule_wins_on_multiple_matches(db):
    """When multiple rules could match, the one with the lowest id wins."""
    # Add a second rule that also matches "Starbucks"
    db.execute(
        "INSERT INTO routing_rules (id, merchant_pattern, line_item_id) VALUES (?, ?, ?)",
        ("rule-0", "Starbucks", "li-retail"),  # id sorts before "rule-1"
    )
    db.commit()

    txn = make_txn("Starbucks Reserve")
    result = apply_rules(db, txn)

    assert result is not None
    # rule-0 < rule-1 lexicographically, so li-retail wins
    assert result["line_item_id"] == "li-retail"


def test_entry_fields_source_confidence_reviewed(db):
    """Returned entry always has source='rule', confidence=1.0, reviewed=0."""
    txn = make_txn("amazon.com")
    result = apply_rules(db, txn)

    assert result is not None
    assert result["source"] == "rule"
    assert result["confidence"] == 1.0
    assert result["reviewed"] == 0
