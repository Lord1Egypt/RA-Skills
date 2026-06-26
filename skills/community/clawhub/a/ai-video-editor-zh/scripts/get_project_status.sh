#!/usr/bin/env bash
# Query the status of a Sparki Business API video processing project using batch query.
#
# Usage: get_project_status.sh <project_id>
#
# Args:
#   project_id: UUID returned by create_project.sh
#
# Outputs (stdout):
#   - On completed:  "completed <result_url>"
#   - On failed:     "failed <error_message>"
#   - On other:      "processing"
#
# Exit codes:
#   0 — terminal state (completed or failed)
#   2 — still in progress (poll again)
#   1 — argument or API error

set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SPARKI_API_BASE="${SPARKI_API_BASE:-https://agent-enterprise-dev.aicoding.live/api/v1}"
RATE_LIMIT_SLEEP=3

# ---------------------------------------------------------------------------
# Validate environment
# ---------------------------------------------------------------------------
: "${SPARKI_API_KEY:?Error: SPARKI_API_KEY environment variable is required}"

# ---------------------------------------------------------------------------
# Validate arguments
# ---------------------------------------------------------------------------
if [[ $# -lt 1 ]]; then
  echo "Usage: get_project_status.sh <project_id>" >&2
  exit 1
fi

PROJECT_ID="$1"

# ---------------------------------------------------------------------------
# Query project status via POST /projects/batch
# ---------------------------------------------------------------------------
sleep "$RATE_LIMIT_SLEEP"

RESPONSE=$(curl -sS \
  -X POST "${SPARKI_API_BASE}/business/projects/batch" \
  -H "X-API-Key: $SPARKI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"project_ids\":[\"${PROJECT_ID}\"]}")

HTTP_CODE=$(echo "$RESPONSE" | jq -r '.code // "unknown"')
MESSAGE=$(echo "$RESPONSE" | jq -r '.message // "unknown"')

if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "0" ]]; then
  echo "Error: Query failed (code=$HTTP_CODE): $MESSAGE" >&2
  exit 1
fi

STATUS=$(echo "$RESPONSE" | jq -r '.data.projects[0].status // empty')
if [[ -z "$STATUS" ]]; then
  echo "Error: Project not found: $PROJECT_ID" >&2
  exit 1
fi

case "$STATUS" in
  completed)
    RESULT_URL=$(echo "$RESPONSE" | jq -r '.data.projects[0].result_url // .data.projects[0].output_videos[0].url // empty')
    echo "completed ${RESULT_URL}"
    exit 0
    ;;
  failed)
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.data.projects[0].error // "unknown error"')
    echo "failed ${ERROR_MSG}"
    exit 0
    ;;
  *)
    # Still in progress — caller should poll
    echo "processing"
    exit 2
    ;;
esac
