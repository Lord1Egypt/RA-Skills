#!/usr/bin/env python3
"""Focused eKYC Suite Face Compare cloud client."""

import argparse
import base64
import io
import json
import os
import platform
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

CLIENT_VERSION = "1.0.18"
MAX_RAW_BYTES = 20 * 1024 * 1024

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def cloud_config():
    endpoint = os.environ.get("EKYC_CLOUD_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("EKYC_CLOUD_API_KEY", "")
    if not endpoint or not api_key:
        raise RuntimeError("Set EKYC_CLOUD_ENDPOINT and EKYC_CLOUD_API_KEY before using this skill.")
    parsed = urlparse(endpoint)
    if parsed.scheme.lower() != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise RuntimeError("EKYC_CLOUD_ENDPOINT must be a valid HTTPS URL without embedded credentials.")
    return endpoint, api_key


def media_input(value):
    path = Path(value)
    if path.is_file():
        size = path.stat().st_size
        if size > MAX_RAW_BYTES:
            raise ValueError("File exceeds the 20MB limit.")
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    if value.startswith("http://"):
        raise ValueError("Only public HTTPS URLs are accepted.")
    return value


def call_cloud(photo1, photo2, source_photo_type):
    endpoint, api_key = cloud_config()
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "user-agent": f"ekyc-suite-face-compare-skill/{CLIENT_VERSION}",
        "x-ekyc-client": "clawhub-skill-face-compare",
        "x-ekyc-version": CLIENT_VERSION,
        "x-ekyc-runtime": f"python/{platform.python_version()} {platform.system()}",
        "x-ekyc-transport": "cli",
    }
    optional = {
        "x-ekyc-source-site": os.environ.get("EKYC_SOURCE_SITE") or os.environ.get("EKYC_SITE"),
        "x-ekyc-source-channel": os.environ.get("EKYC_SOURCE_CHANNEL"),
        "x-ekyc-client-name": os.environ.get("EKYC_CLIENT_NAME"),
        "x-ekyc-client-id": os.environ.get("EKYC_CLIENT_ID"),
        "x-ekyc-workspace": os.environ.get("EKYC_WORKSPACE"),
        "x-ekyc-install-id": os.environ.get("EKYC_INSTALL_ID"),
    }
    headers.update({key: value for key, value in optional.items() if value})
    response = requests.post(
        f"{endpoint}/api/v1/tools/face_compare",
        json={
            "photo1": media_input(photo1),
            "photo2": media_input(photo2),
            "sourcePhotoType": source_photo_type,
        },
        headers=headers,
        timeout=120,
    )
    try:
        data = response.json()
    except ValueError:
        data = {"success": False, "error": f"Cloud backend returned non-JSON data (HTTP {response.status_code})."}
    trace_id = response.headers.get("x-ekyc-trace-id")
    if trace_id and isinstance(data, dict) and "traceId" not in data:
        data["traceId"] = trace_id
    return data


def main():
    parser = argparse.ArgumentParser(description="eKYC Suite Face Compare")
    parser.add_argument("--photo1", required=True)
    parser.add_argument("--photo2", required=True)
    parser.add_argument("--source-photo-type", choices=["1", "2"], default="2")
    args = parser.parse_args()
    try:
        result = call_cloud(args.photo1, args.photo2, args.source_photo_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if isinstance(result, dict) and result.get("success") is False:
            sys.exit(2)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
