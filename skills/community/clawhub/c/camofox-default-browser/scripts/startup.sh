#!/bin/bash
# Auto-start Camofox Browser Server for OpenClaw
# Dipanggil oleh plugin camofox-browser autoStart
# Falls back to manual start if plugin auto-start fails

CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox
cd /root/.openclaw/extensions/camofox-browser 2>/dev/null || cd /tmp/camofox-browser

# Check if server already running
if curl -sf http://localhost:9377/health >/dev/null 2>&1; then
  exit 0
fi

export CAMOUFOX_EXECUTABLE
nohup node server.js --port 9377 > /tmp/camofox-daemon.log 2>&1 &
disown

# Wait up to 10 seconds for server ready
for i in 1 2 3 4 5 6 7 8 9 10; do
  sleep 1
  if curl -sf http://localhost:9377/health >/dev/null 2>&1; then
    break
  fi
done
