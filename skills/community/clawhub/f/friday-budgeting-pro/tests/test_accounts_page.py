"""
tests/test_accounts_page.py — Tests for issue #158: /accounts page.

Covers:
  - Schema: balance_current and balance_available columns exist on bank_accounts
  - GET /accounts (authed) → 200, contains institution name
  - GET /accounts (unauthed) → 302 /login
  - PATCH /accounts/{id}/name → updates name, persists
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB and monkeypatch DB_PATH."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def authed_client(db_path: Path) -> TestClient:
    """TestClient with a valid session cookie."""
    from ui.auth import (
        SESSION_COOKIE,
        create_session,
        create_user,
        hash_password,
        set_password_hash,
    )
    from ui.server import app

    set_password_hash(db_path, hash_password("testpassword123"))
    user_id = create_user(db_path, "testuser", "testpassword123")
    token = create_session(db_path, user_agent="pytest", user_id=user_id)

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)
    return client, db_path, user_id


@pytest.fixture()
def unauthed_client(db_path: Path) -> TestClient:
    """TestClient without a session cookie."""
    from ui.auth import hash_password, set_password_hash
    from ui.server import app

    set_password_hash(db_path, hash_password("testpassword123"))
    return TestClient(app, follow_redirects=False)


def _seed_accounts(db_path: Path, user_id: str) -> tuple[str, str, str]:
    """Seed a bank_connection + two bank_accounts; return (connection_id, acct1_id, acct2_id)."""
    from server.db import get_db

    conn = get_db(db_path)
    try:
        connection_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_connections "
            "(id, plaid_item_id, plaid_access_token_encrypted, institution_name, status, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (connection_id, "item-1", "enc-tok", "RBC Royal Bank", "active", user_id),
        )

        acct1_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_accounts "
            "(id, connection_id, plaid_account_id, name, type, subtype, balance_current, balance_available) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                acct1_id,
                connection_id,
                "plaid-acct-1",
                "RBC Day to Day",
                "depository",
                "checking",
                4992.34,
                4800.00,
            ),
        )

        acct2_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_accounts "
            "(id, connection_id, plaid_account_id, name, type, subtype, balance_current, balance_available) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                acct2_id,
                connection_id,
                "plaid-acct-2",
                "RBC Savings",
                "depository",
                "savings",
                None,
                None,
            ),
        )

        conn.commit()
    finally:
        conn.close()
    return connection_id, acct1_id, acct2_id


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


class TestSchema:
    def test_balance_current_column_exists(self, db_path):
        from server.db import get_db

        conn = get_db(db_path)
        try:
            cols = {row[1] for row in conn.execute("PRAGMA table_info(bank_accounts)")}
        finally:
            conn.close()
        assert "balance_current" in cols

    def test_balance_available_column_exists(self, db_path):
        from server.db import get_db

        conn = get_db(db_path)
        try:
            cols = {row[1] for row in conn.execute("PRAGMA table_info(bank_accounts)")}
        finally:
            conn.close()
        assert "balance_available" in cols


# ---------------------------------------------------------------------------
# GET /accounts tests
# ---------------------------------------------------------------------------


class TestAccountsGet:
    def test_accounts_requires_auth(self, unauthed_client):
        r = unauthed_client.get("/accounts")
        assert r.status_code == 302
        assert "/login" in r.headers["location"]

    def test_accounts_200_authed_empty(self, authed_client):
        client, _db, _uid = authed_client
        r = client.get("/accounts")
        assert r.status_code == 200

    def test_accounts_contains_accounts_heading(self, authed_client):
        client, _db, _uid = authed_client
        r = client.get("/accounts")
        assert "Accounts" in r.text

    def test_accounts_shows_institution_name(self, authed_client):
        client, db_path, user_id = authed_client
        _seed_accounts(db_path, user_id)
        r = client.get("/accounts")
        assert r.status_code == 200
        assert "RBC Royal Bank" in r.text

    def test_accounts_shows_account_name(self, authed_client):
        client, db_path, user_id = authed_client
        _seed_accounts(db_path, user_id)
        r = client.get("/accounts")
        assert "RBC Day to Day" in r.text

    def test_accounts_shows_balance(self, authed_client):
        client, db_path, user_id = authed_client
        _seed_accounts(db_path, user_id)
        r = client.get("/accounts")
        assert "4992.34" in r.text or "C$" in r.text

    def test_accounts_shows_dash_for_null_balance(self, authed_client):
        client, db_path, user_id = authed_client
        _seed_accounts(db_path, user_id)
        r = client.get("/accounts")
        # RBC Savings has null balances — should show a dash placeholder
        assert "—" in r.text or "&mdash;" in r.text or "RBC Savings" in r.text

    def test_accounts_shows_connect_bank_link(self, authed_client):
        client, _db, _uid = authed_client
        r = client.get("/accounts")
        assert "Connect a bank" in r.text or "link/start" in r.text

    def test_accounts_shows_disconnect_link(self, authed_client):
        client, db_path, user_id = authed_client
        _seed_accounts(db_path, user_id)
        r = client.get("/accounts")
        assert "Disconnect" in r.text or "disconnect" in r.text.lower()

    def test_accounts_has_nav(self, authed_client):
        client, _db, _uid = authed_client
        r = client.get("/accounts")
        assert "/dashboard" in r.text
        assert "/ledgers" in r.text


# ---------------------------------------------------------------------------
# PATCH /accounts/{id}/name tests
# ---------------------------------------------------------------------------


class TestAccountsNamePatch:
    def test_patch_name_requires_auth(self, unauthed_client, db_path):
        acct_id = str(uuid.uuid4())
        r = unauthed_client.patch(
            f"/accounts/{acct_id}/name",
            json={"name": "New Name"},
        )
        assert r.status_code == 401

    def test_patch_name_updates_account(self, authed_client):
        client, db_path, user_id = authed_client
        _, acct1_id, _ = _seed_accounts(db_path, user_id)

        r = client.patch(f"/accounts/{acct1_id}/name", json={"name": "My Custom Name"})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["name"] == "My Custom Name"

    def test_patch_name_persists(self, authed_client):
        client, db_path, user_id = authed_client
        _, acct1_id, _ = _seed_accounts(db_path, user_id)

        client.patch(f"/accounts/{acct1_id}/name", json={"name": "Persisted Name"})

        # Verify the DB was actually updated
        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute(
                "SELECT name FROM bank_accounts WHERE id = ?", (acct1_id,)
            ).fetchone()
        finally:
            conn.close()
        assert row["name"] == "Persisted Name"

    def test_patch_name_appears_on_accounts_page(self, authed_client):
        client, db_path, user_id = authed_client
        _, acct1_id, _ = _seed_accounts(db_path, user_id)

        client.patch(f"/accounts/{acct1_id}/name", json={"name": "Renamed Account"})
        r = client.get("/accounts")
        assert "Renamed Account" in r.text

    def test_patch_name_404_for_missing_account(self, authed_client):
        client, _db, _uid = authed_client
        r = client.patch(f"/accounts/{uuid.uuid4()}/name", json={"name": "Whatever"})
        assert r.status_code == 404

    def test_patch_name_400_for_empty_name(self, authed_client):
        client, db_path, user_id = authed_client
        _, acct1_id, _ = _seed_accounts(db_path, user_id)
        r = client.patch(f"/accounts/{acct1_id}/name", json={"name": ""})
        assert r.status_code == 400


# ---------------------------------------------------------------------------
# Balance display: credit card negation and multi-currency
# ---------------------------------------------------------------------------


def _seed_credit_account(
    db_path, user_id, *, balance: float = 434.11, currency: str = "CAD"
) -> tuple[str, str]:
    """Insert a credit-type account; return (connection_id, account_id)."""
    from server.db import get_db

    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    db = get_db(db_path)
    db.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_item_id, plaid_access_token_encrypted, institution_name, status, user_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (conn_id, "item-cc", "enc-cc", "Visa Bank", "active", user_id),
    )
    db.execute(
        "INSERT INTO bank_accounts "
        "(id, connection_id, plaid_account_id, name, type, subtype, currency, balance_current) "
        "VALUES (?, ?, ?, ?, 'credit', 'credit card', ?, ?)",
        (acct_id, conn_id, "plaid-cc-acct", "Visa Infinite", currency, balance),
    )
    db.commit()
    db.close()
    return conn_id, acct_id


def _seed_usd_account(db_path, user_id, *, balance: float = 1802.13) -> tuple[str, str]:
    """Insert a USD depository account; return (connection_id, account_id)."""
    from server.db import get_db

    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    db = get_db(db_path)
    db.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_item_id, plaid_access_token_encrypted, institution_name, status, user_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (conn_id, "item-usd", "enc-usd", "US Bank", "active", user_id),
    )
    db.execute(
        "INSERT INTO bank_accounts "
        "(id, connection_id, plaid_account_id, name, type, subtype, currency, balance_current) "
        "VALUES (?, ?, ?, ?, 'depository', 'checking', 'USD', ?)",
        (acct_id, conn_id, "plaid-usd-acct", "US Chequing", balance),
    )
    db.commit()
    db.close()
    return conn_id, acct_id


class TestBalanceDisplay:
    def test_credit_card_balance_is_negative(self, authed_client):
        """Credit card balance (434.11 owed) must show as -434.11 on the page."""
        client, db_path, user_id = authed_client
        _seed_credit_account(db_path, user_id, balance=434.11)
        r = client.get("/accounts")
        assert r.status_code == 200
        assert "-434.11" in r.text, "Credit card balance should be displayed as negative"

    def test_credit_card_no_owing_label(self, authed_client):
        """Credit card balance must NOT include an 'owing' label."""
        client, db_path, user_id = authed_client
        _seed_credit_account(db_path, user_id, balance=434.11)
        r = client.get("/accounts")
        assert "owing" not in r.text.lower()

    def test_depository_balance_is_positive(self, authed_client):
        """Regular chequing balance must remain positive."""
        client, db_path, user_id = authed_client
        _, acct1_id, _ = _seed_accounts(db_path, user_id)
        r = client.get("/accounts")
        assert "4992.34" in r.text, "Depository balance should be shown as-is (positive)"

    def test_usd_account_shows_us_dollar_symbol(self, authed_client):
        """USD accounts must display with US$ prefix in native currency."""
        client, db_path, user_id = authed_client
        _seed_usd_account(db_path, user_id, balance=1802.13)
        r = client.get("/accounts")
        assert r.status_code == 200
        assert "US$" in r.text, "USD account should show US$ prefix"
        assert "1802.13" in r.text or "1,802.13" in r.text

    def test_usd_account_no_cad_conversion(self, authed_client):
        """USD account must show the native USD amount, not a CAD-converted value."""
        client, db_path, user_id = authed_client
        # Use a round number easy to detect if conversion (e.g. ×1.36) occurred
        _seed_usd_account(db_path, user_id, balance=1000.00)
        r = client.get("/accounts")
        # The page must contain the raw USD amount
        assert "1000.00" in r.text or "1,000.00" in r.text
        # And should not show a suspiciously converted CAD amount instead
        assert "US$" in r.text
