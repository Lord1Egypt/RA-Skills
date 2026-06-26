# AI Personal Brand Growth Engine
### The only content system that gets smarter every time you post.

---

## What This Is

A **self-evolving AI content operating system** for X (Twitter) and LinkedIn.
Not a prompt. Not a template pack. A full micro-architecture that remembers what works,
learns from every post you publish, and compounds your growth over time.

Every post you create feeds the engine. Every data point you enter makes the next batch
better. The longer you use it, the more it knows about your audience, your voice, and
your winning formulas — and the less you have to think.

---

## The Core Feedback Loop

```
Generate → Publish → Collect Data → Analyze → Promote Winners → Generate Better
    ↑                                                                    │
    └────────────────────── (cycles tighter each round) ────────────────┘
```

**Conventional tools:** Same generic output, forever.  
**This engine:** Each cycle produces higher-quality, more targeted content — automatically.

---

## File Structure

```
AI-Personal-Brand-Growth-Engine/
├── SKILL.md                   ← Master brain (upload to ClawHub as main skill)
├── SOUL.md                    ← Brand identity + failure library (you create this)
├── AUDIENCE_PERSONA.md        ← Target audience model (you create this)
├── assets/
│   ├── POST_TEMPLATE.md       ← Schema for each post record
│   └── VIRAL_FORMULAS.md      ← Living formula library (AI self-populates)
├── .content/
│   ├── POST-YYYYMMDD-XXX.md   ← Individual post logs (AI creates these)
│   └── FEEDBACK_LOG.md        ← Performance signal ledger (AI auto-appends)
└── scripts/
    ├── pre-generation-hook.sh ← Context injector (run before content sessions)
    └── growth-reminder.sh     ← Stale post auditor (run at session start)
```

---

## Installation (3 Steps)

### Step 1 — Upload to ClawHub

Upload all files maintaining the directory structure above.  
`SKILL.md` is the entry point — register it as the primary skill file.

### Step 2 — Complete your Brand Foundation (one-time, ~10 minutes)

On first run the AI will guide you through two setup files:

**`AUDIENCE_PERSONA.md`**
- Who are you talking to? Demographics, psychographics
- Top 3 pain points and desires
- Platform behavior and scrolling patterns
- Exact language and phrases your audience uses

**`SOUL.md`**
- Your niche and unique point of view
- Voice rules (tone, style, what to never say)
- Your offer / service description
- Content red lines
- *(Failure Library auto-populates here over time)*

### Step 3 — Start your first session

Say to the AI:
> *"Help me post 5 pieces of content for today."*

The engine loads your Brand Foundation, checks your Content Pillar matrix, and
generates a balanced batch. From there, just follow the system.

---

## Using the Shell Scripts (Optional)

```bash
# Make executable
chmod +x scripts/pre-generation-hook.sh
chmod +x scripts/growth-reminder.sh

# Run at the start of every session
./scripts/growth-reminder.sh

# Run before asking the AI to generate content
./scripts/pre-generation-hook.sh
# → Copy the output block into your prompt
```

---

## Core Features

| Feature                    | What It Does                                                          |
|----------------------------|-----------------------------------------------------------------------|
| **Trigger Matrix**         | AI detects intent and runs the right protocol automatically           |
| **Content Pillar Balance** | Every batch enforces Value / Story / Engagement / Conversion mix      |
| **Post Lifecycle Tracking**| Every post moves draft → published → analyzed with full audit trail   |
| **Memory Leap**            | Winning posts are auto-distilled into reusable formulas               |
| **Failure Library**        | Losing patterns are logged in SOUL.md — never repeated                |
| **Growth Reminder**        | Flags unanalyzed posts so no data is lost                             |
| **Conversion Guard**       | Guarantees every daily batch includes ≥1 monetization post            |

---

## The Compound Growth Timeline

| Period  | What Happens                                                                  |
|---------|-------------------------------------------------------------------------------|
| Week 1  | Brand Foundation set. Content quality stabilizes. First formulas may appear.  |
| Month 1 | 3–5 promoted formulas in library. AI output noticeably more targeted.         |
| Month 3 | 10–20 formulas. Near-zero-effort content generation. Audience model refined.  |
| Month 6 | Deep failure-pattern data. Measurably higher engagement and conversion rates. |
| Month 12| Full compound flywheel. Your AI knows your audience better than most humans.  |

---

## Key Triggers (What to Say)

| You Say                            | Engine Does                                          |
|------------------------------------|------------------------------------------------------|
| "Help me post 5 things today"      | Triggers Trigger A — full content generation batch   |
| "This post got 500 likes"          | Triggers Trigger B — metrics logged, Memory Leap check |
| "Promote my consulting service"    | Triggers Trigger C — 3 conversion post variants      |
| "Analyze my recent performance"    | Triggers Trigger D — full Growth Report              |

---

## Philosophy

> Most creators treat content like a cost center — something to be endured daily.  
> This engine treats content like a data system — something that compounds over time.
>
> The difference between a creator stuck at 500 followers and one at 50,000 is rarely
> talent. It's **systematic feedback loops**. This engine builds those loops for you,
> and it never forgets.

---

*Built for ClawHub / OpenClaw. Requires a file-system-aware AI agent environment.*  
*Compatible with any Claude-based deployment that supports persistent file read/write.*
