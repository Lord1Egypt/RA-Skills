from __future__ import annotations

import json
import mimetypes
import socket
import uuid
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import urlencode

from cdf.ai.config import build_common_headers, build_print_url

DEFAULT_TIMEOUT = 120
CVTURL_TIMEOUT = 60
PFS_TIMEOUT = 180


def _post_json(path: str, payload: dict[str, Any], timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """发送 JSON POST 请求并解析响应。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        build_print_url(path),
        data=body,
        headers=build_common_headers("application/json;charset=utf-8"),
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{path} 返回 HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"{path} 调用失败: {exc}") from exc
    return json.loads(raw) if raw else {}


def _post_form(path: str, payload: dict[str, str], timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """发送 form POST 请求并解析响应。"""
    body = urlencode(payload).encode("utf-8")
    req = request.Request(
        build_print_url(path),
        data=body,
        headers=build_common_headers("application/x-www-form-urlencoded;charset=utf-8"),
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{path} 返回 HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"{path} 调用失败: {exc}") from exc
    return json.loads(raw) if raw else {}


def _clean_dict(values: dict[str, Any]) -> dict[str, Any]:
    """删除 None 和空字符串字段。"""
    cleaned: dict[str, Any] = {}
    for key, value in values.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        cleaned[key] = value
    return cleaned


def _extract_string(response: dict[str, Any], key: str) -> str:
    """从常见响应结构中提取字符串字段。"""
    direct = response.get(key)
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    data = response.get("data")
    if isinstance(data, dict):
        nested = data.get(key)
        if isinstance(nested, str) and nested.strip():
            return nested.strip()
    return ""


def _download_binary(url: str, timeout: int = DEFAULT_TIMEOUT) -> bytes:
    """下载云端返回的二进制打印数据。"""
    if not url.strip():
        raise RuntimeError("下载打印数据失败：fileUrl 为空。")
    req = request.Request(
        url.strip(),
        headers=build_common_headers(),
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"下载打印数据返回 HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"下载打印数据失败: {exc}") from exc


def _send_to_printer(host: str, port: int, data: bytes, timeout: float = 60.0) -> int:
    """通过原始 TCP 连接将打印数据发送到打印机。"""
    if not host.strip():
        raise RuntimeError("发送打印数据失败：打印机地址为空。")
    if not data:
        raise RuntimeError("发送打印数据失败：下载到的打印数据为空。")
    try:
        with socket.create_connection((host.strip(), port), timeout=timeout) as conn:
            conn.settimeout(timeout)
            conn.sendall(data)
    except OSError as exc:
        raise RuntimeError(f"发送打印数据到 {host}:{port} 失败: {exc}") from exc
    return len(data)


def _post_multipart_file(path: str, file_path: Path, field_name: str = "file", timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """上传单文件 multipart/form-data 请求并解析响应。"""
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    boundary = f"----cdf-skill-{uuid.uuid4().hex}"
    content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    body = b"".join(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            (
                f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode("utf-8"),
            file_path.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )

    req = request.Request(
        build_print_url(path),
        data=body,
        headers=build_common_headers(f"multipart/form-data; boundary={boundary}"),
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{path} 返回 HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"{path} 调用失败: {exc}") from exc
    return json.loads(raw) if raw else {}


def upload_file_mcp(file_path: Path) -> dict[str, str]:
    """上传文件到云端并返回 url、repoId、path。"""
    response = _post_multipart_file("/openapi/mcpClient/uploadFileMCP", file_path=file_path)
    url = _extract_string(response, "url")
    if not url:
        raise RuntimeError("uploadFileMCP 未返回 url。")
    return {
        "url": url,
        "repoId": _extract_string(response, "repoId"),
        "path": _extract_string(response, "path"),
    }


def convert_url_to_pdf(repo_id: str, path: str) -> str:
    """调用 _cvturl 将已上传文件转换为 PDF URL（JSON body，60s 超时）。"""
    payload = _clean_dict({"repoId": repo_id, "path": path})
    if not payload.get("repoId") or not payload.get("path"):
        raise RuntimeError("_cvturl 需要 repoId 和 path。")
    response = _post_json(
        "/openapi/cdf/_cvturl",
        {key: str(value) for key, value in payload.items()},
        timeout=CVTURL_TIMEOUT,
    )
    url = _extract_string(response, "url")
    if not url:
        raise RuntimeError("_cvturl 未返回 url。")
    return url


PFS_TIMEOUT = 300


def print_for_skill(
    driver: str,
    name: str,
    port_addr: str,
    url: str,
    *,
    port_type: str = "NET",
    raw_port: int = 9100,
    port_serial: str | None = None,
    from_sn: str | None = None,
    file_name: str = "",
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """调用 _pfs 生成可打印数据，并通过 TCP 发送到打印机。"""
    printer = _clean_dict(
        {
            "driver": driver,
            "name": name,
            "portType": port_type,
            "portAddr": port_addr,
            "portSerial": port_serial,
            "fromSn": from_sn,
        }
    )
    payload: dict[str, Any] = {
        "printer": printer,
        "url": url,
        "config": config or {},
    }
    if file_name:
        payload["fileName"] = file_name
    response = _post_json("/openapi/cdf/_pfs", payload, timeout=PFS_TIMEOUT)
    if "success" not in response:
        response["success"] = False
    if "reason" not in response:
        response["reason"] = None
    file_url = _extract_string(response, "fileUrl")
    response["fileUrl"] = file_url or response.get("fileUrl")
    response["cloudSuccess"] = bool(response.get("success"))

    if not response["cloudSuccess"]:
        return response

    if not file_url:
        response["success"] = False
        response["reason"] = response["reason"] or "_pfs 调用成功，但未返回 fileUrl。"
        return response

    data = _download_binary(file_url, timeout=DEFAULT_TIMEOUT)
    bytes_sent = _send_to_printer(port_addr, raw_port, data)
    response["success"] = True
    response["rawPrint"] = {
        "host": port_addr,
        "port": raw_port,
        "bytes": bytes_sent,
    }
    return response
