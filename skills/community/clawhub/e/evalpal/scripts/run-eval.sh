#!/bin/sh
# run-eval.sh — Trigger an EvalPal evaluation run, poll for completion, and print results.
# Usage: bash scripts/run-eval.sh --eval-id <EVAL_DEFINITION_ID>
#
# Environment:
#   EVALPAL_API_KEY  (required) — API key for authentication
#   EVALPAL_API_URL  (optional) — Base URL (default: https://evalpal.dev)

set -e

# ---------------------------------------------------------------------------
# Defaults & argument parsing
# ---------------------------------------------------------------------------
API_URL="${EVALPAL_API_URL:-https://evalpal.dev}"
EVAL_ID=""

while [ $# -gt 0 ]; do
  case "$1" in
    --eval-id)  EVAL_ID="$2";  shift 2 ;;
    --help|-h)
      echo "Usage: bash run-eval.sh --eval-id <ID>"
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

if [ -z "$EVAL_ID" ]; then
  echo "Error: --eval-id is required"
  exit 1
fi

# Check for required tools
for tool in curl jq; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: '$tool' is required but not installed"
    exit 1
  fi
done

# ---------------------------------------------------------------------------
# Helper: make an authenticated API request
# ---------------------------------------------------------------------------
api_request() {
  _method="$1"
  _path="$2"
  _body="${3:-}"

  _curl_args="-s -w \n%{http_code} -X $_method"
  _curl_args="$_curl_args -H \"Authorization: Bearer \$EVALPAL_API_KEY\""
  _curl_args="$_curl_args -H \"Content-Type: application/json\""

  if [ -n "$_body" ]; then
    _response=$(curl -s -w "\n%{http_code}" -X "$_method" \
      -H "Authorization: Bearer $EVALPAL_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$_body" \
      "${API_URL}${_path}" 2>/dev/null) || {
      echo "Error: Could not reach EvalPal API" >&2
      exit 1
    }
  else
    _response=$(curl -s -w "\n%{http_code}" -X "$_method" \
      -H "Authorization: Bearer $EVALPAL_API_KEY" \
      -H "Content-Type: application/json" \
      "${API_URL}${_path}" 2>/dev/null) || {
      echo "Error: Could not reach EvalPal API" >&2
      exit 1
    }
  fi

  _http_code=$(echo "$_response" | tail -n1)
  _body_out=$(echo "$_response" | sed '$d')

  case "$_http_code" in
    2[0-9][0-9]) echo "$_body_out" ;;
    401) echo "Error: Authentication failed (401)" >&2; exit 1 ;;
    404) echo "Error: Eval definition not found (404)" >&2; exit 1 ;;
    429)
      _retry=$(echo "$_body_out" | jq -r '.retryAfter // "60"' 2>/dev/null || echo "60")
      echo "Error: Rate limited — retry after ${_retry}s (429)" >&2
      exit 1
      ;;
    *)  echo "Error: API returned HTTP $_http_code" >&2; exit 1 ;;
  esac
}

# ---------------------------------------------------------------------------
# Step 1: Trigger the eval run
# ---------------------------------------------------------------------------
echo "Starting evaluation run for eval definition: $EVAL_ID"

RUN_RESPONSE=$(api_request POST "/api/v1/evals/${EVAL_ID}/run" "{}")
RUN_ID=$(echo "$RUN_RESPONSE" | jq -r '.id')

if [ -z "$RUN_ID" ] || [ "$RUN_ID" = "null" ]; then
  echo "Error: Failed to create eval run"
  exit 1
fi

echo "Run created: $RUN_ID"

# ---------------------------------------------------------------------------
# Step 2: Poll for completion (exponential backoff, 5-minute timeout)
# ---------------------------------------------------------------------------
DELAY=2
MAX_DELAY=10
ELAPSED=0
TIMEOUT=300

while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  STATUS_RESPONSE=$(api_request GET "/api/v1/runs/${RUN_ID}")
  STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')

  case "$STATUS" in
    completed|failed) break ;;
    *)
      sleep "$DELAY"
      ELAPSED=$((ELAPSED + DELAY))
      DELAY=$((DELAY + DELAY / 2))
      [ "$DELAY" -gt "$MAX_DELAY" ] && DELAY=$MAX_DELAY
      ;;
  esac
done

if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
  echo "Error: Evaluation timed out after ${TIMEOUT}s"
  exit 1
fi

# ---------------------------------------------------------------------------
# Step 3: Fetch results
# ---------------------------------------------------------------------------
RESULTS_RESPONSE=$(api_request GET "/api/v1/runs/${RUN_ID}/results")

# ---------------------------------------------------------------------------
# Step 4: Format output
# ---------------------------------------------------------------------------
TOTAL=$(echo "$STATUS_RESPONSE" | jq -r '.totalTests // 0')
PASSED=$(echo "$STATUS_RESPONSE" | jq -r '.passedTests // 0')
FAILED=$(echo "$STATUS_RESPONSE" | jq -r '.failedTests // 0')

if [ "$STATUS" = "completed" ] && [ "$FAILED" -eq 0 ]; then
  echo ""
  echo "✅ Evaluation — PASSED ($PASSED/$TOTAL)"
else
  echo ""
  echo "❌ Evaluation — FAILED ($PASSED/$TOTAL)"
fi

# Print per-test-case results
RESULT_COUNT=$(echo "$RESULTS_RESPONSE" | jq 'length')
if [ "$RESULT_COUNT" -gt 0 ]; then
  i=0
  while [ "$i" -lt "$RESULT_COUNT" ]; do
    TC_ID=$(echo "$RESULTS_RESPONSE" | jq -r ".[$i].testCaseId")
    TC_PASS=$(echo "$RESULTS_RESPONSE" | jq -r ".[$i].overallPass")

    if [ "$i" -eq $((RESULT_COUNT - 1)) ]; then
      PREFIX="└──"
    else
      PREFIX="├──"
    fi

    if [ "$TC_PASS" = "true" ]; then
      echo "$PREFIX Test Case $TC_ID: ✓ PASS"
    else
      echo "$PREFIX Test Case $TC_ID: ✗ FAIL"
    fi

    i=$((i + 1))
  done
fi

# Summary line
echo ""
echo "Run ID: $RUN_ID · $TOTAL test cases · ${ELAPSED}s"

# Exit code
if [ "$STATUS" = "failed" ] || [ "$FAILED" -gt 0 ]; then
  exit 1
fi

exit 0
