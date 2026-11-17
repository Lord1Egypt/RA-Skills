#!/usr/bin/env python3
"""
eKYC Suite cloud client.

The public ClawHub skill is intentionally a thin client: it keeps the CLI,
input normalization, and user-facing tool names, then calls the configured
eKYC Suite Cloud backend for verification.
"""

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

CLIENT_VERSION = "1.1.26"
MAX_RAW_BYTES = 20 * 1024 * 1024

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def cloud_config():
    endpoint = os.environ.get("EKYC_CLOUD_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("EKYC_CLOUD_API_KEY", "")
    missing = []
    if not endpoint:
        missing.append("EKYC_CLOUD_ENDPOINT")
    if not api_key:
        missing.append("EKYC_CLOUD_API_KEY")
    if missing:
        raise RuntimeError(
            "Missing cloud configuration: "
            + ", ".join(missing)
            + ". Set these environment variables before using the skill."
        )
    parsed = urlparse(endpoint)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        raise RuntimeError("EKYC_CLOUD_ENDPOINT must be a valid HTTPS URL.")
    if parsed.username or parsed.password:
        raise RuntimeError("EKYC_CLOUD_ENDPOINT must not contain embedded credentials.")
    return endpoint, api_key


def media_input(value: str) -> str:
    path = Path(value)
    if path.is_file():
        size = path.stat().st_size
        if size > MAX_RAW_BYTES:
            raise ValueError(f"File too large: {size / 1024 / 1024:.1f}MB, max 20MB.")
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    if value.startswith("http://"):
        raise ValueError("Only public HTTPS URLs are accepted.")
    return value


def call_cloud(tool: str, payload: dict) -> dict:
    endpoint, api_key = cloud_config()
    url = f"{endpoint}/api/v1/tools/{tool}"
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "user-agent": f"ekyc-suite-skill/{CLIENT_VERSION}",
        "x-ekyc-client": "clawhub-skill",
        "x-ekyc-version": CLIENT_VERSION,
        "x-ekyc-runtime": f"python/{platform.python_version()} {platform.system()}",
        "x-ekyc-transport": "cli",
    }
    optional_headers = {
        "x-ekyc-source-site": os.environ.get("EKYC_SOURCE_SITE") or os.environ.get("EKYC_SITE"),
        "x-ekyc-source-channel": os.environ.get("EKYC_SOURCE_CHANNEL"),
        "x-ekyc-client-name": os.environ.get("EKYC_CLIENT_NAME"),
        "x-ekyc-client-id": os.environ.get("EKYC_CLIENT_ID"),
        "x-ekyc-workspace": os.environ.get("EKYC_WORKSPACE"),
        "x-ekyc-install-id": os.environ.get("EKYC_INSTALL_ID"),
        "x-ekyc-package-manager": os.environ.get("CLAW_HOME") and "clawhub",
    }
    headers.update({key: value for key, value in optional_headers.items() if value})
    response = requests.post(url, json=payload, headers=headers, timeout=120)
    trace_id = response.headers.get("x-ekyc-trace-id")
    try:
        data = response.json()
    except ValueError:
        data = {
            "success": False,
            "error": f"Cloud backend returned non-JSON response (HTTP {response.status_code}).",
        }
    if trace_id and isinstance(data, dict) and "traceId" not in data:
        data["traceId"] = trace_id
    if response.status_code >= 400 and isinstance(data, dict) and "success" not in data:
        data = {
            "success": False,
            "error": data.get("message") or data.get("error") or f"HTTP {response.status_code}",
            "traceId": trace_id,
        }
    return data


def face_compare(photo1: str, photo2: str, source_photo_type: str = "2") -> dict:
    return call_cloud(
        "face_compare",
        {
            "photo1": media_input(photo1),
            "photo2": media_input(photo2),
            "sourcePhotoType": source_photo_type,
        },
    )


def photo_liveness_detect(file_input: str) -> dict:
    return call_cloud("photo_liveness_detect", {"file": media_input(file_input)})


def video_liveness_detect(file_input: str) -> dict:
    return call_cloud("video_liveness_detect", {"file": media_input(file_input)})


def id_card_ocr(image: str, side: str = "0") -> dict:
    return call_cloud("id_card_ocr", {"image": media_input(image), "side": side})


def bank_card_ocr(image: str) -> dict:
    return call_cloud("bank_card_ocr", {"image": media_input(image)})


def driver_license_ocr(image: str) -> dict:
    return call_cloud("driver_license_ocr", {"image": media_input(image)})


def vehicle_license_ocr(image: str, side: str = "1") -> dict:
    return call_cloud("vehicle_license_ocr", {"image": media_input(image), "side": side})


def media_labeling(
    file_input: str,
    label_list: str,
    file_type: str = "image",
    do_live: str = "1",
    do_compare: str = "1",
) -> dict:
    return call_cloud(
        "media_labeling",
        {
            "file": media_input(file_input),
            "labels": label_list,
            "type": file_type,
            "doLive": do_live,
            "doCompare": do_compare,
        },
    )


def main():
    parser = argparse.ArgumentParser(description="eKYC Suite Cloud Client")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    p1 = sub.add_parser("face_compare")
    p1.add_argument("--photo1", required=True)
    p1.add_argument("--photo2", required=True)
    p1.add_argument("--source-photo-type", default="2")

    p2 = sub.add_parser("photo_liveness_detect")
    p2.add_argument("--file", required=True)

    p3 = sub.add_parser("video_liveness_detect")
    p3.add_argument("--file", required=True)

    p4 = sub.add_parser("id_card_ocr")
    p4.add_argument("--image", required=True)
    p4.add_argument("--side", choices=["0", "1"], default="0")

    p5 = sub.add_parser("bank_card_ocr")
    p5.add_argument("--image", required=True)

    p6 = sub.add_parser("driver_license_ocr")
    p6.add_argument("--image", required=True)

    p7 = sub.add_parser("vehicle_license_ocr")
    p7.add_argument("--image", required=True)
    p7.add_argument("--side", choices=["1", "2"], default="1")

    p8 = sub.add_parser("media_labeling")
    p8.add_argument("--file", required=True)
    p8.add_argument("--labels", required=True)
    p8.add_argument("--type", choices=["image", "video"], default="image")
    p8.add_argument("--do-live", default="1")
    p8.add_argument("--do-compare", default="1")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        dispatch = {
            "face_compare": lambda: face_compare(args.photo1, args.photo2, args.source_photo_type),
            "photo_liveness_detect": lambda: photo_liveness_detect(args.file),
            "video_liveness_detect": lambda: video_liveness_detect(args.file),
            "id_card_ocr": lambda: id_card_ocr(args.image, args.side),
            "bank_card_ocr": lambda: bank_card_ocr(args.image),
            "driver_license_ocr": lambda: driver_license_ocr(args.image),
            "vehicle_license_ocr": lambda: vehicle_license_ocr(args.image, args.side),
            "media_labeling": lambda: media_labeling(args.file, args.labels, args.type, args.do_live, args.do_compare),
        }
        result = dispatch[args.command]()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if isinstance(result, dict) and result.get("success") is False:
            sys.exit(2)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
