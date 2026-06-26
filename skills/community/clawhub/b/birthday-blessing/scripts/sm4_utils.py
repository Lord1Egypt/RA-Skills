"""
SM4 加密解密工具类（使用 cryptography 库）
参考 Java Hutool SM4 加密实现
"""

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def sm4_encrypt(plaintext: str, key: bytes) -> str:
    """
    SM4 加密（ECB 模式，PKCS7 填充）
    参考 Java Hutool: SM4.encryptBase64(plainText)
    """
    if not plaintext:
        raise ValueError("明文不能为空")
    
    if len(key) != 16:
        raise ValueError("密钥必须为 16 字节")
    
    # PKCS7 填充
    padding_len = 16 - (len(plaintext.encode('utf-8')) % 16)
    padded = plaintext.encode('utf-8') + bytes([padding_len] * padding_len)
    
    # SM4 ECB 模式加密
    cipher = Cipher(algorithms.SM4(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    
    # 返回 Base64 编码
    return base64.b64encode(ciphertext).decode('utf-8')


def sm4_decrypt(encrypted_text: str, key: bytes) -> str:
    """
    SM4 解密（ECB 模式，PKCS7 填充）
    """
    if not encrypted_text:
        raise ValueError("密文不能为空")
    
    if len(key) != 16:
        raise ValueError("密钥必须为 16 字节")
    
    # Base64 解码
    ciphertext = base64.b64decode(encrypted_text.encode('utf-8'))
    
    # SM4 ECB 模式解密
    cipher = Cipher(algorithms.SM4(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # 去除 PKCS7 填充
    padding_len = plaintext[-1]
    plaintext = plaintext[:-padding_len]
    
    return plaintext.decode('utf-8')


def is_valid_key(key_bytes: bytes) -> bool:
    """验证密钥是否有效（SM4 密钥必须为 16 字节）"""
    return len(key_bytes) == 16
