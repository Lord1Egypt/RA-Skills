#!/usr/bin/env python3
"""Cross-platform secret storage helpers for TOTP seeds."""

from __future__ import annotations

import platform
import subprocess

from totp_common import KEYCHAIN_SERVICE

try:
    import keyring
    from keyring.errors import KeyringError
except Exception:  # pragma: no cover - exercised through backend selection
    keyring = None
    KeyringError = Exception


def backend_name() -> str:
    if keyring is not None:
        return f"keyring:{keyring.get_keyring().__class__.__name__}"
    if platform.system() == "Darwin":
        return "macos-security-cli"
    raise RuntimeError(
        "No supported secure storage backend is available. "
        "Install the 'keyring' package to use system key storage on this platform."
    )


def _store_with_keyring(alias: str, seed: str) -> None:
    assert keyring is not None
    keyring.set_password(KEYCHAIN_SERVICE, alias, seed)


def _fetch_with_keyring(alias: str) -> str:
    assert keyring is not None
    secret = keyring.get_password(KEYCHAIN_SERVICE, alias)
    if not secret:
        raise KeyError(f"No TOTP seed found for alias '{alias}'.")
    return secret


def _delete_with_keyring(alias: str) -> None:
    assert keyring is not None
    try:
        keyring.delete_password(KEYCHAIN_SERVICE, alias)
    except Exception as exc:
        raise KeyError(f"No TOTP seed found for alias '{alias}'.") from exc


def _store_with_macos_security(alias: str, seed: str, issuer: str = "", account: str = "") -> None:
    label = f"{issuer} {account}".strip() or alias
    subprocess.run(
        [
            "security",
            "add-generic-password",
            "-U",
            "-a",
            alias,
            "-s",
            KEYCHAIN_SERVICE,
            "-l",
            label,
            "-w",
            seed,
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def _fetch_with_macos_security(alias: str) -> str:
    result = subprocess.run(
        [
            "security",
            "find-generic-password",
            "-a",
            alias,
            "-s",
            KEYCHAIN_SERVICE,
            "-w",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise KeyError(f"No TOTP seed found for alias '{alias}'.")
    return result.stdout.strip()


def _delete_with_macos_security(alias: str) -> None:
    result = subprocess.run(
        [
            "security",
            "delete-generic-password",
            "-a",
            alias,
            "-s",
            KEYCHAIN_SERVICE,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise KeyError(f"No TOTP seed found for alias '{alias}'.")


def store_seed(alias: str, seed: str, issuer: str = "", account: str = "") -> str:
    if keyring is not None:
        try:
            _store_with_keyring(alias, seed)
            return backend_name()
        except KeyringError as exc:
            if platform.system() != "Darwin":
                raise RuntimeError(f"Secure storage failed via keyring: {exc}") from exc
    if platform.system() == "Darwin":
        _store_with_macos_security(alias, seed, issuer=issuer, account=account)
        return backend_name()
    raise RuntimeError(
        "Secure storage is unavailable. Install the 'keyring' package to use the system vault on this platform."
    )


def fetch_seed(alias: str) -> str:
    if keyring is not None:
        try:
            return _fetch_with_keyring(alias)
        except KeyError:
            pass
        except KeyringError as exc:
            if platform.system() != "Darwin":
                raise RuntimeError(f"Secure storage failed via keyring: {exc}") from exc
    if platform.system() == "Darwin":
        return _fetch_with_macos_security(alias)
    raise KeyError(f"No TOTP seed found for alias '{alias}'.")


def delete_seed(alias: str) -> str:
    if keyring is not None:
        try:
            _delete_with_keyring(alias)
            return backend_name()
        except KeyError:
            pass
        except KeyringError as exc:
            if platform.system() != "Darwin":
                raise RuntimeError(f"Secure storage failed via keyring: {exc}") from exc
    if platform.system() == "Darwin":
        _delete_with_macos_security(alias)
        return backend_name()
    raise KeyError(f"No TOTP seed found for alias '{alias}'.")
