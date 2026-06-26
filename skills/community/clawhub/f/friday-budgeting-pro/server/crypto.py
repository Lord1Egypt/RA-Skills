"""
Token-at-rest encryption helpers for Friday Budgeting Pro.

Design constraint #8: Secrets never live in plaintext on disk.
Plaid access tokens are encrypted with Fernet; the key lives exclusively
in macOS Keychain (via the `keyring` library).  The DB file alone is
useless without Keychain access.

Usage:
    from server.crypto import init_crypto, encrypt, decrypt

    init_crypto()   # call at daemon startup — raises RuntimeError if Keychain unavailable
    token_ciphertext = encrypt(plaid_access_token)
    plaid_access_token = decrypt(token_ciphertext)
"""

import keyring
import keyring.errors
from cryptography.fernet import Fernet, InvalidToken  # noqa: F401 (re-exported)

_SERVICE = "friday-budgeting-pro"
_USERNAME = "fernet-key"

# Module-level cached Fernet instance; reset to None in tests via fixture.
_fernet: Fernet | None = None


def keychain_available() -> bool:
    """Return True if the keyring backend is operational (quick health check)."""
    try:
        # A lightweight probe: reading a missing key returns None — that's fine.
        keyring.get_password(_SERVICE, "__probe__")
        return True
    except (keyring.errors.KeyringError, Exception):
        return False


def get_or_create_key() -> bytes:
    """
    Return the Fernet key as raw bytes (url-safe-base64 encoded, 44 bytes).

    ``Fernet.generate_key()`` returns a url-safe-base64 string that is
    ready to pass directly to ``Fernet()``.  We store that string verbatim
    in the Keychain so no additional encoding layer is needed.

    If no key exists yet, one is generated and persisted.
    """
    stored: str | None = keyring.get_password(_SERVICE, _USERNAME)
    if stored is None:
        # generate_key() returns url-safe-b64 bytes (44 bytes, 32 decoded)
        fernet_key: bytes = Fernet.generate_key()
        stored = fernet_key.decode("utf-8")
        keyring.set_password(_SERVICE, _USERNAME, stored)
    # Return as bytes so callers can pass straight to Fernet()
    return stored.encode("utf-8")


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        key = get_or_create_key()
        _fernet = Fernet(key)
    return _fernet


def encrypt(plaintext: str) -> str:
    """
    Encrypt *plaintext* with Fernet.

    Returns a url-safe-base64 ciphertext string safe for SQLite storage.
    """
    f = _get_fernet()
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt(ciphertext: str) -> str:
    """
    Decrypt a Fernet ciphertext string produced by :func:`encrypt`.

    Raises :class:`cryptography.fernet.InvalidToken` if the ciphertext
    has been tampered with or was not produced by this key.
    """
    f = _get_fernet()
    return f.decrypt(ciphertext.encode("utf-8")).decode("utf-8")


def init_crypto() -> None:
    """
    Module-level guard — call at daemon startup.

    Verifies that the Keychain backend is reachable *and* that a key can
    be read/created.  Raises :class:`RuntimeError` if not; the daemon
    should refuse to start rather than silently fall back to plaintext
    storage (ARCHITECTURE.md Design Constraint #8).
    """
    if not keychain_available():
        raise RuntimeError(
            "Keychain backend is not available.  "
            "Friday Budgeting Pro refuses to start without a working Keychain "
            "because Plaid access tokens must be encrypted at rest "
            "(ARCHITECTURE.md Design Constraint #8).  "
            "Ensure the system keyring is configured before launching the daemon."
        )
    # Warm the Fernet instance so callers can use it immediately after init.
    _get_fernet()
