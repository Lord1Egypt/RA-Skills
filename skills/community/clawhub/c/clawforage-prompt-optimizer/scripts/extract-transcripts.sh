#!/bin/bash
# extract-transcripts.sh — Parse JSONL transcripts into a structured text summary
# Usage: extract-transcripts.sh <jsonl_file_or_dir> [days_back]
# Output: Structured text summary to stdout
set -euo pipefail

INPUT="${1:?Usage: extract-transcripts.sh <jsonl_file_or_dir> [days_back]}"
DAYS_BACK="${2:-7}"

# Collect JSONL files
FILES=()
if [ -d "$INPUT" ]; then
  while IFS= read -r f; do FILES+=("$f"); done < <(find "$INPUT" -name "*.jsonl" -type f)
else
  FILES=("$INPUT")
fi

if [ ${#FILES[@]} -eq 0 ]; then
  echo "No JSONL files found in $INPUT"
  exit 1
fi

# Read all files into a single stream
ALL_MESSAGES=""
for FILE in "${FILES[@]}"; do
  ALL_MESSAGES+=$(cat "$FILE")
  ALL_MESSAGES+=$'\n'
done

# Extract user questions
echo "=== USER QUESTIONS ==="
echo "$ALL_MESSAGES" | jq -r '
  select(.type == "message" and .message.role == "user")
  | .timestamp + " | " + (.message.content[] | select(.type == "text") | .text)
' 2>/dev/null | sort || true

# Find repeated questions (exact match for MVP)
echo ""
echo "=== REPEATED PATTERNS ==="
echo "$ALL_MESSAGES" | jq -r '
  select(.type == "message" and .message.role == "user")
  | (.message.content[] | select(.type == "text") | .text)
' 2>/dev/null | sort | uniq -c | sort -rn | head -10 | while read -r count question; do
  if [ "$count" -gt 1 ]; then
    echo "  ${count}x repeated: $question"
  fi
done || true

# Extract tool usage
echo ""
echo "=== TOOL USAGE ==="
echo "$ALL_MESSAGES" | jq -r '
  select(.type == "message" and .message.role == "assistant")
  | .message.content[]
  | select(.type == "toolUse")
  | .name
' 2>/dev/null | sort | uniq -c | sort -rn || true

# Extract failures (assistant messages containing error indicators)
echo ""
echo "=== FAILURES & ERRORS ==="
echo "$ALL_MESSAGES" | jq -r '
  select(.type == "message" and .message.role == "assistant")
  | .timestamp as $ts
  | .message.content[]
  | select(.type == "text")
  | select(.text | test("error|Error|ERROR|fail|Fail|FAIL|exception|Exception"; "i"))
  | $ts + " | " + .text
' 2>/dev/null | head -20 || true

# Cost summary
echo ""
echo "=== COST SUMMARY ==="
TOTAL_COST=$(echo "$ALL_MESSAGES" | jq -r '
  select(.type == "message" and .message.role == "assistant" and .message.usage.cost.total != null)
  | .message.usage.cost.total
' 2>/dev/null | awk '{s+=$1} END {printf "%.4f", s}' || echo "0")
MSG_COUNT=$(echo "$ALL_MESSAGES" | jq -r '
  select(.type == "message" and .message.role == "user")
  | .timestamp
' 2>/dev/null | wc -l | tr -d ' ' || echo "0")
echo "Total cost: \$${TOTAL_COST}"
echo "Total user messages: ${MSG_COUNT}"
if [ "$MSG_COUNT" -gt 0 ]; then
  AVG=$(echo "$TOTAL_COST $MSG_COUNT" | awk '{printf "%.4f", $1/$2}')
  echo "Average cost per interaction: \$${AVG}"
fi
