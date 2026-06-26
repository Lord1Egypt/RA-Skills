#!/usr/bin/env python3
import os
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import oss2

import os
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from env import get_oss_config


def _normalize_endpoint(endpoint: str) -> str:
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        return endpoint
    return f"https://{endpoint}"


def _build_public_url(endpoint: str, bucket: str, key: str) -> str:
    endpoint = _normalize_endpoint(endpoint)
    parsed = urlparse(endpoint)
    host = parsed.netloc
    scheme = parsed.scheme or "https"
    if host.startswith(f"{bucket}."):
        return f"{scheme}://{host}/{key}"
    return f"{scheme}://{bucket}.{host}/{key}"


def upload_image(image_path: Path, object_key: Optional[str] = None) -> str:
    cfg = get_oss_config()
    access_key = cfg["access_key"]
    secret_key = cfg["secret_key"]
    bucket_name = cfg["bucket"]
    endpoint = cfg["endpoint"]

    image_path = Path(image_path)
    if not image_path.exists():
        raise RuntimeError(f"Image not found: {image_path}")

    suffix = image_path.suffix or ".png"
    object_key = object_key or f"bailian-studio/{int(time.time())}-{image_path.stem}{suffix}"

    auth = oss2.Auth(access_key, secret_key)
    bucket = oss2.Bucket(auth, _normalize_endpoint(endpoint), bucket_name)
    bucket.put_object_from_file(object_key, str(image_path))

    return _build_public_url(endpoint, bucket_name, object_key)
