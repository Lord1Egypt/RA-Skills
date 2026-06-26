#!/usr/bin/env python3
"""
企业 AI 助手机器人主程序
用途：接收飞书消息，调用 OpenClaw API 生成回复
"""

import os
import json
from flask import Flask, request
from lark import MessageManager, EventManager, CardManager
import requests

app = Flask(__name__)

# 配置
with open("config.json") as f:
    config = json.load(f)

OPENCLAW_API_KEY = os.getenv("OPENCLAW_API_KEY", config["openclaw"]["api_key"])
OPENCLAW_BASE_URL = config["openclaw"]["base_url"]
MODEL = config["openclaw"]["model"]

def call_openclaw(messages):
    """调用 OpenClaw API"""
    headers = {
        "Authorization": f"Bearer {OPENCLAW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    response = requests.post(
        f"{OPENCLAW_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ API 调用失败: {response.status_code}"

@app.route("/webhook", methods=["POST"])
def webhook():
    """处理飞书消息"""
    data = request.json
    
    # 验证请求
    if data.get("type") == "url_verification":
        return {"challenge": data["challenge"]}
    
    # 解析消息
    event = data.get("event", {})
    message = event.get("message", {})
    content = json.loads(message.get("content", "{}"))
    text = content.get("text", "")
    sender_id = event.get("sender", {}).get("sender_id", {}).get("open_id", "")
    
    # 调用 AI 生成回复
    messages = [
        {"role": "system", "content": "你是企业AI助手，用简洁专业的中文回答问题。"},
        {"role": "user", "content": text}
    ]
    
    reply = call_openclaw(messages)
    
    # TODO: 调用飞书 API 发送回复
    # 这里需要使用 lark SDK 发送消息
    
    return {"success": True, "reply": reply}

if __name__ == "__main__":
    print("🤖 企业 AI 助手机器人启动中...")
    print(f"📡 监听端口: 8080")
    print(f"🧠 使用模型: {MODEL}")
    app.run(host="0.0.0.0", port=8080)
