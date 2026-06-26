"""
tests/test_ledger_types.py — Unit tests for ledger type support (#174).

Tests:
  - Migrations: fresh DB has type/description on ledgers, default_ledger_id
    on bank_accounts, item_type on line_items
  - list_ledgers() returns type and description fields
  - create_property_ledger() creates ledger with type=property and 6 line items
  - create_investment_ledger() creates ledger with type=investment and 2 line items
  - set_account_ledger() links account to ledger correctly
  - Invalid account or ledger → error response
"""

from __future__ import annotations

import uuid
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
    path = tmp_path / "test_ledger_types.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    """Create a test user + session so get_active_user_id() returns a real ID."""
    user_id = create_user(db_path, "testuser", "testpass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


# ---------------------------------------------------------------------------
# Migration tests: schema columns exist on fresh DB
# ---------------------------------------------------------------------------


def test_ledgers_has_type_column(db_path: Path):
    """Fresh DB: ledgers table has a 'type' column."""
    conn = get_db(db_path)
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(ledgers)")}
    finally:
        conn.close()
    assert "type" in cols, "ledgers.type column missing"


def test_ledgers_has_description_column(db_path: Path):
    """Fresh DB: ledgers table has a 'description' column."""
    conn = get_db(db_path)
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(ledgers)")}
    finally:
        conn.close()
    assert "description" in cols, "ledgers.description column missing"


def test_bank_accounts_has_default_ledger_id(db_path: Path):
    """Fresh DB: bank_accounts table has a 'default_ledger_id' column."""
    conn = get_db(db_path)
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(bank_accounts)")}
    finally:
        conn.close()
    assert "default_ledger_id" in cols, "bank_accounts.default_ledger_id column missing"


def test_line_items_has_item_type_column(db_path: Path):
    """Fresh DB: line_items table has an 'item_type' column."""
    conn = get_db(db_path)
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(line_items)")}
    finally:
        conn.close()
    assert "item_type" in cols, "line_items.item_type column missing"


# ---------------------------------------------------------------------------
# list_ledgers returns type and description
# ---------------------------------------------------------------------------


def test_list_ledgers_returns_type_and_description(db_path: Path, authed_user, monkeypatch):
    """list_ledgers() returns 'type' and 'description' fields for each ledger."""
    from server.main import list_ledgers

    # Seed a personal ledger directly
    uid = authed_user["user_id"]
    ledger_id = str(uuid.uuid4())
    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id, type, description) VALUES (?, ?, ?, ?, ?)",
            (ledger_id, "Personal", uid, "personal", None),
        )
        conn.commit()
    finally:
        conn.close()

    result = list_ledgers()
    assert "ledgers" in result
    assert len(result["ledgers"]) >= 1

    personal = next((lg for lg in result["ledgers"] if lg["name"] == "Personal"), None)
    assert personal is not None
    assert "type" in personal, "list_ledgers response missing 'type' field"
    assert "description" in personal, "list_ledgers response missing 'description' field"
    assert personal["type"] == "personal"


# ---------------------------------------------------------------------------
# create_property_ledger
# ---------------------------------------------------------------------------


def test_create_property_ledger(db_path: Path, authed_user):
    """create_property_ledger creates a ledger with type=property and 6 line items."""
    from server.main import create_property_ledger

    result = create_property_ledger("Test Property", description="123 Main St")
    assert result["status"] == "ok"
    ledger_id = result["ledger_id"]

    conn = get_db(db_path)
    try:
        ledger = conn.execute(
            "SELECT id, name, type, description FROM ledgers WHERE id = ?", (ledger_id,)
        ).fetchone()
        assert ledger is not None
        assert ledger["type"] == "property"
        assert ledger["description"] == "123 Main St"

        items = conn.execute(
            "SELECT name, item_type FROM line_items WHERE ledger_id = ?", (ledger_id,)
        ).fetchall()
    finally:
        conn.close()

    assert len(items) == 6, f"Expected 6 line items, got {len(items)}: {[i['name'] for i in items]}"

    names = [i["name"] for i in items]
    item_types = {i["name"]: i["item_type"] for i in items}

    assert "Rent income" in names
    assert "Mortgage" in names
    assert "Property tax" in names
    assert "Maintenance & repairs" in names
    assert "Insurance" in names
    assert "Utilities" in names

    assert item_types["Rent income"] == "income"
    for expense_name in (
        "Mortgage",
        "Property tax",
        "Maintenance & repairs",
        "Insurance",
        "Utilities",
    ):
        assert item_types[expense_name] == "expense", f"{expense_name} should be expense"


def test_create_property_ledger_no_description(db_path: Path, authed_user):
    """create_property_ledger works without a description."""
    from server.main import create_property_ledger

    result = create_property_ledger("Prop B")
    assert result["status"] == "ok"

    conn = get_db(db_path)
    try:
        ledger = conn.execute(
            "SELECT type, description FROM ledgers WHERE id = ?", (result["ledger_id"],)
        ).fetchone()
    finally:
        conn.close()

    assert ledger["type"] == "property"
    assert ledger["description"] is None


def test_create_property_ledger_no_active_user(db_path: Path):
    """create_property_ledger returns error when no user is logged in."""
    from server.main import create_property_ledger

    result = create_property_ledger("Should Fail")
    assert result["status"] == "error"
    assert "No active user" in result["message"]


# ---------------------------------------------------------------------------
# create_investment_ledger
# ---------------------------------------------------------------------------


def test_create_investment_ledger(db_path: Path, authed_user):
    """create_investment_ledger creates a ledger with type=investment and 2 line items."""
    from server.main import create_investment_ledger

    result = create_investment_ledger("TFSA")
    assert result["status"] == "ok"
    ledger_id = result["ledger_id"]

    conn = get_db(db_path)
    try:
        ledger = conn.execute(
            "SELECT id, name, type FROM ledgers WHERE id = ?", (ledger_id,)
        ).fetchone()
        assert ledger is not None
        assert ledger["type"] == "investment"
        assert ledger["name"] == "TFSA"

        items = conn.execute(
            "SELECT name, item_type FROM line_items WHERE ledger_id = ?", (ledger_id,)
        ).fetchall()
    finally:
        conn.close()

    assert len(items) == 2, f"Expected 2 line items, got {len(items)}"

    item_types = {i["name"]: i["item_type"] for i in items}
    assert "Contributions" in item_types
    assert "Dividends & Returns" in item_types
    assert item_types["Contributions"] == "expense"
    assert item_types["Dividends & Returns"] == "income"


def test_create_investment_ledger_no_active_user(db_path: Path):
    """create_investment_ledger returns error when no user is logged in."""
    from server.main import create_investment_ledger

    result = create_investment_ledger("Should Fail")
    assert result["status"] == "error"
    assert "No active user" in result["message"]


# ---------------------------------------------------------------------------
# set_account_ledger
# ---------------------------------------------------------------------------


def _seed_account_and_ledger(db_path: Path, user_id: str) -> tuple[str, str]:
    """Insert a bank connection + bank account + ledger for testing. Returns (account_id, ledger_id)."""
    conn = get_db(db_path)
    try:
        connection_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_connections "
            "(id, plaid_item_id, plaid_access_token_encrypted, status, user_id, plaid_env) "
            "VALUES (?, ?, ?, 'active', ?, 'sandbox')",
            (connection_id, f"item-{uuid.uuid4()}", "encrypted-token", user_id),
        )

        account_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name) "
            "VALUES (?, ?, ?, ?)",
            (account_id, connection_id, f"plaid-acct-{uuid.uuid4()}", "Test Account"),
        )

        ledger_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id, type) VALUES (?, ?, ?, 'personal')",
            (ledger_id, "Test Ledger", user_id),
        )
        conn.commit()
    finally:
        conn.close()

    return account_id, ledger_id


def test_set_account_ledger(db_path: Path, authed_user):
    """set_account_ledger links account to ledger correctly."""
    from server.main import set_account_ledger

    uid = authed_user["user_id"]
    account_id, ledger_id = _seed_account_and_ledger(db_path, uid)

    result = set_account_ledger(account_id, ledger_id)
    assert result == {"status": "ok"}, f"Unexpected result: {result}"

    conn = get_db(db_path)
    try:
        row = conn.execute(
            "SELECT default_ledger_id FROM bank_accounts WHERE id = ?", (account_id,)
        ).fetchone()
    finally:
        conn.close()

    assert row["default_ledger_id"] == ledger_id


def test_set_account_ledger_invalid_account(db_path: Path, authed_user):
    """set_account_ledger returns error for non-existent account."""
    from server.main import set_account_ledger

    uid = authed_user["user_id"]
    _, ledger_id = _seed_account_and_ledger(db_path, uid)

    result = set_account_ledger("nonexistent-account-id", ledger_id)
    assert result["status"] == "error"


def test_set_account_ledger_invalid_ledger(db_path: Path, authed_user):
    """set_account_ledger returns error for non-existent ledger."""
    from server.main import set_account_ledger

    uid = authed_user["user_id"]
    account_id, _ = _seed_account_and_ledger(db_path, uid)

    result = set_account_ledger(account_id, "nonexistent-ledger-id")
    assert result["status"] == "error"


# ---------------------------------------------------------------------------
# list_ledgers includes property and investment types
# ---------------------------------------------------------------------------


def test_list_ledgers_shows_all_types(db_path: Path, authed_user):
    """list_ledgers() returns all three ledger types when created."""
    from server.main import create_investment_ledger, create_property_ledger, list_ledgers

    create_property_ledger("Property A")
    create_investment_ledger("Investments")

    result = list_ledgers()
    types = [lg["type"] for lg in result["ledgers"]]
    assert "property" in types, f"Expected 'property' in types, got: {types}"
    assert "investment" in types, f"Expected 'investment' in types, got: {types}"
