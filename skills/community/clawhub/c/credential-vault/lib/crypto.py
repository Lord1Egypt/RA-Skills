"""Cryptographic utilities for AES-256-GCM encryption with PBKDF2 key derivation."""
import os
import hashlib
import base64
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


ITERATIONS = 600_000  # OWASP recommendation for PBKDF2-SHA256
KEY_LENGTH = 32  # 256 bits for AES-256


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from password using PBKDF2-SHA256.
    
    Args:
        password: Master password
        salt: Random salt (should be 16+ bytes)
    
    Returns:
        32-byte encryption key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode('utf-8'))


def generate_salt() -> bytes:
    """Generate a cryptographically secure random salt."""
    return os.urandom(16)


def generate_nonce() -> bytes:
    """Generate a random nonce for AES-GCM (96 bits recommended)."""
    return os.urandom(12)


def encrypt(plaintext: str, key: bytes) -> Tuple[bytes, bytes, bytes]:
    """Encrypt plaintext using AES-256-GCM.
    
    Args:
        plaintext: Text to encrypt
        key: 32-byte encryption key
    
    Returns:
        Tuple of (nonce, ciphertext, tag) - all as bytes
    """
    nonce = generate_nonce()
    aesgcm = AESGCM(key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    
    # AES-GCM appends 16-byte tag to ciphertext
    ciphertext = ciphertext_with_tag[:-16]
    tag = ciphertext_with_tag[-16:]
    
    return nonce, ciphertext, tag


def decrypt(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes) -> str:
    """Decrypt ciphertext using AES-256-GCM.
    
    Args:
        nonce: Nonce used during encryption
        ciphertext: Encrypted data
        tag: Authentication tag
        key: 32-byte encryption key
    
    Returns:
        Decrypted plaintext
    
    Raises:
        cryptography.exceptions.InvalidTag: If decryption fails (wrong password or corrupted data)
    """
    aesgcm = AESGCM(key)
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext + tag, None)
    return plaintext_bytes.decode('utf-8')


def hash_password(password: str) -> str:
    """Create a verification hash of the master password.
    
    This is stored to verify password on unlock, without storing the password itself.
    Uses SHA-256 (not for key derivation, just verification).
    
    Returns:
        Base64-encoded hash
    """
    return base64.b64encode(
        hashlib.sha256(password.encode('utf-8')).digest()
    ).decode('ascii')


def encode_b64(data: bytes) -> str:
    """Encode bytes to base64 string."""
    return base64.b64encode(data).decode('ascii')


def decode_b64(data: str) -> bytes:
    """Decode base64 string to bytes."""
    return base64.b64decode(data)
