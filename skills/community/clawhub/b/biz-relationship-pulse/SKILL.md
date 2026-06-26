---
name: biz-relationship-pulse
description: Scans email and LinkedIn for stalled commercial relationships and surfaces re-ignition candidates with scored briefs. Use when a user wants to warm up cold leads, revive partnerships, or identify investor conversations worth restarting.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch
metadata:
  openclaw.emoji: "🤝"
  openclaw.user-invocable: "true"
  openclaw.category: relationships
  openclaw.tags: "networking,crm,sales,pipeline,linkedin,outreach,cold-leads"
  openclaw.triggers: "cold leads,reconnect,business contacts,stalled deals,re-engage,who should I reach out to"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/biz-relationship-pulse


# Biz Relationship Pulse

Finds the conversations that went quiet at the wrong moment.
Not the ones that ended naturally — the ones where something was left open.

Surfaces 3-5 people per week. For each one: who they are, what stalled, what's changed since, and one specific line to re-open it.

---

## Scope — existing relationships only

This skill re-ignites **existing stalled conversations** — people the user
has previously spoken with and who have gone quiet. It is not for:
- Cold outreach to people the user has never contacted
- Lead generation or prospect acquisition
- Mass outreach or automated sales sequences

Every contact surfaced must already exist in the user's communication history.
The opening lines restart real conversations — they do not initiate new ones.

---

## The difference from relationship-pulse

`relationship-pulse` — personal relationships. People you care about. Friendship maintenance.
`biz-relationship-pulse` — commercial relationships. Deals, partnerships, door-openers, former clients. Revenue and opportunity.

Different detection logic. Different output. Different stakes.

---

## File structure

```
biz-relationship-pulse/
  SKILL.md
  config.md          ← relationship types, sources, scoring weights, context
  pipeline.md        ← scored contact log, stall reasons, last action, status
  context.md         ← what you're working on now — used to match relevance
```

Token discipline: weekly cron reads only `config.md` + `pipeline.md` + `context.md`.

---

## What counts as a stalled conversation

A conversation is stalled — not ended — when:

**Recency signal:**
- Was actively exchanged (3+ messages back and forth) within the last 18 months
- Then went quiet for 60+ days with no clean resolution
- Last message was not a hard no or a natural close ("great working with you, take care")

**Momentum signal:**
- The thread contained forward-looking language: "let's reconnect", "follow up next quarter", "send me more when you're ready", "timing isn't right but keep me posted"
- A concrete next step was mentioned but never happened
- One party went quiet mid-thread without a clear reason

**Relationship type signal:**
- Was tagged or inferable as: prospect, partnership discussion, investor conversation, former client, connector/advisor

**Recency of last contact:**
- Cold zone: 6-18 months (most re-ignitable — enough time has passed, not so long it's awkward)
- Warm zone: 2-6 months (still recent enough, something clearly stalled)
- Archive zone: 18+ months (surface only if context.md shows a specific reason to reconnect now)

---

## Sources and what to extract

### Gmail
- Search sent + received threads with external contacts
- Flag: threads with 3+ exchanges that went quiet
- Extract: last message sender, last message content, any forward-looking language, implied next step
- Note: who went quiet — did they stop replying, or did you?

### LinkedIn (if connected via MCP)
- Connection requests accepted but no follow-up conversation
- Message threads that stalled
- Profile views from people in your network — they looked you up recently, timing may be right
- Recent job changes or company news for contacts in pipeline.md — a trigger to reach out

### WhatsApp (if accessible via channel)
- Business conversations that went quiet
- Voice note conversations with no follow-up
- Group chats with relevant contacts

### context.md (internal)
- What are you actively working on, selling, or building right now?
- Who would be specifically relevant to current projects?
- Any names or companies you want to prioritise?

---

## Scoring model

Each candidate contact gets scored across five dimensions:

**1. Momentum score (0-3)**
- 3: had explicit next step that never happened, or they said "follow up in X weeks"
- 2: warm exchange that tapered off, no explicit close
- 1: light exchange, interest was implied but not stated
- 0: one-sided (only you reached out) or clearly ended naturally

**2. Recency score (0-3)**
- 3: stalled 2-6 months ago (warm zone)
- 2: stalled 6-12 months ago
- 1: stalled 12-18 months ago
- 0: stalled 18+ months ago (unless context.md gives specific reason)

**3. Relationship value score (0-3)**
- 3: former client or active deal prospect
- 2: partnership or collaboration discussion
- 2: investor or serious door-opener
- 1: connector or loose advisor conversation
- 0: unclear or low commercial relevance

**4. Context relevance score (0-3)**
- 3: directly relevant to what's in context.md right now
- 2: adjacent — would be useful but not primary
- 1: general network value
- 0: no clear current relevance

**5. Re-ignition plausibility score (0-3)**
- 3: there's a natural hook — their company is in the news, they changed roles, something relevant happened
- 2: time has passed cleanly — "it's been a while" is a natural opener
- 1: harder to re-open without it feeling like a delayed sales follow-up
- 0: would feel forced or inappropriate to reach out

**Total: 0-15. Surface contacts scoring 8+.**
If fewer than 3 score 8+, lower threshold to 6+ for that week.
Hard cap: surface maximum 5 contacts per week. Quality over quantity.

---

## Setup flow

### Step 1 — Connect sources

Confirm which sources are available:
- Gmail: check if connected
- LinkedIn MCP: check if connected
- WhatsApp: check if accessible via channel

Note which are unavailable. The skill runs with whatever is connected — it doesn't fail on missing sources.

### Step 2 — Build context.md

This is the most important setup step.

Ask the user:
"What are you actively working on right now? What would make a re-connection commercially useful — are you fundraising, selling something, looking for partnerships, hiring, or something else?"

Also ask:
"Are there any specific people or companies you've been meaning to reach out to but haven't?"

Write context.md:

```md
# Current Context

## What I'm working on
[Description of current projects, sales focus, fundraising status, etc.]

## Relationship types to prioritise this quarter
[e.g. "investors for Series A", "enterprise clients in DACH", "marketing partnerships"]

## Specific people to watch for
[Names or companies — surface these even if score is below threshold]

## Relationship types to deprioritise
[e.g. "early-stage conversations that went nowhere", "irrelevant industries"]
```

### Step 3 — Write config.md

```md
# Biz Relationship Pulse Config

## Sources
gmail: true
linkedin: true
whatsapp: true

## Relationship types to track
prospects: true
partnerships: true
investors: true
former_clients: true
connectors: true

## Scoring thresholds
surface_above: 8
fallback_threshold: 6
max_per_week: 5

## Stall detection
cold_zone_months: 6-18
warm_zone_months: 2-6
archive_months: 18

## Delivery
channel: [CHANNEL]
to: [TARGET]
day: Monday
time: 08:30
```

### Step 4 — Initial pipeline scan

On first run, do a full scan across all sources going back 18 months.
Build pipeline.md with all candidates found.
This first run will take longer — worth flagging to the user.

### Step 5 — Register cron job

Weekly, Monday morning, isolated, lightContext.

```json
{
  "name": "Biz Relationship Pulse",
  "schedule": { "kind": "cron", "expr": "30 8 * * 1", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run biz-relationship-pulse. Read {baseDir}/config.md, {baseDir}/pipeline.md, and {baseDir}/context.md. Scan connected sources (Gmail, LinkedIn, WhatsApp) for stalled commercial conversations. Score each candidate. Surface top 3-5 scoring 8+ (or 6+ if fewer qualify). For each: write a relationship brief and one specific re-opening message. Update pipeline.md. Deliver via configured channel.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. Read config, pipeline, context

Load scoring preferences, what's been surfaced before, and current commercial priorities.

### 2. Scan sources

**Gmail scan:**
- Search sent mail for external contacts going back 18 months
- Find threads with 3+ exchanges that went quiet
- Extract: last message date, last sender, any forward-looking language
- Note: did you send last (they went quiet) or did they send last (you went quiet)?

**LinkedIn scan (if connected):**
- Check message threads for stalled conversations
- Check for recent profile views from pipeline contacts
- Check for job changes or company news from pipeline contacts

**WhatsApp scan (if accessible):**
- Check business-context conversations
- Flag any threads with pending follow-ups

### 3. Score all candidates

Apply the five-dimension scoring model.
Cross-reference context.md for relevance boost.
Flag any names mentioned specifically in context.md — surface regardless of score.

### 4. Pick top 3-5

Select highest scoring contacts not surfaced in the last 4 weeks.
Avoid surfacing the same person twice in a month.

### 5. For each contact — generate the brief

**Section A: Who they are and what the relationship was**

[NAME] — [Title] at [Company]
*Relationship type: [prospect / partner / investor / former client / connector]*
*Last contact: [X months ago] via [Gmail / LinkedIn / WhatsApp]*

[One sentence: what the conversation was about]
[One sentence: where it stalled and why]

---

**Section B: Why now**

Score: [X/15]
[The specific reason this person is worth re-igniting now — either a trigger event or a clean time-has-passed window]

Examples of good "why now":
- "They changed roles 3 weeks ago — natural moment to reconnect"
- "Their company just announced a funding round — relevant to what you're building"
- "It's been exactly 6 months since they said 'follow up in Q2'"
- "You're now working on [X from context.md] — directly relevant to what they were looking for"

If there's no specific trigger, say: "No recent trigger — but 8 months is a clean enough gap that re-opening won't feel like a delayed chase."

---

**Section C: What to say**

One specific opening line. Not a template. Written for this person, this context.

Rules:
- References something specific from the conversation history — not generic
- Does not feel like a sales follow-up
- Has a reason to reach out that isn't "just checking in"
- Short enough to send as-is or with minimal editing
- Honest about the gap — don't pretend no time has passed

Good:
> "Nico — it's been a while since we spoke about [X]. I've been thinking about our conversation re [specific thing they mentioned] — we've since [relevant development]. Worth a quick call to catch up?"

Bad:
> "Hi [NAME], hope you're well! I wanted to reach out and reconnect. Are you free for a quick call?"

The opening line is the most important output.
If it's generic, the skill has failed.

---

### 6. Update pipeline.md

```md
# Pipeline

## [NAME] — [Company]
Type: [prospect / partner / investor / former client / connector]
First contact: [date]
Last contact: [date]
Last source: [Gmail / LinkedIn / WhatsApp]
Stall reason: [inferred — they went quiet / you went quiet / timing / no next step]
Score: [X/15]
Times surfaced: [N]
Last surfaced: [date]
Status: [monitoring / surfaced / reached out / re-engaged / archived]
Notes: [anything relevant from the conversation history]
```

---

## Context updates

The skill improves the more context.md stays current.

When your situation changes — new project, new funding stage, new product — update context.md:
`/bizpulse context update "We just launched X and are looking for Y"`

The next weekly run will re-score all pipeline contacts against the new context.

---

## Management commands

- `/bizpulse now` — run immediately
- `/bizpulse score [name]` — see the score and reasoning for a specific contact
- `/bizpulse add [name] [context]` — manually add someone to track
- `/bizpulse archive [name]` — remove from active tracking
- `/bizpulse sent [name]` — mark as reached out (pauses for 30 days)
- `/bizpulse reengaged [name]` — mark as re-engaged (moves to active pipeline)
- `/bizpulse context update [text]` — update current commercial context
- `/bizpulse history [name]` — show full history for a contact
- `/bizpulse pipeline` — show full scored pipeline

---

## What makes it good

The opening line has to be specific. That's the whole product.
Anyone can surface a list of cold contacts.
The skill earns its place by writing the first sentence so you don't have to.

The scoring model distinguishes stalled from ended.
A clean goodbye is not a stall. A "let's talk in Q2" that never happened is.

The context.md update loop is the compounding mechanism.
A skill running against current priorities is 3x more useful than one running against stale ones.

The "who went quiet" signal matters.
If you went quiet on them, the re-opening message is different than if they went quiet on you.
The skill tracks this and the opening line reflects it.

---

## Privacy rules

SOUL.md applies. Commercial relationships only.
Never surface personal email threads in the business output.
If a thread is ambiguous (personal friend who is also a business contact), default to not surfacing unless context.md explicitly includes them.

Names in output are fine — these are professional relationships.
Do not include email addresses, phone numbers, or other contact details in the delivery.
User already has these. The skill provides context and a message, not a contact dump.
