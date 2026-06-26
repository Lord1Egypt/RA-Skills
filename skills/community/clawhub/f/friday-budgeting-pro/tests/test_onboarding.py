"""
tests/test_onboarding.py \u2014 Tests for the guided onboarding tools (issue #206).

Covers:
  - setup_interview / list_setup_interview / list_setup_interview_questions
  - analyze_recurring_merchants
  - DB migration: setup_interview table exists after init_db()
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def env(tmp_path, monkeypatch):
    """Patch ``server.paths.DB_PATH`` to a fresh DB for this test only.

    NOTE: we deliberately avoid ``importlib.reload`` here — reloading
    modules pollutes the global module table for tests that run later
    (the canonical case being ``tests/test_recovery_reset.py`` which
    monkey-patches the same attributes).  ``monkeypatch.setattr`` is
    automatically reverted in fixture teardown, keeping cross-test
    isolation intact.
    """
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

    _db.init_db(db_path)
    user_id = _auth.create_user(db_path, "ridvan", "supersecretpw")
    return {
        "paths": _paths,
        "db": _db,
        "auth": _auth,
        "main": _main,
        "user_id": user_id,
        "db_path": db_path,
    }


# ---------------------------------------------------------------------------
# DB migration
# ---------------------------------------------------------------------------


def test_setup_interview_table_created(env):
    conn = env["db"].get_db(env["db_path"])
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(setup_interview)")}
    finally:
        conn.close()
    assert cols == {
        "id",
        "user_id",
        "question_key",
        "answer_text",
        "created_at",
        "updated_at",
    }


def test_init_db_idempotent(env):
    """Calling init_db twice does not raise."""
    env["db"].init_db(env["db_path"])  # second invocation
    env["db"].init_db(env["db_path"])  # third invocation


# ---------------------------------------------------------------------------
# list_setup_interview_questions
# ---------------------------------------------------------------------------


def test_list_setup_interview_questions_returns_canonical_set(env):
    result = env["main"].list_setup_interview_questions()
    assert "questions" in result
    keys = {q["key"] for q in result["questions"]}
    assert {"employer", "subscriptions", "utilities", "properties"} <= keys
    for q in result["questions"]:
        assert q["prompt"]


# ---------------------------------------------------------------------------
# setup_interview / list_setup_interview
# ---------------------------------------------------------------------------


def test_setup_interview_inserts_then_updates(env):
    r1 = env["main"].setup_interview("employer", "Tenstorrent")
    assert r1["created"] is True
    assert r1["question_key"] == "employer"
    assert r1["answer_text"] == "Tenstorrent"

    r2 = env["main"].setup_interview("employer", "Tenstorrent AI")
    assert r2["created"] is False, "second answer should UPDATE not INSERT"
    assert r2["id"] == r1["id"]
    assert r2["answer_text"] == "Tenstorrent AI"


def test_setup_interview_validation(env):
    with pytest.raises(ValueError):
        env["main"].setup_interview("", "anything")
    with pytest.raises(ValueError):
        env["main"].setup_interview("employer", "")
    with pytest.raises(ValueError):
        env["main"].setup_interview("  ", "anything")


def test_list_setup_interview_returns_all_answers(env):
    env["main"].setup_interview("employer", "Tenstorrent")
    env["main"].setup_interview("subscriptions", "Netflix, Spotify, iCloud")
    env["main"].setup_interview("utilities", "Hydro One, Rogers")

    result = env["main"].list_setup_interview()
    assert "answers" in result
    by_key = {a["question_key"]: a for a in result["answers"]}
    assert set(by_key) == {"employer", "subscriptions", "utilities"}
    assert by_key["subscriptions"]["answer_text"] == "Netflix, Spotify, iCloud"
    for ans in result["answers"]:
        assert ans["created_at"] and ans["updated_at"]


def test_setup_interview_scoped_to_active_user(env):
    """Two users should not see each other's onboarding answers."""
    auth = env["auth"]
    main = env["main"]

    # First user answers something.
    main.setup_interview("employer", "Tenstorrent")

    # Add a second user and force the active-user fallback to pick them
    # by deleting all existing sessions and inserting a session for user 2.
    user2 = auth.create_user(env["db_path"], "second", "anotherpassword")
    conn = env["db"].get_db(env["db_path"])
    try:
        import time
        import uuid

        conn.execute("DELETE FROM sessions")
        now = int(time.time())
        conn.execute(
            "INSERT INTO sessions (id, user_id, created_at, last_seen_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), user2, now, now, now + 86400),
        )
        conn.commit()
    finally:
        conn.close()

    # User 2 should not see user 1's answers.
    answers = main.list_setup_interview()["answers"]
    assert answers == []

    # User 2 can write their own answer.
    main.setup_interview("employer", "Other Corp")
    answers = main.list_setup_interview()["answers"]
    assert len(answers) == 1
    assert answers[0]["answer_text"] == "Other Corp"


# ---------------------------------------------------------------------------
# analyze_recurring_merchants
# ---------------------------------------------------------------------------


def _seed_account(env, ledger_id_out: list | None = None):
    """Create a bank_connection + bank_account for the active user."""
    import uuid

    conn = env["db"].get_db(env["db_path"])
    try:
        conn_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_connections "
            "(id, plaid_access_token_encrypted, status, user_id) "
            "VALUES (?, ?, 'active', ?)",
            (conn_id, "enc-token", env["user_id"]),
        )
        acct_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO bank_accounts (id, connection_id, name) VALUES (?, ?, ?)",
            (acct_id, conn_id, "Test Checking"),
        )
        # Also seed a ledger + line item so we can classify one of the txns.
        ledger_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "Personal", env["user_id"]),
        )
        li_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (li_id, ledger_id, "Subscriptions", "expense"),
        )
        conn.commit()
        if ledger_id_out is not None:
            ledger_id_out.append((ledger_id, li_id))
        return acct_id
    finally:
        conn.close()


def _seed_txn(
    env, acct_id: str, merchant: str, amount: float, date: str, plaid_category: str | None = None
):
    import uuid

    conn = env["db"].get_db(env["db_path"])
    try:
        txn_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO transactions (id, bank_account_id, date, merchant, amount, "
            "plaid_category, pending) VALUES (?, ?, ?, ?, ?, ?, 0)",
            (txn_id, acct_id, date, merchant, amount, plaid_category),
        )
        conn.commit()
        return txn_id
    finally:
        conn.close()


def test_analyze_recurring_merchants_returns_recurring_only(env):
    import datetime

    acct = _seed_account(env)
    today = datetime.date.today()
    # Netflix charged twice in the lookback window.
    _seed_txn(env, acct, "Netflix", -15.99, (today - datetime.timedelta(days=10)).isoformat())
    _seed_txn(env, acct, "Netflix", -15.99, (today - datetime.timedelta(days=40)).isoformat())
    # One-off Uber charge \u2014 should be excluded with min_occurrences=2.
    _seed_txn(env, acct, "Uber", -12.50, (today - datetime.timedelta(days=5)).isoformat())
    # Old Spotify charge outside lookback window \u2014 excluded.
    _seed_txn(env, acct, "Spotify", -9.99, (today - datetime.timedelta(days=200)).isoformat())

    result = env["main"].analyze_recurring_merchants(min_occurrences=2, lookback_days=90)
    merchants = result["merchants"]
    by_name = {m["merchant"]: m for m in merchants}
    assert "Netflix" in by_name, f"expected Netflix in {merchants!r}"
    assert by_name["Netflix"]["occurrences"] == 2
    assert "Uber" not in by_name
    assert "Spotify" not in by_name


def test_analyze_recurring_merchants_validation(env):
    with pytest.raises(ValueError):
        env["main"].analyze_recurring_merchants(min_occurrences=0)
    with pytest.raises(ValueError):
        env["main"].analyze_recurring_merchants(lookback_days=0)


def test_analyze_recurring_merchants_includes_current_classification(env):
    import datetime
    import uuid

    ledger_info: list = []
    acct = _seed_account(env, ledger_id_out=ledger_info)
    ledger_id, li_id = ledger_info[0]

    today = datetime.date.today()
    txn1 = _seed_txn(
        env, acct, "Disney Plus", -8.99, (today - datetime.timedelta(days=5)).isoformat()
    )
    txn2 = _seed_txn(
        env, acct, "Disney Plus", -8.99, (today - datetime.timedelta(days=35)).isoformat()
    )

    # Classify one of them.
    conn = env["db"].get_db(env["db_path"])
    try:
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, source, "
            " confidence, reviewed) VALUES (?, ?, ?, ?, ?, 'llm', 0.9, 1)",
            (str(uuid.uuid4()), txn1, ledger_id, li_id, -8.99),
        )
        conn.commit()
    finally:
        conn.close()

    result = env["main"].analyze_recurring_merchants(min_occurrences=2, lookback_days=90)
    disney = next((m for m in result["merchants"] if m["merchant"] == "Disney Plus"), None)
    assert disney is not None
    assert disney["current_line_item"] == "Subscriptions"
    assert disney["current_ledger"] == "Personal"
