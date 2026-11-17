#!/bin/bash
# Scope check before review: lists every changed path in a worktree (committed since the base,
# staged, unstaged and untracked) that the brief's file map does not allow. Run it on the
# executor's work BEFORE spending a review on it.
# Usage: scope-check.sh <worktree> <base-sha> <allowed> [allowed ...]
#   <allowed> is a path or a bash glob relative to the worktree root ('packages/a/src/*' also
#   matches deeper files, since * matches '/'); a trailing '/' allows a whole directory.
# Ignored: .agent-logs/*.log (executor logs). Renames list both paths.
# Exit: 0 every change is inside the map; 1 out-of-map paths (printed, one per line); 2 usage or git error.
if [ "$#" -lt 3 ]; then
  echo "scope-check.sh: usage: scope-check.sh <worktree> <base-sha> <allowed> [allowed ...]" >&2
  exit 2
fi
set -o pipefail
W=$1; BASE=$2; shift 2
if ! git -C "$W" rev-parse --verify --quiet "$BASE^{commit}" >/dev/null; then
  echo "scope-check.sh: '$BASE' is not a commit in $W" >&2
  exit 2
fi

# Content, not the worktree's index: a throwaway index is loaded from BASE and every working-tree
# file is re-hashed into it, so index flags (assume-unchanged, skip-worktree), cached stat data and
# fsmonitor cannot hide an edit. Renames are listed as both paths, so moving a file OUT of the map is
# caught. Git-ignored new files are not listed: they cannot enter a commit, and an edit to .gitignore
# that would hide files is itself a change outside the map. NUL-delimited, so any file name works.
G=(git -C "$W" -c diff.renames=false -c core.quotePath=false -c core.fsmonitor=false -c core.untrackedCache=false)
tmp=$(mktemp -d) || exit 2
trap 'rm -f "$tmp/index" "$tmp/index.lock" "$tmp/list"; rmdir "$tmp" 2>/dev/null' EXIT
export GIT_INDEX_FILE="$tmp/index"
if ! "${G[@]}" read-tree "$BASE" || ! "${G[@]}" add -A -- . \
  || ! "${G[@]}" diff --cached --no-renames --name-only -z "$BASE" -- > "$tmp/list"; then
  echo "scope-check.sh: git failed in $W" >&2
  exit 2
fi
unset GIT_INDEX_FILE
list="$tmp/list"

bad=0
seen=$'\n'
while IFS= read -r -d '' f; do
  [ -z "$f" ] && continue
  case "$seen" in *$'\n'"$f"$'\n'*) continue ;; esac
  seen="$seen$f"$'\n'
  case "$f" in .agent-logs/*.log) continue ;; esac
  ok=0
  for pat in "$@"; do
    case "$pat" in
      */) case "$f" in "$pat"*) ok=1 ;; esac ;;
      *) [[ "$f" == $pat ]] && ok=1 ;;
    esac
    [ "$ok" = 1 ] && break
  done
  if [ "$ok" = 0 ]; then
    echo "$f"
    bad=1
  fi
done < "$list"
exit "$bad"
