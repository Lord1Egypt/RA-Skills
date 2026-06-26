#!/bin/bash
# Dream Cycle - Morning Brief Generator
# Generates a morning summary for the user

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

echo "=== Morning Brief - $TODAY ==="
echo ""

# Get today's date file if exists
echo "📝 Today's Notes:"
if [ -f "$MEMORY_DIR/$TODAY.md" ]; then
    head -20 "$MEMORY_DIR/$TODAY.md"
else
    echo "(No notes yet today)"
fi
echo ""

# Get yesterday's summary
echo "📊 Yesterday's Activity:"
if [ -f "$MEMORY_DIR/$YESTERDAY.md" ]; then
    head -30 "$MEMORY_DIR/$YESTERDAY.md"
else
    echo "(No notes from yesterday)"
fi
echo ""

# Quick stats
echo "📈 Memory Stats:"
echo "- Memory files: $(find "$MEMORY_DIR" -name "*.md" 2>/dev/null | wc -l)"
echo "- AGENTS.md: $(wc -c < "$WORKSPACE/AGENTS.md" 2>/dev/null || echo 0) bytes"
echo "- MEMORY.md: $(wc -c < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0) bytes"

# Check memory search
if command -v openclaw &> /dev/null; then
    INDEXED=$(openclaw memory status 2>/dev/null | grep "Indexed:" | awk '{print $2}')
    echo "- QMD Indexed: ${INDEXED:-unknown} chunks"
fi

echo ""
echo "=== Have a great day! ==="
