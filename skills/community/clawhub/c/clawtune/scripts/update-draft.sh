#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

DRAFT_ID="${1:-$(json_get_file_value "$SESSION_FILE" "current_draft_id")}"
if [[ -z "$DRAFT_ID" ]]; then
  echo "usage: $0 <draft_id> [proposal_summary] [theme] [style] [language] [mood] [scene] [lyrics_input]" >&2
  exit 1
fi

PROPOSAL_SUMMARY="${2:-}"
THEME="${3:-}"
STYLE="${4:-}"
LANGUAGE_VALUE="${5:-}"
MOOD="${6:-}"
SCENE="${7:-}"
LYRICS_INPUT="${8:-}"

PAYLOAD=$(python3 - "$PROPOSAL_SUMMARY" "$THEME" "$STYLE" "$LANGUAGE_VALUE" "$MOOD" "$SCENE" "$LYRICS_INPUT" <<'PY'
import json, sys
proposal_summary, theme, style, language, mood, scene, lyrics_input = sys.argv[1:]
payload = {}
for key, value in {
    "proposal_summary": proposal_summary,
    "theme": theme,
    "style": style,
    "language": language,
    "mood": mood,
    "scene": scene,
    "lyrics_input": lyrics_input,
}.items():
    if value:
        payload[key] = value
print(json.dumps(payload, ensure_ascii=False))
PY
)

if [[ "$PAYLOAD" == "{}" ]]; then
  echo "at least one field is required for draft update" >&2
  exit 1
fi

RESPONSE=$("$SCRIPT_DIR/api-request.sh" PATCH "/creation-drafts/$DRAFT_ID" "$PAYLOAD")
json_assert_nonempty "$RESPONSE" "data.draft_id"
json_assert_nonempty "$RESPONSE" "data.updated_at"
json_assert_in "$RESPONSE" "data.ready_for_quote" "true,false"

READY_FOR_QUOTE="$(json_get_string "$RESPONSE" "data.ready_for_quote")"
"$SCRIPT_DIR/session-state.sh" merge current_phase "draft" current_draft_id "$DRAFT_ID" >/dev/null

save_evidence_json "03-update-draft.payload.json" "$PAYLOAD"
save_evidence_json "03-update-draft.response.json" "$RESPONSE"
append_log "run.log" "update-draft draft_id=$DRAFT_ID ready_for_quote=$READY_FOR_QUOTE"
save_session_snapshot

json_pretty "$RESPONSE"
