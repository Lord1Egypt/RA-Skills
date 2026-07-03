#!/usr/bin/env python3
"""Upload a video to Feishu and send it as a media message.

自动抽取首帧作为封面、用 ffprobe 探测时长，上传后以 msg_type=media 发送，
飞书聊天中可直接播放（带封面 + 时长）。

--file 与 --url 二选一：--url 会先把远端视频下载到临时文件，发送完成后自动删除。
--receive-id 必填，由调用方（模型）传入当前聊天的 chat_id（群聊 oc_）或 open_id（单聊 ou_）。

Usage:
    # 本地文件
    python3 scripts/feishu_send_video.py --file video.mp4 --receive-id oc_xxx

    # 远端 URL（如 OpenViking preview_url），下载后发送并自动清理
    python3 scripts/feishu_send_video.py --url 'https://.../video.mp4' --receive-id oc_xxx

    # 跳过封面
    python3 scripts/feishu_send_video.py --file video.mp4 --receive-id ou_xxx --no-cover
"""
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

import requests


FEISHU_TOKEN_URL = (
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
)
FEISHU_IMAGE_UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/images"
FEISHU_FILE_UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/files"
FEISHU_SEND_MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

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


def download_video(url: str) -> Path:
    """下载远端视频到临时文件，返回本地路径（调用方负责删除）。"""
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in VIDEO_EXTENSIONS:
        suffix = ".mp4"  # URL 无有效后缀时默认 mp4
    fd, tmp_name = tempfile.mkstemp(prefix="_ovvideo_", suffix=suffix)
    os.close(fd)
    tmp_path = Path(tmp_name)
    with requests.get(url, stream=True, timeout=300) as resp:
        resp.raise_for_status()
        with tmp_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                if chunk:
                    f.write(chunk)
    if tmp_path.stat().st_size == 0:
        tmp_path.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded empty file from: {url}")
    return tmp_path


def extract_first_frame(video_path: Path) -> Optional[Path]:
    """用 ffmpeg 抽取第 1 秒首帧作为封面，失败返回 None。"""
    cover_path = Path(tempfile.gettempdir()) / f"_cover_{os.getpid()}.jpg"
    try:
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-ss", "00:00:01",
                "-i", str(video_path),
                "-vframes", "1",
                "-q:v", "2",
                str(cover_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
        )
        if cover_path.exists() and cover_path.stat().st_size > 0:
            return cover_path
    except Exception as exc:  # 封面失败不阻断主流程
        print(f"Warning: extract cover failed, fallback to no cover: {exc}")
    return None


def probe_duration_ms(video_path: Path) -> Optional[int]:
    """用 ffprobe 探测视频时长，返回毫秒；失败返回 None。"""
    try:
        out = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(video_path),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout.strip()
        if out:
            return int(float(out) * 1000)
    except Exception as exc:  # 探测失败不阻断，仅时长显示为 0
        print(f"Warning: probe duration failed: {exc}")
    return None


def upload_cover_image(token: str, image_path: Path) -> str:
    """上传封面图 via /im/v1/images，返回 image_key。"""
    headers = {"Authorization": f"Bearer {token}"}
    with image_path.open("rb") as f:
        resp = requests.post(
            FEISHU_IMAGE_UPLOAD_URL,
            headers=headers,
            data={"image_type": "message"},
            files={"image": (image_path.name, f)},
            timeout=60,
        )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Upload cover image failed: {data}")
    return data["data"]["image_key"]


def upload_video(token: str, file_path: Path) -> str:
    """上传视频 via /im/v1/files（file_type=mp4，带 duration），返回 file_key。"""
    headers = {"Authorization": f"Bearer {token}"}
    form: Dict[str, str] = {
        "file_type": "mp4",
        "file_name": file_path.name,
    }
    duration_ms = probe_duration_ms(file_path)
    if duration_ms:
        form["duration"] = str(duration_ms)
    with file_path.open("rb") as f:
        resp = requests.post(
            FEISHU_FILE_UPLOAD_URL,
            headers=headers,
            data=form,
            files={"file": (file_path.name, f)},
            timeout=120,
        )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Upload video failed: {data}")
    return data["data"]["file_key"]


def send_video_message(
    token: str,
    receive_id: str,
    receive_id_type: str,
    file_key: str,
    image_key: Optional[str] = None,
) -> Dict[str, Any]:
    """发送 msg_type=media 视频消息，可带 image_key 作为封面。"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    params = {"receive_id_type": receive_id_type}

    media_content: Dict[str, str] = {"file_key": file_key}
    if image_key:
        media_content["image_key"] = image_key

    payload = {
        "receive_id": receive_id,
        "msg_type": "media",
        "content": json.dumps(media_content),
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
    if not cli_value:
        raise RuntimeError(
            "Missing --receive-id. 由调用方传入当前聊天的 chat_id（群聊 oc_）"
            "或 open_id（单聊 ou_）。"
        )
    # 归一化：剥掉 OpenClaw 上下文里带的 channel 前缀（如 chat:oc_xxx → oc_xxx）
    value = cli_value.strip()
    if ":" in value:
        value = value.rsplit(":", 1)[-1]
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload a video to Feishu and send it as a media message"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Local video file path")
    source.add_argument("--url", help="Remote video URL (downloaded then cleaned up)")
    parser.add_argument(
        "--receive-id",
        required=True,
        help="必填：当前聊天的 chat_id（群聊 oc_）或 open_id（单聊 ou_）",
    )
    parser.add_argument(
        "--receive-id-type",
        default=None,
        help="chat_id / open_id / user_id (auto-detect if omitted)",
    )
    parser.add_argument(
        "--no-cover",
        action="store_true",
        help="Skip first-frame cover extraction",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # --url：先下载到临时文件，结束后删除；--file：使用本地文件，不删除
    downloaded_path: Optional[Path] = None
    if args.url:
        downloaded_path = download_video(args.url)
        file_path = downloaded_path
    else:
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    if file_path.suffix.lower() not in VIDEO_EXTENSIONS:
        raise ValueError(
            f"Unsupported video extension: {file_path.suffix}. "
            f"Supported: {sorted(VIDEO_EXTENSIONS)}"
        )

    config = load_openclaw_config()
    agent_id = resolve_agent_id(config)
    app_id, app_secret = resolve_feishu_account(config, agent_id)

    receive_id = resolve_receive_id(args.receive_id)
    receive_id_type = infer_receive_id_type(receive_id, args.receive_id_type)

    token = get_tenant_access_token(app_id, app_secret)

    # 先抽首帧上传当封面（失败降级无封面），再上传视频
    image_key: Optional[str] = None
    cover_path: Optional[Path] = None
    try:
        if not args.no_cover:
            cover_path = extract_first_frame(file_path)
            if cover_path:
                try:
                    image_key = upload_cover_image(token, cover_path)
                except Exception as exc:  # 封面上传失败降级无封面
                    print(f"Warning: upload cover failed, fallback to no cover: {exc}")
                    image_key = None

        file_key = upload_video(token, file_path)
        result = send_video_message(
            token, receive_id, receive_id_type, file_key, image_key
        )
        print("Send success:", json.dumps(result, ensure_ascii=False))
    finally:
        # 清理临时封面 + 下载的临时视频
        if cover_path and cover_path.exists():
            cover_path.unlink(missing_ok=True)
        if downloaded_path and downloaded_path.exists():
            downloaded_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
