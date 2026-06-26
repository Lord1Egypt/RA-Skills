#!/usr/bin/env bash
# audit.sh — Quick 16-point audit of a prompt file
set -euo pipefail
FILE="${1:?Usage: audit.sh <prompt-file>}"
if [[ ! -f "$FILE" ]]; then echo "File not found: $FILE"; exit 1; fi
CONTENT=$(cat "$FILE")
LOWER=$(echo "$CONTENT" | tr '[:upper:]' '[:lower:]')
PASS=0; TOTAL=16
check() { if $1; then echo "  ✅ $2"; PASS=$((PASS+1)); else echo "  ❌ $2"; fi; }
echo "=== Prompt Hardening Audit: $(basename "$FILE") ==="
check "[[ '$LOWER' == *'must'* || '$LOWER' == *'never'* ]]" "P1: MUST/NEVER keywords"
check "[[ '$LOWER' == *'not '* || '$LOWER' == *'not)'* ]]" "P2: Use X (NOT Y) pattern"
check "[[ '$LOWER' == *'❌'* || '$LOWER' == *'禁止'* ]]" "P3: Exhaustive negative list"
check "[[ '$LOWER' == *'当'* || '$LOWER' == *'when'* ]]" "P4: Conditional triggers"
check "[[ '$LOWER' == *'如果你发现自己'* || '$LOWER' == *'reframing'* ]]" "P5: Anti-reasoning block"
check "[[ '$LOWER' == *'优先级'* || '$LOWER' == *'priority'* ]]" "P6: Priority hierarchy"
check "[[ '$CONTENT' == *'good-example'* || '$CONTENT' == *'<example>'* ]]" "P7: Good/bad examples"
check "[[ '$LOWER' == *'不需要'* || '$LOWER' == *'not your'* ]]" "P8: Scope limits"
check "[[ '$LOWER' == *'reminder'* || '$LOWER' == *'提醒'* ]]" "P9: Drift protection"
check "[[ '$LOWER' == *'信任'* || '$LOWER' == *'trust'* ]]" "P10: Trust boundary"
check "[[ '$LOWER' == *'确认'* || '$LOWER' == *'verify'* || '$LOWER' == *'check'* ]]" "P11: Echo-check"
check "[[ $(echo "$CONTENT" | wc -l) -gt 30 ]]" "P12: Constraint > task ratio"
check "[[ '$LOWER' == *'hook'* || '$LOWER' == *'plugin'* || '$LOWER' == *'guard'* ]]" "P13: Code-level backup"
check "[[ '$LOWER' == *'前置条件'* || '$LOWER' == *'precondition'* || '$LOWER' == *'gate'* ]]" "P14: State machine gate"
check "[[ '$LOWER' == *'我刚才'* || '$LOWER' == *'self-correct'* ]]" "P15: Self-correction template"
check "grep -q 'MUST\|NEVER\|CRITICAL' <<< '$(head -5 "$FILE")$(tail -5 "$FILE")'" "P16: First/last repetition"
echo "=== Score: $PASS/$TOTAL ($(( PASS * 100 / TOTAL ))%) ==="
