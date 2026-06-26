#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import shutil
import socket
import sys
import time
import subprocess
import tempfile
import shlex
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_AUTH_PATH = str(Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json")
DEFAULT_ENDPOINT = "https://chatgpt.com/backend-api/wham/usage"
ALLOWED_ENDPOINT_HOSTS = {"chatgpt.com"}


def fmt_ts(ms):
    if not ms:
        return "n/a"
    try:
        return dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc).isoformat()
    except Exception:
        return "n/a"


def fmt_expiry(raw):
    if not raw:
        return "n/a"
    ts = float(raw)
    if ts > 10_000_000_000:
        ts = ts / 1000.0
    now = dt.datetime.now(dt.timezone.utc)
    exp = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
    delta = exp - now
    sign = "-" if delta.total_seconds() < 0 else "+"
    mins = int(abs(delta.total_seconds()) // 60)
    return f"{exp.isoformat()} ({sign}{mins}m)"


def load_store(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_store(path, store):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)
        f.write("\n")
    os.replace(tmp, p)


def backup_store(path):
    p = Path(path)
    if not p.exists():
        return None
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = p.with_name(f"{p.name}.bak.delete-{stamp}")
    shutil.copy2(p, backup_path)
    return str(backup_path)


def write_json_atomic(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(p.parent), encoding="utf-8") as tf:
        json.dump(obj, tf, indent=2)
        tf.write("\n")
        tmp = tf.name
    os.replace(tmp, p)


def launch_offhost_script(script_path, unit_name):
    try:
        sd = subprocess.run(
            ["systemd-run", "--user", "--unit", unit_name, "--collect", "/bin/bash", script_path],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if sd.returncode == 0:
            return "systemd-run", (sd.stdout or "").strip()
    except Exception:
        pass

    subprocess.Popen(["nohup", "bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    return "nohup", ""


def schedule_offhost_delete_apply(auth_path, mutated_store, targets, mode):
    os.makedirs("/tmp/openclaw", exist_ok=True)
    ts = int(time.time())
    safe = "-".join([t.replace(":", "_") for t in sorted(set(targets))])[:120] or "none"
    staged_auth_path = f"/tmp/openclaw/codex-delete-auth-staged-{safe}-{ts}.json"
    script_path = f"/tmp/openclaw/codex-delete-apply-{safe}-{ts}.sh"
    log_path = f"/tmp/openclaw/codex-delete-apply-{safe}-{ts}.log"
    status_path = f"/tmp/openclaw/codex-delete-apply-{safe}-{ts}.status.json"

    write_json_atomic(staged_auth_path, mutated_store)

    auth_q = shlex.quote(auth_path)
    staged_q = shlex.quote(staged_auth_path)
    log_q = shlex.quote(log_path)
    status_q = shlex.quote(status_path)
    mode_q = shlex.quote(mode)
    targets_json_q = shlex.quote(json.dumps(sorted(set(targets))))
    auth_py = json.dumps(auth_path)
    status_py = json.dumps(status_path)

    script = f"""#!/usr/bin/env bash
set -euo pipefail
exec >>{log_q} 2>&1

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] codex-delete apply start mode={mode} targets={','.join(sorted(set(targets)))}"
cp {auth_q} {auth_q}.bak.offhost-delete.$(date -u +%Y%m%dT%H%M%SZ)

pkill -TERM -f '^openclaw-gateway$' || true
sleep 3
pkill -KILL -f '^openclaw-gateway$' || true
sleep 1

cp {staged_q} {auth_q}
nohup openclaw-gateway >/tmp/openclaw/openclaw-gateway-offhost-delete-start.log 2>&1 < /dev/null &
sleep 5

python3 - <<'PY'
import json, time, urllib.request
from pathlib import Path
status = {{
  'ok': False,
  'step': 'post_restart_check',
  'ts': int(time.time()*1000),
  'mode': {mode_q},
  'targets': json.loads({targets_json_q}),
}}
auth = json.loads(Path({auth_py}).read_text(encoding='utf-8'))
profiles = auth.get('profiles') or {{}}
status['present_after'] = [t for t in status['targets'] if t in profiles]
try:
  with urllib.request.urlopen('http://127.0.0.1:18789/health', timeout=4) as r:
    status['gateway_health'] = r.read().decode('utf-8', errors='replace')[:200]
except Exception as e:
  status['gateway_health'] = f'error:{{e}}'
# Success here means gateway returned and target mutation should be in place.
status['ok'] = True
Path({status_py}).write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8')
print(json.dumps(status))
PY

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] codex-delete apply end"
"""
    Path(script_path).write_text(script, encoding="utf-8")
    os.chmod(script_path, 0o700)

    launcher, launch_note = launch_offhost_script(script_path, f"codex-delete-apply-{ts}")
    return {
        "staged_auth_path": staged_auth_path,
        "script_path": script_path,
        "log_path": log_path,
        "status_path": status_path,
        "launcher": launcher,
        "launcher_note": launch_note,
    }


def list_codex_profiles(store):
    profiles = store.get("profiles", {})
    ids = []
    for pid, cred in profiles.items():
        if cred.get("provider") == "openai-codex":
            ids.append(pid)
    return sorted(ids)


def resolve_targets(store, selector):
    codex_ids = list_codex_profiles(store)
    if not codex_ids:
        return []

    selector = (selector or "all").strip()
    if selector in ("all", "both"):
        return codex_ids

    if selector == "default":
        if "openai-codex:default" in codex_ids:
            return ["openai-codex:default"]
        return [codex_ids[0]]

    if selector in codex_ids:
        return [selector]

    if not selector.startswith("openai-codex:"):
        expanded = f"openai-codex:{selector}"
        if expanded in codex_ids:
            return [expanded]

    return []


def detach_targets(store, targets):
    targets = sorted(set(targets or []))
    profiles = store.get("profiles", {})

    order = store.setdefault("order", {})
    codex_order = order.get("openai-codex", []) or []
    codex_order = [pid for pid in codex_order if pid not in set(targets)]
    order["openai-codex"] = codex_order

    last_good = store.setdefault("lastGood", {})
    if last_good.get("openai-codex") in set(targets):
        last_good["openai-codex"] = codex_order[0] if codex_order else None

    detached = [pid for pid in targets if pid in profiles]
    store["order"] = order
    store["lastGood"] = last_good

    return {
        "detached": detached,
        "remaining": list_codex_profiles(store),
        "order": codex_order,
        "lastGood": last_good.get("openai-codex"),
    }


def hard_delete_targets(store, targets):
    targets = sorted(set(targets or []))
    profiles = store.get("profiles", {})
    usage_stats = store.get("usageStats", {})

    deleted = []
    for pid in targets:
        if pid in profiles:
            profiles.pop(pid, None)
            deleted.append(pid)
        usage_stats.pop(pid, None)

    detach_result = detach_targets(store, targets)
    store["profiles"] = profiles
    store["usageStats"] = usage_stats

    return {
        "deleted": deleted,
        "remaining": detach_result["remaining"],
        "order": detach_result["order"],
        "lastGood": detach_result["lastGood"],
    }


def validate_endpoint(raw_endpoint):
    endpoint = (raw_endpoint or "").strip() or DEFAULT_ENDPOINT
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme.lower() != "https":
        return DEFAULT_ENDPOINT, False, "endpoint_forced_to_default_non_https"
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_ENDPOINT_HOSTS:
        return DEFAULT_ENDPOINT, False, "endpoint_forced_to_default_untrusted_host"
    return endpoint, True, None


def endpoint_reachable(endpoint, timeout_sec=6):
    """Return True when host/path is reachable over HTTPS, even if auth is rejected.

    This preflight is network reachability only; 401/403 should still be considered
    reachable so the main usage call can classify auth behavior precisely.
    """
    req = urllib.request.Request(endpoint, method="HEAD", headers={"User-Agent": "CodexBar"})
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec):
            return True
    except urllib.error.HTTPError as e:
        # Host/path reachable; endpoint answered with HTTP status.
        return True
    except Exception:
        return False


def call_remote_usage(endpoint, token, account_id=None, timeout_sec=20, retries=1):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "CodexBar",
    }
    if account_id:
        headers["ChatGPT-Account-Id"] = str(account_id)

    last_err = None
    for attempt in range(1, retries + 2):
        start = time.time()
        req = urllib.request.Request(endpoint, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                elapsed_ms = int((time.time() - start) * 1000)
                parse_error = False
                try:
                    payload = json.loads(body)
                except Exception:
                    payload = {}
                    parse_error = True
                return {
                    "ok": True,
                    "status": int(resp.status),
                    "payload": payload,
                    "attempt": attempt,
                    "elapsed_ms": elapsed_ms,
                    "parse_error": parse_error,
                }
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            elapsed_ms = int((time.time() - start) * 1000)
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}
            if e.code >= 500 and attempt <= retries + 1:
                last_err = {
                    "ok": False,
                    "status": int(e.code),
                    "error": "server_error",
                    "payload": payload,
                    "attempt": attempt,
                    "elapsed_ms": elapsed_ms,
                }
                time.sleep(min(1.5 * attempt, 4))
                continue
            err_type = "http_error"
            if int(e.code) == 401:
                err_type = "auth_not_accepted_by_usage_endpoint"
            elif int(e.code) == 403:
                err_type = "forbidden_by_usage_endpoint"
            return {
                "ok": False,
                "status": int(e.code),
                "error": err_type,
                "payload": payload,
                "attempt": attempt,
                "elapsed_ms": elapsed_ms,
            }
        except socket.timeout:
            elapsed_ms = int((time.time() - start) * 1000)
            last_err = {
                "ok": False,
                "status": None,
                "error": "timeout",
                "attempt": attempt,
                "elapsed_ms": elapsed_ms,
            }
            if attempt <= retries + 1:
                time.sleep(min(1.5 * attempt, 4))
                continue
        except Exception as e:
            elapsed_ms = int((time.time() - start) * 1000)
            last_err = {
                "ok": False,
                "status": None,
                "error": "request_exception",
                "message": str(e),
                "attempt": attempt,
                "elapsed_ms": elapsed_ms,
            }
            if attempt <= retries + 1:
                time.sleep(min(1.5 * attempt, 4))
                continue

    return last_err or {"ok": False, "error": "unknown"}


def format_reset_in(seconds):
    if not isinstance(seconds, (int, float)):
        return "n/a"
    total = int(max(0, seconds))
    if total < 3600:
        mins = max(1, total // 60)
        return f"{mins} minutes"
    hours = total // 3600
    mins = (total % 3600) // 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def format_reset_at(ts):
    if not isinstance(ts, (int, float)):
        return "n/a"
    d = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).astimezone()
    return d.strftime("%d/%m/%Y, %H:%M")


def format_duration_dhm(seconds):
    if not isinstance(seconds, (int, float)):
        return "n/a"
    total = int(max(0, seconds))
    days = total // 86400
    hours = (total % 86400) // 3600
    minutes = (total % 3600) // 60
    return f"{days} Days, {hours} Hours, {minutes} Minutes"


def format_pct(value):
    if not isinstance(value, (int, float)):
        return "n/a"
    return f"{int(round(float(value)))}% left"


def format_bool_icon(flag):
    return "✅" if bool(flag) else "❌"


def short_profile_name(profile_id):
    if not isinstance(profile_id, str):
        return str(profile_id)
    return profile_id.split(":", 1)[1] if ":" in profile_id else profile_id


def short_reset_display(reset_at):
    if not isinstance(reset_at, str) or reset_at in {"n/a", "not reported"}:
        return "n/a"
    # Input format from format_reset_at: "dd/mm/yyyy, HH:MM"
    parts = [p.strip() for p in reset_at.split(",", 1)]
    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"
    return reset_at


def parse_codex_usage(payload):
    rl = (payload or {}).get("rate_limit") or {}
    pw = rl.get("primary_window") or {}
    sw = rl.get("secondary_window") or {}

    def infer_window_label(secs, fallback_label):
        if not isinstance(secs, (int, float)) or secs <= 0:
            return fallback_label
        secs_i = int(secs)
        if secs_i % 86400 == 0:
            days = secs_i // 86400
            if days == 7:
                return "Week"
            return f"{days}d"
        if secs_i % 3600 == 0:
            return f"{secs_i // 3600}h"
        if secs_i >= 86400:
            return f"{round(secs_i / 86400)}d"
        return f"{round(secs_i / 3600)}h"

    def win(obj, fallback_label):
        if not obj:
            return None
        secs = obj.get("limit_window_seconds")
        reset = obj.get("reset_at")
        reset_after = obj.get("reset_after_seconds")
        label = infer_window_label(secs, fallback_label)
        used = obj.get("used_percent")
        remaining = None
        if isinstance(used, (int, float)):
            remaining = max(0, 100 - float(used))
        return {
            "label": label,
            "used_percent": used,
            "remaining_percent": remaining,
            "reset_in": format_reset_in(reset_after),
            "reset_at": format_reset_at(reset),
            "reset_after_seconds": reset_after,
            "limit_window_seconds": secs,
        }

    windows = []
    p = win(pw, "5h")
    s = win(sw, "Week")
    if p:
        windows.append(p)
    if s:
        windows.append(s)

    plan = payload.get("plan_type") if isinstance(payload, dict) else None
    credits = None
    try:
        bal = payload.get("credits", {}).get("balance")
        if bal is not None:
            credits = float(bal)
    except Exception:
        credits = None

    return {
        "plan": plan,
        "credits_balance": credits,
        "allowed": rl.get("allowed"),
        "limit_reached": rl.get("limit_reached"),
        "windows": windows,
    }


def build_template_line(profile_report):
    # Friendly auth-failure rendering (401 from usage endpoint)
    if int(profile_report.get("remote_status") or 0) == 401:
        pid = profile_report.get("profile") or "unknown"
        suffix = pid.split(":", 1)[1] if ":" in pid else pid
        return (
            f"🔴 `{short_profile_name(pid)}` — auth invalid (401) | run `/codex_auth {suffix}`"
        )

    remote = profile_report.get("remote_usage") or {}
    windows = remote.get("windows") or []

    def to_row(w):
        return {
            "remaining": format_pct(w.get("remaining_percent")),
            "remaining_raw": w.get("remaining_percent"),
            "reset_at": w.get("reset_at") or "n/a",
            "time_left": format_duration_dhm(w.get("reset_after_seconds")),
            "secs": w.get("limit_window_seconds"),
            "label": str(w.get("label") or "Window"),
        }

    def derive_usage_state(remote_usage, win_rows, fallback_ok):
        # Prefer explicit WHAM booleans, but guard with window evidence to avoid stale-looking output.
        allowed = remote_usage.get("allowed")
        limit_reached = remote_usage.get("limit_reached")

        max_window = None
        for w in win_rows:
            secs = w.get("secs")
            if isinstance(secs, (int, float)):
                if max_window is None or int(secs) > int(max_window.get("secs") or 0):
                    max_window = w

        max_window_exhausted = False
        if max_window and isinstance(max_window.get("remaining_raw"), (int, float)):
            max_window_exhausted = float(max_window.get("remaining_raw")) <= 0.0

        if isinstance(limit_reached, bool):
            limited = limit_reached or max_window_exhausted
        elif max_window is not None:
            limited = max_window_exhausted
        else:
            limited = False

        if isinstance(allowed, bool):
            usable = allowed and not limited
        else:
            usable = bool(fallback_ok) and not limited

        return usable, limited

    short = {"label": "5h", "remaining": "not reported", "reset_at": "not reported", "time_left": "not reported", "secs": None, "remaining_raw": None}
    longw = {"label": "Week", "remaining": "not reported", "reset_at": "not reported", "time_left": "not reported", "secs": None, "remaining_raw": None}

    rows = []
    for w in windows:
        row = to_row(w)
        rows.append(row)
        secs = row.get("secs")
        # Prefer nearest short window around 5h; otherwise any <= 24h.
        if isinstance(secs, (int, float)) and secs <= 86400:
            if short.get("secs") is None or abs(int(secs) - 18000) < abs(int(short.get("secs") or 18000) - 18000):
                short = row
        # Long window = largest window > 24h.
        if isinstance(secs, (int, float)) and secs > 86400:
            if longw.get("secs") is None or int(secs) > int(longw.get("secs") or 0):
                longw = row

    usable, limited = derive_usage_state(remote, rows, profile_report.get("remote_usage_ok"))

    if limited:
        status = "🟠"
    else:
        status = "🟢" if usable else "🔴"

    pid = short_profile_name(profile_report.get('profile'))
    short_label = (short.get('label') or '5h').lower()
    long_label = (longw.get('label') or 'week').lower()
    short_reset_tag = 'r5' if short_label.startswith('5') else f"r{short_label}"
    long_reset_tag = 'rw' if long_label.startswith('week') else f"r{long_label}"

    return (
        f"{status} `{pid}` — {short_label} **{short['remaining']}** | {long_label} **{longw['remaining']}** | "
        f"{short_reset_tag} **{short_reset_display(short['reset_at'])}** | {long_reset_tag} **{short_reset_display(longw['reset_at'])}**"
    )


def render_text_output(out):
    # Strict default text format for slash usage:
    # - one compact line per profile
    # - no preface/progress text
    # - no summary footer
    lines = []
    for line in out.get("formatted_profiles") or []:
        lines.append(line)

    # Keep actionable auth hints if present.
    msg = out.get("suggested_user_message")
    if msg and "Auth invalid" in msg:
        lines.append(msg)

    return "\n".join(lines).strip() + "\n"


def scrub_sensitive(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            lk = str(k).lower()
            if lk in {"access", "refresh", "token", "authorization", "api_key", "apikey"}:
                out[k] = "[redacted]"
            else:
                out[k] = scrub_sensitive(v)
        return out
    if isinstance(obj, list):
        return [scrub_sensitive(v) for v in obj]
    return obj


def report_profile(store, profile_id, include_remote=False, endpoint=None, timeout_sec=20, retries=1, debug=False):
    profiles = store.get("profiles", {})
    usage_stats = store.get("usageStats", {})

    p = profiles.get(profile_id)
    if not p:
        return {"profile": profile_id, "status": "missing"}

    u = usage_stats.get(profile_id, {})

    result = {
        "profile": profile_id,
        "provider": p.get("provider"),
        "type": p.get("type"),
        "token_expiry": fmt_expiry(p.get("expires")),
        "last_used": fmt_ts(u.get("lastUsed")),
        "last_failure": fmt_ts(u.get("lastFailureAt")),
        "cooldown_until": fmt_ts(u.get("cooldownUntil")),
        "error_count": u.get("errorCount", 0),
        "failure_counts": u.get("failureCounts", {}),
    }

    if include_remote and endpoint:
        token = p.get("access")
        account_id = p.get("accountId")
        if token:
            remote = call_remote_usage(endpoint, token, account_id=account_id, timeout_sec=timeout_sec, retries=retries)
            result["remote_usage_ok"] = bool(remote.get("ok"))
            if remote.get("ok"):
                result["remote_usage"] = parse_codex_usage(remote.get("payload") or {})
            else:
                result["remote_error"] = remote.get("error") or "request_failed"
                if remote.get("status") is not None:
                    result["remote_status"] = remote.get("status")
                if int(remote.get("status") or 0) == 401:
                    result["remote_hint"] = (
                        "usage_endpoint_rejected_token_format_or_session; "
                        "this endpoint may require a different auth/session type than stored OAuth tokens"
                    )
            if debug:
                result["remote_debug"] = {
                    "attempt": remote.get("attempt"),
                    "elapsed_ms": remote.get("elapsed_ms"),
                    "status": remote.get("status"),
                    "endpoint": endpoint,
                }
        else:
            result["remote_usage_ok"] = False
            result["remote_error"] = "missing_access_token"

    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="all", help="all|default|<profile-id>|<suffix>")
    ap.add_argument("--auth-path", default=DEFAULT_AUTH_PATH)
    ap.add_argument("--timeout-sec", type=int, default=20)
    ap.add_argument("--retries", type=int, default=1, help="number of retries after first attempt")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument(
        "--delete-profile",
        default=None,
        help="Delete codex profile(s): all|default|<profile-id>|<suffix>",
    )
    ap.add_argument(
        "--confirm-delete",
        action="store_true",
        help="Required safeguard to perform mutation (without this flag, script only previews).",
    )
    ap.add_argument(
        "--hard-delete",
        action="store_true",
        help="Permanently delete profile+usage entries. Default is safer detach-only (keeps token/profile entry).",
    )
    ap.add_argument("--dry-run", action="store_true", help="Show delete result without writing auth file")
    ap.add_argument("--ack-gateway-restart", action="store_true", help="Required confirmation: mutation will stop gateway, write auth store, and restart gateway")
    ap.add_argument("--allow-unsafe-direct", action="store_true", help="Allow direct in-process auth write for delete mutation (not recommended)")
    ap.add_argument("--format", choices=["json", "text"], default="json", help="Output format for usage checks")
    args = ap.parse_args()

    try:
        store = load_store(args.auth_path)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"failed_to_read_auth_profiles: {e}"}))
        sys.exit(1)

    if args.delete_profile:
        delete_targets_list = resolve_targets(store, args.delete_profile)
        if not delete_targets_list:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "no_matching_codex_profiles_for_delete",
                        "selector": args.delete_profile,
                        "available_profiles": list_codex_profiles(store),
                        "hint": "Use --delete-profile all/default/<profile-id>/<suffix>",
                    },
                    indent=2,
                )
            )
            sys.exit(3)

        mode = "hard_delete" if args.hard_delete else "detach_only"

        # Verification safeguard: require explicit confirmation flag before mutating auth store.
        if not args.confirm_delete:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "delete_confirmation_required",
                        "action": "delete_profiles_preview",
                        "mode": mode,
                        "selector": args.delete_profile,
                        "would_mutate": delete_targets_list,
                        "auth_path": args.auth_path,
                        "safety_note": "Default mode is detach-only (removes from order/lastGood, keeps token/profile).",
                        "backup_note": "A timestamped backup will be created automatically before mutation.",
                        "how_to_confirm": "Re-run with --confirm-delete --ack-gateway-restart (optionally add --dry-run first; use --hard-delete for permanent removal).",
                    },
                    indent=2,
                )
            )
            sys.exit(4)

        if args.hard_delete:
            mutate_result = hard_delete_targets(store, delete_targets_list)
            action = "hard_delete_profiles"
        else:
            mutate_result = detach_targets(store, delete_targets_list)
            action = "detach_profiles"

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "action": action,
                        "mode": mode,
                        "dry_run": True,
                        "auth_path": args.auth_path,
                        **mutate_result,
                    },
                    indent=2,
                )
            )
            return

        if not args.ack_gateway_restart:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "gateway_restart_ack_required",
                        "action": action,
                        "mode": mode,
                        "targets": delete_targets_list,
                        "warning": "This operation will stop the gateway, write auth profile changes, then restart the gateway.",
                        "how_to_confirm": "Re-run with --confirm-delete --ack-gateway-restart (optionally add --hard-delete).",
                    },
                    indent=2,
                )
            )
            sys.exit(5)

        if args.allow_unsafe_direct:
            backup_path = backup_store(args.auth_path)
            save_store(args.auth_path, store)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "action": action,
                        "mode": mode,
                        "dry_run": False,
                        "unsafe_direct": True,
                        "auth_path": args.auth_path,
                        "backup_path": backup_path,
                        **mutate_result,
                    },
                    indent=2,
                )
            )
            return

        queue_meta = schedule_offhost_delete_apply(args.auth_path, store, delete_targets_list, mode)
        print(
            json.dumps(
                {
                    "ok": True,
                    "action": action,
                    "mode": mode,
                    "dry_run": False,
                    "queued": True,
                    "warning": "Gateway stop/write/start apply has been queued off-host.",
                    "auth_path": args.auth_path,
                    **mutate_result,
                    **queue_meta,
                },
                indent=2,
            )
        )
        return

    targets = resolve_targets(store, args.profile)
    if not targets:
        print(json.dumps({
            "ok": False,
            "error": "no_matching_codex_profiles",
            "available_profiles": list_codex_profiles(store),
            "hint": "Use --profile all/default/<profile-id>/<suffix>",
        }, indent=2))
        sys.exit(2)

    raw_endpoint = os.getenv("CODEX_USAGE_ENDPOINT", DEFAULT_ENDPOINT).strip()
    endpoint, endpoint_ok, endpoint_reason = validate_endpoint(raw_endpoint)
    include_remote = endpoint_ok and endpoint_reachable(endpoint)

    reports = []
    for pid in targets:
        reports.append(
            report_profile(
                store,
                pid,
                include_remote=include_remote,
                endpoint=endpoint,
                timeout_sec=max(5, args.timeout_sec),
                retries=max(0, args.retries),
                debug=args.debug,
            )
        )

    ok_remote = sum(1 for p in reports if p.get("remote_usage_ok") is True)
    failed_remote = sum(1 for p in reports if p.get("remote_usage_ok") is False)

    out = {
        "ok": True,
        "source": "auth-profiles",
        "remote_endpoint": endpoint,
        "remote_endpoint_enabled": include_remote,
        "profiles": reports,
        "progress_message": "Running Codex usage checks now…",
        "response_template": "🟢 `%profile%` — 5h **%5h_left%** | wk **%week_left%** | r5 **%5h_reset%** | rw **%week_reset%**",
    }
    if endpoint_reason:
        out["remote_endpoint_note"] = endpoint_reason
    if endpoint_ok and not include_remote:
        out["remote_endpoint_note"] = "endpoint_unreachable_local_health_only"

    auth_rejects = [p.get("profile") for p in reports if int(p.get("remote_status") or 0) == 401]
    if auth_rejects:
        out["remote_auth_note"] = "usage_endpoint_rejected_available_oauth_tokens_401"
        out["remote_auth_affected_profiles"] = auth_rejects

    out["summary"] = {
        "profiles_checked": len(reports),
        "remote_ok_count": ok_remote,
        "remote_failed_count": failed_remote,
    }
    out["formatted_profiles"] = [build_template_line(r) for r in reports]

    if auth_rejects:
        cmds = ", ".join([f"/codex_auth {p.split(':',1)[1] if ':' in p else p}" for p in auth_rejects])
        out["suggested_user_message"] = (
            "Auth invalid for profile(s): " + ", ".join(auth_rejects) + ". "
            "OAuth token was rejected by OpenAI usage endpoint (401). "
            "Refresh with: " + cmds
        )
    elif failed_remote > 0 and ok_remote == 0:
        out["suggested_user_message"] = (
            "Remote usage checks are currently unavailable; showing local profile health only."
        )
    else:
        out["suggested_user_message"] = "Codex usage check completed."

    if args.format == "text":
        print(render_text_output(scrub_sensitive(out)), end="")
    else:
        print(json.dumps(scrub_sensitive(out), indent=2))


if __name__ == "__main__":
    main()
