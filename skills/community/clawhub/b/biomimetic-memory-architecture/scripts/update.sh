#!/bin/bash
# BMA — Non-destructive update script.
# Derived from OpenCortex (MIT License). Namespace and naming adapted for BMA.
# Updates BMA cron messages, ensures directories/state, and validates the install.
# Safe to run multiple times; never overwrites user-customized files.
set -euo pipefail

BMA_VERSION="0.1.7"
DRY_RUN=false
for arg in "$@"; do [ "$arg" = "--dry-run" ] && DRY_RUN=true; done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${CLAWD_WORKSPACE:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
FLAGS_FILE="$WORKSPACE/.bma-flags"
VERSION_FILE="$WORKSPACE/.bma-version"
DAILY_MSG="Daily memory maintenance. Read skills/biomimetic-memory-architecture/references/daily-distillation.md for full instructions and follow them. Workspace: $WORKSPACE"
WEEKLY_MSG="Weekly synthesis. Read skills/biomimetic-memory-architecture/references/weekly-synthesis.md for full instructions and follow them. Workspace: $WORKSPACE"
UPDATED=0
SKIPPED=0

set_feature_flag() {
  local key="$1" value="$2"
  if [ "$DRY_RUN" = "true" ]; then
    echo "   [DRY RUN] Would set $key=$value in $FLAGS_FILE"
    return 0
  fi
  touch "$FLAGS_FILE"
  if grep -q "^${key}=" "$FLAGS_FILE" 2>/dev/null; then
    sed -i.bak "s/^${key}=.*/${key}=${value}/" "$FLAGS_FILE" && rm -f "$FLAGS_FILE.bak"
  else
    echo "${key}=${value}" >> "$FLAGS_FILE"
  fi
  chmod 600 "$FLAGS_FILE" 2>/dev/null || true
}

ensure_dirs() {
  if [ "$DRY_RUN" = "true" ]; then
    echo "   [DRY RUN] Would ensure BMA directories"
    return 0
  fi
  mkdir -p \
    "$WORKSPACE/memory/projects" \
    "$WORKSPACE/memory/runbooks" \
    "$WORKSPACE/memory/contacts" \
    "$WORKSPACE/memory/workflows" \
    "$WORKSPACE/memory/archive" \
    "$WORKSPACE/memory/lesson-imprint" \
    "$WORKSPACE/memory-archive/reports"
}

ensure_lesson_imprint() {
  if [ ! -f "$SCRIPT_DIR/lesson_imprint.py" ]; then
    echo "   ⏭️  lesson_imprint.py not found; skipping (run install.sh for full setup)"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi
  if [ "$DRY_RUN" = "true" ]; then
    echo "   [DRY RUN] Would initialize and promote Lesson-Imprint"
    UPDATED=$((UPDATED + 1))
    return 0
  fi
  if python3 "$SCRIPT_DIR/lesson_imprint.py" init >/dev/null 2>&1 && \
     python3 "$SCRIPT_DIR/lesson_imprint.py" promote >/dev/null 2>&1; then
    UPDATED=$((UPDATED + 1))
  else
    echo "   ⚠️  Lesson-Imprint init/promote failed; skipping"
    SKIPPED=$((SKIPPED + 1))
  fi
}

cron_id_by_name() {
  local name="$1"
  python3 - "$name" <<'PY'
import json, subprocess, sys
name = sys.argv[1].lower()
try:
    out = subprocess.check_output(['openclaw', 'cron', 'list', '--json'], text=True)
    data = json.loads(out)
except Exception:
    sys.exit(0)
jobs = data.get('jobs', data if isinstance(data, list) else [])
for job in jobs:
    if name in str(job.get('name', '')).lower():
        print(job.get('id') or job.get('jobId') or job.get('_id') or '')
        break
PY
}

update_cron_message() {
  local name="$1" message="$2" timeout="$3"
  if ! command -v openclaw >/dev/null 2>&1; then
    echo "   ⚠️  openclaw CLI unavailable; skipping $name cron"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi
  local id
  id=$(cron_id_by_name "$name")
  if [ -z "$id" ]; then
    echo "   ⏭️  $name cron not found; run install.sh to create it"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi
  if [ "$DRY_RUN" = "true" ]; then
    echo "   [DRY RUN] Would update $name cron ($id)"
    UPDATED=$((UPDATED + 1))
    return 0
  fi
  if openclaw cron update "$id" --message "$message" --timeout-seconds "$timeout" >/dev/null 2>&1; then
    echo "   ✅ Updated $name cron"
  elif openclaw cron edit "$id" --message "$message" --timeout-seconds "$timeout" >/dev/null 2>&1; then
    echo "   ✅ Updated $name cron"
  else
    echo "   ⚠️  Could not update $name cron automatically"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi
  UPDATED=$((UPDATED + 1))
}

ensure_gitignore() {
  if [ "$DRY_RUN" = "true" ]; then
    echo "   [DRY RUN] Would ensure .vault/ and .secrets-map are gitignored"
    return 0
  fi
  touch "$WORKSPACE/.gitignore"
  grep -qxF ".vault/" "$WORKSPACE/.gitignore" 2>/dev/null || echo ".vault/" >> "$WORKSPACE/.gitignore"
  grep -qxF ".secrets-map" "$WORKSPACE/.gitignore" 2>/dev/null || echo ".secrets-map" >> "$WORKSPACE/.gitignore"
}

echo "🔄 BMA Update v$BMA_VERSION"
echo "   Workspace: $WORKSPACE"
echo "   Script:    $SCRIPT_DIR"
[ "$DRY_RUN" = "true" ] && echo "   Mode:      dry-run"
echo ""

echo "📁 Ensuring directories and state..."
ensure_dirs
UPDATED=$((UPDATED + 1))
ensure_gitignore
UPDATED=$((UPDATED + 1))
ensure_lesson_imprint

echo ""
echo "⏰ Updating cron messages..."
update_cron_message "Daily Memory Distillation" "$DAILY_MSG" 600
update_cron_message "Weekly Synthesis" "$WEEKLY_MSG" 600

echo ""
echo "🏷️  Setting feature flags..."
if [ -f "$WORKSPACE/memory/VOICE.md" ]; then
  set_feature_flag VOICE_PROFILE 1
else
  set_feature_flag VOICE_PROFILE 0
fi

if [ -f "$FLAGS_FILE" ] && grep -q '^INFRA_COLLECT=' "$FLAGS_FILE" 2>/dev/null; then
  : # preserve existing value
elif [ "${BMA_INFRA_COLLECT:-}" = "1" ]; then
  set_feature_flag INFRA_COLLECT 1
else
  set_feature_flag INFRA_COLLECT 0
fi

echo ""
echo "🧪 Running validation..."
if [ "$DRY_RUN" = "true" ]; then
  echo "   [DRY RUN] Would run verify.sh"
else
  bash "$SCRIPT_DIR/verify.sh" || true
  echo "$BMA_VERSION" > "$VERSION_FILE"
fi

echo ""
echo "✅ BMA update complete. updated=$UPDATED skipped=$SKIPPED"
