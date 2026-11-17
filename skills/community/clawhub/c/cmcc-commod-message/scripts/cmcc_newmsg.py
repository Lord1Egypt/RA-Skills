#!/usr/bin/env python3
"""Universal AI/CLI client for China Mobile CMCC New Message / 5G RCS.

Protocol behavior is derived from @openclaw/cmcc-newmsg-channel 1.0.0.
This client intentionally tightens local-file access compared with the original
plugin: outbound local files must live under the configured outbox directory.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import ssl
import sys
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import requests
    import websocket
    import yaml
except ImportError as exc:
    print(json.dumps({"ok": False, "error": f"缺少依赖: {exc}. 请先运行 install.sh 或 pip install -r requirements.txt"}, ensure_ascii=False))
    raise SystemExit(2)

DEFAULT_SERVER_URL = "wss://5gvas01.cmicmaap.com/gtw-ai/openclaw/ws/msg"
DEFAULT_UPLOAD_BASE = "https://5gvas01.cmicmaap.com/gtw-ai/openclaw/api"
DEFAULT_VERSION = "2.0"
API_KEY_RE = re.compile(r"^(ak_|app_)")


def get_state_dir() -> Path:
    raw = os.environ.get("CMCC_NEWMSG_HOME")
    if raw:
        return Path(raw).expanduser().resolve()
    hermes_home = os.environ.get("HERMES_HOME")
    if hermes_home:
        return (Path(hermes_home).expanduser().resolve() / "cmcc-newmsg")
    return (Path.home() / ".cmcc-newmsg").resolve()


def skill_state_dir() -> Path:
    # Kept as a compatibility helper name for older integrations.
    return get_state_dir()


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def expand_path(value: str | Path) -> Path:
    return Path(os.path.expandvars(str(value))).expanduser().resolve()


def load_config() -> dict[str, Any]:
    state = skill_state_dir()
    load_dotenv(state / ".env")
    cfg_path = state / "config.yaml"
    cfg: dict[str, Any] = {}
    if cfg_path.exists():
        loaded = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            cfg = loaded
    cfg.setdefault("server_url", DEFAULT_SERVER_URL)
    cfg.setdefault("upload_base_url", DEFAULT_UPLOAD_BASE)
    cfg.setdefault("protocol_version", DEFAULT_VERSION)
    cfg.setdefault("outbox_dir", str(state / "outbox"))
    cfg.setdefault("inbox_dir", str(state / "inbox"))
    cfg.setdefault("max_upload_mb", 200)
    cfg.setdefault("max_download_mb", 50)
    cfg.setdefault("allow_from", [])
    cfg.setdefault("auto_download_media", False)
    cfg.setdefault("media_host_allowlist", ["5gvas01.cmicmaap.com"])
    return cfg


def api_key() -> str:
    key = os.environ.get("CMCC_NEWMSG_API_KEY") or os.environ.get("SMS_API_KEY") or ""
    if not key:
        raise RuntimeError(
            f"未配置 API Key。请设置 CMCC_NEWMSG_API_KEY，或写入 {skill_state_dir() / '.env'}"
        )
    if not API_KEY_RE.match(key):
        raise RuntimeError("API Key 必须以 ak_ 或 app_ 开头")
    if key in {"ak_xxx", "app_xxx"}:
        raise RuntimeError("API Key 仍是示例占位符，请填写真实 Key")
    return key


def mask_key(key: str) -> str:
    if len(key) < 8:
        return "***"
    return f"{key[:3]}***{key[-3:]}"


def json_out(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


class CMCCClient:
    def __init__(self, cfg: dict[str, Any], key: str):
        self.cfg = cfg
        self.key = key
        self.ws: websocket.WebSocket | None = None
        self._stop = threading.Event()
        self._heartbeat_thread: threading.Thread | None = None

    def connect(self, timeout: int = 12) -> None:
        server_url = str(self.cfg["server_url"])
        if not server_url.startswith("wss://"):
            raise RuntimeError("为避免明文泄露 API Key，仅允许 wss:// server_url")
        self.ws = websocket.create_connection(
            server_url,
            timeout=timeout,
            header=[f"X-API-Key: {self.key}"],
            sslopt={"cert_reqs": ssl.CERT_REQUIRED},
        )
        self.ws.send(json.dumps({
            "type": "auth",
            "apiKey": self.key,
            "version": str(self.cfg.get("protocol_version", DEFAULT_VERSION)),
        }, ensure_ascii=False))

        deadline = time.time() + timeout
        while time.time() < deadline:
            raw = self.ws.recv()
            if raw is None:
                continue
            msg = json.loads(raw)
            typ = msg.get("type")
            if typ == "auth_ok":
                self.ws.settimeout(1.0)
                self._start_heartbeat()
                return
            if typ == "auth_failed":
                raise RuntimeError(msg.get("message") or "认证失败")
            if typ == "error":
                raise RuntimeError(msg.get("message") or "服务端错误")
        raise TimeoutError("等待 auth_ok 超时")

    def close(self) -> None:
        self._stop.set()
        if self.ws is not None:
            try:
                self.ws.close()
            finally:
                self.ws = None

    def _start_heartbeat(self) -> None:
        def run() -> None:
            while not self._stop.wait(15):
                try:
                    if self.ws is not None and self.ws.connected:
                        self.ws.send(json.dumps({"type": "ping"}))
                except Exception:
                    return
        self._heartbeat_thread = threading.Thread(target=run, daemon=True)
        self._heartbeat_thread.start()

    def send_text(self, to: str, content: str) -> str:
        if not self.ws:
            raise RuntimeError("WebSocket 未连接")
        message_id = f"msg_{int(time.time()*1000)}_{os.urandom(5).hex()}"
        payload = {
            "type": "send",
            "apiKey": self.key,
            "to": to,
            "content": content,
            "messageId": message_id,
        }
        self.ws.send(json.dumps(payload, ensure_ascii=False))
        return message_id

    def send_media(
        self,
        media_type: str,
        media_url: str,
        caption: str = "",
        file_name: str | None = None,
        file_size: int | None = None,
        mime_type: str | None = None,
        to: str | None = None,
    ) -> str:
        if not self.ws:
            raise RuntimeError("WebSocket 未连接")
        message_id = f"msg_{int(time.time()*1000)}_{os.urandom(5).hex()}"
        payload: dict[str, Any] = {
            "type": "send",
            "apiKey": self.key,
            "mediaType": media_type,
            "content": caption,
            "mediaUrl": media_url,
            "messageId": message_id,
        }
        # 原 OpenClaw 插件的富媒体 payload 不含 to；这里仅在显式给出时附带，
        # 方便服务端若支持定向路由时使用，未给出则保持官方插件行为。
        if to:
            payload["to"] = to
        if file_name:
            payload["mediaFileName"] = file_name
        if file_size is not None:
            payload["mediaSize"] = file_size
        if mime_type:
            payload["mediaMimeType"] = mime_type
        self.ws.send(json.dumps(payload, ensure_ascii=False))
        return message_id

    def recv(self) -> dict[str, Any] | None:
        if not self.ws:
            raise RuntimeError("WebSocket 未连接")
        try:
            raw = self.ws.recv()
        except websocket.WebSocketTimeoutException:
            return None
        if raw is None:
            return None
        msg = json.loads(raw)
        if msg.get("type") == "pong":
            return None
        return msg


def infer_media_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}:
        return "IMAGE"
    if ext in {".mp4", ".webm", ".3gp", ".mov", ".avi"}:
        return "VIDEO"
    if ext in {".mp3", ".wav", ".aac", ".m4a", ".ogg"}:
        return "AUDIO"
    return "FILE"


def assert_safe_outbox_file(file_path: str, cfg: dict[str, Any]) -> Path:
    p = expand_path(file_path)
    root = expand_path(cfg["outbox_dir"])
    root.mkdir(parents=True, exist_ok=True)
    if not p.is_file():
        raise RuntimeError(f"文件不存在: {p}")
    try:
        p.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(
            f"拒绝发送 outbox 之外的本地文件。请先把文件复制到: {root}"
        ) from exc
    max_bytes = int(cfg.get("max_upload_mb", 200)) * 1024 * 1024
    if p.stat().st_size > max_bytes:
        raise RuntimeError(f"文件超过最大上传限制 {cfg.get('max_upload_mb', 200)} MB")
    return p


def upload_file(p: Path, cfg: dict[str, Any], key: str) -> str:
    base = str(cfg["upload_base_url"]).rstrip("/")
    if not base.startswith("https://"):
        raise RuntimeError("为避免明文泄露 API Key，仅允许 https:// upload_base_url")
    url = f"{base}/upload"
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    # requests 会流式读取文件对象，不像原插件那样把整个文件一次性读入内存。
    with p.open("rb") as fh:
        resp = requests.post(
            url,
            files={"file": (p.name, fh, "application/octet-stream")},
            data={"apiKey": key},
            timeout=(10, 60),
        )
    resp.raise_for_status()
    try:
        body = resp.json()
    except Exception as exc:
        raise RuntimeError(f"上传响应不是 JSON: {resp.text[:300]}") from exc
    if body.get("code") != 10200 or not body.get("data"):
        raise RuntimeError(body.get("message") or f"上传失败，code={body.get('code')}")
    return str(body["data"])


def source_allowed(source: str, cfg: dict[str, Any]) -> bool:
    allow = [str(x) for x in (cfg.get("allow_from") or [])]
    if not allow:
        return True
    return "*" in allow or source in allow


def safe_download(url: str, cfg: dict[str, Any], name: str | None = None) -> Path:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise RuntimeError("仅允许下载 https:// 媒体")
    allow_hosts = {str(x).lower() for x in (cfg.get("media_host_allowlist") or [])}
    host = (parsed.hostname or "").lower()
    if host not in allow_hosts:
        raise RuntimeError(f"媒体域名不在 allowlist: {host}")

    inbox = expand_path(cfg["inbox_dir"])
    inbox.mkdir(parents=True, exist_ok=True)
    safe_name = Path(name or Path(parsed.path).name or f"media_{int(time.time())}").name
    target = inbox / safe_name
    max_bytes = int(cfg.get("max_download_mb", 50)) * 1024 * 1024

    with requests.get(url, stream=True, timeout=(10, 60), allow_redirects=False) as resp:
        resp.raise_for_status()
        declared = int(resp.headers.get("Content-Length") or 0)
        if declared and declared > max_bytes:
            raise RuntimeError("媒体文件超过下载大小限制")
        total = 0
        with target.open("wb") as out:
            for chunk in resp.iter_content(64 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    out.close()
                    target.unlink(missing_ok=True)
                    raise RuntimeError("媒体文件超过下载大小限制")
                out.write(chunk)
    return target


def cmd_init(args: argparse.Namespace) -> int:
    state = skill_state_dir()
    state.mkdir(parents=True, exist_ok=True)
    (state / "outbox").mkdir(exist_ok=True)
    (state / "inbox").mkdir(exist_ok=True)
    skill_dir = Path(__file__).resolve().parent.parent
    cfg_dst = state / "config.yaml"
    env_dst = state / ".env"
    if not cfg_dst.exists():
        cfg_dst.write_text((skill_dir / "config.example.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    if not env_dst.exists():
        env_dst.write_text((skill_dir / ".env.example").read_text(encoding="utf-8"), encoding="utf-8")
        try:
            env_dst.chmod(0o600)
        except OSError:
            pass
    json_out({"ok": True, "state_dir": str(get_state_dir()), "config": str(cfg_dst), "env": str(env_dst)})
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    cfg = load_config()
    result: dict[str, Any] = {
        "ok": True,
        "state_dir": str(get_state_dir()),
        "server_url": cfg["server_url"],
        "upload_base_url": cfg["upload_base_url"],
        "outbox_dir": str(expand_path(cfg["outbox_dir"])),
    }
    try:
        key = api_key()
        result["api_key"] = mask_key(key)
    except Exception as exc:
        result["ok"] = False
        result["api_key_error"] = str(exc)
    json_out(result)
    return 0 if result["ok"] else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    cfg = load_config()
    key = api_key()
    client = CMCCClient(cfg, key)
    try:
        client.connect()
        json_out({"ok": True, "authenticated": True, "server_url": cfg["server_url"], "api_key": mask_key(key)})
        return 0
    finally:
        client.close()


def cmd_send(args: argparse.Namespace) -> int:
    cfg = load_config()
    key = api_key()
    client = CMCCClient(cfg, key)
    try:
        client.connect()
        mid = client.send_text(args.to, args.text)
        json_out({"ok": True, "messageId": mid, "to": args.to})
        return 0
    finally:
        client.close()


def cmd_send_file(args: argparse.Namespace) -> int:
    cfg = load_config()
    key = api_key()
    p = assert_safe_outbox_file(args.file, cfg)
    remote = upload_file(p, cfg, key)
    media_type = args.media_type or infer_media_type(p)
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    client = CMCCClient(cfg, key)
    try:
        client.connect()
        mid = client.send_media(
            media_type,
            remote,
            caption=args.caption or "",
            file_name=p.name,
            file_size=p.stat().st_size,
            mime_type=mime,
            to=args.to,
        )
        json_out({"ok": True, "messageId": mid, "mediaType": media_type, "mediaUrl": remote, "to": args.to})
        return 0
    finally:
        client.close()


def normalize_incoming(msg: dict[str, Any]) -> dict[str, Any] | None:
    typ = msg.get("type")
    if typ not in {"message", "text_message", "media_message"}:
        return None
    return {
        "id": msg.get("messageId") or msg.get("id") or str(int(time.time() * 1000)),
        "from": msg.get("from") or msg.get("phone") or "",
        "content": msg.get("content") or "",
        "timestamp": msg.get("timestamp") or int(time.time() * 1000),
        "mediaType": msg.get("mediaType"),
        "mediaUrl": msg.get("mediaUrl"),
        "mediaFileName": msg.get("mediaFileName"),
        "mediaSize": msg.get("mediaSize"),
        "mediaMimeType": msg.get("mediaMimeType"),
    }


def cmd_listen(args: argparse.Namespace) -> int:
    cfg = load_config()
    key = api_key()
    client = CMCCClient(cfg, key)
    client.connect()
    try:
        while True:
            raw = client.recv()
            if raw is None:
                continue
            msg = normalize_incoming(raw)
            if msg is None:
                if args.verbose:
                    json_out({"event": raw})
                continue
            source = str(msg.get("from") or "")
            msg["allowed"] = source_allowed(source, cfg)
            if not msg["allowed"]:
                json_out({"ok": False, "blocked": True, "message": msg})
                if args.once:
                    return 3
                continue
            if msg.get("mediaUrl") and (args.download_media or cfg.get("auto_download_media")):
                try:
                    local = safe_download(str(msg["mediaUrl"]), cfg, msg.get("mediaFileName"))
                    msg["localMediaPath"] = str(local)
                except Exception as exc:
                    msg["mediaDownloadError"] = str(exc)
            json_out({"ok": True, "message": msg})
            if args.once:
                return 0
    except KeyboardInterrupt:
        return 0
    finally:
        client.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cmcc_newmsg.py", description="中国移动新消息 / 5G 消息通用 AI / CLI 客户端")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="初始化本地状态目录与配置")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("check", help="仅检查本地配置，不联网")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("doctor", help="连接 WSS 并验证 API Key")
    s.set_defaults(func=cmd_doctor)

    s = sub.add_parser("send", help="发送文本消息")
    s.add_argument("--to", required=True, help="目标手机号/服务端 target")
    s.add_argument("--text", required=True)
    s.set_defaults(func=cmd_send)

    s = sub.add_parser("send-file", help="上传并发送 outbox 内的文件")
    s.add_argument("--file", required=True)
    s.add_argument("--to", help="可选目标；原插件富媒体回复未携带 to")
    s.add_argument("--caption", default="")
    s.add_argument("--media-type", choices=["IMAGE", "AUDIO", "VIDEO", "FILE"])
    s.set_defaults(func=cmd_send_file)

    s = sub.add_parser("listen", help="监听收到的新消息")
    s.add_argument("--once", action="store_true", help="收到一条允许消息后退出")
    s.add_argument("--download-media", action="store_true", help="按域名白名单下载媒体")
    s.add_argument("--verbose", action="store_true", help="同时显示非业务事件")
    s.set_defaults(func=cmd_listen)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:
        json_out({"ok": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
