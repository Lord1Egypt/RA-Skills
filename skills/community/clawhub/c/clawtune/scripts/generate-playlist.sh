#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

if [[ $# -lt 3 ]]; then
  echo "usage: $0 <title> <summary> <query> [target_count] [limit] [is_public]" >&2
  exit 1
fi

TITLE="$1"
SUMMARY="$2"
QUERY="$3"
TARGET_COUNT="${4:-5}"
LIMIT="${5:-10}"
IS_PUBLIC="${6:-false}"
USER_REF="${CLAWTUNE_USER_REF:-script-user}"
SKILL_SESSION_ID="${CLAWTUNE_SKILL_SESSION_ID:-$(json_get_file_value "$SESSION_FILE" "skill_session_id")}"
if [[ -z "$SKILL_SESSION_ID" ]]; then
  SKILL_SESSION_ID="skill-$(random_idempotency_key session)"
fi
IDEMPOTENCY_KEY="${CLAWTUNE_IDEMPOTENCY_KEY:-$(random_idempotency_key playlist)}"
STYLE_TAGS_JSON="${CLAWTUNE_STYLE_TAGS_JSON:-[]}"
MOOD_TAGS_JSON="${CLAWTUNE_MOOD_TAGS_JSON:-[]}"
SCENE_TAGS_JSON="${CLAWTUNE_SCENE_TAGS_JSON:-[]}"
LANGUAGE_VALUE="${CLAWTUNE_LANGUAGE:-}"

PAYLOAD=$(python3 - "$TITLE" "$SUMMARY" "$QUERY" "$TARGET_COUNT" "$LIMIT" "$IS_PUBLIC" "$USER_REF" "$SKILL_SESSION_ID" "$IDEMPOTENCY_KEY" "$STYLE_TAGS_JSON" "$MOOD_TAGS_JSON" "$SCENE_TAGS_JSON" "$LANGUAGE_VALUE" <<'PY'
import json, sys
(title, summary, query, target_count, limit, is_public, user_ref, skill_session_id, idempotency_key, style_tags, mood_tags, scene_tags, language) = sys.argv[1:]
payload = {
    "title": title,
    "summary": summary,
    "query": query,
    "target_count": int(target_count),
    "limit": int(limit),
    "is_public": is_public.lower() == 'true',
    "user_ref": user_ref,
    "skill_session_id": skill_session_id,
    "idempotency_key": idempotency_key,
    "style_tags": json.loads(style_tags),
    "mood_tags": json.loads(mood_tags),
    "scene_tags": json.loads(scene_tags),
}
if language:
    payload["language"] = language
print(json.dumps(payload, ensure_ascii=False))
PY
)

RESPONSE=$(CLAWTUNE_IDEMPOTENCY_KEY="$IDEMPOTENCY_KEY" "$SCRIPT_DIR/api-request.sh" POST /playlists/generate "$PAYLOAD")
json_assert_nonempty "$RESPONSE" "data.playlist_id"
json_assert_in "$RESPONSE" "data.generation_status" "ready,partial,generating,failed"

PLAYLIST_ID="$(json_get_string "$RESPONSE" "data.playlist_id")"
PUBLIC_STATUS="$(json_get_string "$RESPONSE" "data.public_status")"
GEN_STATUS="$(json_get_string "$RESPONSE" "data.generation_status")"

"$SCRIPT_DIR/session-state.sh" merge \
  skill_session_id "$SKILL_SESSION_ID" \
  current_phase "playlist" \
  current_playlist_id "$PLAYLIST_ID" \
  source_context_playlist_id "$PLAYLIST_ID" \
  last_user_intent_summary "$QUERY" >/dev/null

save_evidence_json "01-generate-playlist.response.json" "$RESPONSE"
save_evidence_json "01-generate-playlist.payload.json" "$PAYLOAD"
append_log "run.log" "generate-playlist playlist_id=$PLAYLIST_ID generation_status=$GEN_STATUS public_status=$PUBLIC_STATUS"
save_session_snapshot

json_pretty "$RESPONSE"
