#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中台 Skill：Inner-Auth 请求头 + Bearer JWT。业务路径见 procurement。"""

import base64
import hashlib
import hmac
import os
import time
from urllib.parse import urlparse

import requests

# 中台 skill 根路径
_API_BASE_PRODUCTION = "https://spmiddle.1tsoft.com/skill/skill"
API_BASE = os.environ.get("SKILL_API_BASE", _API_BASE_PRODUCTION)

SPMIDDLE_CLIENT_ID_DOUYIN = "ytdyzfbj"
SPMIDDLE_CLIENT_SECRET_DOUYIN = "yxb6aU3dXip1J3WgmtQezrPVP0FyIGrPYSqHwK5N3eU="
SPMIDDLE_CLIENT_ID_TAOBAO = "yttbzfbj"
SPMIDDLE_CLIENT_SECRET_TAOBAO = "Y9Ng8rau+XXJXeKB1QQXQZylYg4ThEQ78DjjBMKSyAc="


def yzg_skill_url(relative_path: str) -> str:
    """拼接 API_BASE + /yzgSkill 下的完整 URL。"""
    rel = relative_path.strip()
    if not rel.startswith("/"):
        rel = "/" + rel
    base = API_BASE.rstrip("/")
    if not base.endswith("/yzgSkill"):
        base = f"{base}/yzgSkill"
    return f"{base}{rel}"


def douyin_skill_url(relative_path: str) -> str:
    """拼接 API_BASE + /dySkill 下的完整 URL。"""
    rel = relative_path.strip()
    if not rel.startswith("/"):
        rel = "/" + rel
    base = API_BASE.rstrip("/")
    if not base.endswith("/dySkill"):
        base = f"{base}/dySkill"
    return f"{base}{rel}"


def resolve_jwt_token(*, token: str | None) -> str:
    """CLI 仅通过 --token 传入 ISV Token（由 Skill 注入）。"""
    jwt_token = (token or "").strip()
    if jwt_token:
        return jwt_token
    raise ValueError("缺少鉴权：请使用 --token 传入 ISV Token")


def _base64url_no_padding(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def _hmac_sha256_base64(secret: str, data: str) -> str:
    mac = hmac.new(secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode("utf-8")


def _resolve_platform_inner_auth(request_url: str) -> tuple[str, str]:
    """根据请求 URL 自动匹配平台并返回对应 inner-auth 凭证。"""
    path = (urlparse(request_url).path or "").lower()
    if "/dyskill" in path:
        return SPMIDDLE_CLIENT_ID_DOUYIN, SPMIDDLE_CLIENT_SECRET_DOUYIN
    return SPMIDDLE_CLIENT_ID_TAOBAO, SPMIDDLE_CLIENT_SECRET_TAOBAO


def build_request_headers(method: str, request_url: str, jwt_token: str) -> dict:
    """单次 HTTP：inner-auth（X-Client-Id 等）+ httpAuthorization Bearer。"""
    token = (jwt_token or "").strip()
    if not token:
        raise ValueError("jwt_token 不能为空")

    client_id, client_secret = _resolve_platform_inner_auth(request_url)
    if not client_id or not client_secret:
        raise ValueError("inner-auth 未配置完整，请检查平台对应的 _api.SPMIDDLE_CLIENT_ID_* / SPMIDDLE_CLIENT_SECRET_*")

    ts = str(int(time.time() * 1000))
    nonce = _base64url_no_padding(os.urandom(16))
    path = urlparse(request_url).path
    body_hash = ""
    sign_base = f"{method}\n{path}\n{ts}\n{nonce}\n{body_hash}"
    sign = _hmac_sha256_base64(client_secret, sign_base)

    headers = {"Content-Type": "application/json"}
    headers.update(
        {
            "X-Client-Id": client_id,
            "X-Timestamp": ts,
            "X-Nonce": nonce,
            "X-Sign": sign,
            "httpAuthorization": f"Bearer {token}",
        }
    )
    return headers


def request_json(
    method: str,
    url: str,
    *,
    token: str | None,
    params=None,
    json_body=None,
    timeout: int = 30,
) -> dict:
    jwt = resolve_jwt_token(token=token)
    headers = build_request_headers(method.upper(), url, jwt)
    headers["Accept"] = "application/json"
    resp = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        json=json_body,
        headers=headers,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()
