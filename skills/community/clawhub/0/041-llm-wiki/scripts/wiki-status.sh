#!/bin/bash
# wiki-status.sh - Quick status check for llm-wiki
# Usage: ./scripts/wiki-status.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIKI_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WIKI_DIR="$WIKI_ROOT/wiki"
LOG_FILE="$WIKI_ROOT/log.md"

echo "📚 LLM-Wiki Status"
echo "=================="
echo ""

# Check wiki directory
if [ ! -d "$WIKI_DIR" ]; then
    echo "❌ Wiki directory not found: $WIKI_DIR"
    exit 1
fi

# Count pages
PAGE_COUNT=$(find "$WIKI_DIR" -name "*.md" -not -name "index.md" | wc -l)
echo "📄 Total pages: $PAGE_COUNT"

# Count sources
SOURCE_COUNT=$(find "$WIKI_ROOT/sources" -type f -not -name "README.md" 2>/dev/null | wc -l)
echo "📁 Source files: $SOURCE_COUNT"

# Recent activity
if [ -f "$LOG_FILE" ]; then
    echo ""
    echo "📅 Recent activity:"
    grep "^## \[" "$LOG_FILE" | tail -3 | sed 's/^## /  - /'
fi

# Check for Python CLI
if [ -f "$WIKI_ROOT/.venv/bin/python" ] || [ -f "$WIKI_ROOT/.venv/Scripts/python.exe" ]; then
    echo ""
    echo "✅ Virtual environment detected"
fi

echo ""
echo "Quick commands:"
echo "  ./scripts/wiki-lint.sh     - Run health check"
echo "  ./scripts/init-wiki.sh     - Initialize new wiki"
