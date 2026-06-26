#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  worktree-list.sh [--branch <branch-name>]

List git worktrees with branch and dirty/clean status.

Options:
  -b, --branch  Filter by branch name
  -h, --help    Show this help
EOF
}

error() {
  echo "Error: $*" >&2
  exit 1
}

require_value() {
  local flag="$1"
  local value="${2:-}"
  if [[ -z "$value" || "$value" == -* ]]; then
    error "Option '$flag' requires a value."
  fi
}

branch_filter=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -b|--branch)
      require_value "$1" "${2:-}"
      branch_filter="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      error "Unknown argument: $1"
      ;;
  esac
done

if [[ -n "$branch_filter" ]] && ! git check-ref-format --branch "$branch_filter" >/dev/null 2>&1; then
  error "Invalid branch name: '$branch_filter'."
fi

if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  error "Not inside a git repository."
fi

cd "$repo_root"

count=0

print_entry() {
  local path="$1"
  local branch="$2"
  local head="$3"
  local status kind

  [[ -z "$path" ]] && return
  [[ -z "$branch" ]] && branch="(detached)"

  if [[ -n "$branch_filter" && "$branch" != "$branch_filter" ]]; then
    return
  fi

  if [[ -n "$(git -C "$path" status --porcelain 2>/dev/null)" ]]; then
    status="dirty"
  else
    status="clean"
  fi

  if [[ "$path" == "$repo_root" ]]; then
    kind="main"
  else
    kind="linked"
  fi

  printf "%-55s %-28s %-10s %-12s\n" "$path" "$branch" "${head:0:8}" "$status/$kind"
  count=$((count + 1))
}

echo "PATH                                                    BRANCH                       HEAD       STATUS"
echo "--------------------------------------------------------------------------------------------------------------"

current_path=""
current_branch=""
current_head=""

while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ -z "$line" ]]; then
    print_entry "$current_path" "$current_branch" "$current_head"
    current_path=""
    current_branch=""
    current_head=""
    continue
  fi

  case "$line" in
    worktree\ *)
      current_path="${line#worktree }"
      ;;
    branch\ refs/heads/*)
      current_branch="${line#branch refs/heads/}"
      ;;
    HEAD\ *)
      current_head="${line#HEAD }"
      ;;
  esac
done < <(git worktree list --porcelain)

print_entry "$current_path" "$current_branch" "$current_head"

if [[ "$count" -eq 0 ]]; then
  if [[ -n "$branch_filter" ]]; then
    echo "No worktree found for branch '$branch_filter'."
  else
    echo "No worktrees found."
  fi
fi
