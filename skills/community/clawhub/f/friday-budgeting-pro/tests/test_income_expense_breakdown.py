"""
tests/test_income_expense_breakdown.py — Income vs expense breakdown + net total (#166).

Covers:
  - Seed ledger with 2 income items + 3 expense items + transaction_entries
  - get_ledger() returns totals with correct income/expenses/net
  - GET /ledgers HTML has separate Income and Expenses sections
  - Net is green when income > expenses (net-positive CSS class)
  - Net is red when expenses > income (net-negative CSS class)
  - Currency prefix is C$ (home currency)
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


def _seed_breakdown_ledger(db_path: Path, user_id: str) -> dict:
    """Seed a ledger with 2 income + 3 expense line items + entries.

    Income items:
      - Salary:     3000.00
      - Freelance:   500.00
      → total income = 3500.00

    Expense items:
      - Rent:       1200.00
      - Groceries:   300.00
      - Utilities:   100.00
      → total expenses = 1600.00

    Net = 3500.00 - 1600.00 = 1900.00  (positive)
    """
    conn = get_db(db_path)
    try:
        ledger_id = _uid()
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "Breakdown Ledger", user_id),
        )

        items = {}
        for name, itype in [
            ("Salary", "income"),
            ("Freelance", "income"),
            ("Rent", "expense"),
            ("Groceries", "expense"),
            ("Utilities", "expense"),
        ]:
            item_id = _uid()
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (item_id, ledger_id, name, itype),
            )
            items[name] = item_id

        amounts = {
            "Salary": 3000.00,
            "Freelance": 500.00,
            "Rent": 1200.00,
            "Groceries": 300.00,
            "Utilities": 100.00,
        }
        for name, amount in amounts.items():
            txn_id = _uid()
            entry_id = _uid()
            conn.execute(
                "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
                (txn_id, "2026-05-15", name, amount),
            )
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (entry_id, txn_id, ledger_id, items[name], amount, amount, "spending", "rule"),
            )

        conn.commit()
    finally:
        conn.close()

    return {"ledger_id": ledger_id, "items": items}


def _seed_expense_heavy_ledger(db_path: Path, user_id: str) -> dict:
    """Seed a ledger where expenses > income (net negative).

    Income:   500.00
    Expenses: 800.00
    Net:     -300.00
    """
    conn = get_db(db_path)
    try:
        ledger_id = _uid()
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "Overspent Ledger", user_id),
        )

        income_id = _uid()
        expense_id = _uid()
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (income_id, ledger_id, "Side Gig", "income"),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (expense_id, ledger_id, "Vacation", "expense"),
        )

        for item_id, amount, merchant in [
            (income_id, 500.00, "Contract"),
            (expense_id, 800.00, "Hotel"),
        ]:
            txn_id = _uid()
            entry_id = _uid()
            conn.execute(
                "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
                (txn_id, "2026-05-20", merchant, amount),
            )
            conn.execute(
                "INSERT INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (entry_id, txn_id, ledger_id, item_id, amount, amount, "spending", "rule"),
            )

        conn.commit()
    finally:
        conn.close()

    return {"ledger_id": ledger_id, "income_id": income_id, "expense_id": expense_id}


# ---------------------------------------------------------------------------
# Fixtures (MCP layer)
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    path = tmp_path / "test_breakdown.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    user_id = create_user(db_path, "breakdownuser", "pass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


# ---------------------------------------------------------------------------
# Fixtures (UI layer)
# ---------------------------------------------------------------------------


@pytest.fixture()
def ui_db_path(tmp_path: Path, monkeypatch) -> Path:
    import server.paths as paths

    db = tmp_path / "test_breakdown_ui.db"
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


# ---------------------------------------------------------------------------
# 1. get_ledger() returns correct income/expenses/net totals
# ---------------------------------------------------------------------------


class TestGetLedgerBreakdownTotals:
    def test_income_total(self, db_path, authed_user):
        """2 income items sum correctly in totals.income."""
        from server.main import get_ledger

        seeded = _seed_breakdown_ledger(db_path, authed_user["user_id"])
        result = get_ledger(seeded["ledger_id"], period=None)

        assert result["totals"]["income"] == pytest.approx(3500.00)

    def test_expenses_total(self, db_path, authed_user):
        """3 expense items sum correctly in totals.expenses."""
        from server.main import get_ledger

        seeded = _seed_breakdown_ledger(db_path, authed_user["user_id"])
        result = get_ledger(seeded["ledger_id"], period=None)

        assert result["totals"]["expenses"] == pytest.approx(1600.00)

    def test_net_total_positive(self, db_path, authed_user):
        """Net = income - expenses (positive when income > expenses)."""
        from server.main import get_ledger

        seeded = _seed_breakdown_ledger(db_path, authed_user["user_id"])
        result = get_ledger(seeded["ledger_id"], period=None)

        assert result["totals"]["net"] == pytest.approx(1900.00)

    def test_net_total_negative(self, db_path, authed_user):
        """Net is negative when expenses > income."""
        from server.main import get_ledger

        seeded = _seed_expense_heavy_ledger(db_path, authed_user["user_id"])
        result = get_ledger(seeded["ledger_id"], period=None)

        assert result["totals"]["net"] == pytest.approx(-300.00)

    def test_income_items_classified_correctly(self, db_path, authed_user):
        """income line items have item_type == 'income'."""
        from server.main import get_ledger

        seeded = _seed_breakdown_ledger(db_path, authed_user["user_id"])
        result = get_ledger(seeded["ledger_id"], period=None)

        income_items = [li for li in result["line_items"] if li["item_type"] == "income"]
        assert len(income_items) == 2
        income_names = {li["name"] for li in income_items}
        assert income_names == {"Salary", "Freelance"}

    def test_expense_items_classified_correctly(self, db_path, authed_user):
        """expense line items have item_type == 'expense'."""
        from server.main import get_ledger

        seeded = _seed_breakdown_ledger(db_path, authed_user["user_id"])
        result = get_ledger(seeded["ledger_id"], period=None)

        expense_items = [li for li in result["line_items"] if li["item_type"] == "expense"]
        assert len(expense_items) == 3
        expense_names = {li["name"] for li in expense_items}
        assert expense_names == {"Rent", "Groceries", "Utilities"}


# ---------------------------------------------------------------------------
# 2. GET /ledgers HTML has separate Income and Expenses sections
# ---------------------------------------------------------------------------


class TestLedgersHTMLSections:
    def test_income_section_present(self, authed_ui_client):
        """GET /ledgers HTML contains an 'Income' section heading."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "Income" in r.text

    def test_expenses_section_present(self, authed_ui_client):
        """GET /ledgers HTML contains an 'Expenses' section heading."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "Expenses" in r.text

    def test_net_section_present(self, authed_ui_client):
        """GET /ledgers HTML contains a 'Net:' label in the totals footer."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "Net:" in r.text

    def test_total_income_label_present(self, authed_ui_client):
        """GET /ledgers HTML contains a 'Total income:' label."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "Total income:" in r.text

    def test_total_expenses_label_present(self, authed_ui_client):
        """GET /ledgers HTML contains a 'Total expenses:' label."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "Total expenses:" in r.text

    def test_income_data_section_attribute(self, authed_ui_client):
        """GET /ledgers HTML has data-section="income" attribute."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert 'data-section="income"' in r.text

    def test_expenses_data_section_attribute(self, authed_ui_client):
        """GET /ledgers HTML has data-section="expenses" attribute."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert 'data-section="expenses"' in r.text


# ---------------------------------------------------------------------------
# 3. Net CSS coloring (positive = green, negative = red)
# ---------------------------------------------------------------------------


class TestNetColorCSSClasses:
    def test_net_positive_css_class_when_income_greater(self, authed_ui_client):
        """net-positive CSS class appears when income > expenses."""
        client, ui_db_path = authed_ui_client

        # Get the ledger created during setup
        conn = get_db(ui_db_path)
        try:
            user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = user["id"]
            ledger = conn.execute("SELECT id FROM ledgers LIMIT 1").fetchone()
            ledger_id = ledger["id"]

            # Seed income > expenses
            income_id = _uid()
            expense_id = _uid()
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (income_id, ledger_id, "Big Salary", "income"),
            )
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (expense_id, ledger_id, "Small Bill", "expense"),
            )
            for item_id, amt, merch in [
                (income_id, 5000.0, "Employer"),
                (expense_id, 200.0, "Bill"),
            ]:
                txn_id = _uid()
                entry_id = _uid()
                conn.execute(
                    "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
                    (txn_id, "2026-05-15", merch, amt),
                )
                conn.execute(
                    "INSERT INTO transaction_entries "
                    "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (entry_id, txn_id, ledger_id, item_id, amt, amt, "spending", "rule"),
                )
            conn.commit()
        finally:
            conn.close()

        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "net-positive" in r.text

    def test_net_negative_css_class_when_expenses_greater(self, authed_ui_client):
        """net-negative CSS class appears when expenses > income."""
        client, ui_db_path = authed_ui_client

        conn = get_db(ui_db_path)
        try:
            ledger = conn.execute("SELECT id FROM ledgers LIMIT 1").fetchone()
            ledger_id = ledger["id"]

            income_id = _uid()
            expense_id = _uid()
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (income_id, ledger_id, "Tiny Gig", "income"),
            )
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (expense_id, ledger_id, "Huge Bill", "expense"),
            )
            for item_id, amt, merch in [
                (income_id, 100.0, "Side Job"),
                (expense_id, 900.0, "Rent"),
            ]:
                txn_id = _uid()
                entry_id = _uid()
                conn.execute(
                    "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
                    (txn_id, "2026-05-15", merch, amt),
                )
                conn.execute(
                    "INSERT INTO transaction_entries "
                    "(id, transaction_id, ledger_id, line_item_id, amount, amount_home, entry_type, source) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (entry_id, txn_id, ledger_id, item_id, amt, amt, "spending", "rule"),
                )
            conn.commit()
        finally:
            conn.close()

        r = client.get("/ledgers")
        assert r.status_code == 200
        assert "net-negative" in r.text


# ---------------------------------------------------------------------------
# 4. Currency prefix is C$
# ---------------------------------------------------------------------------


class TestCurrencyPrefix:
    def test_income_total_has_cad_prefix(self, authed_ui_client):
        """Total income value uses C$ prefix."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        # The totals footer uses C$ prefix on all three values
        assert "C$" in r.text

    def test_net_total_has_cad_prefix(self, authed_ui_client):
        """Net total value uses C$ prefix in the totals footer."""
        client, _ = authed_ui_client
        r = client.get("/ledgers")
        assert r.status_code == 200
        # data-total="net" span contains C$
        assert 'data-total="net"' in r.text
