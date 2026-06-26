#!/usr/bin/env python3
# open-link.py — AutoGLM Open Link（获取页面详细内容）
# 用法: python open-link.py "https://example.com"

import sys
import time
import hashlib
import json
import urllib.request
import urllib.error

APP_ID = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
URL = "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link"
TOKEN_URL = "http://127.0.0.1:53699/get_token"


def generate_sign(app_id: str, timestamp: int, app_key: str) -> str:
    raw = f"{app_id}&{timestamp}&{app_key}"
    return hashlib.md5(raw.encode()).hexdigest()


def get_token() -> str:
    try:
        with urllib.request.urlopen(TOKEN_URL) as resp:
            token = resp.read().decode("utf-8").strip()
    except Exception as e:
        print(f"ERROR: 无法从本地服务获取 token: {e}")
        sys.exit(1)

    if not token:
        print("ERROR: 获取到的 token 为空。")
        sys.exit(1)

    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"

    return token


def open_link(link: str) -> dict:
    token = get_token()

    timestamp = int(time.time())
    sign = generate_sign(APP_ID, timestamp, APP_KEY)

    payload = json.dumps({"url": link}).encode("utf-8")
    req = urllib.request.Request(URL, data=payload, method="POST")
    req.add_header("Authorization", token)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Auth-Appid", APP_ID)
    req.add_header("X-Auth-TimeStamp", str(timestamp))
    req.add_header("X-Auth-Sign", sign)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print('用法: python open-link.py "https://example.com"')
        sys.exit(1)

    link = sys.argv[1].strip()
    response = open_link(link)
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
