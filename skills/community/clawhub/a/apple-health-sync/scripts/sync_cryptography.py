#!/usr/bin/env python3
"""
Shared cryptography helpers for Apple Health Sync.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Tuple

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
except ImportError as import_error:  # pragma: no cover - import failure is runtime environment specific
    raise RuntimeError(
        "Missing Python dependency 'cryptography'. Install it before using protocol v5."
    ) from import_error


# Legacy v4 / previous version


def public_key_base64_from_pem(public_key_pem: str) -> str:
    body = (
        public_key_pem.replace("-----BEGIN PUBLIC KEY-----", "")
        .replace("-----END PUBLIC KEY-----", "")
        .replace("\n", "")
        .replace("\r", "")
        .strip()
    )
    if not body:
        raise RuntimeError("Public key PEM is empty.")
    return body


def canonical_json_bytes(value: Dict[str, Any]) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def build_legacy_onboarding_payload(
    user_id: str,
    onboarding_version: int,
    algorithm: str,
    public_key_base64: str,
) -> Dict[str, Any]:
    base_payload = {
        "v": onboarding_version,
        "id": user_id,
        "alg": algorithm,
        "publicKeyBase64": public_key_base64,
    }
    fingerprint = sha256_hex(canonical_json_bytes(base_payload))
    payload = dict(base_payload)
    payload["fingerprint"] = fingerprint
    return payload


def generate_legacy_rsa_keys(
    private_key_path: Path,
    public_key_path: Path,
    rotate: bool,
) -> str:
    private_exists = private_key_path.exists()
    public_exists = public_key_path.exists()
    if private_exists or public_exists:
        if private_exists and public_exists and not rotate:
            return "existing"
        if not rotate:
            raise RuntimeError("Only one key file exists. Fix manually or run with --rotate.")
        private_key_path.unlink(missing_ok=True)
        public_key_path.unlink(missing_ok=True)

    run_checked(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
            "-out",
            str(private_key_path),
        ]
    )

    run_checked(["openssl", "pkey", "-in", str(private_key_path), "-pubout", "-out", str(public_key_path)])
    os.chmod(private_key_path, 0o600)
    os.chmod(public_key_path, 0o644)
    return "generated"


def sign_legacy_challenge(private_key_path: Path, challenge: str, algorithm: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as challenge_file:
        challenge_file.write(challenge.encode("utf-8"))
        challenge_file_path = Path(challenge_file.name)
    with tempfile.NamedTemporaryFile(delete=False) as signature_file:
        signature_file_path = Path(signature_file.name)

    algo = algorithm.lower()
    if "rsa" in algo:
        command = [
            "openssl",
            "dgst",
            "-sha256",
            "-sign",
            str(private_key_path),
            "-binary",
            "-out",
            str(signature_file_path),
            str(challenge_file_path),
        ]
    else:
        command = [
            "openssl",
            "pkeyutl",
            "-sign",
            "-rawin",
            "-inkey",
            str(private_key_path),
            "-in",
            str(challenge_file_path),
            "-out",
            str(signature_file_path),
        ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        signature_bytes = signature_file_path.read_bytes()
        return base64.b64encode(signature_bytes).decode("ascii")
    except subprocess.CalledProcessError as sign_error:
        message = sign_error.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"Challenge signing failed: {message}") from sign_error
    finally:
        challenge_file_path.unlink(missing_ok=True)
        signature_file_path.unlink(missing_ok=True)


def read_legacy_rsa_block_size(private_key_path: Path) -> int:
    result = subprocess.run(
        ["openssl", "pkey", "-in", str(private_key_path), "-text", "-noout"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    key_size_match = None
    for line in result.stdout.splitlines():
        if "Private-Key:" in line:
            key_size_match = line
            break
    if not key_size_match:
        raise RuntimeError("Unable to determine RSA key size.")

    start = key_size_match.find("(")
    end = key_size_match.find(" bit")
    if start < 0 or end < 0:
        raise RuntimeError("Unable to determine RSA key size.")
    key_bits = int(key_size_match[start + 1:end])
    return key_bits // 8


def decrypt_legacy_rsa_chunk(private_key_path: Path, encrypted_chunk: bytes) -> bytes:
    with tempfile.NamedTemporaryFile(delete=False) as in_file:
        in_file.write(encrypted_chunk)
        in_path = Path(in_file.name)
    with tempfile.NamedTemporaryFile(delete=False) as out_file:
        out_path = Path(out_file.name)

    command = [
        "openssl",
        "pkeyutl",
        "-decrypt",
        "-inkey",
        str(private_key_path),
        "-in",
        str(in_path),
        "-out",
        str(out_path),
        "-pkeyopt",
        "rsa_padding_mode:oaep",
        "-pkeyopt",
        "rsa_oaep_md:sha256",
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return out_path.read_bytes()
    except subprocess.CalledProcessError as decrypt_error:
        message = decrypt_error.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"RSA decrypt failed: {message}") from decrypt_error
    finally:
        in_path.unlink(missing_ok=True)
        out_path.unlink(missing_ok=True)


def decrypt_legacy_rsa_chunked_payload(
    private_key_path: Path,
    encrypted_payload_b64: str,
    block_size: int,
) -> bytes:
    encrypted_bytes = base64.b64decode(encrypted_payload_b64)
    if len(encrypted_bytes) % block_size != 0:
        raise RuntimeError("Encrypted payload length does not align with RSA block size.")

    output = bytearray()
    for offset in range(0, len(encrypted_bytes), block_size):
        chunk = encrypted_bytes[offset : offset + block_size]
        output.extend(decrypt_legacy_rsa_chunk(private_key_path, chunk))
    return bytes(output)


# v5


V5_PROTOCOL_VERSION = 5
V5_SIGNING_ALGORITHM = "Ed25519"
V5_ENCRYPTION_ALGORITHM = "X25519"
V5_BOX_ALGORITHM = "X25519-ChaCha20Poly1305"
V5_HKDF_SALT = b"healthsync-v5"


def run_checked(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def b64decode_bytes(value: str) -> bytes:
    normalized = "".join(str(value).split())
    if not normalized:
        raise RuntimeError("Invalid base64 value: empty input.")
    padding = "=" * ((4 - len(normalized) % 4) % 4)
    try:
        return base64.b64decode(normalized + padding, validate=False)
    except Exception as decode_error:
        raise RuntimeError("Invalid base64 value.") from decode_error


def b64url_no_pad(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def canonical_json_string(value: Dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def fingerprint_hex(value: Dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_string(value).encode("utf-8")).hexdigest()


def key_id_from_public_key_base64(public_key_base64: str) -> str:
    return b64url_no_pad(hashlib.sha256(b64decode_bytes(public_key_base64)).digest())


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def atomic_write_bytes(path: Path, value: bytes, mode: int) -> None:
    ensure_parent_dir(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_bytes(value)
    os.chmod(tmp_path, mode)
    tmp_path.replace(path)


def generate_v5_keys(
    signing_private_path: Path,
    signing_public_path: Path,
    encryption_private_path: Path,
    encryption_public_path: Path,
    rotate: bool,
) -> str:
    existing_paths = [
        signing_private_path,
        signing_public_path,
        encryption_private_path,
        encryption_public_path,
    ]
    existing_count = sum(1 for path in existing_paths if path.exists())
    if existing_count:
        if existing_count == len(existing_paths) and not rotate:
            return "existing"
        if not rotate:
            raise RuntimeError("Only part of the v5 key set exists. Fix manually or run with --rotate.")
        for path in existing_paths:
            path.unlink(missing_ok=True)

    signing_private = ed25519.Ed25519PrivateKey.generate()
    signing_public = signing_private.public_key()
    encryption_private = x25519.X25519PrivateKey.generate()
    encryption_public = encryption_private.public_key()

    atomic_write_bytes(
        signing_private_path,
        signing_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        0o600,
    )
    atomic_write_bytes(
        signing_public_path,
        signing_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
        0o644,
    )
    atomic_write_bytes(
        encryption_private_path,
        encryption_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        0o600,
    )
    atomic_write_bytes(
        encryption_public_path,
        encryption_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
        0o644,
    )
    return "generated"


def load_ed25519_private_key(path: Path) -> ed25519.Ed25519PrivateKey:
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, ed25519.Ed25519PrivateKey):
        raise RuntimeError(f"Unexpected Ed25519 private key type: {path}")
    return key


def load_x25519_private_key(path: Path) -> x25519.X25519PrivateKey:
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, x25519.X25519PrivateKey):
        raise RuntimeError(f"Unexpected X25519 private key type: {path}")
    return key


def ed25519_public_key_base64_from_private_key(path: Path) -> str:
    key = load_ed25519_private_key(path)
    public_bytes = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return b64encode_bytes(public_bytes)


def x25519_public_key_base64_from_private_key(path: Path) -> str:
    key = load_x25519_private_key(path)
    public_bytes = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return b64encode_bytes(public_bytes)


def build_v5_onboarding_payload(
    user_id: str,
    signing_public_key_base64: str,
    encryption_public_key_base64: str,
) -> Dict[str, Any]:
    base_payload: Dict[str, Any] = {
        "v": V5_PROTOCOL_VERSION,
        "id": user_id,
        "sig": {
            "alg": V5_SIGNING_ALGORITHM,
            "publicKeyBase64": signing_public_key_base64,
        },
        "enc": {
            "alg": V5_ENCRYPTION_ALGORITHM,
            "box": V5_BOX_ALGORITHM,
            "publicKeyBase64": encryption_public_key_base64,
        },
    }
    payload = dict(base_payload)
    payload["fingerprint"] = fingerprint_hex(base_payload)
    return payload


def sign_v5_challenge(private_key_path: Path, challenge: str) -> str:
    private_key = load_ed25519_private_key(private_key_path)
    signature = private_key.sign(challenge.encode("utf-8"))
    return b64encode_bytes(signature)


def derive_v5_symmetric_key(shared_secret: bytes, aad_bytes: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=V5_HKDF_SALT,
        info=aad_bytes,
    ).derive(shared_secret)


def decrypt_v5_payload(
    payload: Dict[str, Any],
    encryption_private_key_path: Path,
    encryption_public_key_base64: str,
    expected_user_id: str,
    expected_scope: str,
    max_ciphertext_bytes: int,
    max_plaintext_bytes: int,
) -> Tuple[bytes, Dict[str, Any]]:
    if not isinstance(payload, dict):
        raise RuntimeError("Invalid v5 encrypted payload shape.")
    required_keys = {"alg", "kid", "epk", "nonce", "ciphertext"}
    if not required_keys.issubset(payload.keys()):
        raise RuntimeError("Incomplete v5 encrypted payload.")
    if payload.get("alg") != V5_BOX_ALGORITHM:
        raise RuntimeError("Unsupported v5 encrypted payload algorithm.")

    expected_kid = key_id_from_public_key_base64(encryption_public_key_base64)
    if payload.get("kid") != expected_kid:
        raise RuntimeError("Encrypted payload was not addressed to the configured v5 encryption key.")

    aad_object = {
        "scope": expected_scope,
        "user_id": expected_user_id,
    }
    aad = canonical_json_string(aad_object)
    aad_bytes = aad.encode("utf-8")

    ephemeral_public_bytes = b64decode_bytes(str(payload.get("epk", "")))
    nonce = b64decode_bytes(str(payload.get("nonce", "")))
    ciphertext = b64decode_bytes(str(payload.get("ciphertext", "")))
    if len(ephemeral_public_bytes) != 32:
        raise RuntimeError("Invalid ephemeral X25519 public key.")
    if len(nonce) != 12:
        raise RuntimeError("Invalid ChaCha20-Poly1305 nonce.")
    if len(ciphertext) > max_ciphertext_bytes:
        raise RuntimeError("V5 ciphertext exceeds configured maximum size.")

    private_key = load_x25519_private_key(encryption_private_key_path)
    peer_public_key = x25519.X25519PublicKey.from_public_bytes(ephemeral_public_bytes)
    shared_secret = private_key.exchange(peer_public_key)
    symmetric_key = derive_v5_symmetric_key(shared_secret, aad_bytes)
    cipher = ChaCha20Poly1305(symmetric_key)
    try:
        plaintext = cipher.decrypt(nonce, ciphertext, aad_bytes)
    except Exception as decrypt_error:
        raise RuntimeError("V5 payload decryption failed.") from decrypt_error
    if len(plaintext) > max_plaintext_bytes:
        raise RuntimeError("V5 plaintext exceeds configured maximum size.")
    return plaintext, aad_object


def encrypt_v5_payload(
    plaintext: bytes,
    user_id: str,
    scope: str,
    encryption_public_key_base64: str,
) -> Dict[str, str]:
    peer_public_bytes = b64decode_bytes(encryption_public_key_base64)
    if len(peer_public_bytes) != 32:
        raise RuntimeError("Invalid X25519 public key.")

    peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
    ephemeral_private_key = x25519.X25519PrivateKey.generate()
    ephemeral_public_key = ephemeral_private_key.public_key()
    shared_secret = ephemeral_private_key.exchange(peer_public_key)
    aad = canonical_json_string({
        "scope": scope,
        "user_id": user_id,
    })
    aad_bytes = aad.encode("utf-8")
    symmetric_key = derive_v5_symmetric_key(shared_secret, aad_bytes)
    cipher = ChaCha20Poly1305(symmetric_key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, plaintext, aad_bytes)
    envelope = {
        "alg": V5_BOX_ALGORITHM,
        "kid": key_id_from_public_key_base64(encryption_public_key_base64),
        "epk": b64encode_bytes(
            ephemeral_public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ),
        "nonce": b64encode_bytes(nonce),
        "ciphertext": b64encode_bytes(ciphertext),
    }
    return envelope


def resolve_v5_key_paths(secrets_dir: Path, config_dir: Path) -> Dict[str, Path]:
    return {
        "signing_private_key_path": secrets_dir / "signing_private_key_v5.pem",
        "signing_public_key_path": config_dir / "signing_public_key_v5.pem",
        "encryption_private_key_path": secrets_dir / "encryption_private_key_v5.pem",
        "encryption_public_key_path": config_dir / "encryption_public_key_v5.pem",
    }


def load_v5_public_keys_from_config(config: Dict[str, Any]) -> Tuple[str, str]:
    signing_public_key_base64 = str(config.get("signing_public_key_base64", "")).strip()
    encryption_public_key_base64 = str(config.get("encryption_public_key_base64", "")).strip()
    if not signing_public_key_base64 or not encryption_public_key_base64:
        raise RuntimeError("Missing v5 public keys in config.")
    return signing_public_key_base64, encryption_public_key_base64
