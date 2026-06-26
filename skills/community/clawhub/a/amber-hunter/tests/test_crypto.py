"""
tests/test_crypto.py — 加密/解密核心路径测试
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.crypto import derive_key, encrypt_content, decrypt_content, generate_salt


def test_encrypt_decrypt_roundtrip():
    """明文加解密应完全还原"""
    salt = generate_salt()
    key = derive_key("test-password-123", salt)
    plaintext = "Hello, Amber! 这是一条测试记忆。".encode("utf-8")
    ciphertext, nonce = encrypt_content(plaintext, key)
    decrypted = decrypt_content(ciphertext, key, nonce)
    assert decrypted == plaintext


def test_decrypt_wrong_key_returns_none():
    """错误密钥解密应返回 None"""
    salt = generate_salt()
    key1 = derive_key("correct-password", salt)
    key2 = derive_key("wrong-password", salt)
    plaintext = b"secret data"
    ciphertext, nonce = encrypt_content(plaintext, key1)
    result = decrypt_content(ciphertext, key2, nonce)
    assert result is None


def test_tampered_ciphertext_returns_none():
    """篡改密文应返回 None"""
    salt = generate_salt()
    key = derive_key("password", salt)
    plaintext = b"original content"
    ciphertext, nonce = encrypt_content(plaintext, key)
    # 篡改密文最后一个字节
    tampered = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    result = decrypt_content(tampered, key, nonce)
    assert result is None


def test_different_salts_produce_different_keys():
    """相同密码 + 不同 salt 应产生不同密钥"""
    salt1 = generate_salt()
    salt2 = generate_salt()
    key1 = derive_key("same-password", salt1)
    key2 = derive_key("same-password", salt2)
    assert key1 != key2
