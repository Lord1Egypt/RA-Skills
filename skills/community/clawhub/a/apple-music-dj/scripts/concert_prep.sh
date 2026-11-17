#!/usr/bin/env bash
# concert_prep.sh — Preview (and, only on request, create) a concert prep playlist for a show.
#
# Fetches the artist's top songs + deep cuts. By default NOTHING is written to Apple Music: the
# proposed playlist (name, description, track list) is printed as JSON on stdout. Re-run the same
# command with --create to build it in the user's library.
#
# Usage:
#   scripts/concert_prep.sh <storefront> <artist_name> [playlist_name] [--create]
#
# Requires: APPLE_MUSIC_DEV_TOKEN and APPLE_MUSIC_USER_TOKEN
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
API="$SCRIPT_DIR/apple_music_api.sh"
USAGE="Usage: concert_prep.sh <storefront> <artist_name> [playlist_name] [--create]"

# --create may appear anywhere; everything else is positional
CREATE=0
POSITIONAL=()
for arg in "$@"; do
  if [[ "$arg" == "--create" ]]; then CREATE=1; else POSITIONAL+=("$arg"); fi
done
set -- "${POSITIONAL[@]+"${POSITIONAL[@]}"}"

SF="${1:?$USAGE}"
ARTIST_QUERY="${2:?$USAGE}"

# ── Find artist ──────────────────────────────────────────────────
echo "🔍 Searching for ${ARTIST_QUERY}..." >&2
search_result=$("$API" search "$SF" "$ARTIST_QUERY" "artists")
artist_id=$(echo "$search_result" | jq -r '.results.artists.data[0].id // empty')
artist_name=$(echo "$search_result" | jq -r '.results.artists.data[0].attributes.name // empty')

if [[ -z "$artist_id" ]]; then
  echo "ERROR: Could not find artist: ${ARTIST_QUERY}" >&2
  exit 1
fi

PLAYLIST_NAME="${3:-Concert Prep · ${artist_name} · $(date +"%b %Y")}"
echo "🎤 Found: ${artist_name} (${artist_id})" >&2

# ── Gather top songs ─────────────────────────────────────────────
echo "📋 Fetching top songs..." >&2
top_result=$("$API" artist-top "$SF" "$artist_id")
top_json=$(echo "$top_result" | jq -c '
  [ (.data[0].views["top-songs"].data // [])[:15][]
    | {id, name: .attributes.name, artist: .attributes.artistName, source: "top_song"} ]
' 2>/dev/null || echo '[]')
echo "  Got $(echo "$top_json" | jq 'length') top songs" >&2

# ── Gather deep cuts from albums ─────────────────────────────────
echo "💿 Fetching discography for deep cuts..." >&2
albums_result=$("$API" artist-albums "$SF" "$artist_id")
album_ids=$(echo "$albums_result" | jq -r '.data[].id' 2>/dev/null | head -5)

candidates='[]'
while IFS= read -r album_id; do
  [[ -z "$album_id" ]] && continue
  album_detail=$("$API" album-tracks "$SF" "$album_id" 2>/dev/null) || continue
  album_tracks=$(echo "$album_detail" | jq -c '
    [ (.data[0].relationships.tracks.data // [])[]
      | {id, name: .attributes.name, artist: .attributes.artistName, source: "deep_cut"} ]
  ' 2>/dev/null || echo '[]')
  candidates=$(jq -c -n --argjson a "$candidates" --argjson b "$album_tracks" '$a + $b')
done <<< "$album_ids"

# Deep cuts: tracks that aren't top songs, first-seen order, deduplicated, at most 10
deep_json=$(echo "$candidates" | jq -c --argjson top "$top_json" '
  ($top | map(.id)) as $topids
  | map(select(.id as $i | $topids | index($i) | not))
  | reduce .[] as $t ([]; if any(.[]; .id == $t.id) then . else . + [$t] end)
  | .[:10]
')
echo "  Got $(echo "$deep_json" | jq 'length') deep cuts" >&2

total=$(jq -n --argjson a "$top_json" --argjson b "$deep_json" '($a | length) + ($b | length)')
if [[ "$total" -eq 0 ]]; then
  echo "ERROR: No tracks found for ${artist_name}" >&2
  exit 1
fi

top_count=$(echo "$top_json" | jq 'length')
deep_count=$(echo "$deep_json" | jq 'length')
DESC="Get ready for ${artist_name} live. ${top_count} essential tracks + ${deep_count} deep cuts to know before the show."

# build_playlist.sh quietly skips (exit 0) when a playlist with this name already exists, so look
# first: both the preview and the result must say so instead of claiming something was created.
name_exists=false
existing=$("$API" library-playlists 100 2>/dev/null \
  | jq -r --arg n "$PLAYLIST_NAME" '[.data[]? | select(.attributes.name == $n)] | length' 2>/dev/null || echo 0)
[[ "${existing:-0}" -gt 0 ]] && name_exists=true

plan=$(jq -n --arg artist "$artist_name" --arg artist_id "$artist_id" --arg name "$PLAYLIST_NAME" \
  --arg desc "$DESC" --argjson top "$top_json" --argjson deep "$deep_json" \
  --argjson name_exists "$name_exists" '
  { artist: $artist, artist_id: $artist_id, playlist_name: $name, description: $desc,
    top_song_count: ($top | length), deep_cut_count: ($deep | length),
    track_count: (($top | length) + ($deep | length)),
    tracks: ($top + $deep), name_exists: $name_exists, created: false }')

# ── Preview only (the default): show the plan, write nothing ─────
if [[ "$CREATE" -ne 1 ]]; then
  echo "$plan"
  echo "" >&2
  echo "👀 Preview only — nothing was added to Apple Music." >&2
  echo "   ${PLAYLIST_NAME} (${total} tracks). To build it, re-run with --create." >&2
  if [[ "$name_exists" == "true" ]]; then
    echo "   ⚠️  A playlist named '${PLAYLIST_NAME}' already exists, so --create would skip it." >&2
    echo "      Pass a different playlist name as the third argument." >&2
  fi
  exit 0
fi

# ── Explicit --create, but the name is taken: don't pretend anything was created ─
if [[ "$name_exists" == "true" ]]; then
  echo "$plan" | jq --arg r "A playlist named \"${PLAYLIST_NAME}\" already exists; nothing was created. Choose another name." \
    '.skipped_reason = $r'
  echo "" >&2
  echo "⚠️  A playlist named '${PLAYLIST_NAME}' already exists — nothing was created." >&2
  exit 0
fi

# ── Create (explicit --create) ───────────────────────────────────
TMPIDS=$(mktemp "${TMPDIR:-/tmp}/concert_ids_XXXXXX.txt")
trap 'rm -f "$TMPIDS"' EXIT
echo "$plan" | jq -r '.tracks[].id' > "$TMPIDS"

echo "🎧 Building playlist: ${PLAYLIST_NAME} (${total} tracks)" >&2
# build_playlist.sh prints the API response; keep stdout to the single plan JSON below
if ! "$SCRIPT_DIR/build_playlist.sh" create "$PLAYLIST_NAME" "$DESC" "$TMPIDS" --yes > /dev/null; then
  echo "ERROR: Failed to create concert prep playlist" >&2
  exit 1
fi

echo "$plan" | jq '.created = true'
echo "" >&2
echo "✅ Concert prep playlist created!" >&2
echo "  ${total} tracks: ${top_count} hits + ${deep_count} deep cuts" >&2
echo "  Listen through before the show 🎤" >&2
