#!/bin/bash
# AI Mother - Safe Auto-healing with user intent detection
# Usage: ./auto-heal.sh <PID> [--dry-run]

PID=$1
DRY_RUN=${2:-""}
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONTEXT_SCRIPT="$SKILL_DIR/scripts/get-ai-context.sh"
SEND_TO_AI="$SKILL_DIR/scripts/send-to-ai.sh"
RESUME_AI="$SKILL_DIR/scripts/resume-ai.sh"
DB_SCRIPT="$SKILL_DIR/scripts/db.py"

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID> [--dry-run]"
    exit 1
fi

echo "=== AI Mother Auto-Heal: PID $PID ==="
[ "$DRY_RUN" = "--dry-run" ] && echo "🔍 DRY RUN MODE - No actions will be taken"
echo ""

# Get context
CONTEXT=$("$CONTEXT_SCRIPT" "$PID" 2>/dev/null)
STATE=$(ps -o stat= -p "$PID" 2>/dev/null | head -c 1)
LAST_OUTPUT=$(echo "$CONTEXT" | sed -n '/^--- Last Output ---/,/^---/p' | grep -v "^---" | head -20)
RUNTIME=$(ps -o etimes= -p "$PID" 2>/dev/null | xargs)

HEALED=false

# Check tmux pane content for permission prompts
TMUX_CHECK=$("$SKILL_DIR/scripts/check-tmux-waiting.sh" "$PID" 2>/dev/null)
TMUX_STATUS=$(echo "$TMUX_CHECK" | head -1)
TMUX_CONTENT=$(echo "$TMUX_CHECK" | tail -n +3)

# Healing Rule 0: Permission confirmation in tmux → escalate to owner
if [ "$TMUX_STATUS" = "WAITING_INPUT" ]; then
    if echo "$TMUX_CONTENT" | grep -qi "permission required\|allow once\|allow always\|do you want\|proceed\|yes/no\|y/n"; then
        echo "🔧 Issue: AI waiting for permission confirmation"
        echo ""
        echo "--- Confirmation Prompt ---"
        echo "$TMUX_CONTENT" | tail -8
        echo "---"
        echo ""
        echo "   Action: ESCALATE TO OWNER"

        if [ "$DRY_RUN" != "--dry-run" ]; then
            WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
            AI_TYPE=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
            NOTIFY_SCRIPT="$SKILL_DIR/scripts/notify-owner.sh"
            
            # Show the actual prompt (last 10 lines of tmux content)
            PROMPT_TEXT=$(echo "$TMUX_CONTENT" | tail -10)
            
            # Extract options - try multiple patterns
            OPTIONS_LINE=""
            
            # Pattern 1: OpenCode style "Allow once   Allow always   Reject"
            if [ -z "$OPTIONS_LINE" ]; then
                OPTIONS_LINE=$(echo "$PROMPT_TEXT" | grep -i "allow.*reject\|allow.*deny" | head -1 | sed 's/^[[:space:]┃│┆┊]*//' | sed 's/[[:space:]]*$//')
            fi
            
            # Pattern 2: Inline (y/n) or (Y/n)
            if [ -z "$OPTIONS_LINE" ]; then
                OPTIONS_LINE=$(echo "$PROMPT_TEXT" | grep -oE '\([yYnN]/[yYnN]\)' | head -1)
            fi
            
            # Pattern 3: Numbered options "1. Allow" "2. Deny"
            if [ -z "$OPTIONS_LINE" ]; then
                NUMBERED=$(echo "$PROMPT_TEXT" | grep -E '[0-9]+\.' | sed 's/^[[:space:]┃│┆┊❯]*//')
                if [ -n "$NUMBERED" ]; then
                    OPTIONS_LINE=$(echo "$NUMBERED" | tr '\n' ' ' | sed 's/[[:space:]]*$//')
                fi
            fi

            # Build notification message
            OPTIONS_BLOCK=""
            if [ -n "$OPTIONS_LINE" ]; then
                OPTIONS_BLOCK="Options: $OPTIONS_LINE

"
            fi

            "$NOTIFY_SCRIPT" "💬 AI Agent Needs Permission

AI: $AI_TYPE (PID $PID)
Project: ${WORKDIR/$HOME/~}

${OPTIONS_BLOCK}Prompt:
$PROMPT_TEXT

📱 Reply with exact input to send:
AI Mother: <your-input> $PID

Examples:
- AI Mother: 1 $PID (if numbered options)
- AI Mother: y $PID (if y/n prompt)
- AI Mother: allow once $PID (if text options)

🖥️ Or attach manually:
tmux attach -t 0"

            echo "✅ Owner notified"
        else
            echo "   Would notify owner with prompt details"
        fi
        echo ""
        exit 0
    fi
fi

# Healing Rule 1: Resume stopped process (T state) - ALWAYS ASK OWNER
if [ "$STATE" = "T" ]; then
    echo "🔧 Issue: Process is stopped (Ctrl+Z)"
    
    # Check if task appears complete
    if echo "$LAST_OUTPUT" | grep -qi "done\\|finished\\|completed\\|all tasks complete"; then
        echo "   ✅ AI appears to have finished its task"
        echo "   Action: SKIP - no need to resume"
        echo ""
    else
        # NEVER auto-resume - always notify owner for approval
        echo "   ⚠️  Process is stopped - requires owner approval to resume"
        echo "   Action: NOTIFY OWNER"
        
        if [ "$DRY_RUN" != "--dry-run" ]; then
            WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
            AI_TYPE=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
            NOTIFY_SCRIPT="$SKILL_DIR/scripts/notify-owner.sh"
            
            LAST_OUTPUT_SHORT=$(echo "$LAST_OUTPUT" | head -3 | tr '\n' ' ')
            
            "$NOTIFY_SCRIPT" "⚠️ AI Agent Stopped (PID $PID)

AI Type: $AI_TYPE
Project: $WORKDIR
Runtime: $(ps -o etime= -p "$PID" | xargs)

Last output:
$LAST_OUTPUT_SHORT

Should I resume this process?
Reply 'yes' to resume, or 'no' to keep it stopped."
            
            echo "✅ Owner notified - waiting for approval"
            echo "   Process will NOT be resumed automatically"
        else
            echo "   Would notify owner and wait for approval"
        fi
        echo ""
    fi
fi

# Healing Rule 2: AI waiting for simple confirmation
if echo "$LAST_OUTPUT" | grep -qi "press enter to continue\\|hit enter\\|press any key"; then
    echo "🔧 Issue: AI waiting for Enter key"
    echo "   Action: Send Enter"
    if [ "$DRY_RUN" != "--dry-run" ]; then
        "$SEND_TO_AI" "$PID" --enter
        echo "✅ Enter sent"
        HEALED=true
    else
        echo "   Would run: $SEND_TO_AI $PID --enter"
    fi
    echo ""
fi

# Healing Rule 3: AI asking yes/no for safe operations
if echo "$LAST_OUTPUT" | grep -qi "should i continue\\|shall i proceed\\|continue.*y/n"; then
    # Check if it's a safe operation (read-only, non-destructive)
    if echo "$LAST_OUTPUT" | grep -qi "read\\|view\\|check\\|analyze\\|review"; then
        echo "🔧 Issue: AI asking for confirmation (safe operation)"
        echo "   Action: Send 'yes'"
        if [ "$DRY_RUN" != "--dry-run" ]; then
            "$SEND_TO_AI" "$PID" --yes
            echo "✅ Confirmation sent"
            HEALED=true
        else
            echo "   Would run: $SEND_TO_AI $PID --yes"
        fi
        echo ""
    else
        echo "⚠️  Issue: AI asking for confirmation (potentially unsafe)"
        echo "   Action: SKIP - requires manual review"
        echo ""
    fi
fi

# Healing Rule 4: AI idle for too long - WITH COMPLETION CHECK
RECENT_FILES=$(echo "$CONTEXT" | sed -n '/^--- Recent File Changes/,/^---/p' | grep -v "^---")
if [ -n "$RUNTIME" ] && [ "$RUNTIME" -gt 7200 ] && [ -z "$RECENT_FILES" ]; then
    echo "🔧 Issue: AI idle for >2 hours with no file changes"
    
    # Safety check: Is it actually done?
    if echo "$LAST_OUTPUT" | grep -qi "done\\|finished\\|completed\\|all tasks complete\\|nothing more to do"; then
        echo "   ✅ AI appears to have completed its task"
        echo "   Action: SKIP - no need to wake it up"
        echo "   Suggestion: User can safely kill this process"
        echo ""
    else
        # Check if it's in error state
        if echo "$LAST_OUTPUT" | grep -qi "error\\|failed\\|exception"; then
            echo "   ⚠️  AI is in error state, not just idle"
            echo "   Action: SKIP - needs manual debugging"
            echo ""
        else
            # Truly idle, not done, not errored - safe to ask
            echo "   Action: Request status update"
            if [ "$DRY_RUN" != "--dry-run" ]; then
                "$SEND_TO_AI" "$PID" "What's your current status? Are you done with the task?"
                echo "✅ Status request sent"
                HEALED=true
            else
                echo "   Would send: 'What's your current status? Are you done with the task?'"
            fi
            echo ""
        fi
    fi
fi

# Healing Rule 5: Rate limit - suggest model switch
if echo "$LAST_OUTPUT" | grep -qi "429\\|rate.limit\\|rate_limit"; then
    echo "🔧 Issue: API rate limit (429)"
    echo "   Action: Suggest model switch or wait"
    if [ "$DRY_RUN" != "--dry-run" ]; then
        "$SEND_TO_AI" "$PID" "You're hitting rate limits. Consider switching to a different model or waiting a few minutes."
        echo "✅ Suggestion sent"
        HEALED=true
    else
        echo "   Would send suggestion to switch model"
    fi
    echo ""
fi

# Healing Rule 6: Permission denied - check settings
if echo "$LAST_OUTPUT" | grep -qi "permission denied\\|EACCES\\|not allowed"; then
    echo "🔧 Issue: Permission denied error"
    echo "   Action: Check settings.local.json"
    WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
    if [ -f "$WORKDIR/.claude/settings.local.json" ]; then
        echo "   Settings file exists: $WORKDIR/.claude/settings.local.json"
        echo "   ⚠️  Manual review needed - cannot auto-fix permissions"
    else
        echo "   ⚠️  No settings.local.json found - AI may need permission configuration"
    fi
    echo ""
fi

# Summary
if [ "$HEALED" = true ]; then
    echo "✅ Auto-healing completed - issue(s) addressed"
    exit 0
else
    echo "ℹ️  No auto-healing actions taken"
    echo "   Either no issues detected, or manual intervention required"
    exit 1
fi
