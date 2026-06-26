---
name: meeting-assistant
version: "1.0.0"
url: https://github.com/theagentledger/agent-skills
description: AI meeting partner for solopreneurs and professionals. Generates pre-meeting briefs from your notes and context, captures structured meeting notes during the conversation, and produces action item summaries with owners and deadlines. Integrates with project-tracker, inbox-triage, client-relationship-manager, and solopreneur-assistant skills.
tags: [meetings, notes, action-items, productivity, solopreneur, crm, project-management]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
---

# Meeting Assistant
**by [The Agent Ledger](https://theagentledger.com)**

*Never forget what was decided. Never miss a follow-up. Never walk into a meeting unprepared.*

---

## What This Skill Does

This skill turns your agent into a meeting lifecycle partner that:

- **Prepares** you before meetings with a structured brief (context, goals, talking points, open questions)
- **Captures** meeting notes in a clean, scannable format during or immediately after calls
- **Extracts** action items with owners, deadlines, and priority levels
- **Files** meeting records so past decisions are searchable and linkable
- **Follows up** by surfacing stale action items and flagging overdue commitments

Works for any meeting type: client calls, team standups, investor conversations, vendor negotiations, one-on-ones, discovery calls, and strategy sessions.

---

## Setup (4 Steps)

### Step 1: Add to AGENTS.md

Paste into your `AGENTS.md` standing instructions:

```markdown
## Meeting Assistant (Agent Ledger Skill)

You have a meeting management system. For all meeting-related requests:

**Pre-meeting:** When I say "prep for [meeting name]" or "meeting brief", generate a structured brief.
**During/after:** When I say "meeting notes" or "capture notes", create a structured meeting record.
**Action items:** When I say "action items" or "follow-ups", extract and list all commitments.
**Review:** When I say "meeting review" or "open actions", surface unresolved items from recent meetings.

State file: meetings/meeting-log.md (create if missing)
Active actions file: meetings/open-actions.md (create if missing)
Meeting archive: meetings/YYYY-MM/ (organize by month)

Capture format: Brief → Notes → Actions → Filed. Never skip the action item step.
```

### Step 2: Create the Meetings Folder

```bash
mkdir -p meetings/open-actions
```

Your agent will create individual meeting files automatically. The folder structure:

```
meetings/
  meeting-log.md          ← index of all meetings (title, date, type, key decision)
  open-actions.md         ← running list of unresolved action items across all meetings
  YYYY-MM/
    YYYY-MM-DD-meeting-name.md   ← individual meeting records
```

### Step 3: Initialize Your State Files

Ask your agent:

> "Initialize my meeting assistant. Create meetings/meeting-log.md and meetings/open-actions.md with the standard format."

It will create:

**meetings/meeting-log.md:**
```markdown
# Meeting Log

| Date | Meeting | Type | Key Decision | File |
|------|---------|------|--------------|------|
| (populated automatically) |
```

**meetings/open-actions.md:**
```markdown
# Open Action Items

Last reviewed: YYYY-MM-DD

| # | Action | Owner | Due | Meeting | Status |
|---|--------|-------|-----|---------|--------|
| (populated automatically) |
```

### Step 4: Run Your First Brief

Try: *"Prep brief for a 30-minute sales discovery call with [Company Name]. They're interested in [product/service]. I've spoken to them once before."*

---

## Usage Patterns

### Pre-Meeting Brief

**Trigger:** "Prep brief for [meeting]" or "meeting brief: [details]"

**What to include:** meeting name, attendees, duration, purpose, any prior context

**Example:**
> "Prep brief for weekly client check-in with Acme Corp. 30 min. Status update on their Q1 project. Last call we agreed on revised timeline."

**Output format:**
```markdown
## Meeting Brief — Acme Corp Weekly Check-in
**Date/Time:** [to confirm]
**Duration:** 30 min
**Attendees:** [you] + Acme Corp contact(s)
**Meeting Type:** Client check-in

### Context
[Summary of relationship, project background, last touchpoint]

### Goals for This Meeting
1. [Primary goal]
2. [Secondary goal]

### Talking Points
- [Key update to share]
- [Decision that needs resolution]
- [Question to ask]

### Open Items from Last Meeting
- [ ] [Unresolved action from prior call]

### Questions to Ask
- [Question 1]
- [Question 2]

### Watch For
- [Potential concern or signal to notice]
```

---

### Capture Meeting Notes

**Trigger:** "Meeting notes: [paste or dictate what happened]" or "Capture this meeting: [details]"

**Example:**
> "Meeting notes: Acme call, 45 min. Sarah and Tom attended. They approved the revised scope. Tom raised concern about the March deadline — wants a buffer week. We agreed to move delivery to March 14. Sarah will send updated contract by EOD Friday. I'll send revised project plan by Wednesday."

**Output format:**
```markdown
## Meeting Notes — Acme Corp Weekly Check-in
**Date:** YYYY-MM-DD
**Duration:** 45 min
**Attendees:** [You], Sarah (Acme), Tom (Acme)
**Meeting Type:** Client check-in

### Summary
[2-3 sentence recap of what happened and what was decided]

### Key Decisions
- [Decision 1]
- [Decision 2]

### Discussion Notes
- [Topic 1]: [What was said]
- [Topic 2]: [What was said]

### Action Items
| # | Action | Owner | Due | Priority |
|---|--------|-------|-----|----------|
| 1 | Send updated contract | Sarah (Acme) | EOD Fri | High |
| 2 | Send revised project plan | You | Wed | High |

### Open Questions
- [Unresolved question from meeting]

### Next Meeting
[Date/topic if scheduled, or "TBD"]
```

---

### Extract Action Items Only

**Trigger:** "Pull action items from [meeting notes or description]"

**Use when:** You have raw notes and just need the action list extracted and formatted.

**Output format:**
```markdown
## Action Items — [Meeting Name] (YYYY-MM-DD)

**Your actions:**
- [ ] [Action] — due [date]
- [ ] [Action] — due [date]

**Others' actions (to follow up on):**
- [ ] [Name]: [Action] — due [date]

**Added to open-actions.md:** ✅
```

---

### Weekly Action Review

**Trigger:** "Meeting review" or "open actions" or "what's overdue?"

**What it does:** Scans `meetings/open-actions.md`, flags overdue items, and surfaces commitments due this week.

**Output format:**
```markdown
## Open Actions Review — Week of YYYY-MM-DD

### 🔴 Overdue
- [ ] [Action] | Owner: [name] | Was due: [date] | From: [meeting]

### 🟡 Due This Week
- [ ] [Action] | Owner: [name] | Due: [date] | From: [meeting]

### ✅ Completed Since Last Review
- [x] [Action] | Closed: [date]

### 📋 On Deck (Next 2 Weeks)
- [ ] [Action] | Owner: [name] | Due: [date]

---
Total open: [N] | Overdue: [N] | Due this week: [N]
```

---

### Close Action Item

**Trigger:** "Close action [#] from [meeting]" or "mark done: [description]"

**What it does:** Marks the item complete in `open-actions.md` with a closed date, and updates the source meeting file.

---

### Meeting Type: Discovery Call

**Trigger:** "Discovery brief for [prospect]" or "prep discovery call with [name/company]"

**Extra output sections:**
```markdown
### Discovery Objectives
- Understand their current situation
- Identify the core problem they're trying to solve
- Qualify: budget, timeline, decision-maker
- Assess fit

### BANT Quick-Capture
- **Budget:** [to learn]
- **Authority:** [who decides?]
- **Need:** [what problem are they solving?]
- **Timeline:** [when do they need this?]

### Qualification Signal
- Green flags: [what would make this a strong fit]
- Red flags: [what would disqualify them]
```

---

### Meeting Type: One-on-One

**Trigger:** "1:1 notes with [name]" or "prep my 1:1 with [name]"

**Extra output sections:**
```markdown
### Running Agenda (from last sessions)
- [Carry-forward item]

### This Week's Check-in Points
- Wins since last 1:1
- Blockers / needs support on
- Feedback to give / receive
- Goals progress

### Relationship Notes
- [Anything to remember about this person or dynamic]
```

---

## Meeting Types Reference

| Type | Prep Depth | Notes Detail | Action Focus |
|------|------------|--------------|--------------|
| Discovery/Sales | Deep | Medium | Qualify → Next step |
| Client check-in | Medium | Full | Commitments + deadlines |
| Strategy session | Deep | Full | Decisions + owners |
| Team standup | Light | Brief | Blockers only |
| Vendor/Partner | Medium | Full | Contract + deliverables |
| 1:1 | Medium | Full | Growth + accountability |
| Board/Investor | Deep | Full | Decisions + KPIs |

---

## File Naming Convention

Meeting files are named: `YYYY-MM-DD-[meeting-slug].md`

Examples:
- `2026-03-07-acme-weekly.md`
- `2026-03-10-discovery-rivercity.md`
- `2026-03-12-team-standup.md`

The agent handles naming automatically when you say "file this meeting."

---

## Integration with Other Agent Ledger Skills

| Skill | How They Connect |
|-------|-----------------|
| **client-relationship-manager** | Auto-update CRM after client meetings; pull client history into pre-meeting brief |
| **project-tracker** | Link meeting action items to project milestones; flag project-blocking decisions |
| **inbox-triage** | Meeting invites get triaged with context; follow-up emails drafted from action items |
| **solopreneur-assistant** | Meeting frequency and commitments feed into weekly priority review |
| **goal-tracker** | Strategic meetings update goal progress; decisions logged against relevant goals |
| **decision-log** | Significant meeting decisions auto-captured to decision log for future reference |

### Combined Workflow Example (CRM + Meeting)

> "Prep brief for discovery call with Riverside Design. Check their CRM record first."

Agent will:
1. Pull Riverside Design record from `crm/crm-records.md`
2. Check interaction log for prior touchpoints
3. Generate meeting brief incorporating relationship history
4. After meeting: update CRM interaction log + advance deal stage if qualified

---

## Customization

### Adjust Brief Depth

In `AGENTS.md`, add your preference:

```markdown
## Meeting Brief Depth
- Discovery/Sales calls: Full brief (context, goals, BANT, qualification signals)
- Client check-ins: Standard brief (context, goals, open items)
- Internal calls: Light brief (agenda + open actions only)
- Ad-hoc calls: Minimal (goals + open questions only)
```

### Auto-Archive After N Days

```markdown
## Meeting Archive Rule
After 30 days, meeting files in meetings/ can be moved to meetings/archive/YYYY-MM/
Keep open-actions.md current regardless of file age.
```

### Default Meeting Timezone

```markdown
## Meeting Timezone
Default timezone for all meetings: [Your timezone]
Always include timezone when noting scheduled follow-ups.
```

### Recurring Meeting Templates

For meetings you have weekly, set up recurring context:

```markdown
## Recurring Meetings
- Weekly client call (Mondays, [Client Name]): standard check-in, always 30 min
- Friday retrospective (Fridays, internal): wins/blockers/next week priorities
```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Brief is too generic | Not enough context provided | Include: attendee names, meeting history, current project status |
| Action items missed | Notes too informal | Say "pull action items" separately after capturing notes |
| Open-actions.md getting cluttered | Items not being closed | Run "meeting review" weekly; close completed items explicitly |
| Agent loses CRM context | Not linking skills | In AGENTS.md, explicitly mention "check CRM before client meeting briefs" |
| Wrong meeting type format | Default brief used | Specify meeting type: "discovery brief" or "1:1 prep" |

---

## Privacy Note

All meeting notes and action items are stored **locally in your workspace**. Nothing is shared or transmitted externally. Meeting records may contain sensitive business information — treat the `meetings/` folder accordingly.

The agent will **never** automatically send meeting notes or action items to anyone. All outbound communication (follow-up emails, Slack messages) requires your explicit instruction.

---

*Meeting Assistant is a free skill by [The Agent Ledger](https://theagentledger.com) — a newsletter about building AI systems that actually work.*

*Subscribe at [theagentledger.com](https://theagentledger.com) for more skills, blueprints, and the premium implementation guide.*

*License: [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)*

> *DISCLAIMER: This skill was created by an AI agent. It is provided "as is" for informational and educational purposes only. It does not constitute professional, financial, legal, or technical advice. Review all generated files before use. The Agent Ledger assumes no liability for outcomes resulting from use. Use at your own risk.*
