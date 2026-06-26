---
name: daily-workflow-en
description: "Daily work start, mid-day check-in, and end workflow manager for English-speaking developers. Triggered by customizable phrases (default: 'starting work', 'lunch time', 'ending work'). Manages project documentation (Docs/ folder): PROJECT_TARGET.md, PROJECT_STATUS.md, COMPLETED_JOBS.md, PENDING_JOBS.md, and NEXT_STEPS.md. Ensures smooth AI-to-AI project handover with clear context preservation."
agent_created: true
---

# Daily Workflow Skill (English Version)

Manage daily work sessions with automated project documentation tracking and AI-to-AI handover support.

## First-Run Configuration

When the skill is first triggered, check if the configuration file `.workbuddy/daily-workflow-config.json` exists.

If the configuration file does NOT exist, execute the following initialization flow:

1. **Ask user for custom trigger phrases**
   - Ask the user what phrases they want to use to trigger the three workflow nodes
   - Provide default suggestions:
     - Start phrase: "starting work" or "start of day"
     - Lunch phrase: "lunch time" or "break time"
     - End phrase: "ending work" or "end of day"
   - Allow user to customize each phrase
   - Support mixed Chinese and English

2. **Create configuration file**
   - Create `daily-workflow-config.json` in the `.workbuddy/` folder at project root
   - File format:
   ```json
   {
     "startPhrase": "starting work",
     "lunchPhrase": "lunch time",
     "endPhrase": "ending work",
     "language": "en",
     "firstRun": false
   }
   ```

3. **Confirm configuration**
   - Show the user the configuration result
   - Explain they can modify the configuration file or re-run configuration anytime

If the configuration file already exists, read the config and use the user's customized phrases.

## When to Use This Skill

Trigger this skill when the user mentions phrases configured in `.workbuddy/daily-workflow-config.json`. Default trigger phrases:
- **"starting work"** / **"start of day"** - Starting the work day
- **"lunch time"** / **"break time"** - Mid-day check-in (before lunch/long break)
- **"ending work"** / **"end of day"** - Ending the work day

These phrases indicate intentional work session boundaries where project state should be captured and restored.

## Core Workflow

### Phase 1: Start Work Session

When the user indicates work is starting, execute the following sequence:

1. **Ensure Docs Directory Exists**
   - Check if `Docs/` directory exists in workspace root
   - Create `Docs/` if it does not exist

2. **Check and Create Required Files**
   - Verify these five files exist in `Docs/`:
     - `PROJECT_TARGET.md` - Project objectives and goals
     - `PROJECT_STATUS.md` - Current project status
     - `COMPLETED_JOBS.md` - Completed work items
     - `PENDING_JOBS.md` - Pending/incomplete work items
     - `NEXT_STEPS.md` - Planned next steps
   - Create any missing files with appropriate template headers

3. **Read All Documentation**
   - Read all five files from `Docs/`
   - Extract key information:
     - Current project objectives
     - Latest project status
     - Recently completed work
     - Pending tasks and blockers
     - Planned next steps

4. **Present Work Session Briefing**
   - Summarize current project state
   - Highlight completed work since last session
   - Identify pending tasks
   - Suggest priority work for current session
   - Ask user for confirmation or adjustments to the plan

### Phase 1.5: Mid-Day Check-in ("lunch time")

When the user says "lunch time" (or the customized phrase), execute the following sequence:

**Purpose:** Before lunch or a long break, update project status to ensure quick recovery when returning to work.

1. **Update Project Status**
   - Update `Docs/PROJECT_STATUS.md` with:
     - Current completion percentage
     - Tasks in progress
     - Current focus area
     - Any changes in project direction

2. **Update Completed Jobs**
   - Append morning's completed work items to `Docs/COMPLETED_JOBS.md`
   - Use format: `## [YYYY-MM-DD Morning]\n- [completed item 1]\n- [completed item 2]`
   - Include sufficient detail for another AI to understand what was done

3. **Update Pending Jobs**
   - Update `Docs/PENDING_JOBS.md` with:
     - Tasks started but not completed
     - Blockers encountered
     - Tasks deferred to afternoon
   - Remove completed items from pending list

4. **Update Next Steps**
   - Write clear, actionable next steps to `Docs/NEXT_STEPS.md`
   - Include:
     - Specific tasks to tackle when returning in afternoon
     - Priority order
     - Any prerequisites or dependencies
     - Context needed to resume work immediately

5. **Present Mid-Day Check-in Summary**
   - Summarize morning's completed work
   - List updated documentation files
   - Confirm afternoon next steps are clearly documented
   - Ensure quick state recovery when returning to work

### Phase 2: End Work Session

When the user indicates work is ending, execute the following sequence:

1. **Update Completed Jobs**
   - Append today's completed work items to `Docs/COMPLETED_JOBS.md`
   - Use format: `## [YYYY-MM-DD]\n- [completed item 1]\n- [completed item 2]`
   - Include sufficient detail for another AI to understand what was done

2. **Update Pending Jobs**
   - Update `Docs/PENDING_JOBS.md` with:
     - Tasks started but not completed
     - Blockers encountered
     - Tasks deferred to next session
   - Remove completed items from pending list

3. **Update Project Status**
   - Update `Docs/PROJECT_STATUS.md` with:
     - Current completion percentage
     - Key milestones reached
     - Current focus area
     - Any changes in project direction

4. **Update Project Target (if needed)**
   - Modify `Docs/PROJECT_TARGET.md` only if:
     - Project objectives have changed
     - New requirements discovered
     - Scope adjustments needed
   - Otherwise, leave unchanged

5. **Update Next Steps**
   - Write clear, actionable next steps to `Docs/NEXT_STEPS.md`
   - Include:
     - Specific tasks to tackle next session
     - Priority order
     - Any prerequisites or dependencies
     - Context needed to resume work immediately

6. **Present Session Summary**
   - Summarize what was completed
   - List updated documentation files
   - Confirm next steps are clearly documented
   - Ensure handover-ready state for next AI

## File Templates

When creating missing files, use these templates:

### PROJECT_TARGET.md
```markdown
# Project Target

## Project Overview
[Describe the project's main objective]

## Key Goals
- [Goal 1]
- [Goal 2]

## Success Criteria
- [Criterion 1]
- [Criterion 2]

## Last Updated
[YYYY-MM-DD]
```

### PROJECT_STATUS.md
```markdown
# Project Status

## Current Status
[Brief description of current state]

## Completion
[XX]% complete

## Current Focus
[What is being worked on now]

## Recent Milestones
- [YYYY-MM-DD] [Milestone description]

## Last Updated
[YYYY-MM-DD]
```

### COMPLETED_JOBS.md
```markdown
# Completed Jobs

## [YYYY-MM-DD]
- [Completed task 1]
- [Completed task 2]

## [YYYY-MM-DD Morning]
- [Morning completed task 1]

## [YYYY-MM-DD]
- [Completed task 1]
```

### PENDING_JOBS.md
```markdown
# Pending Jobs

## High Priority
- [ ] [Task 1]
- [ ] [Task 2]

## Medium Priority
- [ ] [Task 3]

## Low Priority
- [ ] [Task 4]

## Blockers
- [Blocker description if any]
```

### NEXT_STEPS.md
```markdown
# Next Steps

## Immediate Actions (Next Session)
1. [Action 1 - with context]
2. [Action 2 - with context]

## Upcoming Tasks
- [Task 1]
- [Task 2]

## Notes for Next AI
[Important context, decisions made, things to remember]
```

## AI-to-AI Handover Principles

Write all documentation assuming the next reader will be a different AI instance that needs to:
- Understand what was being built and why
- Resume work without asking basic questions
- Continue the same coding style and conventions
- Respect decisions already made

**Key practices:**
- Write in detail, not shorthand
- Explain the "why" not just the "what"
- Include code snippets or file references when relevant
- Note any workarounds, hacks, or technical debt
- Record user preferences and decisions

## Workflow Diagram

```
User says "starting work"
    ↓
Check Docs/ exists → Create if missing
    ↓
Check 5 files exist → Create missing with templates
    ↓
Read all 5 files
    ↓
Present work session briefing
    ↓
User works with AI assistance
    ↓
User says "lunch time" (mid-day check-in)
    ↓
Update PROJECT_STATUS.md
    ↓
Update COMPLETED_JOBS.md
    ↓
Update PENDING_JOBS.md
    ↓
Update NEXT_STEPS.md
    ↓
Present mid-day check-in summary
    ↓
User returns from lunch, continues working
    ↓
User says "ending work"
    ↓
Update COMPLETED_JOBS.md
    ↓
Update PENDING_JOBS.md
    ↓
Update PROJECT_STATUS.md
    ↓
Update PROJECT_TARGET.md (if needed)
    ↓
Update NEXT_STEPS.md
    ↓
Present session summary
    ↓
Project state saved for next AI
```

## Important Notes

- Always use absolute paths when referencing `Docs/` directory
- Append to `COMPLETED_JOBS.md` (never overwrite previous entries)
- Overwrite `NEXT_STEPS.md` each session (it's for the immediate next session)
- Preserve historical information in `PROJECT_STATUS.md` and `COMPLETED_JOBS.md`
- When in doubt, write more context, not less
- Custom trigger phrases will be asked on first use, use saved configuration for subsequent uses
- Configuration file location: `.workbuddy/daily-workflow-config.json`
- This skill supports both English and Chinese trigger phrases for flexibility
