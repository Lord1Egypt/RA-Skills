"""File validation helpers shared by zcm commands."""

import mimetypes
import os
import sys
import uuid


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
