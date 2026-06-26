"""
tests/test_account_display.py — Tests for issue #140: Account descriptions show
account name/type instead of raw UUID.

Covers:
  - Profile page never shows a UUID when acct.name=None, acct.mask='1234'
  - Profile page shows acct.name when it is set
  - Profile page uses subtype+mask when only subtype is set (name=None, mask='5678')
  - Profile page falls back to "Unknown Account" when all fields are None/null
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

UUID_RE_PATTERN = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def _uuid_in_visible_text(html: str) -> bool:
    """Return True if a UUID appears as visible text content (not just as an HTML attribute value).

    UUIDs legitimately appear in `data-account-id` and `id="desc-..."` attributes; those are
    fine and expected.  The bug is when a UUID appears as *display text* inside the account
    name span.  We strip all HTML tags and then search for UUID patterns in the remaining text.
    """
    import re

    # Remove HTML tags entirely, leaving only text nodes
    text_only = re.sub(r"<[^>]+>", " ", html)
    return bool(re.search(UUID_RE_PATTERN, text_only, re.IGNORECASE))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    db = tmp_path / "test.db"
    init_db(db)
    monkeypatch.setattr(server.paths, "DB_PATH", db)
    monkeypatch.setattr("server.paths.APP_DIR", tmp_path)
    return db


def _make_authed_client(db_path: Path) -> TestClient:
    token = "test-" + uuid.uuid4().hex
    now = int(time.time())
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO sessions (id, created_at, last_seen_at, expires_at) VALUES (?,?,?,?)",
        (token, now, now, now + 86400 * 3650),
    )
    conn.execute("INSERT OR IGNORE INTO app_config (id) VALUES (1)")
    conn.commit()
    conn.close()

    from ui.server import SESSION_COOKIE, app

    c = TestClient(app, follow_redirects=False)
    c.cookies.set(SESSION_COOKIE, token)
    return c


def _insert_connection(db_path: Path, institution: str = "Test Bank") -> str:
    conn_id = str(uuid.uuid4())
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted, institution_name, status)"
        " VALUES (?, ?, ?, ?, ?)",
        (conn_id, "item-test", "enc", institution, "active"),
    )
    conn.commit()
    conn.close()
    return conn_id


def _insert_account(
    db_path: Path,
    conn_id: str,
    *,
    name: str | None,
    mask: str | None,
    acct_type: str | None = None,
    subtype: str | None = None,
) -> str:
    acct_id = str(uuid.uuid4())
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name, mask, type, subtype)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (acct_id, conn_id, "plaid-" + acct_id[:8], name, mask, acct_type, subtype),
    )
    conn.commit()
    conn.close()
    return acct_id


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_no_uuid_when_name_none_mask_set(db_path):
    """When name=None but mask='1234', page must show mask, not the UUID."""
    conn_id = _insert_connection(db_path)
    acct_id = _insert_account(db_path, conn_id, name=None, mask="1234", acct_type="depository")

    client = _make_authed_client(db_path)
    resp = client.get("/profile")
    assert resp.status_code == 200
    html = resp.text

    # UUID must not appear in the rendered page
    assert not _uuid_in_visible_text(html), "UUID found in profile page HTML — bug not fixed"
    # Mask must appear
    assert "1234" in html


def test_full_name_shown_when_set(db_path):
    """When name is set, it should appear in the page."""
    conn_id = _insert_connection(db_path)
    acct_id = _insert_account(
        db_path, conn_id, name="My Chequing", mask="9999", acct_type="depository"
    )

    client = _make_authed_client(db_path)
    resp = client.get("/profile")
    assert resp.status_code == 200
    html = resp.text

    assert "My Chequing" in html
    assert not _uuid_in_visible_text(html)


def test_subtype_used_when_name_none(db_path):
    """When name=None but subtype='checking' and mask='5678', page shows 'Checking ••••5678'."""
    conn_id = _insert_connection(db_path)
    _insert_account(
        db_path, conn_id, name=None, mask="5678", acct_type="depository", subtype="checking"
    )

    client = _make_authed_client(db_path)
    resp = client.get("/profile")
    assert resp.status_code == 200
    html = resp.text

    assert not _uuid_in_visible_text(html), "UUID found in profile page HTML"
    assert "Checking" in html
    assert "5678" in html


def test_unknown_account_when_all_none(db_path):
    """When name=mask=type=subtype=None, page shows 'Unknown Account', never a UUID."""
    conn_id = _insert_connection(db_path)
    _insert_account(db_path, conn_id, name=None, mask=None, acct_type=None, subtype=None)

    client = _make_authed_client(db_path)
    resp = client.get("/profile")
    assert resp.status_code == 200
    html = resp.text

    assert not _uuid_in_visible_text(html), "UUID found in profile page HTML"
    assert "Unknown Account" in html
