# 本文件负责通过 Telegram Bot API 推送生成好的舆情日报。

import json
import shutil
import subprocess
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def _send_message_with_curl(bot_token, chat_id, text):
    """优先使用 curl 发送，实测比 urllib 在当前环境更稳定。"""
    curl_path = shutil.which("curl")
    if not curl_path:
        raise RuntimeError("curl 不可用")
    command = [
        curl_path,
        "-sS",
        "-X",
        "POST",
        "https://api.telegram.org/bot%s/sendMessage" % bot_token,
        "--data-urlencode",
        "chat_id=%s" % chat_id,
        "--data-urlencode",
        "text=%s" % text,
        "--data-urlencode",
        "disable_web_page_preview=true",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(completed.stdout)
    if not data.get("ok"):
        raise RuntimeError("Telegram 推送失败：%s" % data)
    return data


def _send_message_with_urllib(bot_token, chat_id, text):
    """保留 urllib 作为无 curl 环境下的回退实现。"""
    url = "https://api.telegram.org/bot%s/sendMessage" % bot_token
    payload = urlencode({
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": "true",
    }).encode("utf-8")
    request = Request(url, data=payload, method="POST")
    with urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not data.get("ok"):
        raise RuntimeError("Telegram 推送失败：%s" % data)
    return data


def send_message(bot_token, chat_id, text):
    """调用 Telegram sendMessage，优先走 curl，失败时再尝试 urllib。"""
    try:
        return _send_message_with_curl(bot_token, chat_id, text)
    except Exception:
        return _send_message_with_urllib(bot_token, chat_id, text)
