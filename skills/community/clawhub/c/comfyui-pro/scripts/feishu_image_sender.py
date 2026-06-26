#!/usr/bin/env python3
"""
飞书图片发送工具
将本地图片发送到飞书（显示为图片预览，而非文件附件）
"""

import os
import sys
import json
import base64
from pathlib import Path

# 飞书 API 配置（从 openclaw.json 读取）
FEISHU_CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"


def get_feishu_token():
    """获取飞书 API Token"""
    if not FEISHU_CONFIG_FILE.exists():
        return None
    
    with open(FEISHU_CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 尝试从 channels.feishu 获取
    try:
        channels = config.get('channels', {})
        feishu = channels.get('feishu', {})
        accounts = feishu.get('accounts', {})
        main = accounts.get('main', {})
        token = main.get('appAccessToken')
        if token:
            return token
        # 如果没有 appAccessToken，尝试使用 app_access_token（内部格式）
        return main.get('app_access_token')
    except Exception as e:
        print(f"[ERR] 读取配置失败：{e}")
        return None


def upload_image_to_feishu(image_path: str) -> str:
    """
    上传图片到飞书云端，获取 image_key
    
    Args:
        image_path: 本地图片路径
    
    Returns:
        image_key: 飞书云端图片 key
    """
    import urllib.request
    import urllib.error
    
    token = get_feishu_token()
    if not token:
        print("[ERR] 无法获取飞书 API Token")
        return None
    
    # 读取图片
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 上传到飞书
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    # 构建 multipart/form-data 请求
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"image_type\"\r\n\r\n"
        f"message\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"image\"; filename=\"image.png\"\r\n"
        f"Content-Type: image/png\r\n\r\n"
    ).encode('utf-8') + image_data + f"\r\n--{boundary}--\r\n".encode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    
    req = urllib.request.Request(url, data=body, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result['data']['image_key']
            else:
                print(f"[ERR] 上传失败：{result.get('msg')}")
                return None
    except Exception as e:
        print(f"[ERR] 上传错误：{e}")
        return None


def send_image_message(chat_id: str, image_key: str, caption: str = ""):
    """
    发送图片消息到飞书
    
    Args:
        chat_id: 聊天 ID (user_id 或 chat_id)
        image_key: 飞书云端图片 key
        caption: 图片说明文字
    """
    import urllib.request
    import urllib.error
    
    token = get_feishu_token()
    if not token:
        print("[ERR] 无法获取飞书 API Token")
        return False
    
    # 构建消息内容
    content = {
        "image_key": image_key
    }
    
    # 发送消息
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    params = {"receive_id_type": "user_id"} if chat_id.startswith("ou_") else {"receive_id_type": "chat_id"}
    
    body = json.dumps({
        "receive_id": chat_id,
        "msg_type": "image",
        "content": json.dumps(content)
    }).encode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}", data=body, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                print(f"[OK] 图片发送成功：{result['data']['message_id']}")
                return True
            else:
                print(f"[ERR] 发送失败：{result.get('msg')}")
                return False
    except Exception as e:
        print(f"[ERR] 发送错误：{e}")
        return False


def send_image_to_feishu(image_path: str, chat_id: str, caption: str = "") -> bool:
    """
    一键发送图片到飞书（上传 + 发送）
    
    Args:
        image_path: 本地图片路径
        chat_id: 聊天 ID
        caption: 图片说明文字
    
    Returns:
        bool: 是否成功
    """
    print(f"[IMG] 准备发送图片：{image_path}")
    
    # 1. 上传图片
    print("[IMG] 正在上传图片到飞书...")
    image_key = upload_image_to_feishu(image_path)
    
    if not image_key:
        print("[ERR] 图片上传失败")
        return False
    
    print(f"[OK] 上传成功，image_key: {image_key[:20]}...")
    
    # 2. 发送消息
    print("[IMG] 正在发送消息...")
    success = send_image_message(chat_id, image_key, caption)
    
    return success


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python feishu_image_sender.py <图片路径> <聊天 ID> [说明文字]")
        print("示例：python feishu_image_sender.py output/image.png ou_xxx 哆啦 A 梦")
        sys.exit(1)
    
    image_path = sys.argv[1]
    chat_id = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else ""
    
    if not os.path.exists(image_path):
        print(f"[ERR] 图片文件不存在：{image_path}")
        sys.exit(1)
    
    success = send_image_to_feishu(image_path, chat_id, caption)
    sys.exit(0 if success else 1)
