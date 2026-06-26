#!/usr/bin/env python3
"""
Register a new agent on agent-id.io.

Full registration flow:
1. Generate Ed25519 + X25519 keypair
2. Request PoW challenge (hashcash-sha256)
3. Solve PoW: SHA256(challenge:subject:nonce) with >= difficulty leading zero bits
   where subject = hex(SHA256(public_sign_key_bytes))
4. POST registration with proof

Usage:
    python3 register.py --name "my-agent"
    python3 register.py --name "my-agent" --keys agent_keys.json

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import time

try:
    from .crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer, resolve_api_base
    from .keygen import resolve_output_path
    from .secure_keyfile import encrypt_key_material, resolve_passphrase
except ImportError:
    from crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer, resolve_api_base
    from keygen import resolve_output_path
    from secure_keyfile import encrypt_key_material, resolve_passphrase

try:
    import requests
except ImportError:
    print("Error: 'requests' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
except ImportError:
    print("Error: 'cryptography' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

API_BASE = resolve_api_base()


def generate_keypair():
    sign_priv = None
    enc_priv = None
    sign_priv_buf = bytearray()
    enc_priv_buf = bytearray()
    try:
        sign_priv = Ed25519PrivateKey.generate()
        sign_pub = sign_priv.public_key()
        enc_priv = X25519PrivateKey.generate()
        enc_pub = enc_priv.public_key()
        sign_priv_buf = to_secure_buffer(
            sign_priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        enc_priv_buf = to_secure_buffer(
            enc_priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        return {
            "sign_private_key": base64.b64encode(bytes(sign_priv_buf)).decode(),
            "sign_public_key": base64.b64encode(sign_pub.public_bytes(Encoding.Raw, PublicFormat.Raw)).decode(),
            "enc_private_key": base64.b64encode(bytes(enc_priv_buf)).decode(),
            "enc_public_key": base64.b64encode(enc_pub.public_bytes(Encoding.Raw, PublicFormat.Raw)).decode(),
        }
    finally:
        # Best-effort only: Python/C extensions may retain copies on the C heap.
        if sign_priv_buf:
            secure_zero(sign_priv_buf)
        if enc_priv_buf:
            secure_zero(enc_priv_buf)
        if sign_priv is not None:
            del sign_priv
        if enc_priv is not None:
            del enc_priv


def leading_zero_bits(data: bytes) -> int:
    count = 0
    for b in data:
        if b == 0:
            count += 8
        else:
            for i in range(7, -1, -1):
                if (b & (1 << i)) == 0:
                    count += 1
                else:
                    return count
            return count
    return count


def solve_pow(challenge: str, subject_hex: str, difficulty: int) -> str:
    """
    Find nonce (as string) where:
      SHA256(challenge + ':' + subject_hex + ':' + nonce)
    has >= difficulty leading zero bits.
    """
    print(f"  Solving PoW (difficulty={difficulty})...", end="", flush=True)
    start = time.time()
    nonce = 0
    while True:
        nonce_str = str(nonce)
        data = f"{challenge}:{subject_hex}:{nonce_str}".encode()
        digest = hashlib.sha256(data).digest()
        if leading_zero_bits(digest) >= difficulty:
            elapsed = time.time() - start
            print(f" done in {elapsed:.1f}s (nonce={nonce_str})")
            return nonce_str
        nonce += 1


def main():
    parser = argparse.ArgumentParser(description="Register a new agent on agent-id.io")
    parser.add_argument("--name", required=True, help="Agent display name (3-64 chars)")
    parser.add_argument("--keys", default="agent_keys.json", help="Keys file to create (default: agent_keys.json)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing keys file")
    parser.add_argument("--encrypt", action="store_true", help="Write an encrypted keyfile instead of plaintext JSON")
    parser.add_argument("--passphrase", help="Passphrase for --encrypt (or set AGENT_KEY_PASSPHRASE)")
    args = parser.parse_args()

    output_path = resolve_output_path(args.keys, args.encrypt)
    if os.path.exists(output_path) and not args.overwrite:
        print(f"Error: {output_path} already exists. Use --overwrite to replace.", file=sys.stderr)
        sys.exit(1)

    if not (3 <= len(args.name) <= 64):
        print("Error: display name must be 3-64 characters", file=sys.stderr)
        sys.exit(1)

    print(f"Registering '{args.name}' on agent-id.io...")

    # 1. Generate keypair
    print("1. Generating keypair...")
    keys = generate_keypair()
    sign_pub_b64 = keys["sign_public_key"]
    enc_pub_b64 = keys["enc_public_key"]
    sign_pub_bytes = base64.b64decode(sign_pub_b64)

    # subject = hex(SHA256(public_sign_key_bytes))
    subject_hex = hashlib.sha256(sign_pub_bytes).hexdigest()

    # 2. Request PoW challenge
    print("2. Requesting PoW challenge...")
    resp = requests.post(f"{API_BASE}/agents/register/challenge",
                         json={"public_sign_key": sign_pub_b64}, timeout=10)
    if resp.status_code == 429:
        retry = resp.headers.get("Retry-After", "60")
        print(f"Rate limited. Wait {retry}s and retry.", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    cd = resp.json()
    challenge = cd["challenge"]
    difficulty = cd["difficulty"]
    print(f"  Expires: {cd['expires_at']}")

    # 3. Solve PoW
    print("3. Solving Proof-of-Work...")
    nonce = solve_pow(challenge, subject_hex, difficulty)

    # 4. Register
    print("4. Registering...")
    resp = requests.post(f"{API_BASE}/agents/register", json={
        "display_name": args.name,
        "public_sign_key": sign_pub_b64,
        "public_enc_key": enc_pub_b64,
        "pow_challenge": challenge,
        "pow_nonce": nonce,
    }, timeout=10)

    if resp.status_code == 429:
        retry = resp.headers.get("Retry-After", "60")
        print(f"Rate limited on register. Wait {retry}s and retry.", file=sys.stderr)
        sys.exit(1)
    if resp.status_code == 400 and "invalid_pow" in resp.text:
        print("PoW validation failed (challenge may have expired). Re-run the script.", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()

    result = resp.json()
    agent_id = result["agent_id"]
    keys["agent_id"] = agent_id
    keys["display_name"] = result["display_name"]
    keys["warning"] = "KEEP THIS FILE SECRET. Never share private keys."

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

    print(f"\n✅ Registered!")
    print(f"  Agent ID:  {agent_id}")
    print(f"  Name:      {result['display_name']}")
    print(f"  Keys:      {output_path}")
    print(f"\nNext: python3 scripts/authenticate.py {output_path}")


if __name__ == "__main__":
    main()
