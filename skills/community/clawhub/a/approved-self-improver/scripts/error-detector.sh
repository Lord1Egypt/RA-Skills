#!/bin/bash
# Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect command failures
# Reads CLAUDE_TOOL_OUTPUT environment variable
# Also checks for matching pending improvement proposals

set -e

# Check if tool output indicates an error
# CLAUDE_TOOL_OUTPUT contains the result of the tool execution
OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# Patterns indicating errors (case-insensitive matching)
ERROR_PATTERNS=(
    "error:"
    "Error:"
    "ERROR:"
    "failed"
    "FAILED"
    "command not found"
    "No such file"
    "Permission denied"
    "fatal:"
    "Exception"
    "Traceback"
    "npm ERR!"
    "ModuleNotFoundError"
    "SyntaxError"
    "TypeError"
    "exit code"
    "non-zero"
)

# Check if output contains any error pattern
contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

# Only output reminder if error detected
if [ "$contains_error" = true ]; then
    cat << 'EOF'
<error-detected>
A command error was detected. Consider logging this to .learnings/ERRORS.md if:
- The error was unexpected or non-obvious
- It required investigation to resolve
- It might recur in similar contexts
- The solution could benefit future sessions

Use the self-improvement skill format: [ERR-YYYYMMDD-XXX]

If this error is related to a SKILL failure:
1. Check .learnings/pending-improvements/ for an existing proposal matching this skill
2. If a proposal exists: notify the user that we have a documented fix and recommend applying it
3. If no proposal exists: create one — do NOT modify the skill directly
4. Exception: if the skill is listed in .learnings/AUTO_UPDATE_AUTHORIZATIONS.md, apply the fix directly and inform the user

CRITICAL: Never modify any skill without explicit user approval unless auto-update is authorized.
</error-detected>
EOF

    # Check if there are any pending proposals that might match
    PENDING_DIR=".learnings/pending-improvements"
    if [ -d "$PENDING_DIR" ]; then
        PENDING_FILES=$(find "$PENDING_DIR" -name "IMP-*.md" 2>/dev/null)
        if [ -n "$PENDING_FILES" ]; then
            cat << 'EOF'
<pending-proposals-available>
There are existing improvement proposals in .learnings/pending-improvements/.
Check if this error matches any pending proposal. If it does, add a recurrence
entry to the proposal and notify the user that a known fix is available.
</pending-proposals-available>
EOF
        fi
    fi
fi
