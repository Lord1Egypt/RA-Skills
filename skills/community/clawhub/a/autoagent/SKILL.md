---
name: autoagent
description: "Automatically improve agent guidance through iterative testing and scoring. Use when you want to optimize prompts, AGENTS.md entries, or skill definitions using a Karpathy-style training loop with OpenClaw cron."
---

# Autoagent Skill

Optimize any agent guidance through automated testing and iterative improvement.

## Quick Start

```
/autoagent
```

## What It Does

1. **Setup Phase** - Asks where your guidance lives and what it should do
2. **Creates Sandbox** - Copies guidance to test folder with fixtures
3. **Runs Optimization Loop** - Every 5 minutes via cron:
   - Analyzes current guidance
   - Proposes improvement
   - Tests with subagent
   - Scores result
   - Keeps or discards change
4. **Logs Everything** - Check scores.md for history

---

## Setup Phase (Every Invocation Starts Fresh)

Every invocation of `/autoagent` starts fresh with interactive setup questions.

### Step 1: Ask Sandbox Location

Ask the user:

> Where should I create the sandbox folder? Default: `../../autoagent-sandbox/` (resolves to `/clawd/autoagent-sandbox/`)

You can respond with:
- **Empty/default**: Press enter to use `../../autoagent-sandbox/`
- **Just a name**: "news" creates `../../autoagent-news/` → `/clawd/autoagent-news/`
- **Relative path**: "agentDev/optimize" creates `../../agentDev/optimize/` → `/clawd/agentDev/optimize/`
- **Absolute path**: `/some/other/path/optimize/` → exact path

Wait for their response (or empty for default).

### Step 2: Discuss Success Criteria

Ask the user:

> Let's define how we'll measure success. What does a "good" result look like for this task?

Follow up one at a time based on their response:
- What specific outputs are expected?
- What format should they be in?
- What's the minimum viable quality?
- Any edge cases to consider?

Once you have enough information, propose a draft scoring.md:

```markdown
## Proposed Scoring Criteria

**Score Components:**
- [Component 1]: [X] points - [description]
- [Component 2]: [Y] points - [description]
- ...

**Total:** 100 points

**[Any additional notes]**
```

Wait for user approval or modifications.

### Step 3: Ask About External Scripts/Tools

Ask the user:

> Does the guidance rely on any scripts, tools, or external software?
> - If yes: Note each script/tool path and what functionality it provides
> - The autoagent should analyze these to recommend improvements

### Step 4: Ask Cron Schedule

Ask the user:

> Run optimization every 5 minutes (default), or different interval?

### Step 5: Create Sandbox

After all questions answered, create the sandbox folder at the user-specified path:

```
sandbox/
├── guidance-under-test.md   # Copy of original guidance
├── current-guidance.md      # Same as guidance-under-test initially
├── fixtures/
│   └── test-cases.json      # {"cases": [{"input": "...", "expected": "..."}]}
├── scoring.md               # Scoring criteria document (user-approved)
├── scores.md                # Score history table
└── scripts/                  # (optional) Copy of referenced scripts/tools
```

### Step 6: Set Up Cron

Use OpenClaw cron syntax to schedule the iteration agent:
- Default: every 5 minutes (`*/5 * * * *`)
- Command: invoke the iteration prompt with the sandbox path

### Step 7: Confirm Start

Return confirmation message showing the resolved path:

> "Optimization started at `/clawd/autoagent-news/`. I'll check back every 5 minutes. Monitor progress in `scores.md`."

---

## Iteration Phase (Runs Every Cron Interval)

Each time the cron triggers, do the following:

### Step 1: Analyze Current State

Read from the sandbox:
- `current-guidance.md` - The guidance being optimized
- `scores.md` - History of scores and changes
- `scoring.md` - How to measure success
- `fixtures/test-cases.json` - Test inputs (MUST read this to understand what the guidance is being tested against)

Review score history (last 10 runs or all available runs if fewer than 10 exist), identify patterns, note current score. When fewer than 10 runs exist, treat all available scores as the set for plateau detection.

**Important:** Load the test cases from `fixtures/test-cases.json` to understand what specific outputs/ behaviors are expected. The edit should address gaps revealed by test case failures or missing criteria.

### Step 1b: Analyze External Scripts/Tools (If Applicable)

If the guidance references any scripts, tools, or external software:

1. **Locate each script/tool** - Find the actual script files or binary locations
2. **Analyze the functionality** - Read the code or documentation to understand what it does
3. **Identify improvement opportunities:**
   - **For open-source scripts:** Can the script be modified to improve functionality?
   - **For closed-source/compiled tools:** Can wrapper behavior be improved? Can you recommend API/interface changes?
4. **Note findings in the iteration** - If script improvements could help test scores, document them

**Example outputs:**
- "Script X does Y but could do Z - recommend modification to add feature W"
- "Tool A is closed-source, recommend changing prompt to work around limitation B"
- "Script C has bug in function D - fix would improve test outcomes"

### Step 2: Propose Edit

Generate ONE specific edit to the guidance that might improve the score.

**Analyze Score History First:**
- Read scores.md to find the last 10 runs
- Identify patterns: Which scoring criteria are consistently low?
- Look for repeated failures - if the same criterion failed multiple times, that's your target
- Check what changes were tried before (avoid repeating failed approaches)

**Edit Selection Strategy (Priority Order):**
1. If scores exist: Target the lowest-scoring criteria from scoring.md
2. If all scores high (90+): Add missing detail to any criteria marked as partial
3. If only 1-2 runs: Assume baseline covered basics, add missing methodology
4. Prioritize edits that affect multiple scoring criteria at once

**The edit should:**
- Be specific and actionable (not vague like "improve clarity")
- Address a weakness identified in scoring (target the lowest-scoring criteria)
- Not be identical to recently tried changes (check scores.md for recent descriptions)
- Include the exact text to add/remove/replace

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

Write the edited guidance to `current-guidance.md`

### Step 4: Run Test

Use a subagent to run the task with the new guidance:
- Give the subagent `current-guidance.md`
- Provide test inputs from `fixtures/test-cases.json`
- Capture the output
- **Subagent invocation:** Use `sessions_spawn` with `task` containing the full contents of current-guidance.md, include the test cases JSON inline in the task prompt, set `timeoutSeconds` to 120, and request the subagent to return the raw output (not just pass/fail)

### Step 5: Score Result

Evaluate the output against `scoring.md` criteria.
Generate a score 0-100.

### Step 6: Log Decision

Append to `scores.md`:

```markdown
| N   | Description of change | SCORE | keep/discard |
```

Where N is the run number (increment from last).

### Step 7: Update Guidance

- If score improved: Keep the edit (`current-guidance.md` is already updated)
- If score declined: Revert `current-guidance.md` to previous version

### Step 8: Check Plateau

If last 10 scores are within 5 points of each other:
- Log "Plateau detected - pausing"
- Notify user
- Stop the cron (or pause and await user override)

---

## Files Created in Sandbox

| File | Description |
|------|-------------|
| `guidance-under-test.md` | Original copy (read-only reference) |
| `current-guidance.md` | Working version (edited each iteration) |
| `fixtures/test-cases.json` | Input → expected output pairs |
| `scoring.md` | Scoring methodology |
| `scores.md` | Score history log |
| `scripts/` | (optional) Copies of referenced scripts/tools for analysis |

---

## Usage

1. Invoke: `/autoagent`
2. Answer setup questions
3. Monitor `scores.md` for progress
4. Copy improvements to original when satisfied
5. Stop cron when done

## Stopping

- User can stop cron anytime
- Auto-stops if score plateaus for 10 runs
- Check `scores.md` for progress

---

## Key Principles

- **Non-destructive**: Original guidance stays in `guidance-under-test.md`
- **Learn from history**: Don't repeat failed approaches
- **Be specific**: Vague changes won't score well
- **Human in the loop**: User defines success criteria, can override plateau detection
