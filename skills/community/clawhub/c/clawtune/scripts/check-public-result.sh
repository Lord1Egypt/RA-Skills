#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

MODE="${1:-order}"
TARGET_ID="${2:-}"

case "$MODE" in
  order)
    if [[ -z "$TARGET_ID" ]]; then
      TARGET_ID="$(json_get_file_value "$SESSION_FILE" "current_order_id")"
    fi
    if [[ -z "$TARGET_ID" ]]; then
      echo "usage: $0 order [order_id]" >&2
      exit 1
    fi
    RESPONSE=$(curl -fsSL "${CLAWTUNE_BASE_URL:-https://clawtune.aqifun.com/api/v1}/public/orders/$TARGET_ID/result")
    json_assert_nonempty "$RESPONSE" "data.order_id"
    json_assert_nonempty "$RESPONSE" "data.status_text"
    save_evidence_json "11-check-public-order-result.response.json" "$RESPONSE"
    append_log "run.log" "check-public-result mode=order order_id=$TARGET_ID"
    ;;
  playlist)
    if [[ -z "$TARGET_ID" ]]; then
      TARGET_ID="$(json_get_file_value "$SESSION_FILE" "current_playlist_id")"
    fi
    if [[ -z "$TARGET_ID" ]]; then
      echo "usage: $0 playlist [playlist_id]" >&2
      exit 1
    fi
    RESPONSE=$(curl -fsSL "${CLAWTUNE_BASE_URL:-https://clawtune.aqifun.com/api/v1}/public/playlists/$TARGET_ID")
    json_assert_nonempty "$RESPONSE" "data.playlist_id"
    save_evidence_json "11-check-public-playlist.response.json" "$RESPONSE"
    append_log "run.log" "check-public-result mode=playlist playlist_id=$TARGET_ID"
    ;;
  *)
    echo "usage: $0 [order|playlist] [target_id]" >&2
    exit 1
    ;;
esac

save_session_snapshot
json_pretty "$RESPONSE"
