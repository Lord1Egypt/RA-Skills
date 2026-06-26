#!/usr/bin/env python3
"""
Teambition API 底层工具模块
供其他脚本直接 import 使用，禁止作为 CLI 脚本调用。
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests

API_BASE = "https://open.teambition.com/api"

# ---------- Token ----------

def load_token() -> str:
    """读取 User Token。优先环境变量 TEAMBITION_USER_TOKEN，兼容旧版 TB_USER_TOKEN，fallback user-token.json。"""
    token = os.environ.get("TEAMBITION_USER_TOKEN")
    if token:
        return token
    
    # 兼容旧版环境变量名
    token = os.environ.get("TB_USER_TOKEN")
    if token:
        return token

    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.getcwd(), "user-token.json"),
        os.path.join(script_dir, "user-token.json"),
        os.path.join(script_dir, "..", "user-token.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    t = data.get("userToken")
                    if t:
                        return t
            except Exception:
                pass

    print("❌ 无法获取 User Token。请设置环境变量 TEAMBITION_USER_TOKEN（或兼容旧版 TB_USER_TOKEN）或创建 user-token.json。", file=sys.stderr)
    sys.exit(1)


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {load_token()}",
        "Content-Type": "application/json",
    }


# ---------- HTTP 方法 ----------

def get(path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """发起 GET 请求，返回响应 dict。失败时打印错误并 exit(1)。"""
    url = f"{API_BASE}/{path.lstrip('/')}"
    h = _headers()
    if headers:
        h.update(headers)
    resp = requests.get(url, headers=h, params=params, timeout=30)
    return _handle(resp)

def post(path: str, body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """发起 POST 请求，返回响应 dict。支持传入自定义 headers。"""
    url = f"{API_BASE}/{path.lstrip('/')}"
    h = _headers()
    if headers:
        h.update(headers)
    resp = requests.post(url, headers=h, json=body or {}, timeout=30)
    return _handle(resp)

def put(path: str, body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """发起 PUT 请求，返回响应 dict。支持传入自定义 headers。"""
    url = f"{API_BASE}/{path.lstrip('/')}"
    h = _headers()
    if headers:
        h.update(headers)
    resp = requests.put(url, headers=h, json=body or {}, timeout=30)
    return _handle(resp)


def _handle(resp: requests.Response) -> Dict[str, Any]:
    try:
        data = resp.json()
    except Exception:
        print(f"❌ 响应解析失败 (HTTP {resp.status_code}): {resp.text[:200]}", file=sys.stderr)
        sys.exit(1)

    # 2xx 状态码都是成功；code 200/201/204 都是正常的成功响应
    if not resp.ok or data.get("code", resp.status_code) not in (200, 201, 204):
        request_id = resp.headers.get("X-Request-Id") or resp.headers.get("x-request-id") or "未知"
        print(f"❌ API 错误 (HTTP {resp.status_code})", file=sys.stderr)
        print(f"   API: {resp.request.method} {resp.url}", file=sys.stderr)
        print(f"   RequestId: {request_id}", file=sys.stderr)
        print(f"   响应: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    return data


# ---------- 成员搜索 ----------

def search_member(name: str) -> str:
    """
    按姓名搜索成员，返回唯一匹配的 userId。
    - 唯一结果：直接返回 userId
    - 无结果：打印错误并 exit(1)
    - 多结果：打印候选列表并 exit(1)，提示用户使用更精确的关键词
    """
    data = post(f"v3/member/query?q={name}")
    members: List[Dict[str, Any]] = data.get("result", [])

    if not members:
        print(f"❌ 未找到姓名包含「{name}」的成员。", file=sys.stderr)
        sys.exit(1)

    if len(members) == 1:
        return members[0]["userId"]

    # 多个结果
    print(f"❌ 姓名「{name}」匹配到 {len(members)} 个成员，请使用更精确的关键词重试：", file=sys.stderr)
    for m in members:
        print(f"   - {m.get('name', '?')} (userId: {m.get('userId', '?')}, email: {m.get('email', '?')})", file=sys.stderr)
    sys.exit(1)