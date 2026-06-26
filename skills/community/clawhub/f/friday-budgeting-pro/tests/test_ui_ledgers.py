"""
tests/test_ui_ledgers.py — Tests for the /ledgers CRUD endpoints (issue #48).

Uses the same fixture pattern as tests/test_ui_routes.py.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixtures (mirrors test_ui_routes.py)
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    from ui.server import app

    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def authed_client(db_path: Path) -> TestClient:
    from ui.server import app

    c = TestClient(app, follow_redirects=False)
    _complete_setup(c)
    return _login(c)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _complete_setup(client: TestClient, password: str = "testpass123") -> None:
    r = client.post("/setup/1", data={"password": password, "password_confirm": password})
    assert r.status_code == 200
    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302


def _login(client: TestClient, password: str = "testpass123") -> TestClient:
    r = client.post("/login", data={"password": password})
    assert r.status_code == 302
    return client


def _insert_ledger(db_path: Path, name: str = "Personal") -> str:
    """Directly insert a ledger into the DB and return its id."""
    from server.db import get_db

    lid = str(uuid.uuid4())
    conn = get_db(db_path)
    try:
        conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (lid, name))
        conn.commit()
    finally:
        conn.close()
    return lid


def _insert_item(db_path: Path, ledger_id: str, name: str, item_type: str = "expense") -> str:
    from server.db import get_db

    iid = str(uuid.uuid4())
    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (iid, ledger_id, name, item_type),
        )
        conn.commit()
    finally:
        conn.close()
    return iid


# ---------------------------------------------------------------------------
# Tests — auth guard
# ---------------------------------------------------------------------------


class TestAuthGuard:
    def test_get_ledgers_unauthenticated_redirects(self, client):
        r = client.get("/ledgers")
        assert r.status_code == 302
        assert r.headers["location"] == "/login"

    def test_post_ledgers_unauthenticated_returns_401(self, client):
        r = client.post("/ledgers", json={"name": "Test"})
        assert r.status_code == 401

    def test_delete_ledger_unauthenticated_returns_401(self, client, db_path):
        lid = _insert_ledger(db_path)
        r = client.delete(f"/ledgers/{lid}")
        assert r.status_code == 401

    def test_patch_ledger_unauthenticated_returns_401(self, client, db_path):
        lid = _insert_ledger(db_path)
        r = client.patch(f"/ledgers/{lid}", json={"name": "New"})
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Tests — GET /ledgers
# ---------------------------------------------------------------------------


class TestGetLedgers:
    def test_ledgers_page_renders(self, authed_client, db_path):
        # setup wizard creates a Personal ledger with Salary (income) + 9 expenses
        r = authed_client.get("/ledgers")
        assert r.status_code == 200
        assert "Income" in r.text
        assert "Expenses" in r.text

    def test_ledgers_page_shows_ledger_name(self, authed_client, db_path):
        # setup creates Personal; insert another one
        _insert_ledger(db_path, "MyLedger")
        r = authed_client.get("/ledgers")
        assert r.status_code == 200
        assert "MyLedger" in r.text

    def test_ledgers_page_shows_line_items(self, authed_client, db_path):
        # setup creates Personal with Salary + Groceries already
        r = authed_client.get("/ledgers")
        assert r.status_code == 200
        assert "Salary" in r.text
        assert "Groceries" in r.text


# ---------------------------------------------------------------------------
# Tests — POST /ledgers
# ---------------------------------------------------------------------------


class TestCreateLedger:
    def test_create_ledger_returns_201(self, authed_client):
        r = authed_client.post("/ledgers", json={"name": "Business"})
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == "Business"
        assert "id" in data

    def test_create_ledger_missing_name_returns_400(self, authed_client):
        r = authed_client.post("/ledgers", json={})
        assert r.status_code == 400

    def test_create_ledger_blank_name_returns_400(self, authed_client):
        r = authed_client.post("/ledgers", json={"name": "  "})
        assert r.status_code == 400

    def test_create_ledger_persists(self, authed_client, db_path):
        authed_client.post("/ledgers", json={"name": "Rental"})
        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT name FROM ledgers WHERE name='Rental'").fetchone()
        finally:
            conn.close()
        assert row is not None


# ---------------------------------------------------------------------------
# Tests — DELETE /ledgers/{ledger_id}
# ---------------------------------------------------------------------------


class TestDeleteLedger:
    def test_delete_ledger_success(self, authed_client, db_path):
        # setup created Personal; insert a second ledger to delete
        lid2 = _insert_ledger(db_path, "Business")
        r = authed_client.delete(f"/ledgers/{lid2}")
        assert r.status_code == 200

    def test_delete_only_ledger_returns_409(self, authed_client, db_path):
        # setup creates Personal ledger; use that one (it's the only ledger)
        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT id FROM ledgers WHERE name='Personal'").fetchone()
        finally:
            conn.close()
        assert row is not None, "Expected Personal ledger from setup"
        r = authed_client.delete(f"/ledgers/{row['id']}")
        assert r.status_code == 409

    def test_delete_ledger_removes_line_items(self, authed_client, db_path):
        # setup already created Personal; add a second ledger to delete
        lid2 = _insert_ledger(db_path, "Business")
        iid = _insert_item(db_path, lid2, "Office", "expense")
        authed_client.delete(f"/ledgers/{lid2}")
        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT id FROM line_items WHERE id=?", (iid,)).fetchone()
        finally:
            conn.close()
        assert row is None


# ---------------------------------------------------------------------------
# Tests — PATCH /ledgers/{ledger_id}
# ---------------------------------------------------------------------------


class TestRenameLedger:
    def test_rename_ledger_success(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Old Name")
        r = authed_client.patch(f"/ledgers/{lid}", json={"name": "New Name"})
        assert r.status_code == 200
        assert r.json()["name"] == "New Name"

    def test_rename_ledger_missing_name_returns_400(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Test")
        r = authed_client.patch(f"/ledgers/{lid}", json={})
        assert r.status_code == 400

    def test_rename_ledger_not_found_returns_404(self, authed_client):
        r = authed_client.patch("/ledgers/nonexistent-id", json={"name": "X"})
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Tests — POST /ledgers/{ledger_id}/items
# ---------------------------------------------------------------------------


class TestCreateItem:
    def test_add_income_item(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        r = authed_client.post(
            f"/ledgers/{lid}/items", json={"name": "Salary", "section": "income"}
        )
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == "Salary"
        assert data["item_type"] == "income"

    def test_add_expense_item(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        r = authed_client.post(
            f"/ledgers/{lid}/items", json={"name": "Groceries", "section": "expenses"}
        )
        assert r.status_code == 201
        data = r.json()
        assert data["item_type"] == "expense"

    def test_add_item_missing_name_returns_400(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        r = authed_client.post(f"/ledgers/{lid}/items", json={"section": "expenses"})
        assert r.status_code == 400

    def test_add_item_ledger_not_found_returns_404(self, authed_client):
        r = authed_client.post(
            "/ledgers/nonexistent/items", json={"name": "X", "section": "expenses"}
        )
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Tests — PATCH /ledgers/{ledger_id}/items/{item_id}
# ---------------------------------------------------------------------------


class TestRenameItem:
    def test_rename_item_success(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        iid = _insert_item(db_path, lid, "Groceries", "expense")
        r = authed_client.patch(f"/ledgers/{lid}/items/{iid}", json={"name": "Food"})
        assert r.status_code == 200
        assert r.json()["name"] == "Food"

    def test_rename_item_missing_name_returns_400(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        iid = _insert_item(db_path, lid, "Groceries", "expense")
        r = authed_client.patch(f"/ledgers/{lid}/items/{iid}", json={})
        assert r.status_code == 400

    def test_rename_item_not_found_returns_404(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        r = authed_client.patch(f"/ledgers/{lid}/items/nonexistent", json={"name": "X"})
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Tests — DELETE /ledgers/{ledger_id}/items/{item_id}
# ---------------------------------------------------------------------------


class TestDeleteItem:
    def test_delete_item_success(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        iid = _insert_item(db_path, lid, "Groceries", "expense")
        r = authed_client.delete(f"/ledgers/{lid}/items/{iid}")
        assert r.status_code == 200

    def test_delete_item_not_found_returns_404(self, authed_client, db_path):
        lid = _insert_ledger(db_path, "Personal")
        r = authed_client.delete(f"/ledgers/{lid}/items/nonexistent")
        assert r.status_code == 404

    def test_delete_item_with_entries_returns_409(self, authed_client, db_path):
        from server.db import get_db

        lid = _insert_ledger(db_path, "Personal")
        iid = _insert_item(db_path, lid, "Groceries", "expense")
        # Insert a dummy transaction_entry referencing this item
        conn = get_db(db_path)
        try:
            entry_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO transaction_entries (id, transaction_id, ledger_id, line_item_id, amount)"
                " VALUES (?, NULL, ?, ?, 10.0)",
                (entry_id, lid, iid),
            )
            conn.commit()
        finally:
            conn.close()
        r = authed_client.delete(f"/ledgers/{lid}/items/{iid}")
        assert r.status_code == 409
        assert "entry_count" in r.json()

    def test_delete_item_with_entries_confirm_true_succeeds(self, authed_client, db_path):
        from server.db import get_db

        lid = _insert_ledger(db_path, "Personal")
        iid = _insert_item(db_path, lid, "Groceries", "expense")
        conn = get_db(db_path)
        try:
            entry_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO transaction_entries (id, transaction_id, ledger_id, line_item_id, amount)"
                " VALUES (?, NULL, ?, ?, 10.0)",
                (entry_id, lid, iid),
            )
            conn.commit()
        finally:
            conn.close()
        r = authed_client.delete(f"/ledgers/{lid}/items/{iid}?confirm=true")
        assert r.status_code == 200
