# PM Communication Templates

## Requirements Summary Template

Use this after Phase 1 elicitation to confirm understanding with the client before proceeding to technical assessment.

```
REQUIREMENTS SUMMARY
[Project Name]
Date: [YYYY-MM-DD]
Prepared for: [Client Name]

═══════════════════════════════════════

BACKGROUND
[2-3 sentences: Why is the client requesting this? What business
problem or opportunity is driving the request?]

CURRENT STATE (for existing software)
[Brief summary of how the relevant areas of the software work
today, based on the engineer's software audit. Written so the
client can confirm accuracy.]

REQUESTED CHANGES / NEW FEATURES

1. [Feature/Change Name]
   - What: [Plain-language description of what the client wants]
   - Why: [Business reason / problem it solves]
   - Priority: [Must-Have / Should-Have / Nice-to-Have]
   - Current behavior (if applicable): [How it works now]
   - Desired behavior: [How it should work after]
   - Notes: [Any constraints, preferences, or specifics mentioned]

2. [Feature/Change Name]
   ...

IDENTIFIED CONCERNS
[Anything you spotted during elicitation that needs attention:
conflicts between requirements, implicit dependencies, areas
where the client's request may affect other parts of the system]

ITEMS EXPLICITLY OUT OF SCOPE
[Things discussed and agreed to NOT include]

OPEN QUESTIONS
[Anything you still need clarity on]

NEXT STEPS
- Client confirms this summary is accurate
- PM sends to engineering for technical assessment
- PM returns to client with effort estimates, timeline,
  and any technical concerns

═══════════════════════════════════════
```

## Client Assessment Summary Template

Use this to present the engineer's technical assessment back to the client in business-friendly language.

```
ASSESSMENT SUMMARY
[Project Name]
Date: [YYYY-MM-DD]

═══════════════════════════════════════

OVERVIEW
[1-2 paragraphs: Overall assessment of the requested changes.
Are they feasible? What's the general level of effort? Any
major considerations the client should know upfront?]

FEATURE-BY-FEATURE ASSESSMENT

1. [Feature Name]
   Status: [Feasible / Feasible with considerations / Needs discussion]
   Estimated Effort: [Low / Medium / High — with plain-language
     explanation like "roughly 1-2 weeks of development work"]
   Impact: [What parts of the application are affected]
   What you'll see: [Description of the end result from the
     user's perspective — what the interface/workflow will look
     like after implementation]
   Compared to now: [How this differs from current behavior]
   Considerations: [Any risks, trade-offs, or things the client
     should weigh in on]
   AI Delivery Outlook:
   - Estimated AI delivery time: [X hours/days]
   - Complexity: [Trivial/Low/Medium/High/Very High]
   - Confidence of successful AI delivery: [XX%]
   - Estimated AI cost: $[X.XX]
   - Comparable human cost: $[X.XX] ([X] hours at standard rates)
   - Estimated savings: $[X.XX] ([X]%)

2. [Feature Name]
   ...

OVERALL PROJECT ESTIMATES

   | Metric | Human (Traditional) | AI-Assisted |
   |--------|-------------------|-------------|
   | Total effort | [X] hours | [X] hours |
   | Estimated duration | [X] weeks | [X] days |
   | Total cost | $[X] | $[X] |
   | Savings | — | $[X] ([X]%) |

RECOMMENDATIONS
[Your PM-level recommendations: suggested phasing, things to
prioritize, items to defer, risks to mitigate]

OPEN ITEMS REQUIRING YOUR INPUT
[Decisions the client needs to make before we proceed]

NEXT STEPS
- Client reviews and provides feedback
- PM and client iterate until scope is agreed
- PM produces formal SRS for final review and sign-off

═══════════════════════════════════════
```

## Status Update Template

Use this when the client requests a project status update. Pull data from Asana task states.

```
PROJECT STATUS UPDATE
[Project Name]
Date: [YYYY-MM-DD]
Reporting Period: [Date range]
Overall Status: [On Track / At Risk / Blocked / Ahead of Schedule]

═══════════════════════════════════════

SUMMARY
[2-3 sentences: Where the project stands at a high level.
Lead with the most important information.]

PROGRESS OVERVIEW

   Completed:    [X] of [Y] tasks ([Z]%)
   In Progress:  [X] tasks
   In QA:        [X] tasks
   Not Started:  [X] tasks (Features: [X], Bugs: [X])
   Blocked:      [X] tasks

COMPLETED SINCE LAST UPDATE
- [Task/Feature name]: [Brief description of what was delivered]
- [Task/Feature name]: [Brief description]

CURRENTLY IN PROGRESS
- [Task/Feature name]: [What's happening, expected completion]
- [Task/Feature name]: [What's happening, expected completion]

IN QA / TESTING
- [Task/Feature name]: [Testing status]

RISKS & BLOCKERS
[If none, say "No current risks or blockers identified."]
- [Risk/Blocker]: [Description, impact, what's being done]

UPCOMING
[What's planned for the next period]

TIMELINE ASSESSMENT
[Are we on track relative to original estimates? If not, what
changed and what's the revised expectation?]

DECISIONS NEEDED FROM YOU
[Any items requiring client input or approval]

═══════════════════════════════════════
```

## Change Request Log Template

Use this to track change requests that come in after SRS sign-off.

```
CHANGE REQUEST
CR-[XXX]
Date Submitted: [YYYY-MM-DD]
Requested By: [Client name/contact]
Project: [Project Name]
SRS Version at Time of Request: [X.X]

═══════════════════════════════════════

DESCRIPTION OF REQUESTED CHANGE
[What the client is asking for, in their words]

PM CLASSIFICATION
- Impact Level: [1-5 per the Change Impact Classification]
- Scope Assessment: [Within existing scope / New scope]
- Affected SRS Requirements: [List any existing FR/NFR IDs affected]

PRELIMINARY IMPACT ASSESSMENT
(For Level 1-2, PM completes this directly. For Level 3+,
this section is completed after engineer consultation.)
- Affected areas: [What parts of the system are impacted]
- Effort estimate: [Hours / complexity]
- Timeline impact: [None / Delays completion by X days / etc.]
- Cost impact: [Additional cost estimate if applicable]
- Risk: [Any risks introduced by this change]

RECOMMENDATION
[PM's recommendation: approve, defer, modify, or decline — with
reasoning]

DECISION
- [ ] Approved — proceed with SRS amendment
- [ ] Approved with modifications — [describe modifications]
- [ ] Deferred to future phase
- [ ] Declined — [reason]

Decision Date: [YYYY-MM-DD]
Decided By: [Client name]

IF APPROVED:
- New SRS Version: [X.X]
- New/Modified Asana Tasks: [List task IDs or names]
- Revised Timeline Impact: [Description]
- Additional Cost: $[X.XX]

═══════════════════════════════════════
```

## Project Kickoff Checklist

Use this when starting a new project to ensure nothing is missed.

```
PROJECT KICKOFF CHECKLIST
[Project Name]
Date: [YYYY-MM-DD]

PRE-ENGAGEMENT
- [ ] Client contact information confirmed
- [ ] Project type identified: [New Build / Enhancement / Bug Fix]
- [ ] Project folder exists at ~/.openclaw/projects/[project-id]/
- [ ] project-lock.json confirms phase: idle
- [ ] Existing software? If yes, post Software Audit Request to queues/to-engineer.md

REQUIREMENTS PHASE (project-lock.json → requirements)
- [ ] Discovery conversation completed
- [ ] Requirements Summary produced and sent to client
- [ ] Client confirmed Requirements Summary
- [ ] SPEC-v1-[date].md created in workspace/, SPEC-CURRENT.md updated
- [ ] Technical Assessment posted to queues/to-engineer.md + Asana Engineer Queue
- [ ] Technical Assessment received (queues/to-pm.md entry marked READ)
- [ ] Client Assessment Summary produced and sent to client
- [ ] Client feedback incorporated
- [ ] UI comparisons requested/reviewed (if applicable)
- [ ] Scope agreed upon by client

SRS PHASE
- [ ] SRS draft produced as workspace/SPEC-v[N]-[date].md
- [ ] SRS sent to client
- [ ] Client review feedback received
- [ ] All client decisions logged in DECISIONS.md
- [ ] All revisions completed
- [ ] Engineer marks spec ACCEPTED in SPEC-CURRENT.md
- [ ] Acceptance logged in DECISIONS.md
- [ ] project-lock.json → planning

ENGINEERING HANDOFF (project-lock.json → planning)
- [ ] Implementation Plan request posted to queues/to-engineer.md + Asana
- [ ] Engineer posts completion to queues/to-pm.md
- [ ] workspace/IMPLEMENTATION_GUIDE.md reviewed against all SRS requirements
- [ ] Gaps addressed and plan finalized

ASANA SETUP (project-lock.json → implementation)
- [ ] All tasks created in Backlog with correct descriptions, branch names, estimates
- [ ] Dependencies set between tasks per Task Manifest
- [ ] project-lock.json updated: phase implementation, sprint_id set
- [ ] STATE.md updated to reflect sprint open
- [ ] queues/to-engineer.md notified of sprint open
- [ ] sessions_send nudge sent to engineer and devs

ONGOING
- [ ] Status update cadence agreed with client
- [ ] Change request protocol communicated to client
- [ ] queues/to-pm.md checked at every heartbeat
```
