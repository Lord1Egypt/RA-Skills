"""
tests/test_setup_properties.py — Tests for rental property and investment
account MCP flows (apply_initial_setup).

Note: wizard UI steps 4 (rental properties) and 5 (investments) were removed
when the setup wizard was simplified from 6 steps to 3 steps (#feat/simplify-ui-wizard).
Properties and investment ledgers are now set up post-setup via MCP tools
(create_property_ledger / create_investment_ledger).

Covers:
  MCP layer (apply_initial_setup):
    - rental_properties creates ledger + links account
    - investment_account_ids creates investment ledger + links all accounts
    - both at once: properties first, then investments
    - empty lists are no-ops for the new params
    - missing account_id in property dict skips set_account_ledger
"""

from __future__ import annotations

import uuid

import pytest

import server.main
import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Fixtures — MCP layer
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_db(tmp_path, monkeypatch):
    """Fresh DB with an active user; patches DB_PATH and cron home."""
    db_file = tmp_path / "test.db"
    monkeypatch.setattr(server.paths, "DB_PATH", db_file)
    init_db(db_file)

    # Disable cron registration for all tests.
    monkeypatch.setattr(server.main, "_OPENCLAW_HOME", tmp_path / "dot-openclaw-absent")

    # Insert a user so get_active_user_id returns something.
    from ui.auth import create_user

    create_user(db_file, "testuser", "securepass1")

    return db_file


def _make_bank_account(
    db_file, user_id: str | None = None, acct_type: str = "checking", institution: str = "TD Bank"
) -> str:
    """Insert a minimal bank_connection + bank_account; return account id."""
    conn = get_db(db_file)
    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_item_id, plaid_access_token_encrypted, user_id, institution_name) "
        "VALUES (?, ?, ?, ?, ?)",
        (conn_id, f"item_{conn_id}", "enc_tok", user_id, institution),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name, type) "
        "VALUES (?, ?, ?, ?, ?)",
        (acct_id, conn_id, f"plaid_{acct_id}", "Chequing", acct_type),
    )
    conn.commit()
    conn.close()
    return acct_id


def _get_user_id(db_file) -> str:
    conn = get_db(db_file)
    row = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    conn.close()
    return row["id"]


# ---------------------------------------------------------------------------
# MCP tests — apply_initial_setup with rental_properties
# ---------------------------------------------------------------------------


class TestApplyInitialSetupRentalProperties:
    def test_creates_property_ledger(self, tmp_db):
        uid = _get_user_id(tmp_db)
        acct_id = _make_bank_account(tmp_db, uid)

        result = server.main.apply_initial_setup(
            rental_properties=[
                {"name": "123 Main St", "description": "2-bed condo", "account_id": acct_id}
            ],
            investment_account_ids=[],
        )

        assert result["status"] == "ok"
        assert result["properties_created"] == 1
        assert "123 Main St" in result["ledgers_created"]

        conn = get_db(tmp_db)
        ledger = conn.execute("SELECT id, type FROM ledgers WHERE name = '123 Main St'").fetchone()
        conn.close()
        assert ledger is not None
        assert ledger["type"] == "property"

    def test_links_account_to_property_ledger(self, tmp_db):
        uid = _get_user_id(tmp_db)
        acct_id = _make_bank_account(tmp_db, uid)

        server.main.apply_initial_setup(
            rental_properties=[{"name": "Oak Ave", "account_id": acct_id}],
        )

        conn = get_db(tmp_db)
        row = conn.execute(
            "SELECT ba.default_ledger_id, l.name "
            "FROM bank_accounts ba JOIN ledgers l ON l.id = ba.default_ledger_id "
            "WHERE ba.id = ?",
            (acct_id,),
        ).fetchone()
        conn.close()
        assert row is not None
        assert row["name"] == "Oak Ave"

    def test_no_account_id_skips_link(self, tmp_db):
        result = server.main.apply_initial_setup(
            rental_properties=[{"name": "No Account Prop", "description": "desc"}],
        )
        assert result["status"] == "ok"
        assert result["properties_created"] == 1

    def test_empty_name_skipped(self, tmp_db):
        result = server.main.apply_initial_setup(
            rental_properties=[{"name": "", "account_id": None}],
        )
        assert result["properties_created"] == 0

    def test_empty_list_is_noop(self, tmp_db):
        result = server.main.apply_initial_setup(rental_properties=[])
        assert result["properties_created"] == 0
        assert result["investment_ledger_id"] is None


# ---------------------------------------------------------------------------
# MCP tests — apply_initial_setup with investment_account_ids
# ---------------------------------------------------------------------------


class TestApplyInitialSetupInvestments:
    def test_creates_investment_ledger_and_links_accounts(self, tmp_db):
        uid = _get_user_id(tmp_db)
        acct1 = _make_bank_account(tmp_db, uid, institution="Wealthsimple")
        acct2 = _make_bank_account(tmp_db, uid, institution="Questrade")

        result = server.main.apply_initial_setup(
            investment_account_ids=[acct1, acct2],
        )

        assert result["status"] == "ok"
        assert result["investment_ledger_id"] is not None
        assert "Investments" in result["ledgers_created"]

        conn = get_db(tmp_db)
        # Both accounts should point to the same investment ledger.
        for acct_id in (acct1, acct2):
            row = conn.execute(
                "SELECT default_ledger_id FROM bank_accounts WHERE id = ?", (acct_id,)
            ).fetchone()
            assert row["default_ledger_id"] == result["investment_ledger_id"]
        conn.close()

    def test_empty_list_skips_investment_ledger(self, tmp_db):
        result = server.main.apply_initial_setup(investment_account_ids=[])
        assert result["investment_ledger_id"] is None

        conn = get_db(tmp_db)
        inv = conn.execute("SELECT id FROM ledgers WHERE name = 'Investments'").fetchone()
        conn.close()
        assert inv is None

    def test_none_is_treated_as_empty(self, tmp_db):
        result = server.main.apply_initial_setup(investment_account_ids=None)
        assert result["investment_ledger_id"] is None


# ---------------------------------------------------------------------------
# MCP tests — both at once
# ---------------------------------------------------------------------------


class TestApplyInitialSetupCombined:
    def test_properties_and_investments_together(self, tmp_db):
        uid = _get_user_id(tmp_db)
        prop_acct = _make_bank_account(tmp_db, uid, institution="RBC")
        inv_acct = _make_bank_account(tmp_db, uid, institution="Wealthsimple")

        result = server.main.apply_initial_setup(
            rental_properties=[{"name": "Elm St", "account_id": prop_acct}],
            investment_account_ids=[inv_acct],
        )

        assert result["status"] == "ok"
        assert result["properties_created"] == 1
        assert result["investment_ledger_id"] is not None
        assert "Elm St" in result["ledgers_created"]
        assert "Investments" in result["ledgers_created"]

        conn = get_db(tmp_db)
        # Property account → Elm St ledger
        elm_ledger = conn.execute("SELECT id FROM ledgers WHERE name = 'Elm St'").fetchone()
        assert elm_ledger is not None
        prop_link = conn.execute(
            "SELECT default_ledger_id FROM bank_accounts WHERE id = ?", (prop_acct,)
        ).fetchone()
        assert prop_link["default_ledger_id"] == elm_ledger["id"]

        # Investment account → Investments ledger
        inv_link = conn.execute(
            "SELECT default_ledger_id FROM bank_accounts WHERE id = ?", (inv_acct,)
        ).fetchone()
        assert inv_link["default_ledger_id"] == result["investment_ledger_id"]
        conn.close()


# (UI wizard tests for steps 4 and 5 were removed in feat/simplify-ui-wizard.
#  Properties and investments are now configured post-setup via MCP tools.
#  See TestApplyInitialSetupRentalProperties / TestApplyInitialSetupInvestments above.)
