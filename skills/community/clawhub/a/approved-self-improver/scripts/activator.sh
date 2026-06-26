#!/bin/bash
# Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind Claude about learning capture
# and pending improvement proposals
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

# Output reminder as system context
cat << 'EOF'
<self-improvement-reminder>
After completing this task, evaluate if extractable knowledge emerged:
- Non-obvious solution discovered through investigation?
- Workaround for unexpected behavior?
- Project-specific pattern learned?
- Error required debugging to resolve?
- Skill produced wrong output or failed?

If yes: Log to .learnings/ using the self-improvement skill format.
If a skill failed: Create or update an improvement proposal in .learnings/pending-improvements/ — do NOT modify the skill directly unless it is authorized for auto-update in .learnings/AUTO_UPDATE_AUTHORIZATIONS.md.
If a failure matches an existing proposal: Notify the user and recommend applying it.
If high-value (recurring, broadly applicable): Consider skill extraction.

CRITICAL: Never modify any skill without explicit user approval unless auto-update is authorized for that specific skill.
</self-improvement-reminder>
EOF

# Check for pending improvement proposals and notify
PENDING_DIR=".learnings/pending-improvements"
if [ -d "$PENDING_DIR" ]; then
    PENDING_COUNT=$(find "$PENDING_DIR" -name "IMP-*.md" -exec grep -l "Status\*\*: pending" {} \; 2>/dev/null | wc -l)
    if [ "$PENDING_COUNT" -gt 0 ]; then
        cat << EOF
<pending-improvements-notice>
There are $PENDING_COUNT pending skill improvement proposal(s) awaiting user review.
If a skill failure occurs that matches an existing proposal, notify the user and recommend applying it.
The user can review all proposals by asking: "What skill improvements do you recommend?"
</pending-improvements-notice>
EOF
    fi
fi
