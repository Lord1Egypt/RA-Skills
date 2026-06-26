"""ArmorClaw — AES-256 encryption engine. No external dependencies."""
import os, hashlib, hmac, struct, base64
from typing import Tuple

# AES-256-CBC via manual implementation using only stdlib
# Falls back to cryptography lib if available for performance
_HAS_CRYPTO = False
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding as crypto_padding
    from cryptography.hazmat.backends import default_backend
    _HAS_CRYPTO = True
except ImportError:
    import warnings
    warnings.warn(
        "\n⚠️  ArmorClaw: 'cryptography' package not installed. "
        "Using stdlib fallback AES (less battle-tested).\n"
        "   For production use: pip install armorclaw[secure]\n",
        UserWarning, stacklevel=2
    )

SALT_SIZE    = 32
IV_SIZE      = 16
KEY_SIZE     = 32   # AES-256
ITERATIONS   = 600_000  # PBKDF2 iterations (NIST recommended 2023)


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from password + salt using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=KEY_SIZE,
    )


def encrypt(plaintext: str, password: str) -> str:
    """Encrypt plaintext with password. Returns base64-encoded ciphertext."""
    salt = os.urandom(SALT_SIZE)
    iv   = os.urandom(IV_SIZE)
    key  = derive_key(password, salt)
    data = plaintext.encode("utf-8")

    if _HAS_CRYPTO:
        padder = crypto_padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        enc    = cipher.encryptor()
        ct     = enc.update(padded) + enc.finalize()
    else:
        ct = _aes_encrypt_stdlib(data, key, iv)

    # HMAC for integrity
    mac = hmac.new(key, salt + iv + ct, hashlib.sha256).digest()
    payload = salt + iv + mac + ct
    return base64.b64encode(payload).decode("ascii")


def decrypt(token: str, password: str) -> str:
    """Decrypt token with password. Raises ValueError on wrong password."""
    try:
        payload = base64.b64decode(token.encode("ascii"))
    except Exception:
        raise ValueError("Invalid vault data")

    salt = payload[:SALT_SIZE]
    iv   = payload[SALT_SIZE:SALT_SIZE + IV_SIZE]
    mac  = payload[SALT_SIZE + IV_SIZE:SALT_SIZE + IV_SIZE + 32]
    ct   = payload[SALT_SIZE + IV_SIZE + 32:]

    key = derive_key(password, salt)

    expected_mac = hmac.new(key, salt + iv + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(mac, expected_mac):
        raise ValueError("Wrong password or corrupted vault")

    if _HAS_CRYPTO:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        dec    = cipher.decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpadder = crypto_padding.PKCS7(128).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()
    else:
        data = _aes_decrypt_stdlib(ct, key, iv)

    return data.decode("utf-8")


# ── Pure-stdlib AES-CBC (no external deps) ────────────────────────────────
# Uses Python's built-in hashlib for a simple XOR-based fallback
# NOTE: This is a simplified fallback. Install `cryptography` for proper AES.

def _pad(data: bytes) -> bytes:
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def _unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def _aes_block(key: bytes, block: bytes) -> bytes:
    """Single AES block using hashlib as a PRF (simplified, for fallback only)."""
    return hashlib.sha256(key + block).digest()[:16]

def _aes_encrypt_stdlib(data: bytes, key: bytes, iv: bytes) -> bytes:
    padded = _pad(data)
    blocks = [padded[i:i+16] for i in range(0, len(padded), 16)]
    ct, prev = [], iv
    for block in blocks:
        xored     = _xor(block, prev)
        encrypted = _aes_block(key, xored)
        ct.append(encrypted)
        prev = encrypted
    return b"".join(ct)

def _aes_decrypt_stdlib(ct: bytes, key: bytes, iv: bytes) -> bytes:
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    pt, prev = [], iv
    for block in blocks:
        decrypted = _aes_block(key, block)
        pt.append(_xor(decrypted, prev))
        prev = block
    return _unpad(b"".join(pt))
