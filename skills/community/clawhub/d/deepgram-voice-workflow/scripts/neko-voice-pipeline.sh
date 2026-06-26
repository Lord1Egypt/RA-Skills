#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  neko-voice-pipeline.sh <input-audio.ogg> [--reply "text"] [--out-dir /path]

Pipeline:
  1. STT: transcribe input audio with Deepgram
  2. Optional reply text -> TTS mp3
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

in="${1:-}"
shift || true
reply=""
out_dir=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --reply)
      reply="${2:-}"
      shift 2
      ;;
    --out-dir)
      out_dir="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      ;;
  esac
done

if [[ ! -f "$in" ]]; then
  echo "Input audio not found: $in" >&2
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
base_name="$(basename "${in%.*}")"
if [[ "$out_dir" == "" ]]; then
  out_dir="/tmp/neko-voice-${base_name}"
fi
mkdir -p "$out_dir"

transcript_out="$out_dir/transcript.txt"
"$script_dir/deepgram-transcribe.sh" "$in" --out "$transcript_out" >/dev/null

reply_mp3=""
if [[ "$reply" != "" ]]; then
  reply_mp3="$out_dir/reply.mp3"
  "$script_dir/deepgram-tts.sh" "$reply" --out "$reply_mp3" >/dev/null
fi

python3 - <<'PY' "$transcript_out" "$reply_mp3" "$out_dir"
import json, sys, pathlib
transcript_path = pathlib.Path(sys.argv[1])
reply_mp3 = sys.argv[2]
out_dir = pathlib.Path(sys.argv[3])
obj = {
  'out_dir': str(out_dir),
  'transcript_path': str(transcript_path),
  'transcript': transcript_path.read_text(encoding='utf-8').strip() if transcript_path.exists() else '',
  'reply_audio_path': reply_mp3 or None,
}
print(json.dumps(obj, ensure_ascii=False, indent=2))
PY
