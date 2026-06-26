"""
tests/test_date_range_filter.py — Tests for ledger date range filter (#167).

Covers:
  - GET /ledgers (no period) → 200, defaults to this_month
  - GET /ledgers?period=last_month → 200, scoped to last month
  - GET /ledgers?period=all → 200, shows total across all time
  - Period selector rendered with the active period's link marked active
  - Entries outside the current month are excluded from this_month totals
  - Entries from last month appear under last_month totals
  - last_3_months and this_year periods return 200
  - Unknown period values fall back to this_month
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from server.db import get_db, init_db
from ui.auth import create_session, create_user  # noqa: F401 (create_session used in authed_user)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


def _seed_ledger(db_path: Path, user_id: str, name: str = "TestLedger") -> tuple[str, str, str]:
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
            (ledger_id, name, user_id),
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
    date: str,
    merchant: str = "TestMerchant",
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


def _this_month_date() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-15")


def _last_month_date() -> str:
    now = datetime.now()
    if now.month == 1:
        return f"{now.year - 1}-12-15"
    return f"{now.year}-{now.month - 1:02d}-15"


def _old_date() -> str:
    """Returns a date 6 months ago, well outside this_month or last_month."""
    old = datetime.now() - timedelta(days=180)
    return old.strftime("%Y-%m-15")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    import server.paths as paths

    path = tmp_path / "test_date_range.db"
    init_db(path)
    monkeypatch.setattr(paths, "DB_PATH", path)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return path


@pytest.fixture()
def client(db_path: Path):
    from fastapi.testclient import TestClient

    from ui.server import app

    c = TestClient(app, follow_redirects=False)
    # Run the setup wizard to create a user, then log in
    c.post("/setup/1", data={"password": "testpass123", "password_confirm": "testpass123"})
    c.post("/setup/2", data={"notification_pref": "openclaw"})
    c.post("/setup/3", data={"action": "skip"})  # terminal step — redirects to /dashboard
    c.post("/login", data={"password": "testpass123"})
    return c


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    """Direct DB user for low-level drilldown tests (no HTTP session needed)."""
    user_id = create_user(db_path, "filteruser", "pass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


# ---------------------------------------------------------------------------
# Tests — basic route behaviour
# ---------------------------------------------------------------------------


class TestPeriodRoutes:
    def test_get_ledgers_no_period_returns_200(self, client):
        """GET /ledgers without period param returns 200 (defaults to this_month)."""
        r = client.get("/ledgers")
        assert r.status_code == 200

    def test_get_ledgers_this_month_returns_200(self, client):
        r = client.get("/ledgers?period=this_month")
        assert r.status_code == 200

    def test_get_ledgers_last_month_returns_200(self, client):
        r = client.get("/ledgers?period=last_month")
        assert r.status_code == 200

    def test_get_ledgers_last_3_months_returns_200(self, client):
        r = client.get("/ledgers?period=last_3_months")
        assert r.status_code == 200

    def test_get_ledgers_this_year_returns_200(self, client):
        r = client.get("/ledgers?period=this_year")
        assert r.status_code == 200

    def test_get_ledgers_all_returns_200(self, client):
        r = client.get("/ledgers?period=all")
        assert r.status_code == 200

    def test_unknown_period_falls_back_to_this_month(self, client):
        """Unknown period values should not crash; fall back to this_month."""
        r = client.get("/ledgers?period=bogus")
        assert r.status_code == 200
        # Should render this_month as active
        assert 'href="/ledgers?period=this_month" class="active"' in r.text


# ---------------------------------------------------------------------------
# Tests — period selector rendered correctly
# ---------------------------------------------------------------------------


class TestPeriodSelectorUI:
    def test_default_this_month_link_is_active(self, client):
        r = client.get("/ledgers")
        assert r.status_code == 200
        assert 'href="/ledgers?period=this_month" class="active"' in r.text

    def test_last_month_link_is_active_when_selected(self, client):
        r = client.get("/ledgers?period=last_month")
        assert r.status_code == 200
        assert 'href="/ledgers?period=last_month" class="active"' in r.text
        # this_month should NOT be active
        assert 'href="/ledgers?period=this_month" class="active"' not in r.text

    def test_all_links_present(self, client):
        r = client.get("/ledgers")
        assert "this_month" in r.text
        assert "last_month" in r.text
        assert "last_3_months" in r.text
        assert "this_year" in r.text
        assert 'period=all"' in r.text

    def test_all_time_link_is_active_when_selected(self, client):
        r = client.get("/ledgers?period=all")
        assert r.status_code == 200
        assert 'href="/ledgers?period=all" class="active"' in r.text


# ---------------------------------------------------------------------------
# Tests — totals respect period filter
# ---------------------------------------------------------------------------


class TestPeriodTotals:
    def test_this_month_excludes_old_entries(self, db_path, authed_user):
        """Entries from 6 months ago should not appear in this_month totals."""
        from server.db import get_db as _get_db
        from server.main import _build_ledger_drilldown

        ledger_id, income_id, expense_id = _seed_ledger(
            db_path, authed_user["user_id"], "FilterLedger"
        )
        # Entry this month
        _seed_entry(db_path, ledger_id, expense_id, 100.0, _this_month_date(), "ThisMonthShop")
        # Old entry (6 months ago)
        _seed_entry(db_path, ledger_id, expense_id, 999.0, _old_date(), "OldShop")

        conn = _get_db(db_path)
        try:
            lr = conn.execute(
                "SELECT id, name, type, description FROM ledgers WHERE id = ?",
                (ledger_id,),
            ).fetchone()
            result = _build_ledger_drilldown(conn, lr, period="this_month")
        finally:
            conn.close()

        # Total should only include the 100.0 this-month entry
        expense_item = next(i for i in result["line_items"] if i["name"] == "Groceries")
        assert expense_item["total"] == pytest.approx(100.0)
        txn_merchants = [t["merchant"] for t in expense_item["transactions"]]
        assert "ThisMonthShop" in txn_merchants
        assert "OldShop" not in txn_merchants

    def test_last_month_shows_last_month_entries(self, db_path, authed_user):
        """Entries from last month appear under last_month totals."""
        from server.db import get_db as _get_db
        from server.main import _build_ledger_drilldown

        ledger_id, income_id, expense_id = _seed_ledger(
            db_path, authed_user["user_id"], "LastMonthLedger"
        )
        # Entry last month
        _seed_entry(db_path, ledger_id, expense_id, 200.0, _last_month_date(), "LastMonthShop")
        # Entry this month (should NOT appear in last_month)
        _seed_entry(db_path, ledger_id, expense_id, 50.0, _this_month_date(), "ThisMonthShop")

        conn = _get_db(db_path)
        try:
            lr = conn.execute(
                "SELECT id, name, type, description FROM ledgers WHERE id = ?",
                (ledger_id,),
            ).fetchone()
            result = _build_ledger_drilldown(conn, lr, period="last_month")
        finally:
            conn.close()

        expense_item = next(i for i in result["line_items"] if i["name"] == "Groceries")
        assert expense_item["total"] == pytest.approx(200.0)
        txn_merchants = [t["merchant"] for t in expense_item["transactions"]]
        assert "LastMonthShop" in txn_merchants
        assert "ThisMonthShop" not in txn_merchants

    def test_all_time_includes_all_entries(self, db_path, authed_user):
        """period='all' includes entries from any date."""
        from server.db import get_db as _get_db
        from server.main import _build_ledger_drilldown

        ledger_id, income_id, expense_id = _seed_ledger(
            db_path, authed_user["user_id"], "AllTimeLedger"
        )
        _seed_entry(db_path, ledger_id, expense_id, 100.0, _this_month_date(), "NowShop")
        _seed_entry(db_path, ledger_id, expense_id, 50.0, _last_month_date(), "LastShop")
        _seed_entry(db_path, ledger_id, expense_id, 25.0, _old_date(), "OldShop")

        conn = _get_db(db_path)
        try:
            lr = conn.execute(
                "SELECT id, name, type, description FROM ledgers WHERE id = ?",
                (ledger_id,),
            ).fetchone()
            # "all" sentinel → None for _build_ledger_drilldown
            result = _build_ledger_drilldown(conn, lr, period=None)
        finally:
            conn.close()

        expense_item = next(i for i in result["line_items"] if i["name"] == "Groceries")
        assert expense_item["total"] == pytest.approx(175.0)
        assert len(expense_item["transactions"]) == 3

    def test_get_ledgers_all_via_http(self, client):
        """GET /ledgers?period=all returns 200 and the all-time tab is active."""
        r = client.get("/ledgers?period=all")
        assert r.status_code == 200
        # All time tab should be active
        assert 'href="/ledgers?period=all" class="active"' in r.text
