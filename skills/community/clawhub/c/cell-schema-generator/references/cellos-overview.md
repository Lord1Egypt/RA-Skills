# CellOS Framework Overview

CellOS is an organizational design framework for AI-native teams. It structures organizations as autonomous, accountable decision-making cells that operate independently within defined scope and coordinate via explicit protocols.

## Core Principles

### 1. Explicit Over Implicit
Every cell must document what it does, who owns what, when to escalate, and how it coordinates. Nothing is assumed. If it's not in the schema, it doesn't exist.

### 2. Scope Before Execution
Before a cell can operate, it must have a defined scope boundary. Cells that don't know their edges will expand until they conflict with other cells or break accountability chains.

### 3. Five-Role Completeness
Every cell needs all five steward roles covered. Missing a steward doesn't mean that dimension is handled informally — it means it's unowned, which creates risk.

### 4. Escalation is a Feature, Not a Failure
A well-designed cell escalates frequently and early. Escalation rules are not a sign of weakness — they're how cells maintain human oversight of AI-speed operations.

### 5. Coordination is Explicit
Cells don't "stay in sync" — they have documented protocols: what data moves, in which direction, on what cadence, in what format. If coordination isn't documented, it isn't reliable.

## The Five Steward Roles

### Clarity Steward
**Question answered:** What are we doing and why?

The Clarity steward owns the cell's mission, goals, and scope. They resolve disputes about whether something falls within the cell's mandate. They approve changes to the cell charter.

*Common mistakes:* Making Clarity the most senior person by default. Clarity should go to whoever has the deepest understanding of the mission, not the highest title.

### Execution Steward
**Question answered:** How do we get it done?

The Execution steward owns workflow, deadlines, and resource allocation. They track what's in flight, remove blockers, and manage the operational cadence of the cell.

*Common mistakes:* Conflating Execution with "project manager" — Execution owns the rhythm of work, not just task tracking.

### Narrative Steward
**Question answered:** How do we explain what we're doing?

The Narrative steward owns how the cell communicates externally — to stakeholders, to other cells, to the outside world. They maintain documentation and own the cell's reputation.

*Common mistakes:* Skipping Narrative for internal cells. All cells have stakeholders. All cells need someone to own the story.

### Access Steward
**Question answered:** What do we need to operate?

The Access steward owns tools, data, permissions, and integrations. They ensure the cell has what it needs and that what it has is appropriate to its scope.

*Common mistakes:* Making Access an afterthought. In AI-native orgs, Access is often the most operationally critical role — the wrong tool access or data permissions can cause serious incidents.

### Integrity Steward
**Question answered:** Are we doing this right?

The Integrity steward owns quality, compliance, and risk. They audit the cell's outputs, monitor for drift, and escalate anything that looks wrong.

*Common mistakes:* Treating Integrity as "QA" only. Integrity includes compliance, risk management, and the hard conversations when the cell is producing bad outputs.

## Cell Types

### Operational Cell
Ongoing work with no defined end date. Examples: customer support, pipeline monitoring, content production.

Design note: Operational cells need especially tight scope definitions because they run indefinitely. Scope creep is an existential risk for operational cells.

### Project Cell
Time-bounded initiative with a clear deliverable and end date. Examples: product launch, infrastructure migration, research initiative.

Design note: Project cells should have a defined dissolution protocol — what happens to the cell's knowledge, assets, and team when the project completes.

### Coordination Cell
Exists to synchronize other cells. Examples: executive committee, architecture review board, release management.

Design note: Coordination cells should have strict output definitions. "Staying aligned" is not an output. Define what decisions this cell makes and what artifacts it produces.

### Advisory Cell
Provides input without execution authority. Examples: security review board, ethics committee, external advisory panel.

Design note: Advisory cells are often underspecified. Define what questions they answer and what triggers a consultation — otherwise they become rubber stamps or get bypassed.

## Escalation Design Principles

Good escalation rules are:
- **Specific**: "Amount exceeds $500" not "seems too large"
- **Named**: "Escalate to Sarah Chen (Clarity steward)" not "escalate to leadership"
- **Time-bounded**: "4 hours to respond or trigger fallback"
- **Complete**: What happens if the escalation target doesn't respond?

Common escalation triggers in AI-native orgs:
- Irreversible actions above a threshold (financial, data deletion, external communications)
- Uncertainty above a confidence threshold
- Novel situations without precedent in the cell's memory
- Any action affecting a cell outside the current cell's scope
- Compliance or legal risk indicators

## Common Schema Mistakes

1. **Scope without boundaries**: "Handle customer issues" — what kind? How large? Which channels?
2. **Stewards without responsibilities**: Naming a steward but not defining what they own
3. **Escalation without targets**: "Escalate to leadership" — which leader? By what channel?
4. **Missing out_of_scope**: Only defining what's in scope creates infinite scope by default
5. **No metrics**: Can't tell if the cell is working without measurement
6. **Single-person cells**: One person can't cover all five roles sustainably — identify the person, but note coverage gaps

## Relationship to AI Agents

CellOS cells can have AI agents as stewards. When an AI agent is a steward:
- The agent's SOUL.md or governance spec must be referenced in the schema
- The agent's escalation targets must be human (no agent-to-agent escalation chains)
- An Integrity steward must be human and must have authority to override the agent

The Access steward role is particularly important for AI agent cells — it defines what data the agent can see, which external systems it can call, and what permissions it holds. An underdefined Access role for an AI agent is a security risk.
