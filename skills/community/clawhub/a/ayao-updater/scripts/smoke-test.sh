#!/usr/bin/env bash

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
UPDATE_SCRIPT="$REPO_ROOT/skills/ayao-updater/scripts/update.sh"
INSTALL_CRON_SCRIPT="$REPO_ROOT/skills/ayao-updater/scripts/install-cron.sh"

declare -a CHECK_NAMES=()
declare -a CHECK_RESULTS=()
declare -a CHECK_DETAILS=()

first_non_empty_line() {
  local input="$1"
  local line

  while IFS= read -r line; do
    if [[ -n "${line//[[:space:]]/}" ]]; then
      if [[ "$line" =~ ^\[[^]]+\][[:space:]]*$ ]]; then
        continue
      fi
      printf '%s\n' "$line"
      return 0
    fi
  done <<< "$input"

  return 1
}

record_result() {
  local name="$1"
  local result="$2"
  local detail="$3"

  CHECK_NAMES+=("$name")
  CHECK_RESULTS+=("$result")
  CHECK_DETAILS+=("$detail")
}

check_command() {
  local cmd="$1"
  local resolved

  if resolved="$(command -v "$cmd" 2>/dev/null)"; then
    record_result "command: $cmd" "PASS" "$resolved"
  else
    record_result "command: $cmd" "FAIL" "not found"
  fi
}

run_check() {
  local name="$1"
  shift

  local output
  local status

  output="$("$@" 2>&1)"
  status=$?

  if [[ $status -eq 0 ]]; then
    local detail="exit 0"
    local snippet=""
    if snippet="$(first_non_empty_line "$output")"; then
      detail+="; $snippet"
    fi
    record_result "$name" "PASS" "$detail"
  else
    local detail="exit $status"
    local snippet=""
    if snippet="$(first_non_empty_line "$output")"; then
      detail+="; $snippet"
    fi
    record_result "$name" "FAIL" "$detail"
  fi
}

check_clawhub_list() {
  local output
  local status

  output="$(clawhub list 2>&1)"
  status=$?

  if [[ $status -eq 0 && -n "$output" ]]; then
    local snippet=""
    if snippet="$(first_non_empty_line "$output")"; then
      record_result "clawhub list" "PASS" "exit 0; $snippet"
    else
      record_result "clawhub list" "FAIL" "exit 0; no output"
    fi
  elif [[ $status -eq 0 ]]; then
    record_result "clawhub list" "FAIL" "exit 0; no output"
  else
    local detail="exit $status"
    local snippet=""
    if snippet="$(first_non_empty_line "$output")"; then
      detail+="; $snippet"
    fi
    record_result "clawhub list" "FAIL" "$detail"
  fi
}

check_update_dry_run() {
  local output
  local status

  output="$(bash "$UPDATE_SCRIPT" --dry-run 2>&1)"
  status=$?

  if [[ $status -eq 0 ]]; then
    local snippet=""
    if snippet="$(first_non_empty_line "$output")"; then
      record_result "update.sh --dry-run" "PASS" "exit 0; $snippet"
    else
      record_result "update.sh --dry-run" "PASS" "exit 0"
    fi
  else
    local detail="exit $status"
    local snippet=""
    if snippet="$(first_non_empty_line "$output")"; then
      detail+="; $snippet"
    fi
    record_result "update.sh --dry-run" "FAIL" "$detail"
  fi
}

print_summary() {
  local failures=0
  local i

  printf 'Smoke Test Summary\n'
  printf '==================\n'

  for i in "${!CHECK_NAMES[@]}"; do
    printf '%-4s %s: %s\n' "${CHECK_RESULTS[$i]}" "${CHECK_NAMES[$i]}" "${CHECK_DETAILS[$i]}"
    if [[ "${CHECK_RESULTS[$i]}" == "FAIL" ]]; then
      failures=$((failures + 1))
    fi
  done

  if [[ $failures -eq 0 ]]; then
    printf 'OVERALL PASS\n'
    return 0
  fi

  printf 'OVERALL FAIL (%d failed)\n' "$failures"
  return 1
}

check_command "openclaw"
check_command "clawhub"
check_command "bash"
check_command "python3"
check_clawhub_list
run_check "bash -n update.sh" bash -n "$UPDATE_SCRIPT"
run_check "bash -n install-cron.sh" bash -n "$INSTALL_CRON_SCRIPT"
check_update_dry_run

print_summary
