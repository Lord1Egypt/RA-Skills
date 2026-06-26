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

RESPONSE=$("$SCRIPT_DIR/api-request.sh" GET "/orders/$ORDER_ID/delivery")
json_assert_nonempty "$RESPONSE" "data.order_id"
json_assert_nonempty "$RESPONSE" "data.delivery_status"
PLAYLIST_ID="$(json_get_string "$RESPONSE" "data.playlist_id")"
if [[ -n "$PLAYLIST_ID" ]]; then
  "$SCRIPT_DIR/session-state.sh" merge current_phase "playlist_result" current_order_id "$ORDER_ID" current_playlist_id "$PLAYLIST_ID" >/dev/null
else
  "$SCRIPT_DIR/session-state.sh" merge current_phase "delivery" current_order_id "$ORDER_ID" >/dev/null
fi

save_evidence_json "10-check-order-delivery.response.json" "$RESPONSE"
append_log "run.log" "check-order-delivery order_id=$ORDER_ID delivery_status=$(json_get_string "$RESPONSE" "data.delivery_status") playlist_id=$PLAYLIST_ID"
save_session_snapshot

json_pretty "$RESPONSE"
