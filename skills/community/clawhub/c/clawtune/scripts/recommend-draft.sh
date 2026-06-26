#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

DRAFT_ID="${1:-$(json_get_file_value "$SESSION_FILE" "current_draft_id")}"
if [[ -z "$DRAFT_ID" ]]; then
  echo "usage: $0 [draft_id]" >&2
  exit 1
fi

RESPONSE=$("$SCRIPT_DIR/api-request.sh" POST "/creation-drafts/$DRAFT_ID/recommendations" '{}')
json_assert_nonempty "$RESPONSE" "data.draft_id"
python3 - "$RESPONSE" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
recs = payload.get('data', {}).get('recommendations', [])
if not isinstance(recs, list) or not recs:
    raise SystemExit('recommendations must be a non-empty list')
PY

"$SCRIPT_DIR/session-state.sh" merge current_phase "draft" current_draft_id "$DRAFT_ID" >/dev/null
save_evidence_json "04-recommend-draft.response.json" "$RESPONSE"
append_log "run.log" "recommend-draft draft_id=$DRAFT_ID"
save_session_snapshot

json_pretty "$RESPONSE"
