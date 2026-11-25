#!/usr/bin/env bash
# apple_music_api.sh — Complete Apple Music API wrapper
# Every endpoint referenced in SKILL.md is implemented here.
set -euo pipefail

# Testing hook: APPLE_MUSIC_API_BASE may point at a local mock server (tests/mock_api.py).
# Only loopback addresses are accepted so real tokens can never be sent to another host.
BASE="https://api.music.apple.com"
if [[ -n "${APPLE_MUSIC_API_BASE:-}" ]]; then
  if [[ "$APPLE_MUSIC_API_BASE" =~ ^http://(127\.0\.0\.1|localhost)(:[0-9]+)?$ ]]; then
    BASE="$APPLE_MUSIC_API_BASE"
  else
    echo "ERROR: APPLE_MUSIC_API_BASE must be http://127.0.0.1[:port] or http://localhost[:port]" >&2
    exit 1
  fi
fi

# ── Token check ───────────────────────────────────────────────────
require_dev_token() {
  if [[ -z "${APPLE_MUSIC_DEV_TOKEN:-}" ]]; then
    echo "ERROR: APPLE_MUSIC_DEV_TOKEN not set. Run scripts/setup_auth.py, or try scripts/demo.py tour first." >&2; exit 1
  fi
}
require_user_token() {
  require_dev_token
  if [[ -z "${APPLE_MUSIC_USER_TOKEN:-}" ]]; then
    echo "ERROR: APPLE_MUSIC_USER_TOKEN not set. Run scripts/setup_auth.py, or try scripts/demo.py tour first." >&2; exit 1
  fi
}

# ── Temp-file hygiene ─────────────────────────────────────────────
# No RETURN traps: bash 4+/5 keeps them armed after the function that set them
# returns, so they fire again in the caller where the function's locals no longer
# exist (an unbound-variable error under `set -u`) — and one helper's trap silently
# replaced another's, leaving the token-bearing curl config behind. Instead every
# helper removes its own temp files right after use; the EXIT / INT / TERM traps are
# only the backstop for interrupts. Read commands run as `_get | jq` in a subshell,
# where bash resets traps, so _with_auth re-installs them.
#
# Every temp file is named am_<kind>_<script pid>_XXXXXX (`$$` stays the main script's
# pid inside subshells) and the backstop removes those exact kinds for this pid instead of
# keeping a list: a signal that lands right after mktemp but before a list append would otherwise
# leak the file, because bash runs a pending trap before the next command.
_CURL_PID=""
_cleanup() {
  # `if`, not `cmd && kill`: under `set -e` a failing last `&&` element (curl already dead)
  # would abort the EXIT trap and replace the real exit status with 1.
  if [[ -n "${_CURL_PID:-}" ]]; then
    kill "$_CURL_PID" 2>/dev/null || true
  fi
  rm -f "${TMPDIR:-/tmp}"/am_api_$$_* "${TMPDIR:-/tmp}"/am_auth_$$_* "${TMPDIR:-/tmp}"/am_code_$$_* \
        "${TMPDIR:-/tmp}"/am_rate_$$_* 2>/dev/null || true
  return 0
}
_install_traps() {
  trap _cleanup EXIT
  trap '_cleanup; exit 130' INT
  trap '_cleanup; exit 143' TERM
}
_install_traps

# ── HTTP helpers ──────────────────────────────────────────────────
_retry() {
  # Retry a curl command with exponential backoff on 429 responses.
  # Usage: _retry curl_args...
  #
  # curl runs in the background and we `wait` for it: bash defers traps until the
  # current foreground command finishes, so with a plain `$(curl ...)` a Ctrl-C/TERM
  # that curl happens to miss (e.g. it lands while curl is still being forked) would
  # not be acted on until the whole request completed. `wait` is interrupted at once.
  local max_retries=3
  local delay=1
  local attempt=0
  local rc=0
  local tmpfile codefile
  # Stay inside call_api's 30 s budget: curl is bounded below, and no retry starts past this.
  local deadline=$(( SECONDS + 25 ))
  tmpfile=$(mktemp "${TMPDIR:-/tmp}/am_api_$$_XXXXXX")
  codefile=$(mktemp "${TMPDIR:-/tmp}/am_code_$$_XXXXXX")

  while (( attempt <= max_retries )); do
    local http_code
    local curl_exit=0
    # No attempt may outlast the deadline: each gets at most 20 s, less whatever is left
    local budget=$(( deadline - SECONDS ))
    (( budget > 20 )) && budget=20
    if (( budget < 1 )); then
      echo "ERROR: request timed out (rate limited too long). Try again shortly." >&2
      rc=1
      break
    fi
    curl -sS -g --connect-timeout "$(( budget < 10 ? budget : 10 ))" --max-time "$budget" -o "$tmpfile" -w '%{http_code}' "$@" > "$codefile" &
    _CURL_PID=$!
    wait "$_CURL_PID" || curl_exit=$?
    _CURL_PID=""
    # Exit >= 128 means curl was ended by a signal, or `wait` was interrupted by a trapped
    # one (bash runs that trap only after the next commands). Don't report it as a network
    # failure — clean up and exit with the signal's status.
    if (( curl_exit >= 128 )); then
      _cleanup
      exit "$curl_exit"
    fi
    http_code=$(cat "$codefile")
    if [[ $curl_exit -ne 0 && "$http_code" != "429" ]]; then
      echo "ERROR: curl failed (exit $curl_exit). Check network connectivity." >&2
      rc=1
      break
    fi
    if [[ "$http_code" == "429" && attempt -lt max_retries && $(( SECONDS + delay + 1 )) -lt deadline ]]; then
      (( attempt++ ))
      echo "WARN: Rate limited (429). Retrying in ${delay}s (attempt ${attempt}/${max_retries})..." >&2
      sleep "$delay"
      (( delay *= 2 ))
    else
      cat "$tmpfile"
      [[ "$http_code" =~ ^[45] ]] && rc=1
      break
    fi
  done
  rm -f "$tmpfile" "$codefile"
  return "$rc"
}

_make_auth_config() {
  # Write tokens to a curl config file so they don't appear in ps output.
  local cfgfile
  cfgfile=$(mktemp "${TMPDIR:-/tmp}/am_auth_$$_XXXXXX")
  chmod 600 "$cfgfile"
  if [[ -n "${2:-}" ]]; then
    printf -- '-H "Authorization: Bearer %s"\n-H "Music-User-Token: %s"\n' "$1" "$2" > "$cfgfile"
  else
    printf -- '-H "Authorization: Bearer %s"\n' "$1" > "$cfgfile"
  fi
  echo "$cfgfile"
}

_with_auth() {
  # Usage: _with_auth <dev|both> <curl args...>
  # Runs _retry with a temporary auth config that is always removed afterwards.
  local mode="$1"; shift
  local cfg rc=0
  _install_traps
  if [[ "$mode" == "both" ]]; then
    cfg=$(_make_auth_config "$APPLE_MUSIC_DEV_TOKEN" "$APPLE_MUSIC_USER_TOKEN")
  else
    cfg=$(_make_auth_config "$APPLE_MUSIC_DEV_TOKEN")
  fi
  _retry -K "$cfg" "$@" || rc=$?
  rm -f "$cfg"
  return "$rc"
}

_get() {
  # Personalized request (both tokens)
  require_user_token
  _with_auth both "${BASE}${1}"
}

_get_catalog() {
  # Catalog-only request (dev token only)
  require_dev_token
  _with_auth dev "${BASE}${1}"
}

_post() {
  require_user_token
  _with_auth both -X POST -H "Content-Type: application/json" -d "${2}" "${BASE}${1}"
}

_post_file() {
  require_user_token
  _with_auth both -X POST -H "Content-Type: application/json" -d @"${2}" "${BASE}${1}"
}

_post_empty() {
  # POST with no body (both tokens)
  require_user_token
  _with_auth both -X POST "${BASE}${1}"
}

_put_file() {
  # PUT with a JSON body file (both tokens)
  require_user_token
  _with_auth both -X PUT -H "Content-Type: application/json" -d @"${2}" "${BASE}${1}"
}

_delete() {
  # DELETE request with JSON body (both tokens)
  require_user_token
  _with_auth both -X DELETE -H "Content-Type: application/json" -d @"${2}" "${BASE}${1}"
}

_delete_no_body() {
  # DELETE request without body (both tokens)
  require_user_token
  _with_auth both -X DELETE "${BASE}${1}"
}

_urlencode() {
  jq -sRr @uri <<< "$1"
}

# ── Commands ──────────────────────────────────────────────────────

cmd_verify() {
  require_user_token
  echo "Verifying developer token..." >&2
  if _get_catalog "/v1/storefronts/us" | jq -e '.data[0].id' >/dev/null 2>&1; then
    echo "  ✅ Developer token valid" >&2
  else
    echo "  ❌ Developer token failed — regenerate JWT" >&2; exit 1
  fi
  echo "Verifying user token..." >&2
  if _get "/v1/me/recent/played/tracks?limit=1" | jq -e '.data' >/dev/null 2>&1; then
    echo "  ✅ Music User Token valid" >&2
  else
    echo "  ❌ Music User Token failed (expired? renew it: python3 scripts/setup_auth.py)" >&2; exit 1
  fi
  echo "Both tokens verified. 🎧" >&2
}

cmd_user_storefront() {
  # Detect storefront from the user's account
  require_user_token
  local resp
  resp=$(_get "/v1/me/storefront" 2>/dev/null) || true
  local sf
  sf=$(echo "$resp" | jq -r '.data[0].id // empty' 2>/dev/null)
  if [[ -n "$sf" ]]; then
    echo "$sf"
  else
    echo "us"  # fallback
    echo "WARN: Could not detect storefront, defaulting to 'us'" >&2
  fi
}

_page_failed() {
  # A page failed mid-listing. Nothing fetched yet: fail. Otherwise keep what we have, but say it is partial.
  local offset="$1" response="${2:-}"
  echo "ERROR: request failed at item ${offset}: ${response:0:300}${response:-no response body}" >&2
  [[ "$offset" -eq 0 ]] && return 1
  echo "WARN: stopped at item ${offset} after a failed request; results are partial." >&2
}

cmd_recent_tracks() {
  # Paginate through all 50 available recent tracks
  require_user_token
  local all="[]"
  for offset in 0 10 20 30 40; do
    local page
    page=$(_get "/v1/me/recent/played/tracks?types=songs&limit=10&offset=${offset}") || { _page_failed "$offset" "${page:-}" || return 1; break; }
    local data
    data=$(echo "$page" | jq -c '.data // []')
    [[ "$data" == "[]" ]] && break
    all=$(echo "$all" "$data" | jq -s '.[0] + .[1]')
  done
  echo "$all" | jq .
}

cmd_recent_played() {
  _get "/v1/me/recent/played?limit=10" | jq .
}

cmd_heavy_rotation() {
  _get "/v1/me/history/heavy-rotation?limit=10" | jq .
}

cmd_ratings() {
  local rtype="${1:-songs}"  # songs, albums, playlists, music-videos
  case "$rtype" in
    songs|albums|playlists|music-videos) ;;
    *) echo "ERROR: Invalid rating type: $rtype (allowed: songs, albums, playlists, music-videos)" >&2; return 1 ;;
  esac
  _get "/v1/me/ratings/${rtype}?limit=100" | jq .
}

cmd_library_artists() {
  local limit="${1:-25}"
  [[ "$limit" =~ ^[0-9]+$ ]] || { echo "ERROR: limit must be a number" >&2; return 1; }
  local all="[]"
  local offset=0
  while true; do
    local page
    page=$(_get "/v1/me/library/artists?limit=${limit}&offset=${offset}") || { _page_failed "$offset" "${page:-}" || return 1; break; }
    local data
    data=$(echo "$page" | jq -c '.data // []')
    [[ "$data" == "[]" ]] && break
    all=$(echo "$all" "$data" | jq -s '.[0] + .[1]')
    local count
    count=$(echo "$data" | jq 'length')
    [[ "$count" -lt "$limit" ]] && break
    offset=$((offset + limit))
    if [[ $offset -ge 500 ]]; then  # safety cap
      echo "NOTE: stopped at ${offset} items; the library may have more, so results cover only the first ${offset}." >&2
      break
    fi
  done
  echo "$all" | jq '{"data": .}'
}

cmd_library_songs() {
  local limit="${1:-25}"
  [[ "$limit" =~ ^[0-9]+$ ]] || { echo "ERROR: limit must be a number" >&2; return 1; }
  local all="[]"
  local offset=0
  while true; do
    local page
    page=$(_get "/v1/me/library/songs?limit=${limit}&offset=${offset}&include=catalog" ) || { _page_failed "$offset" "${page:-}" || return 1; break; }
    local data
    data=$(echo "$page" | jq -c '.data // []')
    [[ "$data" == "[]" ]] && break
    all=$(echo "$all" "$data" | jq -s '.[0] + .[1]')
    local count
    count=$(echo "$data" | jq 'length')
    [[ "$count" -lt "$limit" ]] && break
    offset=$((offset + limit))
    if [[ $offset -ge 500 ]]; then  # safety cap
      echo "NOTE: stopped at ${offset} items; the library may have more, so results cover only the first ${offset}." >&2
      break
    fi
  done
  echo "$all" | jq '{"data": .}'
}

cmd_recommendations() {
  _get "/v1/me/recommendations?limit=10" | jq .
}

cmd_replay_summary() {
  local year="${1:-}"
  local endpoint="/v1/me/music-summaries"
  [[ -n "$year" ]] && endpoint="${endpoint}?filter[year]=${year}"
  _get "$endpoint" | jq .
}

cmd_replay_milestones() {
  local year="${1:-}"
  local endpoint="/v1/me/music-summaries/milestones"
  [[ -n "$year" ]] && endpoint="${endpoint}?filter[year]=${year}"
  _get "$endpoint" | jq .
}

cmd_search() {
  local sf="${1:?Usage: search <storefront> <query> [types]}"
  local query="${2:?Usage: search <storefront> <query> [types]}"
  local types="${3:-songs,artists,albums}"
  [[ "$sf" =~ ^[a-z]{2}$ ]] || { echo "ERROR: Invalid storefront code: $sf" >&2; return 1; }
  local encoded
  encoded=$(_urlencode "$query")
  _get_catalog "/v1/catalog/${sf}/search?term=${encoded}&types=${types}&limit=25" | jq .
}

cmd_charts() {
  local sf="${1:?Usage: charts <storefront> [genre_id]}"
  local genre=""
  [[ -n "${2:-}" ]] && genre="&genre=${2}"
  _get_catalog "/v1/catalog/${sf}/charts?types=songs,albums&limit=25${genre}" | jq .
}

cmd_artist_albums() {
  local sf="${1:?Usage: artist-albums <storefront> <artist_id>}"
  local id="${2:?Usage: artist-albums <storefront> <artist_id>}"
  _get_catalog "/v1/catalog/${sf}/artists/${id}/albums?limit=25" | jq .
}

cmd_artist_top() {
  local sf="${1:?Usage: artist-top <storefront> <artist_id>}"
  local id="${2:?Usage: artist-top <storefront> <artist_id>}"
  _get_catalog "/v1/catalog/${sf}/artists/${id}?views=top-songs" | jq .
}

cmd_artist_detail() {
  local sf="${1:?Usage: artist-detail <storefront> <artist_id>}"
  local id="${2:?Usage: artist-detail <storefront> <artist_id>}"
  _get_catalog "/v1/catalog/${sf}/artists/${id}?include=albums,genres" | jq .
}

cmd_album_tracks() {
  local sf="${1:?Usage: album-tracks <storefront> <album_id>}"
  local id="${2:?Usage: album-tracks <storefront> <album_id>}"
  _get_catalog "/v1/catalog/${sf}/albums/${id}?include=tracks" | jq .
}

cmd_song_detail() {
  local sf="${1:?Usage: song-detail <storefront> <song_id>}"
  local id="${2:?Usage: song-detail <storefront> <song_id>}"
  _get_catalog "/v1/catalog/${sf}/songs/${id}?include=artists,albums" | jq .
}

cmd_catalog_playlist() {
  local sf="${1:?Usage: catalog-playlist <storefront> <playlist_id>}"
  local id="${2:?Usage: catalog-playlist <storefront> <playlist_id>}"
  [[ "$sf" =~ ^[a-z]{2}$ ]] || { echo "ERROR: Invalid storefront code: $sf" >&2; return 1; }
  [[ "$id" =~ ^pl\.[A-Za-z0-9_-]+$ ]] || { echo "ERROR: Invalid catalog playlist ID: $id (expected pl.…)" >&2; return 1; }
  _get_catalog "/v1/catalog/${sf}/playlists/${id}?include=tracks" | jq .
}

cmd_catalog_playlist_tracks() {
  local sf="${1:?Usage: catalog-playlist-tracks <storefront> <playlist_id> [offset]}"
  local id="${2:?Usage: catalog-playlist-tracks <storefront> <playlist_id> [offset]}"
  local offset="${3:-0}"
  [[ "$sf" =~ ^[a-z]{2}$ ]] || { echo "ERROR: Invalid storefront code: $sf" >&2; return 1; }
  [[ "$id" =~ ^pl\.[A-Za-z0-9_-]+$ ]] || { echo "ERROR: Invalid catalog playlist ID: $id (expected pl.…)" >&2; return 1; }
  [[ "$offset" =~ ^[0-9]+$ ]] || { echo "ERROR: Invalid offset: $offset" >&2; return 1; }
  _get_catalog "/v1/catalog/${sf}/playlists/${id}/tracks?limit=100&offset=${offset}" | jq .
}

cmd_genres() {
  local sf="${1:?Usage: genres <storefront>}"
  [[ "$sf" =~ ^[a-z]{2}$ ]] || { echo "ERROR: Invalid storefront code: $sf" >&2; return 1; }
  _get_catalog "/v1/catalog/${sf}/genres" | jq .
}

cmd_library_playlists() {
  local limit="${1:-25}"
  _get "/v1/me/library/playlists?limit=${limit}" | jq .
}

cmd_playlist_tracks() {
  local pid="${1:?Usage: playlist-tracks <playlist_library_id>}"
  _get "/v1/me/library/playlists/${pid}/tracks?limit=100" | jq .
}

# Every command that changes the user's account calls _confirm first. Without a trailing --yes
# it only says what it WOULD do and exits 3, so a stray call can never edit a library.
CONFIRMED=0
_confirm() {
  [[ "$CONFIRMED" == "1" ]] && return 0
  echo "WOULD $1 — preview only, nothing was changed. Re-run with --yes to apply." >&2
  exit 3
}

cmd_create_playlist() {
  local json_file="${1:?Usage: create-playlist <json_file>}"
  [[ ! -f "$json_file" ]] && { echo "ERROR: File not found: ${json_file}" >&2; exit 1; }
  _confirm "create a playlist from ${json_file}"
  echo "Creating playlist..." >&2
  local resp
  resp=$(_post_file "/v1/me/library/playlists" "$json_file")
  echo "$resp" | jq .
  local name
  name=$(echo "$resp" | jq -r '.data[0].attributes.name // "Unknown"')
  echo "✅ Playlist '${name}' created in Apple Music!" >&2
}

cmd_add_to_playlist() {
  local pid="${1:?Usage: add-to-playlist <playlist_id> <json_file>}"
  local json_file="${2:?Usage: add-to-playlist <playlist_id> <json_file>}"
  [[ ! -f "$json_file" ]] && { echo "ERROR: File not found: ${json_file}" >&2; exit 1; }
  _confirm "add tracks to playlist ${pid}"
  echo "Adding tracks to playlist ${pid}..." >&2
  _post_file "/v1/me/library/playlists/${pid}/tracks" "$json_file"
  echo "✅ Tracks added." >&2
}

cmd_remove_from_playlist() {
  local pid="${1:?Usage: remove-from-playlist <playlist_id> <json_file>}"
  local json_file="${2:?Usage: remove-from-playlist <playlist_id> <json_file>}"
  [[ ! -f "$json_file" ]] && { echo "ERROR: File not found: ${json_file}" >&2; exit 1; }
  _confirm "remove tracks from playlist ${pid}"
  echo "Removing tracks from playlist ${pid}..." >&2
  _delete "/v1/me/library/playlists/${pid}/tracks" "$json_file"
  echo "✅ Tracks removed." >&2
}

_validate_ids() {
  # Catalog/library IDs: letters, digits, dots and underscores, comma-separated
  [[ "$1" =~ ^[A-Za-z0-9._]+(,[A-Za-z0-9._]+)*$ ]] || { echo "ERROR: invalid ID list: $1" >&2; return 1; }
}

cmd_similar_artists() {
  local sf="${1:?Usage: similar-artists <storefront> <artist_id>}"
  local id="${2:?Usage: similar-artists <storefront> <artist_id>}"
  [[ "$sf" =~ ^[a-z]{2}$ ]] || { echo "ERROR: Invalid storefront code: $sf" >&2; return 1; }
  _validate_ids "$id" || return 1
  _get_catalog "/v1/catalog/${sf}/artists/${id}/view/similar-artists?limit=20" | jq .
}

cmd_add_to_library() {
  local type="${1:?Usage: add-to-library <albums|songs> <id,id,...>}"
  local ids="${2:?Usage: add-to-library <albums|songs> <id,id,...>}"
  [[ "$type" == "albums" || "$type" == "songs" ]] || { echo "ERROR: type must be albums or songs" >&2; return 1; }
  _validate_ids "$ids" || return 1
  _confirm "add ${type} ${ids} to your library"
  _post_empty "/v1/me/library?ids[${type}]=${ids}"
  echo "✅ Added ${type} to library." >&2
}

cmd_recently_added() {
  local limit="${1:-25}"
  [[ "$limit" =~ ^[0-9]+$ ]] || { echo "ERROR: limit must be a number" >&2; return 1; }
  _get "/v1/me/library/recently-added?limit=${limit}" | jq .
}

cmd_recent_stations() {
  _get "/v1/me/recent/radio-stations?limit=10" | jq .
}

cmd_songs_by_isrc() {
  local sf="${1:?Usage: songs-by-isrc <storefront> <isrc,isrc,...>}"
  local isrcs="${2:?Usage: songs-by-isrc <storefront> <isrc,isrc,...>}"
  [[ "$sf" =~ ^[a-z]{2}$ ]] || { echo "ERROR: Invalid storefront code: $sf" >&2; return 1; }
  [[ "$isrcs" =~ ^[A-Z]{2}[A-Z0-9]{3}[0-9]{7}(,[A-Z]{2}[A-Z0-9]{3}[0-9]{7}){0,24}$ ]] \
    || { echo "ERROR: expected 1-25 comma-separated ISRCs" >&2; return 1; }
  _get_catalog "/v1/catalog/${sf}/songs?filter[isrc]=${isrcs}" | jq .
}

cmd_favorite() {
  local type="${1:?Usage: favorite <songs|albums|artists|playlists> <id,id,...>}"
  local ids="${2:?Usage: favorite <songs|albums|artists|playlists> <id,id,...>}"
  [[ "$type" =~ ^(songs|albums|artists|playlists)$ ]] || { echo "ERROR: invalid type: $type" >&2; return 1; }
  _validate_ids "$ids" || return 1
  _confirm "add ${type} ${ids} to your favorites"
  _post_empty "/v1/me/favorites?ids[${type}]=${ids}"
  echo "✅ Added ${type} to favorites." >&2
}

cmd_rate() {
  local id="${1:?Usage: rate <song_id> <1|-1>}"
  local value="${2:?Usage: rate <song_id> <1|-1>}"
  [[ "$value" == "1" || "$value" == "-1" ]] || { echo "ERROR: value must be 1 or -1" >&2; return 1; }
  _validate_ids "$id" || return 1
  _confirm "set your rating of song ${id} to ${value}"
  local tmpfile rc=0
  tmpfile=$(mktemp "${TMPDIR:-/tmp}/am_rate_$$_XXXXXX")
  printf '{"type":"rating","attributes":{"value":%s}}' "$value" > "$tmpfile"
  _put_file "/v1/me/ratings/songs/${id}" "$tmpfile" || rc=$?
  rm -f "$tmpfile"
  return "$rc"
}

cmd_unrate() {
  local id="${1:?Usage: unrate <song_id>}"
  _validate_ids "$id" || return 1
  _confirm "remove your rating of song ${id}"
  _delete_no_body "/v1/me/ratings/songs/${id}"
}

# ── Dispatch ──────────────────────────────────────────────────────
cmd="${1:-help}"; shift 2>/dev/null || true
_args=()
for _a in "$@"; do
  if [[ "$_a" == "--yes" ]]; then CONFIRMED=1; else _args+=("$_a"); fi
done
set -- ${_args[@]+"${_args[@]}"}

case "$cmd" in
  verify)            cmd_verify ;;
  user-storefront)   cmd_user_storefront ;;
  recent-tracks)     cmd_recent_tracks ;;
  recent-played)     cmd_recent_played ;;
  heavy-rotation)    cmd_heavy_rotation ;;
  ratings)           cmd_ratings "$@" ;;
  library-artists)   cmd_library_artists "$@" ;;
  library-songs)     cmd_library_songs "$@" ;;
  recommendations)   cmd_recommendations ;;
  replay-summary)    cmd_replay_summary "$@" ;;
  replay-milestones) cmd_replay_milestones "$@" ;;
  search)            cmd_search "$@" ;;
  charts)            cmd_charts "$@" ;;
  artist-albums)     cmd_artist_albums "$@" ;;
  artist-top)        cmd_artist_top "$@" ;;
  artist-detail)     cmd_artist_detail "$@" ;;
  album-tracks)      cmd_album_tracks "$@" ;;
  song-detail)       cmd_song_detail "$@" ;;
  genres)            cmd_genres "$@" ;;
  catalog-playlist)  cmd_catalog_playlist "$@" ;;
  catalog-playlist-tracks) cmd_catalog_playlist_tracks "$@" ;;
  library-playlists) cmd_library_playlists "$@" ;;
  playlist-tracks)   cmd_playlist_tracks "$@" ;;
  create-playlist)   cmd_create_playlist "$@" ;;
  add-to-playlist)   cmd_add_to_playlist "$@" ;;
  remove-from-playlist) cmd_remove_from_playlist "$@" ;;
  similar-artists)   cmd_similar_artists "$@" ;;
  add-to-library)    cmd_add_to_library "$@" ;;
  recently-added)    cmd_recently_added "$@" ;;
  recent-stations)   cmd_recent_stations ;;
  songs-by-isrc)     cmd_songs_by_isrc "$@" ;;
  favorite)          cmd_favorite "$@" ;;
  rate)              cmd_rate "$@" ;;
  unrate)            cmd_unrate "$@" ;;
  help|*)
    cat <<'EOF'
Apple Music DJ — API Wrapper

Usage: apple_music_api.sh <command> [args...]

Personalized (require both tokens):
  verify                              Validate tokens
  user-storefront                     Detect user's storefront
  recent-tracks                       Recently played (up to 50 tracks)
  recent-played                       Recently played resources
  heavy-rotation                      Heavy rotation albums/playlists
  ratings [type]                      Loved/disliked (songs|albums|playlists)
  library-artists [limit]             Library artists
  library-songs [limit]               Library songs (with catalog IDs)
  library-playlists [limit]           Library playlists
  recommendations                     Personalized recommendations
  replay-summary [year]               Replay / Music Summaries
  replay-milestones [year]            Replay milestones
  playlist-tracks <playlist_id>       Tracks in a library playlist
  create-playlist <json_file>         Create playlist from JSON spec (writes! needs --yes)
  add-to-playlist <id> <json_file>    Add tracks to existing playlist (writes! needs --yes)
  remove-from-playlist <id> <json>    Remove tracks from playlist (writes! needs --yes)
  recently-added [limit]              Recently added library items
  recent-stations                     Recently played radio stations
  add-to-library <type> <ids>         Add albums|songs to library (writes! needs --yes)
  favorite <type> <ids>               Add resources to favorites (writes! needs --yes)
  rate <song_id> <1|-1>               Love/dislike a song (writes! needs --yes)
  unrate <song_id>                    Remove a song rating (writes! needs --yes)

Catalog (require dev token only):
  search <storefront> <query> [types] Search catalog
  charts <storefront> [genre_id]      Top charts
  artist-albums <storefront> <id>     Artist discography
  artist-top <storefront> <id>        Artist top songs
  artist-detail <storefront> <id>     Artist info with albums & genres
  album-tracks <storefront> <id>      Album with track listing
  song-detail <storefront> <id>       Song with artist & album info
  genres <storefront>                  List all genre categories
  catalog-playlist <storefront> <id>  An Apple Music (catalog) playlist with its tracks
  catalog-playlist-tracks <sf> <id> [offset]  The next page of a long playlist's tracks
  similar-artists <storefront> <id>   Artists similar to an artist
  songs-by-isrc <storefront> <isrcs>  Look up songs by ISRC (max 25)
EOF
    ;;
esac
