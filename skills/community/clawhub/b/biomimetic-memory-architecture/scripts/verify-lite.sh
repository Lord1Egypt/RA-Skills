#!/bin/bash
# BMA — Verify integrated memory architecture
# Run from OpenClaw workspace root: bash skills/biomimetic-memory-architecture/scripts/verify.sh
set -euo pipefail
WORKSPACE="${CLAWD_WORKSPACE:-$(pwd)}"
PASS=0; WARN=0; FAIL=0
check(){ label="$1"; result="$2"; case "$result" in ok) echo "✅ $label"; PASS=$((PASS+1));; warn) echo "⚠️  $label"; WARN=$((WARN+1));; *) echo "❌ $label"; FAIL=$((FAIL+1));; esac; }
cd "$WORKSPACE"
echo "🧬 BMA Verification"
echo "Workspace: $WORKSPACE"

for f in MEMORY.md SOUL.md USER.md TOOLS.md AGENTS.md; do [ -f "$f" ] && check "$f exists" ok || check "$f missing" fail; done
for d in memory memory/projects memory/runbooks memory/contacts memory/workflows memory/archive memory/lesson-imprint skills/biomimetic-memory-architecture; do [ -d "$d" ] && check "$d/ exists" ok || check "$d/ missing" fail; done

[ -f memory/preferences.md ] && check "memory/preferences.md exists" ok || check "memory/preferences.md missing" warn
[ -f memory/lesson-imprint/lessons.json ] && check "Lesson-Imprint lessons.json exists" ok || check "Lesson-Imprint lessons.json missing; run lesson_imprint.py init" warn
[ -f memory/lesson-imprint/config.json ] && check "Lesson-Imprint config.json exists" ok || check "Lesson-Imprint config.json missing; run lesson_imprint.py init" warn
[ -f memory/lesson-imprint/BOOTSTRAP.md ] && check "Lesson-Imprint BOOTSTRAP.md exists" ok || check "Lesson-Imprint BOOTSTRAP.md missing; run lesson_imprint.py promote" warn

python3 skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py --workspace . --older-than-days 30 --limit 1 >/tmp/bma-verify-audit.out 2>/tmp/bma-verify-audit.err && check "Retention audit script runs" ok || { cat /tmp/bma-verify-audit.err; check "Retention audit script failed" fail; }
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py init >/tmp/bma-lesson-init.out 2>/tmp/bma-lesson-init.err && check "Lesson-Imprint init command runs" ok || { cat /tmp/bma-lesson-init.err; check "Lesson-Imprint init failed" fail; }
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py validate >/tmp/bma-lesson-validate.out 2>/tmp/bma-lesson-validate.err && check "Lesson-Imprint store validates" ok || { cat /tmp/bma-lesson-validate.err; check "Lesson-Imprint validation failed" fail; }

if command -v openclaw >/dev/null 2>&1; then
  cron_list=$(openclaw cron list 2>/dev/null || true)
  echo "$cron_list" | grep -qi "distill" && check "Daily distillation cron found" ok || check "Daily distillation cron not found" warn
  echo "$cron_list" | grep -qi "synth" && check "Weekly synthesis cron found" ok || check "Weekly synthesis cron not found" warn
else
  check "openclaw CLI unavailable; cron not verified" warn
fi

if command -v openclaw >/dev/null 2>&1; then
  doctor=$(openclaw doctor 2>&1 || true)
  echo "$doctor" | grep -q "Errors: 0" && check "OpenClaw plugins report Errors: 0" ok || check "OpenClaw doctor should be reviewed" warn
fi

echo ""
echo "Result: pass=$PASS warn=$WARN fail=$FAIL"
[ "$FAIL" -eq 0 ]
