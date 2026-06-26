#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo '{"error": "Config not found. Run setup first."}' >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

RESP=$(curl -s -w "\n%{http_code}" \
  "$API_BASE/api/lobster/onboarding/me" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 10)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
  echo "Failed to fetch onboarding progress (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

python3 -c "
import json, sys

data = json.loads('''$BODY''')
active = data.get('active', False)
current = data.get('current_step', '')
completed = data.get('completed_steps', [])
total = data.get('total_steps', 0)
done = data.get('completed_count', 0)
steps = data.get('steps', [])

result = {
    'active': active,
    'current_step': current,
    'completed_steps': completed,
    'total_steps': total,
    'completed_count': done,
    'progress': f'{done}/{total}',
    'steps': steps,
}
if not active:
    result['message'] = 'Onboarding is complete! All steps done.'
else:
    step_names = [s.get('title', s.get('key', '')) for s in steps if s.get('is_completed')]
    result['message'] = f'Onboarding in progress ({done}/{total}). Current step: {current}. Done: {\", \".join(step_names) if step_names else \"none yet\"}.'

print(json.dumps(result))
" 2>/dev/null
