#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

ORDER_ID="${1:-$(json_get_file_value "$SESSION_FILE" "current_order_id")}"
if [[ -z "$ORDER_ID" ]]; then
  echo "usage: $0 [order_id]" >&2
  exit 1
fi

RESPONSE=$("$SCRIPT_DIR/api-request.sh" GET "/orders/$ORDER_ID/status")
json_assert_nonempty "$RESPONSE" "data.order_id"
json_assert_nonempty "$RESPONSE" "data.status_text"
json_assert_nonempty "$RESPONSE" "data.next_action_text"

save_evidence_json "09-check-order-status.response.json" "$RESPONSE"
append_log "run.log" "check-order-status order_id=$ORDER_ID order_status=$(json_get_string "$RESPONSE" "data.order_status")"
save_session_snapshot

json_pretty "$RESPONSE"
