#!/usr/bin/env python3
"""
1688 Skills 网关签名鉴权模块

职责：
  1. 从环境变量 / OpenClaw 配置文件读取 ALI_1688_AK
  2. base64 解码 AK，前 32 位为 access_key_secret，32 位之后为 access_key_id
  3. 按 1688 Skills 网关签名规范生成请求头（HMAC-SHA256 + base64）

与 1688-key-product-selection / 1688-shop-operate 的 _auth.py 实现完全对齐，
避免发布后多个 skill 的 AK 鉴权逻辑漂移。
"""

import base64
import hashlib
import hmac
import json
import os
import time
import uuid
from typing import Dict, Optional, Tuple
from urllib.parse import parse_qs, quote, urlparse

from _const import OPENCLAW_CONFIG_PATH, SKILL_VERSION

# ── AK 解析 ──────────────────────────────────────────────────────────────────

def extract_ak_keys(raw_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    从 ALI_1688_AK 原始值中提取 (access_key_id, access_key_secret)

    AK 规则：
      - 优先尝试 base64 url-safe 解码
      - 解码后前 32 位为 access_key_secret，32 位之后为 access_key_id
    """
    try:
        decoded = base64.urlsafe_b64decode(raw_input).decode("utf-8")
        if decoded:
            raw_input = decoded
    except Exception:
        # 当前 AK 规范并不保证一定是 base64，可回退到原值按长度切分
        pass

    if not raw_input or len(raw_input) < 32:
        return None, None

    access_key_secret = raw_input[:32]
    access_key_id = raw_input[32:]
    return access_key_id, access_key_secret

def _get_ak_raw_from_config() -> Optional[str]:
    """从 OpenClaw 配置文件读取 AK（Gateway 未重启时的 fallback）"""
    if not OPENCLAW_CONFIG_PATH.exists():
        return None
    try:
        with open(OPENCLAW_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        entries = config.get("skills", {}).get("entries", {})
        for skill_name in (
            "1688-product-analysis",
            "1688-key-product-selection",
            "1688-shop-health-check",
            "1688-shop-operate",
            "1688-open-skill-template",
        ):
            skill = entries.get(skill_name)
            if not skill:
                continue
            ak = skill.get("apiKey") or skill.get("env", {}).get("ALI_1688_AK", "")
            if ak:
                return ak
        return None
    except Exception:
        return None

def get_ak_from_env() -> Tuple[Optional[str], Optional[str]]:
    """读取 AK：优先环境变量（OpenClaw 注入），其次配置文件 fallback"""
    raw_input = os.environ.get("ALI_1688_AK") or _get_ak_raw_from_config()
    if not raw_input:
        return None, None
    return extract_ak_keys(raw_input)

# ── 签名生成 ──────────────────────────────────────────────────────────────────

def get_content_md5(body: str) -> str:
    """计算 body 的 MD5 并 base64 编码"""
    if not body:
        return ""
    md5_obj = hashlib.md5(body.encode("utf-8"))
    return base64.b64encode(md5_obj.digest()).decode("utf-8")

def get_canonicalized_resource(uri: str) -> str:
    """规范化资源路径：路径 + 排序后的 query 参数"""
    parsed_uri = urlparse(uri)
    path = parsed_uri.path
    query = parsed_uri.query

    if not query:
        return path

    params = parse_qs(query)
    sorted_keys = sorted(params.keys())
    canonical_query = []
    for key in sorted_keys:
        values = sorted(params[key])
        for value in values:
            encoded_key = quote(key, safe="")
            encoded_val = quote(value, safe="")
            canonical_query.append(f"{encoded_key}={encoded_val}")

    return f"{path}?{'&'.join(canonical_query)}"

def build_signature(
    method: str,
    uri: str,
    body: str,
    content_type: str,
    ak_id: str,
    ak_secret: str,
) -> Dict[str, str]:
    """构建带签名的完整请求头"""
    timestamp = str(int(time.time()))
    nonce = uuid.uuid4().hex[:8]
    content_md5 = get_content_md5(body)

    csk_headers = {
        "x-csk-ak": ak_id,
        "x-csk-time": timestamp,
        "x-csk-nonce": nonce,
        "x-csk-content-md5": content_md5,
        "x-csk-version": SKILL_VERSION,
    }

    sorted_csk_keys = sorted(csk_headers.keys())
    canonicalized_headers = ""
    for key in sorted_csk_keys:
        canonicalized_headers += f"{key.lower()}:{csk_headers[key].strip()}\n"

    string_to_sign = (
        method.upper() + "\n" +
        content_md5 + "\n" +
        content_type + "\n" +
        timestamp + "\n" +
        canonicalized_headers +
        get_canonicalized_resource(uri)
    )

    signature = hmac.new(
        ak_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    sign_base64 = base64.b64encode(signature).decode("utf-8")

    return {
        "Content-Type": content_type,
        "x-csk-sign": sign_base64,
        **csk_headers,
    }

def get_auth_headers(method: str, uri: str, body: str = "") -> Optional[Dict[str, str]]:
    """
    获取已签名的请求头。

    Returns:
        签名后的完整 headers；若 AK 未配置则返回 None。
    """
    ak_id, ak_secret = get_ak_from_env()
    if not ak_id or not ak_secret:
        return None

    return build_signature(
        method=method,
        uri=uri,
        body=body,
        content_type="application/json",
        ak_id=ak_id,
        ak_secret=ak_secret,
    )
