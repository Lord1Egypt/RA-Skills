#!/bin/bash
# Format patrol results for notifications (Feishu-friendly, clean format)
# Usage: ./format-notification.sh [--issues-only]

ISSUES_ONLY=${1:-""}
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"

# Run patrol (non-quiet to get summary)
PATROL_OUTPUT=$(bash "$SKILL_DIR/scripts/patrol.sh" 2>&1)

# Extract summary section (between "=== Summary ===" and end, excluding NEEDS_ATTENTION line)
SUMMARY=$(echo "$PATROL_OUTPUT" | awk '/^=== Summary ===/,0 {if (!/^=== Summary ===/ && !/^NEEDS_ATTENTION=/ && NF > 0) print}')

# Parse results
ISSUES=$(echo "$SUMMARY" | grep -E "^⚠️|^🚫|^❌|^💬")
COMPLETED=$(echo "$SUMMARY" | grep "COMPLETED")
ACTIVE=$(echo "$SUMMARY" | grep "ACTIVE")

ISSUE_COUNT=$(echo "$ISSUES" | grep -v "^$" | wc -l)
COMPLETED_COUNT=$(echo "$COMPLETED" | grep -v "^$" | wc -l)
ACTIVE_COUNT=$(echo "$ACTIVE" | grep -v "^$" | wc -l)

# If issues-only mode and no issues, exit silently
if [ "$ISSUES_ONLY" = "--issues-only" ] && [ "$ISSUE_COUNT" -eq 0 ] && [ "$COMPLETED_COUNT" -eq 0 ]; then
    exit 0
fi

# Build notification message
echo ""

# Header
if [ "$ISSUE_COUNT" -gt 0 ]; then
    echo "🚨 AI Mother Patrol Report"
    echo "Found $ISSUE_COUNT issue(s) that need attention"
elif [ "$COMPLETED_COUNT" -gt 0 ]; then
    echo "✅ AI Mother Patrol Report"
    echo "$COMPLETED_COUNT task(s) completed"
else
    echo "👩‍👧‍👦 AI Mother Patrol Report"
    echo "All AI agents running normally"
fi
echo ""

# Issues section
if [ "$ISSUE_COUNT" -gt 0 ]; then
    echo "[Needs Attention]"
    echo "$ISSUES" | while IFS= read -r line; do
        [ -z "$line" ] && continue
        EMOJI=$(echo "$line" | awk '{print $1}')
        PID=$(echo "$line" | awk '{print $3}')
        TYPE=$(echo "$line" | grep -oP '\(\K[^)]+')
        STATUS=$(echo "$line" | awk '{print $5}')
        PROJECT=$(echo "$line" | awk -F' — ' '{print $2}' | awk '{print $1}')

        echo "$EMOJI $TYPE (PID $PID) - $STATUS"
        echo "   ${PROJECT/$HOME/~}"
    done
    echo ""
fi

# Completed section
if [ "$COMPLETED_COUNT" -gt 0 ]; then
    echo "[Completed]"
    echo "$COMPLETED" | while IFS= read -r line; do
        [ -z "$line" ] && continue
        PID=$(echo "$line" | awk '{print $3}')
        TYPE=$(echo "$line" | grep -oP '\(\K[^)]+')
        PROJECT=$(echo "$line" | awk -F' — ' '{print $2}' | awk '{print $1}')

        echo "✅ $TYPE (PID $PID)"
        echo "   ${PROJECT/$HOME/~}"
    done
    echo ""
fi

# Active section (only if not issues-only mode)
if [ "$ISSUES_ONLY" != "--issues-only" ] && [ "$ACTIVE_COUNT" -gt 0 ]; then
    echo "[Running] $ACTIVE_COUNT AI agent(s) working normally"

    SHOWN=0
    echo "$ACTIVE" | while IFS= read -r line; do
        [ -z "$line" ] && continue
        [ $SHOWN -ge 3 ] && break

        PID=$(echo "$line" | awk '{print $3}')
        TYPE=$(echo "$line" | grep -oP '\(\K[^)]+')
        RUNTIME=$(echo "$line" | grep -oP 'runtime: \K[^)]+')

        echo "  • $TYPE (PID $PID) - $RUNTIME"
        SHOWN=$((SHOWN + 1))
    done

    if [ "$ACTIVE_COUNT" -gt 3 ]; then
        echo "  ... and $((ACTIVE_COUNT - 3)) more"
    fi
    echo ""
fi

# Footer
echo "---"
if [ "$ISSUE_COUNT" -gt 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M') | 💡 Run 'AI Mother dashboard' for details"
else
    echo "$(date '+%Y-%m-%d %H:%M')"
fi
