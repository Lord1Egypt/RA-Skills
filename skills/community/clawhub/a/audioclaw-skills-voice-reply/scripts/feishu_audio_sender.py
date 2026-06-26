#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import re
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
for parent in SCRIPT_DIR.parents:
    candidate = parent / "_shared" / "audioclaw_paths.py"
    if candidate.exists():
        candidate_dir = str(candidate.parent)
        if candidate_dir not in sys.path:
            sys.path.insert(0, candidate_dir)
        break

from audioclaw_paths import get_config_path, get_workspace_root

DEFAULT_CONFIG_PATH = get_config_path()
DEFAULT_WORKSPACE = get_workspace_root()
CHAT_ID_PATTERN = re.compile(r'oc_[0-9a-z]+')


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json in {path}: {exc}") from exc


def load_feishu_config(config_path: Path) -> dict:
    config = load_json(config_path)
    feishu = ((config.get("channels") or {}).get("feishu") or {})
    if not feishu.get("enabled"):
        raise SystemExit("feishu channel is not enabled in config.json")
    app_id = str(feishu.get("app_id") or "").strip()
    app_secret = str(feishu.get("app_secret") or "").strip()
    if not app_id or not app_secret:
        raise SystemExit("feishu app_id/app_secret is missing in config.json")
    return {
        "app_id": app_id,
        "app_secret": app_secret,
    }


def http_json(url: str, payload: dict, headers: Optional[Dict[str, str]] = None) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            **(headers or {}),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"http {exc.code} from {url}: {body}") from exc


def build_multipart(fields: Dict[str, str], file_field: str, file_name: str, content_type: str, file_bytes: bytes) -> Tuple[str, bytes]:
    boundary = f"----CodexBoundary{secrets.token_hex(12)}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f"{value}\r\n"
            ).encode("utf-8")
        )
    chunks.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_bytes)
    chunks.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    return boundary, b"".join(chunks)


def fetch_tenant_token(app_id: str, app_secret: str) -> str:
    data = http_json(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if data.get("code") != 0:
        raise SystemExit(f"failed to fetch tenant token: {json.dumps(data, ensure_ascii=False)}")
    token = str(data.get("tenant_access_token") or "").strip()
    if not token:
        raise SystemExit("tenant token response missing tenant_access_token")
    return token


def infer_chat_id(workspace_root: Path, explicit_chat_id: str, session_file: str) -> tuple[str, str]:
    if explicit_chat_id:
        return explicit_chat_id, ""
    if session_file:
        path = Path(session_file).expanduser()
        chat_id = extract_chat_id(path)
        if chat_id:
            return chat_id, str(path)
        raise SystemExit(f"no chat_id found in {path}")

    sessions_dir = workspace_root / "sessions"
    candidates = sorted(sessions_dir.glob("agent_main_feishu_direct_*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        candidates = sorted(sessions_dir.glob("*feishu*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for candidate in candidates:
        chat_id = extract_chat_id(candidate)
        if chat_id:
            return chat_id, str(candidate)
    state_path = workspace_root / "state" / "state.json"
    try:
        state = load_json(state_path)
    except SystemExit:
        state = {}
    last_channel = str(state.get("last_channel") or "").strip()
    if last_channel.startswith("feishu:"):
        chat_id = last_channel.split(":", 1)[1].strip()
        if chat_id:
            return chat_id, str(state_path)
    raise SystemExit("could not infer feishu chat_id from session logs; pass --chat-id")


def extract_chat_id(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""
    matches = CHAT_ID_PATTERN.findall(text)
    return matches[-1] if matches else ""


def upload_audio(file_path: Path, tenant_token: str, duration_ms: Optional[int]) -> dict:
    file_bytes = file_path.read_bytes()
    suffix = file_path.suffix.lower()
    if suffix not in {".ogg", ".opus"}:
        raise SystemExit("feishu audio sending expects an .ogg or .opus file")
    file_type = "opus"
    content_type = mimetypes.guess_type(file_path.name)[0] or "audio/ogg"
    fields = {
        "file_type": file_type,
        "file_name": file_path.name,
    }
    if duration_ms and duration_ms > 0:
        fields["duration"] = str(duration_ms)
    boundary, body = build_multipart(fields, "file", file_path.name, content_type, file_bytes)
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/files",
        data=body,
        headers={
            "Authorization": f"Bearer {tenant_token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"audio upload failed with http {exc.code}: {body}") from exc
    if data.get("code") != 0:
        raise SystemExit(f"audio upload failed: {json.dumps(data, ensure_ascii=False)}")
    return data


def send_audio_message(chat_id: str, file_key: str, tenant_token: str) -> dict:
    payload = {
        "receive_id": chat_id,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key}, ensure_ascii=False),
    }
    data = http_json(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        payload,
        headers={"Authorization": f"Bearer {tenant_token}"},
    )
    if data.get("code") != 0:
        raise SystemExit(f"audio send failed: {json.dumps(data, ensure_ascii=False)}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload an Ogg/Opus file to Feishu and send it as an audio message.")
    parser.add_argument("--audio-path", required=True)
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--config-path", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--chat-id", default="")
    parser.add_argument("--session-file", default="")
    parser.add_argument("--duration-ms", type=int)
    parser.add_argument("--filename", default="")
    args = parser.parse_args()

    audio_path = Path(args.audio_path).expanduser().resolve()
    if not audio_path.exists():
        raise SystemExit(f"missing audio file: {audio_path}")

    config = load_feishu_config(Path(args.config_path).expanduser())
    chat_id, session_path = infer_chat_id(Path(args.workspace_root).expanduser(), args.chat_id.strip(), args.session_file.strip())
    tenant_token = fetch_tenant_token(config["app_id"], config["app_secret"])
    upload = upload_audio(audio_path, tenant_token, args.duration_ms)
    file_key = (((upload.get("data") or {}).get("file_key")) or "").strip()
    if not file_key:
        raise SystemExit(f"upload response missing file_key: {json.dumps(upload, ensure_ascii=False)}")
    send = send_audio_message(chat_id, file_key, tenant_token)
    result = {
        "mode": "feishu_audio_sent",
        "chat_id": chat_id,
        "session_file": session_path,
        "audio_path": str(audio_path),
        "filename": args.filename or audio_path.name,
        "upload": {
            "file_key": file_key,
            "response": upload,
        },
        "send": send,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
