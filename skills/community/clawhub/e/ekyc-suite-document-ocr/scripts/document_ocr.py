#!/usr/bin/env python3
"""Focused eKYC Suite Document OCR cloud client."""

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
        if path.stat().st_size > MAX_RAW_BYTES:
            raise ValueError("File exceeds the 20MB limit.")
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    if value.startswith("http://"):
        raise ValueError("Only public HTTPS URLs are accepted.")
    return value


def call_cloud(tool, image, side=None):
    endpoint, api_key = cloud_config()
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "user-agent": f"ekyc-suite-document-ocr-skill/{CLIENT_VERSION}",
        "x-ekyc-client": "clawhub-skill-document-ocr",
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
    payload = {"image": media_input(image)}
    if side is not None:
        payload["side"] = side
    response = requests.post(
        f"{endpoint}/api/v1/tools/{tool}",
        json=payload,
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
    parser = argparse.ArgumentParser(description="eKYC Suite Document OCR")
    sub = parser.add_subparsers(dest="document", required=True)
    id_card = sub.add_parser("id-card")
    id_card.add_argument("--image", required=True)
    id_card.add_argument("--side", choices=["0", "1"], default="0")
    bank_card = sub.add_parser("bank-card")
    bank_card.add_argument("--image", required=True)
    driver = sub.add_parser("driver-license")
    driver.add_argument("--image", required=True)
    vehicle = sub.add_parser("vehicle-license")
    vehicle.add_argument("--image", required=True)
    vehicle.add_argument("--side", choices=["1", "2"], default="1")
    args = parser.parse_args()
    mapping = {
        "id-card": ("id_card_ocr", args.side if args.document == "id-card" else None),
        "bank-card": ("bank_card_ocr", None),
        "driver-license": ("driver_license_ocr", None),
        "vehicle-license": ("vehicle_license_ocr", args.side if args.document == "vehicle-license" else None),
    }
    tool, side = mapping[args.document]
    try:
        result = call_cloud(tool, args.image, side)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if isinstance(result, dict) and result.get("success") is False:
            sys.exit(2)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
