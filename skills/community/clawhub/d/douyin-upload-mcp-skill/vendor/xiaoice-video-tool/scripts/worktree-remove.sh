#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  worktree-remove.sh --path <worktree-path> [--force] [--delete-branch]
  worktree-remove.sh --branch <branch-name> [--force] [--delete-branch]

Remove a linked git worktree by path or branch.

Options:
  -p, --path           Worktree path to remove
  -b, --branch         Branch name of the worktree to remove
  -f, --force          Force remove even when worktree has uncommitted changes
  -d, --delete-branch  Delete the local branch after worktree removal
  -h, --help           Show this help
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

normalize_path() {
  local path="$1"
  path="${path%/}"
  if [[ -z "$path" ]]; then
    printf "/\n"
  else
    printf "%s\n" "$path"
  fi
}

lookup_worktree_by_branch() {
  local target_branch="$1"
  local current_path=""
  local current_branch=""
  local line

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -z "$line" ]]; then
      if [[ "$current_branch" == "$target_branch" ]]; then
        printf "%s\n" "$current_path"
        return 0
      fi
      current_path=""
      current_branch=""
      continue
    fi

    case "$line" in
      worktree\ *)
        current_path="${line#worktree }"
        ;;
      branch\ refs/heads/*)
        current_branch="${line#branch refs/heads/}"
        ;;
    esac
  done < <(git worktree list --porcelain)

  if [[ "$current_branch" == "$target_branch" ]]; then
    printf "%s\n" "$current_path"
    return 0
  fi

  return 1
}

lookup_branch_by_worktree() {
  local target_path="$1"
  local current_path=""
  local current_branch=""
  local line

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -z "$line" ]]; then
      if [[ "$(normalize_path "$current_path")" == "$target_path" ]]; then
        printf "%s\n" "$current_branch"
        return 0
      fi
      current_path=""
      current_branch=""
      continue
    fi

    case "$line" in
      worktree\ *)
        current_path="${line#worktree }"
        ;;
      branch\ refs/heads/*)
        current_branch="${line#branch refs/heads/}"
        ;;
    esac
  done < <(git worktree list --porcelain)

  if [[ "$(normalize_path "$current_path")" == "$target_path" ]]; then
    printf "%s\n" "$current_branch"
    return 0
  fi

  return 1
}

target_path=""
target_branch=""
force_remove=false
delete_branch=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--path)
      require_value "$1" "${2:-}"
      target_path="$2"
      shift 2
      ;;
    -b|--branch)
      require_value "$1" "${2:-}"
      target_branch="$2"
      shift 2
      ;;
    -f|--force)
      force_remove=true
      shift
      ;;
    -d|--delete-branch)
      delete_branch=true
      shift
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

if [[ -n "$target_path" && -n "$target_branch" ]]; then
  error "Use either --path or --branch, not both."
fi

if [[ -z "$target_path" && -z "$target_branch" ]]; then
  usage
  error "You must specify --path or --branch."
fi

if [[ -n "$target_branch" ]] && ! git check-ref-format --branch "$target_branch" >/dev/null 2>&1; then
  error "Invalid branch name: '$target_branch'."
fi

if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  error "Not inside a git repository."
fi

cd "$repo_root"

if [[ -n "$target_branch" ]]; then
  if ! target_path="$(lookup_worktree_by_branch "$target_branch")"; then
    error "No worktree found for branch '$target_branch'."
  fi
else
  if [[ "$target_path" != /* ]]; then
    target_path="$repo_root/$target_path"
  fi
  target_path="$(normalize_path "$target_path")"
fi

target_path="$(normalize_path "$target_path")"
repo_root_norm="$(normalize_path "$repo_root")"

if [[ "$target_path" == "$repo_root_norm" ]]; then
  error "Refusing to remove the main worktree: $target_path"
fi

if ! git worktree list --porcelain | awk '/^worktree / {print substr($0, 10)}' | sed 's:/*$::' | grep -Fxq "$target_path"; then
  error "Path is not a registered worktree: $target_path"
fi

branch_for_path="$(lookup_branch_by_worktree "$target_path" || true)"

if [[ "$force_remove" == false ]]; then
  if [[ -n "$(git -C "$target_path" status --porcelain 2>/dev/null)" ]]; then
    error "Worktree has uncommitted changes. Re-run with --force."
  fi
fi

if [[ "$force_remove" == true ]]; then
  git worktree remove --force "$target_path"
else
  git worktree remove "$target_path"
fi

echo "Removed worktree: $target_path"

if [[ "$delete_branch" == true ]]; then
  if [[ -z "$branch_for_path" ]]; then
    error "Worktree had no local branch to delete (detached HEAD)."
  fi

  if [[ "$force_remove" == true ]]; then
    git branch -D "$branch_for_path"
  else
    git branch -d "$branch_for_path"
  fi
  echo "Deleted branch:   $branch_for_path"
fi
