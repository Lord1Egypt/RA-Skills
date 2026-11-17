#!/usr/bin/env python3
"""EVE ESI token refresh helper.

Reads refresh_token from $OPENCLAW_STATE_DIR/eve-tokens.json (default: ~/.openclaw/) and returns a fresh access_token.

Usage:
    python get_token.py --char main          # prints a short-lived access token to stdout
    python get_token.py --char main --json   # token response as JSON, refresh_token redacted
    python get_token.py --char main --char-id  # prints only the character ID
    python get_token.py --list               # list all stored characters

Security note:
    Anything printed here goes to stdout and can end up in shell history, logs,
    CI output or agent chat transcripts. Prefer `esi_query.py --char main`,
    which resolves the token in-process and never prints it.

    Access tokens are short-lived (~20 minutes). The refresh token is NOT:
    it is a long-lived bearer credential that grants continued access to the
    account. `--json` therefore redacts it unless you pass
    `--include-refresh-token` explicitly.

    Capturing a printed token into a shell variable and passing it on a command
    line (`--token "$TOKEN"`) additionally exposes it via `ps` and shell history.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

from token_store import get_tokens_file, load_tokens, save_tokens_unlocked, token_file_lock
from user_agent import USER_AGENT


class TokenError(Exception):
    """Raised when token operations fail (missing file, refresh failure, etc.)."""


def refresh_access_token(refresh_token, client_id):
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }).encode()
    req = urllib.request.Request(
        "https://login.eveonline.com/v2/oauth/token",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise TokenError(f"Token refresh failed ({e.code}): {body}")
    except urllib.error.URLError as e:
        raise TokenError(f"Could not connect to EVE login server: {e.reason}")


def load_tokens_or_raise():
    tokens_file = get_tokens_file()
    if not os.path.exists(tokens_file):
        raise TokenError(f"Tokens file not found: {tokens_file}. Run auth_flow.py first to authenticate.")
    return load_tokens()


def validate_character_metadata(char_name, char_data):
    missing_fields = [
        field
        for field in ("refresh_token", "client_id")
        if not char_data.get(field)
    ]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise TokenError(
            f"Character '{char_name}' is missing required token metadata: {fields}. "
            f"Re-run auth_flow.py --char-name {char_name} to refresh the stored entry."
        )


def get_character_id(char_name):
    """Return the stored character_id for a character key."""
    chars = load_tokens_or_raise().get("characters", {})
    if char_name not in chars:
        raise TokenError(
            f"Character '{char_name}' not found. "
            f"Available: {', '.join(chars.keys()) or 'none'}. "
            f"Run auth_flow.py --char-name <name> to authenticate."
        )
    character_id = chars[char_name].get("character_id")
    if character_id is None:
        raise TokenError(
            f"Character '{char_name}' has no stored character_id. "
            f"Re-run auth_flow.py --char-name {char_name}."
        )
    return character_id


def resolve_access_token(char_name):
    """Refresh and return the full token response for a stored character.

    Importable entry point so other scripts can obtain a token in-process
    instead of passing it across a command line.
    """
    chars = load_tokens_or_raise().get("characters", {})
    if char_name not in chars:
        raise TokenError(
            f"Character '{char_name}' not found. "
            f"Available: {', '.join(chars.keys()) or 'none'}. "
            f"Run auth_flow.py --char-name <name> to authenticate."
        )

    # Lock the token file for the entire read-refresh-write cycle.
    # EVE SSO rotates refresh tokens on each use, so concurrent processes
    # must not read the same token before the new one is persisted.
    with token_file_lock():
        # Re-read under lock to get the freshest state
        tokens = load_tokens_or_raise()
        chars = tokens.get("characters", {})
        char = chars.get(char_name)
        if char is None:
            raise TokenError(
                f"Character '{char_name}' was removed before the lock could be acquired."
            )
        validate_character_metadata(char_name, char)

        token_data = refresh_access_token(char["refresh_token"], char["client_id"])
        if not token_data.get("access_token"):
            raise TokenError("Token refresh response did not include an access_token.")

        # Save updated refresh_token (EVE rotates it on each refresh)
        if "refresh_token" in token_data:
            chars[char_name]["refresh_token"] = token_data["refresh_token"]
            save_tokens_unlocked(tokens)

    return token_data


def main():
    parser = argparse.ArgumentParser(description="Get a fresh EVE ESI access token")
    parser.add_argument("--char", default="main",
                        help="Character key to use (default: main)")
    parser.add_argument("--json", action="store_true",
                        help="Output token response as JSON (refresh_token redacted)")
    parser.add_argument("--include-refresh-token", action="store_true",
                        help="With --json: include the long-lived refresh token in the "
                             "output. Only do this if you know where stdout ends up.")
    parser.add_argument("--char-id", action="store_true",
                        help="Print only the stored character ID (no token, no refresh)")
    parser.add_argument("--list", action="store_true",
                        help="List all stored characters")
    args = parser.parse_args()

    if args.list:
        chars = load_tokens_or_raise().get("characters", {})
        if not chars:
            print("No characters stored. Run auth_flow.py first.")
            return
        for key, c in chars.items():
            print(f"  {key}: {c.get('character_name')} (ID: {c.get('character_id')})")
        return

    if args.char_id:
        print(get_character_id(args.char))
        return

    token_data = resolve_access_token(args.char)

    if args.json:
        payload = dict(token_data)
        if "refresh_token" in payload and not args.include_refresh_token:
            # The refresh token is long-lived — never emit it unless asked.
            payload["refresh_token"] = "<redacted: pass --include-refresh-token to reveal>"
        elif args.include_refresh_token:
            print("WARNING: printing a long-lived refresh token to stdout. "
                  "Anyone who reads this output keeps account access until it is "
                  "revoked at https://community.eveonline.com/support/third-party/",
                  file=sys.stderr)
        print(json.dumps(payload, indent=2))
    else:
        print("Note: access token written to stdout (valid ~20 min). "
              "Prefer esi_query.py --char, which never prints it.", file=sys.stderr)
        print(token_data["access_token"])


if __name__ == "__main__":
    try:
        main()
    except TokenError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
