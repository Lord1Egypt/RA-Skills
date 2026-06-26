#!/usr/bin/env bash
# amp-task.sh — Non-interactive wrapper for Sourcegraph Amp
#
# Usage:
#   bash amp-task.sh --task "description" --dir /path/to/project [--mode rush|smart|deep]
#
# Output:
#   THREAD_ID: <id>
#   <agent final response>
#
# Exit codes:
#   0  — success
#   1  — usage error
#   2  — amp execution error

set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────────────────

AMP_BIN="${AMP_BIN:-$(command -v amp 2>/dev/null || echo "/usr/local/bin/amp")}"

# ── Defaults ─────────────────────────────────────────────────────────────────

TASK=""
DIR=""
MODE="smart"

# ── Argument parsing ──────────────────────────────────────────────────────────

usage() {
  cat >&2 <<EOF
Usage: $(basename "$0") --task "description" --dir /path/to/project [--mode rush|smart|deep]

Options:
  --task   Task description to send to Amp (required)
  --dir    Project root directory (required, amp reads codebase from here)
  --mode   Agent mode: rush | smart | deep  (default: smart)
  --help   Show this help

Examples:
  bash amp-task.sh --task "add pagination" --dir /Users/jonc/clawd/invoicing
  bash amp-task.sh --task "write tests for utils" --dir /Users/jonc/clawd/app --mode rush
  bash amp-task.sh --task "refactor auth module" --dir /Users/jonc/clawd/app --mode deep
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task)
      TASK="$2"
      shift 2
      ;;
    --dir)
      DIR="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --help|-h)
      usage
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      ;;
  esac
done

# ── Validation ────────────────────────────────────────────────────────────────

if [[ -z "$TASK" ]]; then
  echo "Error: --task is required" >&2
  usage
fi

if [[ -z "$DIR" ]]; then
  echo "Error: --dir is required" >&2
  usage
fi

if [[ ! -d "$DIR" ]]; then
  echo "Error: directory does not exist: $DIR" >&2
  exit 1
fi

if [[ ! -x "$AMP_BIN" ]]; then
  echo "Error: amp binary not found or not executable: $AMP_BIN" >&2
  exit 1
fi

case "$MODE" in
  rush|smart|deep|free) ;;
  *)
    echo "Error: --mode must be one of: rush, smart, deep (got: $MODE)" >&2
    exit 1
    ;;
esac

# ── Create a thread for auditability ─────────────────────────────────────────
# We create the thread first so we have an ID to log/report.
# Then we continue it in execute mode with the actual task.

THREAD_ID=$("$AMP_BIN" threads new --no-notifications 2>/dev/null | tr -d '[:space:]')

if [[ -z "$THREAD_ID" ]]; then
  echo "Error: failed to create amp thread" >&2
  exit 2
fi

echo "THREAD_ID: $THREAD_ID"
echo "MODE: $MODE"
echo "DIR: $DIR"
echo "---"

# ── Run the task ──────────────────────────────────────────────────────────────
# - cd to project dir so amp sees the right codebase
# - Use `threads continue <id>` so the work is attached to our thread
# - Pipe task via stdin with -x for non-interactive execute mode
# - --dangerously-allow-all: no tool confirmation prompts
# - --no-notifications: no sound/system alerts
# - --no-ide: don't attempt IDE connection (safe for headless/agent use)
# - -m: set the agent mode

cd "$DIR"

printf '%s' "$TASK" | "$AMP_BIN" \
  threads continue "$THREAD_ID" \
  --dangerously-allow-all \
  --no-notifications \
  --no-ide \
  -m "$MODE" \
  -x

EXIT_CODE=$?

if [[ $EXIT_CODE -ne 0 ]]; then
  echo "" >&2
  echo "Error: amp exited with code $EXIT_CODE" >&2
  echo "Thread $THREAD_ID may be partially complete. Review with:" >&2
  echo "  $AMP_BIN threads markdown $THREAD_ID" >&2
  exit 2
fi
