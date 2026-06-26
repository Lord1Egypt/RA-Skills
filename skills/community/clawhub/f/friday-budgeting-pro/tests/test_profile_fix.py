"""Tests for Issue #157: Profile – Connect bank button placement + Last Synced display."""

from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Helpers to patch DB and session auth so we can render /profile
# ---------------------------------------------------------------------------

FAKE_TS = 1779649905  # a specific raw Unix timestamp


def _make_fake_connections():
    return [
        {
            "id": "conn-1",
            "institution_name": "Test Bank",
            "status": "active",
            "last_synced_at": FAKE_TS,  # raw UTC integer; JS renders client-side
        }
    ]


def _make_never_connections():
    return [
        {
            "id": "conn-2",
            "institution_name": "Empty Bank",
            "status": "active",
            "last_synced_at": 0,  # zero → "Never" in JS
        }
    ]


# ---------------------------------------------------------------------------
# Unit tests for _fmt_last_synced helper
# ---------------------------------------------------------------------------


def test_fmt_last_synced_zero():
    from ui.server import _fmt_last_synced

    assert _fmt_last_synced(0) == "Never"


def test_fmt_last_synced_none():
    from ui.server import _fmt_last_synced

    assert _fmt_last_synced(None) == "Never"


def test_fmt_last_synced_returns_readable():
    from ui.server import _fmt_last_synced

    result = _fmt_last_synced(FAKE_TS)
    # Must NOT be the raw integer
    assert str(FAKE_TS) not in result, f"Raw timestamp leaked: {result}"
    # Must look like a date (contains at least a year digit sequence)
    assert "2026" in result or len(result) > 6, f"Doesn't look like a date: {result}"


def test_fmt_last_synced_format():
    """Spot-check format: 'May 24, 2026 3:17 PM' style."""
    from ui.server import _fmt_last_synced

    # 2026-05-24 15:17:00 UTC → local; we just check it has recognizable parts
    result = _fmt_last_synced(FAKE_TS)
    assert "AM" in result or "PM" in result, f"No AM/PM in: {result}"
    assert "," in result, f"No comma (date format off): {result}"


# ---------------------------------------------------------------------------
# Integration: render /profile with mocked connections and check HTML layout
# ---------------------------------------------------------------------------


def _render_profile_html(monkeypatch, connections):
    """Return the rendered HTML for /profile with fake auth + connections."""
    import ui.server as srv

    # Patch auth so the request looks authenticated
    monkeypatch.setattr(srv, "_is_authenticated", lambda req: True)
    monkeypatch.setattr(srv, "_current_user_id", lambda req: "user-1")
    monkeypatch.setattr(srv, "_get_notification_pref", lambda: "openclaw")
    monkeypatch.setattr(srv, "_get_connections", lambda uid=None: connections)
    monkeypatch.setattr(srv, "_get_accounts", lambda uid=None: [])

    client = TestClient(srv.app, raise_server_exceptions=True)
    resp = client.get("/profile", follow_redirects=False)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    return resp.text


def test_data_utc_attribute_in_html(monkeypatch):
    """Profile HTML must include data-utc attribute with the raw timestamp.

    Client-side JS reads data-utc and converts to local datetime string.
    """
    connections = [
        {
            "id": "conn-1",
            "institution_name": "Test Bank",
            "status": "active",
            "last_synced_at": FAKE_TS,
        }
    ]
    html = _render_profile_html(monkeypatch, connections)
    assert (
        f'data-utc="{FAKE_TS}"' in html
    ), f'data-utc attribute not found in profile HTML (expected data-utc="{FAKE_TS}")'


def test_last_synced_shows_never_when_none(monkeypatch):
    """When last_synced_at is 0, display 'Never' server-side (JS also handles it)."""
    connections = [
        {
            "id": "conn-2",
            "institution_name": "Empty Bank",
            "status": "active",
            "last_synced_at": 0,
        }
    ]
    html = _render_profile_html(monkeypatch, connections)
    assert "Never" in html, "'Never' not found for unsynced connection"


def test_connect_button_in_linked_accounts_section(monkeypatch):
    """'+ Connect a bank' button must appear inside/near the Linked Accounts section."""
    connections = _make_fake_connections()
    html = _render_profile_html(monkeypatch, connections)

    linked_pos = html.find("Linked Accounts")
    connect_pos = html.find("Connect a bank")
    data_section_end = html.find("</section>", linked_pos)

    assert linked_pos != -1, "'Linked Accounts' heading not found"
    assert connect_pos != -1, "'Connect a bank' button not found"
    # Button must appear AFTER the heading
    assert connect_pos > linked_pos, "Connect button appears before Linked Accounts heading"
    # Button must appear BEFORE the section closes
    assert connect_pos < data_section_end, "Connect button is outside the Linked Accounts section"


def test_connect_button_near_heading(monkeypatch):
    """Connect button should be close to the heading (within ~500 chars = same header row)."""
    connections = _make_fake_connections()
    html = _render_profile_html(monkeypatch, connections)

    linked_pos = html.find("Linked Accounts")
    connect_pos = html.find("Connect a bank")

    assert linked_pos != -1
    assert connect_pos != -1
    gap = connect_pos - linked_pos
    assert gap < 500, f"Connect button too far from heading (gap={gap}). Not in header row?"
