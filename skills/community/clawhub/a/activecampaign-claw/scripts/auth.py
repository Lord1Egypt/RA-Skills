#!/usr/bin/env python3
"""
auth.py — Manage AC API credentials via OS keychain or env vars.

Subcommands:
  status              Show which source each credential resolves from.
  set <url> <token>   Store both URL and token in the OS keychain.
  set-url <url>       Store just the URL.
  set-token <token>   Store just the token.
  clear               Remove URL and token from the OS keychain.

The OS keychain support is optional. If `keyring` is not installed, this
script will tell you how to enable it. Without keyring, set the
environment variables `AC_API_URL` and `AC_API_TOKEN` instead.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _skill.secrets import (  # noqa: E402
    delete_credential,
    describe_sources,
    has_keyring,
    set_credential,
)


def cmd_status(_args) -> int:
    sources = describe_sources()
    print("# Credential sources\n")
    print(f"- keyring package installed: {'yes' if sources['keyring_available'] else 'no'}")
    print(f"- AC_API_URL  resolves from: **{sources['AC_API_URL']}**")
    print(f"- AC_API_TOKEN resolves from: **{sources['AC_API_TOKEN']}**")
    print()
    if not sources["keyring_available"]:
        print("To enable OS keychain storage:")
        print("  pip install keyring")
        print()
    if sources["AC_API_URL"] == "missing" or sources["AC_API_TOKEN"] == "missing":
        print("To set credentials:")
        print("  export AC_API_URL='https://YOURACCOUNT.api-us1.com'   # in your shell profile")
        print("  export AC_API_TOKEN='YOUR-TOKEN'                       # in your shell profile")
        print("  # or, if keyring is installed:")
        print("  python3 scripts/auth.py set <url> <token>")
        return 1
    return 0


def _ensure_keyring() -> bool:
    if has_keyring():
        return True
    print(
        "ERROR: The `keyring` package isn't installed.\n"
        "Install it with `pip install keyring` to enable OS keychain support.",
        file=sys.stderr,
    )
    return False


def cmd_set(args) -> int:
    if not _ensure_keyring():
        return 1
    try:
        set_credential("AC_API_URL", args.url)
        set_credential("AC_API_TOKEN", args.token)
    except Exception as e:  # noqa: BLE001 — surface keychain backend errors
        print(_keychain_write_help(e), file=sys.stderr)
        return 1
    print("✓ Stored AC_API_URL and AC_API_TOKEN in the OS keychain.")
    print("  Future scripts will pick them up automatically. If you also")
    print("  have these set as env vars, the env vars will take precedence.")
    return 0


def _keychain_write_help(err: Exception) -> str:
    """Friendly message for the common 'non-interactive shell' keychain error."""
    msg = str(err)
    if "25308" in msg or "InteractionNotAllowed" in msg:
        return (
            "ERROR: macOS Keychain refused the write because this isn't an "
            "interactive Terminal session.\n"
            "Run this command from Terminal.app (not over SSH or from a "
            "non-interactive script) and approve the Keychain prompt."
        )
    return f"ERROR: {err}"


def cmd_set_url(args) -> int:
    if not _ensure_keyring():
        return 1
    try:
        set_credential("AC_API_URL", args.url)
    except Exception as e:  # noqa: BLE001
        print(_keychain_write_help(e), file=sys.stderr)
        return 1
    print("✓ Stored AC_API_URL in the OS keychain.")
    return 0


def cmd_set_token(args) -> int:
    if not _ensure_keyring():
        return 1
    try:
        set_credential("AC_API_TOKEN", args.token)
    except Exception as e:  # noqa: BLE001
        print(_keychain_write_help(e), file=sys.stderr)
        return 1
    print("✓ Stored AC_API_TOKEN in the OS keychain.")
    return 0


def cmd_clear(_args) -> int:
    if not _ensure_keyring():
        return 1
    url_removed = delete_credential("AC_API_URL")
    token_removed = delete_credential("AC_API_TOKEN")
    if url_removed or token_removed:
        print(f"✓ Removed from keychain: "
              f"{'AC_API_URL' if url_removed else ''}"
              f"{' + ' if (url_removed and token_removed) else ''}"
              f"{'AC_API_TOKEN' if token_removed else ''}.")
    else:
        print("Nothing to remove — no credentials were stored in the keychain.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage AC API credentials")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show where credentials resolve from")

    p_set = sub.add_parser("set", help="Store URL and token in the OS keychain")
    p_set.add_argument("url")
    p_set.add_argument("token")

    p_set_url = sub.add_parser("set-url", help="Store URL only")
    p_set_url.add_argument("url")

    p_set_tok = sub.add_parser("set-token", help="Store token only")
    p_set_tok.add_argument("token")

    sub.add_parser("clear", help="Remove URL and token from the OS keychain")

    args = parser.parse_args()
    handler = {
        "status":    cmd_status,
        "set":       cmd_set,
        "set-url":   cmd_set_url,
        "set-token": cmd_set_token,
        "clear":     cmd_clear,
    }[args.command]
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
