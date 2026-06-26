"""
tests/ui/test_profile.py — Playwright tests for the /profile page.

Route shape (from ui/server.py and ui/templates/profile.html):
  GET /profile    → settings + Linked Accounts section (auth required)
  /link/start     → Plaid Link initiation (linked via "+ Connect a bank" button)

Prerequisites (handled by conftest):
  - Server running with a DB pre-seeded with testuser/testpass.

Tests skip cleanly when Playwright / Chromium are not installed (see conftest).
"""

from __future__ import annotations

# Pre-seeded credentials (set up by tests/ui/_server_runner.py)
_USERNAME = "testuser"
_PASSWORD = "testpass"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _login(page, server_url: str) -> None:
    """Log in via the /login form."""
    page.goto(server_url + "/login")
    page.fill("input#username", _USERNAME)
    page.fill("input#password", _PASSWORD)
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard", timeout=5000)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_profile_shows_linked_accounts_section(page, server_url):
    """Authenticated /profile includes the 'Linked Accounts' section."""
    _login(page, server_url)
    page.goto(server_url + "/profile")

    # The <section id="linked-accounts"> is present and has a heading.
    heading = page.locator("#linked-accounts h2")
    assert heading.count() > 0
    assert "Linked Accounts" in heading.first.inner_text()


def test_profile_has_connect_bank_button(page, server_url):
    """Profile page shows a '+ Connect a bank' button."""
    _login(page, server_url)
    page.goto(server_url + "/profile")

    btn = page.locator("a", has_text="Connect a bank")
    assert btn.count() > 0, "Expected '+ Connect a bank' link on /profile"
    assert btn.first.is_visible()
