#!/usr/bin/env python3
"""Upload a local image file through Fotor's current signed upload flow."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib import parse, request


DEFAULT_ENDPOINT = "https://api-b.fotor.com"
UPLOAD_TYPE_BY_TASK = {
    "image2image": "img2img",
    "image_upscale": "img_upscale",
    "background_remove": "bg_remove",
    "single_image2video": "img2video",
    "start_end_frame2video": "img2video",
    "multiple_image2video": "img2video",
}


def infer_suffix(path: Path, explicit_suffix: str = "") -> str:
    if explicit_suffix:
        return explicit_suffix.lstrip(".").lower()
    suffix = path.suffix.lstrip(".").lower()
    if not suffix:
        raise ValueError(f"Unable to infer file suffix from path: {path}")
    return suffix


def upload_type_for_task(task_type: str) -> str:
    try:
        return UPLOAD_TYPE_BY_TASK[task_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported task_type for upload mapping: {task_type}") from exc


def request_upload_ticket(
    *,
    endpoint: str,
    api_key: str,
    upload_type: str,
    suffix: str,
) -> dict:
    query = parse.urlencode({"type": upload_type, "suffix": suffix})
    req = request.Request(
        f"{endpoint.rstrip('/')}/v1/upload/sign?{query}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "curl/8.5.0",
        },
        method="GET",
    )
    with request.urlopen(req) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    data = payload["data"]
    return {
        "upload_url": data["upload_url"],
        "file_url": data["url"],
    }


def upload_file(file_path: Path, upload_url: str) -> None:
    content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    req = request.Request(
        upload_url,
        data=file_path.read_bytes(),
        headers={"Content-Type": content_type},
        method="PUT",
    )
    with request.urlopen(req):
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upload a local image and return a URL")
    parser.add_argument("file", help="Local image path")
    parser.add_argument(
        "--task-type",
        required=True,
        dest="task_type",
        help="Fotor task type used to infer upload type, for example: image2image",
    )
    parser.add_argument(
        "--suffix",
        help="File suffix sent to the sign endpoint. Defaults to the file extension.",
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("FOTOR_OPENAPI_ENDPOINT", DEFAULT_ENDPOINT),
        help=f"Fotor API endpoint (default: {DEFAULT_ENDPOINT})",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    api_key = os.environ.get("FOTOR_OPENAPI_KEY", "")
    if not api_key:
        print(json.dumps({"error": "FOTOR_OPENAPI_KEY not set"}), file=sys.stderr)
        return 1

    file_path = Path(args.file).expanduser().resolve()
    if not file_path.is_file():
        print(json.dumps({"error": f"File not found: {file_path}"}), file=sys.stderr)
        return 1

    try:
        suffix = infer_suffix(file_path, args.suffix or "")
        upload_type = upload_type_for_task(args.task_type)
        ticket = request_upload_ticket(
            endpoint=args.endpoint,
            api_key=api_key,
            upload_type=upload_type,
            suffix=suffix,
        )
        upload_file(file_path, ticket["upload_url"])
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "success": True,
                "file": str(file_path),
                "task_type": args.task_type,
                "upload_type": upload_type,
                "suffix": suffix,
                "file_url": ticket["file_url"],
                "upload_url": ticket["upload_url"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
