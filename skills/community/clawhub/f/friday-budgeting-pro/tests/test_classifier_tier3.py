"""
tests/test_classifier_tier3.py — Tests for Tier 3: review-flag + auto-promotion (issue #20).

Uses a fresh tmp_path SQLite database initialised with the real schema.
"""

from __future__ import annotations

import sqlite3

import pytest

from server.classifier import flag_for_review, maybe_promote_to_rule
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def seed(conn: sqlite3.Connection) -> dict:
    """Seed minimal data: 1 ledger, 2 line_items. Returns their ids."""
    conn.execute(
        "INSERT INTO ledgers (id, name) VALUES (?, ?)",
        ("ledger-1", "Personal"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-food", "ledger-1", "Food & Drink"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-retail", "ledger-1", "Retail"),
    )
    conn.commit()
    return {"ledger_id": "ledger-1", "li_food": "li-food", "li_retail": "li-retail"}


def insert_transaction(
    conn: sqlite3.Connection, txn_id: str, merchant: str, amount: float = 10.0
) -> None:
    conn.execute(
        "INSERT INTO transactions (id, plaid_transaction_id, date, merchant, amount) "
        "VALUES (?, ?, ?, ?, ?)",
        (txn_id, txn_id + "-plaid", "2024-01-01", merchant, amount),
    )
    conn.commit()


def insert_entry(
    conn: sqlite3.Connection,
    entry_id: str,
    transaction_id: str,
    line_item_id: str,
    source: str = "llm",
    reviewed: int = 1,
    confidence: float = 0.9,
) -> None:
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, confidence, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (entry_id, transaction_id, "ledger-1", line_item_id, 10.0, source, confidence, reviewed),
    )
    conn.commit()


def make_txn(merchant: str, txn_id: str = "txn-incoming") -> dict:
    return {"id": txn_id, "merchant": merchant, "amount": 42.00}


def make_llm_result(line_item_id: str, confidence: float = 0.9) -> dict:
    return {
        "transaction_id": "txn-incoming",
        "ledger_id": "ledger-1",
        "line_item_id": line_item_id,
        "amount": 42.00,
        "source": "llm",
        "confidence": confidence,
        "reviewed": 0,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    conn = get_db(db_path)
    seed(conn)
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# flag_for_review tests
# ---------------------------------------------------------------------------


class TestFlagForReview:
    def test_low_confidence_flagged(self, db):
        """Confidence below threshold → source becomes 'llm-needs-review'."""
        txn = make_txn("Starbucks")
        llm_result = make_llm_result("li-food", confidence=0.5)
        result = flag_for_review(txn, llm_result, threshold=0.75)
        assert result["source"] == "llm-needs-review"
        assert result["reviewed"] == 0

    def test_high_confidence_unchanged(self, db):
        """Confidence above threshold → entry returned unchanged (source='llm')."""
        txn = make_txn("Starbucks")
        llm_result = make_llm_result("li-food", confidence=0.9)
        result = flag_for_review(txn, llm_result, threshold=0.75)
        assert result["source"] == "llm"
        assert result["reviewed"] == 0

    def test_exact_threshold_is_high_path(self, db):
        """Confidence exactly at threshold → high path (>= threshold, unchanged)."""
        txn = make_txn("Starbucks")
        llm_result = make_llm_result("li-food", confidence=0.75)
        result = flag_for_review(txn, llm_result, threshold=0.75)
        assert result["source"] == "llm"
        assert result["reviewed"] == 0

    def test_pure_no_mutation(self, db):
        """flag_for_review must not mutate the original llm_result dict."""
        txn = make_txn("Starbucks")
        llm_result = make_llm_result("li-food", confidence=0.5)
        original_source = llm_result["source"]
        flag_for_review(txn, llm_result)
        # original should be untouched
        assert llm_result["source"] == original_source


# ---------------------------------------------------------------------------
# maybe_promote_to_rule tests
# ---------------------------------------------------------------------------


class TestMaybePromoteToRule:
    def test_zero_prior_entries_returns_none(self, db):
        """No prior reviewed entries → None."""
        txn = make_txn("Whole Foods")
        llm_result = make_llm_result("li-food")
        result = maybe_promote_to_rule(db, txn, llm_result)
        assert result is None

    def test_two_consistent_entries_returns_none(self, db):
        """2 consistent reviewed entries (need 3+) → None."""
        merchant = "Whole Foods"
        for i in range(2):
            tid = f"txn-{i}"
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-{i}", tid, "li-food", source="llm", reviewed=1)

        txn = make_txn(merchant)
        llm_result = make_llm_result("li-food")
        result = maybe_promote_to_rule(db, txn, llm_result)
        assert result is None

    def test_three_consistent_entries_creates_rule(self, db):
        """3 consistent reviewed entries → creates a routing_rule and returns it."""
        merchant = "Whole Foods"
        for i in range(3):
            tid = f"txn-{i}"
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-{i}", tid, "li-food", source="llm", reviewed=1)

        txn = make_txn(merchant)
        llm_result = make_llm_result("li-food")
        result = maybe_promote_to_rule(db, txn, llm_result)

        assert result is not None
        assert result["merchant_pattern"] == merchant
        assert result["line_item_id"] == "li-food"
        assert "id" in result

        # Verify row exists in routing_rules table
        row = db.execute(
            "SELECT id, merchant_pattern, line_item_id FROM routing_rules WHERE id = ?",
            (result["id"],),
        ).fetchone()
        assert row is not None
        assert row[1] == merchant
        assert row[2] == "li-food"

    def test_three_inconsistent_entries_returns_none(self, db):
        """3 reviewed entries but mixed line_item_ids → None."""
        merchant = "Mixed Mart"
        # 2 → li-food, 1 → li-retail (not 3 consistent for either)
        for i in range(2):
            tid = f"txn-food-{i}"
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-food-{i}", tid, "li-food", source="llm", reviewed=1)

        insert_transaction(db, "txn-retail-0", merchant)
        insert_entry(db, "entry-retail-0", "txn-retail-0", "li-retail", source="llm", reviewed=1)

        txn = make_txn(merchant)
        llm_result = make_llm_result("li-food")  # target is li-food but only 2 consistent
        result = maybe_promote_to_rule(db, txn, llm_result)
        assert result is None

    def test_idempotent_existing_rule_returned(self, db):
        """If rule already exists for same (merchant_pattern, line_item_id), return it without duplicate."""
        merchant = "Recurring Cafe"
        existing_id = "rule-existing"
        db.execute(
            "INSERT INTO routing_rules (id, merchant_pattern, line_item_id) VALUES (?, ?, ?)",
            (existing_id, merchant, "li-food"),
        )
        db.commit()

        # Seed 3 consistent reviewed entries
        for i in range(3):
            tid = f"txn-cafe-{i}"
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-cafe-{i}", tid, "li-food", source="llm", reviewed=1)

        txn = make_txn(merchant)
        llm_result = make_llm_result("li-food")
        result = maybe_promote_to_rule(db, txn, llm_result)

        assert result is not None
        assert result["id"] == existing_id

        # Ensure no duplicate was created
        count = db.execute(
            "SELECT COUNT(*) FROM routing_rules WHERE merchant_pattern = ? AND line_item_id = ?",
            (merchant, "li-food"),
        ).fetchone()[0]
        assert count == 1
