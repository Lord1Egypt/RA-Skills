#!/usr/bin/env bash
set -euo pipefail

# Commit ONLY Markdown changes in a git repo.
#
# Usage:
#   commit_md_changes.sh [commit-message]
#
# Environment:
#   BRAINGIT_REPO     Repo path (default: current directory)
#   BRAINGIT_PATTERN  Glob pattern for files to include (default: *.md)
#   BRAINGIT_DRY_RUN  If set to 1, do not commit; print what would happen

REPO_DIR="${BRAINGIT_REPO:-$(pwd)}"
PATTERN="${BRAINGIT_PATTERN:-*.md}"
MSG="${1:-md: snapshot}"
DRY_RUN="${BRAINGIT_DRY_RUN:-0}"

cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "braingit: not a git repo: $REPO_DIR" >&2
  exit 2
fi

# Find modified/added/deleted paths.
CHANGED=()
while IFS= read -r -d '' entry; do
  xy="${entry:0:2}"
  path="${entry:3}"

  # Renames/copies are followed by a second NUL token with the new path.
  if [[ "$xy" == R* || "$xy" == C* ]]; then
    IFS= read -r -d '' newpath || true
    path="$newpath"
  fi

  case "$path" in
    $PATTERN) CHANGED+=("$path") ;;
    *) ;;
  esac

done < <(git status --porcelain -z)

if (( ${#CHANGED[@]} == 0 )); then
  exit 0
fi

if [[ "$DRY_RUN" == "1" ]]; then
  echo "braingit: would stage+commit ${#CHANGED[@]} file(s):"
  printf ' - %s\n' "${CHANGED[@]}"
  echo "braingit: message: $MSG"
  exit 0
fi

# Stage only included files
for p in "${CHANGED[@]}"; do
  git add -- "$p" || true
done

# Commit if anything staged
if git diff --cached --quiet; then
  exit 0
fi

git commit -m "$MSG" >/dev/null
