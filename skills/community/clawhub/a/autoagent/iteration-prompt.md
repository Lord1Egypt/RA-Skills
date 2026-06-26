# Autoagent Iteration Prompt

You are running an optimization iteration for the autoagent skill.

## Context

Read these files from the sandbox:
- `current-guidance.md` - The guidance being optimized
- `scores.md` - History of scores and changes
- `scoring.md` - How to measure success
- `fixtures/test-cases.json` - Test inputs

## Your Task

### Step 1: Analyze Current State

- Read current guidance
- Review score history (last 10 runs)
- Identify patterns in what's been tried
- Note current score

### Step 2: Propose Edit

Generate ONE specific edit to the guidance that might improve the score.
The edit should:
- Be specific and actionable
- Address a weakness identified in scoring
- Not be identical to recently tried changes

Format:
```markdown
## Proposed Edit

**Rationale:** Why this change might help

**Change:**
```
[Show exact diff or new text]
```
```

### Step 3: Apply Edit

Write the edited guidance to current-guidance.md

### Step 4: Run Test

Use a subagent to run the task with the new guidance:
- Give the subagent current-guidance.md
- Provide test inputs from fixtures/test-cases.json
- Capture the output

### Step 5: Score Result

Evaluate the output against scoring.md criteria.
Generate a score 0-100.

### Step 6: Log Decision

Append to scores.md:

```markdown
| N   | Description of change | SCORE | keep/discard |
```

Where N is the run number (increment from last).

### Step 7: Update Guidance

- If score improved: Keep the edit (current-guidance.md is already updated)
- If score declined: Revert current-guidance.md to previous version

### Step 8: Check Plateau

If last 10 scores are identical:
- Log "Plateau detected - pausing"
- Notify user
- Stop the cron (or pause and await user override)

## Output Requirements

After completing:
1. Updated scores.md
2. Possibly updated current-guidance.md (if change kept)
3. Brief summary of what happened

## Remember

- Be specific in edits - vague changes won't score well
- Learn from score history - don't repeat failed approaches
- Non-destructive: original guidance stays in guidance-under-test.md
