#!/usr/bin/env python3
"""
飞书图片发送助手
功能：上传图片到飞书并发送图片消息
支持两种方式：
1. 通过 receive_id (user_id/open_id/chat_id) 发送
2. 通过 message_id 回复（自动发送到对话中）

【配置方式】（按优先级）
1. 环境变量：FEISHU_APP_ID / FEISHU_APP_SECRET
2. OpenClaw 主配置：~/.openclaw/openclaw.json 中的 feishu 配置
"""

import os
import json
import requests
import sys
import argparse
import threading
import hashlib
from pathlib import Path

# ========== Rate Limiting ==========
_rate_limit_lock = threading.Lock()
_rate_limit_store = {}

RATE_LIMIT_MAX = 30         # 最多 30 次
RATE_LIMIT_WINDOW = 60       # 滑动窗口 60 秒

def _check_rate_limit(client_key: str) -> bool:
    now = datetime.now()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    with _rate_limit_lock:
        _rate_limit_store[client_key] = [
            ts for ts in _rate_limit_store.get(client_key, []) if ts > window_start
        ]
        if len(_rate_limit_store[client_key]) >= RATE_LIMIT_MAX:
            return False
        _rate_limit_store[client_key].append(now)
        return True

# ========== File Type Validation ==========
_ALLOWED_MAGIC = {
    b'\xff\xd8\xff':       'jpeg',
    b'\x89PNG\r\n\x1a\n': 'png',
    b'GIF87a':             'gif',
    b'GIF89a':             'gif',
    b'RIFF':               'webp',  # RIFF....WEBP
    b'BM':                 'bmp',
}

def _validate_image(path: str) -> bool:
    """通过 magic bytes 校验是否为图片，返回 True 表示通过"""
    try:
        with open(path, 'rb') as f:
            header = f.read(12)
        for magic in _ALLOWED_MAGIC:
            if header.startswith(magic):
                return True
        # WebP 特殊判断（RIFF....WEBP）
        if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
            return True
        return False
    except Exception:
        return False
from datetime import datetime, timedelta


def load_feishu_config():
    """级联读取飞书配置（优先级：环境变量 > OpenClaw主配置）"""
    # 1. 环境变量
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if app_id and app_secret:
        return app_id, app_secret

    # 2. OpenClaw 主配置
    openclaw_config_path = Path.home() / ".openclaw" / "openclaw.json"
    if openclaw_config_path.exists():
        try:
            with open(openclaw_config_path) as f:
                config = json.load(f)
            feishu = config.get("channels", {}).get("feishu") or config.get("feishu") or {}
            app_id = feishu.get("appId") or feishu.get("app_id")
            app_secret = feishu.get("appSecret") or feishu.get("app_secret")
            if app_id and app_secret:
                return app_id, app_secret
        except Exception:
            pass

    return None, None


def get_tenant_token(app_id, app_secret):
    """获取 tenant_access_token"""
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=10
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def upload_image(token, image_path):
    """上传图片到飞书，获取 image_key"""
    with open(image_path, "rb") as f:
        resp = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/images",
            headers={"Authorization": f"Bearer {token}"},
            files={
                "image_type": (None, "message"),
                "image": (os.path.basename(image_path), f, "image/jpeg"),
            },
            timeout=30
        )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"上传图片失败: {data}")
    return data["data"]["image_key"]


def send_image_by_id(token, receive_id_type, receive_id, image_key):
    """通过 receive_id 发送图片"""
    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages",
        params={"receive_id_type": receive_id_type},
        headers={"Authorization": f"Bearer {token}"},
        json={
            "receive_id": receive_id,
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key}),
        },
        timeout=10
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"发送消息失败: {data}")
    return data


def send_image_reply(token, message_id, image_key):
    """通过 message_id 回复图片"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/reply"
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key}),
        },
        timeout=10
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"回复消息失败: {data}")
    return data


def main():
    parser = argparse.ArgumentParser(description="飞书图片发送助手")
    parser.add_argument("image", help="图片路径")
    parser.add_argument("--chat-id", help="群聊 ID (以 chat_ 开头)")
    parser.add_argument("--user-id", help="用户 ID (以 u_ 开头)")
    parser.add_argument("--open-id", help="用户 Open ID (以 o_ 开头)")
    parser.add_argument("--message-id", help="飞书消息 ID (用于回复模式)")

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"错误: 图片文件不存在: {args.image}", file=sys.stderr)
        sys.exit(1)

    # 文件类型校验
    if not _validate_image(args.image):
        print(f"错误: 不是支持的图片格式（支持 JPEG/PNG/GIF/WebP/BMP）: {args.image}", file=sys.stderr)
        sys.exit(1)

    # 速率限制（按发送目标维度）
    rate_key = args.chat_id or args.user_id or args.open_id or args.message_id or "default"
    if not _check_rate_limit(rate_key):
        print(f"错误: 发送过于频繁，请稍后再试（60秒最多{RATE_LIMIT_MAX}次）", file=sys.stderr)
        sys.exit(1)

    # 加载配置
    app_id, app_secret = load_feishu_config()
    if not app_id or not app_secret:
        print("错误: 未配置飞书凭证", file=sys.stderr)
        print("", file=sys.stderr)
        print("请通过以下方式配置（任选一种）：", file=sys.stderr)
        print("1. 环境变量：export FEISHU_APP_ID=xxx FEISHU_APP_SECRET=xxx", file=sys.stderr)
        print("2. OpenClaw 主配置：~/.openclaw/openclaw.json 中的 feishu 节点", file=sys.stderr)
        print("", file=sys.stderr)
        print("获取飞书配置: https://open.feishu.cn/", file=sys.stderr)
        sys.exit(1)

    # 执行发送
    print("获取 token...")
    token = get_tenant_token(app_id, app_secret)

    print("上传图片...")
    image_key = upload_image(token, args.image)
    print(f"图片 key: {image_key}")

    # 选择发送方式
    if args.message_id:
        print(f"回复消息 {args.message_id}...")
        result = send_image_reply(token, args.message_id, image_key)
    elif args.chat_id or args.user_id or args.open_id:
        if args.chat_id:
            receive_id_type = "chat_id"
            receive_id = args.chat_id
        elif args.user_id:
            receive_id_type = "user_id"
            receive_id = args.user_id
        else:
            receive_id_type = "open_id"
            receive_id = args.open_id

        print(f"发送到 {receive_id_type}: {receive_id}...")
        result = send_image_by_id(token, receive_id_type, receive_id, image_key)
    else:
        print(
            "错误: 请指定 --message-id, --chat-id, --user-id 或 --open-id",
            file=sys.stderr,
        )
        sys.exit(1)

    print("发送成功!")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
