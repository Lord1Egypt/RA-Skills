#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  transcribe.sh <audio-file> [options]

Options:
  --out <path>        Output file (default: <input>.txt)
  --language <code>   Language code (e.g. zh, en, ja, ko, de, fr)
  --model <name>      Model name (default: nova-3)
  --json              Output full JSON response
  --speakers          Enable speaker diarization
  --paragraphs        Enable smart paragraphs
  --summarize         Enable AI summary
  --detect-language   Auto-detect language
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

in="${1:-}"
shift || true

model="nova-3"
out=""
language=""
response_format="text"
extra_params=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) model="${2:-}"; shift 2 ;;
    --out) out="${2:-}"; shift 2 ;;
    --language) language="${2:-}"; shift 2 ;;
    --json) response_format="json"; shift ;;
    --speakers) extra_params="${extra_params}&diarize=true"; shift ;;
    --paragraphs) extra_params="${extra_params}&paragraphs=true"; shift ;;
    --summarize) extra_params="${extra_params}&summarize=v2"; shift ;;
    --detect-language) extra_params="${extra_params}&detect_language=true"; shift ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

# --- Input validation ---

if [[ ! -f "$in" ]]; then
  echo "File not found: $in" >&2
  exit 1
fi

if [[ "${DEEPGRAM_API_KEY:-}" == "" ]]; then
  echo "Missing DEEPGRAM_API_KEY" >&2
  exit 1
fi

# Validate language code (alphanumeric + dash only, e.g. en, en-US, zh-CN)
if [[ -n "$language" && ! "$language" =~ ^[a-zA-Z0-9-]+$ ]]; then
  echo "Invalid language code: $language" >&2
  exit 1
fi

# Validate model name (alphanumeric + dash/dot only, e.g. nova-3, nova-2-general)
if [[ ! "$model" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "Invalid model name: $model" >&2
  exit 1
fi

if [[ "$out" == "" ]]; then
  base="${in%.*}"
  if [[ "$response_format" == "json" ]]; then
    out="${base}.json"
  else
    out="${base}.txt"
  fi
fi

mkdir -p "$(dirname "$out")"

# Detect MIME type
mime="audio/wav"
case "${in##*.}" in
  m4a) mime="audio/mp4" ;;
  mp3) mime="audio/mpeg" ;;
  mp4) mime="audio/mp4" ;;
  ogg) mime="audio/ogg" ;;
  flac) mime="audio/flac" ;;
  webm) mime="audio/webm" ;;
  wav) mime="audio/wav" ;;
esac

# Build URL
url="https://api.deepgram.com/v1/listen?model=${model}&smart_format=true&punctuate=true"
if [[ -n "$language" ]]; then
  url="${url}&language=${language}"
fi
url="${url}${extra_params}"

# Secure temp file
tmpfile=$(mktemp /tmp/deepgram_result.XXXXXXXXXX)
trap 'rm -f "$tmpfile"' EXIT

# Call API (-- prevents option injection from filenames starting with -)
http_code=$(curl -sS -w '%{http_code}' -o "$tmpfile" -- "$url" \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H "Content-Type: ${mime}" \
  --data-binary "@${in}")
result=$(cat "$tmpfile")

# Check HTTP status
if [[ "$http_code" != "200" ]]; then
  err_msg=$(echo "$result" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('err_msg', d.get('message', str(d))))
except:
    print(sys.stdin.read() if hasattr(sys.stdin, 'read') else 'Unknown error')
" 2>/dev/null || echo "$result")
  echo "Deepgram API error (HTTP $http_code): $err_msg" >&2
  exit 1
fi

if [[ "$response_format" == "json" ]]; then
  echo "$result" > "$out"
else
  # Extract transcript text from JSON response
  transcript=$(echo "$result" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if 'err_code' in d:
        print(d.get('err_msg', str(d)), file=sys.stderr)
        sys.exit(1)
    ch = d.get('results',{}).get('channels',[{}])[0]
    alts = ch.get('alternatives',[{}])
    parts = []
    for a in alts:
        if 'paragraphs' in a and 'paragraphs' in a['paragraphs']:
            for p in a['paragraphs']['paragraphs']:
                for s in p.get('sentences',[]):
                    parts.append(s.get('text',''))
            break
        elif 'transcript' in a:
            parts.append(a['transcript'])
            break
    print('\n'.join(parts))
except SystemExit:
    raise
except Exception as e:
    print(f'Failed to parse response: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1) || {
    echo "Failed to parse response. Raw:" >&2
    echo "$result" >&2
    exit 1
  }
  echo "$transcript" > "$out"
fi

echo "$out"
