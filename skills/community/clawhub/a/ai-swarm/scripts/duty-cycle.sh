#!/usr/bin/env bash
# duty-cycle.sh — run every 6 hours
# 1) Re-assess model availability
# 2) Check usage/quota pressure (current + week windows)
# 3) If any duty provider >=95% used, rotate that role to another brand
#    (priority: codex > claude > gemini)

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SWARM_DIR/swarm.conf" ]] && source "$SWARM_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"
LOG_DIR="$SWARM_DIR/logs"
mkdir -p "$LOG_DIR"

DUTY_TABLE="$SWARM_DIR/duty-table.json"
ROUTER_DUTY="${ROUTER_DUTY:-}"

# 1) Re-assess availability (best effort)
"$SWARM_DIR/assess-models.sh" >> "$LOG_DIR/assessment.log" 2>&1 || true

# Use freshest duty table source available
if [[ -f "$ROUTER_DUTY" && "$ROUTER_DUTY" -nt "$DUTY_TABLE" ]]; then
  cp "$ROUTER_DUTY" "$DUTY_TABLE" 2>/dev/null || true
fi

USAGE_JSON="$(mktemp)"
openclaw status --usage --json > "$USAGE_JSON" 2>/dev/null || echo '{}' > "$USAGE_JSON"

python3 - <<'PY' "$DUTY_TABLE" "$USAGE_JSON" "$ROUTER_DUTY"
import json, sys, datetime
from copy import deepcopy

duty_path, usage_path, router_path = sys.argv[1], sys.argv[2], sys.argv[3]

with open(duty_path, 'r', encoding='utf-8') as f:
    duty = json.load(f)
try:
    with open(usage_path, 'r', encoding='utf-8') as f:
        usage = json.load(f)
except Exception:
    usage = {}

providers = {}
for p in usage.get('usage', {}).get('providers', []) or []:
    name = p.get('provider')
    if not name:
        continue
    err = (p.get('error') or '').lower()
    windows = p.get('windows') or []
    if err and any(x in err for x in ['429', 'rate', 'quota', 'limit', 'exceed']):
        providers[name] = 100
    elif windows:
        providers[name] = max(int(w.get('usedPercent', 0) or 0) for w in windows)
    else:
        providers[name] = 0

agent_to_provider = {
    'claude': 'anthropic',
    'codex': 'openai-codex',
    'gemini': 'google',
}

def usage_pct_for_agent(agent: str) -> int:
    provider = agent_to_provider.get(agent, '')
    if provider in providers:
        return providers[provider]
    # fallback: fuzzy search for provider keys containing fragments
    if agent == 'gemini':
        for k,v in providers.items():
            if 'gemini' in k or 'google' in k:
                return v
    return 0

threshold = 95

def model_for(agent: str, role: str, available: dict):
    models = (available.get(agent, {}) or {}).get('models', {}) or {}
    def has(m):
        return models.get(m, {}).get('status') == 'available'
    if agent == 'codex':
        return 'gpt-5.3-codex' if has('gpt-5.3-codex') or True else 'gpt-5.3-codex'
    if agent == 'claude':
        if role == 'architect' and has('claude-opus-4-6'):
            return 'claude-opus-4-6'
        return 'claude-sonnet-4-6' if has('claude-sonnet-4-6') else 'claude-opus-4-6'
    if agent == 'gemini':
        if role == 'reviewer' and models.get('gemini-2.5-pro', {}).get('status') == 'available':
            return 'gemini-2.5-pro'
        return 'gemini-2.5-flash' if models.get('gemini-2.5-flash', {}).get('status') == 'available' else 'gemini-2.5-pro'
    return ''

def cmd_for(agent: str, model: str):
    if agent == 'claude':
        return f'claude --model {model} --permission-mode bypassPermissions --print'
    if agent == 'codex':
        return f'codex exec --model {model} --full-auto -'
    if agent == 'gemini':
        return f'gemini -m {model} -p'
    return ''

available = duty.get('availableAgents', {})
old = deepcopy(duty.get('dutyTable', {}))
new = deepcopy(old)
changes = []

# provider preference when rotating: codex > claude > gemini
preferred_agents = ['codex', 'claude', 'gemini']

for role, cfg in old.items():
    cur_agent = cfg.get('agent', '')
    cur_pct = usage_pct_for_agent(cur_agent)
    if cur_pct < threshold:
        continue

    # rotate this role to a DIFFERENT brand not nearing threshold
    for candidate in preferred_agents:
        if candidate == cur_agent:
            continue
        pct = usage_pct_for_agent(candidate)
        if pct >= threshold:
            continue
        model = model_for(candidate, role, available)
        if not model:
            continue
        new[role] = {
            'agent': candidate,
            'model': model,
            'reason': f'Auto-rotated: previous provider near limit ({cur_pct}% >= {threshold}%).',
            'nonInteractiveCmd': cmd_for(candidate, model),
        }
        changes.append((role, f"{cur_agent}/{cfg.get('model','?')}", f"{candidate}/{model}", cur_pct, pct))
        break

if changes:
    duty['dutyTable'] = new

# Keep 6-hour cadence metadata
now = datetime.datetime.now().astimezone()
duty['assessedAt'] = now.isoformat()
duty['nextAssessment'] = (now + datetime.timedelta(hours=6)).isoformat()

hist = duty.setdefault('history', [])
if changes:
    hist.append({
        'date': now.strftime('%Y-%m-%d %H:%M'),
        'changes': '; '.join([f"{r}: {a} -> {b} (from {cp}%)" for r,a,b,cp,_ in changes]),
        'dutyAssignments': ', '.join([f"{r}={duty['dutyTable'][r]['agent']}/{duty['dutyTable'][r]['model']}" for r in duty['dutyTable']]),
    })

with open(duty_path, 'w', encoding='utf-8') as f:
    json.dump(duty, f, indent=2)
    f.write('\n')

# Sync router copy if present
try:
    if router_path and router_path.strip():
        with open(router_path, 'w', encoding='utf-8') as f:
            json.dump(duty, f, indent=2)
            f.write('\n')
except Exception:
    pass

print('CHANGES', len(changes))
for c in changes:
    print('ROTATE', c)
PY

# Optional notify when changed
if grep -q "^ROTATE" <(python3 - <<'PY' "$DUTY_TABLE"
import json,sys
j=json.load(open(sys.argv[1]))
h=j.get('history',[])
if h:
    last=h[-1].get('changes','')
    if '->' in last:
        print('ROTATE')
PY
); then
  LAST_CHANGE=$(python3 - <<'PY' "$DUTY_TABLE"
import json,sys
j=json.load(open(sys.argv[1]))
h=j.get('history',[])
print(h[-1].get('changes','')) if h else print('')
PY
)
  if [[ -n "$NOTIFY_TARGET" ]]; then
    openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "⚙️ Duty auto-rotation applied: $LAST_CHANGE" 2>/dev/null || true
  fi
fi

rm -f "$USAGE_JSON"
