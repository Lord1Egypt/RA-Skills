#!/usr/bin/env bash
set -euo pipefail

# Submit artifact or upload file to ClawGrid API
# Reads API key from config.json automatically
#
# Artifact mode:      bash submit.sh <task_id> <payload_file>
# Upload mode:        bash submit.sh --upload <task_id> <file_path>
# File+Submit mode:   bash submit.sh --file-submit <task_id> <file_path> [description]
#
# Backward compat:    --file is an alias for --upload

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

# Handle --upload mode (--file kept as backward-compat alias)
if [ "${1:-}" = "--upload" ] || [ "${1:-}" = "--file" ]; then
  if [ $# -lt 3 ]; then
    echo "Usage: bash $0 --upload <task_id> <file_path>" >&2
    exit 1
  fi
  TASK_ID="$2"
  FILE_PATH="$3"

  if [ ! -f "$CONFIG" ]; then
    echo "ERROR: Config not found at $CONFIG" >&2
    exit 1
  fi
  if [ ! -f "$FILE_PATH" ]; then
    echo "ERROR: File not found: $FILE_PATH" >&2
    exit 1
  fi

  API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
  API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

  RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/tasks/$TASK_ID/files" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$FILE_PATH" \
    --max-time 60)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "File upload failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

# Handle --file-submit mode: upload file + submit artifact in one step
if [ "${1:-}" = "--file-submit" ]; then
  if [ $# -lt 3 ]; then
    echo "Usage: bash $0 --file-submit <task_id> <file_path> [description]" >&2
    exit 1
  fi
  TASK_ID="$2"
  FILE_PATH="$3"
  DESCRIPTION="${4:-File submission}"

  if [ ! -f "$CONFIG" ]; then
    echo "ERROR: Config not found at $CONFIG" >&2
    exit 1
  fi
  if [ ! -f "$FILE_PATH" ]; then
    echo "ERROR: File not found: $FILE_PATH" >&2
    exit 1
  fi

  API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
  API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")
  FILENAME=$(basename "$FILE_PATH")

  # Step 1: Upload file
  echo "[submit] Uploading $FILENAME ..." >&2
  UP_RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/tasks/$TASK_ID/files" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$FILE_PATH" \
    --max-time 60)

  UP_CODE=$(echo "$UP_RESP" | tail -1)
  UP_BODY=$(echo "$UP_RESP" | sed '$d')

  if [ "$UP_CODE" -lt 200 ] || [ "$UP_CODE" -ge 300 ]; then
    echo "File upload failed (HTTP $UP_CODE): $UP_BODY" >&2
    exit 1
  fi

  FILE_URL=$(echo "$UP_BODY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('download_url','') or d.get('url',''))" 2>/dev/null || echo "")
  FILE_ID=$(echo "$UP_BODY" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
  echo "[submit] File uploaded: id=$FILE_ID" >&2

  # Step 2: Build artifact payload and submit
  ARTIFACT_PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
    'artifact_type': 'dataset',
    'data': {
        'items': [{
            'type': 'file',
            'filename': sys.argv[1],
            'file_id': sys.argv[2],
            'url': sys.argv[3],
            'description': sys.argv[4],
        }],
        'item_count': 1,
    },
}))
" "$FILENAME" "$FILE_ID" "$FILE_URL" "$DESCRIPTION")

  PAYLOAD_TMP=$(mktemp)
  echo "$ARTIFACT_PAYLOAD" > "$PAYLOAD_TMP"
  trap 'rm -f "$PAYLOAD_TMP"' EXIT

  echo "[submit] Submitting artifact ..." >&2
  RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/artifacts" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d @"$PAYLOAD_TMP" \
    --max-time 30)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "Submit failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

if [ $# -lt 2 ]; then
  echo "Usage: bash $0 <task_id> <payload_file>" >&2
  echo "       bash $0 --file <task_id> <file_path>" >&2
  exit 1
fi

TASK_ID="$1"
PAYLOAD_FILE="$2"

mkdir -p "$LOG_DIR"

task_log() {
  local phase="$1"
  local status="$2"
  local detail="${3:-}"
  python3 - "$LOG_DIR/$TASK_ID.log" "$TASK_ID" "$phase" "$status" "$detail" <<'PYEOF'
import json
import sys
from datetime import datetime, timezone

path, task_id, phase, status, detail = sys.argv[1:]
line = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "phase": phase,
    "status": status,
    "detail": detail,
}
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
PYEOF
}

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

if [ ! -f "$PAYLOAD_FILE" ]; then
  echo "ERROR: Payload file not found: $PAYLOAD_FILE" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

task_log "submit_manual" "start" "payload_file=$PAYLOAD_FILE"
ENRICHED_PAYLOAD=$(mktemp)
python3 - "$PAYLOAD_FILE" "$LOG_DIR/$TASK_ID.log" "$ENRICHED_PAYLOAD" <<'PYEOF'
import json
import sys
from pathlib import Path

src, log_path, out = sys.argv[1:]
payload = json.loads(Path(src).read_text(encoding="utf-8"))
lp = Path(log_path)
payload["task_log"] = lp.read_text(encoding="utf-8", errors="replace") if lp.exists() else ""
Path(out).write_text(json.dumps(payload), encoding="utf-8")
PYEOF
trap 'rm -f "$ENRICHED_PAYLOAD"' EXIT

RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/artifacts" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$ENRICHED_PAYLOAD" \
  --max-time 30)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  task_log "submit_manual" "http_$HTTP_CODE" "$BODY"
  echo "$BODY"
  exit 0
else
  task_log "submit_manual" "http_$HTTP_CODE" "$BODY"
  echo "Submit failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
