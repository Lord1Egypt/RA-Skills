#!/usr/bin/env bash
# gamma.sh — Gamma.app API wrapper
# Publisher: autosolutionsai-didac (AutoSolutions.ai)
# Homepage: https://gamma.app
# API endpoint: https://public-api.gamma.app/v1.0
# Required env: GAMMA_API_KEY (get from https://gamma.app/settings)
# Required bins: curl, python3
# Usage:
#   gamma.sh generate "inputText" [options...]
#   gamma.sh template "gammaId" "prompt" [options...]
#   gamma.sh status "generationId"
#   gamma.sh themes [query]
#   gamma.sh folders [query]
#
# Environment:
#   GAMMA_API_KEY — required
#
# Options (for generate/template):
#   --format presentation|document|social|webpage
#   --text-mode generate|condense|preserve
#   --num-cards N
#   --card-split auto|inputTextBreaks
#   --theme THEME_ID
#   --export pdf|pptx
#   --tone "professional, inspiring"
#   --audience "business leaders"
#   --language en
#   --amount brief|medium|detailed|extensive
#   --image-source aiGenerated|pictographic|pexels|noImages|...
#   --image-model flux-1-pro|imagen-4-pro|...
#   --image-style "photorealistic"
#   --instructions "additional instructions"
#   --workspace-access noAccess|view|comment|edit|fullAccess
#   --external-access noAccess|view|comment|edit
#   --dimensions fluid|16x9|4x3|1x1|4x5|9x16|...
#   --wait          Poll until generation completes (default: return immediately)
#   --poll-interval  Seconds between status checks (default: 5)

set -euo pipefail

API_BASE="https://public-api.gamma.app/v1.0"

die() { echo "ERROR: $*" >&2; exit 1; }

# Validate runtime dependencies
command -v curl &>/dev/null || die "curl is required but not found"
command -v python3 &>/dev/null || die "python3 is required but not found"

# Validate API key
[ -z "${GAMMA_API_KEY:-}" ] && die "GAMMA_API_KEY not set. Get one at https://gamma.app/settings"

CMD="${1:-}"
[ -z "$CMD" ] && die "Usage: gamma.sh <generate|template|status|themes|folders> [args...]"
shift

api() {
  local method="$1" endpoint="$2"
  shift 2
  curl -sf -X "$method" "${API_BASE}${endpoint}" \
    -H "X-API-KEY: ${GAMMA_API_KEY}" \
    -H "Content-Type: application/json" \
    -H "accept: application/json" \
    "$@"
}

poll_status() {
  local gen_id="$1" interval="${2:-5}"
  while true; do
    local resp
    resp=$(api GET "/generations/${gen_id}")
    local status
    status=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null || echo "unknown")
    if [ "$status" = "completed" ] || [ "$status" = "failed" ] || [ "$status" = "error" ]; then
      echo "$resp"
      return 0
    fi
    echo "Status: $status — waiting ${interval}s..." >&2
    sleep "$interval"
  done
}

case "$CMD" in
  generate)
    INPUT_TEXT="${1:-}"
    [ -z "$INPUT_TEXT" ] && die "Usage: gamma.sh generate \"input text\" [options...]"
    shift

    # Defaults
    FORMAT="presentation"
    TEXT_MODE="generate"
    NUM_CARDS=""
    CARD_SPLIT="auto"
    THEME_ID=""
    EXPORT_AS=""
    TONE=""
    AUDIENCE=""
    LANGUAGE=""
    AMOUNT=""
    IMG_SOURCE=""
    IMG_MODEL=""
    IMG_STYLE=""
    INSTRUCTIONS=""
    WS_ACCESS=""
    EXT_ACCESS=""
    DIMENSIONS=""
    WAIT=false
    POLL_INTERVAL=5
    FOLDER_IDS=""

    while [ $# -gt 0 ]; do
      case "$1" in
        --format) FORMAT="$2"; shift 2;;
        --text-mode) TEXT_MODE="$2"; shift 2;;
        --num-cards) NUM_CARDS="$2"; shift 2;;
        --card-split) CARD_SPLIT="$2"; shift 2;;
        --theme) THEME_ID="$2"; shift 2;;
        --export) EXPORT_AS="$2"; shift 2;;
        --tone) TONE="$2"; shift 2;;
        --audience) AUDIENCE="$2"; shift 2;;
        --language) LANGUAGE="$2"; shift 2;;
        --amount) AMOUNT="$2"; shift 2;;
        --image-source) IMG_SOURCE="$2"; shift 2;;
        --image-model) IMG_MODEL="$2"; shift 2;;
        --image-style) IMG_STYLE="$2"; shift 2;;
        --instructions) INSTRUCTIONS="$2"; shift 2;;
        --workspace-access) WS_ACCESS="$2"; shift 2;;
        --external-access) EXT_ACCESS="$2"; shift 2;;
        --dimensions) DIMENSIONS="$2"; shift 2;;
        --folder) FOLDER_IDS="$2"; shift 2;;
        --wait) WAIT=true; shift;;
        --poll-interval) POLL_INTERVAL="$2"; shift 2;;
        *) die "Unknown option: $1";;
      esac
    done

    # Build JSON payload
    PAYLOAD=$(python3 -c "
import json, sys

data = {
    'inputText': '''${INPUT_TEXT}''',
    'textMode': '${TEXT_MODE}',
    'format': '${FORMAT}',
    'cardSplit': '${CARD_SPLIT}'
}

if '${NUM_CARDS}': data['numCards'] = int('${NUM_CARDS}')
if '${THEME_ID}': data['themeId'] = '${THEME_ID}'
if '${EXPORT_AS}': data['exportAs'] = '${EXPORT_AS}'
if '${INSTRUCTIONS}': data['additionalInstructions'] = '${INSTRUCTIONS}'
if '${FOLDER_IDS}': data['folderIds'] = '${FOLDER_IDS}'.split(',')

text_opts = {}
if '${TONE}': text_opts['tone'] = '${TONE}'
if '${AUDIENCE}': text_opts['audience'] = '${AUDIENCE}'
if '${LANGUAGE}': text_opts['language'] = '${LANGUAGE}'
if '${AMOUNT}': text_opts['amount'] = '${AMOUNT}'
if text_opts: data['textOptions'] = text_opts

img_opts = {}
if '${IMG_SOURCE}': img_opts['source'] = '${IMG_SOURCE}'
if '${IMG_MODEL}': img_opts['model'] = '${IMG_MODEL}'
if '${IMG_STYLE}': img_opts['style'] = '${IMG_STYLE}'
if img_opts: data['imageOptions'] = img_opts

card_opts = {}
if '${DIMENSIONS}': card_opts['dimensions'] = '${DIMENSIONS}'
if card_opts: data['cardOptions'] = card_opts

sharing = {}
if '${WS_ACCESS}': sharing['workspaceAccess'] = '${WS_ACCESS}'
if '${EXT_ACCESS}': sharing['externalAccess'] = '${EXT_ACCESS}'
if sharing: data['sharingOptions'] = sharing

print(json.dumps(data))
")

    RESP=$(echo "$PAYLOAD" | api POST "/generations" -d @-)
    echo "$RESP"

    GEN_ID=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('generationId',''))" 2>/dev/null || echo "")

    if [ "$WAIT" = true ] && [ -n "$GEN_ID" ]; then
      echo "Polling for completion..." >&2
      poll_status "$GEN_ID" "$POLL_INTERVAL"
    fi
    ;;

  template)
    GAMMA_ID="${1:-}"
    PROMPT="${2:-}"
    [ -z "$GAMMA_ID" ] || [ -z "$PROMPT" ] && die "Usage: gamma.sh template \"gammaId\" \"prompt\" [options...]"
    shift 2

    THEME_ID=""
    EXPORT_AS=""
    IMG_MODEL=""
    IMG_STYLE=""
    WS_ACCESS=""
    EXT_ACCESS=""
    FOLDER_IDS=""
    WAIT=false
    POLL_INTERVAL=5

    while [ $# -gt 0 ]; do
      case "$1" in
        --theme) THEME_ID="$2"; shift 2;;
        --export) EXPORT_AS="$2"; shift 2;;
        --image-model) IMG_MODEL="$2"; shift 2;;
        --image-style) IMG_STYLE="$2"; shift 2;;
        --workspace-access) WS_ACCESS="$2"; shift 2;;
        --external-access) EXT_ACCESS="$2"; shift 2;;
        --folder) FOLDER_IDS="$2"; shift 2;;
        --wait) WAIT=true; shift;;
        --poll-interval) POLL_INTERVAL="$2"; shift 2;;
        *) die "Unknown option: $1";;
      esac
    done

    PAYLOAD=$(python3 -c "
import json
data = {'gammaId': '${GAMMA_ID}', 'prompt': '''${PROMPT}'''}
if '${THEME_ID}': data['themeId'] = '${THEME_ID}'
if '${EXPORT_AS}': data['exportAs'] = '${EXPORT_AS}'
if '${FOLDER_IDS}': data['folderIds'] = '${FOLDER_IDS}'.split(',')
img_opts = {}
if '${IMG_MODEL}': img_opts['model'] = '${IMG_MODEL}'
if '${IMG_STYLE}': img_opts['style'] = '${IMG_STYLE}'
if img_opts: data['imageOptions'] = img_opts
sharing = {}
if '${WS_ACCESS}': sharing['workspaceAccess'] = '${WS_ACCESS}'
if '${EXT_ACCESS}': sharing['externalAccess'] = '${EXT_ACCESS}'
if sharing: data['sharingOptions'] = sharing
print(json.dumps(data))
")

    RESP=$(echo "$PAYLOAD" | api POST "/generations/from-template" -d @-)
    echo "$RESP"

    GEN_ID=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('generationId',''))" 2>/dev/null || echo "")

    if [ "$WAIT" = true ] && [ -n "$GEN_ID" ]; then
      echo "Polling for completion..." >&2
      poll_status "$GEN_ID" "$POLL_INTERVAL"
    fi
    ;;

  status)
    GEN_ID="${1:-}"
    [ -z "$GEN_ID" ] && die "Usage: gamma.sh status <generationId>"
    api GET "/generations/${GEN_ID}"
    ;;

  themes)
    QUERY="${1:-}"
    if [ -n "$QUERY" ]; then
      api GET "/themes?query=${QUERY}&limit=50"
    else
      api GET "/themes?limit=50"
    fi
    ;;

  folders)
    QUERY="${1:-}"
    if [ -n "$QUERY" ]; then
      api GET "/folders?query=${QUERY}&limit=50"
    else
      api GET "/folders?limit=50"
    fi
    ;;

  *)
    die "Unknown command: $CMD. Use: generate, template, status, themes, folders"
    ;;
esac
