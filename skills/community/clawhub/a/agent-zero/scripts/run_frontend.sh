#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
LOG_FILE="${LOG_FILE:-/tmp/agent_zero_frontend.log}"
PORT="${FRONTEND_PORT:-5173}"

cd "$ROOT_DIR"

echo "[frontend] stopping existing frontend process on port $PORT (if any)..."
lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true
pkill -f "npm --prefix frontend run dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

echo "[frontend] building latest frontend bundle..."
npm --prefix "$FRONTEND_DIR" run build

echo "[frontend] starting dev server..."
nohup npm --prefix "$FRONTEND_DIR" run dev -- --host 127.0.0.1 --port "$PORT" --strictPort > "$LOG_FILE" 2>&1 &
PID=$!

echo "[frontend] started with PID $PID"
echo "[frontend] log: $LOG_FILE"

if ! kill -0 "$PID" 2>/dev/null; then
  echo "[frontend] failed to stay running; last log lines:" >&2
  tail -n 50 "$LOG_FILE" >&2 || true
  exit 1
fi

for i in $(seq 1 20); do
  code=0
  curl -fsS -o /dev/null "http://127.0.0.1:$PORT" 2>/dev/null || code=$?
  if [ $code -eq 0 ]; then
    printf '\033[32m[frontend] health check passed ✅ http://127.0.0.1:%s\033[0m\n' "$PORT"
    exit 0
  fi

  # If curl failed to connect (code 7) or other transient error, log and retry
  if [ $code -eq 7 ]; then
    echo "[frontend] curl failed to connect (code $code); retrying ($i/20)..." >&2
  else
    echo "[frontend] health check attempt $i failed (curl exit code $code); retrying ($i/20)..." >&2
  fi

  sleep 1
done

echo "[frontend] process is running but health check failed; inspect $LOG_FILE" >&2
tail -n 50 "$LOG_FILE" >&2 || true
exit 1
