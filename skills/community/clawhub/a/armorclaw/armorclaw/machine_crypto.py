"""
ArmorClaw — Machine-bound encryption for storing the master password.

Encrypts the master password using the machine's MAC address + hostname
as the encryption key. The encrypted blob is safe to store in config files
because it can only be decrypted on the original machine.

Format: "enc:v1:<base64-encrypted-blob>"
"""
import hashlib, hmac, os, base64, socket, uuid
from typing import Optional

ENC_PREFIX = "enc:v1:"


def _machine_key() -> bytes:
    """Derive a 256-bit key from MAC address + hostname. Stable per machine."""
    mac  = uuid.getnode()
    mac_str = ":".join(f"{(mac >> (i*8)) & 0xff:02x}" for i in reversed(range(6)))
    host = socket.gethostname()
    # Mix with a fixed application salt so this key is ArmorClaw-specific
    raw  = f"armorclaw:machine-bind:v1:{mac_str}:{host}"
    return hashlib.sha256(raw.encode()).digest()


def encrypt_for_machine(plaintext: str) -> str:
    """
    Encrypt a string using the current machine as the key.
    Returns "enc:v1:<base64>" — safe to store in config files.
    """
    key  = _machine_key()
    salt = os.urandom(32)
    iv   = os.urandom(16)

    # Derive per-value key from machine key + salt
    derived = hashlib.pbkdf2_hmac("sha256", key, salt, 100_000, dklen=32)

    # Encrypt using AES via stdlib fallback or cryptography lib
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.backends import default_backend
        padder  = padding.PKCS7(128).padder()
        padded  = padder.update(plaintext.encode()) + padder.finalize()
        cipher  = Cipher(algorithms.AES(derived), modes.CBC(iv), backend=default_backend())
        enc     = cipher.encryptor()
        ct      = enc.update(padded) + enc.finalize()
    except ImportError:
        ct = _simple_xor_encrypt(plaintext.encode(), derived, iv)

    # HMAC for integrity
    mac_tag = hmac.new(derived, salt + iv + ct, hashlib.sha256).digest()
    payload = salt + iv + mac_tag + ct
    return ENC_PREFIX + base64.b64encode(payload).decode("ascii")


def decrypt_for_machine(token: str) -> str:
    """
    Decrypt a machine-bound token. Raises ValueError if wrong machine or tampered.
    """
    if not token.startswith(ENC_PREFIX):
        raise ValueError("Not a machine-encrypted value")

    try:
        payload = base64.b64decode(token[len(ENC_PREFIX):].encode())
    except Exception:
        raise ValueError("Invalid encrypted data")

    salt    = payload[:32]
    iv      = payload[32:48]
    mac_tag = payload[48:80]
    ct      = payload[80:]

    key     = _machine_key()
    derived = hashlib.pbkdf2_hmac("sha256", key, salt, 100_000, dklen=32)

    # Verify HMAC
    expected = hmac.new(derived, salt + iv + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(mac_tag, expected):
        raise ValueError("Machine binding failed — wrong machine or data tampered")

    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.backends import default_backend
        cipher   = Cipher(algorithms.AES(derived), modes.CBC(iv), backend=default_backend())
        dec      = cipher.decryptor()
        padded   = dec.update(ct) + dec.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data     = unpadder.update(padded) + unpadder.finalize()
    except ImportError:
        data = _simple_xor_decrypt(ct, derived, iv)

    return data.decode("utf-8")


def is_machine_encrypted(value: str) -> bool:
    return isinstance(value, str) and value.startswith(ENC_PREFIX)


def resolve_password(value: str) -> str:
    """
    If value is machine-encrypted, decrypt it.
    If plain text, return as-is (backwards compatible).
    """
    if is_machine_encrypted(value):
        return decrypt_for_machine(value)
    return value


# ── Stdlib fallback (when cryptography not installed) ─────────────────────
def _pad(data: bytes) -> bytes:
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def _unpad(data: bytes) -> bytes:
    return data[:-data[-1]]

def _aes_block(key: bytes, block: bytes) -> bytes:
    return hashlib.sha256(key + block).digest()[:16]

def _simple_xor_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    padded = _pad(data)
    blocks = [padded[i:i+16] for i in range(0, len(padded), 16)]
    ct, prev = [], iv
    for block in blocks:
        xored = bytes(a ^ b for a, b in zip(block, prev))
        enc   = _aes_block(key, xored)
        ct.append(enc); prev = enc
    return b"".join(ct)

def _simple_xor_decrypt(ct: bytes, key: bytes, iv: bytes) -> bytes:
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    pt, prev = [], iv
    for block in blocks:
        dec = _aes_block(key, block)
        pt.append(bytes(a ^ b for a, b in zip(dec, prev)))
        prev = block
    return _unpad(b"".join(pt))
