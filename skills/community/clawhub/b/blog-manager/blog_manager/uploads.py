"""File upload management — 4 API operations.

Endpoints:
  POST   /api/upload               upload_file    (multipart: file)
  POST   /api/upload/multiple      upload_files   (multipart: files)
  GET    /api/uploads/list         list_uploads
  DELETE /api/uploads/{filename}   delete_upload
"""

from __future__ import annotations

import os
from typing import Any, List, Tuple
from urllib.parse import quote

from .client import BlogClient

UPLOAD_PATH = "/api/upload"
UPLOADS_PATH = "/api/uploads"


def upload_file(client: BlogClient, file_path: str) -> Tuple[Any, str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    name = os.path.basename(file_path)
    with open(file_path, "rb") as fh:
        files = {"file": (name, fh)}
        return client.post(UPLOAD_PATH, files=files), "upload_single"


def upload_files(client: BlogClient, file_paths: List[str]) -> Tuple[Any, str]:
    opened = []
    try:
        for fp in file_paths:
            if not os.path.isfile(fp):
                raise FileNotFoundError(f"文件不存在: {fp}")
            opened.append(open(fp, "rb"))
        files = [
            ("files", (os.path.basename(fp), fh))
            for fp, fh in zip(file_paths, opened)
        ]
        return client.post(f"{UPLOAD_PATH}/multiple", files=files), "upload_multiple"
    finally:
        for fh in opened:
            fh.close()


def list_uploads(client: BlogClient) -> Tuple[Any, str]:
    return client.get(f"{UPLOADS_PATH}/list"), "uploads_list"


def delete_upload(client: BlogClient, filename: str) -> Tuple[Any, str]:
    encoded = quote(filename)
    return client.delete(f"{UPLOADS_PATH}/{encoded}"), "message_response"
