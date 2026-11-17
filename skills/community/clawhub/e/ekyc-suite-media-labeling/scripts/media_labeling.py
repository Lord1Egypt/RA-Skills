#!/usr/bin/env python3
"""Focused eKYC Suite Media Labeling cloud client."""

import argparse
import base64
import io
import json
import os
import platform
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

CLIENT_VERSION = "1.0.18"
MAX_RAW_BYTES = 20 * 1024 * 1024
LABEL_PATTERN = re.compile(r"^[AB][0-9]{2}(,[AB][0-9]{2}){0,4}$")

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
        if path.stat().st_size > MAX_RAW_BYTES:
            raise ValueError("File exceeds the 20MB limit.")
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    if value.startswith("http://"):
        raise ValueError("Only public HTTPS URLs are accepted.")
    return value


def call_cloud(file_input, labels, file_type):
    if not LABEL_PATTERN.fullmatch(labels):
        raise ValueError("Use 1-5 comma-separated label codes such as A02,A14.")
    endpoint, api_key = cloud_config()
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "user-agent": f"ekyc-suite-media-labeling-skill/{CLIENT_VERSION}",
        "x-ekyc-client": "clawhub-skill-media-labeling",
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
        f"{endpoint}/api/v1/tools/media_labeling",
        json={
            "file": media_input(file_input),
            "labels": labels,
            "type": file_type,
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
    parser = argparse.ArgumentParser(description="eKYC Suite Media Labeling")
    parser.add_argument("--file", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--type", choices=["image", "video"], default="image")
    args = parser.parse_args()
    try:
        result = call_cloud(args.file, args.labels, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if isinstance(result, dict) and result.get("success") is False:
            sys.exit(2)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
