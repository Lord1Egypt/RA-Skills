#!/bin/bash
set -euo pipefail

CLAWRENT_API="${CLAWRENT_URL:-https://clawrent.ai}/api/approvals"
ALLOW_FILE="${CLAWRENT_ALLOW_FILE:-$HOME/.openclaw/credentials/telegram-allowFrom.json}"
SKILL_VERSION="${CLAWRENT_SKILL_VERSION:-1.0.0}"

fetch_by_status() {
  local status="$1"
  curl -sf \
    -H "Authorization: Bearer $CLAWRENT_TOKEN" \
    -H "X-Clawrent-Skill: $SKILL_VERSION" \
    "$CLAWRENT_API?status=$status" 2>/dev/null || echo "[]"
}

mark_status() {
  local approval_id="$1"
  local status="$2"

  curl -sf -X PATCH \
    -H "Authorization: Bearer $CLAWRENT_TOKEN" \
    -H "X-Clawrent-Skill: $SKILL_VERSION" \
    -H "Content-Type: application/json" \
    "$CLAWRENT_API" \
    -d "{\"id\":\"$approval_id\",\"status\":\"$status\"}" >/dev/null
}

clear_allowlist() {
  mkdir -p "$(dirname "$ALLOW_FILE")"
  echo "[]" > "$ALLOW_FILE"
}

process_approved() {
  local approvals
  approvals="$(fetch_by_status approved)"

  [ -z "$approvals" ] || [ "$approvals" = "[]" ] && return 0

  echo "$approvals" | jq -c '.[] | {id, code}' | while read -r item; do
    local approval_id code
    approval_id="$(echo "$item" | jq -r '.id')"
    code="$(echo "$item" | jq -r '.code')"

    [ -z "$approval_id" ] || [ "$approval_id" = "null" ] && continue
    [ -z "$code" ] || [ "$code" = "null" ] && continue

    echo "Approving pairing code: $code"
    if openclaw pairing approve telegram "$code" --notify; then
      echo "Approved: $code"
      if mark_status "$approval_id" "executed"; then
        echo "Marked executed: $approval_id"
      else
        echo "Failed to mark executed: $approval_id"
      fi
    else
      echo "Failed to approve: $code"
    fi
  done
}

process_expired() {
  local expired
  expired="$(fetch_by_status expired)"

  [ -z "$expired" ] || [ "$expired" = "[]" ] && return 0

  echo "$expired" | jq -c '.[] | {id, code}' | while read -r item; do
    local approval_id code
    approval_id="$(echo "$item" | jq -r '.id')"
    code="$(echo "$item" | jq -r '.code')"

    [ -z "$approval_id" ] || [ "$approval_id" = "null" ] && continue

    echo "Revoking expired lease: ${code:-unknown-code}"
    if clear_allowlist; then
      if mark_status "$approval_id" "expired"; then
        echo "Marked expired: $approval_id"
      else
        echo "Failed to mark expired: $approval_id"
      fi
    else
      echo "Failed to clear allowlist for expired lease: $approval_id"
    fi
  done
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  process_approved
  process_expired
fi
