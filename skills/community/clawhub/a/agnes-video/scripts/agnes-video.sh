#!/usr/bin/env bash
# agnes-video.sh - Generate videos via Agnes Video V2.0 API
# Usage:
#   ./agnes-video.sh text "prompt" [OUTPUT_FILE]
#   ./agnes-video.sh img2video "prompt" IMAGE_URL [OUTPUT_FILE]
#   ./agnes-video.sh multi "prompt" IMAGE1 IMAGE2 [OUTPUT_FILE]
#   ./agnes-video.sh keyframes "prompt" IMAGE1 IMAGE2 [OUTPUT_FILE]
#
# Environment: ANGES_API_KEY (required, shared with Agnes Image)

set -euo pipefail

API_CREATE="https://apihub.agnes-ai.com/v1/videos"
API_RESULT="https://apihub.agnes-ai.com/agnesapi"
MODEL="agnes-video-v2.0"
API_KEY="${ANGES_API_KEY:-${AGENT_ANGES_API_KEY:-}}"
MAX_WAIT=300
POLL_INTERVAL=5

if [ -z "$API_KEY" ]; then
  echo "ERROR: ANGES_API_KEY or AGENT_ANGES_API_KEY environment variable not set." >&2
  echo "   Set it with: export ANGES_API_KEY='your_api_key_here'" >&2
  exit 1
fi
  echo "ERROR: ANGES_API_KEY or AGENT_ANGES_API_KEY not set." >&2
  exit 1
fi

WORKFLOW="${1:-}"
PROMPT="${2:-}"
shift 2 || { echo "ERROR: insufficient arguments" >&2; exit 1; }

# Separate image URLs from output file
POSITIONAL=()
OUTPUT_FILE="video_output.mp4"
for arg in "$@"; do
  if [[ "$arg" == *.mp4 ]] || [[ "$arg" == *.mov ]] || [[ "$arg" == *.avi ]]; then
    OUTPUT_FILE="$arg"
  else
    POSITIONAL+=("$arg")
  fi
done

# Build images array and mode
MODE="ti2vid"
IMAGE_JSON="[]"
EXTRA_EXTRA_BODY="{}"

if [ "$WORKFLOW" = "img2video" ]; then
  IMAGE_JSON="[\"${POSITIONAL[0]}\"]"
  # For img2video, use top-level "image" field
elif [ "$WORKFLOW" = "multi" ]; then
  MODE="multi"
  IMAGES_JSON="["
  FIRST=true
  for img in "${POSITIONAL[@]}"; do
    $FIRST && FIRST=false || IMAGES_JSON+=","
    IMAGES_JSON+="\"${img}\""
  done
  IMAGES_JSON+="]"
  EXTRA_EXTRA_BODY="{\"image\":${IMAGES_JSON}}"
elif [ "$WORKFLOW" = "keyframes" ]; then
  MODE="keyframes"
  IMAGES_JSON="["
  FIRST=true
  for img in "${POSITIONAL[@]}"; do
    $FIRST && FIRST=false || IMAGES_JSON+=","
    IMAGES_JSON+="\"${img}\""
  done
  IMAGES_JSON+="]"
  EXTRA_EXTRA_BODY="{\"image\":${IMAGES_JSON},\"mode\":\"keyframes\"}"
else
  echo "ERROR: unknown workflow '${WORKFLOW}'" >&2
  exit 1
fi

# Calculate frames: duration ~5s, fps 24 => 121 frames (follows 8n+1 rule)
NUM_FRAMES=121
FPS=24
WIDTH=1152
HEIGHT=768

echo "Creating video task..."
echo "  Model: $MODEL"
echo "  Workflow: $WORKFLOW"
echo "  Prompt: ${PROMPT:0:80}..."
echo ""

# Create task using Python for reliable JSON construction
CREATED=$(python3 <<PYEOF
import json, subprocess, sys

payload = {
    "model": "${MODEL}",
    "prompt": """${PROMPT}""",
    "mode": "${MODE}",
    "width": ${WIDTH},
    "height": ${HEIGHT},
    "num_frames": ${NUM_FRAMES},
    "frame_rate": ${FPS}
}

if "${WORKFLOW}" == "img2video":
    payload["image"] = "${POSITIONAL[0]}"
elif "${WORKFLOW}" in ("multi", "keyframes"):
    payload["extra_body"] = json.loads('${EXTRA_EXTRA_BODY}')

resp = subprocess.run([
    "curl", "-sf", "--max-time", "60",
    "-H", "Authorization: Bearer ${API_KEY}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(payload),
    "${API_CREATE}"
], capture_output=True, text=True)

if resp.returncode != 0:
    print(f"ERROR creating task: {resp.stderr}", file=sys.stderr)
    sys.exit(1)

result = json.loads(resp.stdout)
print(json.dumps(result))
PYEOF
)

VIDEO_ID=$(echo "$CREATED" | python3 -c "import sys,json; print(json.load(sys.stdin)['video_id'])")
TASK_ID=$(echo "$CREATED" | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
STATUS=$(echo "$CREATED" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

echo "Task created!"
echo "  video_id: $VIDEO_ID"
echo "  task_id: $TASK_ID"
echo "  status: $STATUS"
echo ""

# Poll for completion
ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT ]; do
  sleep $POLL_INTERVAL
  ELAPSED=$((ELAPSED + POLL_INTERVAL))
  
  RESPONSE=$(curl -sf --max-time 30 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${API_RESULT}?video_id=${VIDEO_ID}")
  
  STATUS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  PROGRESS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('progress', 0))")
  
  echo -ne "\r  Status: $STATUS | Progress: ${PROGRESS}% | Elapsed: ${ELAPSED}s"
  
  if [ "$STATUS" = "completed" ]; then
    echo ""
    echo ""
    VIDEO_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['remixed_from_video_id'])")
    echo "Video generated successfully!"
    echo "  URL: $VIDEO_URL"
    
    if [ "$OUTPUT_FILE" != "video_output.mp4" ]; then
      curl -sf -o "$OUTPUT_FILE" "$VIDEO_URL"
      echo "  Saved to: $OUTPUT_FILE"
    fi
    exit 0
  elif [ "$STATUS" = "failed" ]; then
    ERROR=$(echo "$RESPONSE" | python3 -c "import sys,json; e=json.load(sys.stdin).get('error'); print(e if e else 'Unknown error')")
    echo ""
    echo ""
    echo "ERROR: Video generation failed!"
    echo "  Error: $ERROR"
    exit 1
  fi
done

echo ""
echo ""
echo "ERROR: Timeout (${MAX_WAIT}s exceeded)."
exit 1
