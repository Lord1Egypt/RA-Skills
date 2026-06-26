#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  deepgram-transcribe.sh <audio-file> [--out /path/to/out.txt] [--model nova-2] [--language zh] [--content-type audio/ogg]
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

in="${1:-}"
shift || true

out=""
model="nova-2"
language="zh"
content_type="audio/ogg"

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
    --language)
      language="${2:-}"
      shift 2
      ;;
    --content-type)
      content_type="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      ;;
  esac
done

if [[ ! -f "$in" ]]; then
  echo "File not found: $in" >&2
  exit 1
fi

if [[ "${DEEPGRAM_API_KEY:-}" == "" && -f /root/.openclaw/.env ]]; then
  export DEEPGRAM_API_KEY="$(sed -n 's/^DEEPGRAM_API_KEY=//p' /root/.openclaw/.env | tail -n1)"
fi

if [[ "${DEEPGRAM_API_KEY:-}" == "" ]]; then
  echo "Missing DEEPGRAM_API_KEY" >&2
  exit 1
fi

if [[ "$out" == "" ]]; then
  out="${in%.*}.deepgram.txt"
fi

mkdir -p "$(dirname "$out")"
json_out="${out}.json"

curl -sS --max-time 120 "https://api.deepgram.com/v1/listen?model=${model}&smart_format=true&language=${language}&punctuate=true" \
  -H "Authorization: Token ${DEEPGRAM_API_KEY}" \
  -H "Content-Type: ${content_type}" \
  --data-binary @"${in}" > "$json_out"

python3 - "$json_out" "$out" <<'PY'
import json, sys
jp, op = sys.argv[1], sys.argv[2]
obj = json.load(open(jp))
if 'results' not in obj:
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(1)
text = obj['results']['channels'][0]['alternatives'][0].get('transcript', '')
with open(op, 'w', encoding='utf-8') as f:
    f.write(text + ('\n' if text and not text.endswith('\n') else ''))
print(op)
PY
