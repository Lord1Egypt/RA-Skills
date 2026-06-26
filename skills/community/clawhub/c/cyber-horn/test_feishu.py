"""
仅测试飞书：鉴权 + 向指定群/会话发一条文本消息。
不依赖 TTS、FFmpeg、ElevenLabs。

用法:
  python test_feishu.py --chat_id <CHAT_ID>
需在 .env 中配置 FEISHU_APP_ID、FEISHU_APP_SECRET。
"""
import argparse
import json
import sys

import requests

from config import load_env, get_env, get_feishu_config
from feishu_client import get_tenant_access_token

MESSAGE_CREATE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


def send_text_message(token: str, receive_id: str, text: str, receive_id_type: str = "chat_id") -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    params = {"receive_id_type": receive_id_type}
    payload = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }
    resp = requests.post(MESSAGE_CREATE_URL, params=params, headers=headers, json=payload, timeout=10)
    result = resp.json()
    code = result.get("code", -1)
    if code != 0:
        msg = result.get("msg", resp.text)
        raise RuntimeError(f"飞书发消息失败 code={code} msg={msg}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="仅测试飞书鉴权与发文本消息")
    parser.add_argument("--chat_id", required=True, help="群/会话的 chat_id")
    parser.add_argument("--text", default="这是一条来自 test_feishu 的测试消息。", help="要发送的文本")
    args = parser.parse_args()

    load_env()
    missing = [k for k in ("FEISHU_APP_ID", "FEISHU_APP_SECRET") if not get_env(k)]
    if missing:
        print(f"[Test] 缺少环境变量: {', '.join(missing)}", file=sys.stderr)
        return 1

    feishu = get_feishu_config()
    print("[Test] 飞书鉴权...")
    try:
        token = get_tenant_access_token(feishu["app_id"], feishu["app_secret"])
    except Exception as e:
        print(f"[Test] 鉴权失败: {e}", file=sys.stderr)
        return 1
    print("[Test] 鉴权成功，发送文本消息...")
    try:
        send_text_message(token, args.chat_id, args.text)
    except Exception as e:
        print(f"[Test] 发消息失败: {e}", file=sys.stderr)
        return 1
    print("[Test] 已发送，请在飞书客户端查看。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
