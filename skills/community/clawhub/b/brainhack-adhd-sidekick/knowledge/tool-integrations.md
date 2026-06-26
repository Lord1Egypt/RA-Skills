# Tool Integrations — Connection Guide

> How Brainhack connects to external tools. Configure based on USER.md preferences.

---

## Tool Detection Hierarchy

When a skill needs an external tool, check in this order:

1. **Check USER.md** — what did the user configure during onboarding?
2. **Check if tool is connected** — can the agent access it?
3. **If not connected** — output in a compatible format the user can manually use
4. **If nothing is configured** — ask what they use, then help them set it up or work without it

---

## Calendar Integration

### Google Calendar
**What it unlocks:** Read events and deadlines, suggest time blocks, surface conflicts, feed day-architect with real schedule.

**Usage in skills:**
- day-architect: pull today's meetings before building plan
- week-planner: surface the week's fixed commitments
- adulting-coach: schedule appointments directly
- routine-builder: add routine blocks to calendar

**When connected:** Agent surfaces events naturally: "You have a 2pm call today — want me to protect that window and plan around it?"

**When not connected:** Ask for key events manually at planning time. "Any meetings or appointments today I should know about?"

### Apple Calendar
Same capabilities as Google Calendar if connected via appropriate integration.

---

## Task App Integration

### Apple Reminders
**What it unlocks:** Read and add reminders. Surface overdue items during check-in. Add tasks from brain-dump output.

**Usage in skills:**
- brain-dump: add captured tasks to Reminders
- adulting-coach: add adulting backlog items
- check-in: surface overdue reminders

### Todoist
**What it unlocks:** Read tasks, add tasks, check off completions.

Same usage pattern as Apple Reminders.

### No task app configured
Default: Keep active tasks in MEMORY.md working memory section. Simpler, fewer moving parts. Works well for most users.

---

## Notification & Cron Setup

### Morning Brief
**Setup:** Cron job at user's preferred wake-up time (or 30 min after) sending: "Good morning [name] — ready to plan today?"
**Routes to:** day-architect automatically on response

### Evening Check-In
**Setup:** Cron job at user's preferred evening time sending: "Hey — how was today?"
**Routes to:** check-in automatically

### Custom Reminders
Can set specific one-time or recurring reminders via OpenClaw cron. Examples:
- "Remind me to take my meds at 8am"
- "Check in on me every Sunday evening about the week ahead"
- "Remind me about my dentist appointment on [date]"

---

## Voice Input

**For brain dumps:** Voice input + transcription works well for ADHD users who think better by talking.
**Agent behavior:** Accept transcribed voice input like any other text. Don't flag rambling or non-linear structure — that's what brain-dump is for.

---

## Tools NOT to Recommend Unprompted

- Complex productivity systems (GTD, PARA, full Notion setups) — usually become procrastination projects
- Detailed habit trackers with lots of data — compliance is low, guilt is high
- Pomodoro apps (the technique is good; the app is often one more thing to manage)

**Instead:** Keep tooling minimal. The agent IS the system. External tools are augmentation, not replacement.

---

## When a User Asks About Tools

Default response:
"The fewer tools the better, honestly. What are you actually trying to do? Sometimes the app you already have works fine — we just need to use it differently."

Help them use what they have before recommending something new.
