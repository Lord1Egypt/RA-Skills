---
name: day-architect
description: Build today's flexible plan. Not a rigid schedule — a loose architecture with buffers, energy awareness, and one optional bonus task. Use for morning planning, "what should I do today," or when user needs to organize a day.
metadata:
  tags: [brainhack, adhd, planning, daily]
---

# Day Architect

## Purpose
Build a day that's actually doable. Not a schedule — an architecture. Flexible enough to survive the unexpected, structured enough to give the ADHD brain a track to run on.

## Trigger
- Morning first message (default route)
- "Plan my day"
- "What should I do today?"
- "Help me figure out today"

## Process

### Step 1: Check context
- Any open loops from yesterday? (MEMORY.md)
- Calendar events or known deadlines? (tool-integrations.md if connected)
- User's energy level right now? (ask if unclear)

### Step 2: The magic question
"What are the 1-3 things that would make today a win?"

**Never ask for more than 3.** Never suggest more than 3. If they list 8 things, help them pick 3.

### Step 3: Map energy to tasks
From USER.md:
- High-energy window → hardest or most important task
- Low-energy window → admin, easy tasks, communication
- Buffer window → overflow, unexpected stuff

### Step 4: Build the architecture
Loose time blocks, not rigid schedule. Include:
- Priority task windows (matched to energy)
- Breaks — at least 2, framed as dopamine recharges not just rest
- Buffer block (30-60 min of nothing planned)
- One optional "bonus" task that's lower stakes or even enjoyable

### Step 5: Check meetings
If calendar connected: surface any meetings and protect 30 min before/after for transition.

### Step 6: Deliver and offer
Send the plan. End with: "Ready to start with [first task]? I can body double with you."

## Output Format

```
Today's architecture 🗓️

Morning [energy level]:
→ [Priority task] — [time estimate]

Midday:
→ Break / lunch / whatever ☕
→ [Secondary task or admin]

Afternoon:
→ [Secondary task]
→ Buffer block — for whatever comes up

Optional bonus: [lower-stakes / enjoyable task]

→ Win condition for today: [the 1-3 things they said]

Ready to start? I can sit with you on [first task].
```

## Rules

**Hard rules — never violate:**
- Max 5 tasks in a day plan. If they listed more: help them choose 5.
- Always include at least 2 breaks
- Always include a buffer block
- If user seems low-energy at planning time: reduce to 2-3 tasks and name it: "Low energy day? Let's keep it light — 3 things max."
- Never schedule more than 90 continuous minutes without a break
- Protect 30 min before/after meetings if calendar shows any

**If user has no idea what they need to do:**
→ Run brain-dump first, then return to day-architect.

## References
- BRAIN.md: Energy/attention cycles, overwhelm thresholds
- USER.md: Energy patterns, calendar integrations
- knowledge/adhd-executive-function.md
- knowledge/dopamine-design.md
- knowledge/tool-integrations.md
