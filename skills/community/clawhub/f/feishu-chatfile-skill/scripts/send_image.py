#!/usr/bin/env python3
"""
飞书发送图片脚本

用法:
  python3 send_image.py <image_path> <receive_id> <app_id> <app_secret> [domain]

示例:
  python3 send_image.py /path/to/image.png ou_xxx cli_xxx secret_xxx
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
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except Exception as e:
        raise Exception(f"请求 token 接口失败: {e}")

    if result.get("code") != 0:
        print(f"❌ 获取 token 失败: code={result.get('code')}, msg={result.get('msg')}")
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
        raise Exception(f"curl 上传失败: {result.stderr.strip()}")
    
    try:
        data = json.loads(result.stdout)
    except Exception as e:
        raise Exception(f"解析上传响应失败: {e}, 响应内容: {result.stdout}")

    if data.get("code") != 0:
        print(f"❌ 上传图片失败: code={data.get('code')}, msg={data.get('msg')}")
        raise Exception(f"上传图片失败: {data}")
    
    image_key = data.get("data", {}).get("image_key")
    if not image_key:
        raise Exception(f"上传成功但未返回 image_key: {data}")
    return image_key


def get_receive_id_type(receive_id: str) -> str:
    """根据 ID 前缀判断类型: ou_ 为 open_id, oc_ 为 chat_id"""
    if receive_id.startswith("ou_"):
        return "open_id"
    if receive_id.startswith("oc_"):
        return "chat_id"
    if "ou_" in receive_id:
        return "open_id"
    if "oc_" in receive_id:
        return "chat_id"
    return "open_id"


def send_image_message(base: str, token: str, receive_id: str, image_key: str):
    # 处理 receive_id 格式，提取 ou_... 或 oc_...
    if "ou_" in receive_id:
        receive_id = "ou_" + receive_id.split("ou_")[1].split()[0]
    elif "oc_" in receive_id:
        receive_id = "oc_" + receive_id.split("oc_")[1].split()[0]

    rid_type = get_receive_id_type(receive_id)
    url = f"{base}/open-apis/im/v1/messages?receive_id_type={rid_type}"
    payload = {
        "receive_id": receive_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key}, ensure_ascii=False),
    }
    data = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except Exception as e:
        raise Exception(f"请求发送消息接口失败: {e}")

    if result.get("code") != 0:
        print(f"❌ 发送失败: code={result.get('code')}, msg={result.get('msg')}")
        raise Exception(f"发送图片消息失败 (type={rid_type}): {result}")
    return result


def main():
    if len(sys.argv) < 5:
        print("用法: python3 send_image.py <image_path> <receive_id> <app_id> <app_secret> [domain]")
        print("说明: receive_id 支持 ou_... (open_id) 或 oc_... (chat_id)")
        sys.exit(1)

    image_path = sys.argv[1]
    receive_id = sys.argv[2]
    app_id = sys.argv[3]
    app_secret = sys.argv[4]
    domain = sys.argv[5] if len(sys.argv) > 5 else "feishu"

    if not os.path.exists(image_path):
        print(f"❌ ERROR: 图片不存在: {image_path}")
        sys.exit(1)

    base = get_base(domain)
    rid_type = get_receive_id_type(receive_id)
    print(f"🖼️  正在发送图片: {os.path.basename(image_path)}")
    print(f"🎯 目标: {receive_id} ({rid_type})")

    try:
        token = get_tenant_token(base, app_id, app_secret)
        image_key = upload_image(base, token, image_path)
        result = send_image_message(base, token, receive_id, image_key)
        
        message_id = result.get("data", {}).get("message_id")
        code = result.get("code")
        msg = result.get("msg")
        print(f"✅ 发送成功！code={code}, msg={msg}, message_id={message_id}")
    except Exception as e:
        print(f"💥 运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
