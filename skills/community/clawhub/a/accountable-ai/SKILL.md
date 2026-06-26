# Accountable AI — Governance Framework for AI Agent Teams

Use this skill to implement accountability structures, decision trails, and responsibility chains across your AI agent team.

## What This Skill Does

Establishes a governance framework that makes every AI agent in your team accountable for:
- What they were asked to do
- What they actually did
- What decisions they made autonomously
- What they escalated and why

## When to Use

- Setting up a new AI agent team
- When you need to know who did what and when
- After something goes wrong and you need to trace the root cause
- When giving agents more autonomy and need guardrails
- When multiple agents interact and ownership gets blurry

## Core Files

This skill installs three files to your agent workspace:

**GOVERNANCE.md** — The accountability charter. Defines roles, decision authority, and responsibility chains. Each agent reads this on startup to know what they can do independently and what requires escalation.

**PROCEDURES.md** — Repeatable checklists for operations that must not be improvised. Config changes, agent onboarding, infrastructure tasks. When an agent encounters a known procedure type, it runs the checklist — not its own interpretation.

**DELEGATION.md** — The delegation protocol. How work moves between agents. Who owns what. How handoffs are documented. Prevents the "I thought someone else was handling it" failure mode.

## How It Works

1. Install the files to your agent workspace
2. Reference them in your AGENTS.md so agents load them each session
3. Agents follow the governance rules automatically when making decisions
4. Procedures prevent improvisation on sensitive operations
5. Delegation logs create an audit trail of who did what

## Installation

```bash
chmod +x install.sh && ./install.sh
```

Or manually copy GOVERNANCE.md, PROCEDURES.md, and DELEGATION.md to your agent workspace.

## After Installing

Add to your AGENTS.md boot sequence:
```
3. Read GOVERNANCE.md — your decision authority and escalation rules
4. Read PROCEDURES.md — before any config change or infrastructure task
```

## Part of Trust AI Suite

Accountable AI is the foundation layer of the Trust AI Suite:

- **Accountable AI** (this) — Governance & accountability
- **Proof of Work** — Verify agents completed tasks
- **AgentOps Tracker** — Full operational visibility ($49)
- **Total Recall** — Forensic memory search ($69)
- **Anticipation** — Predict what you need before you ask ($39)

→ Full suite: [Trust AI Stack on ClawMart](https://www.shopclawmart.com)
