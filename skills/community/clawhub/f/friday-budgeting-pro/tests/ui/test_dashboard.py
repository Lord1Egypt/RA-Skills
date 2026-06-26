"""
tests/ui/test_dashboard.py — Playwright tests for the /dashboard page.

Smoke checks:
  - Page loads after login
  - 'Sync Now' button is present
  - 'Export to Excel' link is present
  - Sync section heading is visible

Prerequisites (handled by conftest):
  - Server running with a DB pre-seeded with testuser/testpass.

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


def test_dashboard_requires_auth(page, server_url):
    """GET /dashboard without auth redirects to /login."""
    page.goto(server_url + "/dashboard")
    assert "/login" in page.url, f"Expected redirect to /login, got {page.url}"


def test_dashboard_loads_after_login(page, server_url):
    """Authenticated GET /dashboard returns 200 and shows Dashboard heading."""
    _login(page, server_url)
    assert "/dashboard" in page.url
    heading = page.locator("h1")
    assert heading.count() > 0
    assert "Dashboard" in heading.first.inner_text()


def test_dashboard_has_sync_now_button(page, server_url):
    """Dashboard page has a 'Sync Now' submit button."""
    _login(page, server_url)
    btn = page.locator("#btn-sync-now")
    assert btn.count() > 0, "Expected #btn-sync-now on dashboard"
    assert btn.first.is_visible()


def test_dashboard_has_export_excel_link(page, server_url):
    """Dashboard page has an 'Export to Excel' link."""
    _login(page, server_url)
    # The export link points to /export/excel
    link = page.locator("a[href='/export/excel']")
    assert link.count() > 0, "Expected 'Export to Excel' link on dashboard"
    assert link.first.is_visible()


def test_dashboard_shows_sync_section(page, server_url):
    """Dashboard has a Sync section with last-synced info."""
    _login(page, server_url)
    # There should be an h2 with "Sync" text
    sync_heading = page.locator("h2", has_text="Sync")
    assert sync_heading.count() > 0, "Expected a 'Sync' section heading on dashboard"
