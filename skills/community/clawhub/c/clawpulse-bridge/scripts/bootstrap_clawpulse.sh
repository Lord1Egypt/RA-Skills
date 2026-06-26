#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLY=0
QR=1
BIND_HOST="${BIND_HOST:-0.0.0.0}"
ROTATE=0

for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    --no-qr) QR=0 ;;
    --rotate-token) ROTATE=1 ;;
    *) ;;
  esac
done

if [[ "$APPLY" != "1" ]]; then
  echo "ClawPulse bootstrap (dry-run)"
  echo "Will run: bridge setup -> monitor setup"
  echo "Default bind host: $BIND_HOST"
  echo "Run with --apply to execute."
  exit 0
fi

bridge_args=(--apply)
monitor_args=(--apply)
if [[ "$QR" != "1" ]]; then
  bridge_args+=(--no-qr)
  monitor_args+=(--no-qr)
fi

if [[ "$ROTATE" == "1" ]]; then
  echo "[1/2] Rotating bridge token + applying bridge..."
  ROTATE_TOKEN=1 BIND_HOST="$BIND_HOST" bash "$SCRIPT_DIR/setup_clawpulse_bridge.sh" "${bridge_args[@]}"
  echo "[2/2] Rotating monitor token + applying monitor..."
  ROTATE_MONITOR_TOKEN=1 bash "$SCRIPT_DIR/setup_clawpulse_monitor.sh" "${monitor_args[@]}"
else
  echo "[1/2] Applying bridge..."
  BIND_HOST="$BIND_HOST" bash "$SCRIPT_DIR/setup_clawpulse_bridge.sh" "${bridge_args[@]}"
  echo "[2/2] Applying monitor..."
  bash "$SCRIPT_DIR/setup_clawpulse_monitor.sh" "${monitor_args[@]}"
fi

echo

echo "Bootstrap complete. Use monitor endpoint/token in ClawPulse app."
