#!/usr/bin/env bash
set -euo pipefail

# cc — Claude Code relay via tmux

TMUX_BIN="${TMUX_BIN:-$(command -v tmux 2>/dev/null || true)}"
FIND_BIN="${FIND_BIN:-$(command -v find 2>/dev/null || true)}"
SORT_BIN="${SORT_BIN:-$(command -v sort 2>/dev/null || true)}"
SLEEP_BIN="${SLEEP_BIN:-$(command -v sleep 2>/dev/null || true)}"
TAIL_BIN="${TAIL_BIN:-$(command -v tail 2>/dev/null || true)}"
GREP_BIN="${GREP_BIN:-$(command -v grep 2>/dev/null || true)}"
BASENAME_BIN="${BASENAME_BIN:-$(command -v basename 2>/dev/null || true)}"
AWK_BIN="${AWK_BIN:-$(command -v awk 2>/dev/null || true)}"
MKDIR_BIN="${MKDIR_BIN:-$(command -v mkdir 2>/dev/null || true)}"
CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude 2>/dev/null || true)}"
WC_BIN="${WC_BIN:-$(command -v wc 2>/dev/null || true)}"
SED_BIN="${SED_BIN:-$(command -v sed 2>/dev/null || true)}"
CUT_BIN="${CUT_BIN:-$(command -v cut 2>/dev/null || true)}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/cc"
CONFIG_FILE="${CONFIG_DIR}/config"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/cc"
LAST_FILE="${STATE_DIR}/last_project"
LOG_DIR="${STATE_DIR}/logs"
MAP_FILE="${SKILL_DIR}/projects.map"

${MKDIR_BIN} -p "${CONFIG_DIR}" "${STATE_DIR}" "${LOG_DIR}"

load_config() {
  PROJECT_ROOT="${HOME}/projects"
  if [[ -f "${CONFIG_FILE}" ]]; then
    local val
    val="$(${SED_BIN} -n 's/^PROJECT_ROOT="\(.*\)"$/\1/p' "${CONFIG_FILE}" 2>/dev/null || true)"
    [[ -n "${val}" ]] && PROJECT_ROOT="${val}"
  fi
  PROJECT_ROOT="${CLAUDE_RELAY_ROOT:-${PROJECT_ROOT}}"
  MAP_FILE="${CLAUDE_RELAY_MAP:-${MAP_FILE}}"
}

save_config_root() {
  local root="${1/#\~/$HOME}"
  [[ -d "${root}" ]] || { echo "ERROR: directory not found: ${root}" >&2; exit 4; }
  echo "PROJECT_ROOT=\"${root}\"" > "${CONFIG_FILE}"
  echo "OK: project root set to ${root}"
}

is_configured() { [[ -f "${CONFIG_FILE}" ]] || [[ -d "${HOME}/projects" ]]; }

load_config

need_bin() { [[ -n "$1" && -x "$1" ]] || { echo "ERROR: missing: ${2:-$1}" >&2; exit 2; }; }

sanitize() {
  local raw="${1,,}"; raw="${raw//[^a-z0-9_]/_}"; raw="${raw#__}"; raw="${raw%%__}"
  echo "${raw:0:40}"
}

session_name() { echo "cc_$(sanitize "$(${BASENAME_BIN} "$1")")"; }

log_file_for() { echo "${LOG_DIR}/${1}.log"; }

strip_ansi() {
  ${SED_BIN} -e 's/\x1b\[[0-9;]*[a-zA-Z]//g' \
             -e 's/\x1b\][0-9]*;[^\x07]*\x07//g' \
             -e 's/\x1b\[[?][0-9]*[a-zA-Z]//g' \
             -e 's/\x1b(B//g' \
             -e '/^$/d'
}

generate_project_pairs() {
  {
    [[ -f "${MAP_FILE}" ]] && ${AWK_BIN} -F'=' '/^[[:space:]]*#/{next}/^[[:space:]]*$/{next}{k=$1;v=substr($0,index($0,"=")+1);gsub(/^[[:space:]]+|[[:space:]]+$/,"",k);gsub(/^[[:space:]]+|[[:space:]]+$/,"",v);if(k!=""&&v!="")print k"|"v}' "${MAP_FILE}"
    [[ -d "${PROJECT_ROOT}" ]] && ${FIND_BIN} "${PROJECT_ROOT}" -mindepth 1 -maxdepth 1 -type d ! -name '.*' 2>/dev/null | while IFS= read -r p; do echo "$(${BASENAME_BIN} "$p")|$p"; done
  } | ${AWK_BIN} -F'|' 'NF>=2&&$1!=""&&$2!=""{k=tolower($1);if(!seen[k]++)print $1"|"$2}'
}

resolve_project() {
  local key="${1:-}"
  if [[ -z "${key}" ]]; then
    [[ -f "${LAST_FILE}" ]] || { echo "ERROR: no project specified" >&2; exit 4; }
    local last; last="$(cat "${LAST_FILE}")"
    [[ -d "${last}" ]] || { echo "ERROR: last project gone: ${last}" >&2; exit 4; }
    echo "${last}"; return 0
  fi
  [[ "${key}" == /* ]] && { [[ -d "${key}" ]] || { echo "ERROR: not found: ${key}" >&2; exit 4; }; echo "${key}"; return 0; }
  local exact; exact="$(generate_project_pairs | ${AWK_BIN} -F'|' -v k="${key}" '$1==k{print $2;exit}')"
  [[ -n "${exact}" ]] && { echo "${exact}"; return 0; }
  local m=(); while IFS= read -r line; do m+=("$line"); done < <(generate_project_pairs | ${AWK_BIN} -F'|' -v k="${key,,}" 'tolower($1)==k{print $2}')
  (( ${#m[@]} == 1 )) && { echo "${m[0]}"; return 0; }
  (( ${#m[@]} > 1 )) && { echo "ERROR: ambiguous '${key}'" >&2; return 1; }
  local f=(); while IFS= read -r line; do f+=("$line"); done < <(generate_project_pairs | ${AWK_BIN} -F'|' -v k="${key,,}" 'index(tolower($1),k)>0||index(tolower($2),k)>0{print $1"|"$2}')
  (( ${#f[@]} == 1 )) && { echo "${f[0]#*|}"; return 0; }
  (( ${#f[@]} > 1 )) && { echo "ERROR: ambiguous '${key}':" >&2; printf ' - %s\n' "${f[@]}" >&2; return 1; }
  echo "ERROR: not found: ${key}" >&2; exit 4
}

do_start() {
  local project="$1" sess; sess="$(session_name "${project}")"
  need_bin "${TMUX_BIN}" "tmux"; need_bin "${CLAUDE_BIN}" "claude"
  local log; log="$(log_file_for "${sess}")"
  if ${TMUX_BIN} has-session -t "${sess}" 2>/dev/null; then
    echo "session running: ${sess}"
  else
    ${TMUX_BIN} new-session -d -s "${sess}" "cd $(printf '%q' "${project}") && $(printf '%q' "${CLAUDE_BIN}") -c"
    ${SLEEP_BIN} 1
    echo "session started: ${sess}"
  fi
  # Start (or restart) pipe-pane logging
  : > "${log}"
  ${TMUX_BIN} pipe-pane -t "${sess}" "cat >> $(printf '%q' "${log}")"
  echo "${project}" > "${LAST_FILE}"
}

do_send() {
  local project="$1"; shift; local text="$*" sess; sess="$(session_name "${project}")"
  need_bin "${TMUX_BIN}" "tmux"
  ${TMUX_BIN} has-session -t "${sess}" 2>/dev/null || { echo "ERROR: no session. /cc on first" >&2; exit 6; }
  [[ -n "${text}" ]] || { echo "ERROR: message required" >&2; exit 7; }

  local log; log="$(log_file_for "${sess}")"
  # Record offset before sending — everything after this is the new reply
  local offset=0
  if [[ -f "${log}" ]]; then
    offset=$(${WC_BIN} -c < "${log}" | tr -d ' ')
  fi

  ${TMUX_BIN} send-keys -t "${sess}" -l -- "${text}"; ${TMUX_BIN} send-keys -t "${sess}" Enter

  # Poll until output stabilizes (same content twice) or max 60s
  local max_wait="${RELAY_WAIT_MAX:-60}" interval=2 elapsed=0 prev="" curr=""
  ${SLEEP_BIN} "${interval}"
  while (( elapsed < max_wait )); do
    curr="$(${TMUX_BIN} capture-pane -t "${sess}" -p 2>/dev/null || true)"
    [[ -n "${prev}" && "${curr}" == "${prev}" ]] && break
    prev="${curr}"
    ${SLEEP_BIN} "${interval}"
    elapsed=$((elapsed + interval))
  done

  # Read incremental output from log file
  if [[ -f "${log}" ]]; then
    ${TAIL_BIN} -c +$((offset + 1)) "${log}" | strip_ansi
  else
    # Fallback: capture-pane if log missing
    ${TMUX_BIN} capture-pane -t "${sess}" -p | strip_ansi | ${TAIL_BIN} -n 80
  fi
}

do_tail() {
  local project="$1" lines="${2:-120}" sess; sess="$(session_name "${project}")"
  need_bin "${TMUX_BIN}" "tmux"
  ${TMUX_BIN} has-session -t "${sess}" 2>/dev/null || { echo "ERROR: no session" >&2; exit 6; }
  local log; log="$(log_file_for "${sess}")"
  if [[ -f "${log}" && -s "${log}" ]]; then
    ${TAIL_BIN} -n "${lines}" "${log}" | strip_ansi
  else
    # Fallback: capture-pane
    ${TMUX_BIN} capture-pane -t "${sess}" -p | strip_ansi | ${TAIL_BIN} -n "${lines}"
  fi
}

do_stop() {
  local project="$1" sess; sess="$(session_name "${project}")"
  need_bin "${TMUX_BIN}" "tmux"
  local log; log="$(log_file_for "${sess}")"
  ${TMUX_BIN} has-session -t "${sess}" 2>/dev/null && { ${TMUX_BIN} kill-session -t "${sess}"; echo "stopped: ${sess}"; } || echo "not running: ${sess}"
  rm -f "${log}"
}

do_status() { need_bin "${TMUX_BIN}" "tmux"; ${TMUX_BIN} list-sessions 2>/dev/null | ${GREP_BIN} -E '^cc_' || echo "no sessions"; }

do_check() {
  local project="$1" sess; sess="$(session_name "${project}")"
  need_bin "${TMUX_BIN}" "tmux"
  if ! ${TMUX_BIN} has-session -t "${sess}" 2>/dev/null; then
    echo "STATUS: no_session"; return 0
  fi
  local pane_pid; pane_pid="$(${TMUX_BIN} display-message -t "${sess}" -p '#{pane_pid}' 2>/dev/null || true)"
  if [[ -n "${pane_pid}" ]] && kill -0 "${pane_pid}" 2>/dev/null; then
    local last_line; last_line="$(${TMUX_BIN} capture-pane -t "${sess}" -p | strip_ansi | ${GREP_BIN} -v '^$' | ${TAIL_BIN} -n 1)"
    if echo "${last_line}" | ${GREP_BIN} -qiE "Thinking|Reading|Working|Searching|Editing|Writing"; then
      echo "STATUS: processing"; echo "LAST: ${last_line}"
    else
      echo "STATUS: ready"; echo "LAST: ${last_line}"
    fi
  else
    echo "STATUS: dead"
  fi
}

do_projects() {
  local lines; lines="$(generate_project_pairs | ${SORT_BIN} -f || true)"
  [[ -z "${lines}" ]] && { echo "no projects in ${PROJECT_ROOT}"; return 0; }
  local last_name=""
  [[ -f "${LAST_FILE}" ]] && last_name="$(${BASENAME_BIN} "$(cat "${LAST_FILE}")" 2>/dev/null || true)"
  while IFS='|' read -r a p; do
    [[ -n "${a}" ]] || continue
    if [[ "${a}" == "${last_name}" ]]; then
      printf ' ★ %-20s %s\n' "${a}" "${p}"
    else
      printf ' - %-20s %s\n' "${a}" "${p}"
    fi
  done <<< "${lines}"
}

check_setup() { is_configured || { echo "SETUP_NEEDED"; exit 100; }; }

first="${1:-}"; shift || true
case "${first}" in
  config) local_sub="${1:-}"; shift || true
    case "${local_sub}" in root) [[ $# -gt 0 ]] && save_config_root "$1" || echo "root: ${PROJECT_ROOT}";; "") echo "root: ${PROJECT_ROOT}";; *) echo "ERROR: unknown: ${local_sub}" >&2; exit 1;; esac;;
  projects|list) check_setup; do_projects;;
  on|start) check_setup; [[ -n "${1:-}" ]] || { echo "ERROR: /cc on <project>" >&2; exit 1; }; p="$(resolve_project "$1")" || exit 1; do_start "${p}";;
  off|stop) check_setup; [[ $# -gt 0 ]] && { p="$(resolve_project "$1" 2>/dev/null)" || p="$1"; } || p="$(resolve_project "")"; do_stop "${p}";;
  tail) check_setup
    if [[ $# -eq 0 ]]; then do_tail "$(resolve_project "")" 120
    elif [[ "$1" =~ ^[0-9]+$ ]]; then do_tail "$(resolve_project "")" "$1"
    else p="$(resolve_project "$1" 2>/dev/null)" || p="$1"; do_tail "${p}" "${2:-120}"; fi;;
  check|"?") check_setup; p="$(resolve_project "${1:-}" 2>/dev/null)" || p="$(resolve_project "")"; do_check "${p}";;
  status) do_status;;
  "") echo "cc — Claude Code relay via tmux"; echo "  /cc on <project>  /cc off  /cc ?  /cc tail  /cc projects  /cc <msg>";;
  *) check_setup
    if p="$(resolve_project "${first}" 2>/dev/null)"; then
      s="$(session_name "${p}")"; ${TMUX_BIN} has-session -t "${s}" 2>/dev/null && { [[ -n "$*" ]] || { echo "ERROR: msg required" >&2; exit 1; }; do_send "${p}" "$@"; exit 0; }
    fi
    msg="${first}"; [[ $# -gt 0 ]] && msg+=" $*"; do_send "$(resolve_project "")" "${msg}";;
esac
