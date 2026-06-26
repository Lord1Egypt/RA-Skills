#!/usr/bin/env python3
"""
飞书/Lark 发送普通文件脚本

用法:
  python3 send_file.py <file_path> <receive_id_type> <receive_id> <app_id> <app_secret> [file_name] [domain]

示例:
  python3 send_file.py /path/to/report.html open_id ou_xxx cli_xxx secret_xxx
  python3 send_file.py /path/to/archive.zip chat_id oc_xxx cli_xxx secret_xxx backup.zip
  python3 send_file.py /path/to/report.pdf open_id ou_xxx cli_xxx secret_xxx report.pdf lark
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


def upload_file(base: str, token: str, file_path: str, file_name: str) -> str:
    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-X",
            "POST",
            f"{base}/open-apis/im/v1/files",
            "-H",
            f"Authorization: Bearer {token}",
            "-F",
            "file_type=stream",
            "-F",
            f"file_name={file_name}",
            "-F",
            f"file=@{file_path}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"上传文件失败: {result.stderr.strip() or 'curl 执行失败'}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"上传文件返回了非 JSON 内容: {result.stdout[:500]}") from exc

    if data.get("code") != 0:
        raise RuntimeError(f"上传文件失败: {data}")

    file_key = data.get("data", {}).get("file_key")
    if not file_key:
        raise RuntimeError(f"上传文件失败，未返回 file_key: {data}")

    return file_key


def send_file_message(base: str, token: str, receive_id_type: str, receive_id: str, file_key: str) -> dict:
    url = f"{base}/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    payload = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key}, ensure_ascii=False),
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
            result = decode_json_bytes(resp.read(), "发送文件消息")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"发送文件消息 HTTP 失败: {exc.code} {body}") from exc

    if result.get("code") != 0:
        raise RuntimeError(f"发送文件消息失败: {result}")

    return result


def main() -> None:
    if len(sys.argv) < 6:
        print("用法: python3 send_file.py <file_path> <receive_id_type> <receive_id> <app_id> <app_secret> [file_name] [domain]")
        sys.exit(1)

    file_path = sys.argv[1]
    receive_id_type = sys.argv[2]
    receive_id = sys.argv[3]
    app_id = sys.argv[4]
    app_secret = sys.argv[5]
    file_name = sys.argv[6] if len(sys.argv) > 6 else os.path.basename(file_path)
    domain = sys.argv[7] if len(sys.argv) > 7 else "feishu"

    if receive_id_type not in VALID_RECEIVE_ID_TYPES:
        print(f"ERROR: receive_id_type 仅支持 {', '.join(sorted(VALID_RECEIVE_ID_TYPES))}")
        sys.exit(1)

    if not os.path.isfile(file_path):
        print(f"ERROR: 文件不存在: {file_path}")
        sys.exit(1)

    try:
        base = get_base(domain)
        print(f"📎 发送文件: {file_name}")
        print(f"🎯 接收类型: {receive_id_type}")
        print(f"🌐 Domain: {domain} ({base})")

        token = get_tenant_token(base, app_id, app_secret)
        print("✅ 获取 token 成功")

        file_key = upload_file(base, token, file_path, file_name)
        print(f"✅ 上传成功, file_key: {file_key}")

        result = send_file_message(base, token, receive_id_type, receive_id, file_key)
        message_id = result.get("data", {}).get("message_id")
        print(f"✅ 发送成功, message_id: {message_id}")
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
