#!/usr/bin/env python3
"""
Authenticate to agent-id.io and get a JWT token.

WebAuthn assertion flow:
  signedData = authenticatorData + SHA256(clientDataJSON)
  signature = Ed25519.Sign(private_key, signedData)

Usage:
    python3 authenticate.py agent_keys.json --save-token token.txt
    python3 authenticate.py agent_keys.json --print-token

Token output is explicit-only. Token valid 15 minutes.

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import hashlib
import json
import os
import sys

try:
    from .crypto_utils import secure_zero, to_secure_buffer, write_secret_file, validate_challenge, resolve_api_base
except ImportError:
    from crypto_utils import secure_zero, to_secure_buffer, write_secret_file, validate_challenge, resolve_api_base

try:
    import requests
except ImportError:
    print("Error: 'requests' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
except ImportError:
    print("Error: 'cryptography' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

API_BASE = resolve_api_base()
RP_ID = "agent-id.io"
ORIGIN = "https://agent-id.io"


def b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def main():
    parser = argparse.ArgumentParser(description="Authenticate to agent-id.io")
    parser.add_argument("keys_file", help="Path to agent_keys.json")
    parser.add_argument("--save-token", help="Save token to this file")
    parser.add_argument("--print-token", action="store_true", help="Print token to stdout (explicit opt-in)")
    args = parser.parse_args()

    if not args.save_token and not args.print_token:
        print(
            "Error: token output is disabled by default. Use --save-token <path> or --print-token.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(args.keys_file) as f:
        keys = json.load(f)

    agent_id = keys.get("agent_id")
    if not agent_id:
        print("Error: agent_id not in keys file. Run register.py first.", file=sys.stderr)
        sys.exit(1)

    private_key = None
    priv_buf = to_secure_buffer(base64.b64decode(keys["sign_private_key"]))
    try:
        # Best-effort only: Python/C extensions may retain private key copies internally.
        private_key = Ed25519PrivateKey.from_private_bytes(bytes(priv_buf))
        pub_bytes = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        credential_id = b64url_encode(pub_bytes)

        # Step 1: Get challenge
        resp = requests.post(f"{API_BASE}/auth/challenge",
                             json={"agent_id": agent_id}, timeout=10)
        if resp.status_code == 403 and "revoked" in resp.text:
            print("Error: Agent revoked. Unrevoke first.", file=sys.stderr)
            sys.exit(1)
        if resp.status_code == 429:
            print(f"Rate limited. Retry after: {resp.headers.get('Retry-After', '?')}s", file=sys.stderr)
            sys.exit(1)
        resp.raise_for_status()
        challenge = resp.json()["challenge"]
        validate_challenge(challenge)

        # Build authenticatorData (rpIdHash + UP flag + sign_count)
        rp_id_hash = hashlib.sha256(RP_ID.encode()).digest()
        flags = bytes([0x01])   # UP (user present)
        sign_count = (0).to_bytes(4, "big")
        authenticator_data = rp_id_hash + flags + sign_count

        # Build clientDataJSON
        client_data = json.dumps({
            "type": "webauthn.get",
            "challenge": challenge,
            "origin": ORIGIN,
        }, separators=(",", ":")).encode()

        # Sign: authenticatorData + SHA256(clientDataJSON)
        client_data_hash = hashlib.sha256(client_data).digest()
        signed_data = authenticator_data + client_data_hash
        signature = private_key.sign(signed_data)

        # Step 2: Verify
        resp = requests.post(f"{API_BASE}/auth/verify", json={
            "agent_id": agent_id,
            "credential_id": credential_id,
            "authenticator_data": b64url_encode(authenticator_data),
            "client_data_json": b64url_encode(client_data),
            "signature": b64url_encode(signature),
        }, timeout=10)

        if resp.status_code == 401:
            print("Error: Authentication failed — wrong key or expired challenge.", file=sys.stderr)
            sys.exit(1)
        if resp.status_code == 429:
            print("Rate limited.", file=sys.stderr)
            sys.exit(1)
        resp.raise_for_status()

        result = resp.json()
        token = result["token"]
        expires_at = result["expires_at"]

        if args.save_token:
            write_secret_file(args.save_token, token)
            print(f"✅ Token saved to {args.save_token}", file=sys.stderr)

        if args.print_token:
            print(token)

        print(f"# Expires: {expires_at}", file=sys.stderr)
    finally:
        secure_zero(priv_buf)
        if private_key is not None:
            del private_key


if __name__ == "__main__":
    main()
