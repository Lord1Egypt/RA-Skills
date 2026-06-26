#!/usr/bin/env bash
set -euo pipefail

# Session startup helper for duru-memory skill
# Usage: session-start.sh [workspace]
# Note: complements OpenClaw memory-core / active-memory, does not replace them.

WORKSPACE="${1:-$(pwd)}"
MEMORY_DIR="${WORKSPACE}/memory"
CORE_DIR="${MEMORY_DIR}/CORE"
SKILL_DIR="${WORKSPACE}/skills/duru-memory"

printf '=== duru-memory: session start ===\n'
printf 'workspace: %s\n' "$WORKSPACE"
printf 'timestamp: %s\n\n' "$(date '+%Y-%m-%d %H:%M:%S %z')"

mkdir -p "$MEMORY_DIR" "$CORE_DIR" "$MEMORY_DIR/daily" "$MEMORY_DIR/projects" "$MEMORY_DIR/people" "$MEMORY_DIR/concepts" "$MEMORY_DIR/handoff" "$MEMORY_DIR/archive/raw"

required=(
  "${CORE_DIR}/hard-rules.md"
  "${CORE_DIR}/current-state.md"
  "${CORE_DIR}/state-changelog.md"
)

printf '[1/4] CORE files\n'
for f in "${required[@]}"; do
  if [[ -f "$f" ]]; then
    printf '  ✓ %s\n' "${f#$WORKSPACE/}"
  else
    printf '  ! missing: %s\n' "${f#$WORKSPACE/}"
  fi
done

printf '\n[2/4] recent daily logs (2 days)\n'
find "$MEMORY_DIR/daily" -type f -name '*.md' -mtime -2 2>/dev/null | sort -r | head -n 10 | sed "s#^${WORKSPACE}/##" | sed 's/^/  - /' || true

printf '\n[3/4] startup guidance\n'
printf '  - read memory/CORE/hard-rules.md\n'
printf '  - read memory/CORE/current-state.md\n'
printf '  - read last 1-3 files in memory/daily/\n'
printf '  - prefer built-in memory_search for normal assistant recall\n'
printf '  - run scripts/memory-search.sh "<query>" for local debugging or deterministic file-level inspection\n'

printf '\n[4/4] semantic index warmup (daily, incremental)\n'
SEM_SCRIPT="${SKILL_DIR}/scripts/memory-semantic-search.py"
STAMP_FILE="${MEMORY_DIR}/.semantic-warmup-date"
TODAY="$(date '+%Y-%m-%d')"
LAST="$(cat "$STAMP_FILE" 2>/dev/null || true)"
if [[ -x "$SEM_SCRIPT" ]]; then
  if [[ "$LAST" != "$TODAY" ]]; then
    if (cd "$SKILL_DIR" && uv run python "$SEM_SCRIPT" "warmup" "$WORKSPACE" --build-only >/dev/null 2>&1); then
      echo "$TODAY" > "$STAMP_FILE"
      printf '  ✓ warmup done for %s\n' "$TODAY"
    else
      printf '  ! warmup skipped (semantic backend unavailable)\n'
    fi
  else
    printf '  - already warmed today (%s)\n' "$TODAY"
  fi
else
  printf '  - semantic script not found; skip\n'
fi

printf '\nready.\n'
