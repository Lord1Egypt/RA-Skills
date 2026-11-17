#!/bin/bash
# Mesh heartbeat watchdog: peerd can wedge internally (process alive, status.json
# heartbeat frozen — seen 2026-07-13..15 on BOTH nodes). pm2/nohup only catch
# crashes, so restart on a stale heartbeat instead. Cron: every 5 min.
S="$HOME/.decent-peer/status.json"
AGE=$(python3 - <<'PY'
import json, datetime, os, sys
p = os.path.expanduser("~/.decent-peer/status.json")
try:
    ts = json.load(open(p)).get("ts")
    t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    print(int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds()))
except Exception:
    print(99999)
PY
)
[ "$AGE" -lt 600 ] && exit 0
echo "$(date) heartbeat stale ${AGE}s — restarting peerd"
if command -v pm2 >/dev/null 2>&1 && pm2 describe peerd >/dev/null 2>&1; then
  pm2 restart peerd >/dev/null 2>&1
else
  pkill -f peerd.mjs 2>/dev/null; sleep 3
  cd "$HOME/.claude/skills/agent-mesh" && nohup node peerd.mjs >> "$HOME/.decent-peer/peerd.log" 2>&1 &
fi
