---
name: executing-plans
description: "Use when you have a written plan to execute, working through tasks sequentially with review checkpoints. Trigger when a plan document exists and the user wants to execute it in the current session. Do not trigger without an existing plan document. If subagents are available, prefer agent-workflow:subagent-driven-execution instead."
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** This skill works much better with subagent support. If subagents are available, use `agent-workflow:subagent-driven-execution` instead — it provides higher quality through fresh context per task and two-stage review.

## The Process

### Step 1: Load and Review Plan

1. Read plan file
2. Review critically — identify any questions or concerns about the plan
3. If concerns: Raise them with the user before starting
4. If no concerns: Create task list and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Work

After all tasks complete and verified:
- Announce: "I'm using the finishing-work skill to complete this work."
- **REQUIRED SUB-SKILL:** Use `agent-workflow:finishing-work`
- Follow that skill to verify outputs, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing input, verification fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- User updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess

## Integration

**Required workflow skills:**
- `agent-workflow:writing-plans` — Creates the plan this skill executes
- `agent-workflow:finishing-work` — Complete work after all tasks are done
