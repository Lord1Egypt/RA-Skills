#!/usr/bin/env bash
# Run defi-yield-monitor with auto proxy detection
set -euo pipefail

DIR="${DEFI_MONITOR_DIR:-$HOME/.openclaw/workspace/projects/defi-yield-monitor}"
MODE="${1:---text}"  # --text | --yield-summary | --json

if [ ! -d "$DIR" ]; then
  echo "❌ Project not found at $DIR. Run setup.sh first."
  exit 1
fi

cd "$DIR"

# Auto-detect proxy (QuickQ or common proxies)
if [ -z "${https_proxy:-}" ]; then
  PROXY_PORT=$(lsof -nP 2>/dev/null | grep -E 'quickqser|clash|v2ray' | grep LISTEN | grep -oE '127\.0\.0\.1:[0-9]+' | head -1 || true)
  if [ -n "$PROXY_PORT" ]; then
    export https_proxy="http://$PROXY_PORT"
    export http_proxy="http://$PROXY_PORT"
  fi
fi

exec .venv/bin/python main.py --config config/config.json "$MODE"
