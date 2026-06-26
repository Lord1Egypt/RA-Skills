# Brainhack — OpenClaw Agent Pack

**The first AI sidekick built for ADHD minds.**

---

## What This Is

Not a productivity app. Not a chatbot. A fully configured agent that already knows how ADHD brains work, already speaks the language, and has the systems baked in.

The shift: from "here are prompts to try" to "your sidekick is already running."

---

## File Structure

```
brainhack/
├── SOUL.md           — Who the agent is
├── BRAIN.md          — ADHD operating protocol
├── USER.md           — Onboarding profile (generated per user)
├── ROUTER.md         — Skill selection logic
├── MEMORY.md         — State tracking & pattern recognition
├── VOICE.md          — Tone calibration
│
├── skills/           — 17 operational skills
│   ├── brain-dump         Chaos → organized, actionable output
│   ├── task-chunker       Any task → ADHD-friendly micro-steps
│   ├── day-architect      Build today's flexible plan
│   ├── week-planner       Zoom out, map the week
│   ├── body-double        Virtual accountability presence
│   ├── hype-engine        Motivational activation
│   ├── spiral-catcher     Emotional first aid
│   ├── meltdown-mode      Emergency protocol — one breath, one anchor, one action
│   ├── daily-rhythm       Proactive daily outreach — morning + evening anchors
│   ├── social-scripter    Write hard messages
│   ├── study-buddy        Learning for ADHD brains
│   ├── adulting-coach     Life admin, bills, appointments
│   ├── check-in           Daily reflection ritual
│   ├── routine-builder    Flexible, sustainable routines
│   ├── explain-it         Complex → simple
│   ├── win-tracker        Celebrate and log victories
│   └── voice-shifter      Personality on demand
│
├── knowledge/        — 6 reference files
│   ├── adhd-executive-function.md
│   ├── cbt-dbt-toolkit.md
│   ├── dopamine-design.md
│   ├── prompt-library.md
│   ├── tool-integrations.md
│   └── adhd-research-base.md
│
├── personas/         — 3 voice modes
│   ├── coach.md           Default: Trusted Cool Mentor
│   ├── hype-friend.md     Maximum energy
│   └── calm-anchor.md     Grounding presence
│
└── memory/
    ├── wins.md            Permanent achievement log
    ├── patterns.md        Learned user patterns
    └── YYYY-MM-DD.md      Daily session state
```

---

## Setup

1. Run onboarding: agent asks 4 questions in casual conversation (~2 min), populates USER.md
2. Start talking: ROUTER.md maps everything the user says to the right skill
3. Memory builds over time: MEMORY.md accumulates patterns and state

---

## What Makes This Different

1. **Agent, not app.** Lives in Telegram/WhatsApp. No new app to download, forget about, and feel guilty about.
2. **It learns you.** Memory means it gets better over time.
3. **Emotional intelligence.** Detects spirals and responds accordingly before touching any task.
4. **Modular.** Install all 15 skills or just the 5 core ones.
5. **Designed for inconsistency.** No punishment for missing a day. Just shows up again tomorrow.

---

## Core Philosophy

ADHD isn't a deficit. It's a different operating system that needs better software.

- Motivation is neurochemical, not moral.
- Shame makes ADHD worse, not better.
- Consistency is built in systems, not willpower.
- Small wins compound.

---

## Distribution

**Free tier (5 core skills):** brain-dump, task-chunker, day-architect, hype-engine, check-in, meltdown-mode

**Pro ($9/mo):** All 15 skills + calendar integration + memory + pattern recognition

**ClawHub:** `openclaw skills install brainhack-adhd-sidekick`
