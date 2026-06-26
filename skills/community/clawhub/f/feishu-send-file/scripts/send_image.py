#!/usr/bin/env python3
"""
飞书发送图片脚本（稳定版）

用途：
- 当 `message` tool 传本地图片路径后，飞书里只显示 `/root/...png` 路径文本，而不是真图片时
- 直接走飞书官方两步：上传图片 -> 发送 image_key

用法：
  python3 send_image.py <image_path> <open_id> <app_id> <app_secret> [domain]

示例：
  python3 send_image.py /root/myfiles/generated-images/demo.png ou_xxx cli_xxx secret_xxx
  python3 send_image.py /root/myfiles/generated-images/demo.png ou_xxx cli_xxx secret_xxx lark
"""

import sys
import os
import json
import urllib.request
import subprocess


def get_base(domain: str) -> str:
    if domain == "lark":
        return "https://open.larksuite.com"
    return "https://open.feishu.cn"


def get_tenant_token(base: str, app_id: str, app_secret: str) -> str:
    url = f"{base}/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise Exception(f"获取 token 失败: {result}")
    return result["tenant_access_token"]


def upload_image(base: str, token: str, image_path: str) -> str:
    result = subprocess.run([
        "curl", "-sS", "-X", "POST",
        f"{base}/open-apis/im/v1/images",
        "-H", f"Authorization: Bearer {token}",
        "-F", "image_type=message",
        "-F", f"image=@{image_path}",
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"上传图片失败: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    if data.get("code") != 0:
        raise Exception(f"上传图片失败: {data}")
    image_key = data.get("data", {}).get("image_key")
    if not image_key:
        raise Exception(f"上传图片失败：未返回 image_key: {data}")
    return image_key


def send_image_message(base: str, token: str, open_id: str, image_key: str):
    url = f"{base}/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": open_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key}, ensure_ascii=False),
    }
    data = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise Exception(f"发送图片消息失败: {result}")
    return result


def main():
    if len(sys.argv) < 5:
        print("用法: python3 send_image.py <image_path> <open_id> <app_id> <app_secret> [domain]")
        sys.exit(1)

    image_path = sys.argv[1]
    open_id = sys.argv[2]
    app_id = sys.argv[3]
    app_secret = sys.argv[4]
    domain = sys.argv[5] if len(sys.argv) > 5 else "feishu"

    if not os.path.exists(image_path):
        print(f"ERROR: 图片不存在: {image_path}")
        sys.exit(1)

    base = get_base(domain)
    print(f"🖼️ 发送图片: {os.path.basename(image_path)}")
    print(f"🌐 Domain: {domain} ({base})")

    token = get_tenant_token(base, app_id, app_secret)
    print("✅ 获取 token 成功")

    image_key = upload_image(base, token, image_path)
    print(f"✅ 上传成功, image_key: {image_key}")

    result = send_image_message(base, token, open_id, image_key)
    message_id = result.get("data", {}).get("message_id")
    print(f"✅ 发送成功, message_id: {message_id}")


if __name__ == "__main__":
    main()
