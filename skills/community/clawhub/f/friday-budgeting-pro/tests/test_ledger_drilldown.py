"""
tests/test_ledger_drilldown.py — Tests for the ledger drilldown (#175).

Covers:
  - get_ledger() returns proper structure for a ledger with no entries
  - With seeded transaction_entries, transactions appear under correct line items
  - period='this_month' filters correctly
  - Invalid ledger_id → error
  - Not authenticated → error
  - UI: GET /ledgers renders line items with data-line-item-id attrs and totals
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

import pytest

import server.paths
from server.db import get_db, init_db
from ui.auth import create_session, create_user

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Fresh temp DB; monkeypatch server.paths.DB_PATH to point at it."""
    path = tmp_path / "test_drilldown.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    """Create a test user + session so get_active_user_id() returns a real ID."""
    user_id = create_user(db_path, "testuser", "testpass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


def _uid() -> str:
    return str(uuid.uuid4())


def _seed_ledger(db_path: Path, user_id: str) -> tuple[str, str, str]:
    """Insert a ledger with one income and one expense line item.

    Returns (ledger_id, income_item_id, expense_item_id).
    """
    conn = get_db(db_path)
    try:
        ledger_id = _uid()
        income_id = _uid()
        expense_id = _uid()
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "TestLedger", user_id),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (income_id, ledger_id, "Salary", "income"),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (expense_id, ledger_id, "Groceries", "expense"),
        )
        conn.commit()
    finally:
        conn.close()
    return ledger_id, income_id, expense_id


def _seed_transaction(
    db_path: Path,
    ledger_id: str,
    line_item_id: str,
    date: str,
    amount: float,
    merchant: str = "Test Merchant",
) -> str:
    """Insert a transaction + transaction_entry. Returns transaction id."""
    conn = get_db(db_path)
    try:
        txn_id = _uid()
        entry_id = _uid()
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
            (txn_id, date, merchant, amount),
        )
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (entry_id, txn_id, ledger_id, line_item_id, amount, amount, "spending", "rule"),
        )
        conn.commit()
    finally:
        conn.close()
    return txn_id


# ---------------------------------------------------------------------------
# Test: get_ledger structure with no entries
# ---------------------------------------------------------------------------


class TestGetLedgerNoEntries:
    def test_returns_ledger_metadata(self, db_path, authed_user):
        """get_ledger() returns ledger dict with id/name/type."""
        from server.main import get_ledger

        ledger_id, _, _ = _seed_ledger(db_path, authed_user["user_id"])
        result = get_ledger(ledger_id)

        assert "ledger" in result
        assert result["ledger"]["id"] == ledger_id
        assert result["ledger"]["name"] == "TestLedger"

    def test_returns_line_items(self, db_path, authed_user):
        """get_ledger() returns line_items list."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        result = get_ledger(ledger_id)

        assert "line_items" in result
        item_ids = {li["id"] for li in result["line_items"]}
        assert income_id in item_ids
        assert expense_id in item_ids

    def test_line_item_has_required_keys(self, db_path, authed_user):
        """Each line item has id, name, item_type, total, transactions."""
        from server.main import get_ledger

        ledger_id, _, _ = _seed_ledger(db_path, authed_user["user_id"])
        result = get_ledger(ledger_id)

        for item in result["line_items"]:
            assert "id" in item
            assert "name" in item
            assert "item_type" in item
            assert "total" in item
            assert "transactions" in item

    def test_empty_transactions_list(self, db_path, authed_user):
        """With no entries, transactions list is empty."""
        from server.main import get_ledger

        ledger_id, _, _ = _seed_ledger(db_path, authed_user["user_id"])
        result = get_ledger(ledger_id)

        for item in result["line_items"]:
            assert item["transactions"] == []
            assert item["total"] == 0.0

    def test_returns_totals(self, db_path, authed_user):
        """get_ledger() returns totals dict with income/expenses/net."""
        from server.main import get_ledger

        ledger_id, _, _ = _seed_ledger(db_path, authed_user["user_id"])
        result = get_ledger(ledger_id)

        assert "totals" in result
        totals = result["totals"]
        assert "income" in totals
        assert "expenses" in totals
        assert "net" in totals
        assert totals["income"] == 0.0
        assert totals["expenses"] == 0.0
        assert totals["net"] == 0.0


# ---------------------------------------------------------------------------
# Test: with seeded transaction_entries, transactions appear under correct items
# ---------------------------------------------------------------------------


class TestGetLedgerWithEntries:
    def test_transaction_appears_under_correct_item(self, db_path, authed_user):
        """Seeded transaction_entry appears in the correct line item."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        _seed_transaction(db_path, ledger_id, expense_id, "2026-01-15", 99.99, "Superstore")

        result = get_ledger(ledger_id, period=None)
        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        income_item = next(li for li in result["line_items"] if li["id"] == income_id)

        assert len(expense_item["transactions"]) == 1
        assert expense_item["transactions"][0]["merchant"] == "Superstore"
        assert expense_item["transactions"][0]["amount"] == 99.99
        assert len(income_item["transactions"]) == 0

    def test_transaction_has_required_keys(self, db_path, authed_user):
        """Each transaction dict has id, date, merchant, amount, account_name, pending."""
        from server.main import get_ledger

        ledger_id, _, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        _seed_transaction(db_path, ledger_id, expense_id, "2026-01-15", 50.0)

        result = get_ledger(ledger_id, period=None)
        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        tx = expense_item["transactions"][0]

        for key in ("id", "date", "merchant", "amount", "account_name", "pending"):
            assert key in tx, f"Missing key: {key}"

    def test_totals_computed_correctly(self, db_path, authed_user):
        """Totals reflect the sum of transaction_entries amounts."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        _seed_transaction(db_path, ledger_id, expense_id, "2026-01-10", 200.0)
        _seed_transaction(db_path, ledger_id, expense_id, "2026-01-20", 150.0)
        _seed_transaction(db_path, ledger_id, income_id, "2026-01-05", 3000.0)

        result = get_ledger(ledger_id, period=None)
        assert result["totals"]["expenses"] == pytest.approx(350.0)
        assert result["totals"]["income"] == pytest.approx(3000.0)
        assert result["totals"]["net"] == pytest.approx(2650.0)


# ---------------------------------------------------------------------------
# Test: period='this_month' filters correctly
# ---------------------------------------------------------------------------


class TestGetLedgerPeriodFilter:
    def test_this_month_includes_current_month(self, db_path, authed_user):
        """period='this_month' includes transactions dated in the current month."""
        from server.main import get_ledger

        ledger_id, _, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        today = datetime.now()
        current_date = f"{today.year}-{today.month:02d}-15"
        _seed_transaction(db_path, ledger_id, expense_id, current_date, 75.0, "InMonth")

        result = get_ledger(ledger_id, period="this_month")
        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        merchants = [tx["merchant"] for tx in expense_item["transactions"]]
        assert "InMonth" in merchants

    def test_this_month_excludes_other_months(self, db_path, authed_user):
        """period='this_month' excludes transactions from other months."""
        from server.main import get_ledger

        ledger_id, _, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        # Use a date far in the past — guaranteed to be out of this month
        _seed_transaction(db_path, ledger_id, expense_id, "2020-01-15", 99.0, "OldTxn")

        result = get_ledger(ledger_id, period="this_month")
        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        merchants = [tx["merchant"] for tx in expense_item["transactions"]]
        assert "OldTxn" not in merchants

    def test_none_period_returns_all(self, db_path, authed_user):
        """period=None returns all transactions regardless of date."""
        from server.main import get_ledger

        ledger_id, _, expense_id = _seed_ledger(db_path, authed_user["user_id"])
        _seed_transaction(db_path, ledger_id, expense_id, "2020-01-15", 99.0, "OldTxn")
        _seed_transaction(db_path, ledger_id, expense_id, "2026-05-01", 50.0, "NewTxn")

        result = get_ledger(ledger_id, period=None)
        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        assert len(expense_item["transactions"]) == 2


# ---------------------------------------------------------------------------
# Test: invalid ledger_id → error
# ---------------------------------------------------------------------------


class TestGetLedgerInvalidId:
    def test_unknown_ledger_returns_error(self, db_path, authed_user):
        """get_ledger() with unknown id returns error dict."""
        from server.main import get_ledger

        result = get_ledger(_uid())
        assert result.get("status") == "error"
        assert "not found" in result.get("message", "").lower()


# ---------------------------------------------------------------------------
# Test: not authenticated → error
# ---------------------------------------------------------------------------


class TestGetLedgerUnauthenticated:
    def test_no_active_user_returns_error(self, db_path):
        """get_ledger() with no active session returns error."""
        from server.main import get_ledger

        result = get_ledger(_uid())
        assert result.get("status") == "error"


# ---------------------------------------------------------------------------
# Test: UI GET /ledgers renders data-line-item-id attrs and totals
# ---------------------------------------------------------------------------


@pytest.fixture()
def ui_db_path(tmp_path: Path, monkeypatch) -> Path:
    import server.paths as paths

    db = tmp_path / "test_ui_drilldown.db"
    init_db(db)
    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def authed_ui_client(ui_db_path: Path):
    from fastapi.testclient import TestClient

    from ui.server import app

    client = TestClient(app, follow_redirects=False)
    # Setup wizard
    client.post("/setup/1", data={"password": "testpass123", "password_confirm": "testpass123"})
    client.post("/setup/2", data={"notification_pref": "openclaw"})
    client.post("/setup/3", data={"action": "skip"})  # terminal step — redirects to /dashboard
    # Login
    client.post("/login", data={"password": "testpass123"})
    return client


class TestLedgersPageDrilldown:
    def test_page_renders_ok(self, authed_ui_client):
        """GET /ledgers returns 200."""
        r = authed_ui_client.get("/ledgers")
        assert r.status_code == 200

    def test_page_has_data_line_item_id(self, authed_ui_client):
        """GET /ledgers HTML contains data-line-item-id attributes on line item rows."""
        r = authed_ui_client.get("/ledgers")
        assert "data-line-item-id" in r.text

    def test_page_shows_totals(self, authed_ui_client):
        """GET /ledgers shows C$ formatted totals for line items."""
        r = authed_ui_client.get("/ledgers")
        assert "C$" in r.text

    def test_page_shows_transaction_count(self, authed_ui_client):
        """GET /ledgers shows 'transactions' text for line item counts."""
        r = authed_ui_client.get("/ledgers")
        assert "transaction" in r.text

    def test_page_with_entry_shows_expand_button(self, authed_ui_client, ui_db_path):
        """When a transaction_entry exists, the expand button is present."""
        # Find the first line item from setup wizard
        conn = get_db(ui_db_path)
        try:
            ledger = conn.execute("SELECT id FROM ledgers LIMIT 1").fetchone()
            item = conn.execute(
                "SELECT id FROM line_items WHERE ledger_id = ? LIMIT 1",
                (ledger["id"],),
            ).fetchone()
            txn_id = _uid()
            entry_id = _uid()
            conn.execute(
                "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
                (txn_id, "2026-05-10", "TestMerchant", 42.0),
            )
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    entry_id,
                    txn_id,
                    ledger["id"],
                    item["id"],
                    42.0,
                    42.0,
                    "spending",
                    "rule",
                ),
            )
            conn.commit()
        finally:
            conn.close()

        r = authed_ui_client.get("/ledgers")
        assert r.status_code == 200
        assert "btn-expand-item" in r.text
        assert "txn-detail-row" in r.text
