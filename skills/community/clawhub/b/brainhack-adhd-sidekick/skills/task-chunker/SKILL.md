---
name: task-chunker
description: Break any task into ADHD-friendly micro-steps. Use when a task feels too big to start, user expresses overwhelm about a specific task, or after brain-dump identifies a task needing breakdown.
metadata:
  tags: [brainhack, adhd, tasks, planning]
---

# Task Chunker

## Purpose
The Goblin Tools Magic ToDo, but native and personal. Any task, no matter how big, becomes manageable when it's small enough. This skill does the breaking-down.

## Trigger
- User names a large or intimidating task
- "I don't know where to start"
- "This feels too big"
- "Break this down for me"
- Task identified from brain-dump output

## Process

### Step 1: Name the task clearly
Make sure you have the actual task. "Do the project" → "Write the introduction section of the project."

### Step 2: Choose spiciness level
Ask if unknown, or infer from context:
- **Level 1 (broad):** 3-5 steps, wider chunks
- **Level 2 (default):** 5-7 detailed steps
- **Level 3 (teeny tiny mode):** 7-10 micro-steps, each under 5 minutes

### Step 3: Break it down
Rules:
- Each step starts with a VERB (action-first language)
- Each step completable in under 15 minutes (level 2) or under 5 minutes (level 3)
- Add time estimates to each step
- Steps should be in logical order but NOT required to be done in that order

### Step 4: Identify the easiest step (not the first — the easiest)
Not the most important. The one that requires the least resistance. Sometimes that's step 4. Start there.

### Step 5: Offer body double
"Want to do that first step together right now? I can sit with you."

## Output Format

```
Here's [Task] broken into [N] steps:

1. [Verb] [specific action] — ~[X] min
2. [Verb] [specific action] — ~[X] min
3. [Verb] [specific action] — ~[X] min
4. [Verb] [specific action] — ~[X] min
5. [Verb] [specific action] — ~[X] min

→ Easiest starting point: Step [N] — "[action]"
That one's low-resistance. Do that one first.

Want to start now? I can body double with you.
```

## Spiciness Examples

### Level 2: "Write a cover letter"
1. Open a new doc — 2 min
2. Write the company name and role at the top — 1 min
3. Write 2 sentences about why you want this job — 5 min
4. Write 2 sentences about your most relevant experience — 5 min
5. Write 1 sentence closing — 2 min
6. Read it out loud once — 3 min
7. Send / save draft — 1 min
→ Easiest start: Step 1. Open the doc. That's it.

### Level 3: "Clean my room" (teeny tiny mode)
1. Pick up everything on the floor — 5 min
2. Put clean clothes away — 3 min
3. Move dirty clothes to hamper/laundry — 2 min
4. Clear the desk surface (put stuff in a pile) — 3 min
5. Sort the pile: keep/trash/move — 5 min
6. Deal with trash pile — 1 min
7. Wipe down desk — 2 min
8. Make the bed — 3 min
9. Do a 30-second "anything looks obviously wrong?" check — 1 min
→ Easiest start: Step 8. Making the bed is satisfying and takes 3 minutes.

## Rules
- Never overwhelm with more than 7 steps visible at first
- Always name the easiest step, not the first step
- Never say "just" in front of a step ("just open the doc")
- If user seems really stuck: go to Level 3 automatically, even if they didn't ask

## References
- BRAIN.md: Task initiation section
- knowledge/adhd-executive-function.md
- knowledge/dopamine-design.md
