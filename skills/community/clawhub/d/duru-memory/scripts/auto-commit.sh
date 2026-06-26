#!/usr/bin/env bash
set -euo pipefail

# Optional git safety-net commit for memory files
# Usage: auto-commit.sh [workspace]

WORKSPACE="${1:-$(pwd)}"
cd "$WORKSPACE"

if ! command -v git >/dev/null 2>&1; then
  echo "git not found; skip"
  exit 0
fi

if [[ ! -d .git ]]; then
  echo "not a git repo; skip"
  exit 0
fi

if [[ -z "$(git status --porcelain memory/ 2>/dev/null || true)" ]]; then
  echo "no memory changes"
  exit 0
fi

TS="$(date '+%Y-%m-%d %H:%M:%S %z')"
CNT_NEW="$(git status --porcelain memory/ | grep -E '^\?\?' | wc -l | tr -d ' ')"
CNT_MOD="$(git status --porcelain memory/ | grep -E '^( M|M |MM|A | D|D )' | wc -l | tr -d ' ')"

msg="[memory] checkpoint ${TS} (new:${CNT_NEW}, changed:${CNT_MOD})"

git add memory/
git commit -m "$msg" >/dev/null

echo "committed: $msg"
