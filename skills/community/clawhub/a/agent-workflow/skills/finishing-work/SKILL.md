---
name: finishing-work
description: "Use when a task or project phase is complete and you need to decide how to deliver or integrate the work. Trigger after all tasks are done and verified. Do not trigger before verification is complete or while tasks are still in progress."
---

# Finishing Work

## Safety Notice

**This skill includes options that may permanently delete drafts, temporary files, or working copies.** All destructive actions (Option 4: Discard, and cleanup steps) require explicit user confirmation before execution. Only clearly identified temporary files created during this workflow will be removed — user-created artifacts are never deleted without specific confirmation.

## Overview

Guide completion of a work phase by presenting clear options and handling the chosen delivery workflow.

**Core principle:** Verify work → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-work skill to complete this work."

## The Process

### Step 1: Verify Work

**Before presenting options, verify the work is complete:**

Check each of the following:
- All planned tasks are done
- All acceptance criteria are met
- No known issues remain unaddressed

**If verification fails:**
```
Work incomplete or issues remain:

[Show what's missing or broken]

Cannot proceed with delivery until work is verified complete.
```

Stop. Don't proceed to Step 2.

**If verification passes:** Continue to Step 2.

### Step 2: Confirm Delivery Target

Ask or confirm: "Where does this work go? Who receives it?"

Examples:
- Integrate into main project
- Submit to stakeholder for review
- Keep as draft for later
- Discard

### Step 3: Present Options

Present exactly these 4 options:

```
Work complete. What would you like to do?

1. Integrate into main project directly
2. Submit for review / deliver to stakeholder
3. Keep as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** — keep options concise.

### Step 4: Execute Choice

#### Option 1: Integrate Directly

1. Merge or apply the work into the main project
2. Verify the integrated result still meets requirements
3. Clean up any working drafts or temporary files
4. Confirm integration complete

#### Option 2: Submit for Review / Deliver

1. Package or prepare the output for delivery
2. Send to stakeholder or submit for review
3. Note any context the reviewer needs
4. Keep working copy until review is complete

Then: Clean up workspace (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping work in progress at [location]. No delivery action taken."

**Don't clean up.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- [Description of what will be deleted]
- [Any associated drafts or working files]

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed: Remove the work and working files.

Then: Clean up workspace (Step 5)

### Step 5: Clean Up Workspace

**For Options 1, 2, 4:**

Before removing any files, list what will be deleted and get explicit user confirmation:

```
The following temporary/working files will be removed:
- [file 1]
- [file 2]

Confirm cleanup? (yes/no)
```

Only remove files that were explicitly created as temporary working artifacts during this workflow. Never remove files that existed before the workflow started or that the user created independently.

**For Option 3:** Keep everything.

## Quick Reference

| Option | Integrate | Deliver | Keep Working Copy | Clean Up |
|--------|-----------|---------|-------------------|----------|
| 1. Integrate directly | ✓ | — | — | ✓ |
| 2. Submit for review | — | ✓ | ✓ | After review |
| 3. Keep as-is | — | — | ✓ | — |
| 4. Discard | — | — | — | ✓ |

## Common Mistakes

**Skipping verification**
- Problem: Delivering incomplete or broken work
- Fix: Always verify before offering options

**Open-ended questions**
- Problem: "What should I do next?" → ambiguous
- Fix: Present exactly 4 structured options

**No confirmation for discard**
- Problem: Accidentally delete work
- Fix: Require typed "discard" confirmation

## Red Flags

**Never:**
- Deliver without verifying work is complete
- Delete work without confirmation
- Skip the options presentation

**Always:**
- Verify work before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up workspace for Options 1 and 4 only

## Integration

**Called by:**
- `agent-workflow:subagent-driven-execution` — After all tasks complete
- `agent-workflow:executing-plans` — After all tasks complete
