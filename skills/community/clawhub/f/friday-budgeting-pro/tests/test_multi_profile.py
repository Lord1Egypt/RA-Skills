"""
tests/test_multi_profile.py — Tests for multi-profile support (#131).

Covers:
  - Profile creation via create_user helper
  - Login with username+password
  - Data isolation (user A can't see user B's bank connections / ledgers)
  - list_profiles() MCP tool
  - Migration: existing single-user DB gets wrapped in default profile
"""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB and monkeypatch paths."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test_multi_profile.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    from ui.server import app

    return TestClient(app, follow_redirects=False)


def _do_setup(client: TestClient, username: str = "alice", password: str = "alicepass123") -> None:
    """Drive the setup wizard to completion (creates first user)."""
    r = client.post(
        "/setup/1",
        data={
            "username": username,
            "password": password,
            "password_confirm": password,
        },
    )
    assert r.status_code == 200
    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302


def _login(
    client: TestClient, username: str = "alice", password: str = "alicepass123"
) -> TestClient:
    """Log in and return the client with session cookie."""
    r = client.post("/login", data={"username": username, "password": password})
    assert r.status_code == 302, f"Login failed (status {r.status_code})"
    return client


# ---------------------------------------------------------------------------
# Profile creation
# ---------------------------------------------------------------------------


class TestProfileCreation:
    def test_create_user_helper(self, db_path):
        from ui.auth import create_user, get_user_by_username

        uid = create_user(db_path, "bob", "bobspassword1")
        assert uid is not None
        user = get_user_by_username(db_path, "bob")
        assert user is not None
        assert user["username"] == "bob"
        assert user["id"] == uid

    def test_duplicate_username_raises(self, db_path):
        from ui.auth import create_user

        create_user(db_path, "dup", "password12")
        with pytest.raises(ValueError, match="already taken"):
            create_user(db_path, "dup", "password12")

    def test_has_any_user_false_on_fresh_db(self, db_path):
        """Fresh DB (no data) has no users — setup wizard creates the first one."""
        from ui.auth import has_any_user

        assert has_any_user(db_path) is False

    def test_list_users_returns_created_users(self, db_path):
        from ui.auth import create_user, list_users

        create_user(db_path, "u1", "password11")
        create_user(db_path, "u2", "password22")
        users = list_users(db_path)
        usernames = {u["username"] for u in users}
        assert "u1" in usernames
        assert "u2" in usernames

    def test_create_profile_via_ui(self, client, db_path):
        """Profile creation via UI was moved to /settings (#159).
        Sending create_profile action to /profile now falls through to
        the default save-settings handler (200 with saved=True)."""
        _do_setup(client, "alice", "alicepass123")
        _login(client, "alice", "alicepass123")

        r = client.post(
            "/profile",
            data={
                "action": "create_profile",
                "new_username": "bob",
                "new_password": "bobpassword1",
            },
        )
        # Action is ignored (falls through to save_settings); profile still 200
        assert r.status_code == 200

    def test_create_profile_short_password_rejected(self, client):
        """Profile creation via UI was moved to /settings (#159).
        Sending create_profile action to /profile falls through to save_settings."""
        _do_setup(client, "alice", "alicepass123")
        _login(client, "alice", "alicepass123")
        r = client.post(
            "/profile",
            data={
                "action": "create_profile",
                "new_username": "bob",
                "new_password": "short",
            },
        )
        # Falls through to save_settings; page renders 200
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# Login with username+password
# ---------------------------------------------------------------------------


class TestLoginWithUsernamePwd:
    def test_login_requires_username_when_multiple_users(self, client, db_path):
        """When multiple users exist, login without username fails."""
        _do_setup(client, "alice", "alicepass123")
        from ui.auth import create_user

        create_user(db_path, "bob", "bobpassword1")

        fresh = TestClient(client.app, follow_redirects=False)
        r = fresh.post("/login", data={"password": "alicepass123"})
        # Should fail because no username and multiple users
        assert r.status_code == 200  # re-rendered login with error
        assert b"Incorrect" in r.content or b"username" in r.content.lower()

    def test_login_single_user_no_username_needed(self, client):
        """With one user, login works without username (backward compat)."""
        _do_setup(client, "alice", "alicepass123")
        # Log out first
        client.post("/logout")
        fresh = TestClient(client.app, follow_redirects=False)
        r = fresh.post("/login", data={"password": "alicepass123"})
        # Single user — should work
        assert r.status_code == 302

    def test_login_with_username(self, client):
        _do_setup(client, "alice", "alicepass123")
        fresh = TestClient(client.app, follow_redirects=False)
        r = fresh.post("/login", data={"username": "alice", "password": "alicepass123"})
        assert r.status_code == 302
        assert r.headers["location"] == "/dashboard"

    def test_login_wrong_password_fails(self, client):
        _do_setup(client, "alice", "alicepass123")
        fresh = TestClient(client.app, follow_redirects=False)
        r = fresh.post("/login", data={"username": "alice", "password": "wrongpassword"})
        assert r.status_code == 200
        assert b"Incorrect" in r.content

    def test_login_unknown_username_fails(self, client):
        _do_setup(client, "alice", "alicepass123")
        fresh = TestClient(client.app, follow_redirects=False)
        r = fresh.post("/login", data={"username": "nobody", "password": "alicepass123"})
        assert r.status_code == 200
        assert b"Incorrect" in r.content

    def test_session_carries_user_id(self, client, db_path):
        """After login, the session row has the correct user_id."""
        from server.db import get_db
        from ui.auth import SESSION_COOKIE, get_user_by_username

        _do_setup(client, "alice", "alicepass123")
        fresh = TestClient(client.app, follow_redirects=False)
        r = fresh.post("/login", data={"username": "alice", "password": "alicepass123"})
        assert r.status_code == 302

        token = fresh.cookies.get(SESSION_COOKIE)
        assert token is not None

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT user_id FROM sessions WHERE id = ?", (token,)).fetchone()
        finally:
            conn.close()

        alice = get_user_by_username(db_path, "alice")
        assert alice is not None
        assert row is not None
        assert row["user_id"] == alice["id"]


# ---------------------------------------------------------------------------
# Data isolation
# ---------------------------------------------------------------------------


class TestDataIsolation:
    def test_bank_connections_are_isolated(self, db_path):
        """Bank connections created for user A are not visible to user B."""
        from server.db import get_db
        from ui.auth import create_user

        uid_a = create_user(db_path, "userA", "passwordabc1")
        uid_b = create_user(db_path, "userB", "passwordabc2")

        conn = get_db(db_path)
        try:
            # Insert a connection for user A
            conn.execute(
                "INSERT INTO bank_connections (id, plaid_access_token_encrypted, status, user_id) "
                "VALUES (?, ?, 'active', ?)",
                (str(uuid.uuid4()), "encrypted_token_a", uid_a),
            )
            conn.commit()

            a_conns = conn.execute(
                "SELECT id FROM bank_connections WHERE user_id = ?", (uid_a,)
            ).fetchall()
            b_conns = conn.execute(
                "SELECT id FROM bank_connections WHERE user_id = ?", (uid_b,)
            ).fetchall()
        finally:
            conn.close()

        assert len(a_conns) == 1
        assert len(b_conns) == 0

    def test_ledgers_are_isolated(self, db_path):
        """Ledgers created for user A are not visible to user B."""
        from server.db import get_db
        from ui.auth import create_user

        uid_a = create_user(db_path, "ledger_a", "passwordabc1")
        uid_b = create_user(db_path, "ledger_b", "passwordabc2")

        conn = get_db(db_path)
        try:
            conn.execute(
                "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), "Alice Budget", uid_a),
            )
            conn.commit()

            a_ledgers = conn.execute(
                "SELECT id FROM ledgers WHERE user_id = ?", (uid_a,)
            ).fetchall()
            b_ledgers = conn.execute(
                "SELECT id FROM ledgers WHERE user_id = ?", (uid_b,)
            ).fetchall()
        finally:
            conn.close()

        assert len(a_ledgers) == 1
        assert len(b_ledgers) == 0

    def test_hints_are_isolated(self, db_path):
        """Classification hints created for user A are not visible to user B."""
        from server.db import get_db
        from ui.auth import create_user

        uid_a = create_user(db_path, "hint_a", "passwordabc1")
        uid_b = create_user(db_path, "hint_b", "passwordabc2")

        conn = get_db(db_path)
        try:
            conn.execute(
                "INSERT INTO classification_hints (id, text, user_id) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), "Always grocery for Walmart", uid_a),
            )
            conn.commit()

            a_hints = conn.execute(
                "SELECT id FROM classification_hints WHERE user_id = ?", (uid_a,)
            ).fetchall()
            b_hints = conn.execute(
                "SELECT id FROM classification_hints WHERE user_id = ?", (uid_b,)
            ).fetchall()
        finally:
            conn.close()

        assert len(a_hints) == 1
        assert len(b_hints) == 0

    def test_profile_page_shows_only_current_user_connections(self, client, db_path):
        """Profile page only shows bank connections for the logged-in user."""
        from server.db import get_db
        from ui.auth import create_user

        _do_setup(client, "alice", "alicepass123")
        uid_alice = client.app  # placeholder

        # Create bob's user and a connection for bob
        uid_bob = create_user(db_path, "bob", "bobpassword1")
        conn = get_db(db_path)
        try:
            conn.execute(
                "INSERT INTO bank_connections (id, plaid_access_token_encrypted, "
                "status, institution_name, user_id) VALUES (?, ?, 'active', ?, ?)",
                (str(uuid.uuid4()), "enc_token", "Bob's Secret Bank", uid_bob),
            )
            conn.commit()
        finally:
            conn.close()

        # Alice's profile page should NOT show Bob's bank
        _login(client, "alice", "alicepass123")
        r = client.get("/profile")
        assert r.status_code == 200
        assert b"Bob's Secret Bank" not in r.content


# ---------------------------------------------------------------------------
# list_profiles() MCP tool
# ---------------------------------------------------------------------------


class TestListProfilesMCP:
    def test_list_profiles_returns_list(self, db_path, monkeypatch):
        """list_profiles() returns a list (not a stub or error)."""
        import server.paths as paths

        monkeypatch.setattr(paths, "DB_PATH", db_path)

        from server.main import list_profiles

        result = list_profiles()
        assert isinstance(result, dict)
        assert "profiles" in result
        assert isinstance(result["profiles"], list)

    def test_list_profiles_includes_created_users(self, db_path, monkeypatch):
        import server.paths as paths

        monkeypatch.setattr(paths, "DB_PATH", db_path)

        from ui.auth import create_user

        create_user(db_path, "carol", "carolpass12")
        create_user(db_path, "dave", "davepass123")

        from server.main import list_profiles

        result = list_profiles()
        usernames = {p["username"] for p in result["profiles"]}
        assert "carol" in usernames
        assert "dave" in usernames

    def test_list_profiles_no_password_hash_exposed(self, db_path, monkeypatch):
        """Password hashes must not appear in list_profiles output."""
        import server.paths as paths

        monkeypatch.setattr(paths, "DB_PATH", db_path)

        from server.main import list_profiles

        result = list_profiles()
        for profile in result["profiles"]:
            assert "password_hash" not in profile
            assert "password" not in profile


# ---------------------------------------------------------------------------
# Migration: existing single-user DB
# ---------------------------------------------------------------------------


class TestMigration:
    def test_existing_db_gets_default_user(self, tmp_path):
        """A DB with existing rows but no users table gets a default user on init_db."""
        db_file = tmp_path / "legacy.db"

        # Create a "legacy" DB with the old schema (no users table, no user_id columns)
        conn = sqlite3.connect(str(db_file))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS bank_connections (
                id TEXT PRIMARY KEY,
                plaid_item_id TEXT UNIQUE,
                plaid_access_token_encrypted TEXT NOT NULL,
                institution_name TEXT,
                status TEXT DEFAULT 'active',
                last_synced_at INTEGER
            );
            CREATE TABLE IF NOT EXISTS ledgers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS classification_hints (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at INTEGER NOT NULL,
                last_seen_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                user_agent TEXT
            );
            CREATE TABLE IF NOT EXISTS app_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                username TEXT,
                ui_password_hash TEXT,
                ui_password_set_at INTEGER
            );
            INSERT INTO bank_connections (id, plaid_access_token_encrypted, status)
                VALUES ('bc-1', 'enc_token', 'active');
            INSERT INTO ledgers (id, name) VALUES ('led-1', 'Personal');
            INSERT INTO classification_hints (id, text) VALUES ('hint-1', 'Test hint');
        """)
        conn.commit()
        conn.close()

        # Run init_db — should create users table + default user + backfill user_id
        from server.db import init_db

        init_db(db_file)

        conn = sqlite3.connect(str(db_file))
        conn.row_factory = sqlite3.Row
        try:
            # A default user should exist
            users = conn.execute("SELECT id, username FROM users").fetchall()
            assert len(users) >= 1

            default_uid = users[0]["id"]

            # Existing rows should have been backfilled with user_id
            bc = conn.execute("SELECT user_id FROM bank_connections WHERE id = 'bc-1'").fetchone()
            assert bc is not None
            assert bc["user_id"] == default_uid

            led = conn.execute("SELECT user_id FROM ledgers WHERE id = 'led-1'").fetchone()
            assert led is not None
            assert led["user_id"] == default_uid

            hint = conn.execute(
                "SELECT user_id FROM classification_hints WHERE id = 'hint-1'"
            ).fetchone()
            assert hint is not None
            assert hint["user_id"] == default_uid
        finally:
            conn.close()

    def test_migration_uses_legacy_password_hash(self, tmp_path):
        """If app_config has a password hash, it is copied to the default user."""
        from argon2 import PasswordHasher

        db_file = tmp_path / "legacy_pw.db"

        ph = PasswordHasher()
        legacy_hash = ph.hash("mysecretpassword")

        conn = sqlite3.connect(str(db_file))
        conn.executescript(f"""
            CREATE TABLE IF NOT EXISTS ledgers (id TEXT PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS bank_connections (
                id TEXT PRIMARY KEY,
                plaid_access_token_encrypted TEXT NOT NULL,
                status TEXT DEFAULT 'active'
            );
            CREATE TABLE IF NOT EXISTS classification_hints (id TEXT PRIMARY KEY, text TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at INTEGER NOT NULL,
                last_seen_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                user_agent TEXT
            );
            CREATE TABLE IF NOT EXISTS app_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                username TEXT,
                ui_password_hash TEXT,
                ui_password_set_at INTEGER
            );
            INSERT INTO app_config (id, ui_password_hash) VALUES (1, '{legacy_hash}');
        """)
        conn.commit()
        conn.close()

        from server.db import init_db

        init_db(db_file)

        from ui.auth import get_password_hash, verify_password

        stored = get_password_hash(db_file)
        assert stored is not None
        assert verify_password("mysecretpassword", stored)

    def test_init_db_idempotent_with_existing_users(self, db_path):
        """Re-running init_db does not create duplicate users."""
        from server.db import init_db
        from ui.auth import list_users

        # init_db was already called (by the db_path fixture)
        count_before = len(list_users(db_path))

        init_db(db_path)

        count_after = len(list_users(db_path))
        assert count_after == count_before

    def test_delete_profile_removes_data(self, db_path):
        """Deleting a profile removes all associated data."""
        from server.db import get_db
        from ui.auth import create_user, delete_user, get_user_by_username

        uid = create_user(db_path, "tobedeleted", "password123")

        conn = get_db(db_path)
        try:
            conn.execute(
                "INSERT INTO bank_connections (id, plaid_access_token_encrypted, status, user_id) "
                "VALUES (?, 'enc', 'active', ?)",
                (str(uuid.uuid4()), uid),
            )
            conn.execute(
                "INSERT INTO ledgers (id, name, user_id) VALUES (?, 'Budget', ?)",
                (str(uuid.uuid4()), uid),
            )
            conn.commit()
        finally:
            conn.close()

        delete_user(db_path, uid)

        assert get_user_by_username(db_path, "tobedeleted") is None

        conn = get_db(db_path)
        try:
            bc = conn.execute(
                "SELECT id FROM bank_connections WHERE user_id = ?", (uid,)
            ).fetchall()
            leds = conn.execute("SELECT id FROM ledgers WHERE user_id = ?", (uid,)).fetchall()
        finally:
            conn.close()

        assert len(bc) == 0
        assert len(leds) == 0
