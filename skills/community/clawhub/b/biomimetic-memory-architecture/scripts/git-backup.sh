#!/bin/bash
# BMA — Safe auto-commit workspace changes.
# Derived from OpenCortex (MIT License). Namespace renamed OPENCORTEX_* → BMA_*.
#
# Secrets are scrubbed in a temporary copy only. The real workspace files and
# real git index are not modified during scrubbing.
#
# Usage:
#   git-backup.sh          Commit locally only
#   git-backup.sh --push   Commit and push to remote
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${CLAWD_WORKSPACE:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
cd "$WORKSPACE"

git rev-parse --show-toplevel >/dev/null 2>&1 || { echo "❌ Not inside a git repository: $WORKSPACE" >&2; exit 1; }

if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  exit 0
fi

PUSH="${1:-}"
SECRETS_FILE="$WORKSPACE/.secrets-map"

for sensitive in ".vault" ".secrets-map"; do
  if [ -e "$WORKSPACE/$sensitive" ] && ! git check-ignore -q "$sensitive" 2>/dev/null; then
    echo "❌ ABORT: $sensitive is not gitignored. Add it to .gitignore first." >&2
    exit 1
  fi
done

TMPDIR_BASE=$(mktemp -d)
SCRUB_DIR="$TMPDIR_BASE/scrub"
TMPINDEX="$TMPDIR_BASE/git-index"
FILE_LIST="$TMPDIR_BASE/files.txt"
DELETED_LIST="$TMPDIR_BASE/deleted.txt"
mkdir -p "$SCRUB_DIR"
cleanup() { rm -rf "$TMPDIR_BASE"; }
trap cleanup EXIT

{ git ls-files; git ls-files --others --exclude-standard; } | sort -u > "$FILE_LIST"
git diff --name-only --diff-filter=D HEAD 2>/dev/null > "$DELETED_LIST" || touch "$DELETED_LIST"

while IFS= read -r f; do
  [ -f "$WORKSPACE/$f" ] || continue
  mkdir -p "$SCRUB_DIR/$(dirname "$f")"
  cp "$WORKSPACE/$f" "$SCRUB_DIR/$f"
done < "$FILE_LIST"

if [ -f "$SECRETS_FILE" ]; then
  while IFS='|' read -r secret placeholder; do
    case "$secret" in ''|'#'*) continue ;; esac
    secret=$(printf '%s' "$secret" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    placeholder=$(printf '%s' "${placeholder:-{{REDACTED}}}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    [ -n "$secret" ] || continue
    while IFS= read -r -d '' f; do
      file -b --mime-encoding "$f" 2>/dev/null | grep -q "binary" && continue
      if grep -qF "$secret" "$f" 2>/dev/null; then
        BMA_SECRET="$secret" BMA_PLACEHOLDER="$placeholder" perl -0pi -e 'BEGIN { $s=$ENV{BMA_SECRET}; $p=$ENV{BMA_PLACEHOLDER}; } s/\Q$s\E/$p/g' "$f"
      fi
    done < <(BMA_SECRET="$secret" BMA_PLACEHOLDER="$placeholder" find "$SCRUB_DIR" -type f -print0)
  done < "$SECRETS_FILE"

  while IFS='|' read -r secret placeholder; do
    case "$secret" in ''|'#'*) continue ;; esac
    secret=$(printf '%s' "$secret" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    [ -n "$secret" ] || continue
    if grep -rlF "$secret" "$SCRUB_DIR" 2>/dev/null | grep -q .; then
      echo "❌ Secret found in scrubbed copy — aborting. Workspace files are untouched." >&2
      exit 1
    fi
  done < "$SECRETS_FILE"
fi

export GIT_INDEX_FILE="$TMPINDEX"
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  git read-tree HEAD
else
  git read-tree --empty
fi

while IFS= read -r f; do
  [ -f "$SCRUB_DIR/$f" ] || continue
  mode=$(GIT_INDEX_FILE= git ls-files --stage "$f" 2>/dev/null | awk '{print $1; exit}')
  [ -n "$mode" ] || mode="100644"
  blob=$(git hash-object -w "$SCRUB_DIR/$f")
  git update-index --add --cacheinfo "$mode,$blob,$f"
done < "$FILE_LIST"

while IFS= read -r f; do
  [ -n "$f" ] || continue
  git update-index --remove "$f" 2>/dev/null || true
done < "$DELETED_LIST"

TREE=$(git write-tree)
PARENT=$(GIT_INDEX_FILE= git rev-parse --verify HEAD 2>/dev/null || true)
COMMIT_MSG="BMA backup: $(date '+%Y-%m-%d %H:%M')"
if [ -n "$PARENT" ]; then
  COMMIT=$(git commit-tree -p "$PARENT" -m "$COMMIT_MSG" "$TREE")
else
  COMMIT=$(git commit-tree -m "$COMMIT_MSG" "$TREE")
fi
unset GIT_INDEX_FILE

BRANCH=$(GIT_INDEX_FILE= git symbolic-ref --short HEAD 2>/dev/null || true)
if [ -n "$BRANCH" ]; then
  git update-ref "refs/heads/$BRANCH" "$COMMIT"
else
  git update-ref HEAD "$COMMIT"
fi

echo "✅ Committed (workspace files untouched — secrets scrubbed in isolated copy)."
if [ "$PUSH" = "--push" ]; then
  git push --quiet
  echo "✅ Pushed to remote."
else
  echo "   Run with --push to push to remote. Or: git push"
fi
