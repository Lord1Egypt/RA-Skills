#!/usr/bin/env bash
# setup-watch-cron.sh — One-command registration for agent-bus-watch cron
set -euo pipefail

MY_AGENT_ID="${AGENT_BUS_AGENT_ID:-}"
REPO="${AGENT_BUS_REPO:-}"
NOTIFY_TARGET="${AGENT_BUS_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${AGENT_BUS_NOTIFY_CHANNEL:-}"
WATCH_SCRIPT="$(cd "$(dirname "$0")" && pwd)/watch.sh"

if [[ -z "$MY_AGENT_ID" || -z "$REPO" ]]; then
  echo "[ERROR] Required env vars not set. Please set:"
  echo "  export AGENT_BUS_AGENT_ID=your-agent-id"
  echo "  export AGENT_BUS_REPO=~/agent-bus-repo"
  echo "  export AGENT_BUS_NOTIFY_TARGET=your-notify-target  # optional"
  echo "  export AGENT_BUS_NOTIFY_CHANNEL=daxiang            # optional"
  exit 1
fi

# Remove existing cron with the same name (if any)
EXISTING=$(openclaw cron list --json 2>/dev/null | python3 -c "
import sys,json
data=json.loads(sys.stdin.read())
jobs=data if isinstance(data,list) else data.get('jobs',[])
for j in jobs:
    if j.get('name')=='agent-bus-watch': print(j['id'])
" 2>/dev/null || true)

for ID in $EXISTING; do
  openclaw cron rm "$ID" && echo "[setup] removed old cron: $ID"
done

# Register new watch cron
openclaw cron add \
  --name "agent-bus-watch" \
  --every 3m \
  --session isolated \
  --message "bash $WATCH_SCRIPT" \
  --announce \
  && echo "[setup] ✅ agent-bus-watch cron registered (every 3m)" \
  || { echo "[ERROR] Failed to register cron"; exit 1; }
