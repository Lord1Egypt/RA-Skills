#!/bin/bash
# Intelligent diagnostics - detect abnormal patterns
# Usage: ./smart-diagnose.sh <PID>

PID=$1
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONTEXT_SCRIPT="$SKILL_DIR/scripts/get-ai-context.sh"

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
echo "=== Smart Diagnosis: PID $PID ==="
echo "Workdir: $WORKDIR"
echo ""

# Get context
CONTEXT=$("$CONTEXT_SCRIPT" "$PID" 2>/dev/null)

# Pattern 1: Repeated file edits (thrashing)
echo "🔍 Checking for file thrashing..."
RECENT_FILES=$(echo "$CONTEXT" | sed -n '/^--- Recent File Changes/,/^---/p' | grep -v "^---")
if [ -n "$RECENT_FILES" ]; then
    # Count how many times the same file appears
    DUPLICATES=$(echo "$RECENT_FILES" | awk '{print $NF}' | sort | uniq -c | awk '$1 > 3 {print $1, $2}')
    if [ -n "$DUPLICATES" ]; then
        echo "⚠️  THRASHING DETECTED: Same file(s) modified repeatedly:"
        echo "$DUPLICATES"
        echo "   → AI may be stuck in a loop, consider intervention"
    else
        echo "✅ No file thrashing detected"
    fi
else
    echo "ℹ️  No recent file changes"
fi
echo ""

# Pattern 2: High CPU with no file changes (infinite loop?)
echo "🔍 Checking for CPU spin..."
CPU=$(ps -o pcpu= -p "$PID" 2>/dev/null | xargs)
if [ -n "$CPU" ]; then
    CPU_INT=$(echo "$CPU" | cut -d. -f1)
    if [ "$CPU_INT" -gt 80 ] && [ -z "$RECENT_FILES" ]; then
        echo "⚠️  CPU SPIN DETECTED: High CPU ($CPU%) with no file activity"
        echo "   → AI may be in infinite loop or stuck computation"
    else
        echo "✅ CPU usage normal ($CPU%)"
    fi
fi
echo ""

# Pattern 3: Repeated API errors (rate limit loop)
echo "🔍 Checking for API error loops..."
ERROR_COUNT=$(echo "$CONTEXT" | grep -c "ERROR.*429\|rate.limit\|rate_limit")
if [ "$ERROR_COUNT" -gt 5 ]; then
    echo "⚠️  RATE LIMIT LOOP: $ERROR_COUNT consecutive 429 errors"
    echo "   → AI is stuck hitting rate limit, needs model switch or wait"
else
    echo "✅ No API error loops"
fi
echo ""

# Pattern 4: Git commit frequency (too many commits)
echo "🔍 Checking git commit frequency..."
if [ -d "$WORKDIR/.git" ]; then
    COMMITS_1H=$(git -C "$WORKDIR" log --since="1 hour ago" --oneline 2>/dev/null | wc -l)
    if [ "$COMMITS_1H" -gt 20 ]; then
        echo "⚠️  EXCESSIVE COMMITS: $COMMITS_1H commits in last hour"
        echo "   → AI may be committing too frequently, check if intentional"
    else
        echo "✅ Commit frequency normal ($COMMITS_1H in last hour)"
    fi
else
    echo "ℹ️  Not a git repo"
fi
echo ""

# Pattern 5: Memory growth (potential leak)
echo "🔍 Checking memory usage..."
MEM_MB=$(ps -o rss= -p "$PID" 2>/dev/null | awk '{print int($1/1024)}')
if [ -n "$MEM_MB" ]; then
    if [ "$MEM_MB" -gt 2048 ]; then
        echo "⚠️  HIGH MEMORY: ${MEM_MB}MB"
        echo "   → Monitor for memory leak if growing"
    else
        echo "✅ Memory usage normal (${MEM_MB}MB)"
    fi
fi
echo ""

# Pattern 6: Long runtime with no progress
echo "🔍 Checking for stalled progress..."
RUNTIME=$(ps -o etimes= -p "$PID" 2>/dev/null | xargs)
if [ -n "$RUNTIME" ] && [ "$RUNTIME" -gt 14400 ]; then  # 4 hours
    if [ -z "$RECENT_FILES" ]; then
        echo "⚠️  STALLED: Running for $((RUNTIME/3600))h with no recent file changes"
        echo "   → AI may be idle or waiting, check status"
    else
        echo "✅ Long runtime but still active"
    fi
else
    echo "✅ Runtime reasonable"
fi
echo ""

echo "=== Diagnosis Complete ==="
