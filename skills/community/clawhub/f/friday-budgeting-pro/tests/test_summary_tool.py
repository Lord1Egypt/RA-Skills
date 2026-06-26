"""
tests/test_summary_tool.py — Tests for the summary() MCP tool.

Uses tmp_path + monkeypatch to keep all DB writes in a temp directory so
the real ~/.friday-bp/data.db is never touched.

Seed
----
- One ledger: "Personal"
- Two line items:
    - "Salary"     (income)
    - "Groceries"  (expense)
- Three transactions in different months / years with classified entries:
    1. 2025-12-15  Salary     +3 000.00  (income)   — prior year
    2. 2026-04-10  Groceries   -200.00   (expense)  — current April 2026
    3. 2026-05-07  Salary     +4 000.00  (income)   — May 2026
    4. 2026-05-20  Groceries   -345.67   (expense)  — May 2026
    5. 2026-05-25  Salary     +1 000.00  (income)   — May 2026 (second entry)

Tests are written against fixed dates so they are deterministic regardless of
when they run; "month"/"year"/"ytd" tests use monkeypatched datetime.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

import server.main as main_module
import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


def seed_db(db_path: Path) -> dict:
    """Seed deterministic fixture data; return IDs for assertions."""
    conn = get_db(db_path)

    # Ledger
    ledger_id = _uid()
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_id, "Personal"))

    # Line items
    li_salary = _uid()
    li_groceries = _uid()
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_salary, ledger_id, "Salary", "income"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_groceries, ledger_id, "Groceries", "expense"),
    )

    # Transactions + entries
    # We insert bank_account_id as NULL — schema allows it for these tests.
    def add_txn(date_str: str, merchant: str, amount: float, line_item_id: str) -> None:
        txn_id = _uid()
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
            (txn_id, date_str, merchant, amount),
        )
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (_uid(), txn_id, ledger_id, line_item_id, amount, "rule", 1),
        )

    # Prior year (2025)
    add_txn("2025-12-15", "Employer", 3000.00, li_salary)

    # 2026-04 (different month, same year)
    add_txn("2026-04-10", "Superstore", -200.00, li_groceries)

    # 2026-05 (two income + one expense entries)
    add_txn("2026-05-07", "Employer", 4000.00, li_salary)
    add_txn("2026-05-20", "Superstore", -345.67, li_groceries)
    add_txn("2026-05-25", "Bonus", 1000.00, li_salary)

    conn.commit()
    conn.close()

    return {
        "ledger_id": ledger_id,
        "li_salary": li_salary,
        "li_groceries": li_groceries,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def seeded_db(tmp_path: Path, monkeypatch):
    """Initialise + seed a temp DB and monkeypatch server.paths.DB_PATH."""
    db_path = tmp_path / "test.db"
    init_db(db_path)
    ids = seed_db(db_path)
    monkeypatch.setattr(server.paths, "DB_PATH", db_path)
    return ids


# ---------------------------------------------------------------------------
# Helper: freeze datetime.now() inside server.main so period-relative tests
# are deterministic.  We mock _datetime inside the module to 2026-05-26.
# ---------------------------------------------------------------------------

FROZEN_DATE = datetime(2026, 5, 26)


# ---------------------------------------------------------------------------
# Tests: specific ISO month
# ---------------------------------------------------------------------------


def test_specific_month(seeded_db):
    """summary('2026-05') returns only May 2026 totals."""
    result = main_module.summary("2026-05")

    assert result["period"] == "2026-05"
    assert result["income"] == pytest.approx(5000.00)  # 4000 + 1000
    assert result["expenses"] == pytest.approx(-345.67)
    assert result["net"] == pytest.approx(5000.00 - (-345.67))


def test_specific_month_excludes_other_months(seeded_db):
    """April transactions must NOT appear in the May summary."""
    result = main_module.summary("2026-05")
    # April had -200.00 groceries; expenses should only reflect May
    assert result["expenses"] == pytest.approx(-345.67)


# ---------------------------------------------------------------------------
# Tests: specific ISO year
# ---------------------------------------------------------------------------


def test_specific_year(seeded_db):
    """summary('2026') returns totals for the whole of 2026."""
    result = main_module.summary("2026")

    assert result["period"] == "2026"
    # income: 4000 + 1000 = 5000 (2025 salary excluded)
    assert result["income"] == pytest.approx(5000.00)
    # expenses: -200 (Apr) + -345.67 (May) = -545.67
    assert result["expenses"] == pytest.approx(-545.67)
    assert result["net"] == pytest.approx(5000.00 - (-545.67))


def test_specific_year_excludes_prior_year(seeded_db):
    """2025 salary must NOT appear in the 2026 summary."""
    result = main_module.summary("2026")
    assert result["income"] == pytest.approx(5000.00)  # not 8000


# ---------------------------------------------------------------------------
# Tests: "month" (relative — frozen to 2026-05-26)
# ---------------------------------------------------------------------------


def test_month_returns_current_month(seeded_db):
    """summary('month') with today=2026-05-26 returns May 2026 totals."""
    with patch.object(main_module, "_datetime") as mock_dt:
        mock_dt.now.return_value = FROZEN_DATE
        result = main_module.summary("month")

    assert result["income"] == pytest.approx(5000.00)
    assert result["expenses"] == pytest.approx(-345.67)


# ---------------------------------------------------------------------------
# Tests: "year" (relative — frozen to 2026-05-26)
# ---------------------------------------------------------------------------


def test_year_returns_current_year(seeded_db):
    """summary('year') with today=2026-05-26 returns full 2026 totals."""
    with patch.object(main_module, "_datetime") as mock_dt:
        mock_dt.now.return_value = FROZEN_DATE
        result = main_module.summary("year")

    assert result["income"] == pytest.approx(5000.00)
    assert result["expenses"] == pytest.approx(-545.67)


# ---------------------------------------------------------------------------
# Tests: "ytd" (relative — frozen to 2026-05-26)
# ---------------------------------------------------------------------------


def test_ytd_returns_year_to_date(seeded_db):
    """summary('ytd') includes Jan-May 2026 inclusive."""
    with patch.object(main_module, "_datetime") as mock_dt:
        mock_dt.now.return_value = FROZEN_DATE
        result = main_module.summary("ytd")

    # Same as full year 2026 since all 2026 dates are <= 2026-05-26
    assert result["income"] == pytest.approx(5000.00)
    assert result["expenses"] == pytest.approx(-545.67)


def test_ytd_excludes_prior_year(seeded_db):
    """YTD must not include the 2025-12-15 salary entry."""
    with patch.object(main_module, "_datetime") as mock_dt:
        mock_dt.now.return_value = FROZEN_DATE
        result = main_module.summary("ytd")

    assert result["income"] == pytest.approx(5000.00)  # not 8000


# ---------------------------------------------------------------------------
# Tests: net = income - expenses
# ---------------------------------------------------------------------------


def test_net_is_income_minus_expenses(seeded_db):
    """Net must equal income - expenses regardless of period."""
    result = main_module.summary("2026")
    assert result["net"] == pytest.approx(result["income"] - result["expenses"])


def test_net_specific_month(seeded_db):
    result = main_module.summary("2026-05")
    assert result["net"] == pytest.approx(result["income"] - result["expenses"])


# ---------------------------------------------------------------------------
# Tests: by_line_item structure and sorting
# ---------------------------------------------------------------------------


def test_by_line_item_structure(seeded_db):
    """Each entry in by_line_item must have the required keys."""
    result = main_module.summary("2026-05")
    assert "by_line_item" in result
    for item in result["by_line_item"]:
        assert "line_item" in item
        assert "ledger" in item
        assert "type" in item
        assert "total" in item


def test_by_line_item_sorted_descending(seeded_db):
    """by_line_item must be sorted by total descending (income first)."""
    result = main_module.summary("2026")
    totals = [item["total"] for item in result["by_line_item"]]
    assert totals == sorted(totals, reverse=True)


def test_by_line_item_values_for_may(seeded_db):
    """Spot-check the line-item breakdown for 2026-05."""
    result = main_module.summary("2026-05")
    by_name = {item["line_item"]: item for item in result["by_line_item"]}

    assert "Salary" in by_name
    assert by_name["Salary"]["type"] == "income"
    assert by_name["Salary"]["total"] == pytest.approx(5000.00)

    assert "Groceries" in by_name
    assert by_name["Groceries"]["type"] == "expense"
    assert by_name["Groceries"]["total"] == pytest.approx(-345.67)


# ---------------------------------------------------------------------------
# Tests: invalid period raises ValueError
# ---------------------------------------------------------------------------


def test_invalid_period_raises():
    with pytest.raises(ValueError, match="Invalid period"):
        main_module.summary("last-week")


def test_invalid_period_partial_date_raises():
    with pytest.raises(ValueError, match="Invalid period"):
        main_module.summary("2026-5")  # needs zero-padded month


def test_invalid_period_empty_raises():
    with pytest.raises(ValueError, match="Invalid period"):
        main_module.summary("")
