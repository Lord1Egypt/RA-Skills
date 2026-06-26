#!/usr/bin/env python3
"""
Sign an agent-id.io auth challenge with the agent's Ed25519 private key.

Signing procedure (WebAuthn assertion):
  signedData = authenticatorData + SHA256(clientDataJSON)
  signature = Ed25519.Sign(private_key, signedData)

Usage:
    python3 sign_challenge.py <challenge_base64url> agent_keys.json [--agent-id uuid]
    python3 sign_challenge.py <challenge> keys.json --output signed.json

Outputs the auth/verify payload as JSON.

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import hashlib
import json
import sys

try:
    from .crypto_utils import atomic_write, secure_zero, to_secure_buffer, validate_challenge
except ImportError:
    from crypto_utils import atomic_write, secure_zero, to_secure_buffer, validate_challenge

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
except ImportError:
    print("Error: 'cryptography' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

RP_ID = "agent-id.io"
ORIGIN = "https://agent-id.io"


def b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def main():
    parser = argparse.ArgumentParser(description="Sign agent-id.io auth challenge")
    parser.add_argument("challenge", help="Base64url challenge from /auth/challenge")
    parser.add_argument("keys_file", help="Path to agent_keys.json")
    parser.add_argument("--agent-id", help="Agent UUID (or read from keys_file)")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()
    validate_challenge(args.challenge)

    with open(args.keys_file) as f:
        keys = json.load(f)

    private_key = None
    priv_buf = to_secure_buffer(base64.b64decode(keys["sign_private_key"]))
    try:
        # Best-effort only: Python/C extensions may retain private key copies internally.
        private_key = Ed25519PrivateKey.from_private_bytes(bytes(priv_buf))
        pub_bytes = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        credential_id = b64url_encode(pub_bytes)

        # Build authenticatorData
        rp_id_hash = hashlib.sha256(RP_ID.encode()).digest()
        flags = bytes([0x01])
        sign_count = (0).to_bytes(4, "big")
        authenticator_data = rp_id_hash + flags + sign_count

        # Build clientDataJSON
        client_data = json.dumps({
            "type": "webauthn.get",
            "challenge": args.challenge,
            "origin": ORIGIN,
        }, separators=(",", ":")).encode()

        # Sign authenticatorData + SHA256(clientDataJSON)
        client_data_hash = hashlib.sha256(client_data).digest()
        signed_data = authenticator_data + client_data_hash
        signature = private_key.sign(signed_data)

        payload = {
            "agent_id": args.agent_id or keys.get("agent_id", "<your-agent-id-uuid>"),
            "credential_id": credential_id,
            "authenticator_data": b64url_encode(authenticator_data),
            "client_data_json": b64url_encode(client_data),
            "signature": b64url_encode(signature),
        }

        output = json.dumps(payload, indent=2)
        if args.output:
            atomic_write(args.output, output, mode=0o600)
            print(f"✅ Signed payload written to {args.output}", file=sys.stderr)
        else:
            print(output)
    finally:
        secure_zero(priv_buf)
        if private_key is not None:
            del private_key


if __name__ == "__main__":
    main()
