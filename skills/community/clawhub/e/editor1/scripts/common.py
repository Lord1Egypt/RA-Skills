"""
公共模块：Knot Agent Editor 共用的认证和工具函数
"""
import os
import json
import base64
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://knot.woa.com/apigw"


def get_env():
    """获取必要的环境变量"""
    jwt_token = os.environ.get("KNOT_JWT_TOKEN", "")
    username = os.environ.get("KNOT_USERNAME", "")
    if not jwt_token:
        print("错误：环境变量 KNOT_JWT_TOKEN 未设置", file=sys.stderr)
        sys.exit(1)
    if not username:
        print("错误：环境变量 KNOT_USERNAME 未设置", file=sys.stderr)
        sys.exit(1)
    return jwt_token, username


def get_api_token(jwt_token: str, username: str) -> str:
    """通过 JWT token 获取 Knot API Token"""
    resp = requests.post(
        f"{BASE_URL}/api/v1/mcpport/get_config",
        headers={"X-Username": username, "Content-Type": "application/json"},
        json={"jwt_token": jwt_token, "for_knot_api_token": True},
        verify=False,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        print(f"错误：获取 API Token 失败：{data.get('msg')}", file=sys.stderr)
        sys.exit(1)
    return data["data"]["knot_api_token"]


def get_auth_headers(jwt_token: str, username: str) -> dict:
    """获取带认证信息的请求头"""
    token = get_api_token(jwt_token, username)
    return {
        "x-knot-api-token": token,
        "Content-Type": "application/json",
    }


def parse_current_agent_id(jwt_token: str) -> str:
    """从 JWT payload 中解析当前对话的 agent_id（scene 字段）"""
    parts = jwt_token.split(".")
    if len(parts) < 2:
        print("错误：JWT token 格式无效", file=sys.stderr)
        sys.exit(1)
    # 补全 base64 padding
    padding = 4 - len(parts[1]) % 4
    padded = parts[1] + ("=" * (padding % 4))
    try:
        payload = json.loads(base64.urlsafe_b64decode(padded))
    except Exception as e:
        print(f"错误：解析 JWT payload 失败：{e}", file=sys.stderr)
        sys.exit(1)
    scene = payload.get("scene")
    if not scene:
        print("错误：JWT payload 中未找到 scene 字段", file=sys.stderr)
        sys.exit(1)
    return scene


def api_post(url: str, headers: dict, payload: dict) -> dict:
    """通用 POST 请求，返回响应 JSON"""
    resp = requests.post(url, headers=headers, json=payload, verify=False, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        print(f"错误：API 请求失败（{url}）：{data.get('msg')}", file=sys.stderr)
        sys.exit(1)
    return data
