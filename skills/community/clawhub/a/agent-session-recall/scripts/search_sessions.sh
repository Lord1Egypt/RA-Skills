#!/bin/bash
# search_sessions.sh - Search across all session transcripts for keywords
# Usage: search_sessions.sh <keyword> [max_results]
#
# Searches both active (.jsonl) and archived (.reset) session files.
# Useful for finding cross-channel context and cron-to-channel messages.
#
# Requires: python3, grep, bash
#
# SECURITY NOTE: Output may contain sensitive data from session history.
# Do not pipe to public channels or logs.

set -euo pipefail

KEYWORD="$1"
MAX_RESULTS="${2:-5}"
SESSIONS_DIR="${OPENCLAW_SESSIONS_DIR:-${HOME}/.openclaw/agents/main/sessions}"

if [ -z "${KEYWORD:-}" ]; then
  echo "Usage: search_sessions.sh <keyword> [max_results]"
  echo ""
  echo "Examples:"
  echo "  search_sessions.sh 'login'             # Find login-related messages"
  echo "  search_sessions.sh 'CXXXXXXXXXX'        # Find messages sent to a channel"
  echo "  search_sessions.sh 'peperon-works' 10   # Return up to 10 matches per file"
  exit 1
fi

if [ ! -d "$SESSIONS_DIR" ]; then
  echo "Sessions directory not found: $SESSIONS_DIR"
  echo "Set OPENCLAW_SESSIONS_DIR or check your OpenClaw installation."
  exit 1
fi

echo "Searching for: $KEYWORD"
echo "Sessions dir: $SESSIONS_DIR"
echo "---"

# Count total matches (using find to avoid glob expansion issues)
TOTAL=$(find "$SESSIONS_DIR" -maxdepth 1 -name '*.jsonl' -exec grep -l "$KEYWORD" {} + 2>/dev/null | wc -l)
ARCHIVED=$(find "$SESSIONS_DIR" -maxdepth 1 -name '*.reset.*' -exec grep -l "$KEYWORD" {} + 2>/dev/null | wc -l)
echo "Found in $TOTAL active session(s), $ARCHIVED archived session(s)"
echo ""

# Search active .jsonl files (current sessions)
find "$SESSIONS_DIR" -maxdepth 1 -name '*.jsonl' -exec grep -l "$KEYWORD" {} + 2>/dev/null | while read -r f; do
  basename="$(basename "$f")"
  echo "=== $basename ==="

  # Pass keyword via environment variable to avoid shell/Python injection
  SEARCH_KEYWORD="$KEYWORD" MAX_PER_FILE="$MAX_RESULTS" python3 -c '
import json, os, sys

kw = os.environ["SEARCH_KEYWORD"]
max_results = int(os.environ.get("MAX_PER_FILE", "5"))
filepath = sys.argv[1]
count = 0

with open(filepath) as fh:
    for line in fh:
        if kw not in line:
            continue
        try:
            obj = json.loads(line)
            if obj.get("type") != "message":
                continue
            msg = obj.get("message", {})
            role = msg.get("role", "?")
            ts = obj.get("timestamp", "?")
            content = msg.get("content") or ""
            if isinstance(content, list):
                for c in content:
                    if c.get("type") == "text" and kw in c.get("text", ""):
                        text = c["text"]
                        idx = text.find(kw)
                        start = max(0, idx - 80)
                        end = min(len(text), idx + 120)
                        snippet = text[start:end].replace("\n", " ")
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(text):
                            snippet = snippet + "..."
                        print(f"  [{ts}] [{role}] {snippet}")
                        count += 1
                        break
            elif isinstance(content, str) and kw in content:
                snippet = content[:200].replace("\n", " ")
                print(f"  [{ts}] [{role}] {snippet}")
                count += 1
            if count >= max_results:
                break
        except Exception:
            pass
' "$f" 2>/dev/null
  echo ""
done

# Report archived matches
if [ "$ARCHIVED" -gt 0 ]; then
  echo "=== Archived sessions with matches ==="
  find "$SESSIONS_DIR" -maxdepth 1 -name '*.reset.*' -exec grep -l "$KEYWORD" {} + 2>/dev/null | head -5 | while read -r f; do
    echo "  $(basename "$f")"
  done
  echo "  (use 'grep' directly on these files for details)"
fi
