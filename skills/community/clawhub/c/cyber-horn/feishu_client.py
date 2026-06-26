"""CyberHorn 飞书交互：鉴权、上传音频、发送语音消息。"""
import json
import sys
from pathlib import Path

import requests

AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FILE_UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/files"
MESSAGE_CREATE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token。失败时抛出并打印 API 错误信息。"""
    resp = requests.post(
        AUTH_URL,
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=10,
    )
    data = resp.json()
    code = data.get("code", -1)
    if code != 0:
        msg = data.get("msg", resp.text)
        print(f"[CyberHorn] 飞书鉴权失败 code={code} msg={msg}", file=sys.stderr)
        raise RuntimeError(f"Feishu auth failed: code={code}, msg={msg}")
    token = data.get("tenant_access_token")
    if not token:
        raise RuntimeError("Feishu auth: no tenant_access_token in response")
    return token


def upload_audio(
    token: str,
    opus_path: str | Path,
    *,
    file_name: str | None = None,
    duration_ms: int | None = None,
) -> str:
    """
    上传 Opus 音频，file_type 必须为 opus。返回 file_key。
    """
    opus_path = Path(opus_path)
    if not opus_path.exists():
        raise FileNotFoundError(f"音频文件不存在: {opus_path}")
    name = file_name or opus_path.name
    if not name.lower().endswith(".opus"):
        name = f"{name}.opus" if not name.endswith(".") else name + "opus"

    with open(opus_path, "rb") as f:
        file_content = f.read()

    # multipart/form-data: file_type=opus, file_name, file, 可选 duration
    data = {"file_type": "opus", "file_name": name}
    if duration_ms is not None:
        data["duration"] = str(duration_ms)
    files = {"file": (name, file_content, "audio/opus")}

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        FILE_UPLOAD_URL,
        headers=headers,
        data=data,
        files=files,
        timeout=30,
    )
    result = resp.json()
    code = result.get("code", -1)
    if code != 0:
        msg = result.get("msg", resp.text)
        print(f"[CyberHorn] 飞书上传失败 code={code} msg={msg}", file=sys.stderr)
        raise RuntimeError(f"Feishu upload failed: code={code}, msg={msg}")

    body = result.get("data", {})
    file_key = body.get("file_key")
    if not file_key:
        raise RuntimeError("Feishu upload: response has no file_key")
    return file_key


def send_audio_message(
    token: str,
    receive_id: str,
    file_key: str,
    *,
    receive_id_type: str = "chat_id",
) -> dict:
    """
    发送语音消息。receive_id 即 chat_id（或 user_id 等，由 receive_id_type 决定）。
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    content = json.dumps({"file_key": file_key})
    params = {"receive_id_type": receive_id_type}
    payload = {"receive_id": receive_id, "msg_type": "audio", "content": content}

    resp = requests.post(
        MESSAGE_CREATE_URL,
        params=params,
        headers=headers,
        json=payload,
        timeout=10,
    )
    result = resp.json()
    code = result.get("code", -1)
    if code != 0:
        msg = result.get("msg", resp.text)
        print(f"[CyberHorn] 飞书发消息失败 code={code} msg={msg}", file=sys.stderr)
        raise RuntimeError(f"Feishu send message failed: code={code}, msg={msg}")
    return result
