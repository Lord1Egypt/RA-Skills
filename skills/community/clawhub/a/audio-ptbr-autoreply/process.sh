#!/usr/bin/env bash
set -euo pipefail
IFS=$'
	'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${WORKSPACE:-${HOME}/.openclaw/workspace}"
VENV_PY="${SCRIPT_DIR}/.venv/bin/python"

log() { printf '%s
' "$*" >&2; }
fail() { log "ERROR: $*"; exit 1; }

python_cmd() {
  if [[ -x "$VENV_PY" ]]; then
    printf '%s
' "$VENV_PY"
  elif command -v python3 >/dev/null 2>&1; then
    printf 'python3
'
  else
    fail "python3 not found"
  fi
}

usage() {
  cat <<'TXT'
Usage:
  bash process.sh --voice-command "listar"
  bash process.sh --audio-file /absolute/path/to/audio.ogg [--target TARGET] [--reply-to MESSAGE_ID]
TXT
}

handle_voice_command() {
  local arg="${1:-}"
  local py
  py="$(python_cmd)"

  case "${arg,,}" in
    ""|"listar"|"lista")
      "$py" "${SCRIPT_DIR}/scripts/voice_config.py" list
      ;;
    "jeff"|"cadu"|"faber"|"miro"|"feminina"|"masculina")
      "$py" "${SCRIPT_DIR}/scripts/voice_config.py" set "$arg"
      ;;
    *)
      usage
      return 1
      ;;
  esac
}

send_media_directive() {
  local audio_path="$1"
  local target="${2:-}"
  local reply_to="${3:-}"

  printf 'MEDIA:%s [[audio_as_voice]]
' "$audio_path"

  if [[ -n "$target" ]] && command -v openclaw >/dev/null 2>&1; then
    openclaw sessions send       --target "$target"       --message "MEDIA:${audio_path} [[audio_as_voice]]"       --reply-to "$reply_to" >/dev/null 2>&1 || true
  fi
}

main() {
  local py audio_file="" target="" reply_to="" voice_cmd=""
  py="$(python_cmd)"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --voice-command)
        shift
        [[ $# -gt 0 ]] || fail "Missing value for --voice-command"
        voice_cmd="$1"
        ;;
      --audio-file)
        shift
        [[ $# -gt 0 ]] || fail "Missing value for --audio-file"
        audio_file="$1"
        ;;
      --target)
        shift
        [[ $# -gt 0 ]] || fail "Missing value for --target"
        target="$1"
        ;;
      --reply-to)
        shift
        [[ $# -gt 0 ]] || fail "Missing value for --reply-to"
        reply_to="$1"
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        fail "Unknown argument: $1"
        ;;
    esac
    shift
  done

  if [[ -n "$voice_cmd" ]]; then
    handle_voice_command "$voice_cmd"
    exit 0
  fi

  [[ -n "$audio_file" ]] || fail "Missing --audio-file"
  [[ -f "$audio_file" ]] || fail "Audio file not found: $audio_file"

  local transcript response audio_path voice transcript_file response_file
  voice="$($py "${SCRIPT_DIR}/scripts/voice_config.py" get)"

  transcript_file="$(mktemp)"
  response_file="$(mktemp)"
  trap 'rm -f "$transcript_file" "$response_file"' EXIT

  "$py" "${SCRIPT_DIR}/scripts/transcribe_universal.py" --text "$audio_file" > "$transcript_file" || fail "Transcription failed"
  [[ -s "$transcript_file" ]] || fail "Empty transcript"

  "$py" "${SCRIPT_DIR}/scripts/claude_adapter.py" --stdin --text < "$transcript_file" > "$response_file" || fail "Response generation failed"
  [[ -s "$response_file" ]] || fail "Empty response"

  audio_path="$($py "${SCRIPT_DIR}/scripts/synthesize_universal.py" --stdin --voice "$voice" --print-path < "$response_file")" || fail "Synthesis failed"
  [[ -f "$audio_path" ]] || fail "Audio output not found"

  send_media_directive "$audio_path" "$target" "$reply_to"
}

main "$@"
