#!/usr/bin/env python3
"""
eoffice-skill Token 获取脚本

用途：获取 e-office10 OpenAPI 的访问令牌
认证方式：使用 agent_id + secret + user 自动换取 token

使用方法：
    python get-token.py

环境变量（必需）：
    EOFFICE_BASE_URL - OA 系统地址，如 https://oa.example.com/server
    EOFFICE_AGENT_ID - 应用 Agent ID
    EOFFICE_SECRET   - 应用密钥
    EOFFICE_USER     - 用户标识（工号/账号/手机号）

输出：
    成功：打印 token 到 stdout
    失败：打印错误信息到 stderr，退出码 1
"""

import os
import sys
import json
import requests

# 默认超时时间（秒）
TIMEOUT = 30


def get_env(name: str, required: bool = True) -> str:
    """获取环境变量"""
    value = os.getenv(name, "").strip()
    if required and not value:
        print(f"ERROR: Environment variable '{name}' is not set or empty", file=sys.stderr)
        print(f"Please set {name} before running this script", file=sys.stderr)
        sys.exit(1)
    return value


def get_token() -> str:
    """获取访问令牌"""
    base_url = get_env("EOFFICE_BASE_URL")
    agent_id = get_env("EOFFICE_AGENT_ID")
    secret = get_env("EOFFICE_SECRET")
    user = get_env("EOFFICE_USER")

    # 构建 token 获取 URL
    token_url = f"{base_url.rstrip('/')}/api/auth/openapi-token"

    # 构建请求 payload
    payload = {
        "user": user,
        "agent_id": agent_id,
        "secret": secret
    }

    try:
        response = requests.post(
            token_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"ERROR: Request timeout ({TIMEOUT}s) when connecting to {token_url}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Failed to connect to {token_url}", file=sys.stderr)
        print(f"Reason: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error {e.response.status_code} when requesting token", file=sys.stderr)
        try:
            error_data = e.response.json()
            print(f"Response: {json.dumps(error_data, ensure_ascii=False, indent=2)}", file=sys.stderr)
        except:
            print(f"Response text: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = response.json()
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON response from server", file=sys.stderr)
        print(f"Response text: {response.text[:500]}", file=sys.stderr)
        sys.exit(1)

    # 检查响应状态
    if result.get("status") != 1:
        errors = result.get("errors", [])
        error_msg = "; ".join([f"{e.get('code', 'UNKNOWN')}: {e.get('message', 'Unknown error')}" for e in errors])
        print(f"ERROR: Failed to get token - {error_msg}", file=sys.stderr)
        sys.exit(1)

    # 提取 token
    data = result.get("data", {})
    token = data.get("token")

    if not token:
        print(f"ERROR: Token not found in response", file=sys.stderr)
        print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}", file=sys.stderr)
        sys.exit(1)

    return token


def refresh_token(current_token: str, refresh_token: str) -> str:
    """刷新访问令牌"""
    base_url = get_env("EOFFICE_BASE_URL")

    refresh_url = f"{base_url.rstrip('/')}/api/auth/openapi-refresh-token"

    payload = {
        "token": current_token,
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(
            refresh_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(f"WARNING: Failed to refresh token: {e}", file=sys.stderr)
        print(f"Falling back to getting new token...", file=sys.stderr)
        return get_token()

    if result.get("status") == 1:
        return result.get("data", {}).get("token", "")

    # 刷新失败，尝试重新获取
    return get_token()


def main():
    """主函数"""
    # 检查是否有现成的 token 和 refresh_token 可以刷新
    current_token = os.getenv("EOFFICE_TOKEN", "")
    refresh_token_val = os.getenv("EOFFICE_REFRESH_TOKEN", "")

    if current_token and refresh_token_val:
        # 尝试刷新
        token = refresh_token(current_token, refresh_token_val)
    else:
        # 直接获取新 token
        token = get_token()

    # 输出 token
    print(token)


if __name__ == "__main__":
    main()
