#!/usr/bin/env python3
"""
飞书 Token 获取与缓存脚本

Usage:
    python3 get_token.py                  # 获取并缓存 token
    python3 get_token.py --check          # 检查缓存状态

Environment:
    env/ 目录下需要配置:
    - app.json: {"app_id": "...", "app_secret": "..."}
    - token_cache.json: (自动生成)
"""

import os
import json
import time
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests 库未安装，请运行: pip install requests", file=sys.stderr)
    sys.exit(1)

# 目录配置
ENV_DIR = Path(__file__).parent / "env"
APP_FILE = ENV_DIR / "app.json"
TOKEN_CACHE = ENV_DIR / "token_cache.json"

# API 端点
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"


def load_app_config():
    """加载应用配置"""
    if not APP_FILE.exists():
        print(f"Error: 配置文件不存在 {APP_FILE}", file=sys.stderr)
        print("请先创建 env/app.json 并填入 app_id 和 app_secret", file=sys.stderr)
        print("", file=sys.stderr)
        print("示例:", file=sys.stderr)
        print('  {"app_id": "cli_xxxxxxxxxxxxxxxx", "app_secret": "..."}', file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(APP_FILE.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: 配置文件格式错误 {APP_FILE}: {e}", file=sys.stderr)
        sys.exit(1)


def get_cached_token():
    """获取缓存的 token"""
    if TOKEN_CACHE.exists():
        try:
            data = json.loads(TOKEN_CACHE.read_text())
            expires_at = data.get("expires_at")
            token = data.get("tenant_access_token")

            if token and expires_at:
                # 提前5分钟刷新
                if time.time() < expires_at - 300:
                    return token
        except (json.JSONDecodeError, KeyError) as e:
            # 缓存文件损坏，忽略并重新获取
            pass
    return None


def request_new_token(app_id, app_secret):
    """请求新 token"""
    response = requests.post(
        TOKEN_URL,
        json={
            "app_id": app_id,
            "app_secret": app_secret
        },
        timeout=10
    )
    data = response.json()

    if data.get("code") != 0:
        print(f"Error: {data.get('msg')}", file=sys.stderr)
        sys.exit(1)

    return data["tenant_access_token"], data["expire"]


def save_token_cache(token, expire_seconds):
    """保存 token 缓存"""
    ENV_DIR.mkdir(parents=True, exist_ok=True)
    cache_data = {
        "tenant_access_token": token,
        "expires_at": time.time() + expire_seconds
    }
    TOKEN_CACHE.write_text(json.dumps(cache_data, indent=2))


def main():
    check_only = "--check" in sys.argv

    # 1. 尝试获取缓存的 token
    if not check_only:
        cached = get_cached_token()
        if cached:
            print(cached)
            return

    # 2. 请求新 token
    config = load_app_config()
    token, expire = request_new_token(config["app_id"], config["app_secret"])

    # 3. 保存缓存
    save_token_cache(token, expire)

    if check_only:
        print(f"Token: {token[:20]}...")
        print(f"Expires: {expire} seconds")
    else:
        print(token)


if __name__ == "__main__":
    main()