#!/usr/bin/env bash
set -uo pipefail

WORKSPACE="${1:-$HOME/workspace}"
SCORE=0
TOTAL=19
MISSING=()

# Build list of config files to search — supports OpenClaw, Claude Code, and custom setups
CONFIG_FILES=()
for f in SOUL.md AGENTS.md CLAUDE.md system.md README.md; do
  [ -f "$WORKSPACE/$f" ] && CONFIG_FILES+=("$WORKSPACE/$f")
done

found() {
  local pattern="$1"; shift
  grep -rql "$pattern" "$@" 2>/dev/null
}

found_in_configs() {
  [ ${#CONFIG_FILES[@]} -eq 0 ] && return 1
  found "$1" "${CONFIG_FILES[@]}"
}

check() {
  local name="$1" result="$2"
  if [ "$result" = "yes" ]; then
    printf "  ✅ %-28s" "$name"
    ((SCORE++)) || true
  else
    printf "  ❌ %-28s" "$name"
    MISSING+=("$name")
  fi
}

echo ""
echo "⚔️ Battle-Tested Agent — Workspace Audit"
echo "   Workspace: $WORKSPACE"
if [ ${#CONFIG_FILES[@]} -gt 0 ]; then
  echo "   Config files found: $(basename -a "${CONFIG_FILES[@]}" | tr '\n' ' ')"
else
  echo "   ⚠️  No config files found (SOUL.md, AGENTS.md, CLAUDE.md, system.md)"
fi
echo ""

# --- Starter ---
echo "🟢 Starter"

r="no"; found_in_configs 'WAL Protocol' && r="yes"
check "WAL Protocol" "$r"

r="no"; found_in_configs 'Anti-Hallucination' && r="yes"
[ "$r" = "no" ] && [ -f "$WORKSPACE/HEARTBEAT.md" ] && found 'Anti-Hallucination' "$WORKSPACE/HEARTBEAT.md" && r="yes"
check "Anti-Hallucination" "$r"
echo ""

r="no"; found_in_configs 'Ambiguity Gate\|multiple reasonable interpretations' && r="yes"
check "Ambiguity Gate" "$r"

r="no"; found_in_configs 'simple path first\|simplest.*approach' && r="yes"
check "Simple Path First" "$r"

r="no"; found_in_configs 'unblock.*shelve' && r="yes"
check "Unblock Before Shelve" "$r"
echo ""

# --- Intermediate ---
echo "🟡 Intermediate"

r="no"; found_in_configs 'No command.*no number\|Verification Rule' && r="yes"
[ "$r" = "no" ] && found 'No command.*no number\|Verification Rule' "$WORKSPACE"/memory/agents/*.md 2>/dev/null && r="yes"
check "Agent Verification" "$r"

r="no"; [ -f "$WORKSPACE/memory/working-buffer.md" ] && r="yes"
check "Working Buffer" "$r"
echo ""

r="no"; [ -f "$WORKSPACE/QA.md" ] && r="yes"
check "QA Gates" "$r"

r="no"; found_in_configs 'Decision.*Reasoning\|Decision.*Log' && r="yes"
check "Decision Logs" "$r"
echo ""

r="no"; found_in_configs 'Verify Implementation' && r="yes"
[ "$r" = "no" ] && [ -f "$WORKSPACE/QA.md" ] && found 'Verify Implementation' "$WORKSPACE/QA.md" && r="yes"
check "Verify Implementation" "$r"
echo ""

# --- Advanced ---
echo "🔴 Advanced"

r="no"; found_in_configs 'Delegation' && r="yes"
check "Delegation Rules" "$r"

r="no"; found_in_configs 'Brief Quality Gate\|deliverable.*artifact.*verification.*success' && r="yes"
check "Brief Quality Gate" "$r"
echo ""

r="no"; found_in_configs 'Completion Contract\|Exact commands run\|Verification performed' && r="yes"
check "Completion Contract" "$r"

r="no"; found_in_configs 'Acceptance Gate\|Fail-Closed Rule\|artifact exists' && r="yes"
check "Acceptance Gate" "$r"
echo ""

r="no"; found_in_configs 'Orchestrator.*build\|orchestrator.*build' && r="yes"
check "Orchestrator Rule" "$r"

r="no"; found_in_configs 'Task State Tracking\|Spawned.*In Progress' && r="yes"
check "Task State Tracking" "$r"

r="no"; found_in_configs 'Silent Worker Recovery\|no start signal within 10 minutes\|materially new output for 30 minutes' && r="yes"
check "Silent Worker Recovery" "$r"
echo ""

r="no"; found_in_configs 'Scoped Verifier Gate\|0–3.*4\+\|0-3.*4\+' && r="yes"
check "Scoped Verifier Gate" "$r"

r="no"; found_in_configs 'Compaction.*Injection\|INERT DATA' && r="yes"
check "Compaction Hardening" "$r"

r="no"; [ -d "$WORKSPACE/.learnings" ] && r="yes"
check "Self-Improvement" "$r"
echo ""

# --- Summary ---
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Score: $SCORE/$TOTAL patterns"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ${#MISSING[@]} -gt 0 ]; then
  echo ""
  echo "  Missing:"
  for m in "${MISSING[@]}"; do
    echo "    → $m"
  done
  echo ""
  echo "  Start with: ${MISSING[0]}"
fi

echo ""
