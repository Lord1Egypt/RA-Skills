#!/usr/bin/env bash
# fallback-swap.sh — Try primary model for a role; if it fails, test fallback.
# If fallback works, swap primary↔fallback in duty-table.json for this week.
#
# Usage: fallback-swap.sh <role>
# Outputs the working command to stdout (caller captures it).
# Exit 0 = got a working model; Exit 1 = both failed.
#
# Roles: architect, builder, reviewer, integrator

set -euo pipefail

ROLE="${1:?Usage: fallback-swap.sh <role>}"
SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
DUTY_TABLE="$SWARM_DIR/duty-table.json"
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"

if [[ ! -f "$DUTY_TABLE" ]]; then
  echo "[fallback-swap] No duty table found" >&2
  exit 1
fi

# Read primary and fallback for the role
read_role() {
  python3 -c "
import json, sys
with open('$DUTY_TABLE') as f: d = json.load(f)
role = d.get('dutyTable', {}).get('$ROLE', {})
kind = sys.argv[1]
if kind == 'primary':
    print(role.get('agent', ''), role.get('model', ''), role.get('nonInteractiveCmd', ''), sep='|')
elif kind == 'fallback':
    fb = role.get('fallback', {})
    if fb:
        # Build cmd from fallback
        agent = fb.get('agent', '')
        model = fb.get('model', '')
        if agent == 'claude':
            cmd = f'claude --model {model} --permission-mode bypassPermissions --print'
        elif agent == 'gemini':
            cmd = f'gemini -m {model}'  # -y -p added by caller wrapper
        elif agent == 'codex':
            cmd = f'codex --model {model} -q'
        else:
            cmd = ''
        print(agent, model, cmd, sep='|')
    else:
        print('||')
" "$1" 2>/dev/null
}

IFS='|' read -r P_AGENT P_MODEL P_CMD <<< "$(read_role primary)"
IFS='|' read -r F_AGENT F_MODEL F_CMD <<< "$(read_role fallback)"

if [[ -z "$P_AGENT" || -z "$P_MODEL" ]]; then
  echo "[fallback-swap] No primary defined for role: $ROLE" >&2
  exit 1
fi

# Test primary
echo "[fallback-swap] Testing primary: $P_AGENT/$P_MODEL for $ROLE..." >&2
if "$SWARM_DIR/try-model.sh" "$P_AGENT" "$P_MODEL" 2>/dev/null; then
  echo "[fallback-swap] ✅ Primary works: $P_AGENT/$P_MODEL" >&2
  echo "$P_CMD"
  exit 0
fi

echo "[fallback-swap] ❌ Primary failed: $P_AGENT/$P_MODEL" >&2

# No fallback defined?
if [[ -z "$F_AGENT" || -z "$F_MODEL" ]]; then
  echo "[fallback-swap] No fallback defined for $ROLE — both failed" >&2
  exit 1
fi

# Test fallback
echo "[fallback-swap] Testing fallback: $F_AGENT/$F_MODEL..." >&2
if ! "$SWARM_DIR/try-model.sh" "$F_AGENT" "$F_MODEL" 2>/dev/null; then
  echo "[fallback-swap] ❌ Fallback also failed: $F_AGENT/$F_MODEL" >&2
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  echo "🚨 [$TIMESTAMP] BOTH primary ($P_AGENT/$P_MODEL) and fallback ($F_AGENT/$F_MODEL) failed for $ROLE!" >> "$NOTIFY_FILE"
  exit 1
fi

echo "[fallback-swap] ✅ Fallback works: $F_AGENT/$F_MODEL — SWAPPING in duty table" >&2

# Swap primary ↔ fallback in duty-table.json
python3 << PYSWAP
import json
from datetime import datetime

with open('$DUTY_TABLE') as f:
    d = json.load(f)

role = d['dutyTable']['$ROLE']
old_primary = {'agent': role['agent'], 'model': role['model']}
fallback = role.get('fallback', {})

# Swap: fallback becomes primary, old primary becomes fallback
role['agent'] = fallback['agent']
role['model'] = fallback['model']

# Rebuild nonInteractiveCmd for new primary
if fallback['agent'] == 'claude':
    role['nonInteractiveCmd'] = f"claude --model {fallback['model']} --permission-mode bypassPermissions --print"
elif fallback['agent'] == 'gemini':
    role['nonInteractiveCmd'] = f"gemini -m {fallback['model']}"
elif fallback['agent'] == 'codex':
    role['nonInteractiveCmd'] = f"codex --model {fallback['model']} -q"

role['fallback'] = old_primary
role['reason'] = f"AUTO-SWAPPED {datetime.now():%Y-%m-%d %H:%M}: {old_primary['model']} failed, {fallback['model']} promoted"

# Log the swap
d.setdefault('history', []).append({
    'date': f"{datetime.now():%Y-%m-%d %H:%M}",
    'changes': f"AUTO-SWAP for $ROLE: {old_primary['agent']}/{old_primary['model']} failed → {fallback['agent']}/{fallback['model']} promoted to primary",
    'dutyAssignments': f"$ROLE={fallback['agent']}/{fallback['model']} (was {old_primary['agent']}/{old_primary['model']})"
})

with open('$DUTY_TABLE', 'w') as f:
    json.dump(d, f, indent=2)

print(f"Swapped: {old_primary['model']} → fallback, {fallback['model']} → primary")
PYSWAP

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "🔄 [$TIMESTAMP] AUTO-SWAP for $ROLE: $P_MODEL failed → $F_MODEL promoted to primary (old primary demoted to fallback)" >> "$NOTIFY_FILE"

# Output the working command (now the former fallback)
echo "$F_CMD"
exit 0
