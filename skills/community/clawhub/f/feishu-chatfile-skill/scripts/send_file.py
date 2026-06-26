#!/usr/bin/env python3
"""
飞书发送文件脚本

用法:
  python3 send_file.py <file_path> <receive_id> <app_id> <app_secret> [file_name]

示例:
  python3 send_file.py /path/to/file.txt ou_xxx cli_xxx secret_xxx
"""

import sys
import os
import json
import urllib.request


def get_tenant_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
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


def upload_file(token, file_path, file_name):
    """上传文件到飞书，返回 file_key"""
    import subprocess
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        "https://open.feishu.cn/open-apis/im/v1/files",
        "-H", f"Authorization: Bearer {token}",
        "-F", "file_type=stream",
        "-F", f"file_name={file_name}",
        "-F", f"file=@{file_path}"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"curl 上传失败: {result.stderr.strip()}")

    try:
        data = json.loads(result.stdout)
    except Exception as e:
        raise Exception(f"解析上传响应失败: {e}, 响应内容: {result.stdout}")

    if data.get("code") != 0:
        print(f"❌ 上传文件失败: code={data.get('code')}, msg={data.get('msg')}")
        raise Exception(f"上传文件失败: {data}")
    return data["data"]["file_key"]


def get_receive_id_type(receive_id):
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


def send_file_message(token, receive_id, file_key):
    """发送文件消息"""
    # 处理 receive_id 格式，提取 ou_... 或 oc_...
    if "ou_" in receive_id:
        receive_id = "ou_" + receive_id.split("ou_")[1].split()[0]
    elif "oc_" in receive_id:
        receive_id = "oc_" + receive_id.split("oc_")[1].split()[0]

    rid_type = get_receive_id_type(receive_id)
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={rid_type}"
    payload = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except Exception as e:
        raise Exception(f"请求发送消息接口失败: {e}")

    if result.get("code") != 0:
        print(f"❌ 发送失败: code={result.get('code')}, msg={result.get('msg')}")
        raise Exception(f"发送消息失败 (type={rid_type}): {result}")
    return result


def main():
    if len(sys.argv) < 5:
        print("用法: python3 send_file.py <file_path> <receive_id> <app_id> <app_secret> [file_name]")
        print("说明: receive_id 支持 ou_... (open_id) 或 oc_... (chat_id)")
        sys.exit(1)

    file_path = sys.argv[1]
    receive_id = sys.argv[2]
    app_id = sys.argv[3]
    app_secret = sys.argv[4]
    file_name = sys.argv[5] if len(sys.argv) > 5 else os.path.basename(file_path)

    if not os.path.exists(file_path):
        print(f"❌ ERROR: 文件不存在: {file_path}")
        sys.exit(1)

    rid_type = get_receive_id_type(receive_id)
    print(f"📎 正在发送文件: {file_name}")
    print(f"🎯 目标: {receive_id} ({rid_type})")

    try:
        token = get_tenant_token(app_id, app_secret)
        file_key = upload_file(token, file_path, file_name)
        result = send_file_message(token, receive_id, file_key)
        
        message_id = result.get("data", {}).get("message_id")
        code = result.get("code")
        msg = result.get("msg")
        print(f"✅ 发送成功！code={code}, msg={msg}, message_id={message_id}")
    except Exception as e:
        print(f"💥 运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
