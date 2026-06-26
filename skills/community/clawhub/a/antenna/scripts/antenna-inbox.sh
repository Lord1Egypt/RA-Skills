#!/usr/bin/env bash
# antenna-inbox.sh — Queue management for Antenna inbox feature.
# Optional approval queue for inbound messages.
#
# Usage:
#   antenna-inbox.sh list
#   antenna-inbox.sh count
#   antenna-inbox.sh show <ref>
#   antenna-inbox.sh approve all | <ref-list>
#   antenna-inbox.sh deny all | <ref-list>
#   antenna-inbox.sh drain [--execute]
#   antenna-inbox.sh clear
#   antenna-inbox.sh queue-add <json-item>
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"
# shellcheck source=../lib/config.sh
source "$SKILL_DIR/lib/config.sh"
QUEUE_PATH=$(config_inbox_queue_path)

# Resolve relative paths against skill dir
if [[ "$QUEUE_PATH" != /* ]]; then
  QUEUE_PATH="$SKILL_DIR/$QUEUE_PATH"
fi

# ── Colors ───────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✓${NC}  $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
err()   { echo -e "${RED}✗${NC}  $*" >&2; }

# ── Logging ──────────────────────────────────────────────────────────────────

log_entry() {
  local log_enabled log_path
  log_enabled=$(config_log_enabled)
  log_path=$(config_log_path)

  if [[ "$log_enabled" != "true" ]]; then
    return 0
  fi

  # Resolve relative log path against skill dir
  if [[ "$log_path" != /* ]]; then
    log_path="$SKILL_DIR/$log_path"
  fi

  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$ts] INBOX    | $*" >> "$log_path"
}

# ── Queue file initialization / locking ─────────────────────────────────────

QUEUE_LOCK_PATH="${QUEUE_PATH}.lock"

ensure_queue_file() {
  mkdir -p "$(dirname "$QUEUE_PATH")"
  if [[ ! -f "$QUEUE_PATH" ]]; then
    echo '[]' > "$QUEUE_PATH"
    chmod 644 "$QUEUE_PATH"
  fi
}

with_queue_lock() {
  ensure_queue_file
  exec 9>"$QUEUE_LOCK_PATH"
  flock -x 9
  "$@"
}

# ── Read queue ───────────────────────────────────────────────────────────────

read_queue() {
  ensure_queue_file
  jq -r '.' "$QUEUE_PATH"
}

# ── Write queue ──────────────────────────────────────────────────────────────

write_queue() {
  local data="$1"
  local tmp
  tmp=$(mktemp)
  echo "$data" > "$tmp" && mv "$tmp" "$QUEUE_PATH"
}

# ── Next ref number ──────────────────────────────────────────────────────────

next_ref() {
  ensure_queue_file
  jq '[.[].ref // 0] | max + 1' "$QUEUE_PATH" 2>/dev/null || echo "1"
}

# ── Parse ref list (supports 1,3,5-7 format) ─────────────────────────────────

parse_ref_list() {
  local input="$1"
  local refs=()

  IFS=',' read -ra parts <<< "$input"
  for part in "${parts[@]}"; do
    part=$(echo "$part" | xargs) # trim whitespace
    if [[ "$part" =~ ^([0-9]+)-([0-9]+)$ ]]; then
      # Range
      local start="${BASH_REMATCH[1]}"
      local end="${BASH_REMATCH[2]}"
      for ((i=start; i<=end; i++)); do
        refs+=("$i")
      done
    elif [[ "$part" =~ ^[0-9]+$ ]]; then
      # Single ref
      refs+=("$part")
    else
      err "Invalid ref format: $part"
      return 1
    fi
  done

  # Output as space-separated
  echo "${refs[@]}"
}

# ── Commands ─────────────────────────────────────────────────────────────────

cmd_list() {
  ensure_queue_file
  local queue
  queue=$(read_queue)
  
  local pending_count
  pending_count=$(echo "$queue" | jq '[.[] | select(.status == "pending")] | length')
  
  if [[ "$pending_count" -eq 0 ]]; then
    echo "No pending messages."
    return 0
  fi
  
  echo "Pending Messages:"
  echo ""
  
  # Print table header
  printf "${BOLD}%-6s %-20s %-20s %-15s %s${NC}\n" "Ref#" "Time" "From" "To" "Preview"
  printf "%-6s %-20s %-20s %-15s %s\n" "────" "──────────────────" "──────────────────" "─────────────" "──────────────────────────────"
  
  # Print pending items
  echo "$queue" | jq -r '.[] | select(.status == "pending") | 
    [.ref, .queued_at, .from, .target_session, .body_preview] | @tsv' | \
  while IFS=$'\t' read -r ref time from to preview; do
    # Truncate fields to fit
    time=$(echo "$time" | cut -c1-19)
    from=$(printf "%-20.20s" "$from")
    to=$(printf "%-15.15s" "$to")
    preview=$(printf "%-40.40s" "$preview")
    printf "%-6s %-20s %-20s %-15s %s\n" "$ref" "$time" "$from" "$to" "$preview"
  done
  
  echo ""
  echo "Total pending: $pending_count"
}

cmd_count() {
  ensure_queue_file
  jq '[.[] | select(.status == "pending")] | length' "$QUEUE_PATH"
}

cmd_show() {
  local ref="${1:?Usage: antenna-inbox.sh show <ref>}"
  ensure_queue_file
  
  local item
  item=$(jq --argjson ref "$ref" '.[] | select(.ref == $ref)' "$QUEUE_PATH")
  
  if [[ -z "$item" ]]; then
    err "Ref #$ref not found in queue"
    return 1
  fi
  
  # Pretty print the full message
  echo ""
  echo -e "${BOLD}Message Ref #$ref${NC}"
  echo "────────────────────────────────────────────────────────────────"
  echo "$item" | jq -r '.full_message'
  echo "────────────────────────────────────────────────────────────────"
  echo ""
  echo "Status: $(echo "$item" | jq -r '.status')"
  echo "From: $(echo "$item" | jq -r '.from') ($(echo "$item" | jq -r '.display_name'))"
  echo "To: $(echo "$item" | jq -r '.target_session')"
  echo "Queued: $(echo "$item" | jq -r '.queued_at')"
  echo "Size: $(echo "$item" | jq -r '.body_chars') chars"
}

cmd_approve_locked() {
  local target="$1"
  local queue
  queue=$(read_queue)

  if [[ "$target" == "all" ]]; then
    local updated
    updated=$(echo "$queue" | jq '[.[] | if .status == "pending" then .status = "approved" else . end]')
    write_queue "$updated"
    local count
    count=$(echo "$updated" | jq '[.[] | select(.status == "approved")] | length')
    ok "Approved all pending messages ($count items)"
    log_entry "action:approve_all | count:$count"
  else
    local refs
    refs=$(parse_ref_list "$target") || return 1

    local updated="$queue"
    local approved_count=0
    for ref in $refs; do
      local exists
      exists=$(echo "$updated" | jq --argjson r "$ref" '[.[] | select(.ref == $r)] | length')
      if [[ "$exists" -eq 0 ]]; then
        warn "Ref #$ref not found, skipping"
        continue
      fi
      updated=$(echo "$updated" | jq --argjson r "$ref" \
        '[.[] | if .ref == $r and .status == "pending" then .status = "approved" else . end]')
      approved_count=$((approved_count + 1))
    done

    write_queue "$updated"
    ok "Approved $approved_count message(s)"
    log_entry "action:approve | refs:$target | count:$approved_count"
  fi
}

cmd_approve() {
  local target="${1:?Usage: antenna-inbox.sh approve all|<ref-list>}"
  with_queue_lock cmd_approve_locked "$target"
}

cmd_deny_locked() {
  local target="$1"
  local queue
  queue=$(read_queue)

  if [[ "$target" == "all" ]]; then
    local updated
    updated=$(echo "$queue" | jq '[.[] | if .status == "pending" then .status = "denied" else . end]')
    write_queue "$updated"
    local count
    count=$(echo "$updated" | jq '[.[] | select(.status == "denied")] | length')
    ok "Denied all pending messages ($count items)"
    log_entry "action:deny_all | count:$count"
  else
    local refs
    refs=$(parse_ref_list "$target") || return 1

    local updated="$queue"
    local denied_count=0
    for ref in $refs; do
      local exists
      exists=$(echo "$updated" | jq --argjson r "$ref" '[.[] | select(.ref == $r)] | length')
      if [[ "$exists" -eq 0 ]]; then
        warn "Ref #$ref not found, skipping"
        continue
      fi
      updated=$(echo "$updated" | jq --argjson r "$ref" \
        '[.[] | if .ref == $r and .status == "pending" then .status = "denied" else . end]')
      denied_count=$((denied_count + 1))
    done

    write_queue "$updated"
    ok "Denied $denied_count message(s)"
    log_entry "action:deny | refs:$target | count:$denied_count"
  fi
}

cmd_deny() {
  local target="${1:?Usage: antenna-inbox.sh deny all|<ref-list>}"
  with_queue_lock cmd_deny_locked "$target"
}

cmd_drain_locked() {
  local queue
  queue=$(read_queue)

  local approved
  approved=$(echo "$queue" | jq '[.[] | select(.status == "approved")]')
  local approved_count
  approved_count=$(echo "$approved" | jq 'length')

  local denied_count
  denied_count=$(echo "$queue" | jq '[.[] | select(.status == "denied")] | length')

  if [[ "$approved_count" -eq 0 && "$denied_count" -eq 0 ]]; then
    info "No messages to drain (nothing approved or denied)"
    return 0
  fi

  # Remove denied items up front — no delivery needed.
  if [[ "$denied_count" -gt 0 ]]; then
    queue=$(echo "$queue" | jq '[.[] | select(.status != "denied")]')
  fi

  local delivered_count=0
  local failed_count=0

  if [[ "$approved_count" -gt 0 ]]; then
    local refs
    refs=$(echo "$approved" | jq -r '.[].ref')

    local ref
    for ref in $refs; do
      local item session_key message
      item=$(echo "$queue" | jq --argjson r "$ref" '.[] | select(.ref == $r)')
      session_key=$(echo "$item" | jq -r '.session_key')
      message=$(echo "$item" | jq -r '.full_message')

      local rpc_params
      rpc_params=$(jq -nc --arg key "$session_key" --arg msg "$message" \
        '{key: $key, message: $msg}')

      local rpc_json rpc_status rpc_runid rpc_err
      rpc_json=$(openclaw gateway call sessions.send \
        --params "$rpc_params" \
        --json \
        --timeout 60000 2>&1) || true

      rpc_status=$(printf '%s' "$rpc_json" | jq -r '.status // empty' 2>/dev/null || true)
      rpc_runid=$(printf '%s' "$rpc_json" | jq -r '.runId // empty' 2>/dev/null || true)
      rpc_err=$(printf '%s' "$rpc_json" | jq -r '.error // empty' 2>/dev/null || true)

      if [[ "$rpc_status" == "started" ]]; then
        queue=$(echo "$queue" | jq --argjson r "$ref" \
          '[.[] | if .ref == $r then .status = "delivered" | del(.last_error) else . end]')
        delivered_count=$((delivered_count + 1))
        log_entry "action:deliver | ref:$ref | session:$session_key | runId:$rpc_runid"
        ok "Delivered ref #$ref → $session_key (runId: $rpc_runid)" >&2
      else
        if [[ -z "$rpc_err" ]]; then
          rpc_err=$(printf '%s' "$rpc_json" | tr '\n' ' ' | sed 's/  */ /g' | head -c 300)
        fi
        queue=$(echo "$queue" | jq --argjson r "$ref" --arg err "$rpc_err" \
          '[.[] | if .ref == $r then .status = "failed" | .last_error = $err else . end]')
        failed_count=$((failed_count + 1))
        log_entry "action:deliver_failed | ref:$ref | session:$session_key | error:$rpc_err"
        err "Failed ref #$ref → $session_key — $rpc_err"
      fi
    done
  fi

  write_queue "$queue"

  log_entry "action:drain | delivered:$delivered_count | failed:$failed_count | denied:$denied_count"
  info "Drained: $delivered_count delivered, $failed_count failed, $denied_count denied (removed)" >&2

  if [[ "$failed_count" -gt 0 ]]; then
    return 1
  fi
}

cmd_drain() {
  with_queue_lock cmd_drain_locked
}

cmd_clear_locked() {
  local queue
  queue=$(read_queue)

  local cleared_count
  cleared_count=$(echo "$queue" | jq '[.[] | select(.status == "delivered" or .status == "denied" or .status == "failed")] | length')

  if [[ "$cleared_count" -eq 0 ]]; then
    info "No processed messages to clear"
    return 0
  fi

  local updated
  updated=$(echo "$queue" | jq '[.[] | select(.status != "delivered" and .status != "denied" and .status != "failed")]')
  write_queue "$updated"

  ok "Cleared $cleared_count processed message(s)"
  log_entry "action:clear | count:$cleared_count"
}

cmd_clear() {
  with_queue_lock cmd_clear_locked
}

cmd_queue_add_locked() {
  local item="$1"

  local from target body
  from=$(echo "$item" | jq -r '.from // empty')
  target=$(echo "$item" | jq -r '.target_session // empty')
  body=$(echo "$item" | jq -r '.full_message // empty')

  if [[ -z "$from" || -z "$target" || -z "$body" ]]; then
    err "Missing required fields in queue item"
    return 1
  fi

  local ref
  ref=$(next_ref)

  local enriched
  enriched=$(echo "$item" | jq --argjson ref "$ref" --arg ts "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    '. + {ref: $ref, queued_at: $ts, status: "pending"}')

  local queue updated
  queue=$(read_queue)
  updated=$(echo "$queue" | jq --argjson item "$enriched" '. + [$item]')
  write_queue "$updated"

  jq -n \
    --argjson ref "$ref" \
    --arg from "$from" \
    '{action: "queue", ref: $ref, from: $from}'

  log_entry "action:queue | ref:$ref | from:$from | session:$target"
}

cmd_queue_add() {
  local item
  item=$(cat)
  with_queue_lock cmd_queue_add_locked "$item"
}

# ── Dispatch ─────────────────────────────────────────────────────────────────

COMMAND="${1:-list}"
shift || true

case "$COMMAND" in
  list)       cmd_list ;;
  count)      cmd_count ;;
  show)       cmd_show "$@" ;;
  approve)    cmd_approve "$@" ;;
  deny)       cmd_deny "$@" ;;
  drain)      cmd_drain "$@" ;;
  clear)      cmd_clear ;;
  queue-add)  cmd_queue_add ;;
  *)
    err "Unknown command: $COMMAND"
    echo "Usage: antenna-inbox.sh list|count|show|approve|deny|drain|clear" >&2
    exit 1
    ;;
esac
