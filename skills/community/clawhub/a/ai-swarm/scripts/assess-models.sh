#!/usr/bin/env bash
# assess-models.sh — Weekly model availability assessment
# Tests all configured agent CLIs and models, updates duty-table.json
#
# Strategy:
#   1. Test all models across all 3 agents (Claude, Codex, Gemini)
#   2. Assign optimal 3-vendor duty table (different vendor per role)
#   3. If any vendor hits token/quota limits mid-week → auto-fallback to Claude-heavy table
#
# Usage: assess-models.sh [--dry-run] [--fallback]
#   --dry-run:  test models but don't update duty-table.json
#   --fallback: force Claude-heavy fallback (for mid-week quota issues)

set -euo pipefail

# macOS compatibility: use gtimeout if timeout not available
if ! command -v timeout &>/dev/null && command -v gtimeout &>/dev/null; then
  timeout() { gtimeout "$@"; }
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SCRIPT_DIR/swarm.conf" ]] && source "$SCRIPT_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"
DUTY_TABLE="$SCRIPT_DIR/duty-table.json"
RESULTS_LOG="$SCRIPT_DIR/assessment.log"
DRY_RUN=""
FORCE_FALLBACK=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --fallback) FORCE_FALLBACK=1 ;;
  esac
done

[ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null || true

echo "Model Assessment — $(date '+%Y-%m-%d %H:%M %Z')" | tee "$RESULTS_LOG"
echo "=========================================" | tee -a "$RESULTS_LOG"

# ============================================================
# FALLBACK: Claude-heavy duty table (high token limit)
# ============================================================
apply_fallback() {
  echo "" | tee -a "$RESULTS_LOG"
  echo "⚠️  FALLBACK MODE: Switching to Claude-heavy duty table" | tee -a "$RESULTS_LOG"

  if [[ -n "$DRY_RUN" ]]; then
    echo "Dry run — not updating duty-table.json"
    return
  fi

  python3 -c "
import json, datetime
with open('$DUTY_TABLE') as f: data = json.load(f)
now = datetime.datetime.now().astimezone()
data['assessedAt'] = now.isoformat()
# Re-assess in 3 days (not full week) to try optimal table sooner
data['nextAssessment'] = (now + datetime.timedelta(hours=6)).isoformat()
data['dutyTable'] = {
    'architect': {'agent': 'claude', 'model': 'claude-opus-4-6', 'reason': 'FALLBACK: High token limit, best reasoning', 'nonInteractiveCmd': 'claude --model claude-opus-4-6 --permission-mode bypassPermissions --print'},
    'builder': {'agent': 'claude', 'model': 'claude-sonnet-4-6', 'reason': 'FALLBACK: High token limit, reliable', 'nonInteractiveCmd': 'claude --model claude-sonnet-4-6 --permission-mode bypassPermissions --print'},
    'reviewer': {'agent': 'claude', 'model': 'claude-sonnet-4-6', 'reason': 'FALLBACK: High token limit, fast review', 'nonInteractiveCmd': 'claude --model claude-sonnet-4-6 --permission-mode bypassPermissions --print'},
    'integrator': {'agent': 'claude', 'model': 'claude-sonnet-4-6', 'reason': 'FALLBACK: High token limit, fastest reliable', 'nonInteractiveCmd': 'claude --model claude-sonnet-4-6 --permission-mode bypassPermissions --print'}
}
data['history'].append({
    'date': now.strftime('%Y-%m-%d'),
    'changes': 'FALLBACK to Claude-heavy table (token/quota limits on Codex/Gemini)',
    'dutyAssignments': 'architect=claude/opus-4-6, builder=claude/sonnet-4-6, reviewer=claude/sonnet-4-6, integrator=claude/sonnet-4-6'
})
with open('$DUTY_TABLE', 'w') as f: json.dump(data, f, indent=2)
print('duty-table.json updated (FALLBACK)')
" | tee -a "$RESULTS_LOG"

  # Notify
  if [[ -n "$NOTIFY_TARGET" ]]; then
    openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" \
      --message "⚠️ Swarm duty table → FALLBACK (Claude-heavy). Codex/Gemini hit limits. Will re-assess in 3 days." \
      2>/dev/null || echo "⚠️ Notification send failed" >> "$RESULTS_LOG"
  fi
}

if [[ -n "$FORCE_FALLBACK" ]]; then
  apply_fallback
  exit 0
fi

# ============================================================
# TEST ALL MODELS
# ============================================================
declare -A MODEL_STATUS

test_model() {
  local agent="$1" model="$2" cmd="$3"
  local tmpout result_file
  result_file=$(mktemp)
  echo -n "  Testing $agent / $model ... " | tee -a "$RESULTS_LOG"

  # Create a temp git repo for codex (codex requires a git repo)
  local tmpdir=""
  if [[ "$agent" == "codex" ]]; then
    tmpdir=$(mktemp -d)
    git init -q "$tmpdir" 2>/dev/null
    cmd="cd $tmpdir && $cmd"
  fi

  # Run from /tmp to avoid CLIs picking up workspace context.
  # Gemini needs stdin closed (hangs waiting for input otherwise).
  # Claude needs stdin open (fails with closed stdin).
  local pid exit_code=0
  if [[ "$agent" == "gemini" ]]; then
    bash -c "cd /tmp && $cmd" < /dev/null > "$result_file" 2>&1 &
  else
    bash -c "cd /tmp && $cmd" > "$result_file" 2>&1 &
  fi
  pid=$!

  # Wait up to 45 seconds
  local waited=0 running=1
  while (( running && waited < 45 )); do
    if ! kill -0 "$pid" 2>/dev/null; then
      running=0
    else
      sleep 1
      (( waited++ )) || true
    fi
  done

  if (( running )) && kill -0 "$pid" 2>/dev/null; then
    # Still running after timeout — force kill
    kill -9 "$pid" 2>/dev/null
    wait "$pid" 2>/dev/null || true
    echo "TIMEOUT" | tee -a "$RESULTS_LOG"
    MODEL_STATUS["${agent}/${model}"]="unavailable"
  else
    wait "$pid" 2>/dev/null
    exit_code=$?
    local result
    result=$(cat "$result_file")
    if [[ $exit_code -eq 0 ]] && ! echo "$result" | grep -qi "error\|quota\|unauthorized\|401\|429\|rate.limit\|exceeded\|capacity"; then
      echo "OK" | tee -a "$RESULTS_LOG"
      MODEL_STATUS["${agent}/${model}"]="available"
    else
      echo "FAIL: $(echo "$result" | tail -1)" | tee -a "$RESULTS_LOG"
      MODEL_STATUS["${agent}/${model}"]="unavailable"
    fi
  fi

  rm -f "$result_file" 2>/dev/null
  [[ -n "$tmpdir" ]] && rm -rf "$tmpdir" 2>/dev/null || true
}

PROBE="Reply with ONLY the word HELLO, nothing else."

echo "" | tee -a "$RESULTS_LOG"
echo "Claude Code (OAuth)" | tee -a "$RESULTS_LOG"
test_model "claude" "claude-opus-4-6" "claude --model claude-opus-4-6 --permission-mode bypassPermissions --print '$PROBE'"
test_model "claude" "claude-sonnet-4-6" "claude --model claude-sonnet-4-6 --permission-mode bypassPermissions --print '$PROBE'"

echo "" | tee -a "$RESULTS_LOG"
echo "Codex (OAuth/ChatGPT Plus)" | tee -a "$RESULTS_LOG"
test_model "codex" "gpt-5.3-codex" "codex exec '$PROBE'"

echo "" | tee -a "$RESULTS_LOG"
echo "Gemini (OAuth/Google)" | tee -a "$RESULTS_LOG"
test_model "gemini" "gemini-2.5-pro" "gemini -m gemini-2.5-pro -p '$PROBE'"
test_model "gemini" "gemini-2.5-flash" "gemini -m gemini-2.5-flash -p '$PROBE'"

echo "" | tee -a "$RESULTS_LOG"
echo "=========================================" | tee -a "$RESULTS_LOG"

# Print summary
echo "Results:" | tee -a "$RESULTS_LOG"
for key in "${!MODEL_STATUS[@]}"; do
  echo "  $key = ${MODEL_STATUS[$key]}" | tee -a "$RESULTS_LOG"
done

# ============================================================
# CHECK IF WE NEED FALLBACK
# ============================================================
CODEX_OK="${MODEL_STATUS[codex/gpt-5.3-codex]:-unavailable}"
GEMINI_PRO_OK="${MODEL_STATUS[gemini/gemini-2.5-pro]:-unavailable}"
GEMINI_FLASH_OK="${MODEL_STATUS[gemini/gemini-2.5-flash]:-unavailable}"
CLAUDE_SONNET_OK="${MODEL_STATUS[claude/claude-sonnet-4-6]:-unavailable}"
CLAUDE_OPUS_OK="${MODEL_STATUS[claude/claude-opus-4-6]:-unavailable}"

# If both Codex AND Gemini are down → fallback to Claude-heavy
if [[ "$CODEX_OK" != "available" && "$GEMINI_PRO_OK" != "available" && "$GEMINI_FLASH_OK" != "available" ]]; then
  echo "" | tee -a "$RESULTS_LOG"
  echo "Both Codex and Gemini unavailable → triggering fallback" | tee -a "$RESULTS_LOG"
  apply_fallback
  exit 0
fi

# ============================================================
# ASSIGN OPTIMAL 3-VENDOR DUTY TABLE
# ============================================================

# Architect: Claude Opus (always, it's the best reasoner)
ARCHITECT="claude/claude-opus-4-6"
[[ "$CLAUDE_OPUS_OK" != "available" ]] && ARCHITECT="claude/claude-sonnet-4-6"

# Workhorse: Codex preferred, fallback to Claude Sonnet
if [[ "$CODEX_OK" == "available" ]]; then
  BUILDER="codex/gpt-5.3-codex"
else
  BUILDER="claude/claude-sonnet-4-6"
  echo "⚠️ Codex unavailable, Claude Sonnet takes builder" | tee -a "$RESULTS_LOG"
fi

# Reviewer: Gemini Pro preferred, fallback to Flash, then Claude
if [[ "$GEMINI_PRO_OK" == "available" ]]; then
  REVIEWER="gemini/gemini-2.5-pro"
elif [[ "$GEMINI_FLASH_OK" == "available" ]]; then
  REVIEWER="gemini/gemini-2.5-flash"
else
  REVIEWER="claude/claude-sonnet-4-6"
  echo "⚠️ Gemini unavailable, Claude Sonnet takes reviewer" | tee -a "$RESULTS_LOG"
fi

# Speedster: Claude Sonnet (always — fast + high token limit)
INTEGRATOR="claude/claude-opus-4-6"

echo "" | tee -a "$RESULTS_LOG"
echo "Duty Assignments:" | tee -a "$RESULTS_LOG"
echo "  architect  = $ARCHITECT" | tee -a "$RESULTS_LOG"
echo "  builder  = $BUILDER" | tee -a "$RESULTS_LOG"
echo "  reviewer   = $REVIEWER" | tee -a "$RESULTS_LOG"
echo "  integrator  = $INTEGRATOR" | tee -a "$RESULTS_LOG"

[[ -n "$DRY_RUN" ]] && { echo "Dry run — not updating duty-table.json"; exit 0; }

# ============================================================
# UPDATE DUTY TABLE
# ============================================================
# Build model status summary from bash vars
MODEL_SUMMARY=""
for key in "${!MODEL_STATUS[@]}"; do
  MODEL_SUMMARY="${MODEL_SUMMARY}${key}=${MODEL_STATUS[$key]}, "
done
MODEL_SUMMARY="${MODEL_SUMMARY%, }"

python3 -c "
import json, datetime
with open('$DUTY_TABLE') as f: data = json.load(f)
now = datetime.datetime.now().astimezone()
data['assessedAt'] = now.isoformat()
data['nextAssessment'] = (now + datetime.timedelta(hours=6)).isoformat()

def cmd(a, m):
    if a == 'claude': return f'claude --model {m} --permission-mode bypassPermissions --print'
    if a == 'codex': return f'codex --model {m} --full-auto exec'
    if a == 'gemini': return f'gemini -m {m} -p'
    return ''

for role, am in {'architect':'$ARCHITECT','builder':'$BUILDER','reviewer':'$REVIEWER','integrator':'$INTEGRATOR'}.items():
    if am:
        a, m = am.split('/')
        data['dutyTable'][role] = {'agent': a, 'model': m, 'reason': role + ' role (auto-assessed)', 'nonInteractiveCmd': cmd(a, m)}

data['history'].append({
    'date': now.strftime('%Y-%m-%d'),
    'changes': 'Weekly assessment: $MODEL_SUMMARY',
    'dutyAssignments': 'architect=$ARCHITECT, builder=$BUILDER, reviewer=$REVIEWER, integrator=$INTEGRATOR'
})
with open('$DUTY_TABLE', 'w') as f: json.dump(data, f, indent=2)
print('duty-table.json updated')
"

# Notify
if [[ -n "$NOTIFY_TARGET" ]]; then
  openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" \
    --message "📊 Weekly model assessment complete. Duty: architect=$ARCHITECT, builder=$BUILDER, reviewer=$REVIEWER, integrator=$INTEGRATOR" \
    2>/dev/null || echo "Notification send failed" >> "$RESULTS_LOG"
fi

echo "" | tee -a "$RESULTS_LOG"
echo "Assessment complete at $(date '+%H:%M %Z')" | tee -a "$RESULTS_LOG"
