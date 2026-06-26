#!/usr/bin/env python3
"""
飞书发送媒体文件（图片/视频）
支持本地文件或 CDN URL，自动优先上传到飞书发送，失败时返回 CDN 链接。

重要：receive_id_type 说明
- open_id  ：发送给单个用户
- chat_id  ：发送到群聊
- 使用场景：
    • 个人聊天 → open_id（用户 open_id 格式：ou_xxx）
    • 群聊     → chat_id（群 ID 格式：oc_xxx）
"""
import requests
import json
import sys
import os

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
API_BASE = "https://open.feishu.cn/open-apis"


def _get_feishu_creds() -> tuple:
    app_id = os.environ.get("FEISHU_APP_ID", FEISHU_APP_ID)
    app_secret = os.environ.get("FEESHU_APP_SECRET", FEISHU_APP_SECRET)
    if not app_id or not app_secret:
        raise EnvironmentError("请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
    return app_id, app_secret


def get_token() -> str:
    """获取 tenant access token"""
    app_id, app_secret = _get_feishu_creds()
    resp = requests.post(
        f"{API_BASE}/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret}
    )
    resp.raise_for_status()
    return resp.json()["tenant_access_token"]


def download_file(url: str) -> bytes:
    """从 CDN URL 下载文件"""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content


def upload_image(token: str, content: bytes, filename: str = "image.jpg") -> str:
    """上传图片到飞书，返回 image_key"""
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime = mime_types.get(ext, "image/jpeg")
    resp = requests.post(
        f"{API_BASE}/im/v1/images",
        files={"image": (filename, content, mime)},
        data={"image_type": "message"},
        headers={"Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    return resp.json()["data"]["image_key"]


def upload_video(token: str, content: bytes, filename: str = "video.mp4") -> str:
    """上传视频到飞书，返回 file_key（注意：视频用 /im/v1/files 接口）"""
    resp = requests.post(
        f"{API_BASE}/im/v1/files",
        files={"file": (filename, content, "video/mp4")},
        data={"file_type": "mp4"},
        headers={"Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    return resp.json()["data"]["file_key"]


def send_image_message(token: str, receive_id: str, image_key: str,
                       receive_id_type: str = "open_id") -> dict:
    """
    发送图片消息

    参数:
        token: 飞书 tenant access token
        receive_id: 接收方 ID（open_id 或 chat_id，取决于 receive_id_type）
        image_key: 上传后的图片 key
        receive_id_type: "open_id"（用户）或 "chat_id"（群聊），默认 open_id
    """
    resp = requests.post(
        f"{API_BASE}/im/v1/messages",
        params={"receive_id_type": receive_id_type},
        json={
            "receive_id": receive_id,
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key})
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    return resp.json()


def send_video_message(token: str, receive_id: str, file_key: str,
                      receive_id_type: str = "open_id") -> dict:
    """
    发送视频消息

    参数:
        token: 飞书 tenant access token
        receive_id: 接收方 ID（open_id 或 chat_id，取决于 receive_id_type）
        file_key: 上传后的视频 file key
        receive_id_type: "open_id"（用户）或 "chat_id"（群聊），默认 open_id
    """
    resp = requests.post(
        f"{API_BASE}/im/v1/messages",
        params={"receive_id_type": receive_id_type},
        json={
            "receive_id": receive_id,
            "msg_type": "media",
            "content": json.dumps({"file_key": file_key, "type": "video"})
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    return resp.json()


def _read_local_file(path: str) -> bytes:
    """读取本地文件，限制只允许 /tmp/ 目录"""
    abs_path = os.path.realpath(path)
    if not abs_path.startswith("/tmp/"):
        raise ValueError(f"本地文件路径必须在 /tmp/ 目录下，拒绝访问: {path}")
    with open(abs_path, "rb") as f:
        return f.read()


def send_image(token: str, receive_id: str, source: str,
               receive_id_type: str = "open_id") -> dict:
    """
    发送图片：优先上传飞书发送，失败返回 CDN 链接

    参数:
        token: 飞书 token（传 None 则自动获取）
        receive_id: 接收方 ID（open_id 或 chat_id）
        source: /tmp/ 下的本地文件路径 或 CDN URL
        receive_id_type: "open_id" 或 "chat_id"，默认 open_id
            - open_id：发送给你用户，例如 ou_xxx
            - chat_id ：发送到群聊，例如 oc_xxx
    """
    if token is None:
        token = get_token()
    try:
        if source.startswith("http://") or source.startswith("https://"):
            content = download_file(source)
        else:
            content = _read_local_file(source)

        filename = os.path.basename(source) if not source.startswith("http") else "image.jpg"
        image_key = upload_image(token, content, filename)
        result = send_image_message(token, receive_id, image_key, receive_id_type)
        return {
            "success": True,
            "method": "feishu",
            "image_key": image_key,
            "receive_id_type": receive_id_type,
            "result": result
        }
    except requests.exceptions.HTTPError as e:
        # 尝试解析飞书错误码，给出更友好的提示
        try:
            err_body = e.response.json()
            code = err_body.get("code")
            msg = err_body.get("msg", "")
            err_msg = f"飞书错误码 {code}: {msg}"
            # 常见错误码说明
            if code == 230001:
                err_msg += "（请检查是否已开通 im:resource 权限）"
            elif code == 99991663:
                err_msg += "（tenant_access_token 已过期，请重新获取）"
        except Exception:
            err_msg = str(e)
        return {
            "success": False,
            "method": "cdn",
            "cdn_url": source if source.startswith("http") else None,
            "error": err_msg,
            "http_status": e.response.status_code if e.response is not None else None
        }
    except Exception as e:
        return {
            "success": False,
            "method": "cdn",
            "cdn_url": source if source.startswith("http") else None,
            "error": str(e)
        }


def send_video(token: str, receive_id: str, source: str,
               receive_id_type: str = "open_id") -> dict:
    """
    发送视频：优先上传飞书发送，失败返回 CDN 链接

    参数:
        token: 飞书 token（传 None 则自动获取）
        receive_id: 接收方 ID（open_id 或 chat_id）
        source: /tmp/ 下的本地文件路径 或 CDN URL
        receive_id_type: "open_id" 或 "chat_id"，默认 open_id
    """
    if token is None:
        token = get_token()
    try:
        if source.startswith("http://") or source.startswith("https://"):
            content = download_file(source)
        else:
            content = _read_local_file(source)

        file_key = upload_video(token, content)
        result = send_video_message(token, receive_id, file_key, receive_id_type)
        return {
            "success": True,
            "method": "feishu",
            "file_key": file_key,
            "receive_id_type": receive_id_type,
            "result": result
        }
    except requests.exceptions.HTTPError as e:
        try:
            err_body = e.response.json()
            code = err_body.get("code")
            msg = err_body.get("msg", "")
            err_msg = f"飞书错误码 {code}: {msg}"
        except Exception:
            err_msg = str(e)
        return {
            "success": False,
            "method": "cdn",
            "cdn_url": source if source.startswith("http") else None,
            "error": err_msg,
            "http_status": e.response.status_code if e.response is not None else None
        }
    except Exception as e:
        return {
            "success": False,
            "method": "cdn",
            "cdn_url": source if source.startswith("http") else None,
            "error": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法:")
        print("  python3 send_feishu.py image <receive_id> <file_or_url> [receive_id_type]")
        print("  python3 send_feishu.py video <receive_id> <file_or_url> [receive_id_type]")
        print("")
        print("参数说明:")
        print("  receive_id      - 接收方 ID（open_id: ou_xxx 或 chat_id: oc_xxx）")
        print("  receive_id_type  - 可选，默认 open_id。发送到群聊时指定 chat_id")
        print("")
        print("示例:")
        print("  # 发送给用户（默认 open_id）")
        print("  python3 send_feishu.py image ou_xxxxxxxx /tmp/a.jpg")
        print("")
        print("  # 发送到群聊")
        print("  python3 send_feishu.py image oc_xxxxxxxx /tmp/a.jpg chat_id")
        sys.exit(1)

    action = sys.argv[1]
    receive_id = sys.argv[2]
    source = sys.argv[3]
    receive_id_type = sys.argv[4] if len(sys.argv) > 4 else "open_id"

    if receive_id_type not in ("open_id", "chat_id"):
        print(f"receive_id_type 必须是 open_id 或 chat_id，当前值: {receive_id_type}")
        sys.exit(1)

    token = get_token()

    if action == "image":
        result = send_image(token, receive_id, source, receive_id_type)
    elif action == "video":
        result = send_video(token, receive_id, source, receive_id_type)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
