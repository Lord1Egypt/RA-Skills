#!/usr/bin/env python3
"""Upload a file or folder through ARKCloud's IPFS upload API."""

from __future__ import annotations

import argparse
import mimetypes
import os
import uuid
from pathlib import Path

from arkcloud_common import base_url, endpoint, fail, print_json, request_json, require_env


def form_filename(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "_").replace("\n", "_")


def multipart_file(field: str, path: Path) -> tuple[bytes, str]:
    boundary = f"----arkcloud-{uuid.uuid4().hex}"
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{form_filename(path.name)}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return head + path.read_bytes() + tail, f"multipart/form-data; boundary={boundary}"


def multipart_folder(root: Path) -> tuple[bytes, str]:
    boundary = f"----arkcloud-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    chunks.append(
        (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="display_name"\r\n\r\n'
            f"{root.name}\r\n"
        ).encode("utf-8")
    )
    files = sorted(p for p in root.rglob("*") if p.is_file())
    if not files:
        fail(f"Folder has no files to upload: {root}")
    for path in files:
        rel = path.relative_to(root).as_posix()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="files"; filename="{form_filename(rel)}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode("utf-8")
        )
        chunks.append(path.read_bytes())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def normalize_result(payload: dict, root: str) -> dict:
    result = {"ok": True, **payload}
    short_url = payload.get("short_url") or payload.get("cid_url")
    if isinstance(short_url, str) and short_url:
        result["short_url"] = short_url
        result["url"] = short_url if short_url.startswith("http") else root.rstrip("/") + short_url
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a file or folder to ARKCloud IPFS.")
    parser.add_argument("path", help="File or folder path to upload")
    parser.add_argument("--folder", action="store_true", help="Upload a folder through the client API")
    parser.add_argument("--base-url", default=None, help="ARKCloud base URL")
    args = parser.parse_args()

    root = base_url(args.base_url)
    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        fail(f"Path does not exist: {target}")

    if args.folder or target.is_dir():
        if not target.is_dir():
            fail("--folder requires a directory path")
        cookie = require_env(
            "ARKCLOUD_CLIENT_COOKIE",
            "Folder upload requires ARKCLOUD_CLIENT_COOKIE and ARKCLOUD_CSRF_TOKEN, "
            "or use the ARKCloud web UI at https://file.arklink.hk/",
        )
        csrf = require_env(
            "ARKCLOUD_CSRF_TOKEN",
            "Folder upload requires ARKCLOUD_CLIENT_COOKIE and ARKCLOUD_CSRF_TOKEN, "
            "or use the ARKCloud web UI at https://file.arklink.hk/",
        )
        body, content_type = multipart_folder(target)
        payload = request_json(
            "POST",
            endpoint(root, "/api/client/upload/folder"),
            headers={
                "Cookie": cookie,
                "X-CSRF-Token": csrf,
                "Content-Type": content_type,
            },
            body=body,
        )
        print_json(normalize_result(payload, root))
        return

    token = require_env("ARKCLOUD_UPLOAD_TOKEN")
    body, content_type = multipart_file("file", target)
    payload = request_json(
        "POST",
        endpoint(root, "/api/upload"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
        body=body,
    )
    print_json(normalize_result(payload, root))


if __name__ == "__main__":
    main()
