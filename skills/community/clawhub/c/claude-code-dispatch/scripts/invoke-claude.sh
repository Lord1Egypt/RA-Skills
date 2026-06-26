#!/usr/bin/env bash
set -euo pipefail

# claude-code-dispatch: invoke Claude Code CLI as a subprocess
# Part of the claude-code-dispatch OpenClaw skill
# Author: Claude Code (Anthropic)

# --- Defaults ---
MODEL="sonnet"
TOOLS="Read,Edit,Glob,Grep"
BUDGET="2.00"
TIMEOUT=300
PROMPT=""
WORKDIR=""
SYSTEM_PROMPT=""

# --- Structured error output ---
error_exit() {
  local category="$1"
  local message="$2"
  echo "ERROR: ${category}: ${message}" >&2
  case "$category" in
    MISSING_DEPENDENCY|MISSING_PARAMETER|INVALID_WORKDIR) exit 2 ;;
    TIMEOUT) exit 3 ;;
    *) exit 1 ;;
  esac
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)  PROMPT="$2";        shift 2 ;;
    --workdir) WORKDIR="$2";       shift 2 ;;
    --model)   MODEL="$2";         shift 2 ;;
    --tools)   TOOLS="$2";         shift 2 ;;
    --budget)  BUDGET="$2";        shift 2 ;;
    --timeout) TIMEOUT="$2";       shift 2 ;;
    --system)  SYSTEM_PROMPT="$2"; shift 2 ;;
    *)
      error_exit "MISSING_PARAMETER" "Unknown argument: $1"
      ;;
  esac
done

# --- Preflight checks ---
if [[ -z "$PROMPT" ]]; then
  error_exit "MISSING_PARAMETER" "--prompt is required"
fi

if [[ -z "$WORKDIR" ]]; then
  error_exit "MISSING_PARAMETER" "--workdir is required"
fi

if [[ ! -d "$WORKDIR" ]]; then
  error_exit "INVALID_WORKDIR" "Directory does not exist: $WORKDIR"
fi

if ! command -v claude &>/dev/null; then
  error_exit "MISSING_DEPENDENCY" "claude (Claude Code CLI) is not installed or not on PATH"
fi

if ! command -v jq &>/dev/null; then
  error_exit "MISSING_DEPENDENCY" "jq is not installed or not on PATH"
fi

# Resolve timeout command (macOS coreutils installs as gtimeout)
TIMEOUT_CMD=""
if command -v timeout &>/dev/null; then
  TIMEOUT_CMD="timeout"
elif command -v gtimeout &>/dev/null; then
  TIMEOUT_CMD="gtimeout"
else
  echo "WARNING: timeout/gtimeout not available, --timeout will be ignored. Install coreutils for timeout support." >&2
fi

# --- Build claude command ---
CLAUDE_ARGS=(
  -p
  --model "$MODEL"
  --output-format json
  --no-session-persistence
  --max-budget-usd "$BUDGET"
)

if [[ -n "$TOOLS" ]]; then
  CLAUDE_ARGS+=(--tools "$TOOLS")
fi

if [[ -n "$SYSTEM_PROMPT" ]]; then
  CLAUDE_ARGS+=(--append-system-prompt "$SYSTEM_PROMPT")
fi

# --- Execute ---
cd "$WORKDIR"

STDOUT_FILE=$(mktemp)
STDERR_FILE=$(mktemp)
trap 'rm -f "$STDOUT_FILE" "$STDERR_FILE"' EXIT

EXIT_CODE=0
if [[ -n "$TIMEOUT_CMD" ]]; then
  echo "$PROMPT" | "$TIMEOUT_CMD" "$TIMEOUT" claude "${CLAUDE_ARGS[@]}" \
    >"$STDOUT_FILE" 2>"$STDERR_FILE" || EXIT_CODE=$?
else
  echo "$PROMPT" | claude "${CLAUDE_ARGS[@]}" \
    >"$STDOUT_FILE" 2>"$STDERR_FILE" || EXIT_CODE=$?
fi

# Check for timeout (exit code 124 from timeout/gtimeout)
if [[ $EXIT_CODE -eq 124 ]]; then
  error_exit "TIMEOUT" "Claude Code did not complete within ${TIMEOUT}s"
fi

# --- Parse output ---
RAW_OUTPUT=$(cat "$STDOUT_FILE")

if ! echo "$RAW_OUTPUT" | jq empty 2>/dev/null; then
  STDERR_CONTENT=$(cat "$STDERR_FILE")
  error_exit "PARSE_ERROR" "Claude Code did not return valid JSON. stderr: ${STDERR_CONTENT:-<empty>}"
fi

IS_ERROR=$(echo "$RAW_OUTPUT" | jq -r '.is_error // false')
RESULT=$(echo "$RAW_OUTPUT" | jq -r '.result // "No result returned"')
COST=$(echo "$RAW_OUTPUT" | jq -r '.total_cost_usd // 0')
DURATION_MS=$(echo "$RAW_OUTPUT" | jq -r '.duration_ms // 0')

# Convert duration to human-readable
DURATION_S=$(( DURATION_MS / 1000 ))
if [[ $DURATION_S -ge 60 ]]; then
  DURATION_MIN=$(( DURATION_S / 60 ))
  DURATION_REM=$(( DURATION_S % 60 ))
  DURATION_HUMAN="${DURATION_MIN}m${DURATION_REM}s"
else
  DURATION_HUMAN="${DURATION_S}s"
fi

# Format cost (locale-safe)
COST_FMT=$(LC_NUMERIC=C printf '$%.2f' "$COST")

# Truncate result at line boundary before 2000 chars
if [[ ${#RESULT} -gt 2000 ]]; then
  RESULT=$(echo "$RESULT" | head -c 2000)
  RESULT="${RESULT%$'\n'*}"
  RESULT="${RESULT}
... (truncated)"
fi

# Determine status
if [[ "$IS_ERROR" == "true" ]]; then
  STATUS="failure"
else
  STATUS="success"
fi

# --- Output summary ---
cat <<SUMMARY
STATUS: ${STATUS}
MODEL: ${MODEL}
COST: ${COST_FMT}
DURATION: ${DURATION_HUMAN}
RESULT: ${RESULT}
SUMMARY

# Exit with appropriate code
if [[ "$STATUS" == "failure" ]]; then
  exit 1
fi
exit 0
