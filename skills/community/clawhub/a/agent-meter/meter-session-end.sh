#!/bin/bash
# meter-session-end.sh — Stop hook for Claude Code
# Parses the session transcript for Claude Code's own token usage,
# then writes a session_summary record to ~/.agent-meter/spend.jsonl.
#
# This captures the REAL spend — Claude Code's own API calls to Anthropic,
# not just explicit curl commands caught by meter-capture.sh.

set -euo pipefail

SPEND_DIR="$HOME/.agent-meter"
SPEND_FILE="$SPEND_DIR/spend.jsonl"

mkdir -p "$SPEND_DIR"

# Read stdin for session context
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null) || SESSION_ID=""
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null) || TRANSCRIPT=""
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null) || CWD=""

# Need session_id to write a record
[ -n "$SESSION_ID" ] || exit 0

PROJECT=""
if [ -n "$CWD" ]; then
  PROJECT=$(basename "$CWD")
fi

TS=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

# Parse the session transcript for token usage
# Each assistant message has: message.usage.input_tokens, message.usage.output_tokens
if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  USAGE=$(jq -s '
    [.[] | select(.type == "assistant" and .message.usage != null) | .message.usage] |
    {
      total_calls: length,
      tokens_in: (map(.input_tokens // 0) | add // 0),
      tokens_out: (map(.output_tokens // 0) | add // 0),
      cache_creation: (map(.cache_creation_input_tokens // 0) | add // 0),
      cache_read: (map(.cache_read_input_tokens // 0) | add // 0)
    }
  ' "$TRANSCRIPT" 2>/dev/null) || USAGE=""

  if [ -n "$USAGE" ]; then
    TOTAL_CALLS=$(echo "$USAGE" | jq -r '.total_calls')
    TOKENS_IN=$(echo "$USAGE" | jq -r '.tokens_in')
    TOKENS_OUT=$(echo "$USAGE" | jq -r '.tokens_out')
    CACHE_CREATION=$(echo "$USAGE" | jq -r '.cache_creation')
    CACHE_READ=$(echo "$USAGE" | jq -r '.cache_read')

    # Skip if no actual usage
    [ "$TOTAL_CALLS" != "0" ] || exit 0

    # Detect model from transcript (first assistant message with model field)
    # Stream instead of slurp — handles large transcripts without loading all into memory
    MODEL=$(jq -r 'select(.type == "assistant" and .message.model != null) | .message.model' "$TRANSCRIPT" 2>/dev/null | head -1) || MODEL="unknown"
    [ -n "$MODEL" ] || MODEL="unknown"

    # Estimate cost — use effective input tokens (input + cache_creation, cache_read is cheaper)
    # Cache read tokens are ~10% of input price for Anthropic
    COST_USD=$(echo "$TOKENS_IN $TOKENS_OUT $CACHE_CREATION $CACHE_READ" | awk -v model="$MODEL" '{
      tin=$1; tout=$2; ccreate=$3; cread=$4
      # Per-1M-token pricing
      if (model ~ /opus/)    { pin=15.0;  pout=75.0 }
      else if (model ~ /sonnet/) { pin=3.0;   pout=15.0 }
      else if (model ~ /haiku/)  { pin=0.25;  pout=1.25 }
      else                       { pin=3.0;   pout=15.0 }
      # cache_creation costs 25% more, cache_read costs 90% less
      cost = (tin * pin + ccreate * pin * 1.25 + cread * pin * 0.1 + tout * pout) / 1000000
      printf "%.6f", cost
    }')

    jq -n -c \
      --arg type "session_summary" \
      --arg ts "$TS" \
      --arg api "api.anthropic.com" \
      --arg model "$MODEL" \
      --arg session_id "$SESSION_ID" \
      --arg project "$PROJECT" \
      --argjson total_calls "$TOTAL_CALLS" \
      --argjson tokens_in "$TOKENS_IN" \
      --argjson tokens_out "$TOKENS_OUT" \
      --argjson cache_creation "$CACHE_CREATION" \
      --argjson cache_read "$CACHE_READ" \
      --argjson cost_usd "${COST_USD:-0}" \
      --arg source "hook" \
      '{
        type: $type,
        ts: $ts,
        api: $api,
        model: $model,
        session_id: $session_id,
        project: $project,
        total_calls: $total_calls,
        tokens_in: $tokens_in,
        tokens_out: $tokens_out,
        cache_creation: $cache_creation,
        cache_read: $cache_read,
        cost_usd: ($cost_usd | tonumber),
        source: $source
      }' > "$SPEND_DIR/pending_${SESSION_ID}.jsonl"

    # Dedup: remove any prior record for this session, then append the new one
    if grep -q "\"session_id\":\"$SESSION_ID\"" "$SPEND_FILE" 2>/dev/null; then
      grep -v "\"session_id\":\"$SESSION_ID\"" "$SPEND_FILE" > "$SPEND_DIR/spend_dedup.jsonl" || true
      mv "$SPEND_DIR/spend_dedup.jsonl" "$SPEND_FILE"
    fi
    cat "$SPEND_DIR/pending_${SESSION_ID}.jsonl" >> "$SPEND_FILE"
    rm -f "$SPEND_DIR/pending_${SESSION_ID}.jsonl"
  fi
fi
