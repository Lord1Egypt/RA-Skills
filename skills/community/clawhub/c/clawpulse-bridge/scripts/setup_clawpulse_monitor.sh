#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DEFAULT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
WORKSPACE="${WORKSPACE:-$WORKSPACE_DEFAULT}"
ENV_FILE="$WORKSPACE/.clawpulse.env"
MONITOR_SRC="$SCRIPT_DIR/clawpulse-monitor.py"
MONITOR_PY="$WORKSPACE/clawpulse-monitor.py"
LOG_FILE="$WORKSPACE/clawpulse-monitor.log"

MONITOR_BIND_HOST="${MONITOR_BIND_HOST:-0.0.0.0}"
MONITOR_PORT="${MONITOR_PORT:-8788}"
BRIDGE_URL="${BRIDGE_URL:-http://127.0.0.1:8787/health}"
APPLY="${APPLY:-0}"
ROTATE_MONITOR_TOKEN="${ROTATE_MONITOR_TOKEN:-0}"
PRINT_QR="${PRINT_QR:-1}"

for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    --rotate-token) ROTATE_MONITOR_TOKEN=1 ;;
    --no-qr) PRINT_QR=0 ;;
    *) ;;
  esac
done

umask 077
mkdir -p "$WORKSPACE"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE, run bridge setup first." >&2
  exit 1
fi

source "$ENV_FILE"

if [[ "$ROTATE_MONITOR_TOKEN" == "1" || -z "${MONITOR_TOKEN:-}" ]]; then
  MONITOR_TOKEN=$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
)
fi

if [[ -z "${STATUS_TOKEN:-}" ]]; then
  echo "STATUS_TOKEN missing in $ENV_FILE" >&2
  exit 1
fi

cat > "$ENV_FILE" <<EOF
STATUS_TOKEN=${STATUS_TOKEN}
MONITOR_TOKEN=${MONITOR_TOKEN}
EOF
chmod 600 "$ENV_FILE"

if [[ ! -f "$MONITOR_SRC" ]]; then
  echo "Missing monitor source: $MONITOR_SRC" >&2
  exit 1
fi
cp "$MONITOR_SRC" "$MONITOR_PY"
chmod 700 "$MONITOR_PY"

TS_DNS=""
TS_IP=""
if command -v tailscale >/dev/null 2>&1; then
  TS_IP="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
  TS_DNS="$(tailscale status --json 2>/dev/null | python3 -c 'import json,sys
try:
 j=json.load(sys.stdin); print(((j.get("Self") or {}).get("DNSName") or "").rstrip("."))
except Exception:
 print("")')"
fi
if [[ -n "$TS_DNS" ]]; then
  ENDPOINT="http://${TS_DNS}:${MONITOR_PORT}/health"
elif [[ -n "$TS_IP" ]]; then
  ENDPOINT="http://${TS_IP}:${MONITOR_PORT}/health"
else
  ENDPOINT="http://127.0.0.1:${MONITOR_PORT}/health"
fi
SETUP_LINK=$(python3 - <<PY
from urllib.parse import quote
u = quote("$ENDPOINT", safe="")
t = quote("$MONITOR_TOKEN", safe="")
print(f"clawpulse://setup?url={u}&token={t}")
PY
)

print_qr() {
  [[ "$PRINT_QR" != "1" ]] && return
  if command -v qrencode >/dev/null 2>&1; then
    qrencode -t ansiutf8 "$SETUP_LINK" || true
    qrencode -o "$WORKSPACE/clawpulse-monitor-setup.png" "$SETUP_LINK" || true
    echo "QR image: $WORKSPACE/clawpulse-monitor-setup.png"
    command -v open >/dev/null 2>&1 && open "$WORKSPACE/clawpulse-monitor-setup.png" >/dev/null 2>&1 || true
  else
    echo "Tip: brew install qrencode (for QR output)"
  fi
}

if [[ "$APPLY" != "1" ]]; then
  echo "ClawPulse monitor plan (dry-run)"
  echo "Bridge URL: $BRIDGE_URL"
  echo "Monitor endpoint: $ENDPOINT"
  echo "Monitor token: $MONITOR_TOKEN"
  print_qr
  echo "Run with --apply to start/restart monitor."
  exit 0
fi

pkill -f clawpulse-monitor.py >/dev/null 2>&1 || true
set -a
source "$ENV_FILE"
export WORKSPACE MONITOR_BIND_HOST MONITOR_PORT BRIDGE_URL BRIDGE_TOKEN="$STATUS_TOKEN"
set +a
nohup python3 "$MONITOR_PY" >"$LOG_FILE" 2>&1 &
sleep 1

echo "ClawPulse monitor running"
echo "Bind: $MONITOR_BIND_HOST:$MONITOR_PORT"
echo "Bridge URL: $BRIDGE_URL"
echo "Monitor endpoint: $ENDPOINT"
echo "Monitor token: $MONITOR_TOKEN"
echo "Log: $LOG_FILE"
print_qr
