"""Token resolution that supports OS keychain as an optional source.

Lookup order:
  1. `AC_API_TOKEN` (or `AC_API_URL`) environment variable, if set.
     This keeps CI / Docker / scripted environments working without surprise.
  2. OS keychain via the `keyring` package, if installed AND the user has
     previously stored a value via `scripts/auth.py`.
  3. Neither — `ACClient.__init__` errors out as before.

Why env var first: developer testing and CI rely on env vars being
authoritative. If someone has a token in the macOS Keychain and then sets
`AC_API_TOKEN` to point at a sandbox, the env var should win.

`keyring` is an optional runtime dependency. If it isn't installed,
keychain lookup silently degrades to "not found" and the env var path
is the only source — no error, no warning.
"""

from __future__ import annotations

import os

# Namespace under which we store credentials in the keychain.
# `keyring.set_password(SERVICE_NAME, KEY, value)`.
SERVICE_NAME = "activecampaign-claw"


def _keyring_lookup(key: str) -> str | None:
    """Return the keychain value for `key`, or None if anything goes wrong.

    Importing `keyring` is lazy: most invocations won't touch it. On systems
    without the package installed (the default), this function is a no-op.
    """
    try:
        import keyring  # type: ignore[import-untyped]
    except ImportError:
        return None
    try:
        val = keyring.get_password(SERVICE_NAME, key)
        return val or None
    except Exception:  # noqa: BLE001 — any backend error degrades silently
        return None


def get_credential(key: str) -> str | None:
    """Resolve a credential by checking env vars first, then the keychain.

    Returns None if neither source has a value.
    """
    val = os.environ.get(key, "").strip()
    if val:
        return val
    return _keyring_lookup(key)


def set_credential(key: str, value: str) -> None:
    """Store a credential in the OS keychain. Raises if `keyring` isn't installed."""
    try:
        import keyring  # type: ignore[import-untyped]
    except ImportError as e:
        raise RuntimeError(
            "The `keyring` package isn't installed. Install it with "
            "`pip install keyring` to enable OS keychain support."
        ) from e
    keyring.set_password(SERVICE_NAME, key, value)


def delete_credential(key: str) -> bool:
    """Remove a credential from the OS keychain. Returns True if removed,
    False if it wasn't there or keychain support isn't available."""
    try:
        import keyring  # type: ignore[import-untyped]
        import keyring.errors  # type: ignore[import-untyped]
    except ImportError:
        return False
    try:
        keyring.delete_password(SERVICE_NAME, key)
        return True
    except keyring.errors.PasswordDeleteError:
        return False
    except Exception:  # noqa: BLE001
        return False


def has_keyring() -> bool:
    """Whether the keyring package is importable in this environment."""
    try:
        import keyring  # type: ignore[import-untyped]  # noqa: F401
        return True
    except ImportError:
        return False


def describe_sources() -> dict:
    """Diagnostic snapshot of where each credential is currently resolving from."""
    snapshot = {"keyring_available": has_keyring()}
    for key in ("AC_API_URL", "AC_API_TOKEN"):
        env_set = bool(os.environ.get(key, "").strip())
        keychain_set = _keyring_lookup(key) is not None
        if env_set:
            snapshot[key] = "env"
        elif keychain_set:
            snapshot[key] = "keychain"
        else:
            snapshot[key] = "missing"
    return snapshot
