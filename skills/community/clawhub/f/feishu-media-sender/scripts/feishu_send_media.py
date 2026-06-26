#!/usr/bin/env python3
"""Upload images or videos to Feishu and send as media messages.

Usage:
    # Send image (auto-detected by extension)
    python3 scripts/feishu_send_media.py --file photo.jpg --receive-id ou_xxx

    # Send video
    python3 scripts/feishu_send_media.py --file video.mp4 --receive-id ou_xxx

    # Explicit type
    python3 scripts/feishu_send_media.py --file clip.gif --receive-id ou_xxx --type video
"""
import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests


FEISHU_TOKEN_URL = (
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
)
FEISHU_IMAGE_UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/images"
FEISHU_FILE_UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/files"
FEISHU_SEND_MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".ico", ".tiff", ".heic"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


def load_openclaw_config() -> Dict[str, Any]:
    if not OPENCLAW_CONFIG.exists():
        raise FileNotFoundError(f"OpenClaw config not found: {OPENCLAW_CONFIG}")
    return json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8"))


def resolve_agent_id(config: Dict[str, Any]) -> str:
    cwd = Path.cwd().resolve()
    best_match = (0, None)

    defaults_ws = config.get("agents", {}).get("defaults", {}).get("workspace")
    if defaults_ws:
        defaults_path = Path(defaults_ws).resolve()
        if str(cwd).startswith(str(defaults_path)):
            best_match = (len(str(defaults_path)), "__defaults__")

    for agent in config.get("agents", {}).get("list", []):
        workspace = agent.get("workspace")
        agent_id = agent.get("id")
        if not workspace or not agent_id:
            continue
        workspace_path = Path(workspace).resolve()
        if str(cwd).startswith(str(workspace_path)):
            match_len = len(str(workspace_path))
            if match_len > best_match[0]:
                best_match = (match_len, agent_id)

    if best_match[1]:
        return best_match[1]
    raise RuntimeError("Unable to resolve agent id from workspace path")


def resolve_feishu_account(
    config: Dict[str, Any], agent_id: str
) -> Tuple[str, str]:
    feishu = config.get("channels", {}).get("feishu", {})

    # Style 1: flat config — channels.feishu.appId / appSecret
    app_id = feishu.get("appId")
    app_secret = feishu.get("appSecret")
    if app_id and app_secret:
        return app_id, app_secret

    # Style 2: nested accounts — channels.feishu.accounts.<id>.appId / appSecret
    accounts = feishu.get("accounts", {})
    bindings = config.get("bindings", [])
    account_id = None
    for binding in bindings:
        bid = binding.get("agentId")
        if bid == agent_id or (agent_id == "__defaults__" and not account_id):
            account_id = binding.get("match", {}).get("accountId")
            if account_id:
                break
    if not account_id and bindings:
        account_id = bindings[0].get("match", {}).get("accountId")
    if not account_id and accounts:
        account_id = next(iter(accounts), None)
    if account_id:
        account = accounts.get(account_id, {})
        app_id = account.get("appId")
        app_secret = account.get("appSecret")
        if app_id and app_secret:
            return app_id, app_secret

    raise RuntimeError(
        "No Feishu credentials found. Check channels.feishu in openclaw.json"
    )


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    resp = requests.post(
        FEISHU_TOKEN_URL,
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Get token failed: {data}")
    return data["tenant_access_token"]


def detect_media_type(file_path: Path, explicit: Optional[str]) -> str:
    if explicit:
        return explicit.lower()
    ext = file_path.suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    # Default to image for unknown extensions
    return "image"


def upload_image(token: str, file_path: Path) -> str:
    """Upload image via /im/v1/images, return image_key."""
    headers = {"Authorization": f"Bearer {token}"}
    with file_path.open("rb") as f:
        resp = requests.post(
            FEISHU_IMAGE_UPLOAD_URL,
            headers=headers,
            data={"image_type": "message"},
            files={"image": (file_path.name, f)},
            timeout=60,
        )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Upload image failed: {data}")
    return data["data"]["image_key"]


def upload_video(token: str, file_path: Path) -> str:
    """Upload video via /im/v1/files with file_type=mp4, return file_key."""
    headers = {"Authorization": f"Bearer {token}"}
    with file_path.open("rb") as f:
        resp = requests.post(
            FEISHU_FILE_UPLOAD_URL,
            headers=headers,
            data={
                "file_type": "mp4",
                "file_name": file_path.name,
            },
            files={"file": (file_path.name, f)},
            timeout=120,
        )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Upload video failed: {data}")
    return data["data"]["file_key"]


def send_media_message(
    token: str,
    receive_id: str,
    receive_id_type: str,
    media_key: str,
    media_type: str,
) -> Dict[str, Any]:
    """Send image or video message."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    params = {"receive_id_type": receive_id_type}

    if media_type == "image":
        msg_type = "image"
        content = json.dumps({"image_key": media_key})
    else:
        msg_type = "media"
        content = json.dumps({"file_key": media_key})

    payload = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": content,
    }
    resp = requests.post(
        FEISHU_SEND_MSG_URL,
        headers=headers,
        params=params,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Send message failed: {data}")
    return data


def infer_receive_id_type(receive_id: str, explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    if receive_id.startswith("oc_"):
        return "chat_id"
    if receive_id.startswith("ou_"):
        return "open_id"
    if receive_id.startswith("on_"):
        return "user_id"
    return "chat_id"


def resolve_receive_id(cli_value: Optional[str]) -> str:
    if cli_value:
        return cli_value
    env_value = (
        os.getenv("OPENCLAW_CHAT_ID")
        or os.getenv("OPENCLAW_RECEIVE_ID")
        or os.getenv("FEISHU_CHAT_ID")
    )
    if env_value:
        return env_value
    raise RuntimeError(
        "Missing receive_id. Provide --receive-id or set OPENCLAW_CHAT_ID."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload image/video to Feishu and send as media message"
    )
    parser.add_argument("--file", required=True, help="Local file path")
    parser.add_argument("--receive-id", default=None, help="chat_id or open_id")
    parser.add_argument(
        "--receive-id-type",
        default=None,
        help="chat_id / open_id / user_id (auto-detect if omitted)",
    )
    parser.add_argument(
        "--type",
        default=None,
        choices=["image", "video"],
        help="Media type (auto-detected from file extension if omitted)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    media_type = detect_media_type(file_path, args.type)

    config = load_openclaw_config()
    agent_id = resolve_agent_id(config)
    app_id, app_secret = resolve_feishu_account(config, agent_id)

    receive_id = resolve_receive_id(args.receive_id)
    receive_id_type = infer_receive_id_type(receive_id, args.receive_id_type)

    token = get_tenant_access_token(app_id, app_secret)

    if media_type == "image":
        media_key = upload_image(token, file_path)
    else:
        media_key = upload_video(token, file_path)

    result = send_media_message(token, receive_id, receive_id_type, media_key, media_type)
    print("Send success:", json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
