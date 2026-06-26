#!/usr/bin/env bash
#
# Search for OpenClaw skills on ClawHub registry.
#
# Usage:
#   ./search-clawhub.sh "query" [limit]
#   ./search-clawhub.sh "react testing" 10
#

set -euo pipefail

QUERY="${1:-}"
LIMIT="${2:-5}"

if [[ -z "$QUERY" ]]; then
    echo "Usage: $0 \"query\" [limit]"
    echo "Example: $0 \"weather\" 5"
    exit 1
fi

# Check for clawhub or npx
if command -v clawhub &> /dev/null; then
    CLAWHUB_CMD="clawhub"
elif command -v npx &> /dev/null; then
    CLAWHUB_CMD="npx clawhub"
    echo "[INFO] Using npx (clawhub not installed globally)"
else
    echo "[ERROR] Neither clawhub nor npx found. Install with: npm i -g clawhub"
    echo "[INFO] Or install Node.js to use npx."
    exit 1
fi

echo "[INFO] Searching ClawHub for: '$QUERY' (Limit: $LIMIT)"

# Run search command
set +e
OUTPUT=$($CLAWHUB_CMD search "$QUERY" --limit "$LIMIT" 2>&1)
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -ne 0 ]] || [[ "$OUTPUT" =~ [Ee]rror: ]] || [[ "$OUTPUT" =~ "×" ]]; then
    echo "[ERROR] Search failed:"
    echo "$OUTPUT"
    
    # Check for rate limit
    if [[ "$OUTPUT" =~ "Rate limit exceeded" ]]; then
        echo "[WARNING] Rate limit exceeded. Try logging in with: clawhub login"
        echo "[WARNING] Or wait a few minutes before trying again."
    fi
    
    exit 1
fi

echo "[SUCCESS] Search completed!"
echo ""
echo "=== ClawHub Search Results ==="
echo "$OUTPUT"
echo "================================"

# Check for no results
if [[ "$OUTPUT" =~ "No skills found" ]] || [[ -z "$(echo "$OUTPUT" | grep -v '^$')" ]]; then
    echo "[WARNING] No skills found for query: '$QUERY'"
    echo "[INFO] Try different search terms or browse at: https://clawhub.ai"
fi

echo "[INFO] To install a skill, use: $CLAWHUB_CMD install <skill-slug>"