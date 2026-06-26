#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
import fcntl
import shutil
import subprocess

AUTH_PATH_DEFAULT = str(Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json")
PENDING_PATH = "/tmp/openclaw/codex-auth-pending.json"

CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
AUTHORIZE_URL = "https://auth.openai.com/oauth/authorize"
TOKEN_URL = "https://auth.openai.com/oauth/token"
REDIRECT_URI = "http://localhost:1455/auth/callback"
SCOPE = "openid profile email offline_access"
JWT_CLAIM_PATH = "https://api.openai.com/auth"
OPENCLAW_CONFIG_PATH = str(Path.home() / ".openclaw" / "openclaw.json")
BACKUP_DIR = "/tmp/openclaw/safety-backups"
APPLY_STATUS_PATH = "/tmp/openclaw/codex-auth-apply-last.json"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def generate_pkce():
    verifier = b64url(os.urandom(32))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


def create_state():
    return b64url(os.urandom(16))


def decode_jwt(token: str):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        payload += "=" * (-len(payload) % 4)
        raw = base64.urlsafe_b64decode(payload.encode())
        return json.loads(raw.decode())
    except Exception:
        return None


def get_account_id(access_token: str):
    payload = decode_jwt(access_token) or {}
    auth = payload.get(JWT_CLAIM_PATH) or {}
    account_id = auth.get("chatgpt_account_id")
    return account_id if isinstance(account_id, str) and account_id else None


def parse_callback_input(value: str):
    value = value.strip()
    if not value:
        return None, None
    try:
        u = urllib.parse.urlparse(value)
        qs = urllib.parse.parse_qs(u.query)
        code = (qs.get("code") or [None])[0]
        state = (qs.get("state") or [None])[0]
        return code, state
    except Exception:
        pass
    if value.startswith("code=") or "&" in value:
        qs = urllib.parse.parse_qs(value)
        code = (qs.get("code") or [None])[0]
        state = (qs.get("state") or [None])[0]
        return code, state
    if "#" in value:
        code, state = value.split("#", 1)
        return code, state
    return value, None


def resolve_profile_id(selector: str):
    selector = (selector or "default").strip()
    if selector.startswith("openai-codex:"):
        return selector
    if selector == "default":
        return "openai-codex:default"
    return f"openai-codex:{selector}"


def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def backup_file(path, tag):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = int(time.time())
    base = os.path.basename(path)
    out = os.path.join(BACKUP_DIR, f"{base}.{tag}.{ts}.bak")
    if os.path.exists(path):
        shutil.copy2(path, out)
    else:
        Path(out).write_text("", encoding="utf-8")
    return out


def build_revert_command(backups):
    ops = []
    if backups.get("config"):
        ops.append(f"cp '{backups['config']}' '{OPENCLAW_CONFIG_PATH}'")
    if backups.get("auth"):
        ops.append(f"cp '{backups['auth']}' '{AUTH_PATH_DEFAULT}'")
    ops.append("openclaw gateway restart")
    return " && ".join(ops)


def ensure_profile_declared_in_config(profile_id):
    cfg = read_json(OPENCLAW_CONFIG_PATH)
    auth = cfg.setdefault("auth", {})
    profiles = auth.setdefault("profiles", {})
    existing = profiles.get(profile_id)
    wanted = {"provider": "openai-codex", "mode": "oauth"}
    changed = existing != wanted
    backup = None
    if changed:
        backup = backup_file(OPENCLAW_CONFIG_PATH, "before-codex-auth")
        profiles[profile_id] = wanted
        write_json_atomic(OPENCLAW_CONFIG_PATH, cfg)
    return {"changed": changed, "backup": backup}


def save_pending(profile_id, verifier, state):
    pending = read_json(PENDING_PATH)
    pending[profile_id] = {
        "verifier": verifier,
        "state": state,
        "createdAt": int(time.time() * 1000)
    }
    os.makedirs(os.path.dirname(PENDING_PATH), exist_ok=True)
    write_json_atomic(PENDING_PATH, pending)


def load_pending(profile_id):
    pending = read_json(PENDING_PATH)
    return pending.get(profile_id)


def exchange_code(code, verifier):
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": REDIRECT_URI,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    data = json.loads(raw)
    if not data.get("access_token") or not data.get("refresh_token") or not isinstance(data.get("expires_in"), (int, float)):
        raise RuntimeError("Token exchange missing fields")
    return {
        "access": data["access_token"],
        "refresh": data["refresh_token"],
        "expires": int(time.time() * 1000) + int(data["expires_in"] * 1000),
    }


def update_auth_profile(auth_path, profile_id, credentials):
    os.makedirs(os.path.dirname(auth_path), exist_ok=True)
    backup = backup_file(auth_path, "before-codex-auth")
    # lock + read existing
    with open(auth_path, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        try:
            raw = f.read().strip()
            store = json.loads(raw) if raw else {}
        except Exception:
            store = {}
        store.setdefault("profiles", {})
        store.setdefault("usageStats", {})
        store.setdefault("order", {})
        store["profiles"][profile_id] = {
            "provider": "openai-codex",
            "type": "oauth",
            "access": credentials["access"],
            "refresh": credentials["refresh"],
            "expires": credentials["expires"],
            "accountId": credentials["accountId"],
        }

        provider_order = store["order"].get("openai-codex")
        if not isinstance(provider_order, list):
            provider_order = []
        if profile_id not in provider_order:
            provider_order.append(profile_id)
        store["order"]["openai-codex"] = provider_order

        write_json_atomic(auth_path, store)
        fcntl.flock(f, fcntl.LOCK_UN)
    return backup


def build_auth_url(verifier, state):
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "code_challenge": b64url(hashlib.sha256(verifier.encode()).digest()),
        "code_challenge_method": "S256",
        "state": state,
        "id_token_add_organizations": "true",
        "codex_cli_simplified_flow": "true",
        "originator": "pi",
    }
    return AUTHORIZE_URL + "?" + urllib.parse.urlencode(params)


def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def apply_with_gateway_restart(payload_path, auth_path):
    payload = read_json(payload_path)
    profile_id = payload["profile"]
    tokens = payload["tokens"]

    # backups + revert command
    cfg_bak = backup_file(OPENCLAW_CONFIG_PATH, "before-codex-auth-apply")
    auth_bak = backup_file(auth_path, "before-codex-auth-apply")
    revert_cmd = f"cp '{cfg_bak}' '{OPENCLAW_CONFIG_PATH}' && cp '{auth_bak}' '{auth_path}' && openclaw gateway restart"

    stop = run_cmd(["openclaw", "gateway", "stop"])
    ok = stop.returncode == 0
    err = []
    if not ok:
        err.append({"step": "stop", "stderr": stop.stderr[-800:]})

    try:
        ensure_profile_declared_in_config(profile_id)
        update_auth_profile(auth_path, profile_id, tokens)
    except Exception as e:
        ok = False
        err.append({"step": "write", "error": str(e)})

    start = run_cmd(["openclaw", "gateway", "start"])
    if start.returncode != 0:
        ok = False
        err.append({"step": "start", "stderr": start.stderr[-800:]})

    out = {
        "ok": ok,
        "profile": profile_id,
        "revert_command": revert_cmd,
        "errors": err,
        "ts": int(time.time() * 1000),
    }
    write_json_atomic(APPLY_STATUS_PATH, out)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s_start = sub.add_parser("start")
    s_start.add_argument("--profile", default="default")
    s_start.add_argument("--auth-path", default=AUTH_PATH_DEFAULT)

    s_finish = sub.add_parser("finish")
    s_finish.add_argument("--profile", default="default")
    s_finish.add_argument("--callback-url", required=True)
    s_finish.add_argument("--auth-path", default=AUTH_PATH_DEFAULT)
    s_finish.add_argument("--queue-apply", action="store_true", help="Queue stop/write/start apply script in background")

    s_apply = sub.add_parser("apply")
    s_apply.add_argument("--payload", required=True)
    s_apply.add_argument("--auth-path", default=AUTH_PATH_DEFAULT)

    s_status = sub.add_parser("status")

    args = ap.parse_args()

    if args.cmd == "status":
        if os.path.exists(APPLY_STATUS_PATH):
            print(json.dumps(read_json(APPLY_STATUS_PATH), indent=2))
        else:
            print(json.dumps({"ok": False, "error": "no_status"}, indent=2))
        return

    if args.cmd == "apply":
        out = apply_with_gateway_restart(args.payload, args.auth_path)
        print(json.dumps(out, indent=2))
        if not out.get("ok"):
            sys.exit(2)
        return

    if args.cmd == "start":
        profile_id = resolve_profile_id(args.profile)
        verifier, _challenge = generate_pkce()
        state = create_state()
        save_pending(profile_id, verifier, state)
        url = build_auth_url(verifier, state)
        print(json.dumps({
            "ok": True,
            "profile": profile_id,
            "login_url": url,
            "redirect_uri": REDIRECT_URI,
            "instructions": "Open the login_url in your browser, then paste the localhost redirect URL back using the finish command.",
        }, indent=2))
        return

    if args.cmd == "finish":
        profile_id = resolve_profile_id(args.profile)
        pending = load_pending(profile_id)
        if not pending:
            print(json.dumps({"ok": False, "error": "no_pending_flow", "profile": profile_id}, indent=2))
            sys.exit(2)
        code, state = parse_callback_input(args.callback_url)
        if not code:
            print(json.dumps({"ok": False, "error": "missing_code"}, indent=2))
            sys.exit(2)
        if pending.get("state") and state and pending["state"] != state:
            print(json.dumps({"ok": False, "error": "state_mismatch"}, indent=2))
            sys.exit(2)
        tokens = exchange_code(code, pending["verifier"])
        account_id = get_account_id(tokens["access"])
        if not account_id:
            print(json.dumps({"ok": False, "error": "missing_account_id"}, indent=2))
            sys.exit(2)
        tokens["accountId"] = account_id

        if args.queue_apply:
            os.makedirs("/tmp/openclaw", exist_ok=True)
            payload_path = f"/tmp/openclaw/codex-auth-apply-{profile_id.replace(':','_')}.json"
            write_json_atomic(payload_path, {"profile": profile_id, "tokens": tokens})
            cmd = [
                "nohup",
                "python3",
                os.path.abspath(__file__),
                "apply",
                "--payload",
                payload_path,
                "--auth-path",
                args.auth_path,
            ]
            with open("/tmp/openclaw/codex-auth-apply.log", "a", encoding="utf-8") as lf:
                subprocess.Popen(cmd, stdout=lf, stderr=lf, stdin=subprocess.DEVNULL)
            print(json.dumps({
                "ok": True,
                "profile": profile_id,
                "accountId": account_id,
                "expires": tokens["expires"],
                "queued": True,
                "warning": "Gateway restart will be performed by background apply job. Avoid long-running tasks.",
                "status_command": f"python3 {os.path.abspath(__file__)} status",
                "log_path": "/tmp/openclaw/codex-auth-apply.log",
            }, indent=2))
            return

        # Non-queued path: write immediately (no restart), may be reconciled later.
        cfg_res = ensure_profile_declared_in_config(profile_id)
        auth_backup = update_auth_profile(args.auth_path, profile_id, tokens)
        backups = {"config": cfg_res.get("backup"), "auth": auth_backup}
        revert_cmd = build_revert_command(backups)
        out = {
            "ok": True,
            "profile": profile_id,
            "accountId": account_id,
            "expires": tokens["expires"],
            "message": "Auth profile updated.",
            "restart_required": bool(cfg_res.get("changed")),
            "pre_restart_message": "Run this command to revert back if failed",
            "revert_command": revert_cmd,
        }
        if cfg_res.get("changed"):
            out["config_note"] = "Profile declaration added to openclaw.json; restart gateway to apply config profile mapping."
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
