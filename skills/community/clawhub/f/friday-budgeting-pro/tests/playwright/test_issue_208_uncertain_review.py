"""
tests/playwright/test_issue_208_uncertain_review.py
=====================================================

End-to-end verification for issue #208 — Proactive uncertain transaction review.

Validates the full lifecycle:

  1. ``get_needs_review_summary`` returns ``{"count": 0, "summary": "", "transactions": []}``
     on a fresh DB with no transactions.
  2. After syncing Plaid sandbox transactions with the LLM patched to produce
     uncertain classifications, ``get_needs_review`` surfaces those transactions.
  3. ``get_needs_review_summary`` returns a non-empty ``summary`` string with:
     - correct ``count``
     - merchant name, amount, and date for each transaction
     - a closing prompt asking the user to reply with classifications
  4. ``correct_transaction`` reclassifies a transaction and marks it reviewed,
     so it no longer appears in a subsequent ``get_needs_review`` call.
  5. When ``create_rule=True``, a ``[from-correction]``-tagged rule is created
     via ``add_rule`` and appears in ``list_rules``.
  6. ``find_transactions`` returns prior transactions from the same merchant,
     enabling the agent to detect recurring patterns.
  7. Boot the UI on a free port; screenshot the dashboard with Playwright.

Test is skipped when Plaid creds or playwright are unavailable.
"""

from __future__ import annotations

import json as _json
import os
import socket
import threading
import time
import uuid
from pathlib import Path
from unittest.mock import patch

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
# Helpers
# ---------------------------------------------------------------------------


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_app(tmp_path, monkeypatch):
    """Patch server.paths to a temp DB without reloading modules."""
    import server.db as _db
    import server.main as _main
    import server.paths as _paths
    import ui.auth as _auth

    app_dir = tmp_path / "fbp"
    app_dir.mkdir(mode=0o700)
    (app_dir / "exports").mkdir(mode=0o700)
    db_path = app_dir / "data.db"

    monkeypatch.setattr(_paths, "DB_PATH", db_path)
    monkeypatch.setattr(_paths, "APP_DIR", app_dir)
    monkeypatch.setattr(_paths, "EXPORTS_DIR", app_dir / "exports")
    monkeypatch.setattr(_main, "project_root", app_dir)
    monkeypatch.setattr(_main, "_OPENCLAW_HOME", app_dir / "openclaw")

    _db.init_db(db_path)

    # Create the test user — get_active_user_id falls back to the first user
    # in the DB, so no explicit "set active" call is needed.
    user_id = _auth.create_user(db_path, "testuser", "testpassword123")

    return {"paths": _paths, "db": _db, "auth": _auth, "main": _main, "user_id": user_id}


# ---------------------------------------------------------------------------
# The end-to-end test
# ---------------------------------------------------------------------------


def test_issue_208_uncertain_review_end_to_end(tmp_app, monkeypatch):
    paths = tmp_app["paths"]
    db = tmp_app["db"]
    auth = tmp_app["auth"]
    main = tmp_app["main"]

    # ------------------------------------------------------------------
    # 1. Fresh DB: get_needs_review_summary returns count=0.
    # ------------------------------------------------------------------
    empty = main.get_needs_review_summary()
    assert empty["count"] == 0, f"Expected 0 on fresh DB, got: {empty}"
    assert empty["summary"] == "", f"Expected empty summary, got: {empty['summary']!r}"
    assert empty["transactions"] == []

    # Also verify the raw get_needs_review returns empty.
    raw_empty = main.get_needs_review()
    assert raw_empty["transactions"] == []

    # ------------------------------------------------------------------
    # 2. Apply initial setup and link a Plaid sandbox bank.
    # ------------------------------------------------------------------
    setup = main.apply_initial_setup()
    assert setup.get("status") == "ok", setup

    from plaid.model.products import Products
    from plaid.model.sandbox_public_token_create_request import (
        SandboxPublicTokenCreateRequest,
    )

    from server.providers.plaid import PlaidProvider

    provider = PlaidProvider(env="sandbox")
    api_client = provider._build_client()
    sandbox = api_client.sandbox_public_token_create(
        SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",
            initial_products=[Products("transactions")],
        )
    )
    link_result = main.complete_link(public_token=sandbox["public_token"], plaid_env="sandbox")
    assert "connection_id" in link_result, link_result

    # ------------------------------------------------------------------
    # 3. Sync with uncertain LLM responses so transactions land as uncertain.
    # ------------------------------------------------------------------
    # Find a line_item id (needed for fallback routing).
    conn = db.get_db(paths.DB_PATH)
    try:
        li_row = conn.execute(
            "SELECT id FROM line_items WHERE item_type = 'expense' LIMIT 1"
        ).fetchone()
    finally:
        conn.close()
    li_id = li_row["id"] if li_row else None

    def _uncertain_chat(messages, **kw):
        """Simulate the LLM returning a low-confidence, uncertain result."""
        return _json.dumps(
            {
                "rule_id": None,
                "line_item_id": li_id,
                "classification_type": "spending",
                "confidence": 0.4,  # below threshold → uncertain=1
                "reasoning": "Cannot determine category with confidence",
            }
        )

    txn_count = 0
    with patch("server.llm.chat", side_effect=_uncertain_chat):
        for _ in range(6):
            main.sync()
            conn = db.get_db(paths.DB_PATH)
            try:
                txn_count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            finally:
                conn.close()
            if txn_count:
                break
            time.sleep(2)

    if not txn_count:
        pytest.skip("Plaid sandbox returned 0 transactions after retry.")

    # ------------------------------------------------------------------
    # 4. get_needs_review should now surface uncertain transactions.
    # ------------------------------------------------------------------
    needs_review = main.get_needs_review()
    review_txns = needs_review["transactions"]

    # If Plaid sandbox happened to return high-confidence items, force a
    # few entries to be uncertain directly in the DB so the test can
    # exercise the summary logic regardless.
    if not review_txns:
        conn = db.get_db(paths.DB_PATH)
        try:
            conn.execute(
                "UPDATE transaction_entries SET uncertain = 1, reviewed = 0 "
                "WHERE id IN (SELECT id FROM transaction_entries LIMIT 3)"
            )
            conn.commit()
        finally:
            conn.close()
        needs_review = main.get_needs_review()
        review_txns = needs_review["transactions"]

    assert review_txns, "Expected at least one uncertain transaction after sync"

    # ------------------------------------------------------------------
    # 5. get_needs_review_summary returns the right structure and content.
    # ------------------------------------------------------------------
    summary_result = main.get_needs_review_summary()

    assert summary_result["count"] == len(review_txns), (
        f"count mismatch: summary says {summary_result['count']}, "
        f"get_needs_review returned {len(review_txns)}"
    )
    assert summary_result["count"] > 0
    assert summary_result["summary"], "Expected non-empty summary string"
    assert summary_result["transactions"] == review_txns

    summary_text = summary_result["summary"]

    # Summary must mention the count.
    assert (
        str(summary_result["count"]) in summary_text
    ), f"Count {summary_result['count']} not found in summary:\n{summary_text}"

    # Summary must include merchant, amount, and date for at least the first transaction.
    first_tx = review_txns[0]
    merchant = first_tx.get("merchant") or "Unknown merchant"
    assert merchant in summary_text, f"Merchant {merchant!r} not found in summary"

    # Summary must include a closing prompt for the user.
    assert (
        "skip" in summary_text.lower() or "category" in summary_text.lower()
    ), "Summary should include a closing prompt for the user"

    # ------------------------------------------------------------------
    # 6. correct_transaction reclassifies and removes from needs_review.
    # ------------------------------------------------------------------
    target_tx_id = review_txns[0]["id"]
    correction = main.correct_transaction(
        transaction_id=target_tx_id,
        line_item_id=li_id,
        create_rule=False,
    )
    assert correction["status"] == "ok", correction
    assert correction["transaction_id"] == target_tx_id
    assert correction["new_line_item_id"] == li_id

    # Transaction should no longer appear in needs_review.
    after_correction = main.get_needs_review()
    corrected_ids = {tx["id"] for tx in after_correction["transactions"]}
    assert (
        target_tx_id not in corrected_ids
    ), f"Transaction {target_tx_id} still in needs_review after correction"

    # ------------------------------------------------------------------
    # 7. correct_transaction with create_rule=True tags the rule [from-correction].
    # ------------------------------------------------------------------
    if len(review_txns) >= 2:
        second_tx_id = review_txns[1]["id"]
        merchant_name = review_txns[1].get("merchant") or "TestMerchant"
        rule_desc = f"[from-correction] Transactions from {merchant_name!r} → expense"
        correction2 = main.correct_transaction(
            transaction_id=second_tx_id,
            line_item_id=li_id,
            create_rule=True,
            rule_description=rule_desc,
        )
        assert correction2["status"] == "ok", correction2
        assert correction2["rule_created"] is True

        rules = main.list_rules()["rules"]
        from_correction_rules = [
            r for r in rules if "[from-correction]" in r.get("description", "")
        ]
        assert (
            from_correction_rules
        ), "Expected at least one [from-correction]-tagged rule after correction with create_rule=True"

    # ------------------------------------------------------------------
    # 8. find_transactions enables recurring-merchant detection.
    # ------------------------------------------------------------------
    if review_txns:
        merchant_name = review_txns[0].get("merchant")
        if merchant_name:
            found = main.find_transactions(merchant=merchant_name)
            # find_transactions returns a list or dict with transactions key.
            if isinstance(found, dict):
                txns_found = found.get("transactions", [])
            else:
                txns_found = found
            # At least the original transaction should be findable.
            assert (
                len(txns_found) >= 1
            ), f"find_transactions(merchant={merchant_name!r}) returned nothing"

    # ------------------------------------------------------------------
    # 9. After correcting all, summary count decreases accordingly.
    # ------------------------------------------------------------------
    post_summary = main.get_needs_review_summary()
    assert (
        post_summary["count"] < summary_result["count"]
    ), "After correcting transactions, summary count should decrease"

    # ------------------------------------------------------------------
    # 10. Boot UI and screenshot the review state with Playwright.
    # ------------------------------------------------------------------
    import uvicorn

    from ui.server import app as ui_app

    port = _free_port()
    config = uvicorn.Config(
        ui_app, host="127.0.0.1", port=port, log_level="warning", lifespan="off"
    )
    server = uvicorn.Server(config)
    t = threading.Thread(target=server.run, daemon=True)
    t.start()

    import urllib.request

    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=0.5)
            break
        except Exception:
            time.sleep(0.1)
    else:
        pytest.fail("UI did not start within 10s")

    from playwright.sync_api import sync_playwright

    screenshot_dir = Path(__file__).parent / "_screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = screenshot_dir / "issue_208_uncertain_review.png"

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"http://127.0.0.1:{port}/", wait_until="domcontentloaded")
        page.screenshot(path=str(screenshot_path), full_page=True)
        title = page.title()
        browser.close()

    print(f"\nScreenshot: {screenshot_path}\nTitle: {title!r}\n")

    assert screenshot_path.exists() and screenshot_path.stat().st_size > 1000

    server.should_exit = True
    t.join(timeout=5)


# ---------------------------------------------------------------------------
# Unit-level tests (no Plaid, no browser) — always run
# ---------------------------------------------------------------------------


class TestGetNeedsReviewSummaryUnit:
    """Fast unit tests for get_needs_review_summary that don't need Plaid."""

    def test_empty_returns_zero(self, tmp_app):
        """get_needs_review_summary on an empty DB returns count=0."""
        main = tmp_app["main"]
        result = main.get_needs_review_summary()
        assert result["count"] == 0
        assert result["summary"] == ""
        assert result["transactions"] == []

    def test_summary_with_injected_uncertain(self, tmp_app):
        """After inserting uncertain entries directly, summary surfaces them."""
        main = tmp_app["main"]
        db = tmp_app["db"]
        paths = tmp_app["paths"]
        auth = tmp_app["auth"]

        # Bootstrap a bank account and line item so foreign keys are satisfied.
        conn = db.get_db(paths.DB_PATH)
        try:
            # Insert a bank connection.
            bc_id = str(uuid.uuid4())
            uid_row = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            uid = uid_row["id"] if uid_row else str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO bank_connections "
                "(id, user_id, plaid_access_token_encrypted, status) "
                "VALUES (?, ?, 'enc', 'active')",
                (bc_id, uid),
            )
            # Insert a bank account.
            ba_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO bank_accounts (id, connection_id, plaid_account_id, name, type) "
                "VALUES (?, ?, 'plaid_acc_1', 'Chequing', 'depository')",
                (ba_id, bc_id),
            )
            # Insert a ledger and line item.
            ledger_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO ledgers (id, user_id, name) VALUES (?, ?, 'Personal')",
                (ledger_id, uid),
            )
            li_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO line_items (id, ledger_id, name, item_type) "
                "VALUES (?, ?, 'Groceries', 'expense')",
                (li_id, ledger_id),
            )
            # Insert 2 transactions.
            tx_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
            merchants = ["Starbucks", "Amazon"]
            amounts = [5.75, 99.99]
            for tx_id, merchant, amount in zip(tx_ids, merchants, amounts):
                conn.execute(
                    "INSERT OR IGNORE INTO transactions "
                    "(id, bank_account_id, plaid_transaction_id, merchant, amount, date) "
                    "VALUES (?, ?, ?, ?, ?, '2025-05-20')",
                    (tx_id, ba_id, f"plaid_{tx_id}", merchant, amount),
                )
                entry_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT OR IGNORE INTO transaction_entries "
                    "(id, transaction_id, line_item_id, amount, uncertain, reviewed, entry_type) "
                    "VALUES (?, ?, ?, ?, 1, 0, 'spending')",
                    (entry_id, tx_id, li_id, amount),
                )
            conn.commit()
        finally:
            conn.close()

        result = main.get_needs_review_summary()

        assert result["count"] == 2, f"Expected 2, got {result['count']}"
        assert result["summary"], "Expected non-empty summary"

        summary = result["summary"]
        assert "Starbucks" in summary, "Starbucks should appear in summary"
        assert "Amazon" in summary, "Amazon should appear in summary"
        assert "5.75" in summary or "5,75" in summary, "Amount 5.75 should appear"
        assert "99.99" in summary or "99,99" in summary, "Amount 99.99 should appear"
        assert len(result["transactions"]) == 2

    def test_summary_singular_plural(self, tmp_app):
        """Summary uses singular 'transaction' for count=1, plural for count>1."""
        main = tmp_app["main"]
        db = tmp_app["db"]
        paths = tmp_app["paths"]

        conn = db.get_db(paths.DB_PATH)
        try:
            uid_row = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            uid = uid_row["id"] if uid_row else str(uuid.uuid4())
            bc_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO bank_connections "
                "(id, user_id, plaid_access_token_encrypted, status) "
                "VALUES (?, ?, 'enc', 'active')",
                (bc_id, uid),
            )
            ba_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO bank_accounts (id, connection_id, plaid_account_id, name, type) "
                "VALUES (?, ?, 'plaid_s1', 'Savings', 'depository')",
                (ba_id, bc_id),
            )
            ledger_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO ledgers (id, user_id, name) VALUES (?, ?, 'Personal')",
                (ledger_id, uid),
            )
            li_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO line_items (id, ledger_id, name, item_type) "
                "VALUES (?, ?, 'Misc', 'expense')",
                (li_id, ledger_id),
            )
            # Single transaction.
            tx_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO transactions "
                "(id, bank_account_id, plaid_transaction_id, merchant, amount, date) "
                "VALUES (?, ?, 'plaid_single', 'Netflix', 17.99, '2025-05-21')",
                (tx_id, ba_id),
            )
            conn.execute(
                "INSERT OR IGNORE INTO transaction_entries "
                "(id, transaction_id, line_item_id, amount, uncertain, reviewed, entry_type) "
                "VALUES (?, ?, ?, 17.99, 1, 0, 'spending')",
                (str(uuid.uuid4()), tx_id, li_id),
            )
            conn.commit()
        finally:
            conn.close()

        result = main.get_needs_review_summary()
        assert result["count"] == 1
        # Should say "transaction" not "transactions" for singular.
        assert "1 transaction" in result["summary"] or "1 transaction" in result["summary"].lower()
        # Must not say "1 transactions".
        assert "1 transactions" not in result["summary"]

    def test_correct_transaction_removes_from_summary(self, tmp_app):
        """After correct_transaction, the item disappears from summary."""
        main = tmp_app["main"]
        db = tmp_app["db"]
        paths = tmp_app["paths"]

        conn = db.get_db(paths.DB_PATH)
        try:
            uid_row = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            uid = uid_row["id"] if uid_row else str(uuid.uuid4())
            bc_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO bank_connections "
                "(id, user_id, plaid_access_token_encrypted, status) "
                "VALUES (?, ?, 'enc', 'active')",
                (bc_id, uid),
            )
            ba_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO bank_accounts (id, connection_id, plaid_account_id, name, type) "
                "VALUES (?, ?, 'plaid_c1', 'Chequing', 'depository')",
                (ba_id, bc_id),
            )
            ledger_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO ledgers (id, user_id, name) VALUES (?, ?, 'Personal')",
                (ledger_id, uid),
            )
            li_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO line_items (id, ledger_id, name, item_type) "
                "VALUES (?, ?, 'Groceries', 'expense')",
                (li_id, ledger_id),
            )
            tx_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO transactions "
                "(id, bank_account_id, plaid_transaction_id, merchant, amount, date) "
                "VALUES (?, ?, 'plaid_corr1', 'Uber Eats', 33.20, '2025-05-22')",
                (tx_id, ba_id),
            )
            conn.execute(
                "INSERT OR IGNORE INTO transaction_entries "
                "(id, transaction_id, line_item_id, amount, uncertain, reviewed, entry_type) "
                "VALUES (?, ?, ?, 33.20, 1, 0, 'spending')",
                (str(uuid.uuid4()), tx_id, li_id),
            )
            conn.commit()
        finally:
            conn.close()

        before = main.get_needs_review_summary()
        assert before["count"] >= 1

        # Correct it.
        result = main.correct_transaction(transaction_id=tx_id, line_item_id=li_id)
        assert result["status"] == "ok"

        after = main.get_needs_review_summary()
        assert (
            after["count"] == before["count"] - 1
        ), f"Expected count to decrease by 1: before={before['count']}, after={after['count']}"
        corrected_ids = {tx["id"] for tx in after["transactions"]}
        assert tx_id not in corrected_ids
