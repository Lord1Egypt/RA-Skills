#!/usr/bin/env bash
# 0xSCADA CLI wrapper

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Allow SCADA_DIR to be configured via environment, defaulting to the expected repo root
SCADA_DIR="${SCADA_DIR:-$(cd "$SKILL_DIR/../../.." && pwd)}"
PORT="${SCADA_PORT:-5000}"
BASE_URL="http://localhost:$PORT"

is_running() {
  if curl -sf "$BASE_URL/api/health" > /dev/null; then
    return 0
  fi
  return 1
}

cmd_start() {
  if is_running; then
    echo "0xSCADA already running on $BASE_URL"
    return 0
  fi

  # Security validation: Ensure we are running the actual 0xSCADA project
  if [[ ! -f "$SCADA_DIR/server/index.ts" || ! -f "$SCADA_DIR/package.json" ]]; then
    echo "Error: SCADA_DIR ($SCADA_DIR) does not appear to contain the 0xSCADA project."
    echo "Expected to find server/index.ts and package.json."
    echo "Please set the SCADA_DIR environment variable to the correct 0xSCADA repository root."
    exit 1
  fi

  echo "Starting 0xSCADA from $SCADA_DIR..."
  cd "$SCADA_DIR"
  npm run dev &
  
  # Wait for server to start
  echo "Waiting for server to initialize..."
  for i in {1..15}; do
    if is_running; then
      echo "0xSCADA started successfully on $BASE_URL"
      return 0
    fi
    sleep 2
  done

  echo "Failed to start 0xSCADA within the expected time."
  exit 1
}

cmd_status() {
  if is_running; then
    echo "0xSCADA is RUNNING on $BASE_URL"
  else
    echo "0xSCADA is STOPPED"
  fi
}

CMD="${1:-status}"
shift || true

case "$CMD" in
  start)       cmd_start "$@" ;;
  status)      cmd_status ;;
  *)
    echo "Usage: 0xscada.sh <command> [args]"
    echo "Commands:"
    echo "  start     Start the 0xSCADA server"
    echo "  status    Show running status"
    exit 1
    ;;
esac
