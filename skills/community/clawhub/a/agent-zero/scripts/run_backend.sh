#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
LOG_FILE="${LOG_FILE:-/tmp/agent_zero_backend.log}"
PORT="${BACKEND_PORT:-8000}"
# AGENT_ZERO_DATA_DIR must be set in your environment before running this script.
# e.g. export AGENT_ZERO_DATA_DIR=~/agent_zero_data

cd "$BACKEND_DIR"

echo "[backend] stopping existing process on port $PORT (if any)..."
lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true
pkill -f "target/release/agent_zero_backend" 2>/dev/null || true
pkill -f "cargo run --release" 2>/dev/null || true

echo "[backend] starting (cargo run --release)..."
nohup cargo run --release --bin agent_zero_backend > "$LOG_FILE" 2>&1 &
PID=$!

echo "[backend] started with PID $PID"
echo "[backend] log: $LOG_FILE"

sleep 2
if ! kill -0 "$PID" 2>/dev/null; then
  echo "[backend] failed to stay running; last log lines:" >&2
  tail -n 50 "$LOG_FILE" >&2 || true
  exit 1
fi

for i in $(seq 1 20); do
  code=0
  curl -fsS -o /dev/null "http://127.0.0.1:$PORT/api/listings" 2>/dev/null || code=$?
  if [ $code -eq 0 ]; then
    printf '\033[32m[backend] health check passed ✅ http://127.0.0.1:%s\033[0m\n' "$PORT"
    break
  fi

  if [ $code -eq 7 ]; then
    echo "[backend] curl failed to connect (code $code); retrying ($i/20)..." >&2
  else
    echo "[backend] health check attempt $i failed (curl exit code $code); retrying ($i/20)..." >&2
  fi

  sleep 1
done

if [ $code -ne 0 ]; then
  echo "[backend] process is running but health check failed; inspect $LOG_FILE" >&2
  tail -n 50 "$LOG_FILE" >&2 || true
  exit 1
fi
