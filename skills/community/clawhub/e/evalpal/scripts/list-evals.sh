#!/bin/sh
# list-evals.sh — List available EvalPal evaluation definitions.
# Usage: bash scripts/list-evals.sh [--project-id <PROJECT_ID>]
#
# Environment:
#   EVALPAL_API_KEY  (required) — API key for authentication
#   EVALPAL_API_URL  (optional) — Base URL (default: https://evalpal.dev)

set -e

# ---------------------------------------------------------------------------
# Defaults & argument parsing
# ---------------------------------------------------------------------------
API_URL="${EVALPAL_API_URL:-https://evalpal.dev}"
PROJECT_ID=""

while [ $# -gt 0 ]; do
  case "$1" in
    --project-id)  PROJECT_ID="$2";  shift 2 ;;
    --help|-h)
      echo "Usage: bash list-evals.sh [--project-id <ID>]"
      echo ""
      echo "Lists all evaluation definitions. Optionally filter by project."
      echo ""
      echo "Environment:"
      echo "  EVALPAL_API_KEY   API key (required)"
      echo "  EVALPAL_API_URL   Base URL (default: https://evalpal.dev)"
      exit 0
      ;;
    *)  echo "Error: Unknown argument: $1"; exit 1 ;;
  esac
done

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
if [ -z "$EVALPAL_API_KEY" ]; then
  echo "Error: EVALPAL_API_KEY is not set"
  exit 1
fi

for tool in curl jq; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: '$tool' is required but not installed"
    exit 1
  fi
done

# ---------------------------------------------------------------------------
# Helper: authenticated GET request
# ---------------------------------------------------------------------------
api_get() {
  _path="$1"

  _response=$(curl -s -w "\n%{http_code}" -X GET \
    -H "Authorization: Bearer $EVALPAL_API_KEY" \
    -H "Content-Type: application/json" \
    "${API_URL}${_path}" 2>/dev/null) || {
    echo "Error: Could not reach EvalPal API" >&2
    exit 1
  }

  _http_code=$(echo "$_response" | tail -n1)
  _body=$(echo "$_response" | sed '$d')

  case "$_http_code" in
    2[0-9][0-9]) echo "$_body" ;;
    401) echo "Error: Authentication failed (401)" >&2; exit 1 ;;
    429)
      _retry=$(echo "$_body" | jq -r '.retryAfter // "60"' 2>/dev/null || echo "60")
      echo "Error: Rate limited — retry after ${_retry}s (429)" >&2
      exit 1
      ;;
    *)  echo "Error: API returned HTTP $_http_code" >&2; exit 1 ;;
  esac
}

# ---------------------------------------------------------------------------
# Fetch and display
# ---------------------------------------------------------------------------
echo "📋 Evaluation Definitions"
echo ""

if [ -n "$PROJECT_ID" ]; then
  # Single project mode
  EVALS=$(api_get "/api/v1/projects/${PROJECT_ID}/eval-definitions")
  EVAL_COUNT=$(echo "$EVALS" | jq 'length')

  if [ "$EVAL_COUNT" -eq 0 ]; then
    echo "  (no evaluations found)"
  else
    i=0
    while [ "$i" -lt "$EVAL_COUNT" ]; do
      EVAL_ID=$(echo "$EVALS" | jq -r ".[$i].id")
      EVAL_NAME=$(echo "$EVALS" | jq -r ".[$i].name")
      echo "  $EVAL_ID  $EVAL_NAME"
      i=$((i + 1))
    done
  fi
else
  # All projects mode
  PROJECTS=$(api_get "/api/v1/projects")
  PROJECT_COUNT=$(echo "$PROJECTS" | jq 'length')

  if [ "$PROJECT_COUNT" -eq 0 ]; then
    echo "  (no projects found)"
    exit 0
  fi

  p=0
  while [ "$p" -lt "$PROJECT_COUNT" ]; do
    P_ID=$(echo "$PROJECTS" | jq -r ".[$p].id")
    P_NAME=$(echo "$PROJECTS" | jq -r ".[$p].name")

    echo "Project: $P_NAME"

    EVALS=$(api_get "/api/v1/projects/${P_ID}/eval-definitions")
    EVAL_COUNT=$(echo "$EVALS" | jq 'length')

    if [ "$EVAL_COUNT" -eq 0 ]; then
      echo "  (no evaluations)"
    else
      i=0
      while [ "$i" -lt "$EVAL_COUNT" ]; do
        EVAL_ID=$(echo "$EVALS" | jq -r ".[$i].id")
        EVAL_NAME=$(echo "$EVALS" | jq -r ".[$i].name")
        echo "  $EVAL_ID  $EVAL_NAME"
        i=$((i + 1))
      done
    fi

    echo ""
    p=$((p + 1))
  done
fi
