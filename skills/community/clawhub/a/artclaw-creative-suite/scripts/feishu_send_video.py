#!/usr/bin/env python3
"""
Send video messages via Feishu (Lark)

Usage:
    python3 feishu_send_video.py \
        --video /path/to/video.mp4 \
        --to ou_xxx \
        [--cover /path/to/cover.jpg | --cover-url https://...] \
        [--duration 20875]

Flow:
    1. Upload video file (file_type=mp4, with duration) -> get file_key
    2. Upload cover image (image_type=message) -> get image_key (optional)
    3. Send media message (msg_type=media)

Key points:
    - msg_type must be "media" (not "video" or "file")
    - file_type is "mp4" when uploading video
    - duration is in milliseconds; shows 00:00 if omitted
    - Cover image uploaded via im/v1/images for image_key, included in content
    - Sending without cover works but shows a black background with no preview

Feishu API reference:
    - Upload file: POST /open-apis/im/v1/files
    - Upload image: POST /open-apis/im/v1/images
    - Send message: POST /open-apis/im/v1/messages
"""

import argparse
import json
import os
import requests
import sys
import tempfile


def get_feishu_credentials():
    """Read Feishu credentials from openclaw config."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path) as f:
        config = json.load(f)
    feishu = config.get("channels", {}).get("feishu", {})
    accounts = feishu.get("accounts", {})
    # Try accounts.main first, then top-level
    if accounts:
        main_acct = accounts.get("main", accounts.get("default", list(accounts.values())[0] if accounts else {}))
        app_id = main_acct.get("appId", "")
        app_secret = main_acct.get("appSecret", "")
    else:
        app_id = feishu.get("appId", "")
        app_secret = feishu.get("appSecret", "")
    if not app_id or not app_secret:
        print(json.dumps({
            "error": "Feishu credentials not found in ~/.openclaw/openclaw.json",
            "hint": "Configure channels.feishu.accounts.main.appId and appSecret"
        }), file=sys.stderr)
        sys.exit(1)
    return app_id, app_secret


def get_tenant_token():
    """Get tenant access token from Feishu."""
    app_id, app_secret = get_feishu_credentials()
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
    )
    resp.raise_for_status()
    return resp.json()["tenant_access_token"]


def upload_video(token, video_path, duration_ms=None):
    """Upload video file, return file_key."""
    data = {"file_type": "mp4", "file_name": os.path.basename(video_path)}
    if duration_ms:
        data["duration"] = str(int(duration_ms))

    with open(video_path, "rb") as f:
        resp = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/files",
            headers={"Authorization": f"Bearer {token}"},
            data=data,
            files={"file": (os.path.basename(video_path), f, "video/mp4")},
            timeout=(15, 120),
        )
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Upload failed: {result}")
    return result["data"]["file_key"]


def upload_cover(token, cover_source):
    """Upload cover image, return image_key. cover_source can be a local path or URL."""
    if cover_source.startswith("http"):
        # Download from URL
        img_resp = requests.get(cover_source, timeout=30)
        img_resp.raise_for_status()
        img_data = img_resp.content
        filename = "cover.jpg"
    else:
        with open(cover_source, "rb") as f:
            img_data = f.read()
        filename = os.path.basename(cover_source)

    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/images",
        headers={"Authorization": f"Bearer {token}"},
        data={"image_type": "message"},
        files={"image": (filename, img_data, "image/jpeg")},
        timeout=(15, 60),
    )
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Cover upload failed: {result}")
    return result["data"]["image_key"]


def send_media_message(token, to, file_key, image_key=None):
    """Send media message via Feishu."""
    content = {"file_key": file_key}
    if image_key:
        content["image_key"] = image_key

    # Strip common prefixes from OpenClaw inbound metadata (e.g. "chat:oc_xxx" -> "oc_xxx")
    if to.startswith("chat:"):
        to = to[len("chat:"):]
    elif to.startswith("user:"):
        to = to[len("user:"):]

    # Determine receive_id_type based on prefix
    if to.startswith("oc_"):
        receive_id_type = "chat_id"
    else:
        receive_id_type = "open_id"

    resp = requests.post(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "receive_id": to,
            "msg_type": "media",
            "content": json.dumps(content),
        },
        timeout=(15, 30),
    )
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Send failed: {result}")
    return result["data"]["message_id"]


def send_image_message(token, to, image_source):
    """Send an image message via Feishu. image_source can be a local path or URL."""
    # Download or read image data
    if image_source.startswith("http"):
        img_resp = requests.get(image_source, timeout=30)
        img_resp.raise_for_status()
        img_data = img_resp.content
        filename = "image.jpg"
    else:
        with open(image_source, "rb") as f:
            img_data = f.read()
        filename = os.path.basename(image_source)

    # Upload image to get image_key
    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/images",
        headers={"Authorization": f"Bearer {token}"},
        data={"image_type": "message"},
        files={"image": (filename, img_data, "image/jpeg")},
        timeout=(15, 60),
    )
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Image upload failed: {result}")
    image_key = result["data"]["image_key"]

    # Send image message
    content = {"image_key": image_key}

    # Strip common prefixes from OpenClaw inbound metadata (e.g. "chat:oc_xxx" -> "oc_xxx")
    if to.startswith("chat:"):
        to = to[len("chat:"):]
    elif to.startswith("user:"):
        to = to[len("user:"):]

    # Determine receive_id_type based on prefix
    if to.startswith("oc_"):
        receive_id_type = "chat_id"
    else:
        receive_id_type = "open_id"

    resp = requests.post(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "receive_id": to,
            "msg_type": "image",
            "content": json.dumps(content),
        },
        timeout=(15, 30),
    )
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Send image failed: {result}")
    return result["data"]["message_id"]


def _download_to_temp(url, suffix):
    """Download URL to a temporary file and return file path."""
    resp = requests.get(url, timeout=(15, 120))
    resp.raise_for_status()
    fd, tmp_path = tempfile.mkstemp(prefix="artclaw_", suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(resp.content)
    return tmp_path


def main():
    parser = argparse.ArgumentParser(
        description="Send video or image messages via Feishu. "
                    "Use --video for videos, --image for images."
    )
    parser.add_argument("--video", help="Video file path")
    parser.add_argument("--video-url", help="Video URL (will be downloaded temporarily)")
    parser.add_argument("--image", help="Image file path or URL")
    parser.add_argument("--to", required=True, help="Recipient open_id (ou_xxx) or group chat_id (oc_xxx)")
    parser.add_argument("--cover", help="Cover image path or URL (for video)")
    parser.add_argument("--cover-url", help="Cover image URL (alias for --cover, for video)")
    parser.add_argument("--duration", type=int, help="Video duration in milliseconds")
    args = parser.parse_args()

    if not args.video and not args.video_url and not args.image:
        print(json.dumps({
            "error": "Must provide one of --video, --video-url, or --image"
        }), file=sys.stderr)
        sys.exit(1)
    if args.image and (args.video or args.video_url):
        print(json.dumps({
            "error": "Cannot specify --image together with video input"
        }), file=sys.stderr)
        sys.exit(1)
    if args.video and args.video_url:
        print(json.dumps({
            "error": "Cannot specify both --video and --video-url"
        }), file=sys.stderr)
        sys.exit(1)

    token = get_tenant_token()

    if args.image:
        print(f"[feishu] Sending image: {args.image}", file=sys.stderr)
        msg_id = send_image_message(token, args.to, args.image)
        print(json.dumps({
            "status": "ok",
            "type": "image",
            "message_id": msg_id,
        }))
        return

    # Video path
    temp_video_path = None
    if args.video_url:
        print(f"[feishu] Downloading video URL: {args.video_url}", file=sys.stderr)
        temp_video_path = _download_to_temp(args.video_url, ".mp4")
        video_path = temp_video_path
    else:
        video_path = args.video
    cover = args.cover or args.cover_url

    try:
        print(f"[feishu] Uploading video: {video_path}", file=sys.stderr)
        file_key = upload_video(token, video_path, args.duration)
        print(f"[feishu] Video file_key: {file_key}", file=sys.stderr)

        image_key = None
        if cover:
            print(f"[feishu] Uploading cover: {cover}", file=sys.stderr)
            image_key = upload_cover(token, cover)
            print(f"[feishu] Cover image_key: {image_key}", file=sys.stderr)

        msg_id = send_media_message(token, args.to, file_key, image_key)
        print(json.dumps({
            "status": "ok",
            "type": "video",
            "message_id": msg_id,
            "file_key": file_key,
            "image_key": image_key,
        }))
    finally:
        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)


if __name__ == "__main__":
    main()
