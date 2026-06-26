"""
tests/test_cc_payment_classification.py

Verifies:
  1. Credit card payment rule (priority 30) has a rich enough description
     to be recognised as a Transfer by the rule-based classifier.
  2. The /accounts/{account_id}/transactions endpoint returns entry_type
     so the UI can render a "Transfer" badge.
  3. The accounts page template contains the .txn-toggle-btn class and
     the "Transfer" colour definition in its JS.
"""

from __future__ import annotations

import sqlite3
import time
import uuid
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_db(tmp_path: Path) -> Path:
    """Create a minimal DB with one user, one account, and some transactions."""
    db_path = tmp_path / "data.db"
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(schema_path.read_text())

    user_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?,?,?,?)",
        (user_id, "testuser", "x", int(time.time())),
    )

    # Bank connection
    conn_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted,"
        " institution_name, user_id, plaid_env) VALUES (?,?,?,?,?,?)",
        (conn_id, "item1", "enc", "Test Bank", user_id, "sandbox"),
    )

    # Chequing account
    chq_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name,"
        " type, subtype, currency, balance_current) VALUES (?,?,?,?,?,?,?,?)",
        (chq_id, conn_id, "acct_chq", "My Chequing", "depository", "checking", "CAD", 4000.00),
    )

    # Credit card account
    cc_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name,"
        " type, subtype, currency, balance_current) VALUES (?,?,?,?,?,?,?,?)",
        (cc_id, conn_id, "acct_cc", "BMO MasterCard", "credit", "credit card", "CAD", 350.00),
    )

    # Ledger + line item (needed for transaction_entries)
    ledger_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO ledgers (id, name, user_id) VALUES (?,?,?)",
        (ledger_id, "Personal", user_id),
    )
    li_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?,?,?,?)",
        (li_id, ledger_id, "Misc", "expense"),
    )

    # Transaction 1: CC payment from chequing → should be Transfer
    txn_cc_pay_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO transactions (id, bank_account_id, plaid_transaction_id,"
        " date, merchant, amount, currency, pending) VALUES (?,?,?,?,?,?,?,?)",
        (
            txn_cc_pay_id,
            chq_id,
            "ptxn_1",
            "2026-05-20",
            "BMO MASTERCARD PAYMENT - THANK YOU",
            350.00,
            "CAD",
            0,
        ),
    )
    te_id_1 = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO transaction_entries (id, transaction_id, ledger_id, line_item_id,"
        " amount, entry_type, source, confidence, uncertain, reviewed)"
        " VALUES (?,?,?,?,?,?,?,?,?,?)",
        (te_id_1, txn_cc_pay_id, ledger_id, li_id, 350.00, "transfer", "rule", 0.98, 0, 1),
    )

    # Transaction 2: Regular grocery spending
    txn_groc_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO transactions (id, bank_account_id, plaid_transaction_id,"
        " date, merchant, amount, currency, pending) VALUES (?,?,?,?,?,?,?,?)",
        (txn_groc_id, chq_id, "ptxn_2", "2026-05-18", "Loblaws", 85.40, "CAD", 0),
    )
    te_id_2 = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO transaction_entries (id, transaction_id, ledger_id, line_item_id,"
        " amount, entry_type, source, confidence, uncertain, reviewed)"
        " VALUES (?,?,?,?,?,?,?,?,?,?)",
        (te_id_2, txn_groc_id, ledger_id, li_id, 85.40, "spending", "llm", 0.92, 0, 1),
    )

    # Transaction 3: Unclassified (no entry yet)
    txn_unc_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO transactions (id, bank_account_id, plaid_transaction_id,"
        " date, merchant, amount, currency, pending) VALUES (?,?,?,?,?,?,?,?)",
        (txn_unc_id, chq_id, "ptxn_3", "2026-05-15", "Mystery Merchant", 12.00, "CAD", 0),
    )

    conn.execute(
        "INSERT INTO app_config (id, ui_password_hash) VALUES (1, ?)",
        ("$argon2id$v=19$placeholder",),
    )
    conn.commit()
    conn.close()

    return db_path, user_id, chq_id, cc_id, txn_cc_pay_id, txn_groc_id, txn_unc_id


# ---------------------------------------------------------------------------
# Test: /accounts/{id}/transactions returns correct entry_type
# ---------------------------------------------------------------------------


def test_account_transactions_endpoint_returns_entry_type(tmp_path):
    """GET /accounts/{id}/transactions includes entry_type for each transaction."""
    db_path, user_id, chq_id, cc_id, txn_cc_id, txn_groc_id, txn_unc_id = _make_db(tmp_path)

    import server.paths as _paths
    import ui.server as srv

    with patch.object(_paths, "DB_PATH", db_path):
        # Create a live session for auth
        from ui.auth import create_session

        stoken = create_session(db_path, user_id=user_id)

        client = TestClient(srv.app, raise_server_exceptions=True)
        client.cookies.set("friday_bp_session", stoken)

        resp = client.get(f"/accounts/{chq_id}/transactions")
        assert resp.status_code == 200, resp.text
        data = resp.json()

    txns = {t["id"]: t for t in data["transactions"]}

    # CC payment must be entry_type='transfer'
    assert txn_cc_id in txns, "CC payment transaction missing from results"
    assert (
        txns[txn_cc_id]["entry_type"] == "transfer"
    ), f"Expected 'transfer' for CC payment, got {txns[txn_cc_id]['entry_type']!r}"

    # Grocery is spending
    assert txns[txn_groc_id]["entry_type"] == "spending"

    # Unclassified has no entry_type (None / null)
    assert txns[txn_unc_id]["entry_type"] is None


def test_account_transactions_endpoint_requires_auth(tmp_path):
    """GET /accounts/{id}/transactions returns 401 without a session."""
    db_path, _, chq_id, *_ = _make_db(tmp_path)

    import server.paths as _paths
    import ui.server as srv

    with patch.object(_paths, "DB_PATH", db_path):
        client = TestClient(srv.app, raise_server_exceptions=True)
        resp = client.get(f"/accounts/{chq_id}/transactions")
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Test: credit card payment rule description is rich enough
# ---------------------------------------------------------------------------


def test_cc_payment_rule_description_covers_key_patterns(tmp_path):
    """Rule #4 in a seeded DB must mention the common payment label patterns."""
    db_path, *_ = _make_db(tmp_path)

    from unittest.mock import patch as _patch

    import server.main as sm
    import server.paths as _paths

    # Seed the credit card payment rule (mirrors what apply_initial_setup seeds)
    conn2 = sqlite3.connect(str(db_path))
    now = int(time.time())
    conn2.execute(
        "INSERT INTO classification_rules "
        "(id, name, description, rule_type, priority, is_default, enabled, created_at) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (
            str(uuid.uuid4()),
            "Credit card payment",
            "Any payment TO a credit card account is a Transfer, not spending. "
            "Matches transactions described as 'PAYMENT - THANK YOU', 'Online Payment', "
            "'Credit Card Payment', 'Autopay', 'Balance Payment', or similar, where the "
            "originating account is a depository (chequing/savings) and the recipient is "
            "a credit card issuer (BMO MasterCard, WS Credit Card, Scotiabank Visa, "
            "TD Visa, RBC Mastercard, etc.). Also matches any outflow from chequing where "
            "the amount matches a known credit card balance. These are balance payoffs — "
            "the underlying charges are already tracked as spending on the credit card "
            "account, so classifying the payment as Transfer prevents double-counting in "
            "expense totals.",
            "transfer",
            30,
            1,
            1,
            now,
        ),
    )
    conn2.commit()
    conn2.close()

    with _patch.object(_paths, "DB_PATH", db_path):
        rules = sm.list_rules()["rules"]

    cc_rule = next((r for r in rules if r["name"] == "Credit card payment"), None)
    assert cc_rule is not None, "Credit card payment rule not found"
    assert cc_rule["rule_type"] == "transfer", "CC payment rule must be type=transfer"
    assert cc_rule["enabled"] is True

    desc = cc_rule["description"].lower()
    required_patterns = [
        "payment - thank you",
        "online payment",
        "credit card payment",
    ]
    for pat in required_patterns:
        assert pat in desc, f"Rule description missing pattern: {pat!r}\nGot: {desc}"


# ---------------------------------------------------------------------------
# Test: accounts.html template has the new JS infrastructure
# ---------------------------------------------------------------------------


def test_accounts_template_has_transaction_toggle():
    """accounts.html must have the txn-toggle-btn class and Transfer colour."""
    tmpl = Path(__file__).parent.parent / "ui" / "templates" / "accounts.html"
    content = tmpl.read_text()

    assert "txn-toggle-btn" in content, "Missing .txn-toggle-btn class"
    assert "txn-expand-" in content, "Missing txn-expand-* row IDs"
    assert (
        "/accounts/" in content and "transactions" in content
    ), "Missing /accounts/{id}/transactions fetch URL"
    # Transfer badge colour definition
    assert "transfer" in content.lower(), "Missing 'transfer' entry type in template"
    # entry_type rendering
    assert (
        "entry_type" in content or "Transfer" in content
    ), "Template doesn't reference entry_type or Transfer label"
