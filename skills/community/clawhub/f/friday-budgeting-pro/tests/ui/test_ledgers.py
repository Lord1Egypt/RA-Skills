"""
tests/ui/test_ledgers.py — Playwright tests for the /ledgers page.

Smoke checks:
  - Page requires authentication
  - Page loads after login with the Ledgers heading
  - The seeded 'Personal' ledger is shown
  - '+ Add Ledger' button is present
  - Income and Expenses sections are shown for the Personal ledger
  - Seeded line items (e.g. 'Salary', 'Groceries') are visible

Prerequisites (handled by conftest):
  - Server running with a DB pre-seeded with testuser/testpass + Personal ledger.

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


def test_ledgers_requires_auth(page, server_url):
    """GET /ledgers without auth redirects to /login."""
    page.goto(server_url + "/ledgers")
    assert "/login" in page.url, f"Expected redirect to /login, got {page.url}"


def test_ledgers_loads_after_login(page, server_url):
    """Authenticated GET /ledgers shows the Ledgers heading."""
    _login(page, server_url)
    page.goto(server_url + "/ledgers")
    assert "/ledgers" in page.url
    heading = page.locator("h1")
    assert heading.count() > 0
    assert "Ledgers" in heading.first.inner_text()


def test_ledgers_has_add_ledger_button(page, server_url):
    """Ledgers page has a '+ Add Ledger' button."""
    _login(page, server_url)
    page.goto(server_url + "/ledgers")
    btn = page.locator("#btn-add-ledger")
    assert btn.count() > 0, "Expected #btn-add-ledger on /ledgers"
    assert btn.first.is_visible()


def test_ledgers_shows_personal_ledger(page, server_url):
    """The seeded 'Personal' ledger is shown on the ledgers page."""
    _login(page, server_url)
    page.goto(server_url + "/ledgers")
    personal = page.locator(".ledger-name-display", has_text="Personal")
    assert personal.count() > 0, "Expected 'Personal' ledger on /ledgers"


def test_ledgers_shows_income_and_expense_sections(page, server_url):
    """Ledgers page shows Income and Expenses sections."""
    _login(page, server_url)
    page.goto(server_url + "/ledgers")
    income_heading = page.locator("h3", has_text="Income")
    expense_heading = page.locator("h3", has_text="Expenses")
    assert income_heading.count() > 0, "Expected an Income section in ledgers"
    assert expense_heading.count() > 0, "Expected an Expenses section in ledgers"


def test_ledgers_shows_seeded_line_items(page, server_url):
    """Seeded line items like 'Salary' and 'Groceries' appear in the ledger."""
    _login(page, server_url)
    page.goto(server_url + "/ledgers")
    salary = page.locator(".item-name-display", has_text="Salary")
    groceries = page.locator(".item-name-display", has_text="Groceries")
    assert salary.count() > 0, "Expected 'Salary' line item in ledger"
    assert groceries.count() > 0, "Expected 'Groceries' line item in ledger"
