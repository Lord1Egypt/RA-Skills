#!/bin/bash
# meter-parse-claude-sessions.sh — Parse Claude Code transcripts into spend records
#
# Scans ~/.claude/projects/*/*.jsonl for session transcripts.
# Extracts per-session usage (tokens, model, cost) and writes to ~/.agent-meter/spend.jsonl.
# Deduplicates by session_id — safe to run repeatedly.
#
# Dependencies: jq, bash 4+

set -uo pipefail

SPEND_DIR="$HOME/.agent-meter"
SPEND_FILE="$SPEND_DIR/spend.jsonl"
CLAUDE_PROJECTS="$HOME/.claude/projects"

mkdir -p "$SPEND_DIR"
touch "$SPEND_FILE"

# Build set of already-processed session IDs (one per line, for grep lookup)
SEEN_FILE=$(mktemp)
jq -r '.session_id // empty' "$SPEND_FILE" 2>/dev/null | sort -u > "$SEEN_FILE"
trap 'rm -f "$SEEN_FILE"' EXIT

NEW=0
SKIPPED=0

for transcript in "$CLAUDE_PROJECTS"/*/*.jsonl; do
  [ -f "$transcript" ] || continue

  # Session ID = filename without .jsonl
  SESSION_ID=$(basename "$transcript" .jsonl)

  # Skip if already processed
  if grep -qx "$SESSION_ID" "$SEEN_FILE" 2>/dev/null; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  # Project = parent directory name, cleaned up
  PROJECT_DIR=$(basename "$(dirname "$transcript")")
  # Convert -Users-admin-oztenbot to oztenbot, -Users-admin to admin, - to unknown
  PROJECT=$(echo "$PROJECT_DIR" | sed 's/^-$/unknown/; s/.*-//')

  # Extract usage from assistant messages — single jq -s pass to avoid SIGPIPE
  USAGE=$(jq -s '
    [.[] | select(.type == "assistant" and .message.usage != null)] |
    if length == 0 then null
    else {
      total_calls: length,
      model: (map(.message.model) | map(select(. != null)) | first // "unknown"),
      tokens_in: (map(.message.usage.input_tokens // 0) | add // 0),
      cache_creation: (map(.message.usage.cache_creation_input_tokens // 0) | add // 0),
      cache_read: (map(.message.usage.cache_read_input_tokens // 0) | add // 0),
      tokens_out: (map(.message.usage.output_tokens // 0) | add // 0)
    } end
  ' "$transcript" 2>/dev/null) || continue

  # Skip empty sessions
  [ "$USAGE" != "null" ] && [ -n "$USAGE" ] || continue

  TOTAL_CALLS=$(echo "$USAGE" | jq -r '.total_calls')
  [ "$TOTAL_CALLS" != "0" ] || continue

  MODEL=$(echo "$USAGE" | jq -r '.model')
  TOKENS_IN=$(echo "$USAGE" | jq -r '.tokens_in')
  TOKENS_OUT=$(echo "$USAGE" | jq -r '.tokens_out')
  CACHE_CREATION=$(echo "$USAGE" | jq -r '.cache_creation')
  CACHE_READ=$(echo "$USAGE" | jq -r '.cache_read')

  # Get timestamp from first record in transcript
  TS=$(jq -r '.timestamp // empty' "$transcript" 2>/dev/null | head -1)
  [ -n "$TS" ] || TS=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

  # Calculate cost based on model
  COST_USD=$(echo "$TOKENS_IN $TOKENS_OUT $CACHE_CREATION $CACHE_READ" | awk -v model="$MODEL" '{
    tin=$1; tout=$2; ccreate=$3; cread=$4
    if (model ~ /opus/)       { pin=15.0;  pout=75.0 }
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
    --arg source "session_parse" \
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
    }' >> "$SPEND_FILE"

  NEW=$((NEW + 1))
done

echo "Parsed $NEW new sessions ($SKIPPED already tracked)"
