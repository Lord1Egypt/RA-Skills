#!/usr/bin/env bash
# assess-models.sh — Weekly model availability assessment
# Runs on the Saturday 12pm Pacific cadence and updates duty-table.json.
#
# Usage: assess-models.sh [--dry-run]
#   --dry-run: test models but don't update duty-table.json

set -euo pipefail

# macOS compatibility: use gtimeout if timeout not available
if ! command -v timeout &>/dev/null && command -v gtimeout &>/dev/null; then
  timeout() { gtimeout "$@"; }
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SCRIPT_DIR/swarm.conf" ]] && source "$SCRIPT_DIR/swarm.conf"
[[ -n "${DEEPSEEK_API_KEY:-}" ]] && export DEEPSEEK_API_KEY
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"
DUTY_TABLE="$SCRIPT_DIR/duty-table.json"
RESULTS_LOG="$SCRIPT_DIR/assessment.log"
DRY_RUN=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
  esac
done

[ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null || true

echo "Model Assessment — $(date '+%Y-%m-%d %H:%M %Z')" | tee "$RESULTS_LOG"
echo "=========================================" | tee -a "$RESULTS_LOG"

declare -A MODEL_STATUS

test_model() {
  local agent="$1" model="$2" cmd="$3"
  local result_file exit_code=0 tmpdir=""
  result_file=$(mktemp)
  echo -n "  Testing $agent / $model ... " | tee -a "$RESULTS_LOG"

  if [[ "$agent" == "codex" ]]; then
    tmpdir=$(mktemp -d)
    git init -q "$tmpdir" 2>/dev/null
    cmd="cd $tmpdir && $cmd"
  fi

  if [[ "$agent" == "gemini" || "$agent" == "deepseek" ]]; then
    timeout 45 bash -c "cd /tmp && $cmd" < /dev/null > "$result_file" 2>&1 || exit_code=$?
  else
    timeout 45 bash -c "cd /tmp && $cmd" > "$result_file" 2>&1 || exit_code=$?
  fi

  local result
  result=$(cat "$result_file")
  if echo "$result" | grep -q '^HELLO$'; then
    echo "OK" | tee -a "$RESULTS_LOG"
    MODEL_STATUS["${agent}/${model}"]="available"
  elif [[ $exit_code -eq 0 ]] && ! echo "$result" | grep -qi "error\|quota\|unauthorized\|401\|429\|rate.limit\|exceeded\|capacity"; then
    echo "OK" | tee -a "$RESULTS_LOG"
    MODEL_STATUS["${agent}/${model}"]="available"
  else
    echo "FAIL: $(echo "$result" | tail -1)" | tee -a "$RESULTS_LOG"
    MODEL_STATUS["${agent}/${model}"]="unavailable"
  fi

  rm -f "$result_file" 2>/dev/null
  [[ -n "$tmpdir" ]] && rm -rf "$tmpdir" 2>/dev/null || true
}

PROBE="Reply with ONLY the word HELLO, nothing else."

echo "" | tee -a "$RESULTS_LOG"
echo "Codex (OAuth/ChatGPT Plus)" | tee -a "$RESULTS_LOG"
test_model "codex" "gpt-5.5" "codex exec --model gpt-5.5 '$PROBE'"
test_model "codex" "gpt-5.3-codex" "codex exec --model gpt-5.3-codex '$PROBE'"

echo "" | tee -a "$RESULTS_LOG"
echo "Gemini (OAuth/Google)" | tee -a "$RESULTS_LOG"
test_model "gemini" "gemini-2.5-pro" "gemini -m gemini-2.5-pro -p '$PROBE'"
test_model "gemini" "gemini-2.5-flash" "gemini -m gemini-2.5-flash -p '$PROBE'"

echo "" | tee -a "$RESULTS_LOG"
echo "DeepSeek (API key)" | tee -a "$RESULTS_LOG"
if [[ -n "${DEEPSEEK_API_KEY:-}" ]]; then
  test_model "deepseek" "deepseek-v4-pro-max" "deepseek -m deepseek-v4-pro-max -y -p '$PROBE'"
else
  echo "  Skipping deepseek / deepseek-v4-pro-max ... DEEPSEEK_API_KEY not set" | tee -a "$RESULTS_LOG"
  MODEL_STATUS["deepseek/deepseek-v4-pro-max"]="unavailable"
fi

echo "" | tee -a "$RESULTS_LOG"
echo "=========================================" | tee -a "$RESULTS_LOG"
echo "Results:" | tee -a "$RESULTS_LOG"
for key in "${!MODEL_STATUS[@]}"; do
  echo "  $key = ${MODEL_STATUS[$key]}" | tee -a "$RESULTS_LOG"
done

CODEX55_OK="${MODEL_STATUS[codex/gpt-5.5]:-unavailable}"
CODEX53_OK="${MODEL_STATUS[codex/gpt-5.3-codex]:-unavailable}"
DEEPSEEK_OK="${MODEL_STATUS[deepseek/deepseek-v4-pro-max]:-unavailable}"
GEMINI_PRO_OK="${MODEL_STATUS[gemini/gemini-2.5-pro]:-unavailable}"
GEMINI_FLASH_OK="${MODEL_STATUS[gemini/gemini-2.5-flash]:-unavailable}"

if [[ "$CODEX55_OK" == "available" ]]; then
  ARCHITECT="codex/gpt-5.5"
  INTEGRATOR="codex/gpt-5.5"
elif [[ "$CODEX53_OK" == "available" ]]; then
  ARCHITECT="codex/gpt-5.3-codex"
  INTEGRATOR="codex/gpt-5.3-codex"
elif [[ "$GEMINI_PRO_OK" == "available" ]]; then
  ARCHITECT="gemini/gemini-2.5-pro"
  INTEGRATOR="gemini/gemini-2.5-pro"
elif [[ "$GEMINI_FLASH_OK" == "available" ]]; then
  ARCHITECT="gemini/gemini-2.5-flash"
  INTEGRATOR="gemini/gemini-2.5-flash"
else
  echo "No viable architect/integrator model found." | tee -a "$RESULTS_LOG"
  exit 1
fi

if [[ "$DEEPSEEK_OK" == "available" ]]; then
  BUILDER="deepseek/deepseek-v4-pro-max"
  REVIEWER="deepseek/deepseek-v4-pro-max"
elif [[ "$CODEX55_OK" == "available" ]]; then
  BUILDER="codex/gpt-5.5"
  REVIEWER="codex/gpt-5.5"
elif [[ "$CODEX53_OK" == "available" ]]; then
  BUILDER="codex/gpt-5.3-codex"
  REVIEWER="codex/gpt-5.3-codex"
elif [[ "$GEMINI_PRO_OK" == "available" ]]; then
  BUILDER="gemini/gemini-2.5-pro"
  REVIEWER="gemini/gemini-2.5-pro"
elif [[ "$GEMINI_FLASH_OK" == "available" ]]; then
  BUILDER="gemini/gemini-2.5-flash"
  REVIEWER="gemini/gemini-2.5-flash"
else
  echo "No viable builder/reviewer model found." | tee -a "$RESULTS_LOG"
  exit 1
fi

echo "" | tee -a "$RESULTS_LOG"
echo "Duty Assignments:" | tee -a "$RESULTS_LOG"
echo "  architect  = $ARCHITECT" | tee -a "$RESULTS_LOG"
echo "  builder    = $BUILDER" | tee -a "$RESULTS_LOG"
echo "  reviewer   = $REVIEWER" | tee -a "$RESULTS_LOG"
echo "  integrator = $INTEGRATOR" | tee -a "$RESULTS_LOG"

[[ -n "$DRY_RUN" ]] && { echo "Dry run — not updating duty-table.json"; exit 0; }

MODEL_SUMMARY=""
for key in "${!MODEL_STATUS[@]}"; do
  MODEL_SUMMARY="${MODEL_SUMMARY}${key}=${MODEL_STATUS[$key]}, "
done
MODEL_SUMMARY="${MODEL_SUMMARY%, }"

python3 - <<PY
import json, datetime
from zoneinfo import ZoneInfo
with open('$DUTY_TABLE') as f:
    data = json.load(f)
pacific = ZoneInfo('America/Los_Angeles')
now = datetime.datetime.now(pacific)
next_assessment = now.replace(hour=12, minute=0, second=0, microsecond=0)
days_until_saturday = (5 - next_assessment.weekday()) % 7
next_assessment += datetime.timedelta(days=days_until_saturday)
if next_assessment <= now:
    next_assessment += datetime.timedelta(days=7)
data['assessedAt'] = now.isoformat()
data['nextAssessment'] = next_assessment.isoformat()

def cmd(agent, model):
    if agent == 'codex':
        return f'codex exec --model {model} --full-auto'
    if agent == 'gemini':
        return f'gemini -m {model} -p'
    if agent == 'deepseek':
        return f'deepseek -m {model} -y -p'
    return ''

for role, am in {'architect': '$ARCHITECT', 'builder': '$BUILDER', 'reviewer': '$REVIEWER', 'integrator': '$INTEGRATOR'}.items():
    existing = data.get('dutyTable', {}).get(role, {})
    if existing.get('pinned'):
        continue
    agent, model = am.split('/')
    data['dutyTable'][role] = {
        'agent': agent,
        'model': model,
        'reason': f'{role} role (manual assessment)',
        'nonInteractiveCmd': cmd(agent, model)
    }

data.setdefault('history', []).append({
    'date': now.strftime('%Y-%m-%d %H:%M PDT'),
    'changes': 'Manual assessment: $MODEL_SUMMARY',
    'dutyAssignments': 'architect=$ARCHITECT, builder=$BUILDER, reviewer=$REVIEWER, integrator=$INTEGRATOR'
})

with open('$DUTY_TABLE', 'w') as f:
    json.dump(data, f, indent=2)
print('duty-table.json updated')
PY

if [[ -n "$NOTIFY_TARGET" ]]; then
  openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" \
    --message "📊 Manual model assessment complete. Duty: architect=$ARCHITECT, builder=$BUILDER, reviewer=$REVIEWER, integrator=$INTEGRATOR" \
    2>/dev/null || echo "Notification send failed" >> "$RESULTS_LOG"
fi

echo "" | tee -a "$RESULTS_LOG"
echo "Assessment complete at $(date '+%H:%M %Z')" | tee -a "$RESULTS_LOG"
