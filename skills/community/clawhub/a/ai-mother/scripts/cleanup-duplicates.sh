#!/bin/bash
# Clean up duplicate AI agents working on the same directory
# Usage: ./cleanup-duplicates.sh [--auto]

AUTO_MODE=${1:-""}
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"

echo "=== AI Mother - Duplicate Cleanup ==="
echo ""

# Find all AI processes
AI_PROCS=$(ps aux | awk '
  /[[:space:]](claude|codex|opencode|gemini)[[:space:]]/ ||
  /[[:space:]](claude|codex|opencode|gemini)$/ {
    if ($0 !~ /grep/ && $0 !~ "ai-mother" && $11 !~ /^tmux/) print $2
  }
')

if [ -z "$AI_PROCS" ]; then
    echo "No AI agents running."
    exit 0
fi

# Group by workdir
declare -A WORKDIR_GROUPS
for PID in $AI_PROCS; do
    ps -p "$PID" > /dev/null 2>&1 || continue
    WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
    if [ -n "$WORKDIR" ]; then
        if [ -n "${WORKDIR_GROUPS[$WORKDIR]}" ]; then
            WORKDIR_GROUPS[$WORKDIR]="${WORKDIR_GROUPS[$WORKDIR]} $PID"
        else
            WORKDIR_GROUPS[$WORKDIR]="$PID"
        fi
    fi
done

# Find duplicates
FOUND_DUPLICATES=false
for WORKDIR in "${!WORKDIR_GROUPS[@]}"; do
    PIDS=(${WORKDIR_GROUPS[$WORKDIR]})
    if [ ${#PIDS[@]} -gt 1 ]; then
        FOUND_DUPLICATES=true
        echo "⚠️  Duplicate AIs detected in: ${WORKDIR/$HOME/~}"
        echo ""
        
        # Show details for each PID
        for PID in "${PIDS[@]}"; do
            AI_TYPE=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
            RUNTIME=$(ps -o etime= -p "$PID" | xargs)
            CPU=$(ps -o pcpu= -p "$PID" | xargs)
            MEM=$(ps -o rss= -p "$PID" | awk '{print int($1/1024)}')
            STATE=$(ps -o stat= -p "$PID" | head -c 1)
            
            # Check activity
            CONTEXT=$("$SKILL_DIR/scripts/get-ai-context.sh" "$PID" 2>/dev/null)
            RECENT_FILES=$(echo "$CONTEXT" | sed -n '/^--- Recent File Changes/,/^---/p' | grep -v "^---" | wc -l)
            
            echo "  PID $PID ($AI_TYPE)"
            echo "    Runtime: $RUNTIME | CPU: $CPU% | Memory: ${MEM}MB | State: $STATE"
            echo "    Recent file changes: $RECENT_FILES"
            
            # Suggest which to keep
            if [ "$STATE" = "T" ]; then
                echo "    💡 Recommendation: KILL (stopped)"
            elif [ "$RECENT_FILES" -eq 0 ] && [ "$CPU" = "0.0" ]; then
                echo "    💡 Recommendation: KILL (idle)"
            else
                echo "    💡 Recommendation: KEEP (active)"
            fi
            echo ""
        done
        
        # Auto-cleanup or prompt
        if [ "$AUTO_MODE" = "--auto" ]; then
            echo "🤖 Auto-cleanup mode: Keeping most active AI, killing others..."
            
            # Find the best PID to keep (most recent files, highest CPU, or newest)
            BEST_PID=""
            BEST_SCORE=0
            
            for PID in "${PIDS[@]}"; do
                SCORE=0
                STATE=$(ps -o stat= -p "$PID" | head -c 1)
                CPU=$(ps -o pcpu= -p "$PID" | xargs | cut -d. -f1)
                CONTEXT=$("$SKILL_DIR/scripts/get-ai-context.sh" "$PID" 2>/dev/null)
                RECENT_FILES=$(echo "$CONTEXT" | sed -n '/^--- Recent File Changes/,/^---/p' | grep -v "^---" | wc -l)
                
                # Scoring: active state + recent files + CPU activity
                [ "$STATE" != "T" ] && SCORE=$((SCORE + 10))
                SCORE=$((SCORE + RECENT_FILES * 5))
                SCORE=$((SCORE + CPU))
                
                if [ "$SCORE" -gt "$BEST_SCORE" ]; then
                    BEST_SCORE=$SCORE
                    BEST_PID=$PID
                fi
            done
            
            # Kill all except best
            for PID in "${PIDS[@]}"; do
                if [ "$PID" != "$BEST_PID" ]; then
                    echo "  Killing PID $PID..."
                    kill "$PID" 2>/dev/null
                    sleep 0.5
                    if ps -p "$PID" > /dev/null 2>&1; then
                        echo "  Force killing PID $PID..."
                        kill -9 "$PID" 2>/dev/null
                    fi
                fi
            done
            
            echo "✅ Kept PID $BEST_PID, killed others"
            echo ""
        else
            echo "📋 Manual cleanup:"
            echo "   To kill a specific PID: kill <PID>"
            echo "   To kill all but one: kill ${PIDS[@]:1}"
            echo "   Or run with --auto flag for automatic cleanup"
            echo ""
        fi
    fi
done

if [ "$FOUND_DUPLICATES" = false ]; then
    echo "✅ No duplicate AIs detected - all working on different directories"
fi
