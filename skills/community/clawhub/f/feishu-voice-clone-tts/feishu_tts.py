#!/usr/bin/env python3
"""
Feishu TTS - 飞书语音消息发送技能（火山引擎音色版）
支持单聊和群聊
"""
import os
import sys
import json
import requests
import subprocess
import tempfile
import uuid
import base64

# 飞书配置 - 从环境变量读取
FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID')
FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET')
FEISHU_CHAT_ID = os.environ.get('FEISHU_CHAT_ID')

# 火山引擎配置
VOLC_API_KEY = os.environ.get('VOLC_API_KEY')
VOLC_TTS_URL = os.environ.get('VOLC_TTS_URL', 'https://openspeech.bytedance.com/api/v1/tts')
VOICE_TYPE = os.environ.get('VOLC_VOICE_TYPE')


def get_volc_api_key():
    """获取火山引擎 API Key"""
    api_key = VOLC_API_KEY
    if not api_key:
        config_file = os.path.expanduser("~/.volcengine_key")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    api_key = data.get("api_key")
            except Exception:
                pass
    return api_key


def text_to_speech_volc(text, output_path):
    """使用火山引擎 TTS 生成语音"""
    api_key = get_volc_api_key()
    if not api_key:
        print("Error: VOLC_API_KEY not set and no config file found")
        print("Please set VOLC_API_KEY environment variable or create ~/.volcengine_key")
        sys.exit(1)

    voice_type = VOICE_TYPE
    if not voice_type:
        print("Error: VOLC_VOICE_TYPE not set")
        print("Please set VOLC_VOICE_TYPE environment variable")
        sys.exit(1)

    payload = {
        "app": {
            "cluster": "volcano_icl"
        },
        "user": {
            "uid": "openclaw_tts"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "operation": "query"
        }
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    print(f"Generating voice for: {text}")
    response = requests.post(VOLC_TTS_URL, headers=headers, json=payload, timeout=60)

    if response.ok:
        result = response.json()
        if "data" in result and result["data"]:
            audio_data = base64.b64decode(result["data"])
            with open(output_path, "wb") as f:
                f.write(audio_data)
            return output_path
        else:
            print(f"API Error: {json.dumps(result, ensure_ascii=False)}")
            sys.exit(1)
    else:
        print(f"API HTTP Error: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)


def get_tenant_access_token():
    """获取飞书 tenant access token"""
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        print("Error: FEISHU_APP_ID or FEISHU_APP_SECRET not set")
        sys.exit(1)

    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    result = resp.json()
    if result.get('code') != 0:
        print(f"Error getting token: {result}")
        sys.exit(1)
    return result.get("tenant_access_token")


def convert_to_opus(input_path, output_path):
    """使用 ffmpeg 将音频转换为 opus 格式"""
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:a", "libopus", "-b:a", "24k",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def get_audio_duration(opus_path):
    """获取音频时长（毫秒）"""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", opus_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return int(float(result.stdout.strip()) * 1000)


def upload_audio(token, opus_path):
    """上传音频文件到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    headers = {"Authorization": f"Bearer {token}"}

    duration_ms = get_audio_duration(opus_path)

    with open(opus_path, 'rb') as f:
        files = {'file': ('audio.opus', f, 'audio/opus')}
        data = {'file_type': 'opus', 'file_name': 'voice.opus', 'duration': str(duration_ms)}
        resp = requests.post(url, headers=headers, files=files, data=data, timeout=60)

    result = resp.json()
    if result.get('code') != 0:
        print(f"Error uploading: {result}")
        sys.exit(1)
    return result.get('data', {}).get('file_key')


def parse_chat_id(chat_id_str):
    """
    解析聊天 ID，判断是单聊还是群聊
    - user:xxxxx  -> open_id, receive_id_type = "open_id"
    - chat:xxxxx  -> chat_id, receive_id_type = "chat_id"
    - 直接是 xxxxx -> 按原格式处理
    """
    if chat_id_str.startswith("user:"):
        return "open_id", chat_id_str.split(":", 1)[1]
    elif chat_id_str.startswith("chat:"):
        return "chat_id", chat_id_str.split(":", 1)[1]
    else:
        return "open_id", chat_id_str


def send_voice_message(token, chat_id, file_key):
    """发送语音消息（支持单聊和群聊）"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    receive_id_type, receive_id = parse_chat_id(chat_id)
    print(f"Using receive_id_type: {receive_id_type}, receive_id: {receive_id}")

    params = {"receive_id_type": receive_id_type}
    data = {
        "receive_id": receive_id,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key})
    }
    resp = requests.post(url, headers=headers, params=params, json=data, timeout=30)
    return resp.json()


def main():
    chat_id = FEISHU_CHAT_ID

    if not chat_id:
        print("Error: FEISHU_CHAT_ID not set")
        sys.exit(1)

    # 支持从命令行参数指定 chat_id
    text = None
    if len(sys.argv) >= 3 and (sys.argv[1] == "--chat" or sys.argv[1] == "-c"):
        chat_id = sys.argv[2]
        text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
    elif len(sys.argv) >= 2:
        text = sys.argv[1]
    else:
        print("Usage:")
        print("  python3 feishu_tts.py '要发送的文本'")
        print("  python3 feishu_tts.py -c 'chat:oc_xxxxx' '要发送的文本'  (指定群聊)")
        print("  python3 feishu_tts.py -c 'user:ou_xxxxx' '要发送的文本' (指定单聊)")
        print("\nEnvironment variables:")
        print("  FEISHU_APP_ID      - 飞书 App ID")
        print("  FEISHU_APP_SECRET  - 飞书 App Secret")
        print("  FEISHU_CHAT_ID     - 飞书聊天 ID (user:xxx 或 chat:xxx)")
        print("  VOLC_API_KEY       - 火山引擎 API Key")
        print("  VOLC_VOICE_TYPE    - 火山引擎音色 ID")
        sys.exit(1)

    if not text:
        print("请提供要发送的文本")
        sys.exit(1)

    # 生成临时文件
    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = os.path.join(tmpdir, "voice.mp3")
        opus_path = os.path.join(tmpdir, "voice.opus")

        # 使用火山引擎生成语音
        text_to_speech_volc(text, mp3_path)

        print("Converting to opus...")
        convert_to_opus(mp3_path, opus_path)

        print("Getting access token...")
        token = get_tenant_access_token()

        print("Uploading audio...")
        file_key = upload_audio(token, opus_path)
        print(f"File key: {file_key}")

        print("Sending voice message...")
        result = send_voice_message(token, chat_id, file_key)

        if result.get('code') == 0:
            print("Voice message sent successfully!")
        else:
            print(f"Error: {result}")
            sys.exit(1)


if __name__ == "__main__":
    main()
