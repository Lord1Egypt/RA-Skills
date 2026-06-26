---
name: "AI Work Session Planner"
description: "Turns a messy work goal into a focused 60 to 120 minute AI-assisted work session with inputs, checkpoints, and a clear done-state."
version: "1.0.0"
type: prompt-flow
tags: ["ai productivity", "focus", "work planning", "deep work", "session planning", "checkpoint"]
---

# AI Work Session Planner

## Overview

Use this prompt-only skill when a user has a fuzzy or overloaded work goal and wants to turn it into a focused 60 to 120 minute session with AI support.

The skill produces a timed work plan, the inputs needed before starting, checkpoint questions, suggested AI handoffs, and a practical done-state for the session.

## When to Use

Use this skill when the user says things like:

- "I have 90 minutes and need to make progress on this."
- "Help me turn this messy project into a focused work block."
- "Plan a work session where AI helps me without distracting me."
- "I do not know where to start, but I need a concrete next sprint."
- "Break this goal into a 60 minute plan."
- "Set checkpoints so I do not drift."

## Required Inputs

Ask for only the details needed to build a useful session plan:

- Main goal or messy task statement
- Available session length, ideally 60, 75, 90, or 120 minutes
- Desired output or visible progress by the end
- Current state of the work
- Known inputs, links, notes, files, drafts, or decisions needed
- Constraints such as deadline, energy level, meetings, interruptions, tools, or format
- Whether the user wants AI help for planning, drafting, reviewing, research synthesis, or decision support
- Any blockers, unanswered questions, or missing materials

If the user does not know an input, mark it as missing instead of forcing a full answer before planning.

## Workflow

1. **Capture the goal.** Rewrite the user's messy goal as one short outcome statement and one practical session objective.
2. **List the inputs.** Separate available inputs from missing inputs, and identify which missing items are blockers versus nice-to-have context.
3. **Set the session frame.** Confirm total time, energy level, environment, and whether the session should optimize for speed, quality, clarity, or momentum.
4. **Split the session.** Divide the time into focused blocks such as setup, core work, AI-assisted expansion, review, decision, and wrap-up.
5. **Add checkpoints.** Insert short checkpoint prompts at natural moments so the user can inspect progress, adjust scope, or stop drifting.
6. **Define AI roles.** State where AI should help and where the user should make the decision, check accuracy, or provide judgment.
7. **Define the done-state.** Describe the minimum acceptable finish, a strong finish, and what to defer if time runs out.
8. **Add a fallback plan.** If inputs are missing or the session gets interrupted, provide a smaller version that still creates useful progress.

## Output Format

Produce the work session plan with these sections:

1. **Session Goal**
   - Plain-language goal
   - Session objective
   - Intended output
   - Time available
2. **Inputs Check**
   - Inputs ready now
   - Missing inputs
   - Blockers to resolve first
   - Assumptions used for the plan
3. **Timed Plan**
   - Start-up block
   - Core work blocks
   - AI-assisted blocks
   - Review block
   - Wrap-up block
4. **Checkpoints**
   - Time marker
   - Question to answer
   - Decision or adjustment to make
5. **AI Prompts to Use**
   - Prompt for clarifying the task
   - Prompt for generating or structuring work
   - Prompt for review or critique
   - Prompt for final polish, if useful
6. **Done-State**
   - Minimum acceptable done
   - Strong done
   - Stop condition
7. **Fallback Plan**
   - If key inputs are missing
   - If only half the time remains
   - If energy drops

## Safety Boundary

- Do not pretend missing inputs are available. Flag missing materials, unclear decisions, and unverified assumptions.
- Do not encourage the user to skip required approvals, confidentiality checks, factual review, or human judgment.
- Do not ask for passwords, secret keys, private credentials, or sensitive account access.
- Do not create an overstuffed plan that cannot fit the stated time. Reduce scope when the goal is too large.
- Keep AI use supportive rather than automatic. Mark where the user must verify facts, make decisions, or review tone.
- If the task involves legal, medical, financial, employment, or safety-critical decisions, frame AI output as drafting or organization support only and recommend appropriate human review.

## Example Prompts

Copy and paste one of these to start:

1. **"I have 90 minutes and need to make progress on my quarterly project review. The draft is half-written but I keep getting distracted. Help me plan a focused work session with checkpoints so I actually finish a clean draft."**

2. **"I'm stuck on a messy task — I need to prepare slides for a team update tomorrow. I have notes scattered across three docs. Plan a 60-minute session where AI helps me structure and draft, but I stay in control of the final message."**

3. **"I have 120 minutes to make headway on a research synthesis for a client proposal. I've got five articles bookmarked and two pages of notes. Help me set up a session plan with research, drafting, and review blocks so I don't just read all morning."**

## Install-First Success Path

**Input:** The user says "I have a messy project and 90 minutes — help me make a focused work plan."

**Steps:**
1. The skill captures the goal: rewrites the messy statement as a clear session objective and practical outcome.
2. Lists available inputs, missing inputs, and flags which missing items are blockers versus nice-to-have context.
3. Sets the session frame: confirms total time, energy level, and whether the session optimizes for speed, quality, clarity, or momentum.
4. Splits the session into timed blocks: setup, core work, AI-assisted expansion, review, decision, and wrap-up.
5. Inserts checkpoint questions at natural moments so the user can inspect progress and adjust scope.
6. Defines where AI helps and where the user must make decisions, check accuracy, or provide judgment.
7. Produces the done-state: minimum acceptable finish, strong finish, and what to defer if time runs out.

**Output:** A timed session plan with goal, inputs check, blocks, checkpoints, AI prompts, done-state, and fallback plan — ready for the user to start the session immediately.

## Quality Checklist

A strong result should:

- Convert a messy goal into a clear session objective
- Identify available inputs, missing inputs, blockers, and assumptions
- Fit within a 60 to 120 minute session
- Include specific time blocks and checkpoint questions
- Define a realistic minimum done-state and strong done-state
- Include AI prompts that match the work, not generic productivity advice
- Provide a fallback plan for missing inputs, interruptions, or low energy
