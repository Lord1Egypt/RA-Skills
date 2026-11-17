#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CRUD CLI for Dumb Panel scheduled tasks, via the panel's own HTTP API.

ddp.exe exposes task list/logs/run/stop but no add, update or delete. Writing to
daidai.db directly works too, except the service only loads its task table at startup,
so an Administrator service restart is required before anything shows up. The API does
both halves: it writes the row and registers the job with the live scheduler, so changes
take effect immediately.

Authentication: the panel signs access tokens with Dumb-Panel/.jwt_secret. This script
reads that key plus an unexpired row from user_sessions and signs a short-lived HS256
token with matching claims (token_type must be "access"). The key, jti and token are
never printed or written anywhere.

Examples:
    python ddp_task_api.py list
    python ddp_task_api.py get 18
    python ddp_task_api.py create --name "nightly backup" \
        --command "task backups/run.py" --cron "15 3 * * *"
    python ddp_task_api.py update 18 --patch '{"cron_expression":"20 3 * * *"}'
    python ddp_task_api.py delete 19 --yes
    python ddp_task_api.py raw GET /tasks/groups
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Local calls must not go through the system proxy, or they can hang.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# Fields returned by GET /api/tasks that must not be sent back in a PUT body.
READ_ONLY = {
    "id", "created_at", "updated_at", "last_run_at", "last_run_status",
    "last_running_time", "last_skip_at", "last_skip_reason", "pid", "log_path",
    "next_run_at", "display_labels", "subscription_labels",
    "notification_channel_name", "notification_channel_enabled",
}

DEFAULT_TASK = {
    "task_type": "cron",
    "status": 1,
    "enabled": True,
    "python_version": "3.12",
    "random_delay_seconds": 0,
    "timeout": 0,
    "success_exit_codes": "0",
    "max_retries": 0,
    "retry_interval": 0,
    "env_scope": "all",
    "env_groups": [],
    "env_names": [],
    "notify_on_failure": True,
    "notify_on_success": False,
    "notify_on_abort": False,
    "notification_channel_id": 1,
    "allow_multiple_instances": False,
    "is_pinned": False,
    "labels": [],
    "task_before": "",
    "task_after": "",
    "stop_schedule": "",
    "depends_on": None,
}


def find_panel_root(explicit: str | None = None) -> Path:
    """Locate the directory that contains Dumb-Panel/ and config.yaml."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    env = os.environ.get("DAIDAI_PANEL_ROOT")
    if env:
        candidates.append(Path(env))
    for seed in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        candidates.append(seed)
        candidates.extend(seed.parents)

    seen = set()
    for c in candidates:
        key = str(c).lower()
        if key in seen:
            continue
        seen.add(key)
        if (c / "Dumb-Panel" / ".jwt_secret").is_file():
            return c
        if c.name == "Dumb-Panel" and (c / ".jwt_secret").is_file():
            return c.parent
    raise SystemExit(
        "Panel root not found (expected Dumb-Panel/.jwt_secret). "
        "Pass --panel-root or set DAIDAI_PANEL_ROOT."
    )


def panel_port(root: Path) -> int:
    cfg = root / "config.yaml"
    if cfg.is_file():
        m = re.search(r"^\s*port:\s*(\d+)", cfg.read_text(encoding="utf-8"), re.M)
        if m:
            return int(m.group(1))
    return 5700


def b64(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def make_token(root: Path) -> str:
    # Use the raw file bytes: the secret is printable text, not hex or base64.
    secret = (root / "Dumb-Panel" / ".jwt_secret").read_bytes().strip()
    db = root / "Dumb-Panel" / "daidai.db"
    conn = sqlite3.connect(str(db))
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = conn.execute(
            "SELECT s.jti, s.user_id, s.username, s.expires_at, u.role "
            "FROM user_sessions s JOIN users u ON u.id = s.user_id "
            "WHERE u.enabled = 1 ORDER BY s.id DESC"
        ).fetchall()
        row = next(
            (r for r in rows if str(r[3] or "")[:19] > now),
            rows[0] if rows else None,
        )
        if not row:
            raise SystemExit(
                "No usable login session in the database; sign in through the web UI first."
            )
        jti, user_id, username, _expires, role = row
    finally:
        conn.close()

    now_ts = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    claims = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "jti": jti,
        "token_type": "access",  # without this the server answers 401 "token type error"
        "exp": now_ts + 3600,
        "iat": now_ts,
    }
    h = b64(json.dumps(header, separators=(",", ":")).encode())
    p = b64(json.dumps(claims, separators=(",", ":")).encode())
    sig = b64(hmac.new(secret, h + b"." + p, hashlib.sha256).digest())
    return (h + b"." + p + b"." + sig).decode()


def call(root: Path, token: str, method: str, path: str, body=None):
    url = f"http://127.0.0.1:{panel_port(root)}/api{path}"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        method=method,
    )
    try:
        with OPENER.open(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", "replace")
            status = resp.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        status = exc.code
    except urllib.error.URLError as exc:
        raise SystemExit(f"Cannot reach the panel backend: {exc}")
    try:
        parsed = json.loads(raw) if raw.strip() else None
    except ValueError:
        parsed = raw
    return status, parsed


def tasks(root: Path, token: str) -> list:
    status, data = call(root, token, "GET", "/tasks")
    if status != 200:
        raise SystemExit(f"Failed to list tasks, HTTP {status}: {data}")
    return data.get("data", []) if isinstance(data, dict) else data


def brief(t: dict) -> dict:
    return {
        "id": t.get("id"),
        "name": t.get("name"),
        "command": t.get("command"),
        "cron": t.get("cron_expression"),
        "enabled": t.get("enabled"),
        "status": t.get("status"),
        "next_run_at": t.get("next_run_at"),
    }


def out(obj):
    # ensure_ascii=False keeps non-ASCII task names readable.
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def load_json_arg(value: str):
    if value.startswith("@"):
        return json.loads(Path(value[1:]).read_text(encoding="utf-8"))
    return json.loads(value)


def main() -> int:
    ap = argparse.ArgumentParser(description="Dumb Panel task CRUD over the panel Web API")
    ap.add_argument("--panel-root", help="panel root directory; auto-detected by default")
    sub = ap.add_subparsers(dest="action", required=True)

    sub.add_parser("list", help="list tasks (compact fields)")
    p = sub.add_parser("get", help="show every field of one task")
    p.add_argument("id", type=int)

    p = sub.add_parser("create", help="create a task")
    p.add_argument("--name", required=True)
    p.add_argument("--command", required=True, help='e.g. task backups/run.py')
    p.add_argument("--cron", required=True, help='e.g. "15 3 * * *"')
    p.add_argument("--delay", type=int, default=0, help="random delay in seconds")
    p.add_argument("--disabled", action="store_true", help="disable right after creation")
    p.add_argument("--json", help="extra/override fields as JSON, or @file.json")

    p = sub.add_parser("update", help="update a task (GET + merge patch + PUT)")
    p.add_argument("id", type=int)
    p.add_argument("--patch", required=True, help="fields to change, JSON or @file.json")
    p.add_argument("--patch-only", action="store_true", help="send only the patch")

    p = sub.add_parser("delete", help="delete a task record (not its script file)")
    p.add_argument("id", type=int)
    p.add_argument("--yes", action="store_true", help="skip confirmation")

    for action in ("run", "enable", "disable", "stop"):
        p = sub.add_parser(action, help=f"{action} a task")
        p.add_argument("id", type=int)

    p = sub.add_parser("raw", help="call any /api route directly")
    p.add_argument("method")
    p.add_argument("path", help="starts with /, relative to /api")
    p.add_argument("--json", help="request body as JSON or @file.json")

    args = ap.parse_args()
    root = find_panel_root(args.panel_root)
    token = make_token(root)

    if args.action == "list":
        out([brief(t) for t in tasks(root, token)])
    elif args.action == "get":
        hit = next((t for t in tasks(root, token) if t.get("id") == args.id), None)
        out(hit if hit else {"error": f"task {args.id} not found"})
    elif args.action == "create":
        body = dict(DEFAULT_TASK)
        body.update({
            "name": args.name,
            "command": args.command,
            "cron_expression": args.cron,
            "random_delay_seconds": args.delay,
        })
        if args.json:
            body.update(load_json_arg(args.json))
        status, result = call(root, token, "POST", "/tasks", body)
        # POST /tasks ignores status and enabled in the body; a separate call is needed.
        if args.disabled and status in (200, 201) and isinstance(result, dict):
            tid = (result.get("data") or {}).get("id")
            if tid:
                disabled = call(root, token, "PUT", f"/tasks/{tid}/disable")
                out({"create": [status, result], "disable": disabled})
                return 0
        out([status, result])
    elif args.action == "update":
        patch = load_json_arg(args.patch)
        if args.patch_only:
            body = patch
        else:
            cur = next((t for t in tasks(root, token) if t.get("id") == args.id), None)
            if not cur:
                raise SystemExit(f"task {args.id} not found")
            body = {k: v for k, v in cur.items() if k not in READ_ONLY}
            body.update(patch)
        out(call(root, token, "PUT", f"/tasks/{args.id}", body))
    elif args.action == "delete":
        if not args.yes:
            raise SystemExit("Deleting requires --yes. This removes the task record only, not the script file.")
        out(call(root, token, "DELETE", f"/tasks/{args.id}"))
    elif args.action in ("run", "enable", "disable", "stop"):
        out(call(root, token, "PUT", f"/tasks/{args.id}/{args.action}"))
    elif args.action == "raw":
        body = load_json_arg(args.json) if args.json else None
        out(call(root, token, args.method.upper(), args.path, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
