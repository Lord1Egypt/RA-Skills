"""Token storage backed by the OS keyring with an encrypted-file fallback for headless hosts.

When the OS keyring is unavailable (typical on bare Linux VPS without a Secret Service daemon, or
locked Keychain on a headless Mac), the user must set DAZZLE_KEYRING_PASSWORD so we can
load keyring's encrypted-file backend. We probe the chosen backend with a write-then-read on first
use and surface a clear error before any device flow starts, so the user never ends up with a
silent zero-byte token write.
"""

from __future__ import annotations

import getpass
import logging
import os
from typing import Final

import keyring
from keyring.errors import KeyringError, NoKeyringError

logger = logging.getLogger(__name__)

_PASSWORD_ENV_VAR: Final[str] = "DAZZLE_KEYRING_PASSWORD"
_FIELDS: Final[tuple[str, ...]] = ("refresh_token", "access_token", "expires_at", "client_id", "host")


def _service_name() -> str:
    user = getpass.getuser()
    return f"dazzle.{user}"


class StorageError(RuntimeError):
    """Raised when the keyring is unusable and no fallback can be initialized."""


def _try_initialize_fallback() -> None:
    """Switch to keyring's encrypted-file backend if the password env var is set."""
    password = os.environ.get(_PASSWORD_ENV_VAR)
    if not password:
        raise StorageError(
            "OS keyring is not available on this host. "
            f"Set {_PASSWORD_ENV_VAR} to use the encrypted-file fallback "
            "(see README headless setup)."
        )
    try:
        from keyrings.alt.file import EncryptedKeyring
    except ImportError as exc:
        raise StorageError("Encrypted-file backend not installed. Run: pip install keyrings.alt") from exc

    backend = EncryptedKeyring()
    backend.keyring_key = password
    keyring.set_keyring(backend)


def ensure_writable() -> None:
    """Probe the keyring backend with a write-then-read so failures surface early."""
    probe_service = _service_name()
    probe_key = "__probe__"
    probe_value = "ok"
    try:
        keyring.set_password(probe_service, probe_key, probe_value)
    except NoKeyringError:
        _try_initialize_fallback()
        keyring.set_password(probe_service, probe_key, probe_value)
    except KeyringError as exc:
        raise StorageError(f"Keyring backend rejected write: {exc}") from exc

    readback = keyring.get_password(probe_service, probe_key)
    if readback != probe_value:
        raise StorageError("Keyring write succeeded but readback returned a different value.")
    keyring.delete_password(probe_service, probe_key)


def get(field: str) -> str | None:
    if field not in _FIELDS:
        raise ValueError(f"Unknown storage field: {field}")
    try:
        return keyring.get_password(_service_name(), field)
    except NoKeyringError:
        _try_initialize_fallback()
        return keyring.get_password(_service_name(), field)


def set_(field: str, value: str) -> None:
    if field not in _FIELDS:
        raise ValueError(f"Unknown storage field: {field}")
    try:
        keyring.set_password(_service_name(), field, value)
    except NoKeyringError:
        _try_initialize_fallback()
        keyring.set_password(_service_name(), field, value)


def delete(field: str) -> None:
    if field not in _FIELDS:
        raise ValueError(f"Unknown storage field: {field}")
    try:
        keyring.delete_password(_service_name(), field)
    except NoKeyringError:
        _try_initialize_fallback()
        try:
            keyring.delete_password(_service_name(), field)
        except keyring.errors.PasswordDeleteError:
            return
    except keyring.errors.PasswordDeleteError:
        return


def clear_all() -> None:
    for field in _FIELDS:
        delete(field)
