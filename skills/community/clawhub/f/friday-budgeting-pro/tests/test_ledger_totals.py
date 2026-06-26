"""
tests/test_ledger_totals.py — Tests for ledger line item totals (#164).

Covers:
  - Ledger with 2 line items + 3 transaction_entries → GET /ledgers shows correct totals
  - get_ledger() returns totals for seeded entries
  - Line item with 0 entries shows C$0.00 · 0 transactions in the UI
  - Income line item total is positive, expense total is positive (amounts stored as positive)
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest

import server.paths
from server.db import get_db, init_db
from ui.auth import create_session, create_user

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


def _seed_ledger_with_items(db_path: Path, user_id: str) -> tuple[str, str, str]:
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
            (ledger_id, "BudgetLedger", user_id),
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


def _seed_entry(
    db_path: Path,
    ledger_id: str,
    line_item_id: str,
    amount: float,
    merchant: str = "Merchant",
    date: str = "2026-05-15",
) -> str:
    """Insert one transaction + transaction_entry. Returns transaction_id."""
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
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    path = tmp_path / "test_ledger_totals.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    user_id = create_user(db_path, "totalsuser", "pass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


# ---------------------------------------------------------------------------
# 1. get_ledger() returns correct totals for seeded entries
# ---------------------------------------------------------------------------


class TestGetLedgerTotals:
    def test_two_line_items_three_entries(self, db_path, authed_user):
        """2 line items with 3 entries → correct individual and aggregate totals."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger_with_items(db_path, authed_user["user_id"])
        _seed_entry(db_path, ledger_id, expense_id, 100.0, "Loblaws")
        _seed_entry(db_path, ledger_id, expense_id, 50.0, "Metro")
        _seed_entry(db_path, ledger_id, income_id, 3000.0, "Employer")

        result = get_ledger(ledger_id, period=None)

        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        income_item = next(li for li in result["line_items"] if li["id"] == income_id)

        assert expense_item["total"] == pytest.approx(150.0)
        assert len(expense_item["transactions"]) == 2

        assert income_item["total"] == pytest.approx(3000.0)
        assert len(income_item["transactions"]) == 1

    def test_totals_block_reflects_all_entries(self, db_path, authed_user):
        """Aggregate totals block sums all line item amounts correctly."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger_with_items(db_path, authed_user["user_id"])
        _seed_entry(db_path, ledger_id, expense_id, 200.0, "Rent")
        _seed_entry(db_path, ledger_id, expense_id, 80.0, "Hydro")
        _seed_entry(db_path, ledger_id, income_id, 4000.0, "Payroll")

        result = get_ledger(ledger_id, period=None)

        assert result["totals"]["expenses"] == pytest.approx(280.0)
        assert result["totals"]["income"] == pytest.approx(4000.0)
        assert result["totals"]["net"] == pytest.approx(3720.0)


# ---------------------------------------------------------------------------
# 2. Zero-entry line items show C$0.00 / 0 transactions
# ---------------------------------------------------------------------------


class TestZeroEntryLineItems:
    def test_zero_total_and_count(self, db_path, authed_user):
        """Line item with no entries has total=0.0 and empty transactions list."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger_with_items(db_path, authed_user["user_id"])
        # No entries added

        result = get_ledger(ledger_id, period=None)
        for item in result["line_items"]:
            assert item["total"] == 0.0
            assert item["transactions"] == []


# ---------------------------------------------------------------------------
# 3. Positive display convention for both item types
# ---------------------------------------------------------------------------


class TestAmountSignConvention:
    def test_expense_amount_positive(self, db_path, authed_user):
        """Expense line item total is stored and returned as a positive number."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger_with_items(db_path, authed_user["user_id"])
        _seed_entry(db_path, ledger_id, expense_id, 99.99, "Costco")

        result = get_ledger(ledger_id, period=None)
        expense_item = next(li for li in result["line_items"] if li["id"] == expense_id)
        assert expense_item["total"] > 0

    def test_income_amount_positive(self, db_path, authed_user):
        """Income line item total is stored and returned as a positive number."""
        from server.main import get_ledger

        ledger_id, income_id, expense_id = _seed_ledger_with_items(db_path, authed_user["user_id"])
        _seed_entry(db_path, ledger_id, income_id, 2500.0, "Payroll")

        result = get_ledger(ledger_id, period=None)
        income_item = next(li for li in result["line_items"] if li["id"] == income_id)
        assert income_item["total"] > 0


# ---------------------------------------------------------------------------
# 4. UI: GET /ledgers shows C$ amounts + counts for seeded entries
# ---------------------------------------------------------------------------


@pytest.fixture()
def ui_db_path(tmp_path: Path, monkeypatch) -> Path:
    import server.paths as paths

    db = tmp_path / "test_ledger_totals_ui.db"
    init_db(db)
    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def authed_ui_client(ui_db_path: Path):
    from fastapi.testclient import TestClient

    from ui.server import app

    client = TestClient(app, follow_redirects=False)
    client.post("/setup/1", data={"password": "testpass123", "password_confirm": "testpass123"})
    client.post("/setup/2", data={"notification_pref": "openclaw"})
    client.post("/setup/3", data={"action": "skip"})  # terminal step — redirects to /dashboard
    client.post("/login", data={"password": "testpass123"})
    return client, ui_db_path


class TestLedgersPageTotals:
    def test_get_ledgers_returns_200(self, authed_ui_client):
        """GET /ledgers returns HTTP 200."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200

    def test_zero_total_renders_c_dollar_zero(self, authed_ui_client):
        """Line items with no entries render C$0.00 in the page."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert "C$0.00" in r.text

    def test_zero_count_renders_zero_transactions(self, authed_ui_client):
        """Line items with no entries render '0 transactions' in the page."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert "0 transactions" in r.text

    def test_seeded_entry_shows_nonzero_total(self, authed_ui_client):
        """After seeding a transaction_entry, /ledgers shows the non-zero C$ total."""
        client, db_path = authed_ui_client

        conn = get_db(db_path)
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
                (txn_id, "2026-05-15", "FreshCo", 123.45),
            )
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (entry_id, txn_id, ledger["id"], item["id"], 123.45, 123.45, "spending", "rule"),
            )
            conn.commit()
        finally:
            conn.close()

        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "C$123.45" in r.text

    def test_seeded_entry_shows_one_transaction(self, authed_ui_client):
        """After seeding a transaction_entry, /ledgers shows '1 transaction' count."""
        client, db_path = authed_ui_client

        conn = get_db(db_path)
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
                (txn_id, "2026-05-15", "NoFrills", 55.00),
            )
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (entry_id, txn_id, ledger["id"], item["id"], 55.00, 55.00, "spending", "rule"),
            )
            conn.commit()
        finally:
            conn.close()

        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "1 transaction" in r.text
