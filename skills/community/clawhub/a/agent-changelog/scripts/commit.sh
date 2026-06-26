#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d .git ]; then
  echo "⚠️ Versioning not initialized"
  echo "Run \`/agent-changelog setup\` to get started."
  exit 1
fi

MANUAL=false
MESSAGE=""
SUMMARY=""
for arg in "$@"; do
  case "$arg" in
    --manual) MANUAL=true ;;
    --summary) shift_next=true ;;
    *)
      if [ "${shift_next:-false}" = true ]; then
        SUMMARY="$arg"
        shift_next=false
      elif [ -z "$MESSAGE" ]; then
        MESSAGE="$arg"
      fi
      ;;
  esac
done

PENDING="$WORKSPACE/pending_commits.jsonl"

# ─── Resolve tracked files ────────────────────────────────────────────
TRACKED=()
while IFS= read -r item; do
  TRACKED+=("$item")
done < <(jq -r '.tracked[]?' "$WORKSPACE/.agent-changelog.json" 2>/dev/null)

# ─── Stage any unstaged changes to tracked files ─────────────────────
for f in "${TRACKED[@]+"${TRACKED[@]}"}"; do
  git add "$f" 2>/dev/null || true
done

# ─── Nothing staged at all → nothing to do ───────────────────────────
if git diff --cached --quiet 2>/dev/null; then
  [ -f "$PENDING" ] && > "$PENDING"
  echo "✓ No changes to commit"
  exit 0
fi

# ─── Build commit message ─────────────────────────────────────────────
STAGED_FILES=$(git diff --cached --name-only | tr '\n' ' ' | sed 's/ $//')
USERS=""
COUNT=0
HAS_PENDING=false
CHANGELOG=""

if [ -f "$PENDING" ] && [ -s "$PENDING" ]; then
  HAS_PENDING=true
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    COUNT=$((COUNT + 1))

    if command -v jq &>/dev/null; then
      user=$(echo "$line" | jq -r '.user // "unknown"' 2>/dev/null || echo "unknown")
      ts=$(echo "$line" | jq -r '.ts // 0' 2>/dev/null || echo "0")
      channel=$(echo "$line" | jq -r '.channel // "unknown"' 2>/dev/null || echo "unknown")
      files=$(echo "$line" | jq -r '(.files // []) | join(", ")' 2>/dev/null || echo "")
      action=$(echo "$line" | jq -r '.action // ""' 2>/dev/null || echo "")
      action_target=$(echo "$line" | jq -r '.target // ""' 2>/dev/null || echo "")
      action_file=$(echo "$line" | jq -r '.file // ""' 2>/dev/null || echo "")
      action_from=$(echo "$line" | jq -r '.from // ""' 2>/dev/null || echo "")
      action_reason=$(echo "$line" | jq -r '.reason // ""' 2>/dev/null || echo "")
    else
      user=$(echo "$line" | grep -o '"user":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
      ts="0"; channel="unknown"; files=""; action=""; action_target=""; action_file=""; action_from=""; action_reason=""
    fi

    # Format timestamp as readable date
    if [ "$ts" != "0" ] && command -v date &>/dev/null; then
      ts_sec=$((ts / 1000))
      readable=$(date -r "$ts_sec" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$ts")
    else
      readable="$ts"
    fi

    # Accumulate unique users
    if [ -n "$user" ] && [ "$user" != "unknown" ]; then
      if [ -z "$USERS" ]; then
        USERS="$user"
      elif ! echo "$USERS" | grep -qF "$user"; then
        USERS="$USERS, $user"
      fi
    fi

    # Build per-turn changelog line
    if [ "$action" = "rollback" ]; then
      CHANGELOG="${CHANGELOG}  [$readable] $user\n"
      CHANGELOG="${CHANGELOG}  action: rollback → $action_target\n"
      [ -n "$action_reason" ] && CHANGELOG="${CHANGELOG}  reason: $action_reason\n"
    elif [ "$action" = "restore" ]; then
      CHANGELOG="${CHANGELOG}  [$readable] $user\n"
      CHANGELOG="${CHANGELOG}  action: restore $action_file from $action_from\n"
      [ -n "$action_reason" ] && CHANGELOG="${CHANGELOG}  reason: $action_reason\n"
    elif [ "$action" = "pl-pull" ]; then
      CHANGELOG="${CHANGELOG}  [$readable] $user\n"
      CHANGELOG="${CHANGELOG}  action: pl-pull → v$action_target\n"
      [ -n "$action_from" ] && CHANGELOG="${CHANGELOG}  label: $action_from\n"
      [ -n "$action_reason" ] && CHANGELOG="${CHANGELOG}  reason: $action_reason\n"
    else
      CHANGELOG="${CHANGELOG}  [$readable] $user ($channel): $files\n"
    fi
  done < "$PENDING"
fi

# ─── Determine prefix ─────────────────────────────────────────────────
CTX="$WORKSPACE/.version-context"

if [ "$MANUAL" = true ]; then
  PREFIX="Manual commit"
  # For manual commits, prefer identity from version-context (set by capture hook)
  if [ -z "$USERS" ] || [ "$USERS" = "unknown" ]; then
    if [ -f "$CTX" ] && command -v jq &>/dev/null; then
      CTX_USER=$(jq -r '.user // ""' "$CTX" 2>/dev/null || true)
      [ -n "$CTX_USER" ] && [ "$CTX_USER" != "unknown" ] && USERS="$CTX_USER"
    fi
  fi
  if [ -z "$USERS" ] || [ "$USERS" = "unknown" ]; then USERS="skill invocation"; fi
elif [ "$HAS_PENDING" = false ] || [ "$COUNT" -eq 0 ]; then
  PREFIX="Auto-commit (cli)"
  USERS="cli"
else
  PREFIX="Auto-commit"
fi

if [ -z "$USERS" ]; then USERS="unknown"; fi

# ─── Assemble full message ────────────────────────────────────────────
if [ -n "$MESSAGE" ]; then
  SUBJECT="$MESSAGE"
else
  SUBJECT="${PREFIX}: $STAGED_FILES"
fi

MSG="$SUBJECT

Triggered by: ${USERS}
Turns: ${COUNT}"

[ -n "$SUMMARY" ] && MSG="${MSG}
Summary: ${SUMMARY}"

if [ -n "$CHANGELOG" ]; then
  MSG="${MSG}

--- Change log ---
$(printf "%b" "$CHANGELOG")"
fi

git commit -m "$MSG"
SHORT_HASH=$(git rev-parse --short HEAD)

[ -f "$PENDING" ] && > "$PENDING"

echo "✅ **Committed** \`$SHORT_HASH\`"
echo "$SUBJECT"
echo "_by ${USERS}_"
[ -n "$SUMMARY" ] && echo "$SUMMARY"

# ─── Sync provider ────────────────────────────────────────────────────
WORKSPACE_CFG="$WORKSPACE/.agent-changelog.json"
SYNC_PROVIDER="local"
if [ -f "$WORKSPACE_CFG" ] && command -v jq &>/dev/null; then
  _pl_enabled=$(jq -r '.promptlayer.enabled // false' "$WORKSPACE_CFG" 2>/dev/null || echo "false")
  _pl_collection=$(jq -r '.promptlayer.collectionId // ""' "$WORKSPACE_CFG" 2>/dev/null || echo "")
  _gh_enabled=$(jq -r '.github.enabled // false' "$WORKSPACE_CFG" 2>/dev/null || echo "false")
  if [ "$_pl_enabled" = "true" ] && [ -n "$_pl_collection" ]; then
    SYNC_PROVIDER="promptlayer"
  elif [ "$_gh_enabled" = "true" ]; then
    SYNC_PROVIDER="github"
  fi
fi

if [ "$SYNC_PROVIDER" = "github" ]; then
  GIT_REMOTE=$(git remote 2>/dev/null | head -1)
  if git push "$GIT_REMOTE" 2>/dev/null; then
    echo "↑ Pushed to \`$GIT_REMOTE\`"
  else
    echo "⚠️ Push to \`$GIT_REMOTE\` failed"
  fi
elif [ "$SYNC_PROVIDER" = "promptlayer" ]; then
  if command -v node &>/dev/null; then
    node "$SCRIPT_DIR/pl-push.js" --message "$SUBJECT" 2>&1 || true
  fi
fi
