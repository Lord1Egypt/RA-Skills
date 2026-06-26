#!/bin/zsh
set -euo pipefail

MONITOR_LABEL="ai.openclaw.gateway-monitor"
WATCHDOG_LABEL="ai.openclaw.gateway-watchdog"

print_agent() {
  local label="$1"
  local target="gui/$(id -u)/$label"
  echo "\n[$label]"
  if launchctl print "$target" >/tmp/.gm_status.$$ 2>/dev/null; then
    grep -E "state =|pid =|last exit code =|runs =" /tmp/.gm_status.$$ || true
  else
    echo "not loaded"
  fi
}

print_agent "$MONITOR_LABEL"
print_agent "$WATCHDOG_LABEL"

rm -f /tmp/.gm_status.$$

echo "\n[health]"
if command -v curl >/dev/null 2>&1; then
  curl -sS --max-time 2 http://127.0.0.1:18990/api/summary >/dev/null && echo "monitor api ok" || echo "monitor api not reachable"
else
  echo "curl not found"
fi
