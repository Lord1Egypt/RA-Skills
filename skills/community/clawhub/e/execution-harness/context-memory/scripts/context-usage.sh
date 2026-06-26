#!/usr/bin/env bash
# context-usage.sh — Extract input token count from Claude Code transcript
# Usage: context-usage.sh <transcript-jsonl-path>
#
# IMPORTANT: Claude Code transcripts do NOT contain a context_window_size
# field. Context window data is only available via the statusLine stdin pipe
# (used by HUD plugins). This script can only report raw input_tokens from
# the last API response — it CANNOT compute a usage percentage.
#
# Output: "Input tokens: NNNNN" or nothing if unavailable

set -euo pipefail

TRANSCRIPT="${1:-}"
[ -z "$TRANSCRIPT" ] && exit 0
[ -f "$TRANSCRIPT" ] || exit 0

SIZE=$(stat -f%z "$TRANSCRIPT" 2>/dev/null || stat -c%s "$TRANSCRIPT" 2>/dev/null || echo 0)
[ "$SIZE" -lt 100 ] && exit 0

# Get the last complete JSONL line (use tail -1, not tail -c 4096,
# because real JSONL lines can be 20KB+)
LAST_LINE=$(tail -1 "$TRANSCRIPT" 2>/dev/null)
[ -z "$LAST_LINE" ] && exit 0

# Extract input_tokens from nested usage object (real format: "usage":{"input_tokens":N,...})
INPUT_TOKENS=$(echo "$LAST_LINE" | jq -r '.usage.input_tokens // empty' 2>/dev/null || true)

# Filter out streaming placeholders (input_tokens <= 10 is likely a stream marker)
if [ -n "$INPUT_TOKENS" ] && [ "$INPUT_TOKENS" -gt 10 ] 2>/dev/null; then
  echo "Input tokens: ${INPUT_TOKENS}"
fi
