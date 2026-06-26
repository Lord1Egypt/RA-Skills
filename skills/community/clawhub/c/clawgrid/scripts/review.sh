#!/usr/bin/env bash
set -euo pipefail

# Publisher review operations: approve, reject, revision, and staged review.
#
# Usage:
#   bash review.sh approve <task_id>                      # approve task (pay earner)
#   bash review.sh reject <task_id> <reason>              # reject task
#   bash review.sh revision <task_id> <reason>            # request revision
#   bash review.sh stages <task_id>                       # list stages of a staged task
#   bash review.sh stage-approve <task_id> <stage_num>    # approve a specific stage
#   bash review.sh stage-reject <task_id> <stage_num> <reason>    # reject a stage
#   bash review.sh stage-revision <task_id> <stage_num> <reason>  # request revision on a stage

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 2 ]; then
  echo "Usage: bash $0 <action> <task_id> [args...]" >&2
  echo "" >&2
  echo "Actions:" >&2
  echo "  approve <task_id>                    — approve task and pay earner" >&2
  echo "  reject <task_id> <reason>            — reject task" >&2
  echo "  revision <task_id> <reason>          — request revision" >&2
  echo "  stages <task_id>                     — list stages of a staged task" >&2
  echo "  stage-approve <task_id> <stage_num>  — approve a specific stage" >&2
  echo "  stage-reject <task_id> <stage_num> <reason>" >&2
  echo "  stage-revision <task_id> <stage_num> <reason>" >&2
  exit 1
fi

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

ACTION="$1"
TASK_ID="$2"

case "$ACTION" in

  approve)
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/tasks/$TASK_ID/review" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"action":"approve"}' \
      --max-time 15)
    ;;

  reject)
    if [ $# -lt 3 ]; then
      echo "Usage: bash $0 reject <task_id> <reason>" >&2
      exit 1
    fi
    REASON="$3"
    BODY=$(python3 -c "import json; print(json.dumps({'action':'reject','reason':'''$REASON'''}))")
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/tasks/$TASK_ID/review" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" \
      --max-time 15)
    ;;

  revision)
    if [ $# -lt 3 ]; then
      echo "Usage: bash $0 revision <task_id> <reason>" >&2
      exit 1
    fi
    REASON="$3"
    BODY=$(python3 -c "import json; print(json.dumps({'action':'request_revision','reason':'''$REASON'''}))")
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/tasks/$TASK_ID/review" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" \
      --max-time 15)
    ;;

  stages)
    RESP=$(curl -s -w "\n%{http_code}" \
      "$API_BASE/api/lobster/tasks/$TASK_ID/stages" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    ;;

  stage-approve)
    if [ $# -lt 3 ]; then
      echo "Usage: bash $0 stage-approve <task_id> <stage_num>" >&2
      exit 1
    fi
    STAGE="$3"
    BODY=$(python3 -c "import json; print(json.dumps({'stage':int('$STAGE'),'action':'approve'}))")
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/tasks/$TASK_ID/stage-review" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" \
      --max-time 15)
    ;;

  stage-reject)
    if [ $# -lt 4 ]; then
      echo "Usage: bash $0 stage-reject <task_id> <stage_num> <reason>" >&2
      exit 1
    fi
    STAGE="$3"
    REASON="$4"
    BODY=$(python3 -c "import json; print(json.dumps({'stage':int('$STAGE'),'action':'reject','reason':'''$REASON'''}))")
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/tasks/$TASK_ID/stage-review" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" \
      --max-time 15)
    ;;

  stage-revision)
    if [ $# -lt 4 ]; then
      echo "Usage: bash $0 stage-revision <task_id> <stage_num> <reason>" >&2
      exit 1
    fi
    STAGE="$3"
    REASON="$4"
    BODY=$(python3 -c "import json; print(json.dumps({'stage':int('$STAGE'),'action':'request_revision','reason':'''$REASON'''}))")
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/tasks/$TASK_ID/stage-review" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" \
      --max-time 15)
    ;;

  *)
    echo "Unknown action: $ACTION" >&2
    echo "Valid actions: approve, reject, revision, stages, stage-approve, stage-reject, stage-revision" >&2
    exit 1
    ;;
esac

HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$RESP_BODY"
  exit 0
else
  echo "Review $ACTION failed (HTTP $HTTP_CODE): $RESP_BODY" >&2
  exit 1
fi
