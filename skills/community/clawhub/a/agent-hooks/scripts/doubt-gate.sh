#!/usr/bin/env bash
# doubt-gate.sh — Stop hook: block completion when agent uses speculative language
# Forces agent to provide concrete evidence before stopping.
# Uses a one-shot guard to prevent infinite loops.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"

INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
GUARD_FILE="${SESSION_DIR}/.doubt-gate-fired"

# If guard already fired this turn, unconditionally allow stop
if [ -f "$GUARD_FILE" ]; then
  rm -f "$GUARD_FILE"
  echo '{"continue":true}'
  exit 0
fi

# Extract last assistant message from hook input
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""' 2>/dev/null)
[ -z "$LAST_MSG" ] && echo '{"continue":true}' && exit 0

# Strip code blocks and blockquotes to avoid false positives
PROSE=$(echo "$LAST_MSG" | sed '/^```/,/^```/d; /^>/d; /^    /d')

# Check for hedging keywords (EN + ZH)
if echo "$PROSE" | grep -qiE \
  'I think|I believe|likely|maybe|might|probably|not sure|not certain|presumably|I assume|should be|could be|possibly|可能|大概|也许|应该是|我认为|我猜|不太确定|估计是'; then

  mkdir -p "$SESSION_DIR"
  touch "$GUARD_FILE"

  echo '{"decision":"block","reason":"Your response contains speculative language (\"maybe\", \"probably\", \"I think\", etc.). Before completing, you MUST provide concrete evidence: run a test, check a log, read the actual file, or verify with a command. Do not guess — verify."}'
else
  echo '{"continue":true}'
fi
