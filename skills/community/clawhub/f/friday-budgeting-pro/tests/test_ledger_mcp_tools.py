"""
tests/test_ledger_mcp_tools.py — Unit tests for ledger MCP tools.

Tests:
  - list_ledgers returns Personal ledger after setup
  - add_ledger creates + appears in list_ledgers
  - add_line_item adds to correct ledger with correct type
  - remove_line_item works when no entries attached
  - remove_line_item returns error when entries exist
  - All tools return empty/error gracefully with no active user
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
    path = tmp_path / "test_ledger.db"
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


# ---------------------------------------------------------------------------
# Helper: seed the Personal ledger via apply_initial_setup
# ---------------------------------------------------------------------------


def _seed_personal(monkeypatch):
    """Call apply_initial_setup with a mocked _register_openclaw_cron."""
    from server.main import apply_initial_setup

    monkeypatch.setattr("server.main._register_openclaw_cron", lambda: False)
    apply_initial_setup(banks_to_link=[], extra_ledgers=[], hints=[])


# ---------------------------------------------------------------------------
# Test: list_ledgers with no active user returns empty list
# ---------------------------------------------------------------------------


def test_list_ledgers_no_active_user(db_path):
    """list_ledgers() with no session → {'ledgers': []}."""
    from server.main import list_ledgers

    result = list_ledgers()
    assert isinstance(result, dict)
    assert result == {"ledgers": []}


# ---------------------------------------------------------------------------
# Test: list_ledgers returns Personal ledger after setup
# ---------------------------------------------------------------------------


def test_list_ledgers_returns_personal(db_path, authed_user, monkeypatch):
    """list_ledgers() returns a dict with Personal ledger + line items."""
    from server.main import list_ledgers

    _seed_personal(monkeypatch)

    result = list_ledgers()
    assert isinstance(result, dict)
    assert "ledgers" in result

    names = [lg["name"] for lg in result["ledgers"]]
    assert "Personal" in names

    personal = next(lg for lg in result["ledgers"] if lg["name"] == "Personal")
    assert "id" in personal
    assert "items" in personal
    assert len(personal["items"]) > 0
    # Each item should have id, name, type
    item = personal["items"][0]
    assert "id" in item
    assert "name" in item
    assert "type" in item


# ---------------------------------------------------------------------------
# Test: add_ledger creates + appears in list_ledgers
# ---------------------------------------------------------------------------


def test_add_ledger_and_list(db_path, authed_user):
    """add_ledger() creates a ledger; list_ledgers() shows it."""
    from server.main import add_ledger, list_ledgers

    result = add_ledger("Business")
    assert result["status"] == "ok"
    assert "ledger_id" in result
    ledger_id = result["ledger_id"]

    ledgers = list_ledgers()["ledgers"]
    ids = [lg["id"] for lg in ledgers]
    assert ledger_id in ids

    names = [lg["name"] for lg in ledgers]
    assert "Business" in names


def test_add_ledger_empty_name_returns_error(db_path, authed_user):
    """add_ledger('') returns an error."""
    from server.main import add_ledger

    result = add_ledger("")
    assert result["status"] == "error"


def test_add_ledger_duplicate_returns_error(db_path, authed_user):
    """add_ledger() twice with the same name returns error on second call."""
    from server.main import add_ledger

    add_ledger("Savings")
    result = add_ledger("Savings")
    assert result["status"] == "error"


def test_add_ledger_no_active_user(db_path):
    """add_ledger() with no active session returns an error."""
    from server.main import add_ledger

    result = add_ledger("NoUser")
    assert result["status"] == "error"


# ---------------------------------------------------------------------------
# Test: add_line_item adds to correct ledger with correct type
# ---------------------------------------------------------------------------


def test_add_line_item_income(db_path, authed_user):
    """add_line_item() with type='income' creates and returns item_id."""
    from server.main import add_ledger, add_line_item, list_ledgers

    add_result = add_ledger("Work")
    ledger_id = add_result["ledger_id"]

    result = add_line_item(ledger_id=ledger_id, name="Freelance", item_type="income")
    assert result["status"] == "ok"
    assert "item_id" in result

    # Verify it appears in list_ledgers
    ledgers = list_ledgers()["ledgers"]
    work = next(lg for lg in ledgers if lg["id"] == ledger_id)
    items = {i["name"]: i for i in work["items"]}
    assert "Freelance" in items
    assert items["Freelance"]["type"] == "income"


def test_add_line_item_expense(db_path, authed_user):
    """add_line_item() with type='expense' creates the item correctly."""
    from server.main import add_ledger, add_line_item, list_ledgers

    ledger_id = add_ledger("Personal2")["ledger_id"]
    result = add_line_item(ledger_id=ledger_id, name="Rent", item_type="expense")
    assert result["status"] == "ok"

    ledgers = list_ledgers()["ledgers"]
    ledger = next(lg for lg in ledgers if lg["id"] == ledger_id)
    items = {i["name"]: i for i in ledger["items"]}
    assert items["Rent"]["type"] == "expense"


def test_add_line_item_invalid_type(db_path, authed_user):
    """add_line_item() with invalid item_type returns error."""
    from server.main import add_ledger, add_line_item

    ledger_id = add_ledger("Test")["ledger_id"]
    result = add_line_item(ledger_id=ledger_id, name="Misc", item_type="invalid")
    assert result["status"] == "error"


def test_add_line_item_wrong_ledger(db_path, authed_user):
    """add_line_item() with unknown ledger_id returns error."""
    from server.main import add_line_item

    result = add_line_item(ledger_id=_uid(), name="Anything", item_type="expense")
    assert result["status"] == "error"


# ---------------------------------------------------------------------------
# Test: remove_line_item works when no entries attached
# ---------------------------------------------------------------------------


def test_remove_line_item_no_entries(db_path, authed_user):
    """remove_line_item() deletes item and returns ok when no entries attached."""
    from server.main import add_ledger, add_line_item, list_ledgers, remove_line_item

    ledger_id = add_ledger("Temp")["ledger_id"]
    item_id = add_line_item(ledger_id=ledger_id, name="TempItem", item_type="expense")["item_id"]

    result = remove_line_item(id=item_id)
    assert result == {"status": "ok"}

    # Verify it's gone from list_ledgers
    ledgers = list_ledgers()["ledgers"]
    temp = next((lg for lg in ledgers if lg["id"] == ledger_id), None)
    if temp:
        item_ids = [i["id"] for i in temp["items"]]
        assert item_id not in item_ids


# ---------------------------------------------------------------------------
# Test: remove_line_item returns error when entries exist
# ---------------------------------------------------------------------------


def test_remove_line_item_with_entries(db_path, authed_user):
    """remove_line_item() returns error when transaction_entries reference the item."""
    from server.main import add_ledger, add_line_item, remove_line_item

    ledger_id = add_ledger("WithEntries")["ledger_id"]
    item_id = add_line_item(ledger_id=ledger_id, name="LinkedItem", item_type="expense")["item_id"]

    # Manually attach a transaction entry referencing this item
    conn = get_db(db_path)
    txn_id = _uid()
    conn.execute(
        "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
        (txn_id, "2026-01-01", "TestMerchant", 100.0),
    )
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (_uid(), txn_id, ledger_id, item_id, 100.0, "rule", 0),
    )
    conn.commit()
    conn.close()

    result = remove_line_item(id=item_id)
    assert result["status"] == "error"
    assert "attached entries" in result["message"].lower() or "entries" in result["message"].lower()


# ---------------------------------------------------------------------------
# Test: remove_line_item with non-existent id
# ---------------------------------------------------------------------------


def test_remove_line_item_not_found(db_path, authed_user):
    """remove_line_item() returns error for unknown item id."""
    from server.main import remove_line_item

    result = remove_line_item(id=_uid())
    assert result["status"] == "error"
