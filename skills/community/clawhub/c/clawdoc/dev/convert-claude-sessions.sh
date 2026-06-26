#!/usr/bin/env bash
set -uo pipefail

# convert-claude-sessions.sh
# Converts real Claude Code session JSONL files to OpenClaw format
# that clawdoc's diagnose.sh can process.
#
# Usage: convert-claude-sessions.sh <input-dir> <output-dir> [max-files]

if [ -z "${1:-}" ]; then
  echo "Usage: convert-claude-sessions.sh <input-dir> [output-dir] [max-files]" >&2
  echo "  input-dir   Directory containing Claude Code session JSONL files (required)" >&2
  echo "  output-dir  Where to write converted files (default: tests/fixtures/real)" >&2
  echo "  max-files   Maximum files to convert (default: 100)" >&2
  exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="${2:-$(dirname "$0")/../tests/fixtures/real}"
MAX_FILES="${3:-100}"

if [ ! -d "$INPUT_DIR" ]; then
  echo "Error: input directory '$INPUT_DIR' does not exist." >&2
  exit 1
fi

if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]; then
  echo "Output directory '$OUTPUT_DIR' exists and is not empty."
  printf "Remove it and regenerate? [y/N] "
  read -r CONFIRM
  if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Aborted." >&2
    exit 1
  fi
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Find all session JSONL files (limit to MAX_FILES)
FILES=()
COUNT=0
while IFS= read -r -d '' f; do
  FILES+=("$f")
  COUNT=$((COUNT + 1))
  if [ "$COUNT" -ge "$MAX_FILES" ]; then break; fi
done < <(find "$INPUT_DIR" -name "*.jsonl" -type f -print0 2>/dev/null)

echo "Found ${#FILES[@]} session files in $INPUT_DIR"
echo "Converting to OpenClaw format in $OUTPUT_DIR..."
echo ""

CONVERTED=0
SKIPPED=0

for f in "${FILES[@]}"; do
  # Skip very small files (< 3 lines)
  LINE_COUNT=$(wc -l < "$f" | tr -d ' ')
  if [ "$LINE_COUNT" -lt 3 ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  # Check if it has assistant messages with usage (limit scan to first 50 lines for speed)
  HAS_USAGE=$(head -50 "$f" | jq -c 'select(.type == "assistant" and .message.usage != null)' 2>/dev/null | head -1)
  if [ -z "$HAS_USAGE" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  CONVERTED=$((CONVERTED + 1))
  OUT_FILE="$OUTPUT_DIR/real-$(printf '%03d' $CONVERTED).jsonl"

  # Extract session metadata from first few lines (avoid scanning whole file)
  SESSION_ID=$(head -10 "$f" | jq -r 'select(.sessionId != null) | .sessionId' 2>/dev/null | head -1)
  MODEL_SLUG=$(head -20 "$f" | jq -r 'select(.type == "assistant") | .slug // "unknown"' 2>/dev/null | head -1)
  FIRST_TS=$(head -5 "$f" | jq -r 'select(.timestamp != null) | .timestamp' 2>/dev/null | head -1)
  SESSION_ID="${SESSION_ID:-unknown-$CONVERTED}"
  MODEL_SLUG="${MODEL_SLUG:-unknown}"
  FIRST_TS="${FIRST_TS:-2026-03-13T10:00:00.000Z}"

  # Map model slug to model name
  MODEL_NAME="anthropic/claude-sonnet-4-6"
  case "$MODEL_SLUG" in
    *opus*) MODEL_NAME="anthropic/claude-opus-4-6" ;;
    *haiku*) MODEL_NAME="anthropic/claude-haiku-4-5" ;;
    *sonnet*) MODEL_NAME="anthropic/claude-sonnet-4-6" ;;
  esac

  # Write session header
  echo "{\"type\":\"session\",\"timestamp\":\"$FIRST_TS\",\"sessionId\":\"$SESSION_ID\",\"agentId\":\"main\",\"model\":\"$MODEL_NAME\",\"sessionKey\":\"agent:main:main\"}" > "$OUT_FILE"

  # Convert each message
  jq -c '
    if .type == "user" then
      # Check if this is a tool result or a user message
      (.message.content // []) as $content |
      if ($content | any(.type == "tool_result")) then
        # Convert tool_result
        {
          type: "message",
          timestamp: (.timestamp // "2026-03-13T10:00:00.000Z"),
          message: {
            role: "toolResult",
            content: [
              ($content[] | select(.type == "tool_result") |
                {type: "text", text: (.content // "(no output)" | if type == "array" then (map(.text // "") | join("\n")) elif type == "string" then . else tostring end)}
              )
            ]
          }
        }
      else
        # Regular user message
        {
          type: "message",
          timestamp: (.timestamp // "2026-03-13T10:00:00.000Z"),
          message: {
            role: "user",
            content: [
              ($content[] | select(.type == "text") | {type: "text", text: .text})
            ]
          }
        }
      end
    elif .type == "assistant" then
      (.message.content // []) as $content |
      (.message.usage // {}) as $usage |
      # Calculate cost estimate from tokens
      (($usage.input_tokens // 0) + ($usage.cache_read_input_tokens // 0)) as $input_tok |
      ($usage.output_tokens // 0) as $output_tok |
      # Rough cost: $3/M input, $15/M output for Sonnet
      (($input_tok * 0.000003) + ($output_tok * 0.000015)) as $cost |
      {
        type: "message",
        timestamp: (.timestamp // "2026-03-13T10:00:00.000Z"),
        message: {
          role: "assistant",
          content: [
            ($content[] |
              if .type == "tool_use" then
                {
                  type: "toolCall",
                  id: .id,
                  name: (if .name == "Bash" then "exec"
                         elif .name == "Read" then "read"
                         elif .name == "Write" then "write"
                         elif .name == "Edit" then "write"
                         else .name end),
                  input: (.input // {})
                }
              elif .type == "text" then
                {type: "text", text: .text}
              else empty end
            )
          ],
          usage: {
            inputTokens: $input_tok,
            outputTokens: $output_tok,
            contextTokens: 200000,
            cost: { total: $cost }
          }
        }
      }
    else empty end
  ' "$f" 2>/dev/null >> "$OUT_FILE" || true

  # Verify output is valid
  if ! jq -s '.' "$OUT_FILE" >/dev/null 2>&1; then
    rm -f "$OUT_FILE"
    CONVERTED=$((CONVERTED - 1))
    SKIPPED=$((SKIPPED + 1))
  fi
done

echo "Converted: $CONVERTED"
echo "Skipped: $SKIPPED (too small or no usage data)"
echo "Output: $OUTPUT_DIR/"
