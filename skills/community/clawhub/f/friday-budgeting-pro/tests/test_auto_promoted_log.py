"""
tests/test_auto_promoted_log.py — Tests for auto-promoted rules log + undo (issue #43).

Uses a fresh tmp_path SQLite database initialised with the real schema.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

import server.paths
from server.classifier import maybe_promote_to_rule
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
        ("li-dining", "ledger-1", "Dining"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        ("li-retail", "ledger-1", "Retail"),
    )
    conn.commit()
    return {"ledger_id": "ledger-1", "li_dining": "li-dining", "li_retail": "li-retail"}


def insert_transaction(
    conn: sqlite3.Connection,
    txn_id: str,
    merchant: str,
    amount: float = 5.50,
) -> None:
    conn.execute(
        "INSERT INTO transactions (id, plaid_transaction_id, date, merchant, amount) "
        "VALUES (?, ?, ?, ?, ?)",
        (txn_id, txn_id + "-plaid", "2024-06-01", merchant, amount),
    )
    conn.commit()


def insert_entry(
    conn: sqlite3.Connection,
    entry_id: str,
    transaction_id: str,
    line_item_id: str,
    source: str = "manual",
    reviewed: int = 1,
    confidence: float = 1.0,
) -> None:
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, confidence, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (entry_id, transaction_id, "ledger-1", line_item_id, 5.50, source, confidence, reviewed),
    )
    conn.commit()


def make_txn(merchant: str, txn_id: str) -> dict:
    return {"id": txn_id, "merchant": merchant, "amount": 5.50}


def make_llm_result(line_item_id: str) -> dict:
    return {
        "transaction_id": "txn-incoming",
        "ledger_id": "ledger-1",
        "line_item_id": line_item_id,
        "amount": 5.50,
        "source": "llm",
        "confidence": 0.95,
        "reviewed": 0,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db_path(tmp_path):
    """Return a path to a freshly initialised test database."""
    p = tmp_path / "test.db"
    init_db(p)
    return p


@pytest.fixture
def db(db_path):
    conn = get_db(db_path)
    seed(conn)
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# Helpers to call MCP tools against the test DB
# ---------------------------------------------------------------------------


def call_list(monkeypatch, db_path):
    """Call the list_auto_promoted_rules MCP tool with the test DB."""
    monkeypatch.setattr(server.paths, "DB_PATH", db_path)
    from server.main import list_auto_promoted_rules

    return list_auto_promoted_rules()


def call_undo(monkeypatch, db_path, rule_id: str):
    """Call the undo_auto_promoted_rule MCP tool with the test DB."""
    monkeypatch.setattr(server.paths, "DB_PATH", db_path)
    from server.main import undo_auto_promoted_rule

    return undo_auto_promoted_rule(rule_id)


# ---------------------------------------------------------------------------
# Core log-creation tests
# ---------------------------------------------------------------------------


class TestAutoPromotedLog:
    def test_promotion_creates_log_row(self, db, db_path, monkeypatch):
        """3 reviewed manual Starbucks→Dining entries trigger promotion + log row."""
        merchant = "Starbucks"
        txn_ids = [f"txn-star-{i}" for i in range(3)]
        for i, tid in enumerate(txn_ids):
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-star-{i}", tid, "li-dining", source="manual", reviewed=1)

        # Trigger promotion with a 4th Starbucks transaction
        txn4 = make_txn(merchant, "txn-star-3")
        insert_transaction(db, "txn-star-3", merchant)
        result = maybe_promote_to_rule(db, txn4, make_llm_result("li-dining"))

        assert result is not None
        rule_id = result["id"]

        # Verify auto_promoted_rules_log has exactly 1 row
        rows = db.execute(
            "SELECT * FROM auto_promoted_rules_log WHERE rule_id = ?",
            (rule_id,),
        ).fetchall()
        assert len(rows) == 1

        log_row = rows[0]
        assert log_row["merchant"] == merchant
        assert log_row["line_item_id"] == "li-dining"
        assert log_row["rule_id"] == rule_id

        # source_transaction_ids should be JSON array containing the 3 reviewed txn ids
        stored_ids = json.loads(log_row["source_transaction_ids"])
        assert isinstance(stored_ids, list)
        assert len(stored_ids) == 3
        for tid in txn_ids:
            assert tid in stored_ids

    def test_idempotent_no_duplicate_log(self, db, db_path, monkeypatch):
        """Calling maybe_promote_to_rule when rule already exists → no new log row."""
        merchant = "Starbucks"
        txn_ids = [f"txn-sbux-{i}" for i in range(3)]
        for i, tid in enumerate(txn_ids):
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-sbux-{i}", tid, "li-dining", source="manual", reviewed=1)

        txn4 = make_txn(merchant, "txn-sbux-3")
        insert_transaction(db, "txn-sbux-3", merchant)

        # First promotion → creates rule + log row
        result1 = maybe_promote_to_rule(db, txn4, make_llm_result("li-dining"))
        assert result1 is not None

        # Second call → returns existing rule WITHOUT adding another log row
        result2 = maybe_promote_to_rule(db, txn4, make_llm_result("li-dining"))
        assert result2 is not None
        assert result2["id"] == result1["id"]

        count = db.execute(
            "SELECT COUNT(*) FROM auto_promoted_rules_log WHERE rule_id = ?",
            (result1["id"],),
        ).fetchone()[0]
        assert count == 1  # still exactly one row


# ---------------------------------------------------------------------------
# list_auto_promoted_rules tool tests
# ---------------------------------------------------------------------------


class TestListAutoPromotedRules:
    def test_list_returns_active_rule(self, db, db_path, monkeypatch):
        """list_auto_promoted_rules returns 1 row with rule_still_active=True."""
        merchant = "Starbucks"
        txn_ids = [f"txn-list-{i}" for i in range(3)]
        for i, tid in enumerate(txn_ids):
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-list-{i}", tid, "li-dining", source="manual", reviewed=1)

        txn4 = make_txn(merchant, "txn-list-3")
        insert_transaction(db, "txn-list-3", merchant)
        rule = maybe_promote_to_rule(db, txn4, make_llm_result("li-dining"))
        assert rule is not None

        response = call_list(monkeypatch, db_path)
        assert "rules" in response
        matching = [r for r in response["rules"] if r["rule_id"] == rule["id"]]
        assert len(matching) == 1

        entry = matching[0]
        assert entry["merchant"] == merchant
        assert entry["line_item_id"] == "li-dining"
        assert entry["rule_still_active"] is True
        assert isinstance(entry["source_transaction_ids"], list)
        assert len(entry["source_transaction_ids"]) == 3
        for tid in txn_ids:
            assert tid in entry["source_transaction_ids"]

    def test_list_empty_when_no_promotions(self, db, db_path, monkeypatch):
        """list_auto_promoted_rules returns empty list when no promotions have occurred."""
        response = call_list(monkeypatch, db_path)
        assert response == {"rules": []}


# ---------------------------------------------------------------------------
# undo_auto_promoted_rule tool tests
# ---------------------------------------------------------------------------


class TestUndoAutoPromotedRule:
    def _setup_promoted_rule(self, db, db_path, monkeypatch) -> dict:
        """Helper: seed 3 reviewed manual entries, trigger promotion, return rule dict."""
        merchant = "Starbucks"
        txn_ids = [f"txn-undo-{i}" for i in range(3)]
        for i, tid in enumerate(txn_ids):
            insert_transaction(db, tid, merchant)
            insert_entry(db, f"entry-undo-{i}", tid, "li-dining", source="manual", reviewed=1)

        txn4 = make_txn(merchant, "txn-undo-3")
        insert_transaction(db, "txn-undo-3", merchant)
        rule = maybe_promote_to_rule(db, txn4, make_llm_result("li-dining"))
        assert rule is not None
        return rule

    def test_undo_deletes_rule_and_log(self, db, db_path, monkeypatch):
        """undo_auto_promoted_rule deletes the rule; CASCADE removes log row."""
        rule = self._setup_promoted_rule(db, db_path, monkeypatch)
        rule_id = rule["id"]

        response = call_undo(monkeypatch, db_path, rule_id)
        assert response["ok"] is True
        assert response["rule_deleted"] is True

        # routing_rule should be gone
        rr_row = db.execute("SELECT id FROM routing_rules WHERE id = ?", (rule_id,)).fetchone()
        assert rr_row is None

        # auto_promoted_rules_log row should be CASCADE-deleted
        log_rows = db.execute(
            "SELECT id FROM auto_promoted_rules_log WHERE rule_id = ?", (rule_id,)
        ).fetchall()
        assert len(log_rows) == 0

    def test_undo_reverts_entries_reviewed_flag(self, db, db_path, monkeypatch):
        """undo reverts reviewed=1 → 0 for rule-sourced entries with matching merchant."""
        merchant = "Starbucks"
        rule = self._setup_promoted_rule(db, db_path, monkeypatch)
        rule_id = rule["id"]

        # Add a transaction_entry sourced from the rule (simulating auto-classification)
        insert_transaction(db, "txn-rule-sourced", merchant)
        insert_entry(
            db,
            "entry-rule-sourced",
            "txn-rule-sourced",
            "li-dining",
            source="rule",
            reviewed=1,
        )

        response = call_undo(monkeypatch, db_path, rule_id)
        assert response["ok"] is True
        assert response["entries_reverted"] >= 1

        # The rule-sourced entry should now have reviewed=0
        row = db.execute(
            "SELECT reviewed FROM transaction_entries WHERE id = ?",
            ("entry-rule-sourced",),
        ).fetchone()
        assert row["reviewed"] == 0

    def test_undo_missing_rule_returns_not_deleted(self, db, db_path, monkeypatch):
        """undo on a non-existent rule_id returns {ok: True, rule_deleted: False, entries_reverted: 0}."""
        response = call_undo(monkeypatch, db_path, "nonexistent-rule-id")
        assert response == {"ok": True, "rule_deleted": False, "entries_reverted": 0}

    def test_undo_rule_still_active_reflects_in_list(self, db, db_path, monkeypatch):
        """After undo, list_auto_promoted_rules shows rule_still_active=False (or rule absent)."""
        rule = self._setup_promoted_rule(db, db_path, monkeypatch)
        rule_id = rule["id"]

        # Undo the rule
        call_undo(monkeypatch, db_path, rule_id)

        # The log row is CASCADE-deleted, so listing should show no entry for this rule
        response = call_list(monkeypatch, db_path)
        matching = [r for r in response["rules"] if r["rule_id"] == rule_id]
        assert len(matching) == 0
