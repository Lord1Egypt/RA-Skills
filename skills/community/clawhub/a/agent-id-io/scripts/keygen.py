#!/usr/bin/env python3
"""
Generate Ed25519 (signing) + X25519 (encryption) keypair for agent-id.io registration.

Usage:
    python3 keygen.py
    python3 keygen.py --output my-agent-keys.json

Output: JSON file with private + public keys (base64 encoded).
        Public keys are ready to POST to /agents/register.
"""
import argparse
import base64
import json
import os
import sys

try:
    from .crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer
    from .secure_keyfile import encrypt_key_material, resolve_passphrase
except ImportError:
    from crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer
    from secure_keyfile import encrypt_key_material, resolve_passphrase

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
except ImportError:
    print("Error: 'cryptography' package required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


def resolve_output_path(path: str, encrypt: bool) -> str:
    """Return the on-disk output path for plaintext or encrypted key material."""
    if encrypt and not path.endswith(".enc"):
        return f"{path}.enc"
    return path


def main():
    parser = argparse.ArgumentParser(description="Generate agent-id.io keypair")
    parser.add_argument("--output", default="agent_keys.json", help="Output file (default: agent_keys.json)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing key file")
    parser.add_argument("--encrypt", action="store_true", help="Write an encrypted keyfile instead of plaintext JSON")
    parser.add_argument("--passphrase", help="Passphrase for --encrypt (or set AGENT_KEY_PASSPHRASE)")
    args = parser.parse_args()

    output_path = resolve_output_path(args.output, args.encrypt)
    if os.path.exists(output_path) and not args.overwrite:
        print(f"Error: {output_path} already exists. Use --overwrite to replace.", file=sys.stderr)
        sys.exit(1)

    sign_private = None
    enc_private = None
    sign_priv_buf = bytearray()
    enc_priv_buf = bytearray()
    try:
        sign_private = Ed25519PrivateKey.generate()
        sign_public = sign_private.public_key()
        sign_priv_buf = to_secure_buffer(
            sign_private.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        sign_pub_bytes = sign_public.public_bytes(Encoding.Raw, PublicFormat.Raw)

        enc_private = X25519PrivateKey.generate()
        enc_public = enc_private.public_key()
        enc_priv_buf = to_secure_buffer(
            enc_private.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        enc_pub_bytes = enc_public.public_bytes(Encoding.Raw, PublicFormat.Raw)

        keys = {
            "warning": "KEEP THIS FILE SECRET. Never share private keys.",
            "sign_private_key": base64.b64encode(bytes(sign_priv_buf)).decode(),
            "sign_public_key": base64.b64encode(sign_pub_bytes).decode(),
            "enc_private_key": base64.b64encode(bytes(enc_priv_buf)).decode(),
            "enc_public_key": base64.b64encode(enc_pub_bytes).decode(),
        }

        payload_buf = to_secure_buffer(json.dumps(keys, indent=2))
        try:
            writer = atomic_write if args.overwrite else atomic_write_new
            if args.encrypt:
                encrypt_key_material(
                    bytes(payload_buf),
                    output_path,
                    resolve_passphrase(args.passphrase),
                    overwrite=args.overwrite,
                )
            else:
                writer(output_path, bytes(payload_buf), mode=0o600)
                print(
                    f"Warning: plaintext private keys were written to {output_path}. Encrypt this file immediately.",
                    file=sys.stderr,
                )
        except FileExistsError:
            print(f"Error: {output_path} already exists. Use --overwrite to replace.", file=sys.stderr)
            sys.exit(1)
        finally:
            secure_zero(payload_buf)

        print(f"✅ Keys generated → {output_path}")
        print(f"\nFor POST /agents/register:")
        print(f'  "public_sign_key": "{keys["sign_public_key"]}"')
        print(f'  "public_enc_key":  "{keys["enc_public_key"]}"')
    finally:
        # Best-effort only: Python/C extensions may retain private key copies internally.
        if sign_priv_buf:
            secure_zero(sign_priv_buf)
        if enc_priv_buf:
            secure_zero(enc_priv_buf)
        if sign_private is not None:
            del sign_private
        if enc_private is not None:
            del enc_private


if __name__ == "__main__":
    main()
