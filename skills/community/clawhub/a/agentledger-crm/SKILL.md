---
name: client-relationship-manager
version: "1.0.0"
url: https://github.com/theagentledger/agent-skills
description: Lightweight AI-native CRM for solopreneurs and freelancers. Track clients, relationships, follow-ups, deal stages, and interaction history in plain text files — no SaaS subscription required. Use when managing client relationships, preparing for meetings, tracking follow-ups, or reviewing pipeline status.
tags: [crm, clients, sales, freelance, solopreneur, relationships, pipeline]
platforms: [openclaw, cursor, windsurf, generic]
category: business
author: The Agent Ledger
license: CC-BY-NC-4.0
---

# Client Relationship Manager
### by [The Agent Ledger](https://theagentledger.com)

A lightweight, AI-native CRM for solopreneurs and freelancers. No SaaS subscription. No monthly seat fees. Just plain text files your agent can read, update, and reason over — with you keeping full control of your data.

---

## What This Skill Does

- Maintains structured client records in plain text
- Tracks deal stages, interaction history, and follow-up queues
- Prepares meeting briefs from client context
- Surfaces overdue follow-ups automatically
- Generates pipeline snapshots and revenue forecasts
- Stays out of the way when you don't need it

---

## Setup (5 Steps)

### Step 1: Create Your CRM Directory

```
crm/
├── clients/          # One file per client
├── pipeline.md       # Active deals and stages
├── follow-ups.md     # Pending follow-up queue
└── README.md         # Index of all clients
```

Ask your agent to create this structure:

> "Set up a CRM directory at `crm/` with subdirectories for clients, and files for pipeline.md and follow-ups.md."

---

### Step 2: Add Your First Client Record

Each client lives in `crm/clients/[client-slug].md`. Use this template:

```markdown
# [Client Name]
**Company:** [Company or "Individual"]
**Contact:** [Primary contact name]
**Email:** [email]
**Phone:** [phone — optional]
**Timezone:** [their timezone]
**Introduced:** [YYYY-MM-DD]
**Source:** [How you met — referral, cold outreach, inbound, etc.]
**Tags:** [industry, service-type, etc.]

## Status
**Stage:** [Lead / Prospect / Active / Paused / Closed-Won / Closed-Lost]
**Value:** [$X/project | $X/month | TBD]
**Next Action:** [What needs to happen next]
**Next Action Due:** [YYYY-MM-DD]

## Background
[2-3 sentences on who they are, what they do, what problem they're trying to solve]

## Our Work Together
[What service/product you're providing or discussing]

## Interaction Log
### YYYY-MM-DD — [Medium: email/call/meeting/message]
[Brief summary of what was discussed, decided, or agreed]

### YYYY-MM-DD — [Medium]
[...]
```

---

### Step 3: Set Up Your Pipeline

`crm/pipeline.md` tracks all active deals in one view:

```markdown
# Pipeline
_Last updated: YYYY-MM-DD_

## Active Deals

| Client | Stage | Value | Next Action | Due |
|--------|-------|-------|-------------|-----|
| [Name] | Proposal Sent | $X | Follow up if no response | YYYY-MM-DD |
| [Name] | Negotiating | $X | Send revised scope | YYYY-MM-DD |
| [Name] | Active | $X/mo | Monthly check-in | YYYY-MM-DD |

## Pipeline Summary
- **Total pipeline value:** $X
- **Weighted forecast (50% close rate):** $X
- **Active client MRR:** $X

## Recently Closed
| Client | Outcome | Value | Date |
|--------|---------|-------|------|
| [Name] | Won | $X | YYYY-MM-DD |
| [Name] | Lost | — | YYYY-MM-DD |
```

---

### Step 4: Set Up Your Follow-Up Queue

`crm/follow-ups.md` is your daily action list:

```markdown
# Follow-Up Queue
_Last updated: YYYY-MM-DD_

## Overdue
- [ ] **[Client Name]** — [What to do] _(was due YYYY-MM-DD)_

## Due Today
- [ ] **[Client Name]** — [What to do]

## Due This Week
- [ ] **[Client Name]** — [What to do] _(YYYY-MM-DD)_

## Due Next Week
- [ ] **[Client Name]** — [What to do] _(YYYY-MM-DD)_

## Someday / No Date
- [ ] **[Client Name]** — [Reconnect when budget opens]
```

---

### Step 5: Give Your Agent the Standing Instructions

Add to your `AGENTS.md` or system prompt:

```
## CRM Protocol

When I mention a client or prospect:
1. Check if they have a record in crm/clients/ — if not, offer to create one
2. After any meeting or call I describe, offer to log an interaction entry
3. If I ask for a "CRM review" or "pipeline check," read crm/pipeline.md and crm/follow-ups.md and report: overdue items, upcoming actions, pipeline value, and any clients I haven't touched in 30+ days
4. If I say "prep me for [client]," read their client file and give me: background, last interaction, current stage, and what I should know before talking to them

Never auto-update files without confirming the entry first.
```

---

## Usage Patterns

### Meeting Prep
> "Prep me for my call with Acme Corp at 2pm."

Your agent reads `crm/clients/acme-corp.md` and gives you:
- Who you're talking to and their background
- Current deal stage and value
- Last interaction summary
- What was agreed or outstanding
- Suggested talking points based on next action

### Log an Interaction
> "Just got off a call with Sarah at Designworks. She liked the proposal but wants a 10% discount. Follow up Friday."

Your agent drafts the interaction log entry and updates the next action + due date. You confirm before it writes.

### CRM Review
> "Give me a CRM review."

Your agent reads pipeline.md and follow-ups.md and reports:
- Overdue follow-ups
- Actions due today and this week
- Pipeline summary (total value, count by stage)
- Clients not touched in 30+ days (potential churn risk)
- Any deals with stale "next action" dates (no movement in 14+ days)

### Add a New Lead
> "Add Jane from TechStartup as a lead. Met her at a conference. She's interested in monthly consulting. Her email is jane@techstartup.io."

Your agent creates `crm/clients/techstartup-jane.md` using the template, fills in what you've told it, and flags the fields that need more information.

### Weekly Pipeline Update
> "Update the pipeline."

Your agent reads all client files, cross-references with pipeline.md, and proposes updates for any stages that appear stale or inconsistent with recent interaction logs.

---

## Deal Stages (Customize These)

| Stage | Definition |
|-------|------------|
| **Lead** | Identified as a potential client, no real conversation yet |
| **Prospect** | Had initial conversation, they know what you offer |
| **Qualified** | Confirmed budget, timeline, and decision-maker involvement |
| **Proposal Sent** | Formal proposal or scope submitted, awaiting response |
| **Negotiating** | Active discussion on terms, scope, or price |
| **Active** | Paying client, work in progress |
| **Paused** | Project on hold — agreed to revisit later |
| **Closed-Won** | Project complete or ongoing retainer secured |
| **Closed-Lost** | Didn't move forward — log the reason |

Adapt these to your sales process. The stage names in client files and pipeline.md should match.

---

## Automated Follow-Up Review (Optional)

Add a periodic check to your HEARTBEAT.md:

```
## CRM
- Read crm/follow-ups.md and flag any overdue items
- Check for clients in crm/clients/ with no interaction in 30+ days
- If pipeline hasn't been updated in 7 days, flag for review
```

Or set a weekly cron:

```bash
openclaw cron add \
  --name "weekly-crm-review" \
  --cron "0 9 * * MON" \
  --model "anthropic/claude-3-5-haiku-20241022" \
  --session isolated \
  --message "Read crm/pipeline.md and crm/follow-ups.md. Report: overdue follow-ups, pipeline value by stage, clients not touched in 30+ days, and deals with no movement in 14+ days. Be concise." \
  --announce \
  --to "[YOUR_TELEGRAM_CHAT_ID]" \
  --tz "America/Chicago"
```

---

## Customization Options

### Industry-Specific Stage Names
Replace the default stages with language that fits your context:
- **Freelancers:** Inquiry → Brief → Quoted → In Progress → Review → Invoiced → Paid
- **Coaches:** Discovery → Enrolled → Active → Alumni
- **Agencies:** RFP → Scoping → Proposal → Negotiation → Onboarding → Retained

### Client Tiers
Add a tier field to segment by relationship priority:
```
**Tier:** A (Top client / referral source) | B (Active, standard) | C (Occasional) | D (Dormant)
```

### Revenue Tracking
Extend pipeline.md with a monthly revenue section:
```markdown
## Revenue (Current Month)
- Invoiced: $X
- Collected: $X
- Outstanding: $X
- Projected (next 30 days): $X
```

### Referral Tracking
Add a referrals section to client files:
```markdown
## Referrals Sent
- Referred [Name] to [Client] on [date] — [outcome if known]

## Referrals Received From This Client
- [Name/Company] — [date] — [outcome]
```

---

## Integration With Other Agent Ledger Skills

| Skill | How They Work Together |
|-------|----------------------|
| **solopreneur-assistant** | Include pipeline summary in your weekly business dashboard |
| **inbox-triage** | Flag emails from pipeline clients as higher urgency |
| **project-tracker** | Link active clients to their project files for unified status |
| **decision-log** | Log major client decisions (pricing changes, scope decisions) |
| **content-calendar** | Track case study opportunities from Closed-Won clients |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent doesn't know about a client | Check that client file is in `crm/clients/` and agent has access to the directory |
| Pipeline gets stale | Add CRM review to your HEARTBEAT.md or set a weekly cron |
| Too many files to manage | Use README.md in `crm/` as a client index with quick status for each |
| Agent writes to files without confirming | Reinforce "never auto-update without confirming" in your AGENTS.md |
| Deal stages are confusing | Pick 4-5 stages max and define them clearly in your AGENTS.md |

---

## Privacy Note

All CRM data lives locally in your workspace. Nothing is synced, shared, or processed externally unless you explicitly ask your agent to send something. Your client data stays yours.

If you're subject to client confidentiality obligations (legal, financial, healthcare), keep this in a local-only workspace and avoid syncing to cloud-backed directories without reviewing your obligations.

---

## About This Skill

Built by [The Agent Ledger](https://theagentledger.com) — practical guides and tools for AI-augmented solopreneurs.

Subscribe for new skills, guides, and subscriber-only content at **theagentledger.com**.

**License:** [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/) — free for personal use, not for resale or redistribution.

---

_Disclaimer: This skill provides a framework for organizing information. It does not replace professional CRM software for enterprise use cases, and the author makes no warranty as to fitness for any particular purpose. Use responsibly and in compliance with any applicable data protection laws and professional obligations._
