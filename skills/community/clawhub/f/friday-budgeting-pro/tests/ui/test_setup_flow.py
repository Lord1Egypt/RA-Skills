"""
tests/ui/test_setup_flow.py — Playwright tests for the first-run setup wizard.

Since the shared test DB is pre-seeded with testuser, setup is already
"complete" and the wizard properly returns 404 for authenticated attempts.
These tests verify:
  - /setup returns 404 when setup is complete (correct guard behaviour)
  - /login page works as the post-setup entry point
  - Root / redirects to login (not setup) when a user exists

Tests skip cleanly when Playwright / Chromium are not installed (see conftest).
"""

from __future__ import annotations

# Pre-seeded credentials (set up by tests/ui/_server_runner.py)
_USERNAME = "testuser"
_PASSWORD = "testpass"


def test_root_redirects_to_login_when_setup_complete(page, server_url):
    """GET / → /login (not /setup) because the DB already has a user."""
    page.goto(server_url + "/")
    # Should redirect to /login since testuser exists and is not authenticated
    assert (
        "/login" in page.url or "/dashboard" in page.url
    ), f"Expected /login or /dashboard after /, got {page.url}"


def test_setup_returns_404_when_complete(page, server_url):
    """GET /setup returns 404 once the setup wizard has been completed."""
    response = page.goto(server_url + "/setup")
    assert response is not None
    # When setup is complete the server responds with 404
    assert (
        response.status == 404
    ), f"Expected 404 from /setup (setup already complete), got {response.status}"


def test_login_page_accessible_after_setup(page, server_url):
    """Login page is accessible and ready after setup is complete."""
    page.goto(server_url + "/login")
    assert page.locator("input#username").is_visible()
    assert page.locator("input#password").is_visible()
    assert page.locator("button[type=submit]").is_visible()


def test_setup_complete_user_can_login(page, server_url):
    """The user created during setup can log in successfully."""
    page.goto(server_url + "/login")
    page.fill("input#username", _USERNAME)
    page.fill("input#password", _PASSWORD)
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard", timeout=5000)
    assert "/dashboard" in page.url
