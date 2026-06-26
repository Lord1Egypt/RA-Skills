#!/usr/bin/env bash
set -euo pipefail

# 用法：
# 1) 不指定项目（自动识别）
#    collect_commit_context.sh <commit1> [commit2] [commit3] ...
#
# 2) 指定项目名（只在工作目录下对应项目中查）
#    collect_commit_context.sh <project> <commit1> [commit2] [commit3] ...
#
# 3) 指定项目路径（只在指定仓库中查）
#    collect_commit_context.sh /path/to/project <commit1> [commit2] [commit3] ...
#
# 说明：
# - 当前目录是 Git 仓库时，会优先检查当前仓库
# - 当前目录不是 Git 仓库时，默认扫描当前目录下的 Git 仓库
# - 可通过 COMMIT_REVIEWER_WORK_ROOT 指定统一扫描根目录
# - 为了避免上下文过大，PATCH 默认截断到 COMMIT_REVIEWER_PATCH_LINES 行

DEFAULT_WORK_ROOT="${COMMIT_REVIEWER_WORK_ROOT:-$(pwd)}"
SCAN_DEPTH="${COMMIT_REVIEWER_SCAN_DEPTH:-4}"
PATCH_LINES="${COMMIT_REVIEWER_PATCH_LINES:-1200}"

if [ "$#" -lt 1 ]; then
  echo "ERROR: no commit hashes or project provided" >&2
  exit 1
fi

for cmd in git find sed grep sort; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $cmd" >&2
    exit 1
  fi
done

trim() {
  local s="$1"
  s="${s#${s%%[![:space:]]*}}"
  s="${s%${s##*[![:space:]]}}"
  printf '%s' "$s"
}

is_git_repo() {
  [ -d "$1" ] && git -C "$1" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

get_repo_root() {
  git -C "$1" rev-parse --show-toplevel 2>/dev/null || true
}

commit_exists_in_repo() {
  local repo="$1"
  local commit="$2"
  git -C "$repo" rev-parse --verify --quiet "${commit}^{commit}" >/dev/null 2>&1
}

# 支持 7~40 位十六进制 commit，兼容短 hash
is_commit_hash() {
  local v="$1"
  [[ "$v" =~ ^[0-9a-fA-F]{7,40}$ ]]
}

looks_like_path() {
  local v="$1"
  [[ "$v" == */* || "$v" == .* || "$v" == ~* ]]
}

expand_path() {
  local p="$1"
  if [[ "$p" == "~" ]]; then
    printf '%s\n' "$HOME"
  elif [[ "$p" == ~/* ]]; then
    printf '%s\n' "$HOME/${p#~/}"
  else
    printf '%s\n' "$p"
  fi
}

find_git_repos_under_root() {
  local root="$1"
  [ -d "$root" ] || return 0

  find "$root" -mindepth 1 -maxdepth "$SCAN_DEPTH" -type d -name ".git" 2>/dev/null \
    | sed 's#/.git$##' \
    | sort -u
}

resolve_project_input() {
  local first_arg="$1"

  if is_commit_hash "$first_arg"; then
    echo "MODE:AUTO"
    return 0
  fi

  if looks_like_path "$first_arg"; then
    local path
    path="$(expand_path "$first_arg")"
    echo "MODE:PATH:$path"
    return 0
  fi

  echo "MODE:NAME:$first_arg"
}

unique_lines() {
  awk '!seen[$0]++'
}

resolve_repo_for_commit() {
  local commit="$1"
  local project_mode="${2:-AUTO}"
  local project_value="${3:-}"
  local -a matches=()
  local current_repo=""

  # 1) 显式指定路径
  if [ "$project_mode" = "PATH" ]; then
    local target_repo="$project_value"

    if [ ! -d "$target_repo" ]; then
      echo "PROJECT_NOT_FOUND:$target_repo"
      return 0
    fi

    if ! is_git_repo "$target_repo"; then
      echo "PROJECT_NOT_GIT:$target_repo"
      return 0
    fi

    target_repo="$(get_repo_root "$target_repo")"

    if commit_exists_in_repo "$target_repo" "$commit"; then
      echo "OK:$target_repo"
    else
      echo "NOT_FOUND_IN_PROJECT:$target_repo"
    fi
    return 0
  fi

  # 2) 显式指定项目名
  if [ "$project_mode" = "NAME" ]; then
    local target_repo="$DEFAULT_WORK_ROOT/$project_value"

    if [ ! -d "$target_repo" ]; then
      echo "PROJECT_NOT_FOUND:$target_repo"
      return 0
    fi

    if ! is_git_repo "$target_repo"; then
      echo "PROJECT_NOT_GIT:$target_repo"
      return 0
    fi

    target_repo="$(get_repo_root "$target_repo")"

    if commit_exists_in_repo "$target_repo" "$commit"; then
      echo "OK:$target_repo"
    else
      echo "NOT_FOUND_IN_PROJECT:$target_repo"
    fi
    return 0
  fi

  # 3) 自动识别：先看当前目录是不是 git 仓库
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    current_repo="$(git rev-parse --show-toplevel 2>/dev/null || true)"
    if [ -n "$current_repo" ] && commit_exists_in_repo "$current_repo" "$commit"; then
      matches+=("$current_repo")
    fi
  fi

  # 4) 再扫描工作根目录下的多个仓库
  while IFS= read -r repo; do
    [ -n "$repo" ] || continue
    repo="$(trim "$repo")"
    [ -n "$repo" ] || continue

    if [ -n "$current_repo" ] && [ "$repo" = "$current_repo" ]; then
      continue
    fi

    if commit_exists_in_repo "$repo" "$commit"; then
      matches+=("$repo")
    fi
  done < <(find_git_repos_under_root "$DEFAULT_WORK_ROOT")

  if [ "${#matches[@]}" -eq 1 ]; then
    echo "OK:${matches[0]}"
    return 0
  fi

  if [ "${#matches[@]}" -eq 0 ]; then
    echo "NOT_FOUND"
    return 0
  fi

  printf '%s\n' "${matches[@]}" | unique_lines | paste -sd '|' - | sed 's/^/MULTIPLE:/'
  return 0
}

print_patch_limited() {
  local repo="$1"
  local commit="$2"
  local tmp_file
  tmp_file="$(mktemp)"

  git -C "$repo" show --format= --unified=20 "$commit" -- . > "$tmp_file" 2>/dev/null || true

  local total_lines
  total_lines="$(wc -l < "$tmp_file" | tr -d ' ')"

  if [ "$total_lines" -le "$PATCH_LINES" ]; then
    cat "$tmp_file"
  else
    head -n "$PATCH_LINES" "$tmp_file"
    echo
    echo "[PATCH TRUNCATED] total_lines=$total_lines shown_lines=$PATCH_LINES"
    echo "[PATCH TRUNCATED] You should still judge cautiously if the modified logic may continue below."
  fi

  rm -f "$tmp_file"
}

print_commit_context() {
  local repo="$1"
  local commit="$2"

  local repo_root current_branch remote_url
  repo_root="$repo"
  current_branch="$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  remote_url="$(git -C "$repo" remote get-url origin 2>/dev/null || echo none)"

  echo "=== REPOSITORY CONTEXT ==="
  echo "repo_root: $repo_root"
  echo "branch: $current_branch"
  echo "remote: $remote_url"
  echo

  echo "============================================================"
  echo "=== COMMIT: $commit ==="
  echo "============================================================"

  echo "--- BASIC INFO ---"
  git -C "$repo" show --quiet --format='commit: %H
author: %an <%ae>
date: %ad
subject: %s' --date=local "$commit"
  echo

  echo "--- PARENTS ---"
  git -C "$repo" rev-list --parents -n 1 "$commit" || true
  echo

  echo "--- CHANGED FILES ---"
  git -C "$repo" diff-tree --no-commit-id --name-status -r "$commit" || true
  echo

  echo "--- STAT ---"
  git -C "$repo" show --stat --format= "$commit" || true
  echo

  echo "--- PATCH ---"
  print_patch_limited "$repo" "$commit"
  echo

  echo "--- POSSIBLE KEYWORDS ---"
  git -C "$repo" show --format= --name-only "$commit" \
    | grep -Ei 'controller|service|view|views|js|ts|vue|react|css|scss|less|config|conf|model|api|popup|modal|dialog|sort|close|button|table|list|page|router' \
    || true
  echo
}

PROJECT_MODE="AUTO"
PROJECT_VALUE=""
COMMITS=()

FIRST_ARG="${1:-}"
resolve_result="$(resolve_project_input "$FIRST_ARG")"

case "$resolve_result" in
  MODE:AUTO)
    PROJECT_MODE="AUTO"
    COMMITS=("$@")
    ;;
  MODE:PATH:*)
    PROJECT_MODE="PATH"
    PROJECT_VALUE="${resolve_result#MODE:PATH:}"
    shift
    [ "$#" -ge 1 ] || {
      echo "ERROR: project path provided but no commit hashes found" >&2
      exit 1
    }
    COMMITS=("$@")
    ;;
  MODE:NAME:*)
    PROJECT_MODE="NAME"
    PROJECT_VALUE="${resolve_result#MODE:NAME:}"
    shift
    [ "$#" -ge 1 ] || {
      echo "ERROR: project provided but no commit hashes found" >&2
      exit 1
    }
    COMMITS=("$@")
    ;;
  *)
    echo "ERROR: unexpected project resolve mode: $resolve_result" >&2
    exit 1
    ;;
esac

for c in "${COMMITS[@]}"; do
  if ! is_commit_hash "$c"; then
    echo "ERROR: invalid commit hash: $c" >&2
    echo "Expected 7 to 40 hexadecimal characters." >&2
    exit 1
  fi
done

echo "=== COMMIT REVIEWER CONTEXT ==="
echo "work_root: $DEFAULT_WORK_ROOT"
echo "scan_depth: $SCAN_DEPTH"
echo "patch_lines: $PATCH_LINES"
case "$PROJECT_MODE" in
  AUTO)
    echo "project: AUTO_DETECT"
    ;;
  NAME)
    echo "project: $PROJECT_VALUE"
    ;;
  PATH)
    echo "project_path: $PROJECT_VALUE"
    ;;
esac
echo

for COMMIT in "${COMMITS[@]}"; do
  result="$(resolve_repo_for_commit "$COMMIT" "$PROJECT_MODE" "$PROJECT_VALUE")"

  case "$result" in
    OK:*)
      repo="${result#OK:}"
      print_commit_context "$repo" "$COMMIT"
      ;;
    PROJECT_NOT_FOUND:*)
      proj="${result#PROJECT_NOT_FOUND:}"
      echo "============================================================"
      echo "=== COMMIT: $COMMIT ==="
      echo "============================================================"
      echo "ERROR: project not found: $proj"
      echo
      ;;
    PROJECT_NOT_GIT:*)
      proj="${result#PROJECT_NOT_GIT:}"
      echo "============================================================"
      echo "=== COMMIT: $COMMIT ==="
      echo "============================================================"
      echo "ERROR: specified project is not a git repository: $proj"
      echo
      ;;
    NOT_FOUND_IN_PROJECT:*)
      proj="${result#NOT_FOUND_IN_PROJECT:}"
      echo "============================================================"
      echo "=== COMMIT: $COMMIT ==="
      echo "============================================================"
      echo "ERROR: commit not found in specified project: $proj"
      echo
      ;;
    NOT_FOUND)
      echo "============================================================"
      echo "=== COMMIT: $COMMIT ==="
      echo "============================================================"
      echo "ERROR: commit not found in current repo or under work root: $DEFAULT_WORK_ROOT"
      echo
      ;;
    MULTIPLE:*)
      repos_raw="${result#MULTIPLE:}"
      echo "============================================================"
      echo "=== COMMIT: $COMMIT ==="
      echo "============================================================"
      echo "ERROR: commit found in multiple repositories"
      echo "matched_repos:"
      printf '%s' "$repos_raw" | tr '|' '\n'
      echo "Please specify the project path or project name."
      echo
      ;;
    *)
      echo "============================================================"
      echo "=== COMMIT: $COMMIT ==="
      echo "============================================================"
      echo "ERROR: unexpected resolve result: $result"
      echo
      ;;
  esac
done
