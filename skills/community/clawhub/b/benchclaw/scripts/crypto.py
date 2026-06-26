"""
BenchClaw 加解密模块 (RSA + AES 混合)

请求：随机 AES-256 密钥 K → gpv；RSA 公钥加密 K → key。题目包响应为明文 JSON，无需解密 data。
目的：用于验证来自服务器的任务签名，确保题目未被篡改。
依赖：cryptography >= 42.0
"""
from __future__ import annotations

import base64
import json
import os
from typing import Any, Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from config import BENCHCLAW_RSA_PUBLIC_KEY_PEM as _cfg_pub

_IV_LEN = 12
_TAG_LEN = 16


def _public_pem() -> str:
    return (os.environ.get("BENCHCLAW_RSA_PUBLIC_KEY_PEM") or _cfg_pub or "").strip()


def _load_public_key():
    pem = _public_pem()
    if not pem:
        raise RuntimeError("BENCHCLAW_RSA_PUBLIC_KEY_PEM 未配置")
    return serialization.load_pem_public_key(pem.encode("utf-8"), backend=default_backend())


def rsa_encrypt_aes_key(aes_key: bytes) -> str:
    pub = _load_public_key()
    encrypted = pub.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(encrypted).decode("ascii")


def aes_gcm_encrypt_json(data: Any, aes_key: bytes) -> str:
    if len(aes_key) != 32:
        raise RuntimeError(f"期望 32 字节 AES 密钥，实际 {len(aes_key)}")
    iv = os.urandom(_IV_LEN)
    if isinstance(data, bytes):
        plaintext = data
    elif isinstance(data, str):
        plaintext = data.encode("utf-8")
    else:
        plaintext = json.dumps(data, ensure_ascii=False).encode("utf-8")
    ct_tag = AESGCM(aes_key).encrypt(iv, plaintext, None)
    return base64.b64encode(iv + ct_tag).decode("ascii")


def hybrid_encrypt_json(data: Any) -> Tuple[str, str, bytes]:
    """
    混合加密可 JSON 序列化的对象。

    Returns
    -------
    key_b64, gpv_b64, aes_key_bytes
        aes_key_bytes 用于解密服务端返回的 data。
    """
    aes_key = os.urandom(32)
    gpv = aes_gcm_encrypt_json(data, aes_key)
    key_b64 = rsa_encrypt_aes_key(aes_key)
    return key_b64, gpv, aes_key


def aes_gcm_decrypt(gpv: str, aes_key: bytes) -> bytes:
    blob = base64.b64decode(gpv)
    if len(blob) < _IV_LEN + _TAG_LEN:
        raise ValueError("密文太短")
    iv, ct_tag = blob[:_IV_LEN], blob[_IV_LEN:]
    return AESGCM(aes_key).decrypt(iv, ct_tag, None)


def client_decrypt(gpv: str, aes_key: bytes) -> Any:
    """使用会话 AES 密钥解密服务端返回的 data。"""
    plain = aes_gcm_decrypt(gpv, aes_key)
    text = plain.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


# 兼容旧脚本名：整包混合加密
def client_encrypt(data: Any) -> str:
    _, gpv, _ = hybrid_encrypt_json(data)
    return gpv


if __name__ == "__main__":
    import argparse as _ap

    parser = _ap.ArgumentParser(description="BenchClaw 加解密 (RSA+AES)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="混合加密往返自检（需服务端私钥才能完整测，此处仅测加密结构）")
    args = parser.parse_args()
    if args.cmd == "check":
        k, g, aes = hybrid_encrypt_json({"t": 1})
        assert len(aes) == 32
        print("hybrid encrypt ok, key len", len(k), "gpv len", len(g))
