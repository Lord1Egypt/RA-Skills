#!/bin/bash
# AI Mother - Health Check
# Quick health check for all AI agents
# Usage: ./health-check.sh

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
PATROL="$SKILL_DIR/scripts/patrol.sh"
SMART_DIAGNOSE="$SKILL_DIR/scripts/smart-diagnose.sh"
AUTO_HEAL="$SKILL_DIR/scripts/auto-heal.sh"

echo "🏥 AI Mother Health Check"
echo "========================="
echo ""

# Run patrol
PATROL_OUTPUT=$("$PATROL" --quiet 2>&1)

# Check if any issues
if echo "$PATROL_OUTPUT" | grep -q "NEEDS_ATTENTION=true"; then
    echo "⚠️  Issues detected!"
    echo ""
    
    # Extract PIDs with issues
    ISSUE_PIDS=$(echo "$PATROL_OUTPUT" | grep "PID" | grep -oP 'PID \K[0-9]+')
    
    for PID in $ISSUE_PIDS; do
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🔍 Analyzing PID $PID"
        echo ""
        
        # Run smart diagnosis
        "$SMART_DIAGNOSE" "$PID" 2>/dev/null
        
        echo ""
        echo "🔧 Attempting auto-heal..."
        if "$AUTO_HEAL" "$PID" 2>/dev/null; then
            echo "✅ Auto-heal successful"
        else
            echo "⚠️  Auto-heal not applicable - manual intervention may be needed"
        fi
        echo ""
    done
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📋 Summary:"
    echo "$PATROL_OUTPUT" | grep -E "🚫|⚠️|❌|💬|✅"
    
else
    echo "✅ All AI agents healthy!"
    echo ""
    echo "$PATROL_OUTPUT" | grep "✅"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 Tip: Run './analytics.py' for performance insights"
