from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


TELEGRAM_DIRECT_RE = re.compile(r"^agent:[^:]+:telegram:direct:(?P<chat_id>-?\d+)$")
TELEGRAM_GROUP_RE = re.compile(r"^agent:[^:]+:telegram:group:(?P<chat_id>-?\d+)(?::topic:(?P<topic_id>\d+))?$")


def load_openclaw_config() -> Dict[str, Any]:
    cfg_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    if not cfg_path:
        cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        raw = Path(cfg_path).read_text(encoding="utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load_openclaw_gateway_password() -> Optional[str]:
    cfg = load_openclaw_config()
    pw = (((cfg.get("gateway") or {}).get("auth") or {}).get("password"))
    return pw if isinstance(pw, str) and pw else None


def load_openclaw_gateway_port() -> Optional[int]:
    cfg = load_openclaw_config()
    port = (cfg.get("gateway") or {}).get("port")
    try:
        return int(port)
    except Exception:
        return None


def gateway_url() -> str:
    explicit = (os.environ.get("OPENCLAW_GATEWAY_URL") or "").strip()
    if explicit:
        return explicit

    raw_port = (os.environ.get("OPENCLAW_GATEWAY_PORT") or "").strip()
    if raw_port:
        try:
            return f"http://127.0.0.1:{int(raw_port)}"
        except Exception:
            pass

    port = load_openclaw_gateway_port()
    if port is None:
        port = 18188
    return f"http://127.0.0.1:{port}"


def auth_header() -> Dict[str, str]:
    token = (os.environ.get("OPENCLAW_GATEWAY_TOKEN") or "").strip()
    if token:
        return {"Authorization": f"Bearer {token}"}

    pw = (os.environ.get("OPENCLAW_GATEWAY_PASSWORD") or "").strip() or load_openclaw_gateway_password()
    if pw:
        return {"Authorization": f"Bearer {pw}"}

    return {}


def tools_invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    url = gateway_url().rstrip("/") + "/tools/invoke"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", **auth_header()}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        return data if isinstance(data, dict) else {"ok": False, "error": {"message": "invalid gateway payload"}}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return {"ok": False, "error": {"type": "http", "message": f"HTTP {e.code}: {detail}"}}
    except Exception as e:
        return {"ok": False, "error": {"type": "net", "message": str(e)}}


def infer_message_route(session_key: str) -> Optional[Dict[str, Any]]:
    value = (session_key or "").strip()

    m = TELEGRAM_DIRECT_RE.match(value)
    if m:
        return {"channel": "telegram", "target": m.group("chat_id")}

    m = TELEGRAM_GROUP_RE.match(value)
    if m:
        out: Dict[str, Any] = {"channel": "telegram", "target": m.group("chat_id")}
        if m.group("topic_id"):
            out["threadId"] = m.group("topic_id")
        return out

    return None


def send_message(
    session_key: str,
    text: str,
    buttons: Optional[List[List[Dict[str, str]]]] = None,
    silent: bool = False,
) -> Dict[str, Any]:
    route = infer_message_route(session_key)
    if not route:
        return {"ok": False, "error": {"type": "route", "message": f"cannot infer target from sessionKey: {session_key}"}}

    args: Dict[str, Any] = {**route, "message": text}
    if buttons is not None:
        args["buttons"] = buttons
    if silent:
        args["silent"] = True

    payload = {"tool": "message", "action": "send", "args": args, "sessionKey": session_key}
    return tools_invoke(payload)


def edit_message(
    session_key: str,
    message_id: str,
    text: str,
    buttons: Optional[List[List[Dict[str, str]]]] = None,
) -> Dict[str, Any]:
    route = infer_message_route(session_key)
    if not route:
        return {"ok": False, "error": {"type": "route", "message": f"cannot infer target from sessionKey: {session_key}"}}

    args: Dict[str, Any] = {**route, "messageId": str(message_id), "message": text}
    if buttons is not None:
        args["buttons"] = buttons

    payload = {"tool": "message", "action": "edit", "args": args, "sessionKey": session_key}
    return tools_invoke(payload)


def extract_message_id(resp: Dict[str, Any]) -> Optional[str]:
    def scan(obj: Any) -> Optional[str]:
        if isinstance(obj, dict):
            for key in ("messageId", "message_id", "id"):
                value = obj.get(key)
                if isinstance(value, (str, int)) and str(value):
                    return str(value)
            for key in ("details", "result", "data", "output"):
                if key in obj:
                    found = scan(obj.get(key))
                    if found:
                        return found
        elif isinstance(obj, list):
            for item in obj:
                found = scan(item)
                if found:
                    return found
        return None

    return scan(resp)
