#!/usr/bin/env python3
"""
飞书语音消息发送脚本
用法: python3 send_voice.py <文本> <open_id> [--voice <音色>] [--config <openclaw.json路径>]
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse

DEFAULT_VOICE = "zh-CN-YunxiNeural"
FEISHU_API = "https://open.feishu.cn/open-apis"

def get_token(app_id, app_secret):
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["tenant_access_token"]

def upload_file(token, opus_path):
    # 用 curl 上传（multipart 在纯 Python 略繁琐）
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        f"{FEISHU_API}/im/v1/files",
        "-H", f"Authorization: Bearer {token}",
        "-F", "file_type=opus",
        "-F", "file_name=voice.opus",
        "-F", f"file=@{opus_path}"
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data["data"]["file_key"]

def send_audio(token, open_id, file_key):
    content = json.dumps({"file_key": file_key})
    body = json.dumps({
        "receive_id": open_id,
        "msg_type": "audio",
        "content": content
    }).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/im/v1/messages?receive_id_type=open_id",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

async def tts_to_mp3(text, voice, mp3_path):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(mp3_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="要转换的文本")
    parser.add_argument("open_id", help="飞书用户 open_id")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS 音色")
    parser.add_argument("--config", default=os.path.expanduser("~/.openclaw/openclaw.json"))
    args = parser.parse_args()

    # 读取配置
    with open(args.config) as f:
        cfg = json.load(f)
    feishu = cfg["channels"]["feishu"]
    app_id = feishu["appId"]
    app_secret = feishu["appSecret"]

    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = os.path.join(tmpdir, "voice.mp3")
        opus_path = os.path.join(tmpdir, "voice.opus")

        # 生成语音
        print(f"生成语音（{args.voice}）...")
        asyncio.run(tts_to_mp3(args.text, args.voice, mp3_path))

        # 转换格式
        subprocess.run(
            ["ffmpeg", "-i", mp3_path, "-c:a", "libopus", opus_path, "-y"],
            capture_output=True, check=True
        )

        # 获取 token
        token = get_token(app_id, app_secret)

        # 上传文件
        print("上传音频...")
        file_key = upload_file(token, opus_path)

        # 发送消息
        result = send_audio(token, args.open_id, file_key)
        if result.get("code") == 0:
            print(f"✅ 语音发送成功！message_id: {result['data']['message_id']}")
        else:
            print(f"❌ 发送失败: {result}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
