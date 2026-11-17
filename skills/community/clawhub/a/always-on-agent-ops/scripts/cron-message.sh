# shellcheck shell=bash
# SOURCE ONLY - do not execute. This file defines one function and nothing else.
# Normalized cron status line. Source it from every preflight and dispatcher so
# all notifications share one shape and stay readable in a chat channel.
# Usage: cron_message <job> <status> <result> <item> <next> <details>

cron_message() {
  local name="${1:-openclaw}"
  local status="${2:-Done}"          # Done | Nothing to do | Started | Blocked | Human action required | Error
  local result="${3:-n/a}"
  local item="${4:-n/a}"
  local next="${5:-n/a}"
  local details="${6:-none}"

  printf '%s - %s\n' "$name" "$status"
  printf 'Result: %s\n' "$result"
  printf 'Item: %s\n' "$item"
  printf 'Next action: %s\n' "$next"
  printf 'Details: %s\n' "$details"
}
