"""COS upload via STS temporary credentials from Leewow backend."""

import os
import time
import uuid
from typing import Optional

import requests
from qcloud_cos import CosConfig, CosS3Client

LEEWOW_API_BASE = os.getenv("LEEWOW_API_BASE", "https://leewow.com")
STS_ENDPOINT = "/v2/api/public/cos/sts/credentials"

_sts_cache: Optional[dict] = None
_sts_expires_at: float = 0
_STS_REFRESH_BUFFER_S = 120


def _fetch_sts_credentials() -> dict:
    global _sts_cache, _sts_expires_at
    now = time.time()
    if _sts_cache and now < _sts_expires_at:
        return _sts_cache

    url = LEEWOW_API_BASE + STS_ENDPOINT
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("tmpSecretId"):
        raise RuntimeError(f"Invalid STS response: {data}")

    _sts_cache = data
    _sts_expires_at = int(data.get("expiredTime", 0)) - _STS_REFRESH_BUFFER_S
    return data


def _get_cos_client() -> tuple:
    sts = _fetch_sts_credentials()
    config = CosConfig(
        Region=sts["region"],
        SecretId=sts["tmpSecretId"],
        SecretKey=sts["tmpSecretKey"],
        Token=sts["sessionToken"],
    )
    return CosS3Client(config), sts["bucket"], sts["region"]


def upload_file_to_cos(file_path: str, key_prefix: str = "claw-upload") -> str:
    ext = os.path.splitext(file_path)[1] or ".jpg"
    key = f"{key_prefix}/{uuid.uuid4().hex}{ext}"
    client, bucket, region = _get_cos_client()
    content_type = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp",
    }.get(ext.lower(), "application/octet-stream")

    with open(file_path, "rb") as fp:
        client.put_object(Bucket=bucket, Body=fp, Key=key, ContentType=content_type)

    return f"https://{bucket}.cos.{region}.myqcloud.com/{key}"
