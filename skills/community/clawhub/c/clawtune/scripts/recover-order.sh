#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

ORDER_ID="${1:-$(json_get_file_value "$SESSION_FILE" "current_order_id")}"

if [[ -n "$ORDER_ID" ]]; then
  STATUS_JSON=$("$SCRIPT_DIR/api-request.sh" GET "/orders/$ORDER_ID/status")
  DELIVERY_JSON=$("$SCRIPT_DIR/api-request.sh" GET "/orders/$ORDER_ID/delivery")
  PLAYLIST_ID="$(json_get_string "$DELIVERY_JSON" "data.playlist_id")"
  "$SCRIPT_DIR/session-state.sh" merge current_phase "order" current_order_id "$ORDER_ID" >/dev/null
  if [[ -n "$PLAYLIST_ID" ]]; then
    "$SCRIPT_DIR/session-state.sh" merge current_phase "playlist_result" current_playlist_id "$PLAYLIST_ID" >/dev/null
  fi
  RESULT=$(python3 - <<'PY' "$ORDER_ID" "$PLAYLIST_ID" "$STATUS_JSON" "$DELIVERY_JSON"
import json, sys
order_id, playlist_id, status_raw, delivery_raw = sys.argv[1:5]
status_payload = json.loads(status_raw)
delivery_payload = json.loads(delivery_raw)
print(json.dumps({
    'recovery_anchor': 'order_id',
    'order_id': order_id,
    'playlist_id': playlist_id or None,
    'status': status_payload.get('data', status_payload),
    'delivery': delivery_payload.get('data', delivery_payload),
}, ensure_ascii=False, indent=2))
PY
)
  save_evidence_json "12-recover-order.response.json" "$RESULT"
  append_log "run.log" "recover-order anchor=order_id order_id=$ORDER_ID playlist_id=$PLAYLIST_ID"
  save_session_snapshot
  json_pretty "$RESULT"
  exit 0
fi

echo "No recoverable order_id found." >&2
exit 1
