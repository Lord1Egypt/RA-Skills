#!/bin/bash
# BMA — Verify installation is working correctly
# Run from your OpenClaw workspace directory: bash skills/biomimetic-memory-architecture/scripts/verify.sh

set -euo pipefail
WORKSPACE="${CLAWD_WORKSPACE:-$(pwd)}"
PASS=0
FAIL=0
WARN=0

echo "🔍 BMA Installation Verification"
INSTALLED_VER="unknown"
[ -f "$WORKSPACE/.bma-version" ] && INSTALLED_VER="v$(cat "$WORKSPACE/.bma-version" | tr -d '[:space:]')"
echo "   Workspace: $WORKSPACE"
echo "   Version:   $INSTALLED_VER"
echo ""

check() {
  local label="$1"
  local result="$2"
  if [ "$result" = "ok" ]; then
    echo "   ✅ $label"
    PASS=$((PASS + 1))
  elif [ "$result" = "warn" ]; then
    echo "   ⚠️  $label"
    WARN=$((WARN + 1))
  else
    echo "   ❌ $label"
    FAIL=$((FAIL + 1))
  fi
}

# --- Core files ---
echo "📁 Core files:"
for f in MEMORY.md SOUL.md USER.md TOOLS.md INFRA.md BOOTSTRAP.md AGENTS.md; do
  if [ -f "$WORKSPACE/$f" ]; then
    check "$f exists" "ok"
  else
    check "$f missing" "fail"
  fi
done
echo ""

# --- Directories ---
echo "📂 Directories:"
for d in memory memory/projects memory/runbooks memory/contacts memory/workflows memory/archive; do
  if [ -d "$WORKSPACE/$d" ]; then
    check "$d/ exists" "ok"
  else
    check "$d/ missing" "fail"
  fi
done
echo ""

# --- Voice profile ---
echo "🎙️ Voice profile:"
FLAGS_FILE="$WORKSPACE/.bma-flags"
VOICE_FLAG=""
if [ -f "$FLAGS_FILE" ]; then
  VOICE_FLAG=$(grep -E '^VOICE_PROFILE=' "$FLAGS_FILE" 2>/dev/null | head -1 | cut -d'=' -f2 | tr -d '[:space:]' || true)
fi
VOICE_ENV="${BMA_VOICE_PROFILE:-}"
if [ -f "$WORKSPACE/memory/VOICE.md" ]; then
  check "VOICE.md exists (voice profiling enabled)" "ok"
  if [ "$VOICE_FLAG" = "1" ] || [ "$VOICE_ENV" = "1" ]; then
    check "Voice profiling runtime gate is enabled (flag/env)" "ok"
  else
    check "VOICE.md exists but runtime voice gate is OFF (set VOICE_PROFILE=1 in .bma-flags or BMA_VOICE_PROFILE=1)" "warn"
  fi
else
  check "VOICE.md not found (voice profiling not enabled — this is fine if you skipped it)" "warn"
fi
echo ""

# --- Cron jobs ---
echo "⏰ Cron jobs:"
if command -v openclaw &>/dev/null; then
  CRON_LIST=$(openclaw cron list 2>/dev/null || echo "")
  if echo "$CRON_LIST" | grep -qi "distill"; then
    check "Daily Memory Distillation cron found" "ok"
  else
    check "Daily Memory Distillation cron NOT found" "fail"
  fi
  if echo "$CRON_LIST" | grep -qi "synth"; then
    check "Weekly Synthesis cron found" "ok"
  else
    check "Weekly Synthesis cron NOT found" "fail"
  fi
  # Check for problematic model overrides (models that don't exist)
  CRON_JSON=$(openclaw cron list --json 2>/dev/null || echo "")
  if [ -n "$CRON_JSON" ]; then
    # Check distillation/weekly prompts are not empty
    if command -v python3 &>/dev/null; then
      DISTILL_MSG=$(echo "$CRON_JSON" | python3 -c "
import sys, json
try:
  data = json.load(sys.stdin)
  jobs = data.get('jobs', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
  for c in jobs:
    n = (c.get('name') or '').lower()
    if 'distill' in n:
      payload = c.get('payload') or {}
      msg = c.get('message') or payload.get('message') or ''
      print(msg.strip())
      break
except: pass
" 2>/dev/null || echo "")
      WEEKLY_MSG=$(echo "$CRON_JSON" | python3 -c "
import sys, json
try:
  data = json.load(sys.stdin)
  jobs = data.get('jobs', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
  for c in jobs:
    n = (c.get('name') or '').lower()
    if 'synth' in n:
      payload = c.get('payload') or {}
      msg = c.get('message') or payload.get('message') or ''
      print(msg.strip())
      break
except: pass
" 2>/dev/null || echo "")
      if [ -n "$DISTILL_MSG" ]; then
        check "Distillation cron prompt is set" "ok"
      else
        check "Distillation cron prompt is empty (distillation will no-op)" "warn"
      fi
      if [ -n "$WEEKLY_MSG" ]; then
        check "Weekly synthesis cron prompt is set" "ok"
      else
        check "Weekly synthesis cron prompt is empty (synthesis will no-op)" "warn"
      fi
    fi

    BAD_MODELS=$(echo "$CRON_JSON" | grep -o '"model":\s*"[^"]*"' | grep -iE '"(anthropic/default|default)"' || true)
    if [ -n "$BAD_MODELS" ]; then
      check "Cron jobs have invalid model overrides (e.g. 'default' is not a real model)" "warn"
    else
      check "No invalid model overrides in crons" "ok"
    fi
    # Check cron timeouts are sufficient
    if command -v python3 &>/dev/null; then
      DISTILL_TIMEOUT=$(echo "$CRON_JSON" | python3 -c "
import sys, json
try:
  data = json.load(sys.stdin)
  if isinstance(data, list):
    for c in data:
      name = c.get('name','')
      if 'distill' in name.lower():
        print(c.get('timeoutSeconds', c.get('timeout_seconds', c.get('timeout', 0))))
        break
except: pass
" 2>/dev/null || echo "")
      SYNTH_TIMEOUT=$(echo "$CRON_JSON" | python3 -c "
import sys, json
try:
  data = json.load(sys.stdin)
  if isinstance(data, list):
    for c in data:
      name = c.get('name','')
      if 'synth' in name.lower():
        print(c.get('timeoutSeconds', c.get('timeout_seconds', c.get('timeout', 0))))
        break
except: pass
" 2>/dev/null || echo "")
      if [ -n "$DISTILL_TIMEOUT" ] && [ "$DISTILL_TIMEOUT" -gt 0 ] 2>/dev/null; then
        if [ "$DISTILL_TIMEOUT" -lt 300 ]; then
          check "Distillation cron timeout is ${DISTILL_TIMEOUT}s — recommended minimum is 300s (set to 600s for best results)" "warn"
        else
          check "Distillation cron timeout: ${DISTILL_TIMEOUT}s (ok)" "ok"
        fi
      fi
      if [ -n "$SYNTH_TIMEOUT" ] && [ "$SYNTH_TIMEOUT" -gt 0 ] 2>/dev/null; then
        if [ "$SYNTH_TIMEOUT" -lt 300 ]; then
          check "Weekly synthesis cron timeout is ${SYNTH_TIMEOUT}s — recommended minimum is 300s for distillation, 600s for synthesis" "warn"
        else
          check "Weekly synthesis cron timeout: ${SYNTH_TIMEOUT}s (ok)" "ok"
        fi
      fi
    fi
  fi
else
  check "openclaw CLI not found — cannot verify cron jobs" "fail"
fi
echo ""

# --- Principles ---
echo "📜 Principles:"
if [ -f "$WORKSPACE/MEMORY.md" ]; then
  P_COUNT=$(grep -c "^### P[0-9]" "$WORKSPACE/MEMORY.md" 2>/dev/null || true)
  P_COUNT=$(printf '%s' "$P_COUNT" | tr -dc '0-9')
  P_COUNT=${P_COUNT:-0}
  if [ "$P_COUNT" -ge 7 ]; then
    check "$P_COUNT principles found in MEMORY.md" "ok"
  elif [ "$P_COUNT" -ge 1 ]; then
    check "Only $P_COUNT principles found (expected 7+)" "warn"
  else
    check "No principles found in MEMORY.md" "fail"
  fi
  # Context budget: check MEMORY.md size
  MEM_SIZE=$(wc -c < "$WORKSPACE/MEMORY.md" 2>/dev/null | tr -d ' ')
  MEM_KB=$(( MEM_SIZE / 1024 ))
  if [ "$MEM_SIZE" -le 5120 ]; then
    check "MEMORY.md size: ${MEM_KB}KB (within 5KB target)" "ok"
  elif [ "$MEM_SIZE" -le 8192 ]; then
    LESSONS_FILE="$WORKSPACE/memory/lessons.md"
    if [ -f "$LESSONS_FILE" ] && [ "$(wc -l < "$LESSONS_FILE" 2>/dev/null)" -gt 5 ]; then
      check "MEMORY.md size: ${MEM_KB}KB (lessons already in memory/lessons.md — size is ok)" "ok"
    else
      check "MEMORY.md size: ${MEM_KB}KB — consider moving lessons to memory/lessons.md" "warn"
    fi
  else
    check "MEMORY.md size: ${MEM_KB}KB — too large, will slow every session boot" "fail"
  fi
else
  check "MEMORY.md not found" "fail"
fi
echo ""

# --- Gitignore ---
echo "🔒 Security:"
if [ -f "$WORKSPACE/.gitignore" ]; then
  if grep -q "^\.vault/" "$WORKSPACE/.gitignore" 2>/dev/null; then
    check ".vault/ is gitignored" "ok"
  else
    check ".vault/ is NOT gitignored" "warn"
  fi
  if grep -q "^\.secrets-map" "$WORKSPACE/.gitignore" 2>/dev/null; then
    check ".secrets-map is gitignored" "ok"
  else
    check ".secrets-map is NOT gitignored" "warn"
  fi
else
  check "No .gitignore found" "warn"
fi
echo ""

# --- Memory Search ---
echo "🔍 Memory Search:"
if command -v openclaw >/dev/null 2>&1; then
  # Check if memory_search is functional by looking for the memory index
  MEM_DB=$(find "$HOME/.openclaw" -name "memory*.sqlite" -o -name "memory*.db" 2>/dev/null | head -1)
  if [ -n "$MEM_DB" ]; then
    DB_SIZE=$(du -k "$MEM_DB" 2>/dev/null | cut -f1)
    check "Memory search index exists (${DB_SIZE}KB)" "ok"
  else
    check "No memory search index (optional — see docs.openclaw.ai/concepts/memory)" "ok"
  fi

  # Check if memory files are being indexed (non-empty memory dir)
  MEM_FILES=$(find "$WORKSPACE/memory" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  if [ "$MEM_FILES" -gt 0 ]; then
    check "$MEM_FILES memory files available for indexing" "ok"
  else
    check "No memory files found in memory/" "warn"
  fi

  # Check MEMORY.md size (should stay small for boot performance)
  if [ -f "$WORKSPACE/MEMORY.md" ]; then
    MEM_SIZE_KB=$(( $(wc -c < "$WORKSPACE/MEMORY.md" 2>/dev/null | tr -d ' ') / 1024 ))
    if [ "$MEM_SIZE_KB" -le 5 ]; then
      check "MEMORY.md is ${MEM_SIZE_KB}KB (target: < 5KB)" "ok"
    elif [ "$MEM_SIZE_KB" -le 8 ]; then
      # Check if lessons are already split out before warning
      LESSONS_FILE="$WORKSPACE/memory/lessons.md"
      if [ -f "$LESSONS_FILE" ] && [ "$(wc -l < "$LESSONS_FILE" 2>/dev/null)" -gt 5 ]; then
        check "MEMORY.md is ${MEM_SIZE_KB}KB (lessons already in memory/lessons.md — size is ok)" "ok"
      else
        check "MEMORY.md is ${MEM_SIZE_KB}KB — consider moving lessons to memory/lessons.md" "warn"
      fi
    else
      check "MEMORY.md is ${MEM_SIZE_KB}KB — too large, will slow every session boot" "fail"
    fi
  fi
else
  check "openclaw not in PATH — cannot verify memory search" "warn"
fi
echo ""

# --- Vault ---
echo "🔐 Vault:"
if [ -f "$WORKSPACE/scripts/vault.sh" ]; then
  check "vault.sh installed" "ok"
  BACKEND=$(bash "$WORKSPACE/scripts/vault.sh" backend 2>/dev/null | head -1 || echo "unknown")
  check "Passphrase backend: $BACKEND" "ok"
else
  check "vault.sh not installed (vault feature not enabled — this is fine if you skipped it)" "warn"
fi
echo ""

# --- Summary ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   ✅ Passed: $PASS"
echo "   ⚠️  Warnings: $WARN"
echo "   ❌ Failed: $FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
  echo "🎉 BMA is installed and ready!"
  echo "   Work normally — the nightly distillation will start organizing your knowledge automatically."
else
  echo "⚠️  Some checks failed. Re-run the installer:"
  echo "   cd $WORKSPACE && bash skills/biomimetic-memory-architecture/scripts/install.sh"
fi

# --- System Compatibility ---
echo ""
echo "🔍 System Compatibility:"
python3 -c "
import json
config_file = '${HOME}/.openclaw/openclaw.json'
try:
    with open(config_file) as f:
        cfg = json.load(f)
    entries = cfg.get('plugins',{}).get('entries',{})
    mw = entries.get('memory-wiki',{})
    am = entries.get('active-memory',{})
    mc = entries.get('memory-core',{})
    bridge = mw.get('config',{}).get('bridge',{})
    dreaming = mc.get('config',{}).get('dreaming',{})
    checks = {
        'plugins.entries.memory-wiki.enabled':                       ('memory-wiki plugin',            mw.get('enabled') == True, 'critical'),
        'plugins.entries.memory-wiki.config.bridge.indexDailyNotes':  ('bridge.indexDailyNotes=true',  bridge.get('indexDailyNotes') == True, 'critical'),
        'plugins.entries.memory-wiki.config.bridge.indexDreamReports':('bridge.indexDreamReports=false',bridge.get('indexDreamReports') == False, 'critical'),
        'plugins.entries.active-memory.enabled':                     ('active-memory plugin',          am.get('enabled') == True, 'critical'),
        'plugins.entries.active-memory.config.persistTranscripts':    ('persistTranscripts=false',     am.get('config',{}).get('persistTranscripts') == False, 'critical'),
        'plugins.entries.memory-core.enabled':                      ('memory-core plugin',            mc.get('enabled') == True, 'critical'),
        'plugins.entries.memory-core.config.dreaming.phases.deep.enabled': ('dreaming.deep.enabled=false',dreaming.get('phases',{}).get('deep',{}).get('enabled') != True, 'critical'),
        'plugins.entries.memory-core.config.dreaming.enabled':        ('dreaming.enabled=true',       dreaming.get('enabled') == True, 'recommended'),
        'plugins.entries.memory-wiki.config.bridge.indexMemoryRoot':  ('bridge.indexMemoryRoot=true',  bridge.get('indexMemoryRoot') == True, 'recommended'),
        'plugins.entries.memory-wiki.config.bridge.followMemoryEvents':('bridge.followMemoryEvents=false',bridge.get('followMemoryEvents') == False, 'recommended'),
    }
    passed = sum(1 for _, ok, _ in checks.values() if ok)
    total = len(checks)
    issues = [(path, desc, sev) for path, (desc, ok, sev) in checks.items() if not ok]
    print(f'   {passed}/{total} checks passed')
    if not issues:
        print('   ✅ All BMA system requirements met.')
    else:
        print()
        critical_paths = [p for p,_,s in issues if s == 'critical']
        for path, desc, sev in issues:
            mark = '❌' if sev == 'critical' else '⚠️'
            print(f'   {mark} {sev}: {desc}')
        print()
        if critical_paths:
            print('   To auto-fix critical issues:')
            for path in critical_paths:
                val_map = {
                    'plugins.entries.memory-wiki.enabled': True,
                    'plugins.entries.memory-wiki.config.bridge.indexDailyNotes': True,
                    'plugins.entries.memory-wiki.config.bridge.indexDreamReports': False,
                    'plugins.entries.active-memory.enabled': True,
                    'plugins.entries.active-memory.config.persistTranscripts': False,
                    'plugins.entries.memory-core.enabled': True,
                    'plugins.entries.memory-core.config.dreaming.phases.deep.enabled': False,
                }
                val = val_map.get(path, True)
                print(f'   gateway config.patch {json.dumps({path: val})}')
            print()
            print('   After fixing, re-run install.sh or verify.sh.')
except Exception as e:
    print(f'   ⚠️  Could not check: {e}')
    print(f'   💡 See BMA README > System Compatibility.')
" 2>/dev/null || echo "   ⚠️  python3 unavailable; skipping"

# --- BMA additions ---
echo ""
echo "🧬 BMA additions:"
if [ -d "$WORKSPACE/memory-archive/reports" ]; then check "memory-archive/reports/ exists" "ok"; else check "memory-archive/reports/ missing" "warn"; fi
if [ -f "$WORKSPACE/skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py" ]; then
  python3 "$WORKSPACE/skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py" --workspace "$WORKSPACE" --older-than-days 30 --limit 1 >/tmp/bma-verify-audit.out 2>/tmp/bma-verify-audit.err && check "BMA retention audit runs" "ok" || check "BMA retention audit failed" "fail"
else
  check "BMA retention audit script missing" "fail"
fi
if [ -f "$WORKSPACE/skills/biomimetic-memory-architecture/scripts/lesson_imprint.py" ]; then
  python3 "$WORKSPACE/skills/biomimetic-memory-architecture/scripts/lesson_imprint.py" validate >/tmp/bma-lesson-validate.out 2>/tmp/bma-lesson-validate.err && check "BMA Lesson-Imprint validates" "ok" || check "BMA Lesson-Imprint validation failed" "warn"
else
  check "BMA Lesson-Imprint script missing" "fail"
fi
