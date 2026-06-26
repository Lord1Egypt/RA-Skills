#!/bin/bash
# Handle owner approval for resuming stopped AI agents
# Usage: ./approve-resume.sh <PID>

PID=$1
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
RESUME_AI="$SKILL_DIR/scripts/resume-ai.sh"

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

# Check if process still exists and is stopped
if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "❌ Process $PID no longer exists"
    exit 1
fi

STATE=$(ps -o stat= -p "$PID" 2>/dev/null | head -c 1)
if [ "$STATE" != "T" ]; then
    echo "ℹ️  Process $PID is not stopped (state: $STATE)"
    echo "   No action needed"
    exit 0
fi

# Resume the process
echo "Resuming PID $PID..."
"$RESUME_AI" "$PID"

if [ $? -eq 0 ]; then
    echo "✅ Process $PID resumed successfully"
    
    # Notify owner
    NOTIFY_SCRIPT="$SKILL_DIR/scripts/notify-owner.sh"
    AI_TYPE=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
    WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
    
    "$NOTIFY_SCRIPT" "✅ AI Agent Resumed

PID: $PID
Type: $AI_TYPE
Project: $WORKDIR

The process has been resumed and is now running." 2>/dev/null
else
    echo "❌ Failed to resume process $PID"
    exit 1
fi
