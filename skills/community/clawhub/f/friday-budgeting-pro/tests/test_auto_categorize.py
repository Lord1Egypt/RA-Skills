"""
tests/test_auto_categorize.py — Tests for auto-categorization of transactions (#165).

Covers:
- classify_pending_transactions: 3 transactions → 3 entries written (mocked LLM)
- Idempotent: running classify_pending_transactions again does not double-write
- classification_type='skip' → no entry written (entry type recorded as skip)
- get_needs_review() returns uncertain transactions
- No active user → graceful no-op (returns all zeros)
- Fallback to default_ledger_id line item when LLM returns no line_item_id
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

from server.db import get_db, init_db
from server.main import classify_pending_transactions, get_needs_review

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _new_id() -> str:
    return str(uuid.uuid4())


def _seed_user(conn, username: str = "testuser") -> str:
    user_id = _new_id()
    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (user_id, username, "hash", int(time.time())),
    )
    conn.commit()
    return user_id


def _seed_connection(conn, user_id: str) -> str:
    conn_id = _new_id()
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_access_token_encrypted, institution_name, user_id, plaid_env) "
        "VALUES (?, ?, ?, ?, ?)",
        (conn_id, "enc", "RBC", user_id, "sandbox"),
    )
    conn.commit()
    return conn_id


def _seed_account(conn, connection_id: str, default_ledger_id: str = None) -> str:
    acct_id = _new_id()
    conn.execute(
        "INSERT INTO bank_accounts "
        "(id, connection_id, plaid_account_id, name, type, default_ledger_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (acct_id, connection_id, _new_id(), "Chequing", "depository", default_ledger_id),
    )
    conn.commit()
    return acct_id


def _seed_ledger(conn, user_id: str, name: str = "Household") -> str:
    ledger_id = _new_id()
    conn.execute(
        "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
        (ledger_id, name, user_id),
    )
    conn.commit()
    return ledger_id


def _seed_line_item(conn, ledger_id: str, name: str, item_type: str = "expense") -> str:
    li_id = _new_id()
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_id, ledger_id, name, item_type),
    )
    conn.commit()
    return li_id


def _seed_transaction(
    conn,
    bank_account_id: str,
    merchant: str = "Starbucks",
    amount: float = 5.50,
    date: str = "2024-01-01",
    pending: int = 0,
) -> str:
    tx_id = _new_id()
    conn.execute(
        "INSERT INTO transactions "
        "(id, bank_account_id, plaid_transaction_id, date, merchant, amount, pending) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (tx_id, bank_account_id, _new_id(), date, merchant, amount, pending),
    )
    conn.commit()
    return tx_id


def _seed_rule(
    conn, name: str, rule_type: str, line_item_id: str = None, priority: int = 10
) -> str:
    rule_id = _new_id()
    conn.execute(
        "INSERT INTO classification_rules "
        "(id, name, description, rule_type, line_item_id, priority, is_default, enabled, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, 0, 1, ?)",
        (rule_id, name, f"Rule for {name}", rule_type, line_item_id, priority, int(time.time())),
    )
    conn.commit()
    return rule_id


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_db(tmp_path: Path, monkeypatch):
    """Create a fresh isolated DB and monkeypatch server.paths.DB_PATH."""
    import server.paths

    db_file = tmp_path / "test.db"
    monkeypatch.setattr(server.paths, "DB_PATH", db_file)
    init_db(db_file)
    return db_file


@pytest.fixture
def db_env(tmp_db):
    """Return (db_file, user_id, account_id, ledger_id, expense_li_id, income_li_id)."""
    conn = get_db(tmp_db)
    try:
        user_id = _seed_user(conn)
        conn_id = _seed_connection(conn, user_id)
        ledger_id = _seed_ledger(conn, user_id)
        expense_li_id = _seed_line_item(conn, ledger_id, "Groceries", "expense")
        income_li_id = _seed_line_item(conn, ledger_id, "Salary", "income")
        acct_id = _seed_account(conn, conn_id, default_ledger_id=ledger_id)
    finally:
        conn.close()
    return {
        "db": tmp_db,
        "user_id": user_id,
        "account_id": acct_id,
        "ledger_id": ledger_id,
        "expense_li_id": expense_li_id,
        "income_li_id": income_li_id,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def _make_llm_response(
    classification_type: str, line_item_id: str = None, confidence: float = 0.9
) -> str:
    import json

    return json.dumps(
        {
            "rule_id": None,
            "line_item_id": line_item_id,
            "classification_type": classification_type,
            "confidence": confidence,
            "reasoning": f"Classified as {classification_type}",
        }
    )


class TestClassifyPendingTransactions:
    def test_classifies_three_transactions(self, db_env):
        """classify_pending_transactions should classify 3 unclassified txns."""
        conn = get_db(db_env["db"])
        try:
            # Seed a rule pointing to the expense line item.
            _seed_rule(conn, "Spending Rule", "spending", db_env["expense_li_id"], priority=10)
            # Insert 3 transactions.
            tx_ids = []
            for i in range(3):
                tx_ids.append(
                    _seed_transaction(
                        conn,
                        db_env["account_id"],
                        merchant=f"Merchant {i}",
                        amount=float(10 + i),
                        date=f"2024-01-0{i + 1}",
                    )
                )
        finally:
            conn.close()

        mock_response = _make_llm_response("spending", db_env["expense_li_id"])

        with (
            patch("server.llm.chat", return_value=mock_response),
            patch("server.main.get_transfer_hint", return_value=None),
        ):
            result = classify_pending_transactions(db_env["user_id"])

        assert result["classified"] == 3
        assert result["skipped"] == 0
        assert result["uncertain"] == 0

        # Verify DB entries were written.
        conn = get_db(db_env["db"])
        try:
            entries = conn.execute("SELECT * FROM transaction_entries").fetchall()
            assert len(entries) == 3
            for entry in entries:
                assert entry["line_item_id"] == db_env["expense_li_id"]
                assert entry["ledger_id"] == db_env["ledger_id"]
                assert entry["source"] == "llm"
        finally:
            conn.close()

    def test_idempotent(self, db_env):
        """Running classify_pending_transactions twice must not double-write."""
        conn = get_db(db_env["db"])
        try:
            _seed_rule(conn, "Spending Rule", "spending", db_env["expense_li_id"], priority=10)
            _seed_transaction(conn, db_env["account_id"])
        finally:
            conn.close()

        mock_response = _make_llm_response("spending", db_env["expense_li_id"])

        with (
            patch("server.llm.chat", return_value=mock_response),
            patch("server.main.get_transfer_hint", return_value=None),
        ):
            first = classify_pending_transactions(db_env["user_id"])
            second = classify_pending_transactions(db_env["user_id"])

        assert first["classified"] == 1
        # Second run should find nothing to classify.
        assert second["classified"] == 0
        assert second["skipped"] == 0
        assert second["uncertain"] == 0

        conn = get_db(db_env["db"])
        try:
            count = conn.execute("SELECT COUNT(*) FROM transaction_entries").fetchone()[0]
            assert count == 1
        finally:
            conn.close()

    def test_skip_classification_type(self, db_env):
        """classification_type='skip' must write a skip entry, not a routing entry."""
        conn = get_db(db_env["db"])
        try:
            _seed_rule(conn, "Skip Rule", "skip", None, priority=5)
            _seed_transaction(conn, db_env["account_id"], merchant="Credit Card Payment")
        finally:
            conn.close()

        mock_response = _make_llm_response("skip", None)

        with (
            patch("server.llm.chat", return_value=mock_response),
            patch("server.main.get_transfer_hint", return_value=None),
        ):
            result = classify_pending_transactions(db_env["user_id"])

        assert result["skipped"] == 1
        assert result["classified"] == 0

        conn = get_db(db_env["db"])
        try:
            entry = conn.execute("SELECT * FROM transaction_entries").fetchone()
            assert entry is not None
            assert entry["entry_type"] == "skip"
            assert entry["line_item_id"] is None
        finally:
            conn.close()

    def test_uncertain_transaction_no_line_item_and_no_default_ledger(self, db_env):
        """When LLM gives no line_item_id and no default_ledger → uncertain."""
        # Remove default_ledger_id from the account.
        conn = get_db(db_env["db"])
        try:
            conn.execute(
                "UPDATE bank_accounts SET default_ledger_id = NULL WHERE id = ?",
                (db_env["account_id"],),
            )
            conn.commit()
            _seed_transaction(conn, db_env["account_id"], merchant="Mystery Merchant")
        finally:
            conn.close()

        mock_response = _make_llm_response("spending", None, confidence=0.4)

        with (
            patch("server.llm.chat", return_value=mock_response),
            patch("server.main.get_transfer_hint", return_value=None),
        ):
            result = classify_pending_transactions(db_env["user_id"])

        assert result["uncertain"] == 1
        assert result["classified"] == 0

    def test_fallback_to_default_ledger_expense(self, db_env):
        """When LLM returns no line_item_id but account has default_ledger_id,
        fallback to first expense line item for 'spending'."""
        conn = get_db(db_env["db"])
        try:
            _seed_transaction(conn, db_env["account_id"], merchant="Unknown Merchant")
        finally:
            conn.close()

        # LLM returns spending but no specific line_item_id.
        mock_response = _make_llm_response("spending", None, confidence=0.85)

        with (
            patch("server.llm.chat", return_value=mock_response),
            patch("server.main.get_transfer_hint", return_value=None),
        ):
            result = classify_pending_transactions(db_env["user_id"])

        # Should be classified via fallback, not uncertain.
        assert result["classified"] == 1
        assert result["uncertain"] == 0

        conn = get_db(db_env["db"])
        try:
            entry = conn.execute("SELECT * FROM transaction_entries").fetchone()
            assert entry["line_item_id"] == db_env["expense_li_id"]
            assert entry["ledger_id"] == db_env["ledger_id"]
        finally:
            conn.close()

    def test_fallback_to_default_ledger_income(self, db_env):
        """When classification_type='income', fallback picks income line item."""
        conn = get_db(db_env["db"])
        try:
            _seed_transaction(conn, db_env["account_id"], merchant="Employer", amount=-2000.0)
        finally:
            conn.close()

        mock_response = _make_llm_response("income", None, confidence=0.92)

        with (
            patch("server.llm.chat", return_value=mock_response),
            patch("server.main.get_transfer_hint", return_value=None),
        ):
            result = classify_pending_transactions(db_env["user_id"])

        assert result["classified"] == 1

        conn = get_db(db_env["db"])
        try:
            entry = conn.execute("SELECT * FROM transaction_entries").fetchone()
            assert entry["line_item_id"] == db_env["income_li_id"]
        finally:
            conn.close()

    def test_no_active_user_graceful_noop(self, tmp_db, monkeypatch):
        """No active user → classify_pending_transactions returns all zeros."""
        result = classify_pending_transactions("")
        assert result == {"classified": 0, "skipped": 0, "uncertain": 0}

    def test_transfer_hint_passed_to_classifier(self, db_env):
        """Transfer hint should be included in the unified classifier context."""
        conn = get_db(db_env["db"])
        try:
            _seed_rule(conn, "Transfer Rule", "transfer", db_env["expense_li_id"], priority=1)
            _seed_transaction(conn, db_env["account_id"], merchant="Transfer To Savings")
        finally:
            conn.close()

        mock_response = _make_llm_response("transfer", db_env["expense_li_id"])

        captured_contexts = []

        # New unified signature (issue #205):
        # classify_transaction(conn, tx_dict, rules, ledger_tree=..., hints=..., context=...)
        def mock_classify(conn_arg, tx_dict, rules, ledger_tree=None, hints=None, context=None):
            captured_contexts.append(context)

            return {
                "rule_id": None,
                "line_item_id": db_env["expense_li_id"],
                "classification_type": "transfer",
                "confidence": 0.9,
                "uncertain": False,
                "reasoning": "Transfer detected",
            }

        hint = {"is_possible_transfer": True, "matched_account": "acct-2", "matched_amount": 50.0}

        with (
            patch("server.main.classify_transaction", side_effect=mock_classify),
            patch("server.main.get_transfer_hint", return_value=hint),
        ):
            classify_pending_transactions(db_env["user_id"])

        assert len(captured_contexts) == 1
        assert captured_contexts[0] is not None
        assert captured_contexts[0].get("possible_internal_transfer") is True


class TestGetNeedsReview:
    def test_returns_uncertain_transactions(self, db_env, monkeypatch):
        """get_needs_review returns transactions flagged uncertain=1."""
        from server.main import get_needs_review

        conn = get_db(db_env["db"])
        try:
            tx_id = _seed_transaction(conn, db_env["account_id"], merchant="Mystery Merchant")
            entry_id = _new_id()
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, "
                " entry_type, source, confidence, uncertain, reasoning, reviewed) "
                "VALUES (?, ?, NULL, NULL, 9.99, 'spending', 'llm', 0.4, 1, 'LLM unsure', 0)",
                (entry_id, tx_id),
            )
            conn.commit()
        finally:
            conn.close()

        # Patch get_active_user_id to return our test user.
        monkeypatch.setattr("server.main.get_active_user_id", lambda _: db_env["user_id"])

        result = get_needs_review()
        assert len(result["transactions"]) == 1
        txn = result["transactions"][0]
        assert txn["merchant"] == "Mystery Merchant"
        assert txn["reasoning"] == "LLM unsure"

    def test_reviewed_transactions_excluded(self, db_env, monkeypatch):
        """Transactions with reviewed=1 must NOT appear in get_needs_review."""
        conn = get_db(db_env["db"])
        try:
            tx_id = _seed_transaction(conn, db_env["account_id"], merchant="Reviewed")
            entry_id = _new_id()
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, "
                " entry_type, source, confidence, uncertain, reviewed) "
                "VALUES (?, ?, ?, ?, 5.0, 'spending', 'llm', 0.95, 1, 1)",
                (entry_id, tx_id, db_env["ledger_id"], db_env["expense_li_id"]),
            )
            conn.commit()
        finally:
            conn.close()

        monkeypatch.setattr("server.main.get_active_user_id", lambda _: db_env["user_id"])

        result = get_needs_review()
        assert result["transactions"] == []

    def test_skip_entries_excluded(self, db_env, monkeypatch):
        """Skip entries with uncertain=1 must NOT appear (entry_type='skip' excluded)."""
        conn = get_db(db_env["db"])
        try:
            tx_id = _seed_transaction(conn, db_env["account_id"], merchant="Credit Payment")
            entry_id = _new_id()
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, "
                " entry_type, source, confidence, uncertain, reviewed) "
                "VALUES (?, ?, NULL, NULL, 100.0, 'skip', 'llm', 0.99, 0, 0)",
                (entry_id, tx_id),
            )
            conn.commit()
        finally:
            conn.close()

        monkeypatch.setattr("server.main.get_active_user_id", lambda _: db_env["user_id"])

        result = get_needs_review()
        assert result["transactions"] == []

    def test_no_active_user_returns_empty(self, tmp_db, monkeypatch):
        """No active user → get_needs_review returns empty transactions list."""

        monkeypatch.setattr("server.main.get_active_user_id", lambda _: None)

        result = get_needs_review()
        assert result == {"transactions": []}
