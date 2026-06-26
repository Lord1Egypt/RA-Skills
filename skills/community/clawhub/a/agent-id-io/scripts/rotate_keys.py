#!/usr/bin/env python3
"""
Generate a new Ed25519 + X25519 keypair and create or apply a rotation request.

The rotation signature proves ownership of the old keypair by signing
both new public keys (sign + encryption) with the old private key.

Usage:
    python3 rotate_keys.py agent_keys.json
    python3 rotate_keys.py agent_keys.json --new-keys new_agent_keys.json --payload rotation_payload.json
    python3 rotate_keys.py agent_keys.json --apply --token <jwt>

Default mode is manual: it writes the new key material and a POST payload
for the caller to submit. Use --apply to POST the rotation and atomically
replace the original key file only after the API accepts the new keys.

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from .crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer, resolve_api_base
except ImportError:
    from crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer, resolve_api_base

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
except ImportError:
    print("Error: 'cryptography' package required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

API_BASE = resolve_api_base()
ROTATION_SIG_CONTEXT = b"agent-id:rotate:v2:"


def build_rotation_signature_message(new_sign_pub_bytes: bytes, new_enc_pub_bytes: bytes) -> bytes:
    """Build canonical rotation-signature bytes with explicit domain separation."""
    return ROTATION_SIG_CONTEXT + new_sign_pub_bytes + new_enc_pub_bytes


def build_rotation_material(old_keys: dict) -> tuple[dict, dict]:
    """Generate new keys plus the rotation payload signed by the old key."""
    old_private_key = None
    new_sign_private = None
    new_enc_private = None
    old_priv_buf = to_secure_buffer(base64.b64decode(old_keys["sign_private_key"]))
    new_sign_priv_buf = bytearray()
    new_enc_priv_buf = bytearray()
    try:
        # Best-effort only: Python/C extensions may retain secret copies internally.
        old_private_key = Ed25519PrivateKey.from_private_bytes(bytes(old_priv_buf))

        new_sign_private = Ed25519PrivateKey.generate()
        new_sign_public = new_sign_private.public_key()
        new_sign_priv_buf = to_secure_buffer(
            new_sign_private.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        new_sign_pub_bytes = new_sign_public.public_bytes(Encoding.Raw, PublicFormat.Raw)

        new_enc_private = X25519PrivateKey.generate()
        new_enc_public = new_enc_private.public_key()
        new_enc_priv_buf = to_secure_buffer(
            new_enc_private.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        new_enc_pub_bytes = new_enc_public.public_bytes(Encoding.Raw, PublicFormat.Raw)

        rotation_signature_input = build_rotation_signature_message(new_sign_pub_bytes, new_enc_pub_bytes)
        rotation_signature = old_private_key.sign(rotation_signature_input)

        new_keys = {
            "warning": "KEEP THIS FILE SECRET. Never share private keys.",
            "sign_private_key": base64.b64encode(bytes(new_sign_priv_buf)).decode(),
            "sign_public_key": base64.b64encode(new_sign_pub_bytes).decode(),
            "enc_private_key": base64.b64encode(bytes(new_enc_priv_buf)).decode(),
            "enc_public_key": base64.b64encode(new_enc_pub_bytes).decode(),
        }
        if "agent_id" in old_keys:
            new_keys["agent_id"] = old_keys["agent_id"]
        if "display_name" in old_keys:
            new_keys["display_name"] = old_keys["display_name"]

        payload = {
            "new_public_sign_key": base64.b64encode(new_sign_pub_bytes).decode(),
            "new_public_enc_key": base64.b64encode(new_enc_pub_bytes).decode(),
            "rotation_signature": base64.b64encode(rotation_signature).decode(),
        }
        return new_keys, payload
    finally:
        secure_zero(old_priv_buf)
        if new_sign_priv_buf:
            secure_zero(new_sign_priv_buf)
        if new_enc_priv_buf:
            secure_zero(new_enc_priv_buf)
        if old_private_key is not None:
            del old_private_key
        if new_sign_private is not None:
            del new_sign_private
        if new_enc_private is not None:
            del new_enc_private


def main():
    parser = argparse.ArgumentParser(description="Rotate agent-id.io cryptographic keys")
    parser.add_argument("keys_file", help="Current agent_keys.json")
    parser.add_argument("--new-keys", default="new_agent_keys.json", help="Output file for new keys")
    parser.add_argument("--payload", default="rotation_payload.json", help="Output file for POST payload")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")
    parser.add_argument("--apply", action="store_true", help="Apply the rotation via API and atomically replace keys_file")
    parser.add_argument("--token", help="Bearer token for --apply (or set AGENT_ID_TOKEN)")
    args = parser.parse_args()

    if args.apply:
        token = args.token or os.environ.get("AGENT_ID_TOKEN")
        if not token:
            print("Error: --apply requires --token or AGENT_ID_TOKEN.", file=sys.stderr)
            sys.exit(1)
    else:
        for path in [args.new_keys, args.payload]:
            if os.path.exists(path) and not args.overwrite:
                print(f"Error: {path} already exists. Use --overwrite to replace.", file=sys.stderr)
                sys.exit(1)

    with open(args.keys_file) as f:
        old_keys = json.load(f)

    new_keys, payload = build_rotation_material(old_keys)
    new_keys_buf = to_secure_buffer(json.dumps(new_keys, indent=2))
    payload_buf = to_secure_buffer(json.dumps(payload, indent=2))

    try:
        if args.apply:
            agent_id = old_keys.get("agent_id")
            if not agent_id:
                print("Error: --apply requires agent_id in the existing keys file.", file=sys.stderr)
                sys.exit(1)

            response = requests.post(
                f"{API_BASE}/agents/{agent_id}/keys/rotate",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=10,
            )
            if response.status_code in (400, 401, 403):
                print(f"Error: rotation failed ({response.status_code}): {response.text}", file=sys.stderr)
                sys.exit(1)
            response.raise_for_status()

            backup_path = f"{args.keys_file}.bak"
            with open(args.keys_file, "rb") as handle:
                original_buf = to_secure_buffer(handle.read())
            try:
                atomic_write(backup_path, bytes(original_buf), mode=0o600)
            finally:
                secure_zero(original_buf)

            atomic_write(args.keys_file, bytes(new_keys_buf), mode=0o600)

            print(f"✅ Rotation applied → {args.keys_file}")
            print(f"✅ Backup saved → {backup_path}")
            return

        writer = atomic_write if args.overwrite else atomic_write_new
        try:
            writer(args.new_keys, bytes(new_keys_buf), mode=0o600)
            writer(args.payload, bytes(payload_buf), mode=0o600)
        except FileExistsError as exc:
            existing_path = exc.filename or str(exc)
            print(f"Error: {existing_path} already exists. Use --overwrite to replace.", file=sys.stderr)
            sys.exit(1)

        print(f"✅ New keys → {args.new_keys}")
        print(f"✅ Rotation payload → {args.payload}")
        print("Warning: manual mode does not update the original key file atomically.", file=sys.stderr)
        print("Use --apply with a Bearer token to rotate remotely and replace the key file safely.", file=sys.stderr)
        print(f"\nPOST this payload to:")
        print(f"  POST {API_BASE}/agents/<agent_id>/keys/rotate")
        print(f"  Authorization: Bearer <token>")
        print(f"\nAfter successful rotation:")
        print(f"  mv {args.new_keys} {args.keys_file}")
    finally:
        secure_zero(new_keys_buf)
        secure_zero(payload_buf)


if __name__ == "__main__":
    main()
