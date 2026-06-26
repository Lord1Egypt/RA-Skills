#!/usr/bin/env python3
"""
飞书/Lark 稳定发送图片脚本

用途:
- 当常规消息链路把本地图片错误发送为路径文本时，直接走官方上传图片接口

用法:
  python3 send_image.py <image_path> <receive_id_type> <receive_id> <app_id> <app_secret> [domain]

示例:
  python3 send_image.py /path/to/demo.png open_id ou_xxx cli_xxx secret_xxx
  python3 send_image.py /path/to/demo.png chat_id oc_xxx cli_xxx secret_xxx lark
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request


VALID_RECEIVE_ID_TYPES = {"open_id", "chat_id"}
VALID_DOMAINS = {
    "feishu": "https://open.feishu.cn",
    "lark": "https://open.larksuite.com",
}


def get_base(domain: str) -> str:
    if domain not in VALID_DOMAINS:
        raise ValueError(f"不支持的 domain: {domain}，仅支持: {', '.join(sorted(VALID_DOMAINS))}")
    return VALID_DOMAINS[domain]


def decode_json_bytes(raw: bytes, context: str) -> dict:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"{context} 返回了非 UTF-8 内容") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{context} 返回了非 JSON 内容: {text[:500]}") from exc


def get_tenant_token(base: str, app_id: str, app_secret: str) -> str:
    url = f"{base}/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as resp:
            result = decode_json_bytes(resp.read(), "获取 token")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"获取 token HTTP 失败: {exc.code} {body}") from exc

    if result.get("code") != 0:
        raise RuntimeError(f"获取 token 失败: {result}")

    token = result.get("tenant_access_token")
    if not token:
        raise RuntimeError(f"获取 token 失败，返回中缺少 tenant_access_token: {result}")
    return token


def upload_image(base: str, token: str, image_path: str) -> str:
    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-X",
            "POST",
            f"{base}/open-apis/im/v1/images",
            "-H",
            f"Authorization: Bearer {token}",
            "-F",
            "image_type=message",
            "-F",
            f"image=@{image_path}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"上传图片失败: {result.stderr.strip() or 'curl 执行失败'}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"上传图片返回了非 JSON 内容: {result.stdout[:500]}") from exc

    if data.get("code") != 0:
        raise RuntimeError(f"上传图片失败: {data}")

    image_key = data.get("data", {}).get("image_key")
    if not image_key:
        raise RuntimeError(f"上传图片失败，未返回 image_key: {data}")

    return image_key


def send_image_message(base: str, token: str, receive_id_type: str, receive_id: str, image_key: str) -> dict:
    url = f"{base}/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    payload = {
        "receive_id": receive_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key}, ensure_ascii=False),
    }
    data = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = decode_json_bytes(resp.read(), "发送图片消息")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"发送图片消息 HTTP 失败: {exc.code} {body}") from exc

    if result.get("code") != 0:
        raise RuntimeError(f"发送图片消息失败: {result}")

    return result


def main() -> None:
    if len(sys.argv) < 6:
        print("用法: python3 send_image.py <image_path> <receive_id_type> <receive_id> <app_id> <app_secret> [domain]")
        sys.exit(1)

    image_path = sys.argv[1]
    receive_id_type = sys.argv[2]
    receive_id = sys.argv[3]
    app_id = sys.argv[4]
    app_secret = sys.argv[5]
    domain = sys.argv[6] if len(sys.argv) > 6 else "feishu"

    if receive_id_type not in VALID_RECEIVE_ID_TYPES:
        print(f"ERROR: receive_id_type 仅支持 {', '.join(sorted(VALID_RECEIVE_ID_TYPES))}")
        sys.exit(1)

    if not os.path.isfile(image_path):
        print(f"ERROR: 图片不存在: {image_path}")
        sys.exit(1)

    try:
        base = get_base(domain)
        print(f"🖼️ 发送图片: {os.path.basename(image_path)}")
        print(f"🎯 接收类型: {receive_id_type}")
        print(f"🌐 Domain: {domain} ({base})")

        token = get_tenant_token(base, app_id, app_secret)
        print("✅ 获取 token 成功")

        image_key = upload_image(base, token, image_path)
        print(f"✅ 上传成功, image_key: {image_key}")

        result = send_image_message(base, token, receive_id_type, receive_id, image_key)
        message_id = result.get("data", {}).get("message_id")
        print(f"✅ 发送成功, message_id: {message_id}")
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
