#!/usr/bin/env bash
# gemini-run.sh — Run Gemini CLI headlessly with workspace access
#
# Usage:
#   gemini-run.sh <prompt-file> <include-dirs> [output-file]
#
# Arguments:
#   prompt-file    Path to a file containing the prompt text
#   include-dirs   Comma-separated list of absolute dirs to include
#                  e.g. "/root/.openclaw/workspace,/tmp/task-output"
#   output-file    (Optional) Capture stdout to this file (also prints to terminal)
#
# Environment variables:
#   GEMINI_TIMEOUT   Timeout in seconds (default: 300)
#   GEMINI_MODEL     Model override (default: gemini-2.5-pro-preview-03-25)
#
# Examples:
#   # Basic usage
#   gemini-run.sh /tmp/prompt.txt /tmp/task-dir
#
#   # With output capture
#   gemini-run.sh /tmp/prompt.txt "/root/workspace,/tmp" /tmp/results.txt
#
#   # With model override
#   GEMINI_MODEL=gemini-2.0-flash gemini-run.sh /tmp/prompt.txt /tmp/dir
#
#   # With longer timeout (e.g. large codebase analysis)
#   GEMINI_TIMEOUT=600 gemini-run.sh /tmp/prompt.txt /path/to/big-repo
#
# Notes:
#   - All include-dirs must be absolute paths that exist before running
#   - gemini must be authenticated (run `gemini` interactively once first)
#   - See references/troubleshooting.md for common errors

set -euo pipefail

# --- Args ---
PROMPT_FILE="${1:?Usage: gemini-run.sh <prompt-file> <include-dirs> [output-file]}"
INCLUDE_DIRS="${2:?Provide comma-separated include dirs (absolute paths)}"
OUTPUT_FILE="${3:-}"

# --- Config ---
TIMEOUT="${GEMINI_TIMEOUT:-300}"
MODEL="${GEMINI_MODEL:-}"

# --- Validation ---
if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

# Check gemini is installed
if ! command -v gemini &>/dev/null; then
  echo "ERROR: gemini CLI not found. Install with: npm install -g @google/gemini-cli" >&2
  exit 1
fi

# Validate include dirs exist
IFS=',' read -ra DIRS <<< "$INCLUDE_DIRS"
for DIR in "${DIRS[@]}"; do
  DIR="${DIR// /}"  # trim spaces
  if [ ! -d "$DIR" ]; then
    echo "WARNING: Include dir does not exist: $DIR (creating it)" >&2
    mkdir -p "$DIR"
  fi
done

PROMPT=$(cat "$PROMPT_FILE")
PROMPT_LEN=${#PROMPT}

echo "─────────────────────────────────────────" >&2
echo "gemini-run.sh" >&2
echo "  Prompt file:    $PROMPT_FILE ($PROMPT_LEN chars)" >&2
echo "  Include dirs:   $INCLUDE_DIRS" >&2
echo "  Output file:    ${OUTPUT_FILE:-<stdout>}" >&2
echo "  Timeout:        ${TIMEOUT}s" >&2
echo "  Model:          ${MODEL:-default}" >&2
echo "─────────────────────────────────────────" >&2

# --- Build command ---
CMD=(
  timeout "$TIMEOUT"
  gemini
  --include-directories "$INCLUDE_DIRS"
  --yolo
)

if [ -n "$MODEL" ]; then
  CMD+=(--model "$MODEL")
fi

CMD+=(-p "$PROMPT")

# --- Execute ---
START_TIME=$(date +%s)

if [ -n "$OUTPUT_FILE" ]; then
  "${CMD[@]}" 2>&1 | tee "$OUTPUT_FILE"
  EXIT_CODE="${PIPESTATUS[0]}"
else
  "${CMD[@]}" 2>&1
  EXIT_CODE=$?
fi

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "" >&2
echo "─────────────────────────────────────────" >&2
if [ "$EXIT_CODE" -eq 0 ]; then
  echo "✅ Done in ${ELAPSED}s" >&2
elif [ "$EXIT_CODE" -eq 124 ]; then
  echo "⏱️  Timed out after ${TIMEOUT}s" >&2
  exit 1
else
  echo "❌ Failed with exit code $EXIT_CODE (${ELAPSED}s)" >&2
  exit "$EXIT_CODE"
fi
echo "─────────────────────────────────────────" >&2
