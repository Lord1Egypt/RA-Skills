#!/usr/bin/env bash
set -euo pipefail

STATE_ROOT=".git/.guarded-edit"
SESSIONS_DIR="$STATE_ROOT/sessions"
CURRENT_SESSION_FILE="$STATE_ROOT/current-session"
STATE_FORMAT="file-change-tracker"

SESSION_ID=""
SESSION_DIR=""
STATE_FILE=""
PATHS_FILE=""
SESSION_COMMENT=""
SESSION_REASON=""
PRE_SHA=""
POST_SHA=""
SESSION_STATUS=""
REPO_ROOT=""
PATHS_FILE_ABS=""
ACTIVE_GUARD_IGNORE=""
TS=""
CLOSED_TS=""
LAST_POST_STATUS=""
LAST_POST_MESSAGE=""

OPEN_SESSION_IDS=()
TARGET_PATHS=()
TARGET_STATUS=""
HAS_STAGED=0
HAS_DIRTY=0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd -P)"
DISTRIBUTED_IGNORE_FILE="$SKILL_DIR/guarded-edit.ignore"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

git_literal() {
  git --literal-pathspecs "$@"
}

need_git_repo() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return 0
  fi
  git init -q >/dev/null
}

ensure_identity() {
  if ! git config --get user.name >/dev/null 2>&1; then
    git config user.name "OpenClaw Tracker"
  fi
  if ! git config --get user.email >/dev/null 2>&1; then
    git config user.email "openclaw@local.invalid"
  fi
}

ensure_state_dirs() {
  mkdir -p "$SESSIONS_DIR"
}

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd -P
}

active_guard_ignore_file() {
  if [ -f "$DISTRIBUTED_IGNORE_FILE" ]; then
    echo "$DISTRIBUTED_IGNORE_FILE"
    return 0
  fi
  return 1
}

require_paths_not_excluded() {
  [ "$#" -gt 0 ] || return 0

  local ignore_file
  ignore_file="$(active_guard_ignore_file || true)"
  [ -n "$ignore_file" ] || return 0

  local path matched=0 detail
  for path in "$@"; do
    if git -c core.excludesFile="$ignore_file" check-ignore --no-index -q -- "$path"; then
      detail="$(git -c core.excludesFile="$ignore_file" check-ignore --no-index -v -- "$path" 2>/dev/null || true)"
      printf 'EXCLUDED_PATH %s\n' "$path" >&2
      if [ -n "$detail" ]; then
        printf '  %s\n' "$detail" >&2
      fi
      matched=1
    fi
  done

  if [ "$matched" -eq 1 ]; then
    fail "one or more target paths are excluded by active ignore rules. Edit $(printf '%q' "$ignore_file") or choose different target paths."
  fi
}

current_head() {
  git rev-parse --short HEAD 2>/dev/null || true
}

current_head_full() {
  git rev-parse HEAD 2>/dev/null || true
}

has_head() {
  git rev-parse --verify HEAD >/dev/null 2>&1
}

require_paths() {
  if [ "$#" -eq 0 ]; then
    fail "no target paths provided. Run: $0 pre \"reason\" -- <path> [<path> ...]"
  fi
}

set_session_files() {
  SESSION_DIR="$1"
  STATE_FILE="$SESSION_DIR/state.bin"
  PATHS_FILE="$SESSION_DIR/paths.nul"
}

new_session() {
  ensure_state_dirs
  SESSION_DIR="$(mktemp -d "$SESSIONS_DIR/session.XXXXXX")"
  SESSION_ID="$(basename "$SESSION_DIR")"
  set_session_files "$SESSION_DIR"
}

clear_loaded_state() {
  PRE_SHA=""
  POST_SHA=""
  SESSION_STATUS=""
  SESSION_COMMENT=""
  SESSION_REASON=""
  REPO_ROOT=""
  PATHS_FILE_ABS=""
  ACTIVE_GUARD_IGNORE=""
  TS=""
  CLOSED_TS=""
  LAST_POST_STATUS=""
  LAST_POST_MESSAGE=""
}

write_state_pair() {
  printf '%s\0%s\0' "$1" "$2"
}

write_state() {
  : > "$STATE_FILE"
  {
    write_state_pair "STATE_FORMAT" "$STATE_FORMAT"
    write_state_pair "SESSION_ID" "$SESSION_ID"
    write_state_pair "PRE_SHA" "${PRE_SHA:-}"
    write_state_pair "POST_SHA" "${POST_SHA:-}"
    write_state_pair "SESSION_STATUS" "${SESSION_STATUS:-open}"
    write_state_pair "SESSION_COMMENT" "${SESSION_COMMENT:-${SESSION_REASON:-manual edit}}"
    write_state_pair "REASON" "${SESSION_REASON:-${SESSION_COMMENT:-manual edit}}"
    write_state_pair "REPO_ROOT" "$(repo_root)"
    write_state_pair "PATHS_FILE_ABS" "$(paths_file_abs)"
    write_state_pair "ACTIVE_GUARD_IGNORE" "${ACTIVE_GUARD_IGNORE:-}"
    write_state_pair "TS" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    write_state_pair "CLOSED_TS" "${CLOSED_TS:-}"
    write_state_pair "LAST_POST_STATUS" "${LAST_POST_STATUS:-}"
    write_state_pair "LAST_POST_MESSAGE" "${LAST_POST_MESSAGE:-}"
  } >> "$STATE_FILE"
}

load_state_kv() {
  local key="$1"
  local value="$2"

  case "$key" in
    STATE_FORMAT)
      [ "$value" = "$STATE_FORMAT" ] || return 1
      ;;
    SESSION_ID|PRE_SHA|POST_SHA|SESSION_STATUS|SESSION_COMMENT|REASON|REPO_ROOT|PATHS_FILE_ABS|ACTIVE_GUARD_IGNORE|TS|CLOSED_TS|LAST_POST_STATUS|LAST_POST_MESSAGE)
      printf -v "$key" '%s' "$value"
      if [ "$key" = "REASON" ]; then
        SESSION_REASON="$value"
      fi
      ;;
    *)
      return 1
      ;;
  esac

  return 0
}

load_state() {
  [ -f "$STATE_FILE" ] || return 1

  clear_loaded_state

  local format_ok=0 key value
  while IFS= read -r -d '' key && IFS= read -r -d '' value; do
    if ! load_state_kv "$key" "$value"; then
      clear_loaded_state
      return 1
    fi
    if [ "$key" = "STATE_FORMAT" ]; then
      format_ok=1
    fi
  done < "$STATE_FILE"

  [ "$format_ok" -eq 1 ] || return 1
  [ -n "$SESSION_ID" ] || return 1

  SESSION_COMMENT="${SESSION_COMMENT:-${REASON:-manual edit}}"
  SESSION_REASON="${REASON:-${SESSION_COMMENT:-manual edit}}"
  REPO_ROOT="${REPO_ROOT:-$(repo_root)}"
  PATHS_FILE_ABS="${PATHS_FILE_ABS:-$(paths_file_abs)}"
  ACTIVE_GUARD_IGNORE="${ACTIVE_GUARD_IGNORE:-$(active_guard_ignore_file || true)}"
  SESSION_STATUS="${SESSION_STATUS:-open}"
  CLOSED_TS="${CLOSED_TS:-}"
  LAST_POST_STATUS="${LAST_POST_STATUS:-}"
  LAST_POST_MESSAGE="${LAST_POST_MESSAGE:-}"
  return 0
}

list_open_sessions() {
  OPEN_SESSION_IDS=()
  ensure_state_dirs

  local dir saved_session_id saved_session_dir saved_state_file saved_paths_file
  saved_session_id="$SESSION_ID"
  saved_session_dir="$SESSION_DIR"
  saved_state_file="$STATE_FILE"
  saved_paths_file="$PATHS_FILE"

  shopt -s nullglob
  for dir in "$SESSIONS_DIR"/session.*; do
    [ -d "$dir" ] || continue
    SESSION_DIR="$dir"
    SESSION_ID="$(basename "$SESSION_DIR")"
    set_session_files "$SESSION_DIR"
    if ! load_state; then
      continue
    fi
    if [ "${SESSION_STATUS:-open}" = "open" ]; then
      OPEN_SESSION_IDS+=("$SESSION_ID")
    fi
  done
  shopt -u nullglob

  SESSION_ID="$saved_session_id"
  SESSION_DIR="$saved_session_dir"
  STATE_FILE="$saved_state_file"
  PATHS_FILE="$saved_paths_file"
}

latest_session_id() {
  ensure_state_dirs
  local dir
  while IFS= read -r dir; do
    [ -d "$dir" ] || continue
    SESSION_DIR="$dir"
    SESSION_ID="$(basename "$SESSION_DIR")"
    set_session_files "$SESSION_DIR"
    if load_state; then
      printf '%s\n' "$SESSION_ID"
      return 0
    fi
  done < <(ls -1dt "$SESSIONS_DIR"/session.* 2>/dev/null || true)
  return 1
}

resolve_default_session() {
  list_open_sessions

  case "${#OPEN_SESSION_IDS[@]}" in
    1)
      SESSION_ID="${OPEN_SESSION_IDS[0]}"
      ;;
    0)
      fail "no open edit session found. Run PRE first or pass --session <session-id>."
      ;;
    *)
      fail "multiple open edit sessions exist. Run: $0 sessions 10, then pass --session <session-id>."
      ;;
  esac
}

select_session() {
  local requested_session="${1:-}"

  ensure_state_dirs
  if [ -n "$requested_session" ]; then
    SESSION_ID="$requested_session"
  else
    resolve_default_session
  fi

  SESSION_DIR="$SESSIONS_DIR/$SESSION_ID"
  [ -d "$SESSION_DIR" ] || fail "session not found: $SESSION_ID"
  set_session_files "$SESSION_DIR"
}

select_report_session() {
  ensure_state_dirs

  if [ -f "$CURRENT_SESSION_FILE" ]; then
    SESSION_ID="$(cat "$CURRENT_SESSION_FILE")"
    SESSION_DIR="$SESSIONS_DIR/$SESSION_ID"
    if [ -d "$SESSION_DIR" ]; then
      set_session_files "$SESSION_DIR"
      if load_state; then
        return 0
      fi
    fi
  fi

  if SESSION_ID="$(latest_session_id)"; then
    SESSION_DIR="$SESSIONS_DIR/$SESSION_ID"
    set_session_files "$SESSION_DIR"
    load_state
    return 0
  fi

  return 1
}

set_current_session() {
  printf '%s\n' "$SESSION_ID" > "$CURRENT_SESSION_FILE"
}

clear_current_session_if_matches() {
  if [ -f "$CURRENT_SESSION_FILE" ] && [ "$(cat "$CURRENT_SESSION_FILE")" = "$SESSION_ID" ]; then
    rm -f "$CURRENT_SESSION_FILE"
  fi
}

paths_file_abs() {
  if [ -f "$PATHS_FILE" ]; then
    echo "$(cd "$(dirname "$PATHS_FILE")" && pwd -P)/$(basename "$PATHS_FILE")"
  else
    echo "$PATHS_FILE"
  fi
}

save_paths() {
  : > "$PATHS_FILE"
  local path
  for path in "$@"; do
    printf '%s\0' "$path" >> "$PATHS_FILE"
  done
}

load_paths() {
  TARGET_PATHS=()
  [ -f "$PATHS_FILE" ] || return 1

  local path
  while IFS= read -r -d '' path; do
    TARGET_PATHS+=("$path")
  done < "$PATHS_FILE"

  [ "${#TARGET_PATHS[@]}" -gt 0 ]
}

refresh_target_status() {
  [ "${#TARGET_PATHS[@]}" -gt 0 ] || fail "internal error: no target paths loaded"

  TARGET_STATUS="$(git_literal status --porcelain=v1 --untracked-files=all -- "${TARGET_PATHS[@]}")"
  HAS_STAGED=0
  HAS_DIRTY=0

  if [ -n "$TARGET_STATUS" ]; then
    HAS_DIRTY=1
  fi

  local line x
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    if [[ "$line" == '?? '* ]]; then
      continue
    fi
    x="${line:0:1}"
    if [ "$x" != " " ]; then
      HAS_STAGED=1
      break
    fi
  done <<< "$TARGET_STATUS"
}

paths_dirty() {
  refresh_target_status
  [ "$HAS_DIRTY" -eq 1 ]
}

staged_changes_present() {
  refresh_target_status
  [ "$HAS_STAGED" -eq 1 ]
}

refuse_if_staged_changes_present() {
  if staged_changes_present; then
    fail "target paths already have staged changes. Refusing to rewrite target-path index state because that can flatten partial staging. Clean, commit, or stash those staged changes first, then run PRE/POST again."
  fi
}

stage_paths() {
  git_literal add -A -- "${TARGET_PATHS[@]}"
}

unstage_paths_best_effort() {
  if has_head; then
    git_literal reset -q HEAD -- "${TARGET_PATHS[@]}" >/dev/null 2>&1 || true
  else
    git reset -q -- "${TARGET_PATHS[@]}" >/dev/null 2>&1 || true
  fi
}

scoped_staged_diff_exists() {
  ! git_literal diff --cached --quiet -- "${TARGET_PATHS[@]}"
}

require_pre_state() {
  if ! load_state; then
    fail "no PRE snapshot found for this edit session. Run: $0 pre \"reason\" -- <path> [<path> ...]"
  fi
  if [ -z "$PRE_SHA" ]; then
    fail "PRE snapshot state is incomplete. Run: $0 pre \"reason\" -- <path> [<path> ...]"
  fi
  if ! load_paths; then
    fail "no stored target paths found for this edit session. Run PRE again with explicit paths."
  fi
  if [ "$(repo_root)" != "$REPO_ROOT" ]; then
    fail "current repo root does not match the stored edit session. Expected: $REPO_ROOT"
  fi
}

commit_subject() {
  local sha="$1"
  [ -n "$sha" ] || return 1
  git show -s --format=%s "$sha" 2>/dev/null || return 1
}

commit_summary() {
  local sha="$1"
  [ -n "$sha" ] || return 1
  git show -s --format='%h %s' "$sha" 2>/dev/null || return 1
}

print_commit_line() {
  local label="$1"
  local sha="$2"
  local fallback="$3"

  if [ -n "$sha" ] && commit_summary "$sha" >/dev/null 2>&1; then
    printf '%s: %s\n' "$label" "$(commit_summary "$sha")"
  else
    printf '%s: none %s\n' "$label" "$fallback"
  fi
}

create_scoped_commit() {
  local message="$1"
  if ! git_literal commit --no-verify -m "$message" --only -- "${TARGET_PATHS[@]}" >/dev/null; then
    unstage_paths_best_effort
    fail "guard commit failed while creating snapshot for the declared target paths"
  fi
}

close_session_state() {
  SESSION_STATUS="closed"
  CLOSED_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  write_state
  clear_current_session_if_matches
}

print_scope_summary() {
  echo "SESSION $SESSION_ID"
  echo "REPO $(repo_root)"
  echo "STATUS ${SESSION_STATUS:-open}"
  echo "COMMENT ${SESSION_COMMENT:-${SESSION_REASON:-manual edit}}"
  echo "PATHS ${#TARGET_PATHS[@]}"
  if [ -n "${ACTIVE_GUARD_IGNORE:-}" ]; then
    echo "IGNORE_FILE ${ACTIVE_GUARD_IGNORE}"
  fi
}

print_paths() {
  local path
  for path in "${TARGET_PATHS[@]}"; do
    printf '  - %s\n' "$path"
  done
}

pre() {
  SESSION_REASON="$1"
  SESSION_COMMENT="$SESSION_REASON"
  shift || true

  require_paths "$@"
  TARGET_PATHS=("$@")

  need_git_repo
  ensure_identity
  ACTIVE_GUARD_IGNORE="$(active_guard_ignore_file || true)"
  require_paths_not_excluded "${TARGET_PATHS[@]}"
  new_session
  save_paths "${TARGET_PATHS[@]}"

  local short_head full_head

  if has_head; then
    if paths_dirty; then
      refuse_if_staged_changes_present
      stage_paths
      if ! scoped_staged_diff_exists; then
        unstage_paths_best_effort
        full_head="$(current_head_full)"
        short_head="$(current_head)"
        PRE_SHA="$full_head"
        POST_SHA=""
        SESSION_STATUS="open"
        CLOSED_TS=""
        LAST_POST_STATUS=""
        LAST_POST_MESSAGE=""
        set_current_session
        write_state
        echo "PRE_REUSED $short_head $(commit_subject "$full_head")"
        print_scope_summary
        return 0
      fi
      create_scoped_commit "guard(pre): $SESSION_REASON"
      full_head="$(current_head_full)"
      short_head="$(current_head)"
      PRE_SHA="$full_head"
      POST_SHA=""
      SESSION_STATUS="open"
      CLOSED_TS=""
      LAST_POST_STATUS=""
      LAST_POST_MESSAGE=""
      set_current_session
      write_state
      echo "PRE_COMMIT $short_head $(commit_subject "$full_head")"
      print_scope_summary
      return 0
    fi

    full_head="$(current_head_full)"
    short_head="$(current_head)"
    PRE_SHA="$full_head"
    POST_SHA=""
    SESSION_STATUS="open"
    CLOSED_TS=""
    LAST_POST_STATUS=""
    LAST_POST_MESSAGE=""
    set_current_session
    write_state
    echo "PRE_REUSED $short_head $(commit_subject "$full_head")"
    print_scope_summary
    return 0
  fi

  if paths_dirty; then
    refuse_if_staged_changes_present
    stage_paths
    if ! scoped_staged_diff_exists; then
      unstage_paths_best_effort
      git commit --allow-empty --no-verify -m "guard(init): $SESSION_REASON" >/dev/null
    else
      create_scoped_commit "guard(init): $SESSION_REASON"
    fi
  else
    git commit --allow-empty --no-verify -m "guard(init): $SESSION_REASON" >/dev/null
  fi

  full_head="$(current_head_full)"
  short_head="$(current_head)"
  PRE_SHA="$full_head"
  POST_SHA=""
  SESSION_STATUS="open"
  CLOSED_TS=""
  LAST_POST_STATUS=""
  LAST_POST_MESSAGE=""
  set_current_session
  write_state
  echo "PRE_INIT $short_head $(commit_subject "$full_head")"
  print_scope_summary
}

post() {
  local post_reason="$1"
  local requested_session="${2:-}"

  need_git_repo
  ensure_identity
  ensure_state_dirs
  select_session "$requested_session"
  require_pre_state
  [ "$SESSION_STATUS" = "open" ] || fail "edit session is already closed: $SESSION_ID"
  SESSION_COMMENT="${SESSION_COMMENT:-${SESSION_REASON:-manual edit}}"

  if paths_dirty; then
    refuse_if_staged_changes_present
    stage_paths
    if ! scoped_staged_diff_exists; then
      unstage_paths_best_effort
      POST_SHA=""
      LAST_POST_STATUS="none"
      LAST_POST_MESSAGE="no staged diff for stored paths"
      close_session_state
      echo "POST_NONE $LAST_POST_MESSAGE"
      print_scope_summary
      return 0
    fi
    create_scoped_commit "guard(post): $post_reason"
    POST_SHA="$(current_head_full)"
    LAST_POST_STATUS="commit"
    LAST_POST_MESSAGE="$(commit_subject "$POST_SHA")"
    close_session_state
    echo "POST_COMMIT $(commit_summary "$POST_SHA")"
    print_scope_summary
    return 0
  fi

  POST_SHA=""
  LAST_POST_STATUS="none"
  LAST_POST_MESSAGE="no changes in stored paths"
  close_session_state
  echo "POST_NONE $LAST_POST_MESSAGE"
  print_scope_summary
}

recent_paths() {
  local count="$1"
  if [ "${#TARGET_PATHS[@]}" -eq 0 ]; then
    echo "No target paths"
    return 0
  fi
  if ! git_literal log --pretty=format:'%h %s' -n "$count" -- "${TARGET_PATHS[@]}" 2>/dev/null; then
    echo "No commits yet for target paths"
  fi
}

recent() {
  need_git_repo
  local count="${1:-5}"
  if ! [[ "$count" =~ ^[0-9]+$ ]]; then
    count=5
  fi
  if ! has_head; then
    echo "No commits yet"
    return 0
  fi

  if select_report_session && load_paths; then
    recent_paths "$count"
    return 0
  fi

  git log --pretty=format:'%h %s' -n "$count"
}

session_row() {
  local mark="$1"
  local pre_summary post_summary
  if [ -n "$PRE_SHA" ] && commit_summary "$PRE_SHA" >/dev/null 2>&1; then
    pre_summary="$(commit_summary "$PRE_SHA")"
  else
    pre_summary="none missing pre snapshot"
  fi

  if [ -n "$POST_SHA" ] && commit_summary "$POST_SHA" >/dev/null 2>&1; then
    post_summary="$(commit_summary "$POST_SHA")"
  else
    post_summary="none ${LAST_POST_MESSAGE:-not created}"
  fi

  printf '%s %s | %s | comment=%s | pre=%s | post=%s\n' \
    "$mark" \
    "$SESSION_ID" \
    "${SESSION_STATUS:-open}" \
    "${SESSION_COMMENT:-${SESSION_REASON:-manual edit}}" \
    "$pre_summary" \
    "$post_summary"
}

sessions() {
  ensure_state_dirs
  local count="${1:-5}"
  if ! [[ "$count" =~ ^[0-9]+$ ]]; then
    count=5
  fi

  local current=""
  if [ -f "$CURRENT_SESSION_FILE" ]; then
    current="$(cat "$CURRENT_SESSION_FILE")"
  fi

  local dir shown=0 mark
  while IFS= read -r dir; do
    [ -d "$dir" ] || continue
    SESSION_DIR="$dir"
    SESSION_ID="$(basename "$SESSION_DIR")"
    set_session_files "$SESSION_DIR"
    if ! load_state; then
      continue
    fi
    mark=" "
    if [ "$SESSION_ID" = "$current" ]; then
      mark="*"
    fi
    session_row "$mark"
    shown=$((shown + 1))
    if [ "$shown" -ge "$count" ]; then
      break
    fi
  done < <(ls -1dt "$SESSIONS_DIR"/session.* 2>/dev/null || true)

  if [ "$shown" -eq 0 ]; then
    echo "No saved edit sessions"
  fi
}

rollback_help() {
  local requested_session="${1:-}"

  need_git_repo
  ensure_state_dirs
  if [ -n "$requested_session" ]; then
    select_session "$requested_session"
  elif ! select_report_session; then
    echo "No guard session state found. Use: git log --oneline -n 5 && git reflog -n 10"
    return 0
  fi

  if ! load_state; then
    echo "No guard session state found. Use: git log --oneline -n 5 && git reflog -n 10"
    return 0
  fi
  if ! load_paths; then
    fail "session exists but target paths could not be loaded"
  fi

  echo "Rollback help"
  echo "SESSION_ID=${SESSION_ID}"
  echo "REPO_ROOT=${REPO_ROOT}"
  echo "SESSION_STATUS=${SESSION_STATUS}"
  echo "SESSION_COMMENT=${SESSION_COMMENT:-${SESSION_REASON:-manual edit}}"
  echo "TARGET_PATHS=${#TARGET_PATHS[@]}"
  print_paths
  echo "PATHS_FILE=${PATHS_FILE_ABS}"
  if [ -n "$ACTIVE_GUARD_IGNORE" ]; then
    echo "ACTIVE_GUARD_IGNORE=${ACTIVE_GUARD_IGNORE}"
  fi
  print_commit_line "PRE_SNAPSHOT" "$PRE_SHA" "missing pre snapshot"
  print_commit_line "POST_SNAPSHOT" "$POST_SHA" "${LAST_POST_MESSAGE:-not created}"
  if [ -n "$POST_SHA" ]; then
    echo "Preview result diff for stored paths: git diff ${PRE_SHA}..${POST_SHA} --pathspec-from-file=$(printf '%q' "$PATHS_FILE_ABS") --pathspec-file-nul"
    echo "History-preserving undo of the post commit: git revert ${POST_SHA}"
  fi
  if [ -n "$PRE_SHA" ]; then
    echo "Safest path-scoped rollback to the pre-edit snapshot: git restore --source=${PRE_SHA} --staged --worktree --pathspec-from-file=$(printf '%q' "$PATHS_FILE_ABS") --pathspec-file-nul"
  fi
  echo "Recovery history: git reflog -n 10"
}

report() {
  need_git_repo
  ensure_state_dirs

  local count="${1:-5}"
  if ! [[ "$count" =~ ^[0-9]+$ ]]; then
    count=5
  fi

  if ! select_report_session; then
    echo "No saved edit sessions"
    if has_head; then
      echo
      echo "最近${count}次记录:"
      git log --pretty=format:'- %h %s' -n "$count"
    fi
    return 0
  fi

  load_state || fail "session state could not be loaded"
  load_paths || fail "session paths could not be loaded"

  echo "文件变更保护状态："
  echo
  echo "会话: ${SESSION_ID} (${SESSION_STATUS})"
  echo "会话备注: ${SESSION_COMMENT:-${SESSION_REASON:-manual edit}}"
  echo "仓库: ${REPO_ROOT}"
  if [ -n "$ACTIVE_GUARD_IGNORE" ]; then
    echo "排除文件: ${ACTIVE_GUARD_IGNORE}"
  fi
  echo "保护路径:"
  print_paths
  print_commit_line "PRE 快照" "$PRE_SHA" "missing pre snapshot"
  print_commit_line "POST 快照" "$POST_SHA" "${LAST_POST_MESSAGE:-not created}"
  echo
  echo "最近${count}次记录:"
  if git_literal log --pretty=format:'- %h %s' -n "$count" -- "${TARGET_PATHS[@]}" 2>/dev/null; then
    :
  else
    echo "- none no commits yet for target paths"
  fi
  echo
  echo "最近${count}次会话:"
  sessions "$count"
}

parse_optional_session_arg() {
  OPTIONAL_SESSION_ID=""
  if [ "$#" -eq 0 ]; then
    return 0
  fi
  if [ "$1" = "--session" ]; then
    [ "$#" -ge 2 ] || fail "missing session id after --session"
    OPTIONAL_SESSION_ID="$2"
    [ "$#" -eq 2 ] || fail "unexpected extra arguments"
    return 0
  fi
  fail "unexpected arguments"
}

command_name="${1:-}"
shift || true

case "$command_name" in
  pre)
    reason="${1:-manual edit}"
    shift || true
    if [ "${1:-}" = "--" ]; then
      shift
    fi
    pre "$reason" "$@"
    ;;
  post)
    reason="${1:-manual edit}"
    shift || true
    parse_optional_session_arg "$@"
    post "$reason" "$OPTIONAL_SESSION_ID"
    ;;
  report)
    report "${1:-5}"
    ;;
  recent)
    recent "${1:-5}"
    ;;
  sessions)
    sessions "${1:-5}"
    ;;
  rollback-help)
    parse_optional_session_arg "$@"
    rollback_help "$OPTIONAL_SESSION_ID"
    ;;
  *)
    cat >&2 <<USAGE
Usage:
  $0 pre "reason" -- <path> [<path> ...]
  $0 post "reason" [--session <session-id>]
  $0 recent [count]
  $0 sessions [count]
  $0 report [count]
  $0 rollback-help [--session <session-id>]
USAGE
    exit 1
    ;;
esac
