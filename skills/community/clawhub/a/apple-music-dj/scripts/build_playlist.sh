#!/usr/bin/env bash
# build_playlist.sh — Create or update a playlist in Apple Music
#
# Usage:
#   scripts/build_playlist.sh create <name> <description> <song_ids_file>
#   scripts/build_playlist.sh refresh <playlist_id> <song_ids_file>
#   scripts/build_playlist.sh remove <playlist_id> <song_ids_file>
#
# Every mode changes your Apple Music library, so each only previews ("WOULD ...", exit 3)
# unless --yes is the LAST argument. Callers pass it after their own confirmation.
#
# song_ids_file: one Apple Music catalog song ID per line
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

MODE="${1:?Usage: build_playlist.sh <create|refresh|remove> ...}"

# A trailing --yes is the confirmation; strip it so the positional arguments stay as documented.
YES=0
if [[ "${*: -1}" == "--yes" ]]; then
  YES=1
  set -- "${@:1:$(($# - 1))}"
fi
_require_yes() {
  [[ "$YES" == "1" ]] && return 0
  echo "WOULD $1 — preview only, nothing was changed. Re-run with --yes as the last argument to apply." >&2
  exit 3
}

case "$MODE" in
  create)
    NAME="${2:?Usage: build_playlist.sh create <name> <description> <song_ids_file>}"
    DESC="${3:?Usage: build_playlist.sh create <name> <description> <song_ids_file>}"
    IDS_FILE="${4:?Usage: build_playlist.sh create <name> <description> <song_ids_file>}"
    [[ ! -f "$IDS_FILE" ]] && { echo "ERROR: File not found: ${IDS_FILE}" >&2; exit 1; }

    track_count=$(grep -c -v '^\s*$' "$IDS_FILE" 2>/dev/null || echo 0)
    [[ "$track_count" -eq 0 ]] && { echo "ERROR: No song IDs in ${IDS_FILE}" >&2; exit 1; }
    _require_yes "create playlist '${NAME}' with ${track_count} tracks"

    # ── Playlist deduplication: check if a playlist with this name already exists ──
    existing_playlists=$("$SCRIPT_DIR/apple_music_api.sh" library-playlists 100 2>/dev/null || true)
    if [[ -n "$existing_playlists" ]]; then
        existing_id=$(echo "$existing_playlists" | jq -r --arg name "$NAME" \
            '.data[]? | select(.attributes.name == $name) | .id' 2>/dev/null | head -1)
        if [[ -n "$existing_id" ]]; then
            echo "⚠️  A playlist named '${NAME}' already exists (ID: ${existing_id})." >&2
            echo "   Skipping creation. Use 'refresh' to update it, or choose a different name." >&2
            exit 0
        fi
    fi

    echo "🎧 Creating playlist: ${NAME} (${track_count} tracks)" >&2

    # Build tracks array (filter blank/whitespace-only lines)
    tracks_json=$(grep -v '^\s*$' "$IDS_FILE" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | jq -R '{"id": ., "type": "songs"}' | jq -s '.')

    # Build full request
    TMPFILE=$(mktemp "${TMPDIR:-/tmp}/playlist_create_XXXXXX.json")
    trap 'rm -f "$TMPFILE"' EXIT
    jq -n \
      --arg name "$NAME" \
      --arg desc "$DESC" \
      --argjson tracks "$tracks_json" \
      '{
        "attributes": {"name": $name, "description": $desc},
        "relationships": {"tracks": {"data": $tracks}}
      }' > "$TMPFILE"

    if ! "$SCRIPT_DIR/apple_music_api.sh" create-playlist "$TMPFILE" --yes; then
      echo "ERROR: Failed to create playlist '${NAME}'" >&2
      exit 1
    fi

    # Log to playlist history
    if command -v python3 &>/dev/null && [[ -f "$SCRIPT_DIR/playlist_history.py" ]]; then
      (cd "$SCRIPT_DIR" && python3 playlist_history.py log "$NAME" "manual" "$IDS_FILE" 2>/dev/null) || true
    fi
    ;;

  refresh)
    PID="${2:?Usage: build_playlist.sh refresh <playlist_id> <song_ids_file>}"
    IDS_FILE="${3:?Usage: build_playlist.sh refresh <playlist_id> <song_ids_file>}"
    [[ ! -f "$IDS_FILE" ]] && { echo "ERROR: File not found: ${IDS_FILE}" >&2; exit 1; }

    track_count=$(grep -c -v '^\s*$' "$IDS_FILE" 2>/dev/null || echo 0)
    [[ "$track_count" -eq 0 ]] && { echo "ERROR: No song IDs in ${IDS_FILE}" >&2; exit 1; }

    _require_yes "add ${track_count} tracks to playlist ${PID}"
    echo "🎧 Adding ${track_count} tracks to playlist ${PID}" >&2

    tracks_json=$(grep -v '^\s*$' "$IDS_FILE" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | jq -R '{"id": ., "type": "songs"}' | jq -s '.')

    TMPFILE=$(mktemp "${TMPDIR:-/tmp}/playlist_add_XXXXXX.json")
    trap 'rm -f "$TMPFILE"' EXIT
    jq -n --argjson tracks "$tracks_json" '{"data": $tracks}' > "$TMPFILE"

    if ! "$SCRIPT_DIR/apple_music_api.sh" add-to-playlist "$PID" "$TMPFILE" --yes; then
      echo "ERROR: Failed to add tracks to playlist ${PID}" >&2
      exit 1
    fi
    ;;

  remove)
    PID="${2:?Usage: build_playlist.sh remove <playlist_id> <song_ids_file>}"
    IDS_FILE="${3:?Usage: build_playlist.sh remove <playlist_id> <song_ids_file>}"
    [[ ! -f "$IDS_FILE" ]] && { echo "ERROR: File not found: ${IDS_FILE}" >&2; exit 1; }

    track_count=$(grep -c -v '^\s*$' "$IDS_FILE" 2>/dev/null || echo 0)
    [[ "$track_count" -eq 0 ]] && { echo "ERROR: No song IDs in ${IDS_FILE}" >&2; exit 1; }

    _require_yes "remove ${track_count} tracks from playlist ${PID}"
    echo "🎧 Removing ${track_count} tracks from playlist ${PID}" >&2

    tracks_json=$(grep -v '^\s*$' "$IDS_FILE" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | jq -R '{"id": ., "type": "songs"}' | jq -s '.')

    TMPFILE=$(mktemp "${TMPDIR:-/tmp}/playlist_remove_XXXXXX.json")
    trap 'rm -f "$TMPFILE"' EXIT
    jq -n --argjson tracks "$tracks_json" '{"data": $tracks}' > "$TMPFILE"

    if ! "$SCRIPT_DIR/apple_music_api.sh" remove-from-playlist "$PID" "$TMPFILE" --yes; then
      echo "ERROR: Failed to remove tracks from playlist ${PID}" >&2
      exit 1
    fi
    ;;

  *)
    echo "Usage: build_playlist.sh <create|refresh|remove> ... --yes" >&2
    echo "  create <name> <description> <song_ids_file>" >&2
    echo "  refresh <playlist_id> <song_ids_file>" >&2
    echo "  remove <playlist_id> <song_ids_file>" >&2
    exit 1
    ;;
esac
