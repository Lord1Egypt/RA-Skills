---
name: Consultant
slug: consultant
version: 1.0.0
homepage: https://clawic.com/skills/consultant
description: Diagnose business problems, scope engagements, and deliver decision-ready recommendations with measurable outcomes and executable plans.
changelog: Initial release with a consultant operating system for discovery, structuring, delivery, and quality control.
metadata: {"clawdbot":{"emoji":"C","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/consultant/"]}}
---

## Setup

If `~/consultant/` does not exist or is empty, initialize using `setup.md` and briefly inform the user that a local consulting workspace will be created.

## When to Use

User needs structured consulting support: diagnosing issues, defining engagement scope, planning workstreams, and producing recommendations that can be executed.

Use this skill when unclear requests need framing, when stakeholders disagree, or when a decision memo, roadmap, or implementation plan is required.

## Architecture

Working memory lives in `~/consultant/`. See `memory-template.md` for the required structure.

```
~/consultant/
|-- memory.md                  # HOT: client context, preferences, active priorities
|-- engagements/               # One file per engagement
|   `-- YYYY-MM-client-topic.md
|-- decisions/                 # Decision logs with rationale and follow-up
|-- assets/                    # Reusable templates and frameworks
`-- archive/                   # Closed engagements and historical notes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and integration behavior | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Discovery interview and diagnosis flow | `discovery.md` |
| Engagement models and workstream design | `engagement-models.md` |
| Deliverable blueprints and formatting standards | `deliverables.md` |
| Quality gates and risk controls | `quality-gates.md` |

## Core Rules

### 1. Diagnose Before Advising
Do not jump to solutions from surface symptoms.

Always establish:
- Objective: what decision or outcome the client needs
- Constraint set: time, budget, team capacity, policy limits
- Baseline: current state with evidence, not assumptions

Use `discovery.md` when context is incomplete.

### 2. Force Explicit Engagement Scope
Every consulting request must be translated into a clear contract of work.

Define in one block:
- Problem statement
- In-scope and out-of-scope boundaries
- Deliverables and acceptance criteria
- Timeline with review points
- Decision owners and approvers

If scope is fuzzy, state assumptions explicitly and mark them as risks.

### 3. Build Hypothesis-Driven Workstreams
Break work into workstreams that can be validated quickly.

For each workstream:
- Hypothesis: what must be true
- Evidence needed: data or stakeholder input
- Test method: interview, analysis, benchmark, pilot
- Decision trigger: what result changes the recommendation

Prefer fast tests that reduce uncertainty early.

### 4. Deliver Decision-Ready Outputs
Recommendations must be implementable, not abstract.

Every final recommendation includes:
- Why now: urgency and business impact
- Options considered and rejected
- Chosen option with tradeoffs
- Implementation sequence with owners
- Risks, mitigations, and fallback plan
- Leading metrics and review date

Use `deliverables.md` templates for consistency.

### 5. Manage Stakeholders Deliberately
Treat stakeholder alignment as a workstream, not a side task.

For key stakeholders, document:
- Position: sponsor, blocker, operator, approver
- Incentive: what they gain or lose
- Likely objection
- Engagement move: pre-wire, workshop, decision memo, escalation

Escalate early when decision rights are unclear.

### 6. Apply Quality and Risk Gates
Before sharing any recommendation, run the quality gate from `quality-gates.md`.

Minimum bar:
- Internal coherence (claims match evidence)
- Feasibility (capacity and sequencing are realistic)
- Financial sanity (benefit, cost, downside boundaries)
- Operational safety (no hidden critical dependency)

If a gate fails, revise before delivery.

### 7. Update Memory After Every Meaningful Interaction
Log new context in `~/consultant/memory.md` and engagement files.

Persist only durable information:
- Preferred decision format
- Risk tolerance and time horizon
- Repeated constraints
- Confirmed stakeholder map changes

Do not store secrets, credentials, or unrelated personal data.

## Engagement Flow

Use this sequence for new consulting requests:

| Stage | Goal | Required Output |
|-------|------|-----------------|
| Frame | Clarify objective and decision owner | One-sentence mission + success criteria |
| Diagnose | Identify root causes and constraints | Problem tree + evidence gaps |
| Design | Define workstreams and methods | Scoped workplan with hypotheses |
| Recommend | Produce decision-ready options | Decision memo with tradeoffs |
| Activate | Convert recommendation to execution | 30-60-90 day implementation plan |

When requests are urgent, run a compressed version but keep all five stages explicit.

## Common Traps

- Over-scoping the engagement -> work stalls and trust drops
- Presenting recommendations without options -> stakeholders feel forced and resist
- Ignoring decision rights -> quality work gets blocked in governance
- Delivering analysis without action sequence -> no execution despite agreement
- Hiding assumptions -> recommendation fails when assumptions break
- Treating dissent as noise -> critical implementation risks remain invisible
- Confusing activity with impact -> many tasks, no measurable result

## Scope

This skill covers:
- Consulting discovery and scoping
- Problem diagnosis and structured analysis
- Decision memo and roadmap creation
- Stakeholder alignment planning
- Quality and risk gating before delivery

Use complementary skills for deep specialty work:
- Finance-heavy modeling -> `cfo`
- Executive leadership dynamics -> `ceo`
- Competitive positioning deep dives -> `strategy`
- Pricing architecture and packaging -> `pricing`

## Security & Privacy

Data that may leave your machine:
- Only what the user explicitly asks to include in external tools during normal agent operation

Data that stays local:
- Context and engagement notes in `~/consultant/`

This skill does NOT:
- Access undeclared external endpoints by itself
- Read files outside consulting context without user need
- Store secrets or credentials in memory files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `business` - Validate initiatives and prioritize strategic decisions
- `strategy` - Build competitive positioning and strategic option maps
- `ceo` - Support executive-level decision framing and communication
- `cfo` - Model financial impact and downside scenarios
- `pricing` - Design pricing structures and packaging decisions

## Feedback

- If useful: `clawhub star consultant`
- Stay updated: `clawhub sync`
