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
import shlex
import copy

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


def safe_profile_slug(profile_id: str) -> str:
    return (profile_id or "unknown").replace(":", "_")


def per_profile_status_path(profile_id: str) -> str:
    return f"/tmp/openclaw/codex-auth-apply-last-{safe_profile_slug(profile_id)}.json"


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


def guard_default_mutation(profile_id: str, allow_default: bool):
    if profile_id == "openai-codex:default" and not allow_default:
        print(json.dumps({
            "ok": False,
            "error": "default_profile_protected",
            "profile": profile_id,
            "hint": "Refusing to mutate/auth default profile unless explicitly allowed. Re-run with --allow-default if this is intentional.",
        }, indent=2))
        sys.exit(2)


def assert_only_target_profile_changed(before_profiles, after_profiles, target_profile, context):
    before_profiles = before_profiles or {}
    after_profiles = after_profiles or {}
    keys = set(before_profiles.keys()) | set(after_profiles.keys())
    drift = []
    for k in sorted(keys):
        if k == target_profile:
            continue
        if before_profiles.get(k) != after_profiles.get(k):
            drift.append(k)
    if drift:
        raise RuntimeError(
            f"profile_drift_detected:{context}:target={target_profile}:changed={','.join(drift)}"
        )


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


def ensure_profile_declared_in_config_obj(cfg, profile_id):
    auth = cfg.setdefault("auth", {})
    profiles = auth.setdefault("profiles", {})
    before_profiles = copy.deepcopy(profiles)
    existing = profiles.get(profile_id)
    wanted = {"provider": "openai-codex", "mode": "oauth"}
    changed = existing != wanted
    if changed:
        profiles[profile_id] = wanted
    assert_only_target_profile_changed(before_profiles, profiles, profile_id, "config")
    return changed


def ensure_profile_declared_in_config(profile_id):
    cfg = read_json(OPENCLAW_CONFIG_PATH)
    changed = ensure_profile_declared_in_config_obj(cfg, profile_id)
    backup = None
    if changed:
        backup = backup_file(OPENCLAW_CONFIG_PATH, "before-codex-auth")
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


def upsert_auth_profile_obj(store, profile_id, credentials):
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
    return store


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

        before_profiles = copy.deepcopy((store.get("profiles") or {}))
        store = upsert_auth_profile_obj(store, profile_id, credentials)
        assert_only_target_profile_changed(before_profiles, store.get("profiles") or {}, profile_id, "auth")
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


def stop_gateway_processes():
    # Avoid `openclaw gateway stop` because CLI config parsing may fail.
    subprocess.run(["pkill", "-TERM", "-f", "^openclaw-gateway$"], capture_output=True, text=True)
    time.sleep(3)
    subprocess.run(["pkill", "-KILL", "-f", "^openclaw-gateway$"], capture_output=True, text=True)
    time.sleep(1)


def start_gateway_process():
    os.makedirs("/tmp/openclaw", exist_ok=True)
    log_path = "/tmp/openclaw/codex-auth-gateway-start.log"
    lf = open(log_path, "a", encoding="utf-8")

    # Prefer direct gateway binary when present.
    gw_bin = shutil.which("openclaw-gateway")
    if gw_bin:
        subprocess.Popen([gw_bin], stdout=lf, stderr=lf, stdin=subprocess.DEVNULL, start_new_session=True)
        return log_path

    # Fallback for installs where only the CLI is on PATH.
    oc_bin = shutil.which("openclaw")
    if not oc_bin:
        raise FileNotFoundError("Neither 'openclaw-gateway' nor 'openclaw' found on PATH")

    subprocess.run([oc_bin, "gateway", "start"], stdout=lf, stderr=lf, stdin=subprocess.DEVNULL, check=False)
    return log_path


def wait_gateway_live(timeout_sec=25):
    deadline = time.time() + timeout_sec
    url = "http://127.0.0.1:18789/health"
    last_err = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                if '"ok":true' in raw or '"status":"live"' in raw:
                    return True, raw[:200]
        except Exception as e:
            last_err = str(e)
        time.sleep(1)
    return False, (last_err or "health_check_timeout")


def apply_with_gateway_restart(payload_path, auth_path):
    payload = read_json(payload_path)
    profile_id = payload["profile"]
    tokens = payload["tokens"]

    # backups + revert command
    cfg_bak = backup_file(OPENCLAW_CONFIG_PATH, "before-codex-auth-apply")
    auth_bak = backup_file(auth_path, "before-codex-auth-apply")
    revert_cmd = f"cp '{cfg_bak}' '{OPENCLAW_CONFIG_PATH}' && cp '{auth_bak}' '{auth_path}' && openclaw gateway restart"

    err = []
    ok = True

    # Build staged copies first (while gateway may still be running)
    stage_dir = "/tmp/openclaw"
    os.makedirs(stage_dir, exist_ok=True)
    ts = int(time.time())
    staged_cfg = os.path.join(stage_dir, f"openclaw.staged.{ts}.json")
    staged_auth = os.path.join(stage_dir, f"auth-profiles.staged.{ts}.json")

    try:
        if os.path.exists(OPENCLAW_CONFIG_PATH):
            shutil.copy2(OPENCLAW_CONFIG_PATH, staged_cfg)
        else:
            write_json_atomic(staged_cfg, {})
        if os.path.exists(auth_path):
            shutil.copy2(auth_path, staged_auth)
        else:
            write_json_atomic(staged_auth, {})

        cfg = read_json(staged_cfg)
        ensure_profile_declared_in_config_obj(cfg, profile_id)
        write_json_atomic(staged_cfg, cfg)

        store = read_json(staged_auth)
        before_profiles = copy.deepcopy((store.get("profiles") or {}))
        store = upsert_auth_profile_obj(store, profile_id, tokens)
        assert_only_target_profile_changed(before_profiles, store.get("profiles") or {}, profile_id, "apply_auth")
        write_json_atomic(staged_auth, store)

        if not (read_json(staged_auth).get("profiles", {}).get(profile_id)):
            raise RuntimeError("staged_auth_missing_profile_after_write")
    except Exception as e:
        ok = False
        err.append({"step": "stage", "error": str(e)})

    # Activate staged files only while gateway is stopped
    if ok:
        try:
            stop_gateway_processes()
        except Exception as e:
            ok = False
            err.append({"step": "stop", "error": str(e)})

    if ok:
        try:
            shutil.copy2(staged_cfg, OPENCLAW_CONFIG_PATH)
            os.makedirs(os.path.dirname(auth_path), exist_ok=True)
            shutil.copy2(staged_auth, auth_path)
        except Exception as e:
            ok = False
            err.append({"step": "activate", "error": str(e)})

    gateway_start_log = None
    if ok:
        try:
            gateway_start_log = start_gateway_process()
            live_ok, health_note = wait_gateway_live(timeout_sec=25)
            if not live_ok:
                ok = False
                err.append({"step": "start", "error": f"gateway_not_live:{health_note}"})
        except Exception as e:
            ok = False
            err.append({"step": "start", "error": str(e)})

    out = {
        "ok": ok,
        "profile": profile_id,
        "revert_command": revert_cmd,
        "staged": {
            "config": staged_cfg,
            "auth": staged_auth,
        },
        "gateway_start_log": gateway_start_log,
        "errors": err,
        "ts": int(time.time() * 1000),
    }
    write_json_atomic(APPLY_STATUS_PATH, out)
    write_json_atomic(per_profile_status_path(profile_id), out)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s_start = sub.add_parser("start")
    s_start.add_argument("--profile", default="default")
    s_start.add_argument("--auth-path", default=AUTH_PATH_DEFAULT)
    s_start.add_argument("--allow-default", action="store_true", help="Required to mutate/auth the default profile")

    s_finish = sub.add_parser("finish")
    s_finish.add_argument("--profile", default="default")
    s_finish.add_argument("--callback-url", required=True)
    s_finish.add_argument("--auth-path", default=AUTH_PATH_DEFAULT)
    s_finish.add_argument("--queue-apply", action="store_true", default=True, help="Queue stop/write/start apply script in background (strict default)")
    s_finish.add_argument("--allow-default", action="store_true", help="Required to mutate/auth the default profile")
    s_finish.add_argument("--allow-unsafe-direct", action="store_true", help="Allow direct in-process writes without off-host stop/write/start (not recommended)")

    s_apply = sub.add_parser("apply")
    s_apply.add_argument("--payload", required=True)
    s_apply.add_argument("--auth-path", default=AUTH_PATH_DEFAULT)
    s_apply.add_argument("--allow-default", action="store_true", help="Required to mutate/auth the default profile")

    s_status = sub.add_parser("status")
    s_status.add_argument("--profile", default=None, help="Optional profile suffix/id for per-profile apply status")

    args = ap.parse_args()

    if args.cmd == "status":
        chosen = APPLY_STATUS_PATH
        if args.profile:
            pid = resolve_profile_id(args.profile)
            candidate = per_profile_status_path(pid)
            if os.path.exists(candidate):
                chosen = candidate
        if os.path.exists(chosen):
            out = read_json(chosen)
            if isinstance(out, dict):
                out.setdefault("status_path", chosen)
            print(json.dumps(out, indent=2))
        else:
            print(json.dumps({"ok": False, "error": "no_status", "status_path": chosen}, indent=2))
        return

    if args.cmd == "apply":
        payload_preview = read_json(args.payload)
        guard_default_mutation(payload_preview.get("profile"), getattr(args, "allow_default", False))
        out = apply_with_gateway_restart(args.payload, args.auth_path)
        print(json.dumps(out, indent=2))
        if not out.get("ok"):
            sys.exit(2)
        return

    if args.cmd == "start":
        profile_id = resolve_profile_id(args.profile)
        guard_default_mutation(profile_id, getattr(args, "allow_default", False))
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
        guard_default_mutation(profile_id, getattr(args, "allow_default", False))
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
            safe_profile = safe_profile_slug(profile_id)
            payload_path = f"/tmp/openclaw/codex-auth-apply-{safe_profile}.json"
            script_path = f"/tmp/openclaw/codex-auth-apply-{safe_profile}.sh"
            log_path = f"/tmp/openclaw/codex-auth-apply-{safe_profile}.log"
            status_path = per_profile_status_path(profile_id)
            write_json_atomic(payload_path, {"profile": profile_id, "tokens": tokens})

            py = shlex.quote(sys.executable or "python3")
            this_file = shlex.quote(os.path.abspath(__file__))
            payload_q = shlex.quote(payload_path)
            auth_q = shlex.quote(args.auth_path)
            log_q = shlex.quote(log_path)
            allow_default_flag = " --allow-default" if (profile_id == "openai-codex:default" and args.allow_default) else ""

            script = f"""#!/usr/bin/env bash
set -euo pipefail
{{
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] codex-auth apply start profile={profile_id}";
  {py} {this_file} apply --payload {payload_q} --auth-path {auth_q}{allow_default_flag};
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] codex-auth apply done profile={profile_id}";
}} >> {log_q} 2>&1
"""
            Path(script_path).write_text(script, encoding="utf-8")
            os.chmod(script_path, 0o700)

            launcher = "nohup"
            unit_name = f"codex-auth-apply-{safe_profile}-{int(time.time())}"
            try:
                sd = subprocess.run(
                    ["systemd-run", "--user", "--unit", unit_name, "--collect", "/bin/bash", script_path],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                if sd.returncode == 0:
                    launcher = "systemd-run"
                else:
                    subprocess.Popen(["nohup", "bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            except Exception:
                subprocess.Popen(["nohup", "bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

            print(json.dumps({
                "ok": True,
                "profile": profile_id,
                "accountId": account_id,
                "expires": tokens["expires"],
                "queued": True,
                "launcher": launcher,
                "warning": "Strict mode: off-host stop/write/start apply script scheduled. Avoid long-running tasks.",
                "status_command": f"python3 {os.path.abspath(__file__)} status --profile {args.profile}",
                "status_path": status_path,
                "log_path": log_path,
                "script_path": script_path,
                "payload_path": payload_path,
            }, indent=2))
            return

        if not args.allow_unsafe_direct:
            print(json.dumps({
                "ok": False,
                "error": "strict_mode_requires_queue_apply",
                "hint": "This skill now enforces off-host queue apply by default. Re-run with --queue-apply (default) or explicitly pass --allow-unsafe-direct if you truly need direct write.",
            }, indent=2))
            sys.exit(2)

        # Unsafe direct path (explicitly opt-in only)
        cfg_res = ensure_profile_declared_in_config(profile_id)
        auth_backup = update_auth_profile(args.auth_path, profile_id, tokens)
        backups = {"config": cfg_res.get("backup"), "auth": auth_backup}
        revert_cmd = build_revert_command(backups)
        out = {
            "ok": True,
            "profile": profile_id,
            "accountId": account_id,
            "expires": tokens["expires"],
            "message": "Auth profile updated (unsafe direct path).",
            "restart_required": bool(cfg_res.get("changed")),
            "pre_restart_message": "Run this command to revert back if failed",
            "revert_command": revert_cmd,
        }
        if cfg_res.get("changed"):
            out["config_note"] = "Profile declaration added to openclaw.json; restart gateway to apply config profile mapping."
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
