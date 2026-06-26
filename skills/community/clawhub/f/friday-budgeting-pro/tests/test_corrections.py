"""
tests/test_corrections.py — Tests for natural-language transaction corrections (#173).

Covers:
  - Schema migrations apply (source, corrected_from_line_item_id, corrected_at)
  - find_transactions(merchant=...) returns matching transactions
  - find_transactions(amount=...) returns transactions within ±$0.50 tolerance
  - find_transactions(date=..., days_window=...) returns transactions within window
  - find_transactions(account=...) filters by account/institution name
  - correct_transaction() updates line_item_id, source, reviewed, corrected_from
  - corrected_from_line_item_id is preserved in the entry
  - correct_transaction(create_rule=True) calls add_rule with proper args
  - Invalid transaction_id → error response
  - No authenticated user → graceful error
"""

from __future__ import annotations

import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

import server.paths
from server.db import get_db, init_db
from ui.auth import create_session, create_user

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Fresh temp DB; monkeypatch server.paths.DB_PATH."""
    path = tmp_path / "test_corrections.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    """Create a test user + session so get_active_user_id() returns a real ID."""
    user_id = create_user(db_path, "testuser", "testpass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


def _seed_full(db_path: Path, user_id: str) -> dict:
    """Seed a complete set of fixtures: connection, account, ledger, line items, transactions.

    Returns a dict with all important IDs.
    """
    conn = get_db(db_path)
    try:
        # Bank connection + account
        conn_id = _uid()
        account_id = _uid()
        conn.execute(
            "INSERT INTO bank_connections (id, plaid_access_token_encrypted, status, user_id, institution_name) "
            "VALUES (?, ?, 'active', ?, ?)",
            (conn_id, "enc:fake", user_id, "Test Bank"),
        )
        conn.execute(
            "INSERT INTO bank_accounts (id, connection_id, name) VALUES (?, ?, ?)",
            (account_id, conn_id, "Chequing"),
        )

        # Ledger + line items
        ledger_id = _uid()
        li_coffee = _uid()
        li_travel = _uid()
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "Personal", user_id),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (li_coffee, ledger_id, "Coffee", "expense"),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (li_travel, ledger_id, "Travel", "expense"),
        )

        # Transactions
        tx_coffee = _uid()
        tx_ride = _uid()
        tx_exact = _uid()

        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount, bank_account_id) VALUES (?, ?, ?, ?, ?)",
            (tx_coffee, "2026-05-20", "Tim Hortons Coffee", 3.50, account_id),
        )
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount, bank_account_id) VALUES (?, ?, ?, ?, ?)",
            (tx_ride, "2026-05-18", "Uber Ride", 42.50, account_id),
        )
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount, bank_account_id) VALUES (?, ?, ?, ?, ?)",
            (tx_exact, "2026-05-15", "Amazon", 99.99, account_id),
        )

        # Existing entry for tx_coffee (classified as coffee)
        entry_coffee_id = _uid()
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (entry_coffee_id, tx_coffee, ledger_id, li_coffee, 3.50, "rule", 0),
        )

        conn.commit()
    finally:
        conn.close()

    return {
        "conn_id": conn_id,
        "account_id": account_id,
        "ledger_id": ledger_id,
        "li_coffee": li_coffee,
        "li_travel": li_travel,
        "tx_coffee": tx_coffee,
        "tx_ride": tx_ride,
        "tx_exact": tx_exact,
        "entry_coffee_id": entry_coffee_id,
    }


# ---------------------------------------------------------------------------
# Schema migration tests
# ---------------------------------------------------------------------------


class TestSchemaMigrations:
    def test_source_column_exists(self, db_path):
        """transaction_entries.source column must exist after init_db."""
        conn = get_db(db_path)
        cols = {row[1] for row in conn.execute("PRAGMA table_info(transaction_entries)")}
        conn.close()
        assert "source" in cols

    def test_corrected_from_line_item_id_column_exists(self, db_path):
        """transaction_entries.corrected_from_line_item_id must exist after init_db."""
        conn = get_db(db_path)
        cols = {row[1] for row in conn.execute("PRAGMA table_info(transaction_entries)")}
        conn.close()
        assert "corrected_from_line_item_id" in cols

    def test_corrected_at_column_exists(self, db_path):
        """transaction_entries.corrected_at must exist after init_db."""
        conn = get_db(db_path)
        cols = {row[1] for row in conn.execute("PRAGMA table_info(transaction_entries)")}
        conn.close()
        assert "corrected_at" in cols

    def test_migration_idempotent(self, db_path):
        """Calling init_db twice must not raise and columns are still present."""
        init_db(db_path)  # second call
        conn = get_db(db_path)
        cols = {row[1] for row in conn.execute("PRAGMA table_info(transaction_entries)")}
        conn.close()
        assert "corrected_from_line_item_id" in cols
        assert "corrected_at" in cols


# ---------------------------------------------------------------------------
# find_transactions tests
# ---------------------------------------------------------------------------


class TestFindTransactions:
    def test_find_by_merchant(self, db_path, authed_user):
        """find_transactions(merchant='Coffee') returns matching transactions."""
        from server.main import find_transactions

        ids = _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(merchant="Coffee")

        assert "transactions" in result
        assert len(result["transactions"]) == 1
        assert result["transactions"][0]["id"] == ids["tx_coffee"]
        assert "Coffee" in result["transactions"][0]["merchant"]

    def test_find_by_merchant_case_insensitive(self, db_path, authed_user):
        """Merchant matching should be case-insensitive."""
        from server.main import find_transactions

        _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(merchant="coffee")
        assert len(result["transactions"]) == 1

    def test_find_by_amount_exact(self, db_path, authed_user):
        """find_transactions(amount=42.50) returns the ride transaction."""
        from server.main import find_transactions

        ids = _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(amount=42.50)

        assert len(result["transactions"]) == 1
        assert result["transactions"][0]["id"] == ids["tx_ride"]

    def test_find_by_amount_within_tolerance(self, db_path, authed_user):
        """Transactions within ±$0.50 of given amount are included."""
        from server.main import find_transactions

        ids = _seed_full(db_path, authed_user["user_id"])
        # 42.50 ± 0.50 → 42.00–43.00, ride is 42.50 ✓
        result = find_transactions(amount=42.75)
        assert any(t["id"] == ids["tx_ride"] for t in result["transactions"])

    def test_find_by_amount_outside_tolerance_excluded(self, db_path, authed_user):
        """Transactions more than $0.50 away are excluded."""
        from server.main import find_transactions

        _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(amount=50.00)
        assert len(result["transactions"]) == 0

    def test_find_by_date_window(self, db_path, authed_user):
        """find_transactions(date='2026-05-20', days_window=3) returns within ±3 days."""
        from server.main import find_transactions

        ids = _seed_full(db_path, authed_user["user_id"])
        # 2026-05-20 ± 3 days = 2026-05-17 to 2026-05-23
        # tx_coffee: 2026-05-20 ✓, tx_ride: 2026-05-18 ✓, tx_exact: 2026-05-15 ✗
        result = find_transactions(date="2026-05-20", days_window=3)
        returned_ids = {t["id"] for t in result["transactions"]}
        assert ids["tx_coffee"] in returned_ids
        assert ids["tx_ride"] in returned_ids
        assert ids["tx_exact"] not in returned_ids

    def test_find_by_date_window_excludes_outside(self, db_path, authed_user):
        """Transactions outside the date window are excluded."""
        from server.main import find_transactions

        ids = _seed_full(db_path, authed_user["user_id"])
        # Pivot far in the future
        result = find_transactions(date="2026-06-01", days_window=3)
        assert len(result["transactions"]) == 0

    def test_find_by_account_name(self, db_path, authed_user):
        """find_transactions(account='Chequing') filters by account name."""
        from server.main import find_transactions

        _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(account="Chequing")
        assert len(result["transactions"]) > 0

    def test_find_by_institution_name(self, db_path, authed_user):
        """find_transactions(account='Test Bank') filters by institution name."""
        from server.main import find_transactions

        _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(account="Test Bank")
        assert len(result["transactions"]) > 0

    def test_find_returns_classification(self, db_path, authed_user):
        """find_transactions should include line_item_id and current_classification."""
        from server.main import find_transactions

        ids = _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(merchant="Tim Hortons")
        assert len(result["transactions"]) == 1
        tx = result["transactions"][0]
        assert tx["line_item_id"] == ids["li_coffee"]
        assert tx["current_classification"] is not None

    def test_find_no_match_returns_empty(self, db_path, authed_user):
        """No matching transactions → empty list, no error."""
        from server.main import find_transactions

        _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(merchant="ZZZNonexistent")
        assert result["transactions"] == []

    def test_find_not_authenticated(self, db_path):
        """No active session → graceful error response."""
        from server.main import find_transactions

        # No user or session created
        result = find_transactions(merchant="Coffee")
        assert result.get("error") == "not_authenticated"
        assert result["transactions"] == []

    def test_find_invalid_date_returns_error(self, db_path, authed_user):
        """Invalid date string returns an error dict."""
        from server.main import find_transactions

        _seed_full(db_path, authed_user["user_id"])
        result = find_transactions(date="not-a-date")
        assert "error" in result


# ---------------------------------------------------------------------------
# correct_transaction tests
# ---------------------------------------------------------------------------


class TestCorrectTransaction:
    def test_correct_updates_line_item(self, db_path, authed_user):
        """correct_transaction() changes line_item_id on the entry."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])
        result = correct_transaction(ids["tx_coffee"], ids["li_travel"])

        assert result["status"] == "ok"
        assert result["new_line_item_id"] == ids["li_travel"]

        conn = get_db(db_path)
        entry = conn.execute(
            "SELECT line_item_id, source, reviewed FROM transaction_entries WHERE transaction_id = ?",
            (ids["tx_coffee"],),
        ).fetchone()
        conn.close()
        assert entry["line_item_id"] == ids["li_travel"]
        assert entry["source"] == "manual"
        assert entry["reviewed"] == 1

    def test_correct_preserves_corrected_from(self, db_path, authed_user):
        """corrected_from_line_item_id must be set to the original line_item_id."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])
        correct_transaction(ids["tx_coffee"], ids["li_travel"])

        conn = get_db(db_path)
        entry = conn.execute(
            "SELECT corrected_from_line_item_id, corrected_at FROM transaction_entries WHERE transaction_id = ?",
            (ids["tx_coffee"],),
        ).fetchone()
        conn.close()
        assert entry["corrected_from_line_item_id"] == ids["li_coffee"]
        assert entry["corrected_at"] is not None

    def test_correct_inserts_entry_when_missing(self, db_path, authed_user):
        """If no existing entry, correct_transaction inserts one with source='manual'."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])
        # tx_ride has no entry
        result = correct_transaction(ids["tx_ride"], ids["li_travel"])

        assert result["status"] == "ok"

        conn = get_db(db_path)
        entry = conn.execute(
            "SELECT line_item_id, source, reviewed FROM transaction_entries WHERE transaction_id = ?",
            (ids["tx_ride"],),
        ).fetchone()
        conn.close()
        assert entry is not None
        assert entry["line_item_id"] == ids["li_travel"]
        assert entry["source"] == "manual"
        assert entry["reviewed"] == 1

    def test_correct_with_create_rule(self, db_path, authed_user):
        """correct_transaction(create_rule=True) invokes add_rule with priority=80."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])

        with patch("server.main.add_rule") as mock_add_rule:
            mock_add_rule.return_value = {"status": "ok", "rule_id": _uid()}
            result = correct_transaction(
                ids["tx_coffee"],
                ids["li_travel"],
                create_rule=True,
                rule_description="Coffee shops are travel expenses",
            )

        assert result["rule_created"] is True
        mock_add_rule.assert_called_once()
        call_kwargs = mock_add_rule.call_args
        # Check priority=80 and the custom description
        assert call_kwargs.kwargs.get("priority") == 80 or (
            len(call_kwargs.args) > 4 and call_kwargs.args[4] == 80
        )
        assert "Coffee shops are travel expenses" in (
            call_kwargs.kwargs.get("description", "") or call_kwargs.args[1]
        )

    def test_correct_with_create_rule_auto_description(self, db_path, authed_user):
        """When rule_description is None, an auto-generated description is used."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])

        with patch("server.main.add_rule") as mock_add_rule:
            mock_add_rule.return_value = {"status": "ok", "rule_id": _uid()}
            result = correct_transaction(ids["tx_coffee"], ids["li_travel"], create_rule=True)

        assert result["rule_created"] is True
        mock_add_rule.assert_called_once()
        # Description should be auto-generated and non-empty
        desc = mock_add_rule.call_args.kwargs.get("description", "")
        assert len(desc) > 0

    def test_correct_invalid_transaction_id(self, db_path, authed_user):
        """Non-existent transaction_id returns error response."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])
        result = correct_transaction("nonexistent-id", ids["li_travel"])

        assert result["status"] == "error"
        assert "not found" in result["error"]

    def test_correct_not_authenticated(self, db_path):
        """No active session → graceful error response."""
        from server.main import correct_transaction

        # No user or session
        result = correct_transaction("any-id", "any-line-item")
        assert result["status"] == "error"
        assert result["error"] == "not_authenticated"

    def test_correct_without_create_rule(self, db_path, authed_user):
        """create_rule=False (default) does not call add_rule."""
        from server.main import correct_transaction

        ids = _seed_full(db_path, authed_user["user_id"])

        with patch("server.main.add_rule") as mock_add_rule:
            result = correct_transaction(ids["tx_coffee"], ids["li_travel"])

        assert result["rule_created"] is False
        mock_add_rule.assert_not_called()
