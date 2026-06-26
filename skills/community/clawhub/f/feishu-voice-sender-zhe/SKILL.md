---
name: feishu-voice-sender
description: 飞书语音/音频发送器 — 通过飞书 OpenAPI 发送音频文件，支持语音消息直接播放。| Feishu Voice/Audio Sender — Send audio files via Feishu OpenAPI for inline voice message playback.
license: MIT
compatibility: openclaw
metadata:
  version: "1.0.0"
  tags: [feishu, voice, audio, speech, send, im, messaging, openapi]
  author: ZheYanyan
  openclaw:
    emoji: "🎤"
    requires:
      bins: [curl, python3]
---

# Feishu Voice Sender | 飞书语音发送器

发送音频文件到飞书聊天中，以语音消息形式展示（可直接点击播放）。

Send audio files to Feishu chat as voice messages (click to play inline).

## 核心发现 | Key Discovery

飞书语音消息需要：
1. 上传时使用 `file_type=opus`
2. 发送时使用 `msg_type=audio`

其他文件类型（mp3/stream）会以文件形式发送，需要下载才能播放。

Feishu voice messages require:
1. Upload with `file_type=opus`
2. Send with `msg_type=audio`

Other file types (mp3/stream) are sent as files requiring download.

## 快速开始 | Quick Start

```bash
# 发送语音消息（自动识别 .mp3/.m4a/.wav 等格式）
python3 scripts/feishu_voice_sender.py --file /path/to/audio.mp3

# 指定接收者
python3 scripts/feishu_voice_sender.py --file /path/to/audio.mp3 --receive-id ou_xxx
```

## 脚本 | Script

```python
#!/usr/bin/env python3
"""
Feishu Voice Sender - 发送语音/音频到飞书作为语音消息
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

def get_tenant_token(app_id: str, app_secret: str) -> str:
    """获取 tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                return result["tenant_access_token"]
            raise Exception(f"获取token失败: {result.get('msg')}")
    except urllib.error.URLError as e:
        raise Exception(f"网络错误: {e}")

def upload_file(token: str, file_path: str) -> str:
    """上传文件，返回 file_key"""
    filename = os.path.basename(file_path)
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    
    boundary = "----FeishuBoundary"
    with open(file_path, "rb") as f:
        content = f.read()
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file_name"\r\n\r\n'
        f"{filename}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file_type"\r\n\r\n'
        f"opus\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: audio/mpeg\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                return result["data"]["file_key"]
            raise Exception(f"上传失败: {result.get('msg')}")
    except urllib.error.URLError as e:
        raise Exception(f"上传失败: {e}")

def send_audio_message(token: str, receive_id: str, file_key: str) -> str:
    """发送音频消息"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": receive_id,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key})
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                return result["data"]["message_id"]
            raise Exception(f"发送失败: {result.get('msg')}")
    except urllib.error.URLError as e:
        raise Exception(f"发送失败: {e}")

def read_openclaw_config() -> dict:
    """读取 OpenClaw 飞书配置"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(config_path):
        raise Exception(f"配置文件不存在: {config_path}")
    
    with open(config_path) as f:
        config = json.load(f)
    
    feishu = config.get("channels", {}).get("feishu", {})
    if not feishu:
        raise Exception("未找到飞书配置")
    
    return {
        "app_id": feishu.get("appId"),
        "app_secret": feishu.get("appSecret")
    }

def get_receive_id_from_env() -> str:
    """从环境变量获取 receive_id"""
    return os.environ.get("OPENCLAW_CHAT_ID") or os.environ.get("FEISHU_CHAT_ID") or ""

def main():
    parser = argparse.ArgumentParser(description="发送语音消息到飞书")
    parser.add_argument("--file", "-f", required=True, help="音频文件路径")
    parser.add_argument("--receive-id", "-r", default=get_receive_id_from_env(), help="接收者 open_id")
    args = parser.parse_args()
    
    if not args.receive_id:
        print("错误: 请指定 --receive-id 或设置 OPENCLAW_CHAT_ID 环境变量", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.file):
        print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    print(f"读取飞书配置...")
    feishu_config = read_openclaw_config()
    
    print(f"获取访问令牌...")
    token = get_tenant_token(feishu_config["app_id"], feishu_config["app_secret"])
    
    print(f"上传音频文件: {args.file}")
    file_key = upload_file(token, args.file)
    
    print(f"发送语音消息...")
    message_id = send_audio_message(token, args.receive_id, file_key)
    
    print(f"成功! message_id: {message_id}")

if __name__ == "__main__":
    main()
