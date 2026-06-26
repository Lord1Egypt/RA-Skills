"""
tests/playwright/test_issue_209_correction_rules.py
====================================================

End-to-end verification for issue #209 — Manual correction triggers rule
evaluation.

What this test does:

  1. Spin up a fresh temp ``FRIDAY_BP_APP_DIR`` (no live data touched).
  2. Initialise DB, create a user, seed Personal ledger via apply_initial_setup.
  3. Mint a Plaid sandbox public token, exchange it, and sync transactions.
  4. Patch the LLM so all transactions are classified to a known expense line
     item (li_A).
  5. Test A — Conflicting routing_rule detection:
     - Insert a routing_rule pointing merchant → li_A (wrong; we'll correct to li_B).
     - Call correct_transaction(tx_id, li_B).
     - Assert response contains rule_suggestions with action='update_or_disable_rule'.
     - Assert rule_id matches the inserted routing_rule.
  6. Test B — Create-rule suggestion for recurring merchant:
     - Ensure 2+ transactions exist for the same merchant (no routing_rule).
     - Call correct_transaction on one of them to li_B.
     - Assert response contains rule_suggestions with action='create_rule'.
     - Assert suggested_description contains '[from-correction]'.
  7. Start the FastAPI UI and use Playwright to screenshot the Accounts page
     as a visual artefact.

Skipped when:
  - PLAID_CLIENT_ID / PLAID_SECRET not set, OR
  - playwright not installed / browser binary missing.
"""

from __future__ import annotations

import os
import socket
import threading
import time
import uuid
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Skip guards
# ---------------------------------------------------------------------------

os.environ.setdefault("PLAID_CLIENT_ID", "6a108c2ccfbb2f000d022c26")
os.environ.setdefault("PLAID_SECRET", "7ed0d08cc23ca47f6b550504f314ab")
os.environ.setdefault("PLAID_ENV", "sandbox")

PLAID_CREDS = bool(os.environ.get("PLAID_CLIENT_ID")) and bool(os.environ.get("PLAID_SECRET"))

try:
    from playwright.sync_api import sync_playwright  # noqa: F401

    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False

pytestmark = [
    pytest.mark.skipif(
        not PLAID_CREDS,
        reason="Plaid sandbox creds not set (PLAID_CLIENT_ID/PLAID_SECRET).",
    ),
    pytest.mark.skipif(
        not PLAYWRIGHT_AVAILABLE,
        reason="playwright not installed.",
    ),
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_app_dir(tmp_path, monkeypatch):
    """Redirect ~/.friday-bp/ to a temp directory and reload server.paths."""
    app_dir = tmp_path / "friday-bp"
    app_dir.mkdir(mode=0o700)
    monkeypatch.setenv("FRIDAY_BP_APP_DIR", str(app_dir))

    import importlib

    import server.paths as _paths

    importlib.reload(_paths)
    import server.db as _db

    importlib.reload(_db)
    import ui.auth as _auth

    importlib.reload(_auth)
    import server.main as _main

    importlib.reload(_main)

    _db.init_db(_paths.DB_PATH)
    yield {
        "app_dir": app_dir,
        "db_path": _paths.DB_PATH,
        "paths": _paths,
        "db": _db,
        "auth": _auth,
        "main": _main,
    }


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# End-to-end test
# ---------------------------------------------------------------------------


def test_issue_209_correction_rule_evaluation(tmp_app_dir, monkeypatch):
    """Sync → correct → rule suggestions returned; Playwright screenshots Accounts."""
    from unittest.mock import patch

    paths = tmp_app_dir["paths"]
    db = tmp_app_dir["db"]
    auth = tmp_app_dir["auth"]
    main = tmp_app_dir["main"]

    # ------------------------------------------------------------------
    # 1. Create user and seed ledger.
    # ------------------------------------------------------------------
    user_id = auth.create_user(paths.DB_PATH, "testuser209", "strongpass-209")
    assert user_id

    setup_result = main.apply_initial_setup()
    assert setup_result.get("status") == "ok", setup_result

    conn = db.get_db(paths.DB_PATH)
    try:
        rows = conn.execute(
            "SELECT id, name, item_type FROM line_items "
            "WHERE ledger_id IN (SELECT id FROM ledgers WHERE user_id = ?)",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    li_expense = next((r["id"] for r in rows if r["item_type"] == "expense"), None)
    li_income = next((r["id"] for r in rows if r["item_type"] == "income"), None)
    assert (
        li_expense and li_income
    ), f"expected expense+income line items after apply_initial_setup; got {rows!r}"

    # ------------------------------------------------------------------
    # 2. Mint sandbox public token and sync.
    # ------------------------------------------------------------------
    from plaid.model.products import Products
    from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest

    from server.providers.plaid import PlaidProvider

    provider = PlaidProvider(env="sandbox")
    api_client = provider._build_client()
    sandbox_resp = api_client.sandbox_public_token_create(
        SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",
            initial_products=[Products("transactions")],
        )
    )
    public_token = sandbox_resp["public_token"]

    link_result = main.complete_link(public_token=public_token, plaid_env="sandbox")
    assert "connection_id" in link_result, link_result

    # Patch LLM → classify all transactions to li_expense.
    import json

    def _fake_chat(messages, *, model=None, **kw):
        return json.dumps(
            {
                "line_item_id": li_expense,
                "reasoning": "test: patched to expense",
                "confidence": 0.99,
                "uncertain": False,
                "entry_type": "expense",
            }
        )

    with patch("server.llm.chat", side_effect=_fake_chat):
        sync_result = main.sync()

    assert sync_result.get("status") == "ok", sync_result

    # ------------------------------------------------------------------
    # 3. Seed synthetic transactions for the rule-evaluation assertions.
    #    We always create our own so the test doesn't depend on Plaid
    #    sandbox returning transactions with a specific merchant pattern.
    # ------------------------------------------------------------------
    conn = db.get_db(paths.DB_PATH)
    try:
        # Find an account created by complete_link / sync, or create one.
        account_row = conn.execute(
            "SELECT ba.id FROM bank_accounts ba "
            "JOIN bank_connections bc ON bc.id = ba.connection_id "
            "WHERE bc.user_id = ? LIMIT 1",
            (user_id,),
        ).fetchone()

        if account_row:
            account_id = account_row["id"]
        else:
            # Fallback: insert a minimal bank connection + account.
            bc_id = _uid()
            account_id = _uid()
            conn.execute(
                "INSERT INTO bank_connections "
                "(id, plaid_access_token_encrypted, status, user_id, institution_name) "
                "VALUES (?, 'enc:synthetic', 'active', ?, 'Synthetic Bank')",
                (bc_id, user_id),
            )
            conn.execute(
                "INSERT INTO bank_accounts (id, connection_id, name) VALUES (?, ?, ?)",
                (account_id, bc_id, "Chequing"),
            )

        ledger_id = conn.execute(
            "SELECT id FROM ledgers WHERE user_id = ? LIMIT 1", (user_id,)
        ).fetchone()["id"]

        recurring_merchant = "SyntheticMerchant209"
        tx_id_a = _uid()
        tx_id_b = _uid()
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount, bank_account_id) "
            "VALUES (?, '2026-05-10', ?, 50.0, ?)",
            (tx_id_a, recurring_merchant, account_id),
        )
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount, bank_account_id) "
            "VALUES (?, '2026-05-11', ?, 55.0, ?)",
            (tx_id_b, recurring_merchant, account_id),
        )
        # Entries classified to li_expense
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
            "VALUES (?, ?, ?, ?, 50.0, 'llm', 0)",
            (_uid(), tx_id_a, ledger_id, li_expense),
        )
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
            "VALUES (?, ?, ?, ?, 55.0, 'llm', 0)",
            (_uid(), tx_id_b, ledger_id, li_expense),
        )
        conn.commit()
    finally:
        conn.close()

    # ------------------------------------------------------------------
    # TEST A: Conflicting routing_rule detection.
    # ------------------------------------------------------------------
    # Insert a routing_rule for this merchant pointing to li_expense (wrong).
    conflict_rule_id = _uid()
    conn = db.get_db(paths.DB_PATH)
    try:
        conn.execute(
            "INSERT INTO routing_rules (id, merchant_pattern, line_item_id) VALUES (?, ?, ?)",
            (conflict_rule_id, recurring_merchant, li_expense),
        )
        conn.commit()
    finally:
        conn.close()

    # Correct tx_id_a to li_income — the routing rule now conflicts.
    result_a = main.correct_transaction(
        transaction_id=tx_id_a,
        line_item_id=li_income,
    )
    assert result_a["status"] == "ok", result_a
    assert "rule_suggestions" in result_a, "rule_suggestions key missing from response"

    conflict_suggestions = [
        s for s in result_a["rule_suggestions"] if s["action"] == "update_or_disable_rule"
    ]
    assert (
        len(conflict_suggestions) >= 1
    ), f"Expected at least 1 update_or_disable_rule suggestion; got {result_a['rule_suggestions']!r}"
    matched = next((s for s in conflict_suggestions if s["rule_id"] == conflict_rule_id), None)
    assert (
        matched is not None
    ), f"Conflicting rule {conflict_rule_id!r} not in suggestions: {conflict_suggestions!r}"
    assert matched["suggested_line_item_id"] == li_income
    assert "reason" in matched

    # ------------------------------------------------------------------
    # TEST B: Create-rule suggestion for recurring merchant (no routing_rule).
    # ------------------------------------------------------------------
    # Remove the conflicting routing rule so it doesn't suppress the create suggestion.
    conn = db.get_db(paths.DB_PATH)
    try:
        conn.execute("DELETE FROM routing_rules WHERE id = ?", (conflict_rule_id,))
        conn.commit()
    finally:
        conn.close()

    # Correct tx_id_b (no existing routing rule, merchant appears 2+ times).
    result_b = main.correct_transaction(
        transaction_id=tx_id_b,
        line_item_id=li_income,
    )
    assert result_b["status"] == "ok", result_b
    assert "rule_suggestions" in result_b

    create_suggestions = [s for s in result_b["rule_suggestions"] if s["action"] == "create_rule"]
    assert (
        len(create_suggestions) >= 1
    ), f"Expected at least 1 create_rule suggestion; got {result_b['rule_suggestions']!r}"
    cs = create_suggestions[0]
    assert cs["merchant"] == recurring_merchant
    assert cs["suggested_line_item_id"] == li_income
    assert cs["occurrence_count"] >= 2
    assert (
        "[from-correction]" in cs["suggested_description"]
    ), f"suggested_description missing [from-correction] tag: {cs['suggested_description']!r}"

    # ------------------------------------------------------------------
    # TEST C: Playwright — screenshot Accounts page as visual artefact.
    # ------------------------------------------------------------------
    import uvicorn

    from ui.server import app as fastapi_app

    screenshots_dir = Path(__file__).parent / "_screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    port = _free_port()
    config = uvicorn.Config(fastapi_app, host="127.0.0.1", port=port, log_level="warning")
    server_inst = uvicorn.Server(config)
    thread = threading.Thread(target=server_inst.run, daemon=True)
    thread.start()

    # Wait for server to be ready.
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            import urllib.request

            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
            break
        except Exception:
            time.sleep(0.2)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/accounts", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=10000)
            page.screenshot(
                path=str(screenshots_dir / "issue_209_accounts.png"),
                full_page=True,
            )
            browser.close()
    finally:
        server_inst.should_exit = True
        thread.join(timeout=5)
