#!/usr/bin/env bash
# agent-radio CLI
# Usage: radio <command> [args]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${AGENT_RADIO_BASE_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
PREF_FILE="${AGENT_RADIO_PREF_FILE:-$BASE_DIR/preferences.json}"
STATIONS_FILE="${AGENT_RADIO_STATIONS_FILE:-$BASE_DIR/stations.json}"

mkdir -p "$(dirname "$PREF_FILE")"

DEFAULT_PREFS='{"last_station":"","volume":80,"favorites":[],"audio_device":"auto","current_pid":null,"paused":false}'

require_bin() {
  local bin="$1"
  local label="$2"

  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "Error: $label requires '$bin' to be installed."
    return 1
  fi
}

ensure_pref_file() {
  if [[ ! -f "$PREF_FILE" ]]; then
    printf '%s\n' "$DEFAULT_PREFS" > "$PREF_FILE"
  fi
}

load_prefs() {
  ensure_pref_file
  jq -c '.' "$PREF_FILE"
}

save_prefs() {
  printf '%s\n' "$1" > "$PREF_FILE"
}

refresh_prefs() {
  prefs_json="$(load_prefs)"
  last_station="$(jq -r '.last_station // ""' <<< "$prefs_json")"
  volume="$(jq -r '.volume // 80' <<< "$prefs_json")"
  favorites="$(jq -c '.favorites // []' <<< "$prefs_json")"
  audio_device="$(jq -r '.audio_device // "auto"' <<< "$prefs_json")"
  current_pid="$(jq -r '.current_pid // empty' <<< "$prefs_json")"
  paused="$(jq -r '.paused // false' <<< "$prefs_json")"
}

persist_prefs() {
  save_prefs "$prefs_json"
  refresh_prefs
}

detect_audio_device() {
  case "$(uname -s)" in
    Darwin) echo "coreaudio/BuiltInSpeakerDevice" ;;
    Linux) echo "alsa/default" ;;
    MINGW*|MSYS*|CYGWIN*) echo "directsound/default" ;;
    *) echo "auto" ;;
  esac
}

pid_is_running() {
  local pid="${1:-}"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

player_command() {
  local pid="${1:-}"

  if [[ -z "$pid" ]]; then
    return 1
  fi

  ps -p "$pid" -o comm= 2>/dev/null | tr -d '[:space:]'
}

resolve_station_url() {
  local input="${1:-}"
  local normalized matches url

  if [[ -z "$input" ]]; then
    return 1
  fi

  if [[ "$input" =~ ^https?:// ]]; then
    printf '%s\n' "$input"
    return 0
  fi

  normalized="$(tr '[:upper:]' '[:lower:]' <<< "$input")"
  matches="$(
    {
      jq -c '.[]?' <<< "$favorites"
      if [[ -f "$STATIONS_FILE" ]]; then
        jq -c '.[]?' "$STATIONS_FILE" 2>/dev/null || true
      fi
    } | jq -r --arg n "$normalized" '
      select((.name // "" | ascii_downcase) == $n) | .url
    ' | head -n 1
  )"

  if [[ -n "$matches" ]]; then
    printf '%s\n' "$matches"
    return 0
  fi

  return 1
}

random_station_url() {
  if [[ -f "$STATIONS_FILE" ]]; then
    jq -r '.[].url' "$STATIONS_FILE" 2>/dev/null | awk 'NF' | shuf -n 1
    return 0
  fi

  return 1
}

stop_playback() {
  refresh_prefs

  if pid_is_running "$current_pid"; then
    kill "$current_pid" 2>/dev/null || true
    wait "$current_pid" 2>/dev/null || true
  fi

  prefs_json="$(jq '.current_pid = null | .paused = false' <<< "$prefs_json")"
  persist_prefs
}

cmd_play() {
  local input="${1:-}"
  local vol="${2:-$volume}"
  local url dev new_pid

  if [[ ! "$vol" =~ ^[0-9]+$ ]] || (( vol < 0 || vol > 100 )); then
    echo "Volume must be 0-100"
    return 1
  fi

  if [[ -z "$input" ]]; then
    url="$(random_station_url || true)"
    if [[ -z "$url" ]]; then
      echo "No built-in stations available. Provide a station name or direct URL."
      return 1
    fi
    echo "Random station: $url"
  elif ! url="$(resolve_station_url "$input")"; then
    echo "Station '$input' not found in favorites or built-in list."
    echo "Use a direct URL, run 'find <query>', or add it to favorites first."
    return 1
  fi

  stop_playback

  dev="$audio_device"
  if [[ "$dev" == "auto" ]]; then
    dev="$(detect_audio_device)"
  fi

  if command -v mpv >/dev/null 2>&1; then
    mpv --no-video --audio-device="$dev" --volume="$vol" --cache=yes "$url" >/dev/null 2>&1 &
    new_pid=$!
  elif command -v ffplay >/dev/null 2>&1; then
    ffplay -nodisp -autoexit "$url" >/dev/null 2>&1 &
    new_pid=$!
  else
    echo "Error: Neither mpv nor ffplay found. Install mpv or ffmpeg/ffplay first."
    return 1
  fi

  prefs_json="$(jq --arg s "$url" --argjson p "$new_pid" --argjson v "$vol" \
    '.last_station = $s | .current_pid = $p | .volume = $v | .paused = false' <<< "$prefs_json")"
  persist_prefs

  echo "Playing: $url (PID $new_pid, volume $vol%)"
}

cmd_stop() {
  stop_playback
  echo "Stopped."
}

cmd_pause() {
  local signal state

  refresh_prefs

  if ! pid_is_running "$current_pid"; then
    prefs_json="$(jq '.current_pid = null | .paused = false' <<< "$prefs_json")"
    persist_prefs
    echo "Nothing playing."
    return 0
  fi

  if [[ "$paused" == "true" ]]; then
    signal="CONT"
    state="resumed"
    prefs_json="$(jq '.paused = false' <<< "$prefs_json")"
  else
    signal="STOP"
    state="paused"
    prefs_json="$(jq '.paused = true' <<< "$prefs_json")"
  fi

  kill "-SIG$signal" "$current_pid" 2>/dev/null || {
    echo "Pause/resume is not supported for the current player on this platform."
    return 1
  }

  persist_prefs
  echo "Playback $state."
}

cmd_next() {
  local next_url

  refresh_prefs

  next_url="$(
    jq -r --arg current "$last_station" '
      if length == 0 then
        empty
      else
        map(.url) as $urls
        | ($urls | index($current)) as $idx
        | if $idx == null then $urls[0] else $urls[(($idx + 1) % ($urls | length))] end
      end
    ' <<< "$favorites"
  )"

  if [[ -z "$next_url" ]]; then
    echo "No favorites. Add some with: favorite add <name> <url>"
    return 0
  fi

  cmd_play "$next_url"
}

cmd_volume() {
  local vol player

  if [[ $# -eq 0 ]]; then
    echo "Current volume: ${volume}%"
    return 0
  fi

  vol="$1"
  if [[ ! "$vol" =~ ^[0-9]+$ ]] || (( vol < 0 || vol > 100 )); then
    echo "Volume must be 0-100"
    return 1
  fi

  prefs_json="$(jq --argjson v "$vol" '.volume = $v' <<< "$prefs_json")"
  persist_prefs

  player="$(player_command "$current_pid" || true)"
  if [[ "$player" == "mpv" ]]; then
    echo "Volume set to ${vol}%. Restart playback if the current stream does not pick up the new level."
  else
    echo "Volume set to ${vol}% for the next playback session."
  fi
}

cmd_favorite() {
  local subcmd="${1:-}"
  local name url before_count after_count

  shift || true

  case "$subcmd" in
    add)
      name="${1:-}"
      url="${2:-}"

      if [[ -z "$name" || -z "$url" ]]; then
        echo "Usage: favorite add <name> <url>"
        return 1
      fi

      if ! [[ "$url" =~ ^https?:// ]]; then
        echo "Favorite URL must start with http:// or https://"
        return 1
      fi

      if jq -e --arg n "$name" '.[] | select((.name // "") == $n)' <<< "$favorites" >/dev/null; then
        echo "Station '$name' already in favorites."
        return 0
      fi

      favorites="$(jq -c --arg n "$name" --arg u "$url" '. + [{"name": $n, "url": $u}]' <<< "$favorites")"
      prefs_json="$(jq --argjson f "$favorites" '.favorites = $f' <<< "$prefs_json")"
      persist_prefs
      echo "Added '$name' to favorites."
      ;;
    remove)
      name="${1:-}"

      if [[ -z "$name" ]]; then
        echo "Usage: favorite remove <name>"
        return 1
      fi

      before_count="$(jq 'length' <<< "$favorites")"
      favorites="$(jq -c --arg n "$name" 'map(select((.name // "") != $n))' <<< "$favorites")"
      after_count="$(jq 'length' <<< "$favorites")"
      prefs_json="$(jq --argjson f "$favorites" '.favorites = $f' <<< "$prefs_json")"
      persist_prefs

      if [[ "$before_count" == "$after_count" ]]; then
        echo "Station '$name' was not in favorites."
      else
        echo "Removed '$name' from favorites."
      fi
      ;;
    *)
      echo "Usage: favorite add <name> <url> | remove <name>"
      return 1
      ;;
  esac
}

cmd_list() {
  echo "Favorites:"
  if [[ "$(jq 'length' <<< "$favorites")" -eq 0 ]]; then
    echo "  (none)"
  else
    jq -r '.[] | "  \(.name): \(.url)"' <<< "$favorites"
  fi

  if [[ -f "$STATIONS_FILE" ]]; then
    echo ""
    echo "Built-in stations:"
    jq -r '.[] | "  \(.name): \(.url)"' "$STATIONS_FILE" 2>/dev/null || true
  fi
}

cmd_now() {
  local status="Stopped"

  refresh_prefs

  if pid_is_running "$current_pid"; then
    if [[ "$paused" == "true" ]]; then
      status="Paused"
    else
      status="Playing"
    fi
  fi

  echo "Now playing:"
  echo "  Station: ${last_station:-"(none)"}"
  echo "  Volume: $volume%"
  echo "  PID: ${current_pid:-"(none)"}"
  echo "  Status: $status"
}

cmd_find() {
  local query="${1:-}"
  local play_num="${2:-}"
  local encoded_query results count play_url

  if [[ -z "$query" ]]; then
    echo "Usage: find <query> [number]"
    echo "Example: find jazz"
    echo "         find jazz 1"
    return 1
  fi

  require_bin curl "station search" || return 1

  encoded_query="$(jq -rn --arg q "$query" '$q|@uri')"
  results="$(
    curl -fsSL "https://de1.api.radio-browser.info/json/stations/byname/$encoded_query" \
      | jq -r '.[:10] | .[] | select(.url_resolved // .url) | "\(.name)|\(.url_resolved // .url)|\(.tags // "N/A")"'
  )"

  if [[ -z "$results" ]]; then
    echo "No stations found."
    return 1
  fi

  echo "Searching for: $query"
  echo ""

  count=0
  while IFS='|' read -r name url tags; do
    [[ -z "$url" ]] && continue
    count=$((count + 1))
    echo "  [$count] $name"
    echo "      URL: $url"
    echo "      Tags: $tags"
    echo ""
  done <<< "$results"

  if [[ -n "$play_num" ]]; then
    if [[ "$play_num" =~ ^[0-9]+$ ]] && (( play_num >= 1 && play_num <= count )); then
      play_url="$(sed -n "${play_num}p" <<< "$results" | cut -d'|' -f2)"
      echo "Playing station #$play_num"
      cmd_play "$play_url"
    else
      echo "Invalid station number. Choose 1-$count"
      return 1
    fi
  else
    echo "To play one now: /radio find \"$query\" <number>"
  fi
}

main() {
  require_bin jq "agent-radio" || exit 1

  refresh_prefs

  case "${1:-}" in
    play) shift; cmd_play "$@" ;;
    stop) cmd_stop ;;
    pause) cmd_pause ;;
    next) cmd_next ;;
    volume) shift; cmd_volume "$@" ;;
    now) cmd_now ;;
    find) shift; cmd_find "$@" ;;
    favorite) shift; cmd_favorite "$@" ;;
    list) cmd_list ;;
    *)
      echo "Usage: radio <play|stop|pause|next|volume|now|find|favorite|list> [args]"
      exit 1
      ;;
  esac
}

main "$@"
