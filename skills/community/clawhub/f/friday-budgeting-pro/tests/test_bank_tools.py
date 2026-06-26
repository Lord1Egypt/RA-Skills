"""
tests/test_bank_tools.py — Tests for the bank-connection MCP tools in server/main.py.

Uses a tmp_path SQLite DB (monkeypatching server.paths.DB_PATH) so no real
Keychain or Plaid network calls are made.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    """Create a fresh temp DB and monkeypatch server.paths.DB_PATH to point at it."""
    path = tmp_path / "test.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture(autouse=True)
def patch_crypto(monkeypatch):
    """Patch encrypt/decrypt with transparent passthrough fakes."""
    fake_encrypt = MagicMock(side_effect=lambda plaintext: "enc:" + plaintext)
    fake_decrypt = MagicMock(side_effect=lambda ciphertext: ciphertext[len("enc:") :])
    monkeypatch.setattr("server.crypto.encrypt", fake_encrypt)
    monkeypatch.setattr("server.crypto.decrypt", fake_decrypt)


# ---------------------------------------------------------------------------
# start_link
# ---------------------------------------------------------------------------


def test_start_link_returns_url_with_link_token(db_path):
    with patch(
        "server.providers.plaid.PlaidProvider.create_link_token", return_value="link-token-abc"
    ) as mock_create:
        from server.main import start_link

        result = start_link()

    assert "url" in result
    assert "link-token-abc" in result["url"]
    mock_create.assert_called_once()


# ---------------------------------------------------------------------------
# complete_link
# ---------------------------------------------------------------------------


def test_complete_link_inserts_row_and_returns_connection_id(db_path):
    exchange_result = {"access_token": "access-sandbox-xyz", "item_id": "item-abc"}

    with patch(
        "server.providers.plaid.PlaidProvider.exchange_public_token", return_value=exchange_result
    ) as mock_exchange:
        from server.main import complete_link

        result = complete_link("public-token-test")

    assert "connection_id" in result
    connection_id = result["connection_id"]
    assert result["institution_name"] is None
    mock_exchange.assert_called_once_with("public-token-test")

    # Verify the row was inserted and the encrypted token is stored
    conn = get_db(db_path)
    row = conn.execute("SELECT * FROM bank_connections WHERE id = ?", (connection_id,)).fetchone()
    conn.close()

    assert row is not None
    assert row["plaid_item_id"] == "item-abc"
    assert row["plaid_access_token_encrypted"] == "enc:access-sandbox-xyz"
    assert row["status"] == "active"
    # Encrypted token must NOT be the plaintext
    assert row["plaid_access_token_encrypted"] != "access-sandbox-xyz"


# ---------------------------------------------------------------------------
# list_connections
# ---------------------------------------------------------------------------


def test_list_connections_returns_all_without_encrypted_token(db_path):
    exchange_result_1 = {"access_token": "access-1", "item_id": "item-1"}
    exchange_result_2 = {"access_token": "access-2", "item_id": "item-2"}

    with patch(
        "server.providers.plaid.PlaidProvider.exchange_public_token",
        side_effect=[exchange_result_1, exchange_result_2],
    ):
        from server.main import complete_link, list_connections

        complete_link("public-token-1")
        complete_link("public-token-2")

    result = list_connections()

    assert "connections" in result
    assert len(result["connections"]) == 2

    for conn_entry in result["connections"]:
        # Required fields present
        assert "id" in conn_entry
        assert "institution_name" in conn_entry
        assert "status" in conn_entry
        assert "last_synced_at" in conn_entry
        # Encrypted token must NEVER appear
        assert "plaid_access_token_encrypted" not in conn_entry


# ---------------------------------------------------------------------------
# disconnect
# ---------------------------------------------------------------------------


def test_disconnect_removes_connection_and_sync_cursor(db_path):
    exchange_result = {"access_token": "access-del", "item_id": "item-del"}

    with patch(
        "server.providers.plaid.PlaidProvider.exchange_public_token", return_value=exchange_result
    ):
        from server.main import complete_link

        result = complete_link("public-token-del")

    connection_id = result["connection_id"]

    # Insert a sync_cursor row for this connection
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO sync_cursors (connection_id, cursor) VALUES (?, ?)",
        (connection_id, "cursor-val"),
    )
    conn.commit()
    conn.close()

    from server.main import disconnect

    disconnect_result = disconnect(connection_id)
    assert disconnect_result == {"ok": True}

    # Verify both rows are gone
    conn = get_db(db_path)
    bc_row = conn.execute(
        "SELECT id FROM bank_connections WHERE id = ?", (connection_id,)
    ).fetchone()
    sc_row = conn.execute(
        "SELECT connection_id FROM sync_cursors WHERE connection_id = ?", (connection_id,)
    ).fetchone()
    conn.close()

    assert bc_row is None
    assert sc_row is None


# ---------------------------------------------------------------------------
# refresh_connection
# ---------------------------------------------------------------------------


def test_refresh_connection_returns_url_with_link_token(db_path):
    with patch(
        "server.providers.plaid.PlaidProvider.create_link_token", return_value="link-update-token"
    ) as mock_create:
        from server.main import refresh_connection

        result = refresh_connection("any-connection-id")

    assert "url" in result
    assert "link-update-token" in result["url"]
    mock_create.assert_called_once()
