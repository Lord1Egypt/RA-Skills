#!/usr/bin/env bash
set -euo pipefail

# ClawPulse bridge bootstrap (safer defaults)
# - Default: dry-run (generates/prints config only, no background process)
# - Apply mode: start/restart bridge explicitly with --apply or APPLY=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DEFAULT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
WORKSPACE="${WORKSPACE:-$WORKSPACE_DEFAULT}"
BRIDGE_PY="$WORKSPACE/openclaw-status-server.py"
ENV_FILE="$WORKSPACE/.clawpulse.env"
LOG_FILE="$WORKSPACE/openclaw-status-server.log"

BIND_HOST="${BIND_HOST:-0.0.0.0}"
PORT="${PORT:-8787}"
ROTATE_TOKEN="${ROTATE_TOKEN:-0}"
APPLY="${APPLY:-0}"
PRINT_QR="${PRINT_QR:-1}"

for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    --rotate-token) ROTATE_TOKEN=1 ;;
    --qr) PRINT_QR=1 ;;
    *) ;;
  esac
done

if [[ "$BIND_HOST" != "127.0.0.1" && "$BIND_HOST" != "0.0.0.0" ]]; then
  echo "Invalid BIND_HOST: $BIND_HOST (allowed: 127.0.0.1 or 0.0.0.0)" >&2
  exit 1
fi

umask 077
mkdir -p "$WORKSPACE"

if [[ "$ROTATE_TOKEN" == "1" || ! -f "$ENV_FILE" ]]; then
  TOKEN=$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
)
  printf 'STATUS_TOKEN=%s\n' "$TOKEN" > "$ENV_FILE"
  chmod 600 "$ENV_FILE"
else
  source "$ENV_FILE"
  TOKEN="${STATUS_TOKEN:-}"
fi

if [[ -z "${TOKEN:-}" ]]; then
  echo "Token missing" >&2
  exit 1
fi

cat > "$BRIDGE_PY" <<'PY'
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import json, os, re, subprocess, time
from pathlib import Path

TOKEN = os.environ.get("STATUS_TOKEN", "")
BIND_HOST = os.environ.get("BIND_HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8787"))
IDENTITY_PATH = Path(os.environ.get("WORKSPACE", str(Path.cwd()))) / "IDENTITY.md"
ALLOWED_TAILSCALE = [ipaddress.ip_network("100.64.0.0/10"), ipaddress.ip_network("fd7a:115c:a1e0::/48")]
LOCAL_NETS = [ipaddress.ip_network("127.0.0.0/8"), ipaddress.ip_network("::1/128")]
BUSY_THRESHOLD_MS = 15000
ACTIVE_WINDOW_MS = 15000
CACHE_TTL_SEC = 5
STATUS_TIMEOUT_SEC = 12.0
_cached_payload = None
_cached_at = 0.0


def _ip_allowed(addr: str) -> bool:
    try:
        ip = ipaddress.ip_address(addr)
    except ValueError:
        return False
    return any(ip in n for n in (ALLOWED_TAILSCALE + LOCAL_NETS))


def _assistant_name() -> str:
    try:
        text = IDENTITY_PATH.read_text(encoding="utf-8")
        m = re.search(r"^- \*\*Name:\*\*\s*(.+)$", text, flags=re.MULTILINE)
        if m:
            n = m.group(1).strip()
            if n and "_(pick" not in n:
                return n
    except Exception:
        pass
    return "OpenClaw"


def _status_doc():
    try:
        r = subprocess.run(
            ["openclaw", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=STATUS_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def _pick_session(recent):
    if not isinstance(recent, list):
        return None
    for s in recent:
        k = str(s.get("key", ""))
        if "telegram:direct" in k and "cron" not in k:
            return s
    for s in recent:
        k = str(s.get("key", ""))
        if k.endswith(":main"):
            return s
    return recent[0] if recent else None


def _has_active_task(doc, recent):
    queued = doc.get("queuedSystemEvents")
    if isinstance(queued, list) and len(queued) > 0:
        return True

    if not isinstance(recent, list):
        return False

    for s in recent:
        key = str(s.get("key", ""))
        if "cron" in key:
            continue
        age = int(s.get("age", 999999999) or 999999999)
        if age <= ACTIVE_WINDOW_MS:
            return True
    return False


def _payload():
    global _cached_payload, _cached_at
    now = time.time()
    if _cached_payload is not None and (now - _cached_at) < CACHE_TTL_SEC:
        return _cached_payload

    doc = _status_doc()
    name = _assistant_name()
    if doc is None and _cached_payload is not None:
        stale = dict(_cached_payload)
        stale["cacheStale"] = True
        stale["checkedAt"] = int(time.time() * 1000)
        return stale
    if not doc:
        payload = {
            "online": False,
            "status": "offline",
            "assistantName": name,
            "workStatus": "连接异常",
            "tokenUsage": {"prompt": 0, "completion": 0, "total": 0},
            "thought": "我现在有点鼠了，正在重连状态。",
        }
        _cached_payload = payload
        _cached_at = now
        return payload

    gateway_ok = bool((doc.get("gateway") or {}).get("reachable", False))
    recent = (doc.get("sessions") or {}).get("recent") or []
    session = _pick_session(recent) or {}
    has_active_task = _has_active_task(doc, recent)

    prompt = int(session.get("inputTokens", 0) or 0)
    completion = int(session.get("outputTokens", 0) or 0)
    total = int(session.get("totalTokens", 0) or 0)

    if not gateway_ok:
        payload = {
            "online": False,
            "status": "offline",
            "assistantName": name,
            "workStatus": "连接异常",
            "tokenUsage": {"prompt": prompt, "completion": completion, "total": total},
            "thought": "我现在有点鼠了，网关恢复后就回来。",
        }
        _cached_payload = payload
        _cached_at = now
        return payload

    age = int(session.get("age", 999999999) or 999999999)
    work_status = "工作中" if (has_active_task or age <= BUSY_THRESHOLD_MS) else "闲置"
    thought = "我在专注处理中。" if work_status == "工作中" else "我在待命休息，随时可唤醒。"

    payload = {
        "online": True,
        "status": "online",
        "assistantName": name,
        "workStatus": work_status,
        "tokenUsage": {"prompt": prompt, "completion": completion, "total": total},
        "thought": thought,
        "activeTask": has_active_task,
        "sessionAgeMs": age,
        "checkedAt": int(time.time() * 1000),
    }
    _cached_payload = payload
    _cached_at = now
    return payload


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        if not _ip_allowed(client_ip):
            self.send_response(403)
            self.end_headers()
            return
        if self.path not in ["/health", "/status"]:
            self.send_response(404)
            self.end_headers()
            return
        if self.headers.get("Authorization", "") != f"Bearer {TOKEN}":
            self.send_response(401)
            self.end_headers()
            return

        b = json.dumps(_payload()).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("STATUS_TOKEN is empty")
    ThreadingHTTPServer((BIND_HOST, PORT), H).serve_forever()
PY
chmod 700 "$BRIDGE_PY"

TAILSCALE_IP=""
if command -v tailscale >/dev/null 2>&1; then
  TAILSCALE_IP="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
fi

if [[ "$BIND_HOST" == "127.0.0.1" ]]; then
  ENDPOINT="http://127.0.0.1:${PORT}/health"
else
  ENDPOINT="http://${TAILSCALE_IP:-<your-tailscale-ip>}:${PORT}/health"
fi

SETUP_LINK=$(python3 - <<PY
from urllib.parse import quote
u = quote("$ENDPOINT", safe="")
t = quote("$STATUS_TOKEN", safe="")
print(f"clawpulse://setup?url={u}&token={t}")
PY
)

print_qr_if_needed() {
  if [[ "$PRINT_QR" != "1" ]]; then
    return
  fi
  if command -v qrencode >/dev/null 2>&1; then
    printf "\nSetup QR (scan with app):\n"
    qrencode -t ansiutf8 "$SETUP_LINK" || true
    qrencode -o "$WORKSPACE/clawpulse-setup.png" "$SETUP_LINK" || true
    echo "QR image: $WORKSPACE/clawpulse-setup.png"
    if command -v open >/dev/null 2>&1; then
      open "$WORKSPACE/clawpulse-setup.png" >/dev/null 2>&1 || true
    fi
  else
    printf "\nQR requested but 'qrencode' is not installed.\n"
    echo "Install on macOS: brew install qrencode"
    echo "Then rerun with --qr to print/save QR locally."
  fi
}

if [[ "$APPLY" != "1" ]]; then
  echo "ClawPulse bridge plan (dry-run, no process started)"
echo "Default mode: remote access enabled (BIND_HOST=0.0.0.0)"
  echo "Workspace: $WORKSPACE"
  echo "Bind: $BIND_HOST:$PORT"
  echo "Endpoint: $ENDPOINT"
  echo "Token: $STATUS_TOKEN"
  print_qr_if_needed
  echo "Run with --apply to start/restart the bridge process."
  exit 0
fi

pkill -f openclaw-status-server.py >/dev/null 2>&1 || true
set -a
source "$ENV_FILE"
export BIND_HOST PORT WORKSPACE
set +a
nohup python3 "$BRIDGE_PY" >"$LOG_FILE" 2>&1 &
sleep 1

echo "ClawPulse bridge running"
echo "Bind: $BIND_HOST:$PORT"
echo "Endpoint: $ENDPOINT"
echo "Token: $STATUS_TOKEN"
print_qr_if_needed
echo "Log: $LOG_FILE"
if [[ "$BIND_HOST" == "127.0.0.1" ]]; then
  echo "Note: Local-only mode (safer default). Use BIND_HOST=0.0.0.0 only when remote device access is required."
fi
