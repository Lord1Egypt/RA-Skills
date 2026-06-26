"""
tests/integration/test_plaid.py — Plaid sandbox integration test suite.

All tests run against the real Plaid sandbox API (no mocks).
They are SKIPPED gracefully when PLAID_CLIENT_ID or PLAID_SECRET env vars
are not set, so CI passes today and starts running real tests once the
GitHub Actions secrets are added.

To activate locally:
    export PLAID_CLIENT_ID=<your_id>
    export PLAID_SECRET=<your_sandbox_secret>
    export PLAID_ENV=sandbox
    pytest tests/integration/test_plaid.py -v
"""

from __future__ import annotations

import os

import pytest
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest

from server.providers.plaid import PlaidProvider

# ---------------------------------------------------------------------------
# Skip guard — all tests in this module are skipped when creds are absent
# ---------------------------------------------------------------------------

PLAID_CREDS_AVAILABLE = bool(os.environ.get("PLAID_CLIENT_ID")) and bool(
    os.environ.get("PLAID_SECRET")
)

pytestmark = pytest.mark.skipif(
    not PLAID_CREDS_AVAILABLE,
    reason=(
        "PLAID_CLIENT_ID and/or PLAID_SECRET not set — Plaid sandbox tests skipped. "
        "Add to GitHub Actions secrets to enable."
    ),
)

# ---------------------------------------------------------------------------
# Module-scoped fixtures (minimise Plaid API calls — sandbox rate limits)
# ---------------------------------------------------------------------------

_SANDBOX_INSTITUTION_ID = "ins_109508"  # First Platypus Bank (Plaid sandbox fixture)


@pytest.fixture(scope="module")
def provider() -> PlaidProvider:
    """PlaidProvider configured for the sandbox environment."""
    return PlaidProvider(env="sandbox")


@pytest.fixture(scope="module")
def access_token(provider: PlaidProvider) -> str:
    """
    Create a sandbox public token and exchange it for an access token.

    Module-scoped so the exchange only runs once per test session.
    """
    api_client = provider._build_client()
    sandbox_request = SandboxPublicTokenCreateRequest(
        institution_id=_SANDBOX_INSTITUTION_ID,
        initial_products=[Products("transactions")],
    )
    sandbox_response = api_client.sandbox_public_token_create(sandbox_request)
    public_token = sandbox_response["public_token"]

    result = provider.exchange_public_token(public_token)
    return result["access_token"]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_create_link_token_returns_valid_token(provider: PlaidProvider) -> None:
    """create_link_token() returns a string starting with 'link-sandbox-'."""
    token = provider.create_link_token(user_id="test-user")
    assert isinstance(token, str), "link token must be a string"
    assert token.startswith(
        "link-sandbox-"
    ), f"sandbox link token must start with 'link-sandbox-', got: {token!r}"


def test_sandbox_public_token_exchange(provider: PlaidProvider) -> None:
    """
    Full public-token round-trip:
      1. Mint a sandbox public token via sandbox_public_token_create.
      2. Exchange it via provider.exchange_public_token().
      3. Assert access_token starts with 'access-sandbox-' and item_id is non-empty.
    """
    api_client = provider._build_client()
    sandbox_request = SandboxPublicTokenCreateRequest(
        institution_id=_SANDBOX_INSTITUTION_ID,
        initial_products=[Products("transactions")],
    )
    sandbox_response = api_client.sandbox_public_token_create(sandbox_request)
    public_token = sandbox_response["public_token"]
    assert isinstance(public_token, str) and public_token, "public_token must be a non-empty string"

    result = provider.exchange_public_token(public_token)
    assert "access_token" in result, "exchange result must contain 'access_token'"
    assert "item_id" in result, "exchange result must contain 'item_id'"
    assert result["access_token"].startswith(
        "access-sandbox-"
    ), f"sandbox access_token must start with 'access-sandbox-', got: {result['access_token']!r}"
    assert result["item_id"], "item_id must be a non-empty string"


def test_get_institution_name(provider: PlaidProvider, access_token: str) -> None:
    """get_institution_name() returns a non-empty string for the sandbox item."""
    name = provider.get_institution_name(access_token)
    assert (
        isinstance(name, str) and name
    ), f"institution name must be a non-empty string, got: {name!r}"


def test_sync_transactions_initial_fetch(provider: PlaidProvider, access_token: str) -> None:
    """
    sync_transactions(cursor=None) returns the expected dict shape with seed data.

    Sandbox items are seeded with transactions, so:
      - added must be non-empty
      - next_cursor must be non-empty
    """
    result = provider.sync_transactions(access_token, cursor=None)

    for key in ("added", "modified", "removed", "next_cursor", "accounts"):
        assert key in result, f"sync result missing key '{key}'"

    assert isinstance(result["added"], list), "'added' must be a list"
    assert isinstance(result["modified"], list), "'modified' must be a list"
    assert isinstance(result["removed"], list), "'removed' must be a list"
    assert isinstance(result["accounts"], list), "'accounts' must be a list"

    assert len(result["added"]) > 0, "sandbox item should have seeded transactions in 'added'"
    assert result["next_cursor"], "'next_cursor' must be a non-empty string"


def test_sync_with_cursor_returns_delta(provider: PlaidProvider, access_token: str) -> None:
    """
    Calling sync_transactions twice in a row:
      - First call (cursor=None) populates the cursor.
      - Second call (cursor=<first cursor>) returns empty 'added' (no new txns).
    """
    first = provider.sync_transactions(access_token, cursor=None)
    cursor = first["next_cursor"]
    assert cursor, "first sync must return a non-empty next_cursor"

    second = provider.sync_transactions(access_token, cursor=cursor)
    assert (
        second["added"] == []
    ), "second sync with cursor should return no new 'added' transactions"


def test_get_item_status(provider: PlaidProvider, access_token: str) -> None:
    """
    get_item_status() returns the expected dict shape for a healthy sandbox item.

    A healthy item has error_code=None, error_message=None, and a non-empty item_id.
    """
    status = provider.get_item_status(access_token)

    assert isinstance(status, dict), "get_item_status() must return a dict"
    assert "error_code" in status, "status must contain 'error_code'"
    assert "error_message" in status, "status must contain 'error_message'"
    assert "item_id" in status, "status must contain 'item_id'"

    assert (
        status["error_code"] is None
    ), f"healthy sandbox item should have error_code=None, got: {status['error_code']!r}"
    assert (
        status["error_message"] is None
    ), f"healthy sandbox item should have error_message=None, got: {status['error_message']!r}"
    assert status["item_id"], "'item_id' must be a non-empty string"
