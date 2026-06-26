"""NewApi 采购认证：SHA512 签名与 AES 乘客加密（与 export CryptoServiceImpl 一致）。"""
from __future__ import annotations

import base64
import hashlib
import time
from typing import Any

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def sha512_sign(app_key: str, app_secret: str, timestamp: str) -> str:
    """sign = SHA512(appkey + appSecret + timestamp)，timestamp 为秒级字符串。"""
    raw = f"{app_key}{app_secret}{timestamp}"
    return hashlib.sha512(raw.encode("utf-8")).hexdigest()


def build_authentication(app_key: str, app_secret: str) -> dict[str, str]:
    ts = str(int(time.time()))
    return {
        "timestamp": ts,
        "sign": sha512_sign(app_key, app_secret, ts),
    }


def aes_encrypt(content: str, password: str) -> str:
    """
    AES/CBC/PKCS5Padding，IV 为 16 字节零；密钥须为 UTF-8 恰好 16 字节。
    与 CryptoServiceImpl.encrypt 一致。
    """
    key = password.encode("utf-8")
    if len(key) != 16:
        raise ValueError(
            f"NewApi AES 密钥长度必须为 16 字节，当前为 {len(key)}。"
            "请检查 FR_NEWAPI_AES_SECRET（PurchaseAppSecret AES）。"
        )
    cipher = AES.new(key, AES.MODE_CBC, iv=b"\x00" * 16)
    encrypted = cipher.encrypt(pad(content.encode("utf-8"), AES.block_size))
    return base64.b64encode(encrypted).decode("ascii")


def encrypt_passengers(passengers: list[dict[str, Any]], aes_secret: str) -> str:
    import json

    return aes_encrypt(json.dumps(passengers, ensure_ascii=False), aes_secret)
