#!/bin/bash
# cleanup-agents.sh — Close all agent tmux sessions after swarm completion
# Usage: cleanup-agents.sh
#
# Called automatically by on-complete.sh when all tasks are done.
# Also safe to call manually.
#
# Sessions that are ALWAYS preserved (fixed infrastructure):
#   cc-plan       — planning agent (reused across swarms)
#   cc-review     — review agent
#   codex-review  — review agent
#
# Sessions that are closed (dynamic coding agents):
#   codex-1, codex-2, codex-3, codex-4
#   cc-frontend-1, cc-frontend-2

set -euo pipefail

POOL_FILE="$HOME/.openclaw/workspace/swarm/agent-pool.json"
POOL_LOCK="${POOL_FILE}.lock"
NOTIFY_TARGET=$(cat "$HOME/.openclaw/workspace/swarm/notify-target" 2>/dev/null || echo "")
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"

# Sessions to NEVER kill (fixed infrastructure)
PRESERVE=("cc-plan" "cc-review" "codex-review")

echo "🧹 Starting cleanup of agent sessions..."

CLOSED=()
PRESERVED=()
SKIPPED=()

# Dynamic coding agents to clean up
DYNAMIC_SESSIONS=(
  "codex-1" "codex-2" "codex-3" "codex-4"
  "cc-frontend-1" "cc-frontend-2"
)

for SESSION in "${DYNAMIC_SESSIONS[@]}"; do
  # Check if in preserve list
  SKIP=false
  for P in "${PRESERVE[@]}"; do
    [[ "$SESSION" == "$P" ]] && SKIP=true && break
  done

  if $SKIP; then
    PRESERVED+=("$SESSION")
    continue
  fi

  if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux kill-session -t "$SESSION"
    CLOSED+=("$SESSION")
    echo "🗑️  Closed: $SESSION"
  else
    SKIPPED+=("$SESSION")
  fi
done

# Update agent-pool.json — remove closed sessions
if [[ -f "$POOL_FILE" ]]; then
  (
    flock -x 9
    POOL_FILE="$POOL_FILE" \
    NOW="$NOW" \
    python3 - <<'PYEOF'
import json
import os

pool_file = os.environ['POOL_FILE']
now = os.environ['NOW']

with open(pool_file, 'r') as f:
    pool = json.load(f)

dynamic = ['codex-1','codex-2','codex-3','codex-4','cc-frontend-1','cc-frontend-2']
pool['agents'] = [a for a in pool.get('agents', []) if a.get('id') not in dynamic]
pool['updated_at'] = now

tmp = pool_file + '.tmp'
with open(tmp, 'w') as f:
    json.dump(pool, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, pool_file)

print('agent-pool.json updated.')
PYEOF
  ) 9>"$POOL_LOCK" 2>/dev/null || true
fi

# Summary
CLOSED_STR="${CLOSED[*]:-none}"
echo ""
echo "✅ Cleanup complete."
echo "   Closed:    $CLOSED_STR"
echo "   Preserved: ${PRESERVE[*]}"

# Notify
if [[ -n "$NOTIFY_TARGET" && ${#CLOSED[@]} -gt 0 ]]; then
  openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
    -m "🧹 Swarm 完成，已自动关闭 ${#CLOSED[@]} 个 agent session：$CLOSED_STR" --silent 2>/dev/null &
fi

exit 0
