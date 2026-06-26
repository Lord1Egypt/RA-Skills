#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <proposal_summary> [theme] [style] [language] [mood] [scene] [lyrics_input]" >&2
  exit 1
fi

PROPOSAL_SUMMARY="$1"
THEME="${2:-}"
STYLE="${3:-}"
LANGUAGE_VALUE="${4:-}"
MOOD="${5:-}"
SCENE="${6:-}"
LYRICS_INPUT="${7:-}"
USER_REF="${CLAWTUNE_USER_REF:-script-user}"
SKILL_SESSION_ID="${CLAWTUNE_SKILL_SESSION_ID:-$(json_get_file_value "$SESSION_FILE" "skill_session_id")}"
SOURCE_CONTEXT_PLAYLIST_ID="${CLAWTUNE_SOURCE_CONTEXT_PLAYLIST_ID:-$(json_get_file_value "$SESSION_FILE" "current_playlist_id")}"
SOURCE_CONTEXT_SONG_ID="${CLAWTUNE_SOURCE_CONTEXT_SONG_ID:-$(json_get_file_value "$SESSION_FILE" "source_context_song_id")}"
if [[ -z "$SKILL_SESSION_ID" ]]; then
  SKILL_SESSION_ID="skill-$(random_idempotency_key session)"
fi

PAYLOAD=$(python3 - "$PROPOSAL_SUMMARY" "$THEME" "$STYLE" "$LANGUAGE_VALUE" "$MOOD" "$SCENE" "$LYRICS_INPUT" "$USER_REF" "$SKILL_SESSION_ID" "$SOURCE_CONTEXT_PLAYLIST_ID" "$SOURCE_CONTEXT_SONG_ID" <<'PY'
import json, sys
proposal_summary, theme, style, language, mood, scene, lyrics_input, user_ref, skill_session_id, source_context_playlist_id, source_context_song_id = sys.argv[1:]
payload = {
    "proposal_summary": proposal_summary,
    "user_ref": user_ref,
    "skill_session_id": skill_session_id,
}
optional = {
    "theme": theme,
    "style": style,
    "language": language,
    "mood": mood,
    "scene": scene,
    "lyrics_input": lyrics_input,
    "source_context_playlist_id": source_context_playlist_id,
    "source_context_song_id": source_context_song_id,
}
for key, value in optional.items():
    if value:
        payload[key] = value
print(json.dumps(payload, ensure_ascii=False))
PY
)

RESPONSE=$("$SCRIPT_DIR/api-request.sh" POST /creation-drafts "$PAYLOAD")
json_assert_nonempty "$RESPONSE" "data.draft_id"
json_assert_nonempty "$RESPONSE" "data.draft_status"

DRAFT_ID="$(json_get_string "$RESPONSE" "data.draft_id")"
DRAFT_STATUS="$(json_get_string "$RESPONSE" "data.draft_status")"

"$SCRIPT_DIR/session-state.sh" merge \
  skill_session_id "$SKILL_SESSION_ID" \
  current_phase "draft" \
  current_draft_id "$DRAFT_ID" \
  source_context_playlist_id "$SOURCE_CONTEXT_PLAYLIST_ID" \
  source_context_song_id "$SOURCE_CONTEXT_SONG_ID" \
  last_user_intent_summary "$PROPOSAL_SUMMARY" >/dev/null

save_evidence_json "02-create-draft.payload.json" "$PAYLOAD"
save_evidence_json "02-create-draft.response.json" "$RESPONSE"
append_log "run.log" "create-draft draft_id=$DRAFT_ID draft_status=$DRAFT_STATUS"
save_session_snapshot

json_pretty "$RESPONSE"
