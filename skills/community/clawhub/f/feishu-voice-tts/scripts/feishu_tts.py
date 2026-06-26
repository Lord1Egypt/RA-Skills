#!/usr/bin/env python3
"""飞书语音 TTS 发送脚本：MOSS-TTS + ffmpeg 转码 + 飞书上传 + 发送语音消息"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

MOSS_API_KEY = os.getenv("MOSS_API_KEY")
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")

DEFAULT_VOICE_ID = "2001286865130360832"  # 周周
TTS_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "tts.py")
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/files"


def fail(msg: str, code: int = 1):
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _json(resp: requests.Response):
    try:
        return resp.json()
    except ValueError:
        fail(f"non-JSON response (HTTP {resp.status_code}): {resp.text[:300]}")


def get_tenant_access_token(timeout=30):
    try:
        resp = requests.post(TOKEN_URL, json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}, timeout=timeout)
    except requests.RequestException as e:
        fail(f"获取 token 请求失败: {e}")

    data = _json(resp)
    if resp.status_code >= 400 or data.get("code") != 0:
        fail(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def generate_tts(text, voice_id, output_path):
    cmd = [
        sys.executable,
        TTS_SCRIPT_PATH,
        "--text", text,
        "--voice_id", voice_id,
        "--output", output_path,
    ]
    env = os.environ.copy()
    env["MOSS_API_KEY"] = MOSS_API_KEY
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        fail(f"TTS 生成失败: {result.stderr or result.stdout}")
    print(f"✓ TTS 生成完成: {output_path}")


def convert_to_opus(input_wav, output_opus):
    if not shutil.which("ffmpeg"):
        fail("未找到 ffmpeg，请先安装")
    cmd = [
        "ffmpeg", "-y", "-i", input_wav,
        "-ac", "1", "-ar", "16000",
        "-c:a", "libopus", "-b:a", "24k", output_opus,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"音频转码失败: {result.stderr}")
    print(f"✓ 转码完成: {output_opus}")


def upload_to_feishu(token, file_path, timeout=60):
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        data = {"file_type": "opus", "file_name": os.path.basename(file_path)}
        files = {"file": (os.path.basename(file_path), f, "audio/ogg")}
        try:
            resp = requests.post(UPLOAD_URL, headers=headers, data=data, files=files, timeout=timeout)
        except requests.RequestException as e:
            fail(f"文件上传请求失败: {e}")

    payload = _json(resp)
    if resp.status_code >= 400 or payload.get("code") != 0:
        fail(f"文件上传失败: {payload}")

    file_key = payload.get("data", {}).get("file_key")
    if not file_key:
        fail(f"上传返回缺少 file_key: {payload}")
    print(f"✓ 文件上传成功: {file_key}")
    return file_key


def send_voice_message(token, receive_id, receive_id_type, file_key, timeout=30):
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "receive_id": receive_id,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key}),
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as e:
        fail(f"发送消息请求失败: {e}")

    data = _json(resp)
    if resp.status_code >= 400 or data.get("code") != 0:
        fail(f"发送消息失败: {data}")

    message_id = data.get("data", {}).get("message_id")
    if not message_id:
        fail(f"发送返回缺少 message_id: {data}")
    print(f"✓ 语音消息发送成功: {message_id}")
    return data["data"]


def main():
    parser = argparse.ArgumentParser(description="飞书语音 TTS 发送")
    parser.add_argument("--text", required=True, help="要转语音的文本")
    parser.add_argument("--chat_id", help="飞书群 ID")
    parser.add_argument("--receive_id", help="接收者 ID")
    parser.add_argument("--receive_id_type", default="chat_id", choices=["chat_id", "open_id"], help="接收者类型")
    parser.add_argument("--voice_id", default=DEFAULT_VOICE_ID, help="MOSS 音色 ID")
    parser.add_argument("--output", default="feishu_voice.wav", help="输出文件路径")
    args = parser.parse_args()

    if not args.text.strip():
        fail("--text 不能为空")

    if args.chat_id and args.receive_id:
        fail("--chat_id 与 --receive_id 只能二选一")

    if args.chat_id:
        receive_id = args.chat_id
        receive_id_type = "chat_id"
    elif args.receive_id:
        receive_id = args.receive_id
        receive_id_type = args.receive_id_type
    else:
        fail("必须指定 --chat_id 或 --receive_id")

    if not MOSS_API_KEY:
        fail("未设置 MOSS_API_KEY 环境变量")
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        fail("未设置 FEISHU_APP_ID 或 FEISHU_APP_SECRET 环境变量")
    if not Path(TTS_SCRIPT_PATH).exists():
        fail(f"未找到 tts 脚本: {TTS_SCRIPT_PATH}")

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "tts.wav")
        opus_path = os.path.join(tmpdir, "voice.opus")

        print(f"正在生成语音: {args.text[:50]}...")
        generate_tts(args.text, args.voice_id, wav_path)

        print("正在转码为 OPUS...")
        convert_to_opus(wav_path, opus_path)

        print("正在获取飞书 token...")
        token = get_tenant_access_token()

        print("正在上传到飞书...")
        file_key = upload_to_feishu(token, opus_path)

        print("正在发送语音消息...")
        send_voice_message(token, receive_id, receive_id_type, file_key)

    print("\n✅ 全部完成！")


if __name__ == "__main__":
    main()
