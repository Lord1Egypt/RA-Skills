---
name: agentic-loop-designer
version: 1.0.0
price: 29
bundle: ai-setup-productivity-pack
bundle_price: 79
last_validated: 2026-03-07
---

# Agentic Loop Designer

**Framework: The Yes/No Loop Canvas**
*Worth $300/hr consultant time. Yours for $29.*

---

## What This Skill Does

Turns any repeatable task you're doing manually into an autonomous agent loop: trigger → agent → Slack ping → approve/skip. Includes 5 ready-to-deploy loop templates and a decision tree to design your own from scratch.

**Problem it solves:** Founders spend hours on task sequences that could run themselves. Email triage, weekly reports, standup summaries, lead qualification — if you do it the same way more than twice a week, it should be a loop.

---

## The Yes/No Loop Canvas

A structured framework for designing any agentic loop in under 10 minutes. Built around one insight: **every automatable task is just a series of yes/no decisions**.

### Canvas Structure

```
┌─────────────────────────────────────────────┐
│              YES/NO LOOP CANVAS             │
├─────────────────────────────────────────────┤
│  TRIGGER: What starts this loop?           │
│  ─────────────────────────────────────────  │
│  AGENT ACTION: What does the agent do?     │
│  ─────────────────────────────────────────  │
│  DECISION GATE: Approve / Skip / Escalate? │
│  ─────────────────────────────────────────  │
│  OUTPUT: What gets created or sent?        │
│  ─────────────────────────────────────────  │
│  MEMORY: What should persist for next run? │
└─────────────────────────────────────────────┘
```

---

### Step 1: Trigger Qualification

**What kicks off this loop?**

```
Is there a natural trigger?
├── Time-based (daily/weekly/on schedule)
│   └── → Use: cron trigger
├── Event-based (new email, new issue, form submit)
│   └── → Use: webhook trigger
├── Threshold-based (metric crosses a line)
│   └── → Use: polling trigger with condition
└── Manual ("run this now")
    └── → Use: manual trigger with /command
```

**Trigger scoring:**
| Trigger Type | Reliability | Setup Effort | Recommended For |
|-------------|-------------|--------------|-----------------|
| Cron | ★★★★★ | Low | Reports, summaries, digests |
| Webhook | ★★★★☆ | Medium | New data events |
| Polling | ★★★☆☆ | Medium | Metric-based |
| Manual | ★★★★★ | None | On-demand workflows |

---

### Step 2: Agent Action Design

**What should the agent actually do?**

The action block answers three questions:
1. **What data does the agent need?** (sources)
2. **What transformation happens?** (the work)
3. **What's the output format?** (how it lands)

**Action Template:**
```
SOURCES: [List tools/APIs the agent reads from]
TRANSFORM: [Plain English description of what agent does]
OUTPUT FORMAT: [Slack message / doc / file / API call]
```

**Example:**
```
SOURCES: Linear API (open issues), GitHub API (open PRs)
TRANSFORM: Group issues by assignee, flag items > 3 days old
OUTPUT FORMAT: Slack message with bullet list, @mention for flagged items
```

---

### Step 3: Decision Gate Design

**The most important part of any agentic loop.**

Every loop needs a clear approval model. Use this matrix:

| Risk Level | Data Sensitivity | Action Scope | Gate Type |
|------------|-----------------|--------------|-----------|
| Low | Non-sensitive | Read-only | Auto-run (no gate) |
| Low | Non-sensitive | Write/send | Slack preview → auto-send after 15 min |
| Medium | Semi-sensitive | Write/send | Slack approve button required |
| High | Sensitive | Any | Human review always |
| Any | Any | Irreversible | Human review always |

**Gate implementation:**
```
Slack message format for approval gates:
─────────────────────────────────
🤖 Loop: {Loop Name} | Run #{N}
{Agent output preview}

[✅ Approve] [⏭ Skip] [🛑 Stop Loop]
─────────────────────────────────
Timeout: {N} minutes → {default action}
```

---

### Step 4: Output Design

**Where does the work land?**

```
Output destination decision tree:
├── Team visibility needed?
│   ├── Yes → Slack channel message
│   └── No → DM or file
├── Needs to be acted on later?
│   ├── Yes → Notion page / Linear issue / GitHub issue
│   └── No → Slack message (ephemeral OK)
├── Needs structured data?
│   ├── Yes → Notion database row / JSON file
│   └── No → Prose summary
└── External delivery needed?
    ├── Yes → Email (via SMTP/SendGrid) / webhook
    └── No → Internal tool
```

---

### Step 5: Memory Design

**What should persist between runs?**

```
Memory checklist:
□ Last run timestamp (prevent duplicate work)
□ Previously processed item IDs (deduplication)
□ Cumulative state (running totals, streaks)
□ User preferences (learned from approvals/skips)
□ Error log (for debugging)
```

**Simple memory implementation (file-based):**
```json
{
  "loop_id": "weekly-standup",
  "last_run": "2026-03-07T09:00:00Z",
  "processed_ids": ["issue-123", "pr-456"],
  "run_count": 14,
  "skip_count": 2
}
```

---

## 5 Ready-to-Deploy Loop Templates

### Loop 1: Weekly Standup Digest

**Trigger:** Every Monday at 9am
**Sources:** Linear (open issues), GitHub (open PRs), Slack (#general last 7 days)
**Action:** Summarize each team member's open work + any blockers
**Gate:** Auto-send (low risk, read-only)
**Output:** Slack message in #standup

```
LOOP CONFIG:
─────────────────────────────────────
Name: Weekly Standup Digest
Trigger: cron("0 9 * * MON")
Agent prompt: |
  Read all open Linear issues assigned to each team member.
  Read all open GitHub PRs by author.
  For each person, write 2-3 bullet points: what they're working on,
  what's overdue (> 3 days), any blockers mentioned in Slack this week.
  Format as a Slack message with @mentions.
Gate: None (auto-send)
Output: POST to #standup
Memory: last_run timestamp
─────────────────────────────────────
```

**Setup time:** ~20 minutes | **Time saved:** 30-60 min/week

---

### Loop 2: New Lead Qualifier

**Trigger:** New form submission (webhook from Typeform/Tally)
**Sources:** Form response, company domain lookup (Clearbit/Apollo)
**Action:** Score lead on ICP criteria, draft personalized follow-up email
**Gate:** Slack approve → send email
**Output:** Draft email + lead score in Notion CRM

```
LOOP CONFIG:
─────────────────────────────────────
Name: New Lead Qualifier
Trigger: webhook (form submission)
Agent prompt: |
  Receive new lead form data.
  Look up company via domain (use Clearbit if available).
  Score on: company size (0-30), role seniority (0-30),
  use case fit (0-40).
  Draft personalized 3-sentence intro email.
  Post to Slack: lead summary + score + draft email.
Gate: Approve button → sends email | Skip → logs as not qualified
Output: Notion CRM row + email (if approved)
Memory: processed form IDs (dedup)
─────────────────────────────────────
```

**Setup time:** ~45 minutes | **Time saved:** 2-4 hrs/week

---

### Loop 3: GitHub PR Review Reminder

**Trigger:** Every weekday at 3pm
**Sources:** GitHub API (open PRs, age, reviewer assignments)
**Action:** Find PRs waiting > 24hr for review, draft reminder message
**Gate:** Auto-send if PR age > 48hr, Slack preview if 24-48hr
**Output:** Slack message @mentioning overdue reviewers

```
LOOP CONFIG:
─────────────────────────────────────
Name: PR Review Reminder
Trigger: cron("0 15 * * MON-FRI")
Agent prompt: |
  Fetch all open PRs across [repos].
  Find PRs with requested reviewers but no review in > 24 hours.
  Group by reviewer. For each reviewer, list their overdue PRs.
  Draft a friendly Slack message with PR links and ages.
Gate: If any PR > 48hr → auto-send. If 24-48hr → preview + 30min timeout
Output: #engineering Slack channel
Memory: last sent reminder per PR (avoid nagging)
─────────────────────────────────────
```

**Setup time:** ~15 minutes | **Time saved:** Ad-hoc interruptions → 0

---

### Loop 4: Weekly Revenue Snapshot

**Trigger:** Every Friday at 5pm
**Sources:** Stripe API, Notion metrics database, previous week's snapshot
**Action:** Calculate WoW change in MRR, churn, new customers
**Gate:** Auto-send (read-only financial data)
**Output:** Slack message in #founders with sparkline context

```
LOOP CONFIG:
─────────────────────────────────────
Name: Weekly Revenue Snapshot
Trigger: cron("0 17 * * FRI")
Agent prompt: |
  Pull current MRR from Stripe.
  Compare to snapshot from 7 days ago (stored in memory).
  Calculate: MRR change ($, %), new customers, churned customers.
  Write 3-sentence narrative: what changed, why (if obvious), what to watch.
  Format for Slack with clear numbers.
Gate: Auto-send
Output: #founders Slack channel + update Notion metrics DB
Memory: last week's MRR, customer count (for WoW delta)
─────────────────────────────────────
```

**Setup time:** ~30 minutes | **Time saved:** 1-2 hrs/week manual pulling

---

### Loop 5: Content Idea Capture & Queue

**Trigger:** Any message containing #idea in designated Slack channel
**Sources:** Slack message, existing content queue in Notion
**Action:** Extract idea, score for relevance, add to queue with metadata
**Gate:** Auto-add if score > 70, Slack preview if 50-70, discard if < 50
**Output:** Notion content database row

```
LOOP CONFIG:
─────────────────────────────────────
Name: Content Idea Capture
Trigger: Slack event (message in #ideas with #idea tag)
Agent prompt: |
  Extract the core idea from the Slack message.
  Score on: audience fit (0-30), differentiation (0-30), 
  timely/relevant (0-20), producibility (0-20).
  Write a one-line description and suggested format (post/thread/video).
  If score >= 70: auto-add to Notion queue.
  If 50-69: post preview to Slack with Add/Skip buttons.
  If < 50: silently discard.
Gate: Score-based (auto/preview/discard)
Output: Notion "Content Ideas" database
Memory: processed Slack message IDs
─────────────────────────────────────
```

**Setup time:** ~25 minutes | **Time saved:** Idea capture friction → 0

---

## Design Your Own Loop: 10-Minute Workshop

**Step 1: Identify the task (2 min)**
> What do you do manually that feels like groundhog day?
> Write it in one sentence: "Every [timeframe] I [action] using [sources] and [output]"

**Step 2: Fill the Canvas (5 min)**
```
TRIGGER: _______________
SOURCES: _______________
AGENT ACTION: _______________
GATE: Auto / Preview / Approve (circle one)
OUTPUT: _______________
MEMORY: _______________
```

**Step 3: Risk-check (2 min)**
- Can this loop send external messages? → Need approval gate
- Does it write or delete data? → Need approval gate
- Is it purely read + summarize? → Auto-run is fine

**Step 4: Name it and ship it (1 min)**
> Name your loop. Add it to your agent config. Run it once manually. Watch it work.

---

## Yes/No Loop Scoring Rubric

Before deploying any loop, score it:

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| Trigger is reliable | Manual only | Partially automated | Fully automated |
| Sources are available | Not connected | Partially connected | All connected via MCP |
| Gate is appropriate | No gate on risky action | Gate exists but clunky | Gate matches risk level |
| Output is useful | No one reads it | Sometimes useful | Consistently acted on |
| Memory prevents duplicates | No dedup | Partial | Full dedup |

**Score 8-10:** Deploy it. This loop is ready.
**Score 5-7:** Fix the weak spots (usually gate or sources) before deploying.
**Score 0-4:** Back to Canvas. Something fundamental is wrong.

---

## Example Session

**User prompt:**
> "I spend every Monday morning pulling GitHub PRs and posting a status to Slack. Help me automate this."

**Agent response using this skill:**
1. Fills Yes/No Loop Canvas with user's specific repos and Slack channel
2. Identifies trigger: Monday 9am cron
3. Confirms GitHub MCP is connected (or instructs setup via MCP Server Setup Kit)
4. Applies Loop Template 1 (Weekly Standup Digest), customized for their stack
5. Scores the loop using the rubric: should hit 8-10
6. Provides final config block ready to deploy

---

## Bundle Note

This skill is part of the **AI Setup & Productivity Pack** ($79 bundle):
- MCP Server Setup Kit ($19)
- Agentic Loop Designer ($29) — *you are here*
- AI OS Blueprint ($39)
- Context Budget Optimizer ($19)
- Non-Technical Agent Quickstart ($9)

Save $36 with the full bundle. Built by [@Remy_Claw](https://remyclaw.com).
