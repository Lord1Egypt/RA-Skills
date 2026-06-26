"""
tests/test_plaid_e2e.py — End-to-end Plaid sandbox test.

Exercises the full Plaid flow against the real sandbox API using
plaid-python's SandboxPublicTokenCreate helper (no browser / Link UI needed).

Skips gracefully when PLAID_CLIENT_ID, PLAID_SECRET, or PLAID_ENV != "sandbox"
are not present in the environment — safe for CI runs without sandbox creds.

Reference: /Users/hal9000/.openclaw/workspace/plaid-test/index.js
  - institution_id "ins_109508" = "First Platypus Bank" (Plaid sandbox fixture)
  - sandboxPublicTokenCreate pattern reproduced here with plaid-python SDK

Run only this test:
    pytest -q -m e2e tests/test_plaid_e2e.py

Skip in CI by filtering out the marker:
    pytest -q -m "not e2e"
"""

from __future__ import annotations

import os

import keyring
import pytest
from keyring.backend import KeyringBackend

# ---------------------------------------------------------------------------
# Helpers: decide at collection time whether to skip
# ---------------------------------------------------------------------------


def _sandbox_creds_available() -> bool:
    return (
        bool(os.environ.get("PLAID_CLIENT_ID"))
        and bool(os.environ.get("PLAID_SECRET"))
        and os.environ.get("PLAID_ENV", "").lower() == "sandbox"
    )


# ---------------------------------------------------------------------------
# In-memory keyring (same pattern as tests/test_crypto.py)
# ---------------------------------------------------------------------------


class _InMemoryKeyring(KeyringBackend):
    """Simple dict-backed keyring — avoids touching the real macOS Keychain."""

    priority = 10  # must be > 0 to be considered

    def __init__(self):
        self._store: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, username: str) -> str | None:
        return self._store.get((service, username))

    def set_password(self, service: str, username: str, password: str) -> None:
        self._store[(service, username)] = password

    def delete_password(self, service: str, username: str) -> None:
        self._store.pop((service, username), None)


@pytest.fixture()
def in_memory_keyring():
    """
    Swap the global keyring backend for an in-memory store for the duration of
    each test, then restore the original and reset the cached Fernet instance.
    """
    original = keyring.get_keyring()
    mem = _InMemoryKeyring()
    keyring.set_keyring(mem)

    import server.crypto as crypto_mod

    crypto_mod._fernet = None

    yield mem

    keyring.set_keyring(original)
    crypto_mod._fernet = None


# ---------------------------------------------------------------------------
# E2E test
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.skipif(
    not _sandbox_creds_available(),
    reason=(
        "Plaid sandbox creds not set. "
        "Export PLAID_CLIENT_ID, PLAID_SECRET, and PLAID_ENV=sandbox to run."
    ),
)
def test_plaid_full_sandbox_flow(in_memory_keyring):
    """
    Full Plaid sandbox flow, no browser required.

    1. create_link_token        → non-empty link_token string
    2. sandbox public token     → public_token via SandboxPublicTokenCreateRequest
    3. exchange_public_token    → access_token + item_id present
    4. sync_transactions        → added/modified/removed lists + next_cursor key
    5. get_item_status          → returns a dict (may have None error fields)
    6. crypto round-trip        → encrypt(access_token) → decrypt → original
    """
    from plaid.model.products import Products
    from plaid.model.sandbox_public_token_create_request import (
        SandboxPublicTokenCreateRequest,
    )

    from server.crypto import decrypt, encrypt
    from server.providers.plaid import PlaidProvider

    provider = PlaidProvider()

    # ------------------------------------------------------------------
    # Step 1: create_link_token
    # ------------------------------------------------------------------
    link_token = provider.create_link_token()
    assert (
        isinstance(link_token, str) and link_token
    ), "create_link_token() must return a non-empty string"

    # ------------------------------------------------------------------
    # Step 2: create a sandbox public token (bypasses the Link UI)
    # Reference: index.js sandboxPublicTokenCreate with ins_109508
    # ------------------------------------------------------------------
    api_client = provider._build_client()  # reuse same env-var logic
    sandbox_request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",  # First Platypus Bank (Plaid sandbox fixture)
        initial_products=[Products("transactions")],
    )
    sandbox_response = api_client.sandbox_public_token_create(sandbox_request)
    public_token = sandbox_response["public_token"]
    assert (
        isinstance(public_token, str) and public_token
    ), "sandbox_public_token_create() must return a non-empty public_token"

    # ------------------------------------------------------------------
    # Step 3: exchange_public_token
    # ------------------------------------------------------------------
    exchange_result = provider.exchange_public_token(public_token)
    assert (
        "access_token" in exchange_result and exchange_result["access_token"]
    ), "exchange_public_token() must include a non-empty access_token"
    assert (
        "item_id" in exchange_result and exchange_result["item_id"]
    ), "exchange_public_token() must include a non-empty item_id"
    access_token = exchange_result["access_token"]

    # ------------------------------------------------------------------
    # Step 4: sync_transactions (initial fetch — cursor=None)
    # Fresh sandbox items may have 0 added transactions; that's fine.
    # ------------------------------------------------------------------
    sync_result = provider.sync_transactions(access_token, cursor=None)
    for key in ("added", "modified", "removed", "next_cursor"):
        assert key in sync_result, f"sync_transactions() result missing key '{key}'"
    assert isinstance(sync_result["added"], list), "added must be a list"
    assert isinstance(sync_result["modified"], list), "modified must be a list"
    assert isinstance(sync_result["removed"], list), "removed must be a list"

    # ------------------------------------------------------------------
    # Step 5: get_item_status
    # ------------------------------------------------------------------
    item_status = provider.get_item_status(access_token)
    assert isinstance(item_status, dict), "get_item_status() must return a dict"

    # ------------------------------------------------------------------
    # Step 6: crypto round-trip (in-memory keyring, no macOS Keychain I/O)
    # ------------------------------------------------------------------
    ciphertext = encrypt(access_token)
    assert isinstance(ciphertext, str) and ciphertext, "encrypt() must return a non-empty string"
    decrypted = decrypt(ciphertext)
    assert (
        decrypted == access_token
    ), "decrypt(encrypt(access_token)) must equal the original access_token"
