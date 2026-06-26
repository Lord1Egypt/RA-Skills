---
name: focus-session-timer
description: Build a focused work session card with the right session mode, a visible finish line, start ritual, distraction capture plan, break rule, and interruption recovery. Use when the user wants help choosing between a quick sprint, standard focus block, or deep work block without relying on an actual timer app.
---

# Focus Session Timer

## Overview

Use this skill to shape one work or study block into a clear, recoverable session instead of a vague attempt to "focus harder." It helps the user match session length to task difficulty, define what done looks like, protect attention during the block, and restart cleanly after interruptions.

This skill is descriptive only. It does not run a stopwatch, trigger notifications, or connect to focus apps.

## Trigger

Use this skill when the user wants to:
- choose the right focus block for a task
- define one visible finish line before starting
- reduce distraction drift during work or study
- recover from interruptions without abandoning the session
- end a session with a clean handoff into the next block

### Example prompts
- "Help me set up a deep work block for writing"
- "I need a focus session card for studying calculus"
- "I keep getting interrupted and losing my work rhythm"
- "Choose a better work interval than random Pomodoros"

## Workflow

1. Identify the task and how cognitively heavy it is.
2. Match the task to a mode: Quick Sprint, Standard Focus, or Deep Work Block.
3. Define a visible finish line for the session.
4. Add a start ritual, distraction capture method, and break rule.
5. Add an interruption recovery protocol.
6. End with a short debrief and next starting point.

## Inputs

The user can provide any mix of:
- the task or study target
- difficulty or cognitive load
- time available
- energy level
- interruption risk
- work, family, or support-role constraints
- what usually derails focus

## Outputs

Return a markdown focus card with:
- session goal and definition of done
- chosen mode
- start ritual
- during-session distraction handling
- break plan
- short end review

## Safety

- Keep one session equal to one clear objective.
- Match the session mode to real energy and interruption risk, not idealized ambition.
- Encourage breaks that restore attention instead of fragmenting it.
- Do not pretend this skill is an actual timer or attention-treatment tool.

## Acceptance Criteria

- Return markdown text.
- Include a clear task, definition of done, and chosen mode.
- Include interruption recovery and a next starting point.
- Keep the session realistic for the stated context.
