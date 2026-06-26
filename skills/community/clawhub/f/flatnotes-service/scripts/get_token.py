#!/usr/bin/env python3
"""
获取 Flatnotes 认证令牌
用法: python3 get_token.py [--username USER] [--password PASS] [--base-url URL]
环境变量: FLATNOTES_BASE_URL, FLATNOTES_USERNAME, FLATNOTES_PASSWORD
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def get_base_url() -> str:
    base_url = os.getenv("FLATNOTES_BASE_URL")
    if not base_url:
        print("❌ 错误: FLATNOTES_BASE_URL 环境变量未设置")
        print()
        print("📌 请先配置以下环境变量：")
        print("   export FLATNOTES_BASE_URL=\"https://your-flatnotes-host\"")
        print("   export FLATNOTES_USERNAME=\"your-username\"")
        print("   export FLATNOTES_PASSWORD=\"your-password\"")
        print()
        print("   添加到 ~/.bashrc 后执行: source ~/.bashrc")
        sys.exit(1)
    return base_url


def get_token(username: str = None, password: str = None, base_url: str = None) -> str:
    """使用用户名密码获取访问令牌"""
    if base_url is None:
        base_url = get_base_url()
    if username is None:
        username = os.getenv("FLATNOTES_USERNAME")
    if password is None:
        password = os.getenv("FLATNOTES_PASSWORD")
    
    if not username or not password:
        print("❌ 错误: FLATNOTES_USERNAME 或 FLATNOTES_PASSWORD 环境变量未设置")
        print()
        print("📌 请先配置以下环境变量：")
        print("   export FLATNOTES_BASE_URL=\"https://your-flatnotes-host\"")
        print("   export FLATNOTES_USERNAME=\"your-username\"")
        print("   export FLATNOTES_PASSWORD=\"your-password\"")
        print()
        print("   添加到 ~/.bashrc 后执行: source ~/.bashrc")
        print("   或通过 --username 和 --password 参数传入")
        sys.exit(1)
    
    url = f"{base_url}/api/token"
    data = json.dumps({"username": username, "password": password}).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Content-Length": len(data)
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            token = result.get("access_token") or result.get("token")
            if token:
                print(f"✅ 获取令牌成功")
                return token
            else:
                print(f"❌ 响应中没有找到令牌: {result}")
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ 登录失败: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取 Flatnotes 认证令牌")
    parser.add_argument("--username", help="用户名（默认从 FLATNOTES_USERNAME 读取）")
    parser.add_argument("--password", help="密码（默认从 FLATNOTES_PASSWORD 读取）")
    parser.add_argument("--base-url", help="服务地址（默认从 FLATNOTES_BASE_URL 读取）")
    
    args = parser.parse_args()
    token = get_token(args.username, args.password, args.base_url)
    # 不打印 token，避免泄露到 stdout/logs
