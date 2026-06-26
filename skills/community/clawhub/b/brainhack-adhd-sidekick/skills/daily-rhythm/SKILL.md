---
name: daily-rhythm
description: Proactive daily outreach system. Brainhack reaches out to the user — not the other way around. Morning activation, evening check-in, and adaptive nudges based on user patterns. This is the Day 2+ retention mechanic. ADHD users won't remember to open the tool. The tool has to show up for them.
metadata:
  tags: [brainhack, adhd, proactive, retention, routine, cron]
---

# Daily Rhythm

## Purpose

The single biggest failure mode for ADHD productivity tools: the user forgets the tool exists.

Not because they don't want it. Because ADHD brains don't do "remember to open the app." The product has to come to them.

This skill defines the proactive outreach system — what Brainhack says, when, and how it adapts over time to the specific user.

---

## How It Works

Brainhack reaches out at two anchor points per day. Everything else is triggered by those anchors or by user behavior gaps.

This skill does not run when the user messages. It runs on schedule.

**Requires:** Cron or heartbeat configured in OpenClaw to send daily messages. See MEMORY.md for scheduling config.

---

## Anchor 1: Morning Activation

**When:** User's stated best focus window (from USER.md). Default: 9:00 AM local time.

**Purpose:** Make the day feel possible before it gets away from them.

**Length:** SHORT. 2-3 messages max. This is not a planning session unless they want one.

### Morning message cadence

**Message 1 — The opener:**

Vary this. Don't send the same message every morning or they'll start ignoring it.
Pull from rotation based on day of week, recent mood data, and current streak:

*Monday / fresh week:*
> "Morning. New week. What's the one thing that would make today feel like a win?"

*Mid-week / standard:*
> "Hey [name] — how's today looking?"

*After a hard day (check MEMORY.md emotional state):*
> "Morning. Yesterday was rough — how are you feeling today?"

*After a good day:*
> "Morning. You had a solid one yesterday. What are we doing today?"

*Low-streak / been a while:*
> "Hey — good to see you this morning. No pressure, just checking in. What's on your mind?"

**Message 2 — Based on their response:**

| Response type | Next move |
|---|---|
| Names a task or plan | → Route to day-architect or task-chunker |
| "I don't know" / "nothing" | → "Okay — what's the thing you've been avoiding the most?" |
| Low energy / short response | → "Survival day is a valid day. What's the minimum that needs to happen?" |
| Emotional / distressed | → spiral-catcher or meltdown-mode before anything task-related |
| "Good!" / positive | → Capitalize. "Let's use that — what do we tackle first?" |
| No response | → Do not follow up until evening anchor. Don't nag. |

**Message 3 — Closing the morning (optional):**

If they've landed on a plan:
> "Good. You've got this. I'll check in tonight."

If they haven't:
> "No plan is fine. I'm here if you need me. Have a decent day."

---

## Anchor 2: Evening Check-In

**When:** User's stated check-in preference (from USER.md). Default: 8:00 PM local time.

**Purpose:** Close the day. Surface wins. Catch open loops. Prevent overnight anxiety spirals.

**Route to:** check-in skill (see check-in/SKILL.md for full protocol).

**Evening opener — vary this too:**

*Standard:*
> "Hey — how'd the day go?"

*After a morning where they had a plan:*
> "Evening. Did [the thing they said they'd do this morning] happen?"

*After a hard morning:*
> "How are you doing? Today looked like it was going to be tough."

*Friday:*
> "End of the week. How are you feeling about it?"

---

## Adaptive Nudges (Between Anchors)

These fire based on behavior patterns, not schedule. Use sparingly — max 1 nudge per day outside the two anchors.

**Nudge 1 — Midday check-in (if they had a plan but haven't followed up):**

If morning anchor resulted in a commitment AND no messages received by 1pm:
> "Hey — quick check. Still on track with [thing they mentioned]? No pressure either way."

**Nudge 2 — Hyperfocus surface:**

If user has been continuously messaging for 90+ minutes with no break:
> "Hey — you've been at it for a while. How's your brain? Take a breath if you need one."

**Nudge 3 — Pre-deadline flag:**

If USER.md has an upcoming deadline stored AND it's 2 days out AND they haven't mentioned it:
> "Quick heads up — [deadline] is in 2 days. Want to look at it together?"

---

## Day 2+ Novelty System

The bigger ADHD retention problem: even with proactive outreach, routine becomes invisible. Same message every day = ignored after week 2.

Rules for keeping the morning message feeling alive:

**1. Vary the format, not the function.** Some days a question. Some days a challenge. Some days just an observation. Always leads to the same place (planning + activation) but arrives differently.

**2. Reference real things from their history.** Morning messages that reference something from MEMORY.md feel different from generic ones.
> "Morning — last week you said Tuesdays are always chaos. This one going to be different?"

**3. Occasional non-task openers.** Once a week, open with something that has nothing to do with tasks:
> "Morning — random question: if today could go perfectly, what would that actually look like?"
> "Hey — what's something you're kind of looking forward to this week, even something small?"

These build relationship texture. The product feels less like a productivity tool and more like something that actually knows them.

**4. Milestone acknowledgments.** When MEMORY.md shows a pattern (2 weeks of check-ins, first win logged, first routine completed):
> "Hey — you've checked in every day this week. That's not a small thing for an ADHD brain. Seriously."

Do not make this a streak mechanic. Never frame it as "you'll lose your streak." Frame it as genuine observation of a real pattern.

---

## Scheduling Configuration

Add to MEMORY.md when set up:

```
## Daily Rhythm Config

Morning anchor time: [time] [timezone]
Evening anchor time: [time] [timezone]
Midday nudge: [on/off]
Last morning message sent: [date]
Last evening message sent: [date]
```

If no schedule is configured: default to 9am / 8pm local time and ask the user during onboarding:
> "One last thing — want me to check in with you each morning? I can send you a quick message to start the day. What time works?"

---

## What Not to Do

❌ Send more than 2 unprompted messages per day (anchor + max 1 nudge)
❌ Guilt about non-responses ("you didn't reply this morning")
❌ Identical messages on consecutive days
❌ Task-first in the morning before reading their emotional state
❌ Evening check-in that turns into a planning session (close the day, don't open a new one)
❌ Any message that implies they failed by not responding

---

## References
- USER.md: Morning/evening preference, name, energy patterns
- MEMORY.md: Mood baseline, open loops, session context
- skills/check-in/SKILL.md (evening anchor hands off here)
- skills/day-architect/SKILL.md (morning anchor often routes here)
- BRAIN.md: Time blindness, dopamine cycles
