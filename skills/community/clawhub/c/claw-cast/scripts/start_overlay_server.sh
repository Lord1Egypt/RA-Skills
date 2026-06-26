#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OVERLAY_ROOT="$SKILL_ROOT/assets/overlays"
PORT="${OVERLAY_PORT:-8787}"
LOG_DIR="$SKILL_ROOT/.runtime"
LOG="$LOG_DIR/http-server.log"

if [[ ! -d "$OVERLAY_ROOT" ]]; then
  echo "ERROR: overlay directory not found: $OVERLAY_ROOT"
  exit 1
fi

mkdir -p "$LOG_DIR"

if ss -ltn | grep -q ":$PORT "; then
  echo "Overlay server already listening on :$PORT"
else
  # Security scope: serve skill-local overlays only (not workspace root).
  nohup python3 -m http.server "$PORT" --directory "$SKILL_ROOT" > "$LOG" 2>&1 &
  sleep 1
  echo "Started overlay server on :$PORT (root=$SKILL_ROOT)"
fi

IP=$(hostname -I | awk '{print $1}')
echo "LAN base URL: http://$IP:$PORT"
echo "Overlay base URL: http://$IP:$PORT/assets/overlays"
