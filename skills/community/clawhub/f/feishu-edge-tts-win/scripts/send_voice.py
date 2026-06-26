#!/usr/bin/env python3
"""
Usage:
  python send_voice.py <text> <open_id> [--voice <voice>] [--config <openclaw.json path>]
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
FEISHU_API = "https://open.feishu.cn/open-apis"


def default_config_path() -> str:
    user_home = os.path.expanduser("~")
    return os.path.join(user_home, ".openclaw", "openclaw.json")


def get_token(app_id: str, app_secret: str) -> str:
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/auth/v3/tenant_access_token/internal",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read())
    return payload["tenant_access_token"]


def upload_file(token: str, opus_path: str) -> str:
    # Use curl for multipart upload.
    result = subprocess.run(
        [
            "curl",
            "-s",
            "-X",
            "POST",
            f"{FEISHU_API}/im/v1/files",
            "-H",
            f"Authorization: Bearer {token}",
            "-F",
            "file_type=opus",
            "-F",
            "file_name=voice.opus",
            "-F",
            f"file=@{opus_path}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    return payload["data"]["file_key"]


def send_audio(token: str, open_id: str, file_key: str) -> dict:
    content = json.dumps({"file_key": file_key})
    body = json.dumps(
        {
            "receive_id": open_id,
            "msg_type": "audio",
            "content": content,
        }
    ).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/im/v1/messages?receive_id_type=open_id",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


async def tts_to_mp3(text: str, voice: str, mp3_path: str) -> None:
    import edge_tts

    communicator = edge_tts.Communicate(text, voice)
    await communicator.save(mp3_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("open_id", help="Feishu user open_id")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS voice")
    parser.add_argument("--config", default=default_config_path(), help="Path to openclaw.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not os.path.exists(args.config):
        print(f"Config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    feishu = config["channels"]["feishu"]
    app_id = feishu["appId"]
    app_secret = feishu["appSecret"]

    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = os.path.join(tmpdir, "voice.mp3")
        opus_path = os.path.join(tmpdir, "voice.opus")

        print(f"Generating speech ({args.voice})...")
        asyncio.run(tts_to_mp3(args.text, args.voice, mp3_path))

        subprocess.run(
            ["ffmpeg", "-i", mp3_path, "-c:a", "libopus", opus_path, "-y"],
            capture_output=True,
            check=True,
        )

        token = get_token(app_id, app_secret)

        print("Uploading audio...")
        file_key = upload_file(token, opus_path)

        result = send_audio(token, args.open_id, file_key)
        if result.get("code") == 0:
            print(f"Success. message_id: {result['data']['message_id']}")
            return

        print(f"Send failed: {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
