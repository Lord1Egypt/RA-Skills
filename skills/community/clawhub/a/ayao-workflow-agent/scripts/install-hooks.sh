#!/bin/bash
# install-hooks.sh — Install git hooks for agent swarm event-driven automation
# Usage: install-hooks.sh <project_dir>
#
# Installs a post-commit hook that:
# 1. Detects commits during active swarm operations
# 2. Runs tsc --noEmit compile check (reverts on failure)
# 3. Auto-pushes the commit
# 4. Writes a signal for the orchestrator
# 5. Wakes OpenClaw via webhook

set -euo pipefail

PROJECT_DIR="${1:?Usage: install-hooks.sh <project_dir>}"
HOOKS_DIR="$PROJECT_DIR/.git/hooks"

if [[ ! -d "$PROJECT_DIR/.git" ]]; then
  echo "❌ Not a git repo: $PROJECT_DIR"
  exit 1
fi

mkdir -p "$HOOKS_DIR"

# Save project dir for other scripts
echo "$PROJECT_DIR" > ~/.openclaw/workspace/swarm/project-dir

# Write the post-commit hook
cat > "$HOOKS_DIR/post-commit" << 'HOOK'
#!/bin/bash
# Agent Swarm post-commit hook — event-driven automation + compile gate
# Installed by: install-hooks.sh

TASKS_FILE="$HOME/.openclaw/workspace/swarm/active-tasks.json"
SIGNAL_FILE="/tmp/agent-swarm-signals.jsonl"

# Only act if swarm is active
[[ ! -f "$TASKS_FILE" ]] && exit 0

# Check if there are any running tasks
if ! grep -q '"running"\|"reviewing"' "$TASKS_FILE" 2>/dev/null; then
  exit 0
fi

COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=%s)
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | tr '\n' ',' | sed 's/,$//')
TS=$(date +%s)

# ═══════════════════════════════════════════
# Compile Gate: tsc --noEmit
# If compilation fails, revert the commit and notify.
# ═══════════════════════════════════════════
TSC_FAILED=false
TSC_OUTPUT=""

# Detect which subdirectory was changed and run tsc there
for subdir in polygo-daemon polygo-web-admin; do
  if echo "$CHANGED_FILES" | grep -q "^$subdir/" && [[ -f "$subdir/tsconfig.json" ]]; then
    TSC_OUTPUT=$(cd "$subdir" && npx tsc --noEmit 2>&1) || {
      # Filter out pre-existing errors (like @types/pg missing) vs new errors
      # Count errors in changed files only
      NEW_ERRORS=""
      for f in $(git diff-tree --no-commit-id --name-only -r HEAD | grep "^$subdir/"); do
        REL_FILE="${f#$subdir/}"
        FILE_ERRORS=$(echo "$TSC_OUTPUT" | grep "^$REL_FILE" || true)
        if [[ -n "$FILE_ERRORS" ]]; then
          NEW_ERRORS="${NEW_ERRORS}${FILE_ERRORS}\n"
        fi
      done

      if [[ -n "$NEW_ERRORS" ]]; then
        TSC_FAILED=true
        # Revert the commit (keep changes in working tree for agent to fix)
        git reset --soft HEAD~1

        # Write failure signal
        echo "{\"event\":\"compile_fail\",\"hash\":\"$COMMIT_HASH\",\"message\":\"$COMMIT_MSG\",\"errors\":\"tsc failed in $subdir\",\"time\":$TS}" >> "$SIGNAL_FILE"

        # Notify
        NOTIFY_TARGET=$(cat "$HOME/.openclaw/workspace/swarm/notify-target" 2>/dev/null)
        if [[ -n "$NOTIFY_TARGET" ]]; then
          ESCAPED_ERRORS=$(echo -e "$NEW_ERRORS" | head -5 | tr '\n' ' ')
          openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
            -m "❌ 编译失败，commit 已回退: $COMMIT_HASH — $ESCAPED_ERRORS" --silent 2>/dev/null &
        fi

        echo "❌ tsc --noEmit failed for changed files in $subdir. Commit reverted (soft)."
        echo -e "$NEW_ERRORS"
        exit 0  # exit 0 so git doesn't show confusing errors
      fi
    }
  fi
done

if $TSC_FAILED; then
  exit 0
fi

# ═══════════════════════════════════════════
# ESLint Gate: only for polygo-web-admin
# Run eslint on changed .ts/.tsx files only (fast, targeted)
# ═══════════════════════════════════════════
ESLINT_FAILED=false

CHANGED_WEB_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD \
  | grep "^polygo-web-admin/.*\.[tj]sx\?$" \
  | grep -v "node_modules\|\.next\|out\|build" || true)

if [[ -n "$CHANGED_WEB_FILES" ]] && [[ -f "polygo-web-admin/package.json" ]]; then
  # Build file list relative to polygo-web-admin/
  REL_FILES=$(echo "$CHANGED_WEB_FILES" | sed 's|^polygo-web-admin/||' | tr '\n' ' ')

  ESLINT_OUTPUT=$(cd polygo-web-admin && npx eslint --max-warnings=0 $REL_FILES 2>&1) || {
    ESLINT_FAILED=true
    # Revert the commit (soft — keep changes for agent to fix)
    git reset --soft HEAD~1

    # Write failure signal
    echo "{\"event\":\"eslint_fail\",\"hash\":\"$COMMIT_HASH\",\"message\":\"$COMMIT_MSG\",\"time\":$TS}" >> "$SIGNAL_FILE"

    # Notify
    NOTIFY_TARGET=$(cat "$HOME/.openclaw/workspace/swarm/notify-target" 2>/dev/null)
    if [[ -n "$NOTIFY_TARGET" ]]; then
      ESCAPED=$(echo "$ESLINT_OUTPUT" | head -5 | tr '\n' ' ')
      openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
        -m "❌ ESLint 失败，commit 已回退: $COMMIT_HASH — $ESCAPED" --silent 2>/dev/null &
    fi

    echo "❌ ESLint failed. Commit reverted (soft)."
    echo "$ESLINT_OUTPUT"
    exit 0
  }
fi

if $ESLINT_FAILED; then
  exit 0
fi

# ═══════════════════════════════════════════
# All gates passed — proceed normally
# ═══════════════════════════════════════════

# Write signal
echo "{\"event\":\"commit\",\"hash\":\"$COMMIT_HASH\",\"message\":\"$COMMIT_MSG\",\"files\":\"$CHANGED_FILES\",\"time\":$TS}" >> "$SIGNAL_FILE"

# Auto-push (background)
git push 2>/dev/null &

# Wake OpenClaw orchestrator via webhook
HOOK_TOKEN=$(cat "$HOME/.openclaw/workspace/swarm/hook-token" 2>/dev/null || echo "")
NOTIFY_TARGET=$(cat "$HOME/.openclaw/workspace/swarm/notify-target" 2>/dev/null || echo "")

if [[ -n "$HOOK_TOKEN" ]]; then
  curl -s -X POST http://127.0.0.1:18789/hooks/wake \
    -H "Authorization: Bearer $HOOK_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"Swarm commit: $COMMIT_HASH — $COMMIT_MSG\",\"mode\":\"now\"}" >/dev/null 2>&1 &
fi

# Backup: direct Telegram notification
if [[ -n "$NOTIFY_TARGET" ]]; then
  openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
    -m "✅ Commit: $COMMIT_HASH — $COMMIT_MSG" --silent 2>/dev/null &
fi

exit 0
HOOK

chmod +x "$HOOKS_DIR/post-commit"
echo "✅ post-commit hook installed at $HOOKS_DIR/post-commit (with compile gate)"
