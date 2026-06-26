"""蝉镜通用文件上传：create_upload_url、PUT、file_detail 轮询。"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE = os.environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")


def get_chanjing_file_detail(token: str, file_id: str) -> tuple[Any | None, str | None]:
    """GET file_detail；API 业务错误返回 (None, msg)，网络异常向上抛出。"""
    url = f"{API_BASE}/open/v1/common/file_detail?id={urllib.parse.quote(file_id)}"
    req = urllib.request.Request(url, headers={"access_token": token}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if body.get("code") != 0:
        return None, str(body.get("msg", "file_detail failed"))
    return body.get("data"), None


def poll_chanjing_file_until_ready(
    token: str,
    file_id: str,
    *,
    interval: float = 5.0,
    timeout: float = 300.0,
    ready_statuses: set[Any],
    failed_statuses: set[Any] | None = None,
    pending_statuses: set[Any] | None = None,
) -> tuple[bool, str | None]:
    """
    pending_statuses 非 None 时：仅这些状态视为处理中；其余非 ready 视为失败（定制数字人）。
    pending_statuses 为 None 时：非 ready 且非 failed_statuses 则继续等待（视频合成上传）。
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        data, err = get_chanjing_file_detail(token, file_id)
        if err:
            return False, err
        if data is None:
            return False, "no data"

        status = data.get("status")
        if status in ready_statuses:
            return True, None
        if failed_statuses is not None and status in failed_statuses:
            return False, data.get("msg") or f"file status={status}"
        if pending_statuses is not None:
            if status not in pending_statuses:
                return False, data.get("msg") or f"unexpected file status={status}"
        time.sleep(interval)
    return False, "poll timeout"


def fetch_create_upload_url_payload(
    token: str, service: str, name: str
) -> tuple[dict[str, Any] | None, str | None]:
    """GET create_upload_url；成功返回 (data 字段内容, None)。"""
    qs = urllib.parse.urlencode({"service": service, "name": name})
    url = f"{API_BASE}/open/v1/common/create_upload_url?{qs}"
    req = urllib.request.Request(url, headers={"access_token": token}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if body.get("code") != 0:
        return None, str(body.get("msg", body))
    data = body.get("data", {})
    if not isinstance(data, dict):
        return None, "invalid create_upload_url data"
    return data, None


def put_file_to_sign_url(sign_url: str, content: bytes, mime_type: str) -> tuple[bool, str | None]:
    put_req = urllib.request.Request(
        sign_url,
        data=content,
        headers={"Content-Type": mime_type},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(put_req, timeout=120) as put_resp:
            if put_resp.status not in (200, 204):
                return False, f"上传返回状态: {put_resp.status}"
    except Exception as exc:
        return False, f"上传失败: {exc}"
    return True, None


def upload_local_file_via_chanjing(
    token: str,
    local_path: Path,
    service: str,
    *,
    poll_interval: float = 5.0,
    poll_timeout: float = 300.0,
    ready_statuses: set[Any],
    failed_statuses: set[Any] | None = None,
    pending_statuses: set[Any] | None = None,
) -> tuple[str | None, str | None]:
    """
    完整上传链路。成功返回 (file_id, None)，失败返回 (None, error_message)。
    """
    if not local_path.is_file():
        return None, f"文件不存在: {local_path}"

    payload, err = fetch_create_upload_url_payload(token, service, local_path.name)
    if err:
        return None, err

    sign_url = payload.get("sign_url")
    mime_type = payload.get("mime_type", "application/octet-stream")
    file_id = payload.get("file_id")
    if not sign_url or not file_id:
        return None, "响应缺少 sign_url 或 file_id"

    content = local_path.read_bytes()
    ok, put_err = put_file_to_sign_url(sign_url, content, mime_type)
    if not ok:
        return None, put_err or "上传失败"

    ready, poll_err = poll_chanjing_file_until_ready(
        token,
        file_id,
        interval=poll_interval,
        timeout=poll_timeout,
        ready_statuses=ready_statuses,
        failed_statuses=failed_statuses,
        pending_statuses=pending_statuses,
    )
    if not ready:
        return None, poll_err or "文件未就绪"

    return str(file_id), None
