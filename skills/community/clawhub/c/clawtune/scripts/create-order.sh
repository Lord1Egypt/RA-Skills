#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

DRAFT_ID="${1:-$(json_get_file_value "$SESSION_FILE" "current_draft_id")}"
PROPOSAL_SUMMARY="${2:-$(json_get_file_value "$SESSION_FILE" "last_user_intent_summary")}"
CURRENCY_VALUE="${3:-CNY}"
IDEMPOTENCY_KEY="${CLAWTUNE_IDEMPOTENCY_KEY:-$(random_idempotency_key order)}"
SKILL_SESSION_ID="${CLAWTUNE_SKILL_SESSION_ID:-$(json_get_file_value "$SESSION_FILE" "skill_session_id")}"
SOURCE_CONTEXT_PLAYLIST_ID="${CLAWTUNE_SOURCE_CONTEXT_PLAYLIST_ID:-$(json_get_file_value "$SESSION_FILE" "source_context_playlist_id")}"
SOURCE_CONTEXT_SONG_ID="${CLAWTUNE_SOURCE_CONTEXT_SONG_ID:-$(json_get_file_value "$SESSION_FILE" "source_context_song_id")}"
if [[ -z "$DRAFT_ID" || -z "$PROPOSAL_SUMMARY" ]]; then
  echo "usage: $0 [draft_id] [proposal_summary] [currency]" >&2
  exit 1
fi

USER_REF="${CLAWTUNE_USER_REF:-script-user}"

PAYLOAD=$(python3 - "$DRAFT_ID" "$PROPOSAL_SUMMARY" "$CURRENCY_VALUE" "$USER_REF" "$SKILL_SESSION_ID" "$SOURCE_CONTEXT_PLAYLIST_ID" "$SOURCE_CONTEXT_SONG_ID" "$IDEMPOTENCY_KEY" <<'PY'
import json, sys
(draft_id, proposal_summary, currency, user_ref, skill_session_id, source_context_playlist_id, source_context_song_id, idempotency_key) = sys.argv[1:]
payload = {
    "draft_id": draft_id,
    "proposal_summary": proposal_summary,
    "currency": currency,
    "user_ref": user_ref,
    "idempotency_key": idempotency_key,
}
optional = {
    "skill_session_id": skill_session_id,
    "source_context_playlist_id": source_context_playlist_id,
    "source_context_song_id": source_context_song_id,
}
for key, value in optional.items():
    if value:
        payload[key] = value
print(json.dumps(payload, ensure_ascii=False))
PY
)

RESPONSE=$(CLAWTUNE_IDEMPOTENCY_KEY="$IDEMPOTENCY_KEY" "$SCRIPT_DIR/api-request.sh" POST /orders "$PAYLOAD")
json_assert_nonempty "$RESPONSE" "data.order_id"
json_assert_nonempty "$RESPONSE" "data.order_status"
json_assert_nonempty "$RESPONSE" "data.order_confirm_url"

ORDER_ID="$(json_get_string "$RESPONSE" "data.order_id")"
ORDER_STATUS="$(json_get_string "$RESPONSE" "data.order_status")"
ORDER_CONFIRM_URL="$(json_get_string "$RESPONSE" "data.order_confirm_url")"

"$SCRIPT_DIR/session-state.sh" merge \
  current_phase "order" \
  current_order_id "$ORDER_ID" \
  current_draft_id "$DRAFT_ID" \
  last_user_intent_summary "$PROPOSAL_SUMMARY" >/dev/null

save_evidence_json "06-create-order.payload.json" "$PAYLOAD"
save_evidence_json "06-create-order.response.json" "$RESPONSE"
append_log "run.log" "create-order order_id=$ORDER_ID order_status=$ORDER_STATUS order_confirm_url=$ORDER_CONFIRM_URL"
save_session_snapshot

json_pretty "$RESPONSE"
