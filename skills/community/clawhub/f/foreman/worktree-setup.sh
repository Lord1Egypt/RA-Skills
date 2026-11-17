#!/bin/bash
# foreman dispatch helper: create an isolated git worktree for one task and print its absolute path on stdout.
#
# Why a script instead of "remember to run git worktree add": for a long time "one git worktree per task" was an
# invariant written in prose, while the copy-paste dispatch example never showed how to create one or pass --cwd to
# `handoff run`. That cost a real incident: a task sent to one backend switched branches and committed directly in the
# main session's own working directory, and the main session's HEAD went along with it. Nothing was lost that time —
# the work happened to be committed — but that is exactly the risk isolation exists to remove. Earlier dispatches had
# done it right; it just wasn't in the example, so the next person copying the example (including the session writing
# the work order) left it out. This script makes the correct path the path of least resistance.
#
# Usage:
#   WT=$(bash <skill-dir>/worktree-setup.sh <repo-path> <slug> [base-ref])
#   handoff run --backend "$BE" --cwd "$WT" ~/.handoff/tasks/<RUN_ID>.prompt.md
#
# base-ref defaults to main — when several tasks share an integration branch, pass that branch.
# Worktrees go under ${FOREMAN_WORKTREE_ROOT:-~/foreman-worktrees}/<slug>, on branch work/<slug>.
# (Keep that root under your home directory if you use the caged worker: container VMs usually share only ~.)

set -euo pipefail

REPO_PATH="${1:?usage: worktree-setup.sh <repo-path> <slug> [base-ref]}"
SLUG="${2:?usage: worktree-setup.sh <repo-path> <slug> [base-ref]}"
BASE_REF="${3:-main}"

if [[ ! "$SLUG" =~ ^[a-z0-9][a-z0-9-]*[a-z0-9]$ ]]; then
  echo "slug must be lowercase letters, digits and hyphens (not starting or ending with a hyphen): $SLUG" >&2
  exit 1
fi

REPO_PATH="$(cd "$REPO_PATH" && pwd -P)"
WT_ROOT="${FOREMAN_WORKTREE_ROOT:-$HOME/foreman-worktrees}"
mkdir -p "$WT_ROOT"
# Physical path: `git worktree list` reports resolved paths, so a root reached through a symlink
# (e.g. /var → /private/var on macOS) would never match and a clean worktree would be refused instead of reused.
WT_ROOT="$(cd "$WT_ROOT" && pwd -P)"
WT="$WT_ROOT/$SLUG"
BRANCH="work/$SLUG"

# The path already exists — most likely left over from an earlier dispatch with the same slug.
# Reuse it only if git still knows it as a worktree and it is clean; otherwise stop and let a human decide,
# rather than deleting a directory that may hold uncommitted work.
if [[ -d "$WT" ]]; then
  if git -C "$REPO_PATH" worktree list --porcelain | grep -qxF "worktree $WT"; then
    if [[ -z "$(git -C "$WT" status --porcelain 2>/dev/null)" ]]; then
      echo "$WT"   # clean worktree from before — reuse it
      exit 0
    fi
    echo "worktree exists and is not clean — deal with it before redispatching: $WT (git -C \"$WT\" status)" >&2
    exit 1
  fi
  echo "path exists but is not a known worktree (a stray directory?): $WT — clean it up by hand first" >&2
  exit 1
fi

# An existing branch is refused too, never silently reused: it may be the previous round's leftovers,
# and hanging a new task's commits onto an old task's history makes the diff boundary check count the wrong changes.
if git -C "$REPO_PATH" show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "branch already exists, not reusing it (probably left from an earlier round): $BRANCH — delete it or pick another slug" >&2
  exit 1
fi

git -C "$REPO_PATH" worktree add "$WT" -b "$BRANCH" "$BASE_REF" >&2

# Defensive assertion: the new worktree's physical path must not be the caller's own repository.
# `git worktree add` can't normally produce that; this turns "isolated" from an assumption into a checked fact.
if [[ "$(cd "$WT" && pwd -P)" == "$(cd "$REPO_PATH" && pwd -P)" ]]; then
  echo "worktree path equals the main repository path — this should never happen; aborting" >&2
  exit 1
fi

echo "$WT"
