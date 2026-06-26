"""
Tests for server/crypto.py — token-at-rest encryption helpers.

Uses keyring's in-memory test backend so that no actual macOS Keychain
entries are created during CI or local test runs.
"""

import keyring
import keyring.errors
import pytest
from keyring.backend import KeyringBackend

# ---------------------------------------------------------------------------
# In-memory keyring backend (avoids touching the real macOS Keychain)
# ---------------------------------------------------------------------------


class _InMemoryKeyring(KeyringBackend):
    """Simple dict-backed keyring for testing."""

    priority = 10  # must be > 0 to be considered

    def __init__(self):
        self._store: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, username: str) -> str | None:
        return self._store.get((service, username))

    def set_password(self, service: str, username: str, password: str) -> None:
        self._store[(service, username)] = password

    def delete_password(self, service: str, username: str) -> None:
        self._store.pop((service, username), None)


class _BrokenKeyring(KeyringBackend):
    """Always raises — simulates an unusable Keychain backend."""

    priority = 10

    def get_password(self, service: str, username: str) -> str | None:
        raise keyring.errors.KeyringError("backend unavailable")

    def set_password(self, service: str, username: str, password: str) -> None:
        raise keyring.errors.KeyringError("backend unavailable")

    def delete_password(self, service: str, username: str) -> None:
        raise keyring.errors.KeyringError("backend unavailable")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=False)
def in_memory_keyring():
    """
    Replace the global keyring backend with an in-memory store for the
    duration of each test, then restore the original.
    Also resets the module-level _fernet cache so each test gets a fresh key.
    """
    original = keyring.get_keyring()
    mem = _InMemoryKeyring()
    keyring.set_keyring(mem)

    # Reset cached Fernet instance inside the module under test
    import server.crypto as crypto_mod

    crypto_mod._fernet = None

    yield mem

    # Restore
    keyring.set_keyring(original)
    crypto_mod._fernet = None


@pytest.fixture()
def broken_keyring():
    """Replace the global keyring backend with a permanently-broken one."""
    original = keyring.get_keyring()
    keyring.set_keyring(_BrokenKeyring())

    import server.crypto as crypto_mod

    crypto_mod._fernet = None

    yield

    keyring.set_keyring(original)
    crypto_mod._fernet = None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_round_trip(in_memory_keyring):
    """encrypt then decrypt returns the original plaintext."""
    from server.crypto import decrypt, encrypt

    plaintext = "access-sandbox-abc123def456"
    assert decrypt(encrypt(plaintext)) == plaintext


def test_tampered_ciphertext_raises(in_memory_keyring):
    """Decrypting a tampered ciphertext raises InvalidToken."""
    from cryptography.fernet import InvalidToken

    from server.crypto import decrypt, encrypt

    ciphertext = encrypt("some-plaid-token")
    # Flip a few bytes in the middle of the ciphertext
    bad = ciphertext[:-4] + "XXXX"
    with pytest.raises(InvalidToken):
        decrypt(bad)


def test_different_plaintexts_produce_different_ciphertexts(in_memory_keyring):
    """Two distinct plaintexts must encrypt to different ciphertexts."""
    from server.crypto import encrypt

    ct1 = encrypt("token-aaa")
    ct2 = encrypt("token-bbb")
    assert ct1 != ct2


def test_keychain_available_true_with_in_memory_backend(in_memory_keyring):
    """keychain_available() returns True when the backend is working."""
    from server.crypto import keychain_available

    assert keychain_available() is True


def test_init_crypto_raises_with_broken_backend(broken_keyring):
    """init_crypto() raises RuntimeError when the Keychain backend is broken."""
    from server.crypto import init_crypto

    with pytest.raises(RuntimeError, match="Keychain backend is not available"):
        init_crypto()


def test_encrypt_returns_string(in_memory_keyring):
    """encrypt() must return a plain string (safe for SQLite storage)."""
    from server.crypto import encrypt

    result = encrypt("hello")
    assert isinstance(result, str)
    assert len(result) > 0


def test_decrypt_returns_string(in_memory_keyring):
    """decrypt() must return a plain string."""
    from server.crypto import decrypt, encrypt

    result = decrypt(encrypt("world"))
    assert isinstance(result, str)


def test_key_persisted_across_calls(in_memory_keyring):
    """The same key is reused across multiple encrypt/decrypt calls."""
    from server.crypto import decrypt, encrypt

    ct = encrypt("persistent-token")
    # Decrypting with the *same* module (same key) should succeed
    assert decrypt(ct) == "persistent-token"


def test_key_generated_and_stored_in_keychain(in_memory_keyring):
    """get_or_create_key() stores the key in the keyring on first call."""
    import keyring as kr

    from server.crypto import get_or_create_key

    get_or_create_key()
    stored = kr.get_password("friday-budgeting-pro", "fernet-key")
    assert stored is not None
    assert len(stored) > 0
