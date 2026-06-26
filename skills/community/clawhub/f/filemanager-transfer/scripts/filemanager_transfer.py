#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import re
import socket
import sys
import uuid
from pathlib import Path
from urllib import error, parse, request

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_PATH = SCRIPT_DIR / ".env"


class FriendlyError(Exception):
    pass


def fail(message):
    raise FriendlyError(message)


def load_env():
    values = {}
    if ENV_PATH.exists():
        try:
            lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            fail(f"无法读取配置文件：{ENV_PATH}\n原因：{exc}")
        for index, raw in enumerate(lines, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                fail(f"配置文件格式错误：{ENV_PATH} 第 {index} 行缺少等号")
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    values.update({k: v for k, v in os.environ.items() if k.startswith("FILEMANAGER_")})
    return values


def config():
    env = load_env()
    base_url = env.get("FILEMANAGER_BASE_URL", "").rstrip("/")
    appkey = env.get("FILEMANAGER_APPKEY", "")
    if not base_url:
        fail(f"缺少 FILEMANAGER_BASE_URL，请在 {ENV_PATH} 中配置")
    if not appkey:
        fail(f"缺少 FILEMANAGER_APPKEY，请在 {ENV_PATH} 中配置")
    parsed = parse.urlparse(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        fail("FILEMANAGER_BASE_URL 格式不正确，应类似：http://localhost:8080")
    return base_url, appkey


def parse_http_error(exc):
    detail = exc.read().decode("utf-8", errors="replace").strip()
    message = detail
    try:
        payload = json.loads(detail)
        if isinstance(payload, dict):
            message = payload.get("error") or payload.get("message") or detail
    except json.JSONDecodeError:
        pass
    hints = {
        400: "请求参数不正确，请检查文件、远程目录、分享密码或备注。",
        401: "认证失败，请检查 scripts/.env 中的 FILEMANAGER_APPKEY 是否正确。",
        403: "权限不足，当前 AppKey 不允许执行该操作。",
        404: "接口、远程目录或文件 ID 不存在。上传时请确认远程目录已存在；下载时请确认文件 ID 正确。",
        413: "文件超过服务端允许的上传大小。",
        500: "服务端内部错误，请查看 FileManager 服务端日志。",
    }
    hint = hints.get(exc.code, "请检查 FileManager 服务端状态和请求参数。")
    return f"FileManager API 返回错误：HTTP {exc.code}\n原因：{message}\n建议：{hint}"


def parse_url_error(exc, url):
    reason = exc.reason
    parsed = parse.urlparse(url)
    target = parsed.netloc or url
    if isinstance(reason, ConnectionRefusedError):
        return f"无法连接 FileManager 服务：{target}\n原因：目标主机拒绝连接。\n建议：确认 FileManager 程序已经启动，并检查 FILEMANAGER_BASE_URL 的地址和端口是否正确。"
    if isinstance(reason, TimeoutError) or "timed out" in str(reason).lower():
        return f"连接 FileManager 超时：{target}\n建议：确认服务可访问，网络正常，或稍后重试。"
    if isinstance(reason, socket.gaierror):
        return f"无法解析 FileManager 主机名：{target}\n建议：检查 FILEMANAGER_BASE_URL 中的域名或 IP 是否正确。"
    return f"无法访问 FileManager API：{target}\n原因：{reason}\n建议：确认服务已启动、地址端口正确、网络可达。"


def request_api(method, url, appkey, body=None, headers=None):
    req = request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {appkey}")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        return request.urlopen(req, timeout=120)
    except error.HTTPError as exc:
        fail(parse_http_error(exc))
    except error.URLError as exc:
        fail(parse_url_error(exc, url))
    except OSError as exc:
        fail(f"请求 FileManager API 失败。\n原因：{exc}\n建议：确认网络、地址和端口配置正确。")


def request_json(method, url, appkey, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    resp = request_api(method, url, appkey, body=body, headers={"Content-Type": "application/json"})
    text = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail(f"FileManager API 返回的 JSON 无法解析。\n响应内容：{text}")


def multipart_body(file_path, remark=""):
    boundary = "----filemanager-" + uuid.uuid4().hex
    path = Path(file_path)
    filename = path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    try:
        data = path.read_bytes()
    except OSError as exc:
        fail(f"无法读取待上传文件：{path}\n原因：{exc}")
    parts = []
    if remark:
        parts.extend([
            f"--{boundary}\r\n".encode(),
            b'Content-Disposition: form-data; name="remark"\r\n\r\n',
            remark.encode("utf-8"),
            b"\r\n",
        ])
    parts.extend([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"),
        f"Content-Type: {content_type}\r\n\r\n".encode(),
        data,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return b"".join(parts), boundary


def upload_file(base_url, appkey, file_path, remote_dir, remark):
    query = parse.urlencode({"path": remote_dir})
    body, boundary = multipart_body(file_path, remark)
    resp = request_api(
        "POST",
        f"{base_url}/api/files/upload?{query}",
        appkey,
        body=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    text = resp.read().decode("utf-8", errors="replace")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        fail(f"上传接口返回的 JSON 无法解析。\n响应内容：{text}")
    uploaded = payload.get("uploaded")
    if not isinstance(uploaded, list) or not uploaded:
        fail(f"上传接口没有返回文件信息。\n响应内容：{text}")
    return uploaded[0]


def validate_local_file(value):
    file_path = Path(value)
    if not file_path.exists():
        fail(f"文件不存在：{file_path}")
    if not file_path.is_file():
        fail(f"上传路径不是文件：{file_path}")
    return file_path


def create_share(base_url, appkey, file_id, password, expires_hours, max_downloads):
    if not password or not password.strip():
        fail("分享密码不能为空。请使用 --password 设置非空密码。")
    payload = {"file_id": file_id, "password": password.strip(), "expires_hours": expires_hours}
    if max_downloads is not None:
        payload["max_downloads"] = max_downloads
    return request_json("POST", f"{base_url}/api/share", appkey, payload)


def absolute_share_url(base_url, share_url):
    if share_url.startswith("http://") or share_url.startswith("https://"):
        return share_url
    return base_url + "/" + share_url.lstrip("/")


def upload(args):
    base_url, appkey = config()
    file_path = validate_local_file(args.file)
    uploaded = upload_file(base_url, appkey, file_path, args.remote_dir, args.remark)
    result = {"uploaded": uploaded}
    if not args.no_share:
        share = create_share(base_url, appkey, uploaded.get("id", ""), args.password, args.expires_hours, args.max_downloads)
        result["share"] = {
            "url": absolute_share_url(base_url, share.get("share_url", "")),
            "password": args.password.strip(),
            "expires_at": share.get("expires_at"),
            "share_id": share.get("share_id"),
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def filename_from_content_disposition(value):
    if not value:
        return None
    match = re.search(r"filename\*=UTF-8''([^;]+)", value)
    if match:
        return parse.unquote(match.group(1))
    match = re.search(r'filename="?([^";]+)"?', value)
    return match.group(1) if match else None


def download(args):
    base_url, appkey = config()
    url = f"{base_url}/api/files/download/{parse.quote(args.file_id, safe='')}"
    resp = request_api("GET", url, appkey)
    output = Path(args.output) if args.output else None
    if output is None:
        name = filename_from_content_disposition(resp.headers.get("Content-Disposition")) or args.file_id
        output = Path.cwd() / name
    elif output.exists() and output.is_dir():
        name = filename_from_content_disposition(resp.headers.get("Content-Disposition")) or args.file_id
        output = output / name
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(resp.read())
    except OSError as exc:
        fail(f"无法写入下载文件：{output}\n原因：{exc}\n建议：检查输出路径是否有效，以及是否有写入权限。")
    print(str(output))


def main():
    parser = argparse.ArgumentParser(description="通过 FileManager API 上传、创建密码分享或下载文件。")
    sub = parser.add_subparsers(dest="command", required=True)

    up = sub.add_parser("upload", help="上传本地文件，并默认自动创建带密码的分享")
    up.add_argument("file", help="要上传的本地文件路径")
    up.add_argument("--remote-dir", default="/", help="远程目录，默认：/")
    up.add_argument("--remark", default="", help="文件备注，可选")
    up.add_argument("--password", required=True, help="分享密码，必填且不能为空")
    up.add_argument("--expires-hours", type=int, default=24, help="分享有效小时数，默认 24，服务端最多 168")
    up.add_argument("--max-downloads", type=int, help="最大下载次数，可选")
    up.add_argument("--no-share", action="store_true", help="只上传，不创建分享。一般不要使用，除非明确不需要分享")
    up.set_defaults(func=upload)

    down = sub.add_parser("download", help="按 FileManager 文件 ID 下载文件")
    down.add_argument("file_id", help="FileManager 文件 ID")
    down.add_argument("--output", "-o", help="输出文件或目录")
    down.set_defaults(func=download)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except FriendlyError as exc:
        print(f"脚本无法继续执行：\n{exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("脚本已被用户中断。", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"脚本发生未预期错误，但已隐藏 Python traceback。\n原因：{exc}\n建议：检查参数、配置文件和 FileManager 服务状态；如果仍无法解决，请把这段错误信息反馈给维护者。", file=sys.stderr)
        sys.exit(1)
