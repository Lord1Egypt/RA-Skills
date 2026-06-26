#!/bin/bash
# openclaw-face — start / stop the Dynamic Island widget
# Usage: ./start.sh          (start)
#        ./start.sh stop     (stop)

DIR="$(cd "$(dirname "$0")" && pwd)"
PID_SERVER="/tmp/openclaw-face-server.pid"
PID_WIDGET="/tmp/openclaw-face-widget.pid"

stop() {
  for pf in "$PID_SERVER" "$PID_WIDGET"; do
    if [ -f "$pf" ]; then
      kill "$(cat "$pf")" 2>/dev/null
      rm -f "$pf"
    fi
  done
  # Fallback: kill by port / process name / all widget processes
  lsof -ti:7788 -ti:7789 2>/dev/null | xargs kill -9 2>/dev/null
  pkill -f "swift.*widget" 2>/dev/null
  pkill -f "widget-compiled" 2>/dev/null
  echo "[openclaw-face] stopped"
}

start() {
  stop
  sleep 1

  # Start server
  python3 "$DIR/server.py" &
  echo $! > "$PID_SERVER"

  # Wait for HTTP to be ready
  for i in $(seq 1 20); do
    curl -s -o /dev/null http://localhost:7788 && break
    sleep 0.3
  done

  # Start widget
  swift "$DIR/widget.swift" &
  echo $! > "$PID_WIDGET"

  echo "[openclaw-face] started"
  echo "  HTTP  → http://localhost:7788"
  echo "  Widget PID → $(cat $PID_WIDGET)"
}

case "${1:-start}" in
  stop)  stop ;;
  start) start ;;
  restart) stop; sleep 1; start ;;
  *)     echo "Usage: $0 {start|stop|restart}"; exit 1 ;;
esac
