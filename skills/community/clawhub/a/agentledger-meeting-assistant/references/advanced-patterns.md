# Meeting Assistant — Advanced Patterns
**by [The Agent Ledger](https://theagentledger.com)**

*Advanced workflows for high-volume meeting environments and complex coordination.*

---

## Pattern 1: Pre-Meeting Intelligence Chain

Chain research-assistant → meeting-assistant for data-backed briefs before important calls.

**Trigger:** "Full intel brief for meeting with [Company/Person]"

**Chain:**
1. Research assistant pulls: company background, recent news, LinkedIn signals, competitor context
2. Meeting assistant formats: structured brief with research findings embedded
3. Output includes "Research Confidence" rating (High/Medium/Low based on source quality)

**AGENTS.md instruction:**
```markdown
## Pre-Meeting Intel Chain
When I request a "full intel brief" for an external meeting:
1. Use research-assistant to pull public information about the company/person
2. Summarize research findings in 3-5 bullet points
3. Feed findings into the meeting brief under "Context" and "Watch For" sections
4. Note research confidence level (High = multiple verified sources, Medium = limited sources, Low = minimal public info)
```

**Use case:** High-stakes sales calls, investor meetings, partnership conversations, first-time client meetings.

---

## Pattern 2: Async Meeting Capture

For asynchronous work (Loom recordings, voice memos, Slack threads), capture meeting-style notes from unstructured sources.

**Trigger:** "Async notes: [paste transcript or summary of async exchange]"

**What it does:**
- Formats async decisions as meeting records (dated, with attendees)
- Extracts commitments even from informal Slack/email exchanges
- Files to `meetings/async/YYYY-MM-DD-[topic].md` to keep separate from synchronous meetings

**AGENTS.md instruction:**
```markdown
## Async Meeting Capture
Async decisions (Slack threads, email exchanges, voice memos) can be captured as meeting records.
File async records in meetings/async/ folder.
Apply same action item extraction and open-actions.md update rules.
Mark these with [ASYNC] in the meeting log type column.
```

**Use case:** Remote teams, distributed decisions, decision audit trails for async-first workflows.

---

## Pattern 3: Deal Meeting Timeline

For sales or partnership deals with multiple meetings, maintain a deal timeline that spans all meetings.

**File:** `meetings/deals/[deal-name]-timeline.md`

**Format:**
```markdown
# Deal Timeline — [Company Name]
**Deal Stage:** [stage]
**Total Meetings:** [N]
**Deal Owner:** [you]
**Est. Close:** [date]

## Meeting History

### [Date] — [Meeting #1 Name]
**Outcome:** [brief description]
**Key Decisions:** [list]
**Next Step Agreed:** [what was promised]
**Status at Exit:** [stage after this meeting]

### [Date] — [Meeting #2 Name]
...

## Cumulative Open Items
| Action | Owner | Due | Status |
|--------|-------|-----|--------|

## Deal Signals Log
- [Date]: [Positive/Negative signal observed]
- [Date]: [Signal]
```

**AGENTS.md instruction:**
```markdown
## Deal Timeline Tracking
For active sales deals, maintain a deal timeline file in meetings/deals/.
After each meeting with a prospect, update their deal timeline with outcome, decisions, and next steps.
Cross-reference with CRM if client-relationship-manager skill is active.
```

---

## Pattern 4: Meeting Productivity Metrics

Track your meeting habits to identify waste and optimize your schedule.

**File:** `meetings/meeting-metrics.md`

**Format:**
```markdown
# Meeting Metrics
Last updated: YYYY-MM-DD

## Month: [Month YYYY]

| Week | Meetings | Total Hours | Action Items Created | Closed | Carry-Over |
|------|----------|-------------|---------------------|--------|------------|
| Wk 1 | [N] | [H] | [N] | [N] | [N] |

### Meeting Mix (this month)
- Client: [N] meetings, [H] hours
- Sales/Discovery: [N] meetings, [H] hours  
- Internal: [N] meetings, [H] hours
- Strategic: [N] meetings, [H] hours

### Time Spent
- Prep: ~[H] hours
- In meetings: [H] hours
- Follow-up: ~[H] hours
- **Total meeting overhead:** [H] hours ([%] of work week)

### Action Item Health
- Created: [N]
- Closed on time: [N] ([%])
- Overdue: [N]
- Closed late: [N]

### Notes
[Any patterns, time sinks, or optimization observations]
```

**Heartbeat trigger:**
```markdown
## Meeting Metrics Heartbeat
Every Friday, update meetings/meeting-metrics.md:
- Count meetings this week (scan meetings/YYYY-MM/ for this week's files)
- Tally hours (use duration from meeting files)
- Count action items created and closed
- Note any metric worth flagging
```

---

## Pattern 5: Board / Investor Meeting Pack

For high-stakes periodic meetings (board calls, investor updates), generate a structured pack that integrates multiple data sources.

**Trigger:** "Prep investor update pack for [date]"

**Pack structure:**
```markdown
# Investor Update — [Month YYYY]
*Prepared [date] | Duration: [planned] | Attendees: [list]*

## 1. Business Highlights (Since Last Update)
- [Win 1]
- [Win 2]

## 2. Key Metrics
| Metric | Last Period | This Period | Target | Status |
|--------|------------|-------------|--------|--------|
| Revenue | | | | |
| [KPI] | | | | |

## 3. Progress on Last Meeting's Action Items
| Action | Committed By | Status | Notes |
|--------|-------------|--------|-------|

## 4. Strategic Discussion Items
- [Topic 1]: [Context for discussion]
- [Topic 2]: [Context for discussion]

## 5. Asks / Needs from This Group
- [Specific ask 1]
- [Specific ask 2]

## 6. Outlook / Next Period
- [What's coming]
- [Key risks]

---
*Attachments: [list any supporting docs]*
```

**Chain:** solopreneur-assistant (business snapshot) → financial-tracker (revenue metrics) → goal-tracker (KPI progress) → meeting-assistant (format into pack)

---

## Pattern 6: Automated Follow-Up Draft

After capturing meeting notes, automatically draft follow-up emails for each action owner.

**Trigger:** "Draft follow-up emails for [meeting name]"

**Output:** One draft per external action owner:

```markdown
## Follow-Up Draft — [Action Owner Name]
**To:** [Name]
**Subject:** Follow-up: [Meeting Name] — [Date]

Hi [Name],

Thanks for the call today. Quick summary of what we aligned on:

**Decisions made:**
- [Decision 1]

**Your action items:**
- [ ] [Action] by [date]
- [ ] [Action] by [date]

**My commitments:**
- [ ] [Your action] by [date]

Our next touchpoint: [next meeting date or "TBD — I'll reach out by [date]"]

Let me know if I missed anything.

[Your name]

---
⚠️ DRAFT — Review before sending. Do not auto-send.
```

**AGENTS.md instruction:**
```markdown
## Follow-Up Draft Rule
When I say "draft follow-up for [meeting]", create one email draft per external action owner.
Always include: decisions made, their action items, my action items, next touchpoint.
Always mark drafts with "⚠️ DRAFT — Review before sending." Never send automatically.
Save drafts to meetings/YYYY-MM/YYYY-MM-DD-[meeting]-followups.md
```

---

## Pattern 7: Recurring Meeting Agenda Builder

For weekly recurring meetings, auto-build the agenda from open action items and project status.

**Trigger:** "Build agenda for [recurring meeting name]"

**What it does:**
1. Pulls open action items due before next meeting
2. Pulls any flagged project status updates (if project-tracker active)
3. Builds a time-boxed agenda

**Output:**
```markdown
## Agenda — [Recurring Meeting Name]
**Date:** [next occurrence]
**Duration:** [standard duration]

### Standing Items (10 min)
- Wins since last meeting
- Blockers needing discussion

### Action Item Review (10 min)
Open items due today or overdue:
- [ ] [Item] — Owner: [name] — Due: [date]
- [ ] [Item] — Owner: [name] — Due: [date]

### Discussion Items (30 min)
1. [Topic from project or goal updates] — [5-10 min]
2. [Topic] — [10 min]

### New Business (10 min)
- [Any new topic raised before meeting]

### Action Items Review (5 min)
- Confirm owners and deadlines for anything decided today

**Notes taker:** [name or TBD]
```

---

## Pattern 8: Client Onboarding Meeting Series

For new clients, generate a structured meeting sequence for the onboarding phase.

**Trigger:** "Create onboarding meeting plan for [client name]"

**Output:** A 4-meeting onboarding sequence with brief templates for each:

```markdown
# Onboarding Meeting Plan — [Client Name]

## Meeting 1: Kickoff (Week 1)
**Goal:** Establish relationship, align on scope and success metrics
**Duration:** 60 min
**Agenda:**
- Introductions + context (10 min)
- Project scope walkthrough (20 min)
- Success metrics definition (15 min)
- Communication preferences + meeting cadence (10 min)
- Next steps (5 min)

## Meeting 2: Discovery Deep-Dive (Week 2)
**Goal:** Understand their current state in detail
**Duration:** 60 min
**Agenda:**
- Current process walkthrough (30 min)
- Pain points and priorities (20 min)
- Data/access needs (10 min)

## Meeting 3: Solution Walkthrough (Week 3)
**Goal:** Present approach, get alignment before execution
**Duration:** 45 min
**Agenda:**
- Proposed approach (20 min)
- Q&A and refinement (15 min)
- Confirm scope, timeline, deliverables (10 min)

## Meeting 4: First Check-in (Week 4)
**Goal:** Early pulse check before deep into execution
**Duration:** 30 min
**Agenda:**
- Progress update (10 min)
- Early questions/concerns (10 min)
- Next 30 days preview (10 min)

---
*Auto-generate brief for each meeting using meeting-assistant when date approaches.*
```

---

## Pattern 9: Heartbeat Integration — Stale Action Alert

Flag overdue meeting commitments during regular heartbeat checks.

**HEARTBEAT.md addition:**
```markdown
## Meeting Action Check
Every Monday morning, scan meetings/open-actions.md:
- List any action items that are overdue (past due date)
- List any items due this week
- If any MY actions are overdue, flag with 🔴 in daily briefing
- If any OTHERS' actions are overdue (I'm waiting on them), list separately for follow-up
```

**Alert format:**
```
🔴 Overdue Meeting Actions
- [My action] — was due [date] | from: [meeting]
⏳ Others' Overdue (awaiting):
- [Their action] — [name] was due [date] | from: [meeting]
```

---

## Pattern 10: Meeting-to-Newsletter Pipeline

Turn high-value meeting learnings into newsletter content.

**Trigger:** "What from my recent meetings could become newsletter content?"

**What it does:**
1. Scans recent meeting files (last 30 days)
2. Identifies: interesting decisions made, problems solved, patterns noticed, counterintuitive learnings
3. Generates content hooks for each

**Output:**
```markdown
## Newsletter Content Mining — Recent Meetings

### Potential Content Angles

**1. [Topic from meeting]**
Hook: "[Draft headline or hook]"
From: [meeting name, date]
Why it's interesting: [1-2 sentences]
Format suggestion: [essay / listicle / case study / framework]

**2. [Topic]**
Hook: "[Draft headline]"
...

---
*Link to content-calendar skill to schedule the best candidates.*
```

---

*Meeting Assistant — Advanced Patterns | by [The Agent Ledger](https://theagentledger.com)*

*Subscribe at [theagentledger.com](https://theagentledger.com) | License: [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)*
