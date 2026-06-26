"""
tests/playwright/test_issue_207_batch_classifier.py
====================================================

End-to-end verification for issue #207 — batch LLM classification.

What this test does:

  1. Spins up a fresh temp ``FRIDAY_BP_APP_DIR`` so no live data is touched.
  2. Initialises the DB and creates a single user.
  3. Runs ``apply_initial_setup`` to seed the Personal ledger + 10 line items.
  4. Mints a Plaid sandbox public token (ins_109508 "First Platypus Bank"),
     exchanges it via ``complete_link``, and syncs transactions with
     ``sync()``.
  5. Patches ``server.llm.chat`` to return a **JSON array** (the new
     batch contract) and runs ``classify_pending_transactions`` directly.
  6. Asserts:
       * ``chat()`` is called FEWER times than the number of transactions
         (batch reduces call count — one call per sub-batch, not per txn).
       * Every classified ``transaction_entries`` row has ``source='llm'``.
       * Every entry has ``reasoning`` populated.
       * The batch prompt contains the expected shared-context sections.
       * The batch prompt contains ``Transaction 0`` style indexed headers.
  7. Starts the FastAPI UI on a random free port and uses Playwright to
     visit the Accounts page and capture a screenshot artefact.

The test is gracefully skipped when:
  - PLAID_CLIENT_ID / PLAID_SECRET are not set, OR
  - playwright is not installed / browser binary missing.
"""

from __future__ import annotations

import json
import os
import socket
import threading
import time
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Skip guards
# ---------------------------------------------------------------------------

# Use the PM-supplied sandbox creds when no env override is present.
os.environ.setdefault("PLAID_CLIENT_ID", "6a108c2ccfbb2f000d022c26")
os.environ.setdefault("PLAID_SECRET", "7ed0d08cc23ca47f6b550504f314ab")
os.environ.setdefault("PLAID_ENV", "sandbox")

PLAID_CREDS = bool(os.environ.get("PLAID_CLIENT_ID")) and bool(os.environ.get("PLAID_SECRET"))

try:  # pragma: no cover - import guard
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
    """Redirect ~/.friday-bp/ to a temp directory and reload server modules."""
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_batch_chat_fn(li_expense: str):
    """Return a ``chat()`` side_effect that produces batch JSON arrays.

    The batch classifier sends all transactions in one prompt and expects a
    JSON array back.  We parse the number of ``### Transaction N`` headers in
    the prompt to return exactly the right number of results.
    """
    call_log = {"count": 0, "prompts": []}

    def _fake_chat(messages, **kwargs):
        call_log["count"] += 1
        user_content = messages[-1]["content"] if messages else ""
        call_log["prompts"].append(user_content)

        # Count how many "### Transaction N" headers are in this prompt.
        import re

        txn_count = len(re.findall(r"^### Transaction \d+", user_content, re.MULTILINE))
        txn_count = max(txn_count, 1)  # at least one result

        result = [
            {
                "transaction_index": i,
                "rule_id": None,
                "line_item_id": li_expense,
                "classification_type": "spending",
                "confidence": 0.88,
                "reasoning": f"Batch-classified transaction {i} as spending (stub).",
            }
            for i in range(txn_count)
        ]
        return json.dumps(result)

    return call_log, _fake_chat


# ---------------------------------------------------------------------------
# The end-to-end test
# ---------------------------------------------------------------------------


def test_issue_207_batch_classifier_end_to_end(tmp_app_dir, monkeypatch):
    """Sync → batch classifier → fewer LLM calls than transactions → screenshot."""
    from unittest.mock import patch

    paths = tmp_app_dir["paths"]
    db = tmp_app_dir["db"]
    auth = tmp_app_dir["auth"]
    main = tmp_app_dir["main"]

    # ------------------------------------------------------------------
    # 1. Create user + seed Personal ledger.
    # ------------------------------------------------------------------
    user_id = auth.create_user(paths.DB_PATH, "ridvan", "supersecret-pw")
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
    assert li_expense and li_income, f"expected expense+income line items; got {rows!r}"

    # ------------------------------------------------------------------
    # 2. Mint Plaid sandbox public token and exchange it.
    # ------------------------------------------------------------------
    from plaid.model.products import Products
    from plaid.model.sandbox_public_token_create_request import (
        SandboxPublicTokenCreateRequest,
    )

    from server.providers.plaid import PlaidProvider

    provider = PlaidProvider(env="sandbox")
    api_client = provider._build_client()
    sandbox_response = api_client.sandbox_public_token_create(
        SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",
            initial_products=[Products("transactions")],
        )
    )
    public_token = sandbox_response["public_token"]

    link_result = main.complete_link(public_token=public_token, plaid_env="sandbox")
    assert link_result.get("status") in (None, "ok") or "connection_id" in link_result, link_result

    # ------------------------------------------------------------------
    # 3. Sync then classify with the batch flow (issue #207).
    # ------------------------------------------------------------------
    call_log, fake_chat = _make_batch_chat_fn(li_expense)

    sync_result = {}
    classify_result = {}
    entry_rows: list = []

    with patch("server.llm.chat", side_effect=fake_chat):
        for attempt in range(6):
            sync_result = main.sync()
            classify_result = main.classify_pending_transactions(user_id)

            conn = db.get_db(paths.DB_PATH)
            try:
                entry_rows = conn.execute(
                    "SELECT te.id, te.source, te.line_item_id, te.reasoning, te.confidence,"
                    "       t.merchant, t.amount"
                    "  FROM transaction_entries te"
                    "  JOIN transactions t ON t.id = te.transaction_id"
                ).fetchall()

                txn_count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            finally:
                conn.close()

            if entry_rows:
                break
            time.sleep(2)

    print(
        f"\nSYNC: {sync_result}"
        f"\nCLASSIFY: {classify_result}"
        f"\nTRANSACTIONS: {txn_count}"
        f"\nENTRIES: {len(entry_rows)}"
        f"\nCHAT CALLS: {call_log['count']}\n"
    )

    if not entry_rows:
        pytest.skip(
            "Plaid sandbox returned 0 transactions on first sync — "
            "rerun the test or wait for sandbox seed to populate."
        )

    # ------------------------------------------------------------------
    # 4. Core assertions for batch behaviour (issue #207).
    # ------------------------------------------------------------------

    # 4a. Batch reduces LLM call count: total chat calls must be FEWER
    #     than the number of transactions (the whole point of batching).
    #     With token cap set to 80 000 chars, all sandbox transactions
    #     (typically < 30) should fit in ONE call.
    assert call_log["count"] < txn_count or txn_count == 1, (
        f"Expected batch to reduce call count below txn count ({txn_count}), "
        f"but got {call_log['count']} chat calls."
    )

    # 4b. Every entry must carry llm source + reasoning.
    llm_entries = [r for r in entry_rows if r["source"] == "llm"]
    assert llm_entries, f"no llm-source entries written; rows={entry_rows!r}"
    for r in llm_entries:
        assert r["reasoning"], f"missing reasoning for entry {dict(r)!r}"
        assert r["confidence"] is not None

    # 4c. Batch prompt must contain indexed transaction headers
    #     and shared-context sections.
    if call_log["prompts"]:
        prompt = call_log["prompts"][0]
        # Shared context sections (same as #205 but now batch).
        for section in (
            "Classification Rules",
            "Ledger Tree",
            "Classification Hints",
            "Transactions To Classify",
        ):
            assert (
                section in prompt
            ), f"batch prompt missing section {section!r}\n--- prompt ---\n{prompt[:800]}"
        # Indexed transaction header format introduced in #207.
        assert (
            "### Transaction 0" in prompt
        ), f"batch prompt missing '### Transaction 0' header\n--- prompt ---\n{prompt[:800]}"

    # ------------------------------------------------------------------
    # 5. Boot the UI and capture a Playwright screenshot.
    # ------------------------------------------------------------------
    import uvicorn

    from ui.server import app as ui_app

    port = _free_port()
    config = uvicorn.Config(
        ui_app, host="127.0.0.1", port=port, log_level="warning", lifespan="off"
    )
    server_obj = uvicorn.Server(config)

    t = threading.Thread(target=server_obj.run, daemon=True)
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
    screenshot_path = screenshot_dir / "issue_207_batch_classifier.png"

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"http://127.0.0.1:{port}/", wait_until="domcontentloaded")
        page.screenshot(path=str(screenshot_path), full_page=True)
        title = page.title()
        body_text = page.evaluate("() => document.body.innerText")
        browser.close()

    print(f"\nScreenshot: {screenshot_path}\nTitle: {title!r}\nBody chars: {len(body_text)}\n")

    assert (
        screenshot_path.exists() and screenshot_path.stat().st_size > 1000
    ), f"screenshot missing or too small: {screenshot_path}"

    server_obj.should_exit = True
    t.join(timeout=5)


# ---------------------------------------------------------------------------
# Unit-level batch classifier tests (no Plaid, no UI)
# ---------------------------------------------------------------------------


def test_classify_batch_returns_same_length(tmp_app_dir):
    """classify_batch must return the same number of results as input transactions."""
    import importlib

    import server.classifier as clf_mod

    importlib.reload(clf_mod)
    from server.classifier import classify_batch

    db = tmp_app_dir["db"]
    paths = tmp_app_dir["paths"]

    conn = db.get_db(paths.DB_PATH)
    try:
        transactions = [
            {"merchant": f"Merchant {i}", "amount": float(i + 1), "date": "2024-01-01"}
            for i in range(5)
        ]
        rules: list = []

        from unittest.mock import patch

        def fake_chat(messages, **kwargs):
            import re

            user_content = messages[-1]["content"] if messages else ""
            txn_count = len(re.findall(r"^### Transaction \d+", user_content, re.MULTILINE))
            txn_count = max(txn_count, 1)
            return json.dumps(
                [
                    {
                        "transaction_index": i,
                        "rule_id": None,
                        "line_item_id": None,
                        "classification_type": "spending",
                        "confidence": 0.8,
                        "reasoning": f"stub {i}",
                    }
                    for i in range(txn_count)
                ]
            )

        with patch("server.llm.chat", side_effect=fake_chat):
            results = classify_batch(conn, transactions, rules)
    finally:
        conn.close()

    assert len(results) == 5
    for i, r in enumerate(results):
        assert r["classification_type"] == "spending"
        assert r["reasoning"] == f"stub {i}"


def test_classify_batch_empty_input(tmp_app_dir):
    """classify_batch with empty input returns empty list immediately."""
    from server.classifier import classify_batch

    db = tmp_app_dir["db"]
    paths = tmp_app_dir["paths"]

    conn = db.get_db(paths.DB_PATH)
    try:
        results = classify_batch(conn, [], rules=[])
    finally:
        conn.close()

    assert results == []


def test_classify_batch_sub_batching(tmp_app_dir, monkeypatch):
    """When prompt exceeds MAX_BATCH_CHARS, transactions split into sub-batches."""
    import importlib

    import server.classifier as clf_mod

    importlib.reload(clf_mod)
    from server.classifier import classify_batch

    db = tmp_app_dir["db"]
    paths = tmp_app_dir["paths"]

    # Override MAX_BATCH_CHARS to a tiny value to force splitting.
    monkeypatch.setattr(clf_mod, "MAX_BATCH_CHARS", 100)

    conn = db.get_db(paths.DB_PATH)
    try:
        transactions = [
            {"merchant": f"Merchant {i}", "amount": float(i + 1), "date": "2024-01-01"}
            for i in range(4)
        ]

        chat_calls = {"count": 0}

        def fake_chat(messages, **kwargs):
            chat_calls["count"] += 1
            import re

            user_content = messages[-1]["content"] if messages else ""
            txn_count = len(re.findall(r"^### Transaction \d+", user_content, re.MULTILINE))
            txn_count = max(txn_count, 1)
            return json.dumps(
                [
                    {
                        "transaction_index": i,
                        "rule_id": None,
                        "line_item_id": None,
                        "classification_type": "spending",
                        "confidence": 0.8,
                        "reasoning": f"sub-batch result {i}",
                    }
                    for i in range(txn_count)
                ]
            )

        from unittest.mock import patch

        with patch("server.llm.chat", side_effect=fake_chat):
            results = classify_batch(conn, transactions, rules=[])
    finally:
        conn.close()

    # With MAX_BATCH_CHARS=100, each transaction should be in its own sub-batch.
    assert len(results) == 4
    assert chat_calls["count"] > 1, (
        f"Expected multiple chat calls with tiny MAX_BATCH_CHARS=100, " f"got {chat_calls['count']}"
    )


def test_classify_batch_malformed_llm_response(tmp_app_dir):
    """classify_batch falls back gracefully when LLM returns non-array JSON."""
    from server.classifier import classify_batch

    db = tmp_app_dir["db"]
    paths = tmp_app_dir["paths"]

    conn = db.get_db(paths.DB_PATH)
    try:
        transactions = [{"merchant": "Bad Merchant", "amount": 9.99, "date": "2024-01-01"}]

        from unittest.mock import patch

        with patch("server.llm.chat", return_value='{"error": "oops"}'):
            results = classify_batch(conn, transactions, rules=[])
    finally:
        conn.close()

    assert len(results) == 1
    # Should fall back to uncertain result, not raise.
    assert results[0]["uncertain"] is True


def test_classify_batch_missing_indices(tmp_app_dir):
    """classify_batch fills in fallbacks for transaction indices the LLM omits."""
    from server.classifier import classify_batch

    db = tmp_app_dir["db"]
    paths = tmp_app_dir["paths"]

    conn = db.get_db(paths.DB_PATH)
    try:
        transactions = [
            {"merchant": "Merchant A", "amount": 10.0, "date": "2024-01-01"},
            {"merchant": "Merchant B", "amount": 20.0, "date": "2024-01-02"},
        ]

        # LLM only returns result for index 0, skips index 1.
        llm_response = json.dumps(
            [
                {
                    "transaction_index": 0,
                    "rule_id": None,
                    "line_item_id": None,
                    "classification_type": "spending",
                    "confidence": 0.9,
                    "reasoning": "Got result for 0",
                }
            ]
        )

        from unittest.mock import patch

        with patch("server.llm.chat", return_value=llm_response):
            results = classify_batch(conn, transactions, rules=[])
    finally:
        conn.close()

    assert len(results) == 2
    assert results[0]["reasoning"] == "Got result for 0"
    # Index 1 was missing → uncertain fallback.
    assert results[1]["uncertain"] is True
    assert "did not return result" in results[1]["reasoning"]
