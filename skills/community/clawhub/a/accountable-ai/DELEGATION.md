# Delegation — Cross-Agent Task Protocol

When one agent needs to delegate work to another, this protocol ensures clear communication, accountability, and verification. This document is platform-agnostic and works with Discord, Slack, Teams, email, or any communication system.

## Core Principles

1. **Clarity** — The delegated task is clearly specified before work starts
2. **Accountability** — Delegator and agent both understand success criteria
3. **Audit Trail** — All delegations are logged for transparency
4. **Verification** — Work is verified before considered complete
5. **Closure** — Delegations are formally closed with lessons documented
6. **Independence** — The receiving agent can execute without constant escalation

## Delegation Lifecycle

Every delegation follows this four-stage lifecycle:

### Stage 1: Request

**Duration:** 5-10 minutes
**Participants:** Delegator, delegated agent
**Channel:** Communication platform (Discord, Slack, Teams, email)

The delegator initiates the delegation with a clear request:

**Request message includes:**
- Task title/name
- Detailed description of what needs to be done
- Why this task matters (context)
- Who the delegated agent is (addressed directly)
- Verification criteria (how we'll know it's done right)
- Estimated time/effort (optional)
- Dependencies or prerequisites
- Deadline (if time-sensitive)
- Resources needed (links, access, information)

**Example:**
```
@analyst-agent Delegation: Analyze Q1 quarterly review data

Description: Compile Q1 performance metrics from the past 3 months
(Jan-Mar) and identify top 3 trends and 3 areas for improvement.

Context: Leadership needs this for April strategy meeting.

Verification criteria:
- Document format: Markdown
- Must include specific metrics with sources
- Trends and improvements must be data-backed, not opinions
- Completion time: 2 hours

Resources:
- Q1 data file: ~/workspace/data/q1-metrics.csv
- Template: ~/templates/analysis-format.md
- Slack channel for questions: #quarterly-reviews

Deadline: Tomorrow 5 PM

Do you have availability for this?
```

**Delegated agent responds:**
- Confirms receipt and understanding
- Asks clarifying questions if needed
- Provides availability and estimated completion time
- Confirms they have required access/resources
- Updates daily memory with delegation details

---

### Stage 2: Execute

**Duration:** Varies (based on task complexity)
**Participants:** Delegated agent
**Channel:** Agent's workspace

The delegated agent completes the work:

**During execution:**
- Work in designated workspace (not shared publicly)
- Update daily memory with progress (timestamps, challenges)
- Document any blockers or assumptions made
- Reach out to delegator if clarifications needed
- Avoid scope creep (do what was requested, not extras)
- Complete work before deadline

**If blocked:**
- Agent tries to resolve independently first
- If unresolvable, escalate to delegator with context
- Document blocker in daily memory
- Wait for clarification before proceeding

**Example progress update (in daily memory):**
```
## Q1 Analysis Delegation

Started: 2026-03-28 10:00 AM
Status: In progress

Progress:
- Imported Q1 metrics CSV successfully
- Analyzed top 5 trends (3 identified so far)
- Found interesting anomaly in March performance

Blockers:
- One data point missing for Feb (reached out to delegator)

Next steps:
- Await response on missing data
- Finalize improvement recommendations
```

---

### Stage 3: Verify

**Duration:** 10-20 minutes
**Participants:** Delegator, delegated agent
**Channel:** Communication platform

The delegator reviews completed work:

**Verification checklist:**
- [ ] Work matches the original request
- [ ] All verification criteria met
- [ ] Format and structure are correct
- [ ] Quality is acceptable (no obvious errors)
- [ ] Deadlines met
- [ ] All agreed-upon deliverables present
- [ ] Documentation is clear

**Verification message from delegator:**
```
@analyst-agent Q1 Analysis - VERIFICATION

Received: Q1 quarterly review analysis (delivered on time)

Verification results:
✅ Format matches template
✅ All 3 top trends identified with metrics
✅ 3 improvement areas documented
✅ Sources provided for all claims
✅ Delivered before deadline

Status: VERIFIED - Ready to close

Thank you! This is exactly what was needed for the strategy meeting.
```

**If work doesn't meet criteria:**

The delegator provides specific feedback:
```
@analyst-agent Q1 Analysis - REVISION NEEDED

Issue: Improvement areas lack supporting data (verification criteria #4)

Feedback:
- Trend #1: ✅ Solid (metrics clear)
- Trend #2: ✅ Solid (metrics clear)
- Trend #3: ✅ Solid (metrics clear)
- Improvement #1: ❌ Needs more data (source?)
- Improvement #2: ✅ Solid
- Improvement #3: ❌ Needs more data (explain the connection)

Next steps: Revise improvements #1 and #3 with supporting data.
Can you send updated version by EOD tomorrow?
```

**Agent responds:**
- Acknowledges feedback
- Asks clarifying questions if needed
- Revises work or provides corrections
- Resubmits for verification
- Updates daily memory with revision results

---

### Stage 4: Close

**Duration:** 5-10 minutes
**Participants:** Delegator, delegated agent
**Channel:** Communication platform + workspace

The delegation is formally closed with documentation:

**Closure message:**
```
@analyst-agent Q1 Analysis - CLOSED

Final status: ✅ COMPLETE

Deliverables:
- Q1 Analysis Report (Markdown)
- Supporting metrics spreadsheet
- Presentation summary (3 slides)

Location: ~/workspace/deliverables/q1-analysis/

This analysis was crucial for our April strategy meeting. Excellent work
on the trend analysis and supporting data. The improvement recommendations
are actionable.

Duration: 2.5 hours (estimated 2 hours)
Effort: Good match between estimate and actual
Quality: Exceeds expectations

Key learnings for next analysis:
- Having data sources upfront saved revision cycles
- Format template worked well
- 2-hour estimate was accurate for this scope

Closing delegation: Q1 Analysis
```

**In delegated agent's daily memory:**
```
## Delegations - Closed

### Q1 Analysis (Closed 2026-03-28)
- Delegator: admin-agent
- Status: Complete
- Time spent: 2.5 hours
- Outcome: Accepted and deployed to strategy meeting
- Quality feedback: Exceeded expectations
- Learning: Data source clarity prevented revisions

Next time: Ask for data sources upfront to streamline analysis.
```

---

## Delegation Log (Audit Trail)

Each workspace should maintain a delegation log to track all cross-agent work. This is your audit trail and accountability mechanism.

**Location:** `DELEGATION-LOG.md` in shared workspace

**Format:**

```markdown
# Delegation Log

## 2026-03-28

### Q1 Analysis
- Delegator: admin-agent
- Delegated agent: analyst-agent
- Request time: 10:15 AM
- Completion time: 12:45 PM (2.5 hours)
- Status: ✅ COMPLETE
- Quality: Exceeds expectations
- Verification: Passed all criteria
- Notes: Excellent trend analysis

### Meeting Notes Compilation
- Delegator: admin-agent
- Delegated agent: writer-agent
- Request time: 11:00 AM
- Status: 🔄 IN PROGRESS (deadline: tomorrow)
- Blockers: None
- Notes: On track

## 2026-03-27

### Market Research Summary
- Delegator: analyst-agent
- Delegated agent: researcher-agent
- Request time: 2:00 PM
- Completion time: 4:15 PM (2.25 hours)
- Status: ✅ COMPLETE
- Quality: Acceptable
- Verification: Required one revision
- Notes: First-time collaboration, went well

```

**Log updates:**
- Delegator or admin updates log when delegation created
- Agent updates log when delegation complete
- Log is reviewed monthly (see PROCEDURES.md Procedure 3)

---

## Channel Map (Customize for Your Platform)

Replace these with your organization's actual channels:

| Channel Type | Channel Name | Purpose |
|---|---|---|
| Delegations | #delegations | Public requests between agents |
| Urgent | #urgent-delegations | Time-sensitive work (2h SLA) |
| Closed | #delegations-closed | Archive of completed delegations |
| Escalations | #escalations | Issues that require administrator decision |
| Admin | #admin-team | Private admin-only discussions |

**Implementation examples:**

**Discord:**
```
#delegations
- Thread per delegation
- Reactions: 👀 (seen), ✅ (complete), ❌ (blocked)

#urgent-delegations
- Critical path work
- @mentions required
```

**Slack:**
```
Channel: #delegations
- Use threads to keep conversations organized
- Reactions: thumbsup (confirm), eyes (in progress), checkmark (done)

Channel: #urgent-delegations
- Notify @channel if truly urgent
- Use Slack reminders for follow-up
```

**Teams:**
```
Channel: Delegations
- Use @mentions for visibility
- Replies maintain conversation thread
- Pin important delegation requests
```

**Email:**
```
Subject format: [DELEGATION] Task Name - From: Delegator To: Agent

Use folder structure:
- DELEGATIONS/IN-PROGRESS/
- DELEGATIONS/CLOSED/
```

---

## Delegation Scenarios

### Scenario 1: Simple, Low-Risk Delegation

**Task:** "Write a summary of today's standup meeting"

**Time to delegate:** 5 minutes
**Time to execute:** 20 minutes
**Verification:** Quick spot-check

Process:
1. Delegator sends request via communication channel
2. Agent confirms and starts work
3. Agent completes and submits summary
4. Delegator spot-checks (1 minute) and approves
5. Delegator sends closure message
6. Update delegation log
7. Done

---

### Scenario 2: Complex, High-Risk Delegation

**Task:** "Refactor authentication module in production system"

**Time to delegate:** 15 minutes
**Time to execute:** 8 hours (multi-day)
**Verification:** Thorough code review + testing

Process:
1. Delegator and agent meet to discuss scope, approach, timeline
2. Delegator creates detailed specification document
3. Agent asks clarifying questions and estimates effort
4. Agent stages work in development environment
5. Agent requests code review from third agent
6. Reviewers provide feedback (see PROCEDURES.md Procedure 7)
7. Agent revises based on feedback
8. Agent tests in staging environment
9. Delegator verifies tests pass and code quality is high
10. Delegator approves for production deployment
11. Deployment follows PROCEDURES.md Procedure 8
12. Post-deployment verification
13. Closure with lessons learned
14. Update delegation log with timeline

---

### Scenario 3: Blocked Delegation

**Initial request:** "Analyze competitor pricing data"

**Agent discovers:** Data file is missing/inaccessible

**Response:**
1. Agent notifies delegator immediately (don't wait)
2. Provides context: "data/competitor-pricing.csv doesn't exist in workspace"
3. Asks: "Where should I pull this data from?"
4. Delegator responds: "Check shared drive: S:/market-research/2026/pricing.xlsx"
5. Agent accesses data and resumes work
6. Delegation continues normally

**In delegation log:**
- Note: "Blocked 30 minutes on data location; resolved by delegator"

---

## Quality Standards for Delegations

### Delegator Responsibilities

- ✅ Provide clear, written task specification
- ✅ Include verification criteria upfront
- ✅ Give agent required resources or links
- ✅ Specify deadline or urgency level
- ✅ Verify work promptly (don't let it sit)
- ✅ Provide constructive feedback if revisions needed
- ✅ Close delegation formally with closure message
- ✅ Log the delegation in audit trail
- ✅ Thank the agent for their work

### Agent Responsibilities

- ✅ Confirm receipt and understanding
- ✅ Ask clarifying questions before starting
- ✅ Complete work according to spec
- ✅ Update delegator on progress for long tasks
- ✅ Escalate blockers immediately
- ✅ Submit work before deadline
- ✅ Accept feedback professionally
- ✅ Revise if verification criteria not met
- ✅ Document lessons in daily memory

### Red Flags (Avoid These)

- ❌ Vague task descriptions ("make it better")
- ❌ No verification criteria ("I'll know it when I see it")
- ❌ Missing context or resources
- ❌ Unrealistic deadlines
- ❌ Agent starts without confirming understanding
- ❌ Agent disappears mid-task without updates
- ❌ Delegator ignores finished work for days
- ❌ Work accepted without verification
- ❌ Delegations never closed or logged

---

## Integration with Governance

This protocol works with GOVERNANCE.md:

- **Delegation requests** are shared context communication (see Group Chat Etiquette)
- **Blocked delegations** follow escalation from GOVERNANCE.md
- **Long delegations** require heartbeat check-ins (see Heartbeats)
- **Delegation outcomes** are recorded in daily memory (see Memory Management)
- **Delegation patterns** are reviewed in quarterly reviews (see PROCEDURES.md)

## Summary

The delegation protocol ensures:

1. **Clarity** — Both parties understand the task before work starts
2. **Execution** — Agent works independently with clear success criteria
3. **Quality** — Delegator verifies work before acceptance
4. **Accountability** — All delegations are logged and tracked
5. **Learning** — Closure captures lessons for future delegations
6. **Scalability** — Works whether you have 2 agents or 20

Use this protocol for any work that moves between agents. Over time, you'll build trust and efficiency through consistent, clear delegation practices.
