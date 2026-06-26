#!/usr/bin/env python3
"""
Encrypt/decrypt agent_keys.json using AES-256-GCM with a passphrase.

The agent stores this encrypted file. To use any key-related script,
the agent decrypts the keyfile in memory — the plaintext never touches disk.

Usage:
    # Encrypt (protect the keyfile)
    python3 secure_keyfile.py encrypt agent_keys.json
    → creates agent_keys.json.enc (delete the plaintext after this)

    # Decrypt to stdout (pipe into other scripts)
    python3 secure_keyfile.py decrypt agent_keys.json.enc | python3 authenticate.py /dev/stdin

    # Decrypt to temp file (for use with scripts that need a file path)
    python3 secure_keyfile.py decrypt agent_keys.json.enc --out /tmp/keys_decrypted.json

The passphrase should be stored in a secret manager or injected at runtime via
an environment variable — NOT hardcoded in any script or config file.

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import getpass
import json
import os
import sys

try:
    from .crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer
except ImportError:
    from crypto_utils import atomic_write, atomic_write_new, secure_zero, to_secure_buffer

try:
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
except ImportError:
    print("Error: 'cryptography' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

MAGIC = b"AGENTKEY1"  # file format identifier
SCRYPT_N = 2**17       # CPU/memory cost (high = more secure, slower)
SCRYPT_R = 8
SCRYPT_P = 1


def derive_key(passphrase: str, salt: bytes, scrypt_n: int = SCRYPT_N) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=scrypt_n, r=SCRYPT_R, p=SCRYPT_P)
    return kdf.derive(passphrase.encode())


def encrypt_key_material(
    plaintext: bytes | str,
    output_path: str,
    passphrase: str,
    scrypt_n: int = SCRYPT_N,
    overwrite: bool = True,
) -> None:
    """Encrypt key material from memory without persisting plaintext to disk."""
    plaintext_buf = to_secure_buffer(plaintext)
    key_buf = bytearray()
    try:
        # Best-effort only: Python and C extensions may retain copies on the C heap.
        try:
            keys = json.loads(bytes(plaintext_buf))
            if "sign_private_key" not in keys:
                print("Warning: file doesn't look like an agent_keys.json", file=sys.stderr)
        except json.JSONDecodeError:
            print("Error: not valid JSON", file=sys.stderr)
            sys.exit(1)

        salt = os.urandom(32)
        nonce = os.urandom(12)
        key_buf = to_secure_buffer(derive_key(passphrase, salt, scrypt_n=scrypt_n))

        aesgcm = AESGCM(bytes(key_buf))
        ciphertext = MAGIC + salt + nonce + aesgcm.encrypt(nonce, bytes(plaintext_buf), None)
        writer = atomic_write if overwrite else atomic_write_new
        writer(output_path, ciphertext, mode=0o600)
    finally:
        secure_zero(plaintext_buf)
        if key_buf:
            secure_zero(key_buf)


def encrypt_keyfile(
    plaintext_path: str,
    output_path: str,
    passphrase: str,
    scrypt_n: int = SCRYPT_N,
    overwrite: bool = True,
) -> None:
    with open(plaintext_path, "rb") as f:
        raw = f.read()
    # Use secure buffer so the plaintext is zeroable after use
    plaintext_buf = to_secure_buffer(raw)
    try:
        encrypt_key_material(
            bytes(plaintext_buf),
            output_path,
            passphrase,
            scrypt_n=scrypt_n,
            overwrite=overwrite,
        )
    finally:
        secure_zero(plaintext_buf)


def decrypt_keyfile(
    encrypted_path: str,
    passphrase: str,
    scrypt_n: int = SCRYPT_N,
) -> bytes:
    with open(encrypted_path, "rb") as f:
        data = f.read()

    if not data.startswith(MAGIC):
        print("Error: not a valid encrypted agent keyfile", file=sys.stderr)
        sys.exit(1)

    offset = len(MAGIC)
    salt = data[offset:offset + 32]
    nonce = data[offset + 32:offset + 44]
    ciphertext = data[offset + 44:]

    key_buf = to_secure_buffer(derive_key(passphrase, salt, scrypt_n=scrypt_n))
    try:
        # Best-effort only: decrypt() and the crypto backend may keep internal copies.
        aesgcm = AESGCM(bytes(key_buf))
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        except InvalidTag:
            print("Error: wrong passphrase or corrupted file", file=sys.stderr)
            sys.exit(1)
        return plaintext
    finally:
        secure_zero(key_buf)


def resolve_passphrase(explicit_passphrase: str | None) -> str:
    """Resolve the encryption passphrase from CLI, env, or prompt.

    Warns when passphrase is supplied via CLI argument: it is visible in
    process listings (ps aux, /proc/<pid>/cmdline) on multi-user systems.
    Prefer AGENT_KEY_PASSPHRASE env var or the interactive prompt.
    """
    import sys  # local import to keep module-level clean
    if explicit_passphrase is not None:
        print(
            "Warning: --passphrase is visible in process listings (ps aux / /proc/*/cmdline). "
            "Prefer AGENT_KEY_PASSPHRASE env var or omit --passphrase for an interactive prompt.",
            file=sys.stderr,
        )
        return explicit_passphrase
    return (
        os.environ.get("AGENT_KEY_PASSPHRASE")
        or getpass.getpass("Passphrase: ")
    )


def main():
    parser = argparse.ArgumentParser(description="Encrypt/decrypt agent_keys.json")
    sub = parser.add_subparsers(dest="command")

    enc = sub.add_parser("encrypt", help="Encrypt agent_keys.json")
    enc.add_argument("keyfile", help="Path to agent_keys.json")
    enc.add_argument("--out", help="Output path (default: <keyfile>.enc)")
    enc.add_argument("--passphrase", help="Passphrase (or set AGENT_KEY_PASSPHRASE env var)")

    dec = sub.add_parser("decrypt", help="Decrypt agent_keys.json.enc")
    dec.add_argument("keyfile", help="Path to encrypted keyfile")
    dec.add_argument("--out", help="Output path (default: stdout)")
    dec.add_argument("--passphrase", help="Passphrase (or set AGENT_KEY_PASSPHRASE env var)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Get passphrase
    passphrase = resolve_passphrase(args.passphrase)

    if args.command == "encrypt":
        out_path = args.out or (args.keyfile + ".enc")
        print(f"Encrypting {args.keyfile} → {out_path}")
        encrypt_keyfile(args.keyfile, out_path, passphrase)
        print(f"✅ Encrypted → {out_path}")
        print(f"   Delete the plaintext: rm {args.keyfile}")

    elif args.command == "decrypt":
        plaintext = decrypt_keyfile(args.keyfile, passphrase)
        if args.out:
            plaintext_buf = to_secure_buffer(plaintext)
            try:
                atomic_write(args.out, bytes(plaintext_buf), mode=0o600)
                print(f"✅ Decrypted → {args.out}", file=sys.stderr)
            finally:
                secure_zero(plaintext_buf)
        else:
            sys.stdout.buffer.write(plaintext)


if __name__ == "__main__":
    main()
