"""
tests/ui/test_login.py — Playwright tests for the login / logout flow.

Prerequisites (handled by conftest):
  - Server running with a DB pre-seeded with testuser/testpass.

Tests skip cleanly when Playwright / Chromium are not installed (see conftest).
"""

from __future__ import annotations

# Pre-seeded credentials (set up by tests/ui/_server_runner.py)
_USERNAME = "testuser"
_PASSWORD = "testpass"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _login(page, server_url: str, username: str = _USERNAME, password: str = _PASSWORD) -> None:
    """Log in via the /login form."""
    page.goto(server_url + "/login")
    page.fill("input#username", username)
    page.fill("input#password", password)
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard", timeout=5000)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_login_page_renders(page, server_url):
    """GET /login shows username and password fields."""
    page.goto(server_url + "/login")
    assert page.locator("input#username").is_visible()
    assert page.locator("input#password").is_visible()


def test_login_wrong_password_shows_error(page, server_url):
    """Wrong password keeps the user on /login and shows an error."""
    page.goto(server_url + "/login")
    page.fill("input#username", _USERNAME)
    page.fill("input#password", "wrongpassword!")
    page.click("button[type=submit]")

    # Still on /login
    assert "/login" in page.url
    # Error message visible somewhere on the page
    assert page.locator(".alert-error").is_visible()


def test_login_correct_password_redirects_to_dashboard(page, server_url):
    """Correct credentials redirect to /dashboard."""
    page.goto(server_url + "/login")
    page.fill("input#username", _USERNAME)
    page.fill("input#password", _PASSWORD)
    page.click("button[type=submit]")

    page.wait_for_url("**/dashboard", timeout=5000)
    assert "/dashboard" in page.url


def test_logout_redirects_to_login(page, server_url):
    """Clicking Sign out lands back on /login."""
    _login(page, server_url)

    # Navigate to profile to find the Log out link
    page.goto(server_url + "/profile")
    # Click the Log out link
    page.click("a[href='/logout']")
    page.wait_for_url("**/login", timeout=5000)
    assert "/login" in page.url
