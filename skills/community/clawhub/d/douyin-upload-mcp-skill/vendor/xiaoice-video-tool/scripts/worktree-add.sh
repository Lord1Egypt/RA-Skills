#!/usr/bin/env bash
set -euo pipefail

DEFAULT_BASE_BRANCH="phase1/bootstrap"

usage() {
  cat <<'EOF'
Usage:
  worktree-add.sh --branch <feature-branch> [--path <worktree-path>] [--base <base-branch>]
  worktree-add.sh <feature-branch> [--path <worktree-path>] [--base <base-branch>]

Create a new git worktree + branch for parallel subagent work.

Options:
  -b, --branch  New feature branch name (required unless passed positionally)
  -p, --path    Worktree directory (default: <repo>/.worktrees/<branch-with-dashes>)
  -B, --base    Base branch/start-point (default: phase1/bootstrap)
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

branch_name=""
worktree_path=""
base_branch="$DEFAULT_BASE_BRANCH"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -b|--branch)
      require_value "$1" "${2:-}"
      branch_name="$2"
      shift 2
      ;;
    -p|--path)
      require_value "$1" "${2:-}"
      worktree_path="$2"
      shift 2
      ;;
    -B|--base)
      require_value "$1" "${2:-}"
      base_branch="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      error "Unknown option: $1"
      ;;
    *)
      if [[ -z "$branch_name" ]]; then
        branch_name="$1"
      else
        error "Unexpected argument: $1"
      fi
      shift
      ;;
  esac
done

if [[ -z "$branch_name" ]]; then
  usage
  error "Missing required branch name."
fi

if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  error "Not inside a git repository."
fi

if ! git check-ref-format --branch "$branch_name" >/dev/null 2>&1; then
  error "Invalid branch name: '$branch_name'."
fi

if ! git check-ref-format --branch "$base_branch" >/dev/null 2>&1; then
  error "Invalid base branch name: '$base_branch'."
fi

cd "$repo_root"

if git show-ref --verify --quiet "refs/heads/$branch_name"; then
  error "Local branch '$branch_name' already exists."
fi

if git show-ref --verify --quiet "refs/remotes/origin/$branch_name"; then
  error "Remote branch 'origin/$branch_name' already exists."
fi

if git show-ref --verify --quiet "refs/heads/$base_branch"; then
  start_point="$base_branch"
elif git show-ref --verify --quiet "refs/remotes/origin/$base_branch"; then
  start_point="origin/$base_branch"
else
  error "Base branch '$base_branch' not found locally or on origin."
fi

if [[ -z "$worktree_path" ]]; then
  safe_name="${branch_name//\//-}"
  worktree_path="$repo_root/.worktrees/$safe_name"
elif [[ "$worktree_path" != /* ]]; then
  worktree_path="$repo_root/$worktree_path"
fi

if git worktree list --porcelain | awk '/^worktree / {print substr($0, 10)}' | grep -Fxq "$worktree_path"; then
  error "Worktree path is already registered: $worktree_path"
fi

if [[ -e "$worktree_path" ]]; then
  error "Path already exists: $worktree_path"
fi

mkdir -p "$(dirname "$worktree_path")"
git worktree add -b "$branch_name" "$worktree_path" "$start_point"

echo "Created worktree: $worktree_path"
echo "Created branch:   $branch_name"
echo "Base branch:      $start_point"
