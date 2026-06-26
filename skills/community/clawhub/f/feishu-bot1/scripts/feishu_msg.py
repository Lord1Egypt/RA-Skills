"""
飞书消息操作脚本（支持文件发送）
用法:
  python feishu_msg.py send-user <open_id> <消息内容>
  python feishu_msg.py send-chat <chat_id> <消息内容>
  python feishu_msg.py search-user <姓名关键词>
  python feishu_msg.py search-chat <群名关键词>
  python feishu_msg.py get-messages <chat_id> [page_size]
  python feishu_msg.py send-file <chat_id> <本地文件路径>
"""

import json
import sys
import urllib.parse
import uuid
import datetime
import os

# 全局 UTF-8 输出修复（Windows GBK 终端适配）
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = __file__.rsplit("/", 1)[0] if "/" in __file__ else __file__.rsplit("\\", 1)[0]
CONFIG_PATH = SCRIPT_DIR + "/config.json"

# 尝试导入 lark-oapi SDK，upload_file 函数会用到
try:
    import lark_oapi as lark
    from lark_oapi.api.im.v1 import *
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result.get("tenant_access_token", "")


def send_message(receive_id, receive_id_type, content, msg_type="text"):
    if not SDK_AVAILABLE:
        # fallback to urllib
        import urllib.request
        config = load_config()
        token = get_tenant_access_token(config["app_id"], config["app_secret"])
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=" + receive_id_type
        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps({"text": content}) if msg_type == "text" else content,
            "uuid": str(uuid.uuid4())
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST", headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}"
        })
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        print(json.dumps(result, ensure_ascii=False))
        return result

    # Use SDK
    client = lark.Client.builder() \
        .app_id(load_config()["app_id"]) \
        .app_secret(load_config()["app_secret"]) \
        .log_level(lark.LogLevel.ERROR) \
        .build()

    request = CreateMessageRequest.builder() \
        .receive_id_type(receive_id_type) \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type(msg_type)
            .content(content if msg_type != "text" else json.dumps({"text": content}))
            .build()) \
        .build()

    response = client.im.v1.message.create(request)
    print(json.dumps({"code": response.code, "msg": response.msg}, ensure_ascii=False))
    return {"code": response.code, "msg": response.msg}


def send_user(open_id, content):
    return send_message(open_id, "open_id", content)


def send_chat(chat_id, content):
    return send_message(chat_id, "chat_id", content)


def _upload_file_http(filename, file_data):
    """通过 HTTP multipart/form-data 直接上传文件（适合所有文件大小）"""
    import urllib.request, urllib.error

    file_size = len(file_data)
    boundary = uuid.uuid4().hex

    # Build multipart form data
    body_parts = []
    body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file_type"\r\n\r\nstream'.encode())
    body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file_name"\r\n\r\n{filename}'.encode())
    body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="size"\r\n\r\n{file_size}'.encode())
    header_part = f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()
    body_parts.append(header_part + file_data + f'\r\n--{boundary}--'.encode())
    body = b'\r\n'.join(body_parts)

    # Get token
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])

    url = 'https://open.feishu.cn/open-apis/im/v1/files?receive_id_type=chat_id'
    req = urllib.request.Request(url, data=body, headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    })

    try:
        with urllib.request.urlopen(req, timeout=max(60, file_size // 1024 // 100)) as r:
            resp = json.loads(r.read())
            if resp.get('code') == 0:
                return resp['data']['file_key']
            else:
                print(json.dumps({"code": resp.get('code'), "msg": resp.get('msg')}, ensure_ascii=False))
                return None
    except urllib.error.HTTPError as e:
        body_err = e.read().decode('utf-8', errors='replace')
        try:
            err_obj = json.loads(body_err)
            print(json.dumps({"code": err_obj.get('code'), "msg": err_obj.get('msg')}, ensure_ascii=False))
        except Exception:
            print(json.dumps({"code": e.code, "msg": body_err[:500]}, ensure_ascii=False))
        return None


def send_file(chat_id, filepath):
    """上传本地文件并发送到群聊"""
    import io
    if not SDK_AVAILABLE:
        print("错误: 需要安装 lark-oapi SDK，请运行: pip install lark-oapi")
        return

    if not os.path.exists(filepath):
        print(f"错误: 文件不存在: {filepath}")
        return

    filename = os.path.basename(filepath)
    config = load_config()

    client = lark.Client.builder() \
        .app_id(config["app_id"]) \
        .app_secret(config["app_secret"]) \
        .log_level(lark.LogLevel.ERROR) \
        .build()

    # 1. 根据扩展名判断文件类型
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    image_exts = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    with open(filepath, 'rb') as f:
        file_data = f.read()

    file_size = len(file_data)
    print(f"文件大小: {file_size/1024/1024:.2f} MB")

    # 图片类型使用 image.create API
    if ext in image_exts:
        from lark_oapi.api.im.v1 import CreateImageRequest, CreateImageRequestBody
        upload_req = CreateImageRequest.builder().request_body(
            CreateImageRequestBody.builder().image_type('message').image(io.BytesIO(file_data)).build()
        ).build()
        upload_resp = client.im.v1.image.create(upload_req)
        if upload_resp.code != 0:
            print(json.dumps({"code": upload_resp.code, "msg": upload_resp.msg}, ensure_ascii=False))
            return
        image_key = upload_resp.data.image_key
        print(f"图片上传成功: {filename} -> image_key: {image_key}")
        content = json.dumps({"image_key": image_key})
        msg_type = "image"
    else:
        # 其他文件使用 HTTP 直传（所有文件均走 im/v1/files 接口）
        file_key = _upload_file_http(filename, file_data)
        if file_key is None:
            return
        print(f"文件上传成功: {filename} -> file_key: {file_key}")
        content = json.dumps({"file_key": file_key})
        msg_type = "file"

    # 2. 发送消息
    from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
    msg_request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type(msg_type)
            .content(content)
            .build()) \
        .build()

    msg_response = client.im.v1.message.create(msg_request)
    print(json.dumps({"code": msg_response.code, "msg": msg_response.msg}, ensure_ascii=False))


def search_user(keyword):
    import urllib.request
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/search?query={encoded_keyword}&page_size=20&user_id_type=open_id"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def search_chat(keyword):
    import urllib.request
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://open.feishu.cn/open-apis/im/v1/chats?search_key={encoded_keyword}&page_size=20"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def get_messages(chat_id, page_size=50):
    """获取群聊消息列表，正确解析并展示中文内容"""
    import urllib.request
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id={chat_id}&page_size={page_size}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if result.get("code") != 0:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    items = result.get("data", {}).get("items", [])
    print(f"共获取到 {len(items)} 条消息：")
    print()

    for it in items:
        msg_type = it.get("msg_type")
        sender = it.get("sender", {})
        sender_id = sender.get("id", "")
        sender_type = sender.get("sender_type", "")
        ct = int(it.get("create_time", 0)) // 1000
        dt = datetime.datetime.fromtimestamp(ct).strftime("%Y-%m-%d %H:%M:%S") if ct else "N/A"

        body_str = it.get("body", {}).get("content", "{}")
        body = json.loads(body_str)

        print(f"[{dt}] {sender_type} {sender_id[:16]} | {msg_type}")

        if msg_type == "text":
            text = body.get("text", "")
            print(f"  {text}")
        elif msg_type == "post":
            title = body.get("title", "")
            parts = []
            for section in body.get("content", []):
                for item in section:
                    tag = item.get("tag", "")
                    if tag == "text":
                        parts.append(item.get("text", ""))
                    elif tag == "at":
                        parts.append("@" + item.get("user_id", ""))
                    elif tag == "a":
                        parts.append(item.get("text", "") + "(" + item.get("href", "") + ")")
            content = "".join(parts)
            if title:
                print(f"  Title: {title}")
            print(f"  {content}")
        elif msg_type == "file":
            file_key = body.get("file_key", "")
            print(f"  [文件] key: {file_key}")
        elif msg_type == "system":
            template = body.get("template", "")
            from_user = ",".join(body.get("from_user", []))
            to_chatters = ",".join(body.get("to_chatters", []))
            try:
                content_str = template.format(from_user=from_user, to_chatters=to_chatters)
            except Exception:
                content_str = json.dumps(body, ensure_ascii=False)
            print(f"  {content_str}")
        else:
            print(f"  {json.dumps(body, ensure_ascii=False)[:100]}")
        print()

    return result


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("用法: python feishu_msg.py <command> [args...]")
        print("可用命令: send-user, send-chat, search-user, search-chat, get-messages, send-file")
        sys.exit(1)

    cmd = args[0]

    if cmd == "send-user" and len(args) >= 3:
        send_user(args[1], args[2])
    elif cmd == "send-chat" and len(args) >= 3:
        send_chat(args[1], args[2])
    elif cmd == "search-user" and len(args) >= 2:
        search_user(args[1])
    elif cmd == "search-chat" and len(args) >= 2:
        search_chat(args[1])
    elif cmd == "get-messages" and len(args) >= 2:
        page_size = int(args[2]) if len(args) >= 3 else 50
        get_messages(args[1], page_size)
    elif cmd == "send-file" and len(args) >= 3:
        send_file(args[1], args[2])
    else:
        print("未知命令或参数不足")
        print("可用命令: send-user, send-chat, search-user, search-chat, get-messages, send-file")
        sys.exit(1)
