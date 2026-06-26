#!/usr/bin/env python3
# generate-image.py — AutoGLM 文生图
# 用法: python generate-image.py "图片描述文字"

import sys
import json
import hashlib
import time
import urllib.request

# ── 配置 ──────────────────────────────────────────
APP_ID  = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
URL     = "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image"
TOKEN_URL = "http://127.0.0.1:53699/get_token"

# ── Step 1: 获取 token ────────────────────────────
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

# ── Step 2: 读取图片描述 ──────────────────────────
if len(sys.argv) < 2:
    print('用法: python generate-image.py "图片描述文字"')
    sys.exit(1)

text = sys.argv[1]

# ── Step 3: 生成签名 Headers ──────────────────────
timestamp = str(int(time.time()))
sign_data = f"{APP_ID}&{timestamp}&{APP_KEY}"
sign      = hashlib.md5(sign_data.encode("utf-8")).hexdigest()

# ── Step 4: 发起请求 ──────────────────────────────
payload = json.dumps({"text": text}).encode("utf-8")
headers = {
    "Authorization":    token,
    "Content-Type":     "application/json",
    "X-Auth-Appid":     APP_ID,
    "X-Auth-TimeStamp": timestamp,
    "X-Auth-Sign":      sign,
}

req = urllib.request.Request(URL, data=payload, headers=headers, method="POST")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
