#!/usr/bin/env python3
"""
1688 API 认证模块（AK 提取 + HMAC-SHA256 签名）
"""

import hashlib
import hmac
import base64
import time
import uuid
import json
import os
from typing import Optional, Dict, Tuple
from urllib.parse import urlparse, parse_qs, quote
from _const import SKILL_VERSION, OPENCLAW_CONFIG_PATH

SKILL_NAME = "1688-freedom-query-merchant-data"


def extract_ak_keys(raw_input: str) -> Tuple[Optional[str], Optional[str]]:
    """从原始输入中提取 AccessKeyID 和 AccessKeySecret"""
    try:
        decoded = base64.urlsafe_b64decode(raw_input).decode("utf-8")
        if decoded:
            raw_input = decoded
    except Exception:
        pass

    if not raw_input or len(raw_input) < 32:
        return None, None

    access_key_secret = raw_input[:32]
    access_key_id = raw_input[32:]

    return access_key_id, access_key_secret


def _get_ak_raw_from_config() -> Optional[str]:
    """从 OPENCLAW_CONFIG_PATH 读取 AK"""
    if not OPENCLAW_CONFIG_PATH.exists():
        return None
    try:
        with open(OPENCLAW_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        entries = config.get("skills", {}).get("entries", {})
        skill = entries.get(SKILL_NAME, {})
        ak = skill.get("apiKey") or skill.get("env", {}).get("ALI_1688_AK", "")
        return ak if ak else None
    except Exception:
        return None


def get_ak_from_env() -> Tuple[Optional[str], Optional[str]]:
    """读取 AK：优先环境变量，其次配置文件"""
    raw_input = os.environ.get("ALI_1688_AK") or _get_ak_raw_from_config()
    if not raw_input:
        return None, None
    return extract_ak_keys(raw_input)


def get_content_md5(body: str) -> str:
    """计算 body 的 MD5 并 Base64 编码"""
    if not body:
        return ""
    md5_obj = hashlib.md5(body.encode('utf-8'))
    return base64.b64encode(md5_obj.digest()).decode('utf-8')


def get_canonicalized_resource(uri: str) -> str:
    """规范化资源路径"""
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
            encoded_key = quote(key, safe='')
            encoded_val = quote(value, safe='')
            canonical_query.append(f"{encoded_key}={encoded_val}")

    return f"{path}?{'&'.join(canonical_query)}"


def build_signature(
    method: str,
    uri: str,
    body: str,
    content_type: str,
    ak_id: str,
    ak_secret: str
) -> Dict[str, str]:
    """构建带签名的请求头"""
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
        ak_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    sign_base64 = base64.b64encode(signature).decode('utf-8')

    headers = {
        "Content-Type": content_type,
        "x-csk-sign": sign_base64,
        **csk_headers,
    }

    return headers


def get_auth_headers(method: str, uri: str, body: str = "") -> Optional[Dict[str, str]]:
    """获取认证头"""
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
