#!/bin/zsh
set -euo pipefail

PORT="${PORT:-18990}"
UID_NUM="$(id -u)"

for label in ai.openclaw.gateway ai.openclaw.gateway-monitor ai.openclaw.gateway-watchdog; do
  echo "===== ${label} ====="
  launchctl print "gui/${UID_NUM}/${label}" 2>&1 | sed -n '1,24p'
  echo
done

if command -v curl >/dev/null 2>&1; then
  echo "===== health ====="
  curl -s "http://127.0.0.1:${PORT}/api/summary" | head -c 400
  echo
fi
