#!/usr/bin/env python3
"""
generate_dev_token.py — Generate an Apple Music Developer Token (JWT)

Required env vars:
  APPLE_KEY_ID             MusicKit key ID
  APPLE_TEAM_ID            Apple Developer Team ID
  APPLE_PRIVATE_KEY_PATH   Path to the .p8 private key file

Optional:
  APPLE_TOKEN_EXPIRY       Expiry in seconds (default: 15552000 = 180 days)

Dependencies: pip install PyJWT cryptography
"""

import sys
if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import os
import time

DEFAULT_EXPIRY = 15552000  # 180 days, Apple's maximum


class TokenError(Exception):
    """A dev token could not be made; the message says why and what to do."""


def make_dev_token(key_id: str, team_id: str, key_path: str, expiry: int = DEFAULT_EXPIRY) -> str:
    """Sign an ES256 developer token with the MusicKit .p8 key."""
    try:
        import jwt
    except ImportError:
        raise TokenError("PyJWT not installed.\n"
                         "  Install: python3 -m venv .venv && .venv/bin/pip install PyJWT cryptography") from None
    if not os.path.isfile(key_path):
        raise TokenError(f"Key file not found: {os.path.basename(key_path)}\n"
                         "  Check that the path points to the .p8 file you downloaded from Apple.")
    try:
        with open(key_path) as f:
            private_key = f.read()
    except OSError as e:
        raise TokenError(f"Can't read the key file {os.path.basename(key_path)}: {e.strerror or e}\n"
                         "  Check that it exists and that you can read it.") from e
    now = int(time.time())
    try:
        token = jwt.encode(
            {"iss": team_id, "iat": now, "exp": now + expiry},
            private_key, algorithm="ES256",
            headers={"alg": "ES256", "kid": key_id},
        )
    except Exception as e:
        raise TokenError(f"Failed to sign token: {e}\n"
                         "  Verify your .p8 key file is a valid ES256 private key.") from e
    return token.decode("utf-8") if isinstance(token, bytes) else token


def main():
    key_id = os.environ.get("APPLE_KEY_ID")
    team_id = os.environ.get("APPLE_TEAM_ID")
    key_path = os.environ.get("APPLE_PRIVATE_KEY_PATH")

    missing = [v for v, val in [("APPLE_KEY_ID", key_id), ("APPLE_TEAM_ID", team_id),
               ("APPLE_PRIVATE_KEY_PATH", key_path)] if not val]
    if missing:
        print(f"ERROR: Missing env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    try:
        expiry = int(os.environ.get("APPLE_TOKEN_EXPIRY", DEFAULT_EXPIRY))
    except ValueError:
        print("ERROR: APPLE_TOKEN_EXPIRY must be a number (seconds)", file=sys.stderr)
        sys.exit(1)

    try:
        token = make_dev_token(key_id, team_id, key_path, expiry)
    except TokenError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(token)
    print(f"\n✅ Token generated. Expires in {expiry // 86400} days.", file=sys.stderr)
    print("  export APPLE_MUSIC_DEV_TOKEN=\"<token printed to stdout>\"", file=sys.stderr)
    print("  Tip: scripts/setup_auth.py does this and the user token in one step.", file=sys.stderr)

if __name__ == "__main__":
    main()
