#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  deepgram-tts.sh "text to speak" [--out /path/to/out.mp3] [--model aura-2-luna-en]
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

text="${1:-}"
shift || true

out=""
model="aura-2-luna-en"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      out="${2:-}"
      shift 2
      ;;
    --model)
      model="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      ;;
  esac
done

if [[ "${DEEPGRAM_API_KEY:-}" == "" && -f /root/.openclaw/.env ]]; then
  export DEEPGRAM_API_KEY="$(sed -n 's/^DEEPGRAM_API_KEY=//p' /root/.openclaw/.env | tail -n1)"
fi

if [[ "${DEEPGRAM_API_KEY:-}" == "" ]]; then
  echo "Missing DEEPGRAM_API_KEY" >&2
  exit 1
fi

if [[ "$out" == "" ]]; then
  out="/tmp/deepgram-tts-$(date +%Y%m%d-%H%M%S).mp3"
fi

mkdir -p "$(dirname "$out")"

payload="$(TEXT_TO_SPEAK="$text" python3 - <<'PY'
import json, os
print(json.dumps({"text": os.environ["TEXT_TO_SPEAK"]}, ensure_ascii=False))
PY
)"

curl -sS --max-time 120 "https://api.deepgram.com/v1/speak?model=${model}" \
  -H "Authorization: Token ${DEEPGRAM_API_KEY}" \
  -H 'Content-Type: application/json' \
  --data "$payload" > "$out"

echo "$out"
