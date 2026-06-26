#!/usr/bin/env bash
set -euo pipefail

# BurnThisShit -- Obliterate a session from orbit
# Usage: burn.sh <sessionId> [--force]
#
# NEVER burns anything outside the agent sessions directory.
# NEVER touches memory, skills, config, or any other data.
# Shreds files with 3-pass + zero-fill. Removes sessions.json entries.

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

# Agent resolved: first arg is always the sessionId
# OPENCLAW_AGENT env var sets the agent name (default: first arg of --agent or main)
AGENT="${OPENCLAW_AGENT:-main}"
SESSIONS_DIR="$HOME/.openclaw/agents/$AGENT/sessions"

# Safety: validate sessions dir structure
EXPECTED_PARENT="$HOME/.openclaw/agents"
if [[ "$SESSIONS_DIR" != "$EXPECTED_PARENT/"* ]]; then
    echo -e "${RED}FATAL:${NC} Session dir doesn't match expected parent"
    exit 1
fi
if [ ! -d "$SESSIONS_DIR" ]; then
    echo -e "${RED}Error:${NC} Sessions directory not found: $SESSIONS_DIR"
    exit 1
fi

SESSIONS_JSON="$SESSIONS_DIR/sessions.json"
if [ ! -f "$SESSIONS_JSON" ]; then
    echo -e "${RED}Error:${NC} sessions.json not found: $SESSIONS_JSON"
    exit 1
fi

# Help
if [ $# -lt 1 ]; then
    echo "Usage: $0 <sessionId> [--force]"
    echo "  Set OPENCLAW_AGENT env var to target a specific agent (default: main)"
    exit 1
fi

SESSION_ID="$1"
FORCE="${2:-}"

# Safety: validate session ID format (hex + hyphens only)
if ! echo "$SESSION_ID" | grep -qE '^[a-f0-9\-]+$'; then
    echo -e "${RED}Error:${NC} Invalid session ID format"
    exit 1
fi

# Safety: refuse to burn main
if [ "$SESSION_ID" = "main" ]; then
    echo -e "${RED}ERROR:${NC} Refusing to burn 'main' session."
    exit 1
fi

# Safety: minimum length
if [ ${#SESSION_ID} -lt 8 ]; then
    echo -e "${RED}Error:${NC} Session ID too short."
    exit 1
fi

# Build search patterns -- all prefixed with session ID so only matching files are found
declare -a SEARCH_PATTERNS=(
    "${SESSION_ID}.jsonl"
    "${SESSION_ID}.jsonl.bak-*"
    "${SESSION_ID}.jsonl.deleted.*"
    "${SESSION_ID}.jsonl.reset.*"
    "${SESSION_ID}.trajectory.jsonl"
    "${SESSION_ID}.trajectory-path.json"
    "${SESSION_ID}-topic-*.jsonl"
    "${SESSION_ID}-topic-*.jsonl.bak-*"
    "${SESSION_ID}-topic-*.jsonl.deleted.*"
    "${SESSION_ID}-topic-*.jsonl.reset.*"
    "${SESSION_ID}-topic-*.trajectory.jsonl"
    "${SESSION_ID}-topic-*.trajectory-path.json"
)

# Locate files
declare -a FILES=()
for pattern in "${SEARCH_PATTERNS[@]}"; do
    while IFS= read -r -d '' f; do
        FILES+=("$f")
    done < <(find "$SESSIONS_DIR" -maxdepth 1 -type f -name "$pattern" -print0 2>/dev/null || true)
done

# Safety: verify every found file is actually inside sessions dir
VERIFIED_FILES=()
for f in "${FILES[@]}"; do
    DIR=$(dirname "$f")
    if [ "$DIR" != "$SESSIONS_DIR" ]; then
        echo -e "${RED}SECURITY ERROR:${NC} File outside sessions dir, aborting."
        exit 1
    fi
    if [ ! -f "$f" ]; then
        continue
    fi
    VERIFIED_FILES+=("$f")
done
FILES=("${VERIFIED_FILES[@]}")

# Report
TOTAL_BYTES=0
echo ""
echo "=== BurnThisShit ==="
echo "Session: $SESSION_ID"
echo "Agent:   $AGENT"
echo "Dir:     $SESSIONS_DIR"
echo ""

if [ ${#FILES[@]} -eq 0 ]; then
    echo "No disk files found for this session ID."
else
    echo "Files to destroy (${#FILES[@]} total):"
    for f in "${FILES[@]}"; do
        SIZE=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 0)
        TOTAL_BYTES=$((TOTAL_BYTES + SIZE))
        echo "  -> $(basename "$f") (${SIZE} bytes)"
    done
    echo "Total: ${TOTAL_BYTES} bytes"
fi

# Check sessions.json
MATCHING_KEYS=$(
    jq -r --arg sid "$SESSION_ID" '
        to_entries[]
        | select(
            (.value.sessionId == $sid)
            or (.value.usageFamilySessionIds // [] | index($sid))
            or (.key | endswith(":" + $sid))
        )
        | .key
    ' "$SESSIONS_JSON" 2>/dev/null || true
)

FAMILY_KEYS=$(
    jq -r --arg sid "$SESSION_ID" '
        to_entries[]
        | select(.value.usageFamilySessionIds // [] | index($sid))
        | .key
    ' "$SESSIONS_JSON" 2>/dev/null || true
)

SESSION_KEYS_COUNT=$(echo "$MATCHING_KEYS" | grep -c . 2>/dev/null || echo 0)
if [ -n "$MATCHING_KEYS" ] && [ "$SESSION_KEYS_COUNT" -gt 0 ]; then
    echo ""
    echo "sessions.json entries to remove:"
    while IFS= read -r key; do
        [ -z "$key" ] && continue
        echo "  -> $key"
    done <<< "$MATCHING_KEYS"
else
    echo ""
    echo "No sessions.json entries found."
fi

# Confirm unless --force
if [ "$FORCE" != "--force" ]; then
    echo ""
    echo "WARNING: This is IRREVERSIBLE. Files will be shredded."
    read -r -p "Proceed? (y/N) " CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        echo "Aborted."
        exit 0
    fi
fi

# SHRED
echo ""
echo "Burning..."

BURNED=0
FAILED=0

if command -v shred &>/dev/null; then
    SHRED_CMD="shred -n 3 -z -u"
else
    SHRED_CMD=""
fi

for f in "${FILES[@]}"; do
    if [ ! -f "$f" ]; then
        continue
    fi

    BN=$(basename "$f")

    if [ -n "$SHRED_CMD" ]; then
        if $SHRED_CMD "$f" 2>/dev/null; then
            echo "  OK  shredded: $BN"
            BURNED=$((BURNED + 1))
        else
            echo "  FAIL  $BN"
            FAILED=$((FAILED + 1))
        fi
    else
        SIZE=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 1024)
        count=$((SIZE / 4096 + 1))
        dd if=/dev/urandom of="$f" bs=4096 count=$count 2>/dev/null
        dd if=/dev/urandom of="$f" bs=4096 count=$count 2>/dev/null
        dd if=/dev/urandom of="$f" bs=4096 count=$count 2>/dev/null
        rm -f "$f"
        echo "  OK  wiped: $BN"
        BURNED=$((BURNED + 1))
    fi
done

# CLEAN SESSIONS.JSON
if [ -n "$MATCHING_KEYS" ]; then
    JQ_FILTER="."

    while IFS= read -r key; do
        [ -z "$key" ] && continue
        ESCAPED_KEY=$(echo "$key" | sed 's/[\\.\\[\\*\\?+^\\$\\(\\)\\{\\}/\\\\]/\\\\&/g')
        JQ_FILTER="$JQ_FILTER | del(.[\"$ESCAPED_KEY\"])"
    done <<< "$MATCHING_KEYS"

    while IFS= read -r key; do
        [ -z "$key" ] && continue
        ESCAPED_KEY=$(echo "$key" | sed 's/[\\.\\[\\*\\?+^\\$\\(\\)\\{\\}/\\\\]/\\\\&/g')
        JQ_FILTER="$JQ_FILTER | (.[\"$ESCAPED_KEY\"].usageFamilySessionIds) |= map(select(. != \"$SESSION_ID\"))"
    done <<< "$FAMILY_KEYS"

    TMP_JSON="${SESSIONS_JSON}.tmp.burn"
    if jq "$JQ_FILTER" "$SESSIONS_JSON" > "$TMP_JSON" 2>/dev/null; then
        TMP_KEYS=$(jq 'keys | length' "$TMP_JSON" 2>/dev/null || echo 0)
        ORIG_KEYS=$(jq 'keys | length' "$SESSIONS_JSON" 2>/dev/null || echo 0)
        if [ "$TMP_KEYS" -eq 0 ]; then
            echo "  FAIL  sessions.json would be empty! Refusing."
            rm -f "$TMP_JSON"
            FAILED=$((FAILED + 1))
        else
            mv "$TMP_JSON" "$SESSIONS_JSON"
            echo "  OK  sessions.json cleaned (${ORIG_KEYS} -> ${TMP_KEYS} keys)"
        fi
    else
        echo "  FAIL  sessions.json update failed"
        rm -f "$TMP_JSON"
        FAILED=$((FAILED + 1))
    fi
fi

# REPORT
echo ""
if [ "$FAILED" -eq 0 ] && { [ "$BURNED" -gt 0 ] || [ "$SESSION_KEYS_COUNT" -gt 0 ]; }; then
    echo "Session ${SESSION_ID} completely obliterated."
    echo "${BURNED} files shredded, sessions.json cleaned."
elif [ "$FAILED" -eq 0 ]; then
    echo "Nothing to burn for session ${SESSION_ID}."
else
    echo "${BURNED} files burned, ${FAILED} failures."
fi

exit $FAILED
