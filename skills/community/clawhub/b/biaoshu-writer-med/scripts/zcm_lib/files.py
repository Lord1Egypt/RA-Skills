"""File validation helpers shared by zcm commands."""

import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

from .storage import output_dir


MAX_TENDER_MB = 50
MAX_BID_MB = 1024
MAX_DUP_TOTAL_MB = 2048


def is_url(value):
    return value.startswith("http://") or value.startswith("https://")


def _die(message, code=1):
    print(message, file=sys.stderr, flush=True)
    raise SystemExit(code)


def check_size(path, max_mb, label):
    """Validate a local file size, leaving unreadable files to server-side checks."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return
    if size > max_mb * 1024 * 1024:
        _die(
            f"{label}超过大小上限：{size / 1024 / 1024:.1f} MB > {max_mb} MB"
            f"（{os.path.basename(path)}）。请压缩或拆分后重试。"
        )


def check_total_size(paths, max_mb, label):
    """Validate batch upload size; unreadable files are left to server-side checks."""
    total = 0
    for path in paths:
        try:
            total += os.path.getsize(path)
        except OSError:
            return
    if total > max_mb * 1024 * 1024:
        _die(f"{label}总大小超过上限：{total / 1024 / 1024:.1f} MB > {max_mb} MB。请压缩或减少文件后重试。")


def encode_multipart(fields, files):
    """Build a multipart/form-data request body from fields and local files."""
    boundary = "----zcm" + uuid.uuid4().hex
    crlf = b"\r\n"
    buf = bytearray()
    for name, value in (fields or {}).items():
        buf += b"--" + boundary.encode() + crlf
        buf += f'Content-Disposition: form-data; name="{name}"'.encode() + crlf + crlf
        buf += str(value).encode("utf-8") + crlf
    for field_name, filepath in files:
        if not os.path.isfile(filepath):
            _die(f"文件不存在：{filepath}")
        fname = os.path.basename(filepath)
        ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
        with open(filepath, "rb") as f:
            content = f.read()
        buf += b"--" + boundary.encode() + crlf
        buf += (
            f'Content-Disposition: form-data; name="{field_name}"; filename="{fname}"'
        ).encode("utf-8") + crlf
        buf += f"Content-Type: {ctype}".encode() + crlf + crlf
        buf += content + crlf
    buf += b"--" + boundary.encode() + b"--" + crlf
    return bytes(buf), f"multipart/form-data; boundary={boundary}"


def download_to_local(url, max_mb=None):
    """Download a remote file into the skill output directory before upload."""
    parsed = urllib.parse.urlparse(url)
    name = os.path.basename(urllib.parse.unquote(parsed.path)) or "download"
    dest_dir = os.path.join(output_dir(), "_downloads")
    os.makedirs(dest_dir, exist_ok=True)
    local = os.path.join(dest_dir, name)
    req = urllib.request.Request(url, headers={"User-Agent": "zcm-client"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            clen = resp.headers.get("Content-Length") if resp.headers else None
            if max_mb and clen and clen.isdigit() and int(clen) > max_mb * 1024 * 1024:
                _die(f"云端文件超过大小上限：{int(clen) / 1024 / 1024:.1f} MB > {max_mb} MB（{url}）。")
            cd = (resp.headers.get("Content-Disposition", "") if resp.headers else "") or ""
            if "filename=" in cd:
                fn = os.path.basename(urllib.parse.unquote(
                    cd.split("filename=")[-1].split(";")[0].strip().strip('"\'')))
                if fn:
                    local = os.path.join(dest_dir, fn)
            with open(local, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
    except urllib.error.HTTPError as e:
        _die(f"下载云端文件失败 HTTP {e.code}：{url}", code=1)
    except urllib.error.URLError as e:
        _die(f"下载云端文件失败：{e.reason}（{url}）", code=1)
    print(f"已下载云端文件到本地：{local}", file=sys.stderr, flush=True)
    return local
