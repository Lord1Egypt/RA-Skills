#!/usr/bin/env python3
"""
Derive SSH and PGP Ed25519 keys from the agent's master seed (Ed25519 private key).

Uses HKDF to deterministically derive child keys. The same master seed
always produces the same SSH and PGP keys — reproducible from backup.

Key hierarchy:
  master_seed (Ed25519 seed, 32 bytes)
  ├── HKDF(info="agent-id/ssh-ed25519")  → SSH Ed25519 key pair
  └── HKDF(info="agent-id/pgp-ed25519")  → PGP Ed25519 key pair

Usage:
    python3 derive_keys.py agent_keys.json
    python3 derive_keys.py agent_keys.json --out-dir ~/.ssh
    python3 derive_keys.py agent_keys.json --uid "My Agent <myagent@example.com>"

Output:
    id_agent_ed25519        SSH private key (OpenSSH format, chmod 600)
    id_agent_ed25519.pub    SSH public key
    agent_pgp_public.asc    PGP public key (ASCII-armored, importable with gpg)
    agent_pgp_private.asc   PGP private key (ASCII-armored, importable with gpg)

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import binascii
import hashlib
import json
import os
import struct
import sys
import time
from datetime import datetime, timezone

try:
    from .crypto_utils import atomic_write, secure_zero, to_secure_buffer
except ImportError:
    from crypto_utils import atomic_write, secure_zero, to_secure_buffer

try:
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except ImportError:
    print("Error: 'cryptography' required. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


def derive_child_seed(master_seed: bytes, info: str) -> bytes:
    """HKDF-SHA256: derive 32-byte child seed from master_seed."""
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                info=info.encode()).derive(master_seed)


def decode_master_seed(keys: dict) -> bytearray:
    """Decode and validate sign_private_key from keys json."""
    encoded_seed = keys.get("sign_private_key")
    if not isinstance(encoded_seed, str):
        raise ValueError("sign_private_key is missing or not a string")

    try:
        master_seed = base64.b64decode(encoded_seed, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("sign_private_key is not valid base64") from exc

    if len(master_seed) != 32:
        raise ValueError(
            f"sign_private_key must decode to exactly 32 bytes (got {len(master_seed)})"
        )

    return to_secure_buffer(master_seed)


# ── SSH ──────────────────────────────────────────────────────────────────────

def write_ssh_keys(ssh_seed: bytes, out_dir: str, comment: str) -> tuple:
    priv = Ed25519PrivateKey.from_private_bytes(ssh_seed)
    pub = priv.public_key()

    priv_pem = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.OpenSSH,
        serialization.NoEncryption(),
    )
    pub_raw = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    key_type = b"ssh-ed25519"
    wire = (struct.pack(">I", len(key_type)) + key_type +
            struct.pack(">I", len(pub_raw)) + pub_raw)
    pub_line = f"ssh-ed25519 {base64.b64encode(wire).decode()} {comment}\n"

    priv_path = os.path.join(out_dir, "id_agent_ed25519")
    pub_path = os.path.join(out_dir, "id_agent_ed25519.pub")
    atomic_write(priv_path, priv_pem, mode=0o600)
    atomic_write(pub_path, pub_line, mode=0o644)
    return priv_path, pub_path


# ── OpenPGP (pure Python, no pgpy) ───────────────────────────────────────────

def pgp_mpi(data: bytes) -> bytes:
    """OpenPGP Multi-Precision Integer encoding."""
    bits = len(data) * 8
    for byte in data:
        if byte == 0: bits -= 8
        else:
            b = byte
            while not (b & 0x80): bits -= 1; b <<= 1
            break
    return struct.pack(">H", bits) + data


def pgp_crc24(data: bytes) -> bytes:
    crc = 0xB704CE
    for byte in data:
        crc ^= byte << 16
        for _ in range(8):
            crc <<= 1
            if crc & 0x1000000: crc ^= 0x1864CFB
    return struct.pack(">I", crc & 0xFFFFFF)[1:]


def armor(data: bytes, label: str) -> str:
    lines = base64.b64encode(data).decode()
    lines = "\n".join(lines[i:i+64] for i in range(0, len(lines), 64))
    crc = base64.b64encode(pgp_crc24(data)).decode()
    return (f"-----BEGIN PGP {label}-----\n\n{lines}\n={crc}\n"
            f"-----END PGP {label}-----\n")


def pgp_packet(tag: int, body: bytes) -> bytes:
    """OpenPGP new-format packet."""
    n = len(body)
    if n < 192:   length_bytes = bytes([n])
    elif n < 8384: n2 = n - 192; length_bytes = bytes([((n2 >> 8) + 192), n2 & 0xFF])
    else:          length_bytes = b"\xff" + struct.pack(">I", n)
    return bytes([0xC0 | tag]) + length_bytes + body


# Ed25519 OID for OpenPGP: 1.3.6.1.4.1.11591.15.1
ED25519_OID = bytes([0x2b, 0x06, 0x01, 0x04, 0x01, 0xda, 0x47, 0x0f, 0x01])


def pgp_pubkey_body(pub_bytes: bytes, creation_time: int) -> bytes:
    mpi = pgp_mpi(bytes([0x40]) + pub_bytes)
    return (bytes([0x04]) + struct.pack(">I", creation_time) +
            bytes([0x16]) +  # algorithm 22 = EdDSA
            bytes([len(ED25519_OID)]) + ED25519_OID + mpi)


def pgp_fingerprint(key_body: bytes) -> bytes:
    # SHA1 is mandated by OpenPGP RFC 4880 §12.2 for V4 key fingerprints — not a security weakness here
    return hashlib.sha1(bytes([0x99]) + struct.pack(">H", len(key_body)) + key_body).digest()  # nosec B324


def pgp_seckey_body(pub_body: bytes, priv_seed: bytes) -> bytes:
    """Secret key packet: public key body + cleartext secret key material."""
    # S2K usage octet 0x00 = no passphrase
    # Secret key MPI: just the 32-byte seed (as MPI)
    secret_mpi = pgp_mpi(priv_seed)
    # Checksum: sum of all secret bytes mod 65536
    checksum = sum(secret_mpi) & 0xFFFF
    return pub_body + bytes([0x00]) + secret_mpi + struct.pack(">H", checksum)


def pgp_uid_packet(uid: str) -> bytes:
    uid_bytes = uid.encode()
    return pgp_packet(13, uid_bytes)  # tag 13 = User ID


def pgp_self_sig(pub_body: bytes, uid: str, priv: Ed25519PrivateKey, creation_time: int) -> bytes:
    """Self-signature packet (type 0x13 = positive certification)."""
    fp = pgp_fingerprint(pub_body)
    key_id = fp[-8:]

    # Hashed subpackets: signature creation time (type 2) + key flags (type 27)
    sig_creation = bytes([0x05, 0x02]) + struct.pack(">I", creation_time)
    key_flags = bytes([0x02, 0x1b, 0x03])  # certify + sign

    hashed_subs = sig_creation + key_flags
    hashed_subs_encoded = struct.pack(">H", len(hashed_subs)) + hashed_subs

    # Unhashed subpackets: issuer key ID (type 16)
    issuer_sub = bytes([0x09, 0x10]) + key_id
    unhashed_subs = struct.pack(">H", len(issuer_sub)) + issuer_sub

    # Signature body (without signature MPI) for hashing
    sig_body_prefix = (
        bytes([0x04, 0x13, 0x16, 0x08]) +  # version, type, pubkey algo (EdDSA), hash algo (SHA256)
        hashed_subs_encoded
    )

    # Data to sign: pubkey packet + UID packet + sig body prefix + trailer
    uid_bytes = uid.encode()
    pubkey_packet_for_hash = bytes([0x99]) + struct.pack(">H", len(pub_body)) + pub_body
    uid_for_hash = bytes([0xb4]) + struct.pack(">I", len(uid_bytes)) + uid_bytes
    trailer = bytes([0x04, 0xFF]) + struct.pack(">I", len(sig_body_prefix))
    to_sign = pubkey_packet_for_hash + uid_for_hash + sig_body_prefix + trailer

    digest = hashlib.sha256(to_sign).digest()
    signature = priv.sign(to_sign)  # Ed25519 signs the full data (not just hash)

    # Signature MPI: r and s are the 32-byte halves of the 64-byte Ed25519 signature
    sig_mpi_r = pgp_mpi(signature[:32])
    sig_mpi_s = pgp_mpi(signature[32:])

    sig_packet_body = (
        sig_body_prefix +
        unhashed_subs +
        digest[:2] +        # left 2 bytes of hash (quick check)
        sig_mpi_r + sig_mpi_s
    )
    return pgp_packet(2, sig_packet_body)


def write_pgp_keys(pgp_seed: bytes, out_dir: str, uid: str) -> tuple:
    """Write PGP public + private key in ASCII-armored OpenPGP format."""
    priv = Ed25519PrivateKey.from_private_bytes(pgp_seed)
    pub_bytes = priv.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)

    creation_time = int(time.time())
    pub_body = pgp_pubkey_body(pub_bytes, creation_time)

    pubkey_pkt = pgp_packet(6, pub_body)   # tag 6 = public key
    seckey_pkt = pgp_packet(5, pgp_seckey_body(pub_body, pgp_seed))  # tag 5 = secret key
    uid_pkt = pgp_uid_packet(uid)
    sig_pkt = pgp_self_sig(pub_body, uid, priv, creation_time)

    pub_cert = pubkey_pkt + uid_pkt + sig_pkt
    sec_cert = seckey_pkt + uid_pkt + sig_pkt

    pub_path = os.path.join(out_dir, "agent_pgp_public.asc")
    priv_path = os.path.join(out_dir, "agent_pgp_private.asc")
    atomic_write(pub_path, armor(pub_cert, "PUBLIC KEY BLOCK"), mode=0o644)
    atomic_write(priv_path, armor(sec_cert, "PRIVATE KEY BLOCK"), mode=0o600)

    fp = pgp_fingerprint(pub_body)
    return priv_path, pub_path, fp.hex().upper()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Derive SSH + PGP keys from agent-id.io master seed")
    parser.add_argument("keys_file", help="Path to agent_keys.json")
    parser.add_argument("--out-dir", default=".", help="Output directory (default: .)")
    parser.add_argument("--uid", help="PGP User ID (default: <agent_id>@agent-id.io)")
    parser.add_argument("--comment", help="SSH comment (default: <agent_id>@agent-id.io)")
    args = parser.parse_args()

    with open(args.keys_file) as f:
        keys = json.load(f)

    agent_id = keys.get("agent_id", "unknown")
    uid = args.uid or f"{agent_id} <{agent_id}@agent-id.io>"
    comment = args.comment or f"{agent_id}@agent-id.io"

    priv_buf = bytearray()
    ssh_seed = bytearray()
    pgp_seed = bytearray()
    try:
        priv_buf = decode_master_seed(keys)

        os.makedirs(args.out_dir, exist_ok=True)

        print(f"Agent: {agent_id}")
        print(f"Output: {args.out_dir}")
        print()

        # Best-effort only: Python/C extensions may retain derived-key copies internally.
        ssh_seed = to_secure_buffer(derive_child_seed(bytes(priv_buf), "agent-id/ssh-ed25519"))
        priv_path, pub_path = write_ssh_keys(bytes(ssh_seed), args.out_dir, comment)
        with open(pub_path) as handle:
            ssh_pub = handle.read().strip()
        print(f"✅ SSH private key → {priv_path}")
        print(f"✅ SSH public key  → {pub_path}")
        print(f"   {ssh_pub}")
        print()

        pgp_seed = to_secure_buffer(derive_child_seed(bytes(priv_buf), "agent-id/pgp-ed25519"))
        priv_path, pub_path, fp = write_pgp_keys(bytes(pgp_seed), args.out_dir, uid)
        key_id = fp[-16:]
        print(f"✅ PGP private key → {priv_path}")
        print(f"✅ PGP public key  → {pub_path}")
        print(f"   Fingerprint: {fp}")
        print(f"   Key ID: {key_id}")
        print(f"   UID: {uid}")
        print(f"   Import: gpg --import {pub_path}")
        print()

        print("ℹ️  Keys are DETERMINISTIC — regenerate anytime from agent_keys.json")
        print("   Keep agent_keys.json encrypted: python3 scripts/secure_keyfile.py encrypt agent_keys.json")
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    finally:
        if priv_buf:
            secure_zero(priv_buf)
        if ssh_seed:
            secure_zero(ssh_seed)
        if pgp_seed:
            secure_zero(pgp_seed)


if __name__ == "__main__":
    main()
