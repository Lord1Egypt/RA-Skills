#!/bin/bash
# meter.sh — Single entry point for /meter skill
# Checks setup, backfills if needed, shows spend summary. One script, one prompt.

set -uo pipefail

SPEND_DIR="$HOME/.agent-meter"
SPEND_FILE="$SPEND_DIR/spend.jsonl"
CLAUDE_PROJECTS="$HOME/.claude/projects"

mkdir -p "$SPEND_DIR"

# --- Find skill directory ---
SKILL_DIR=""
for d in "$HOME/.claude/skills/agent-meter" "$HOME/.claude/skills/meter" ".claude/skills/meter" ".claude/skills/agent-meter"; do
  if [ -f "$d/meter-session-end.sh" ]; then
    SKILL_DIR="$d"
    break
  fi
done

# --- Check & install hook ---
if [ ! -f ".claude/hooks/meter-session-end.sh" ]; then
  if [ -n "$SKILL_DIR" ]; then
    mkdir -p .claude/hooks
    cp "$SKILL_DIR/meter-session-end.sh" .claude/hooks/
    chmod +x .claude/hooks/meter-session-end.sh
    echo "SETUP: Installed session-end hook to .claude/hooks/"
  else
    echo "ERROR: meter-session-end.sh not found. Reinstall the agent-meter skill."
    exit 1
  fi
fi

# --- Ensure Stop hook is wired in settings.json ---
SETTINGS_FILE=".claude/settings.json"
HOOK_CMD="/bin/bash .claude/hooks/meter-session-end.sh"
if [ -f "$SETTINGS_FILE" ]; then
  # Check if the hook command is already present
  if ! jq -e '.hooks.Stop[0].hooks[]? | select(.command == "'"$HOOK_CMD"'")' "$SETTINGS_FILE" >/dev/null 2>&1; then
    # Merge the Stop hook into existing settings
    jq --arg cmd "$HOOK_CMD" '
      .hooks //= {} |
      .hooks.Stop //= [{"hooks": []}] |
      .hooks.Stop[0].hooks += [{"type": "command", "command": $cmd}]
    ' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
    echo "SETUP: Added Stop hook to $SETTINGS_FILE"
  fi
else
  # Create settings.json with the Stop hook
  mkdir -p .claude
  jq -n --arg cmd "$HOOK_CMD" '{
    hooks: {
      Stop: [{
        hooks: [{
          type: "command",
          command: $cmd
        }]
      }]
    }
  }' > "$SETTINGS_FILE"
  echo "SETUP: Created $SETTINGS_FILE with Stop hook"
fi

# --- Backfill from Claude Code transcripts ---
touch "$SPEND_FILE"

# Build set of already-tracked session IDs
SEEN_FILE=$(mktemp)
trap 'rm -f "$SEEN_FILE"' EXIT
jq -r '.session_id // empty' "$SPEND_FILE" 2>/dev/null | sort -u > "$SEEN_FILE"

BACKFILLED=0
for transcript in "$CLAUDE_PROJECTS"/*/*.jsonl; do
  [ -f "$transcript" ] || continue

  SESSION_ID=$(basename "$transcript" .jsonl)

  # Skip already tracked
  grep -qx "$SESSION_ID" "$SEEN_FILE" 2>/dev/null && continue

  # Project from directory name
  PROJECT_DIR=$(basename "$(dirname "$transcript")")
  PROJECT=$(echo "$PROJECT_DIR" | sed 's/^-$/unknown/; s/.*-//')

  # Extract usage — single jq -s pass
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

  [ "$USAGE" != "null" ] && [ -n "$USAGE" ] || continue

  TOTAL_CALLS=$(echo "$USAGE" | jq -r '.total_calls')
  [ "$TOTAL_CALLS" != "0" ] || continue

  MODEL=$(echo "$USAGE" | jq -r '.model')
  TOKENS_IN=$(echo "$USAGE" | jq -r '.tokens_in')
  TOKENS_OUT=$(echo "$USAGE" | jq -r '.tokens_out')
  CACHE_CREATION=$(echo "$USAGE" | jq -r '.cache_creation')
  CACHE_READ=$(echo "$USAGE" | jq -r '.cache_read')

  TS=$(jq -r '.timestamp // empty' "$transcript" 2>/dev/null | head -1)
  [ -n "$TS" ] || TS=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

  COST_USD=$(echo "$TOKENS_IN $TOKENS_OUT $CACHE_CREATION $CACHE_READ" | awk -v model="$MODEL" '{
    tin=$1; tout=$2; ccreate=$3; cread=$4
    if (model ~ /opus/)        { pin=15.0;  pout=75.0 }
    else if (model ~ /sonnet/) { pin=3.0;   pout=15.0 }
    else if (model ~ /haiku/)  { pin=0.25;  pout=1.25 }
    else                       { pin=3.0;   pout=15.0 }
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
      type: $type, ts: $ts, api: $api, model: $model,
      session_id: $session_id, project: $project,
      total_calls: $total_calls, tokens_in: $tokens_in,
      tokens_out: $tokens_out, cache_creation: $cache_creation,
      cache_read: $cache_read, cost_usd: ($cost_usd | tonumber),
      source: $source
    }' >> "$SPEND_FILE"

  BACKFILLED=$((BACKFILLED + 1))
done

[ "$BACKFILLED" -gt 0 ] && echo "Backfilled $BACKFILLED new sessions."

# --- Show spend summary ---
RECORD_COUNT=$(wc -l < "$SPEND_FILE" | tr -d ' ')
if [ "$RECORD_COUNT" = "0" ]; then
  echo "No spend data yet. The session-end hook will start capturing after your next session."
  exit 0
fi

TODAY=$(date -u +"%Y-%m-%d")

echo "## Today ($TODAY)"
jq -s "[.[] | select(.ts | startswith(\"$TODAY\"))]" "$SPEND_FILE" | jq -r '
  if length == 0 then "  No sessions today"
  else
    "  Sessions: \(length)\n" +
    "  Output tokens: \(map(.tokens_out) | add // 0 | . / 1000 | floor)K\n" +
    "  Cost: $\(map(.cost_usd) | add // 0 | . * 100 | round / 100)\n" +
    "  By project: " + (group_by(.project) | map("\(.[0].project) $\(map(.cost_usd) | add // 0 | . * 100 | round / 100)") | join(", "))
  end
' 2>/dev/null || echo "  (no data)"

echo ""
echo "## All Time"
jq -s '
  "  Sessions: \(length)\n" +
  "  Output tokens: \(map(.tokens_out) | add // 0 | . / 1000 | floor)K\n" +
  "  Cache read: \(map(.cache_read) | add // 0 | . / 1000000 | . * 100 | round / 100)M\n" +
  "  Total cost: $\(map(.cost_usd) | add // 0 | . * 100 | round / 100)\n\n" +
  "  By Project:\n" +
  (group_by(.project) | map(
    "    \(.[0].project): \(length) sessions, $\(map(.cost_usd) | add // 0 | . * 100 | round / 100)"
  ) | sort | reverse | join("\n")) +
  "\n\n  By Model:\n" +
  (group_by(.model) | map(
    "    \(.[0].model): \(length) sessions, $\(map(.cost_usd) | add // 0 | . * 100 | round / 100)"
  ) | sort | reverse | join("\n"))
' "$SPEND_FILE" -r 2>/dev/null || echo "  (no data)"

# --- Sync hint ---
if [ ! -f "$SPEND_DIR/sync.json" ]; then
  echo ""
  echo "TIP: Sync to the dashboard at dashboard.agentmeter.io:"
  echo "  bash .claude/skills/agent-meter/meter-sync.sh --setup"
fi
