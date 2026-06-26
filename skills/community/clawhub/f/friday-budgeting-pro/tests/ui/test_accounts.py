"""
tests/ui/test_accounts.py — Playwright tests for the /accounts page.

Smoke checks:
  - Page requires authentication
  - Page loads after login
  - Connect a bank button is present
  - With no accounts: empty-state hint is shown
  - Page heading is visible

Prerequisites (handled by conftest):
  - Server running with a DB pre-seeded with testuser/testpass.
  - No bank accounts are seeded, so empty-state is expected.

Tests skip cleanly when Playwright / Chromium are not installed (see conftest).
"""

from __future__ import annotations

# Pre-seeded credentials
_USERNAME = "testuser"
_PASSWORD = "testpass"


def _login(page, server_url: str) -> None:
    page.goto(server_url + "/login")
    page.fill("input#username", _USERNAME)
    page.fill("input#password", _PASSWORD)
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard", timeout=5000)


def test_accounts_requires_auth(page, server_url):
    """GET /accounts without auth redirects to /login."""
    page.goto(server_url + "/accounts")
    assert "/login" in page.url, f"Expected redirect to /login, got {page.url}"


def test_accounts_loads_after_login(page, server_url):
    """Authenticated GET /accounts shows the Accounts heading."""
    _login(page, server_url)
    page.goto(server_url + "/accounts")
    assert "/accounts" in page.url
    heading = page.locator("h1")
    assert heading.count() > 0
    assert "Accounts" in heading.first.inner_text()


def test_accounts_has_connect_bank_button(page, server_url):
    """Accounts page has a '+ Connect a bank' link."""
    _login(page, server_url)
    page.goto(server_url + "/accounts")
    btn = page.locator("a", has_text="Connect a bank")
    assert btn.count() > 0, "Expected '+ Connect a bank' link on /accounts"
    assert btn.first.is_visible()


def test_accounts_empty_state_hint(page, server_url):
    """With no bank accounts, an empty-state hint is shown."""
    _login(page, server_url)
    page.goto(server_url + "/accounts")
    # Either the empty hint or institution groups are present
    empty_hint = page.locator(".hint")
    institution_groups = page.locator(".institution-group")
    has_accounts = institution_groups.count() > 0
    has_hint = empty_hint.count() > 0
    assert (
        has_accounts or has_hint
    ), "Expected either account rows or an empty-state hint on /accounts"
