#!/usr/bin/env bash
# agnes-image.sh - Generate/edit images via Agnes Image 2.0 Flash API
# Usage:
#   ./agnes-image.sh text "prompt" SIZE [OUTPUT_FILE]
#   ./agnes-image.sh img2img "prompt" SIZE IMAGE_URL [OUTPUT_FILE]
#   ./agnes-image.sh multi "prompt" SIZE IMAGE_URL1 IMAGE_URL2 [...] [OUTPUT_FILE]
#
# Environment: ANGES_API_KEY (required)

set -euo pipefail

API_URL="https://apihub.agnes-ai.com/v1/images/generations"
MODEL="agnes-image-2.0-flash"
API_KEY="${ANGES_API_KEY:-${AGENT_ANGES_API_KEY:-}}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: ANGES_API_KEY or AGENT_ANGES_API_KEY environment variable not set." >&2
  echo "   Set it with: export ANGES_API_KEY='your_api_key_here'" >&2
  exit 1
fi

WORKFLOW="${1:-}"
PROMPT="${2:-}"
SIZE="${3:-}"
shift 3 || { echo "ERROR: missing arguments" >&2; exit 1; }

if [ -z "$WORKFLOW" ] || [ -z "$PROMPT" ] || [ -z "$SIZE" ]; then
  echo "Usage:" >&2
  echo "  $0 text \"prompt\" SIZE [OUTPUT]" >&2
  echo "  $0 img2img \"prompt\" SIZE IMAGE_URL [OUTPUT]" >&2
  echo "  $0 multi \"prompt\" SIZE IMAGE1 IMAGE2 [...] [OUTPUT]" >&2
  exit 1
fi

OUTPUT_FILE="${1:-}"

build_body() {
  local body="{\"model\":\"${MODEL}\",\"prompt\":$(echo "$PROMPT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),\"size\":\"${SIZE}\""

  if [ "$WORKFLOW" != "text" ]; then
    # Collect image URLs
    local images=("$@")
    local json_images="["
    local first=true
    for img in "${images[@]}"; do
      if [ "$first" = true ]; then
        first=false
      else
        json_images+=","
      fi
      json_images+="$(echo "$img" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))')"
    done
    json_images+="]"
    body+=",\"extra_body\":{\"image\":${json_images},"
    
    if [ -n "$OUTPUT_FILE" ] && [[ "$OUTPUT_FILE" == *.base64 ]]; then
      body+="\"response_format\":\"b64_json\"}"
    else
      body+="\"response_format\":\"url\"}"
    fi
  else
    if [ -n "$OUTPUT_FILE" ] && [[ "$OUTPUT_FILE" == *.base64 ]]; then
      body+=",\"return_base64\":true}"
    else
      body+=",\"extra_body\":{\"response_format\":\"url\"}}"
    fi
  fi

  echo "$body"
}

if [ "$WORKFLOW" = "text" ]; then
  BODY=$(build_body)
elif [ "$WORKFLOW" = "img2img" ]; then
  BODY=$(build_body "$@")
elif [ "$WORKFLOW" = "multi" ]; then
  BODY=$(build_body "$@")
else
  echo "ERROR: unknown workflow '${WORKFLOW}'. Use text, img2img, or multi." >&2
  exit 1
fi

# Send request
RESPONSE=$(curl -sf --max-time 360 \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "$API_URL")

if [ "$WORKFLOW" = "text" ] && [[ "$OUTPUT_FILE" == *.base64 ]]; then
  # Extract base64
  echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
b64 = data['data'][0]['b64_json']
print(b64)
" > "$OUTPUT_FILE"
  echo "Saved Base64 to: $OUTPUT_FILE"
elif [ "$WORKFLOW" != "text" ] && [[ "$OUTPUT_FILE" == *.base64 ]]; then
  echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
b64 = data['data'][0]['b64_json']
print(b64)
" > "$OUTPUT_FILE"
  echo "Saved Base64 to: $OUTPUT_FILE"
else
  # Extract URL
  URL=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data['data'][0]['url'])
")
  echo "Generated image URL: $URL"
  
  if [ -n "$OUTPUT_FILE" ]; then
    curl -sf -o "$OUTPUT_FILE" "$URL"
    echo "Saved image to: $OUTPUT_FILE"
  fi
fi
