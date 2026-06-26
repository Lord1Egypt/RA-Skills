"""
tests/ui/test_settings.py — Playwright tests for the /settings page.

Smoke checks:
  - Page requires authentication
  - Page loads after login with Settings heading
  - Home Currency dropdown is present with CAD option
  - Save button is visible
  - Saving a currency value redirects with ?saved=1

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


def test_settings_requires_auth(page, server_url):
    """GET /settings without auth redirects to /login."""
    page.goto(server_url + "/settings")
    assert "/login" in page.url, f"Expected redirect to /login, got {page.url}"


def test_settings_loads_after_login(page, server_url):
    """Authenticated GET /settings shows the Settings heading."""
    _login(page, server_url)
    page.goto(server_url + "/settings")
    assert "/settings" in page.url
    heading = page.locator("h1")
    assert heading.count() > 0
    assert "Settings" in heading.first.inner_text()


def test_settings_has_currency_dropdown(page, server_url):
    """Settings page has a Home Currency dropdown."""
    _login(page, server_url)
    page.goto(server_url + "/settings")
    select = page.locator("select#home_currency")
    assert select.count() > 0, "Expected #home_currency select on /settings"
    assert select.first.is_visible()


def test_settings_currency_dropdown_has_cad(page, server_url):
    """Home Currency dropdown includes CAD option."""
    _login(page, server_url)
    page.goto(server_url + "/settings")
    cad_option = page.locator("select#home_currency option[value='CAD']")
    assert cad_option.count() > 0, "Expected CAD option in currency dropdown"


def test_settings_has_save_button(page, server_url):
    """Settings page has a Save / submit button."""
    _login(page, server_url)
    page.goto(server_url + "/settings")
    save_btn = page.locator("button[type=submit]")
    assert save_btn.count() > 0, "Expected a submit button on /settings"
    assert save_btn.first.is_visible()


def test_settings_save_redirects_with_saved_flag(page, server_url):
    """Submitting settings form redirects back with ?saved=1."""
    _login(page, server_url)
    page.goto(server_url + "/settings")
    # Select CAD (default) and save
    page.select_option("select#home_currency", "CAD")
    page.click("button[type=submit]")
    # Should redirect to /settings?saved=1
    page.wait_for_url("**/settings*", timeout=5000)
    assert "saved=1" in page.url, f"Expected ?saved=1 in URL after save, got {page.url}"
