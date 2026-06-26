#!/usr/bin/env python3
"""
Upload a binary file to the Dr. Binary sandbox.

Usage:
    python upload.py <file_path>

Output:
    Remote sandbox path, e.g. /sandbox/abc123.exe

Environment:
    DRBINARY_API_KEY — drbinary.ai → Settings → Billing → API Key
"""

import os
import sys
import json
import urllib.request
import mimetypes
from pathlib import Path


UPLOAD_URL = "https://mcp.deepbits.com/workspace/upload"


def load_env() -> None:
    env_file = Path(__file__).parent.parent.parent / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def upload(file_path: str) -> str:
    api_key = os.environ.get("DRBINARY_API_KEY", "")
    if not api_key:
        sys.exit("error: DRBINARY_API_KEY is not set")
    if not os.path.isfile(file_path):
        sys.exit(f"error: file not found: {file_path}")

    filename = os.path.basename(file_path)
    boundary = "----DrBinaryUpload"

    with open(file_path, "rb") as f:
        file_data = f.read()

    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        UPLOAD_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "curl/7.88.1",
        },
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())

    return f"/sandbox/{result['pathname']}"


if __name__ == "__main__":
    load_env()
    if len(sys.argv) < 2:
        sys.exit("usage: upload.py <file_path>")
    print(upload(sys.argv[1]))
