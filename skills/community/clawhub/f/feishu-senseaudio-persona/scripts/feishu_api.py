from __future__ import annotations

import importlib
import json
import mimetypes
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


def ensure_python_package(import_name: str, pip_name: str | None = None) -> None:
    pip_name = pip_name or import_name
    try:
        importlib.import_module(import_name)
        return
    except ImportError:
        pass

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"缺少 Python 依赖 {pip_name}，自动安装失败。\n"
            f"请手动执行: {sys.executable} -m pip install {pip_name}\n"
            f"stderr:\n{result.stderr}"
        )


def _requests_module():
    ensure_python_package("requests")
    return importlib.import_module("requests")


def get_tenant_access_token() -> str:
    requests = _requests_module()

    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError("缺少 FEISHU_APP_ID 或 FEISHU_APP_SECRET")

    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("code") != 0:
        raise RuntimeError(f"获取飞书 tenant_access_token 失败: {json.dumps(payload, ensure_ascii=False)}")
    return payload["tenant_access_token"]


def upload_opus_file(opus_path: str, file_name: str = "reply.opus") -> Dict[str, Any]:
    requests = _requests_module()
    token = get_tenant_access_token()
    path = Path(opus_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"找不到 OPUS 文件: {path}")

    headers = {"Authorization": f"Bearer {token}"}
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    with path.open("rb") as f:
        files = {
            "file": (file_name, f, content_type),
        }
        data = {"file_type": "opus", "file_name": file_name}
        resp = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/files",
            headers=headers,
            data=data,
            files=files,
            timeout=120,
        )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("code") != 0:
        raise RuntimeError(f"上传飞书 OPUS 文件失败: {json.dumps(payload, ensure_ascii=False)}")
    file_key = payload.get("data", {}).get("file_key")
    if not file_key:
        raise RuntimeError(f"上传返回中缺少 file_key: {json.dumps(payload, ensure_ascii=False)}")
    return {"file_key": file_key, "raw": payload}


def send_audio_message(chat_id: str, file_key: str) -> Dict[str, Any]:
    requests = _requests_module()
    token = get_tenant_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    body = {
        "receive_id": chat_id,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key}, ensure_ascii=False),
    }
    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        headers=headers,
        json=body,
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("code") != 0:
        raise RuntimeError(f"发送飞书语音消息失败: {json.dumps(payload, ensure_ascii=False)}")
    return payload
