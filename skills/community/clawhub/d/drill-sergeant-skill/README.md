# 🫡 Drill Sergeant

Lightweight governance for multi-agent teams.

## System hierarchy

```text
┌──────────────────────────────┐
│ MAIN SYSTEM                  │
│ (ClawStation / Orchestrator) │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DRILL SERGEANT SKILL         │
│ (Agent Discipline & Task     │
│ Enforcement)                 │
└──────────────┬───────────────┘
               │
   ┌───────────┼───────────┐
   ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│ Task      │ │ Behavior  │ │ Monitor   │
│ Manager   │ │ Enforcer  │ │ System    │
│ Assigns   │ │ Prevents  │ │ Watches   │
│ tickets   │ │ random    │ │ loops/    │
│ and jobs  │ │ actions   │ │ stale work│
└─────┬─────┘ └─────┬─────┘ └─────┬─────┘
      │             │             │
      ▼             ▼             ▼
  ┌───────┐     ┌───────┐     ┌───────┐
  │Agent 1│     │Agent 2│     │Agent 3│
  │Coder  │     │Tester │     │Ops    │
  └───────┘     └───────┘     └───────┘
```

Drill Sergeant helps enforce communication discipline and execution hygiene in shared work channels by identifying common operational failure patterns and producing clear corrective actions.

## What it helps with

- Detect repeated/looping messages
- Flag routing violations (wrong channel / wrong audience)
- Surface missing ownership signals
- Highlight stale in-review work
- Reduce noisy status chatter
- Produce concise manager-ready summaries

## Typical workflow

1. Define scope and rules for the review window
2. Collect message/task signals from approved sources
3. Detect violations using the checklist
4. Deduplicate repeated findings
5. Output owner-specific corrective actions
6. Escalate only high-severity or repeated issues

## Output structure

Each finding should include:

- `type`
- `severity` (`low|medium|high`)
- `evidence`
- `action`
- `owner`

Then summarize:

- Top 3 immediate actions
- Escalations (if any)
- All clear (when no actionable issues)

## Included references

- `references/enforcement-checklist.md`
- `references/message-templates.md`
- `references/public-safety-checklist.md`

## Public-safety stance

This package is designed to be publish-safe:

- No personal identifiers
- No webhook/callback dependencies
- No API keys, tokens, or secrets
- No internal host/IP references

## Installation

### ClawHub (after listing is live)

```bash
clawhub install drill-sergeant
```

### Local

Copy this folder into your OpenClaw skills directory and load it per your normal skill workflow.

## Upgrade path

Drill Sergeant is the lightweight discipline layer.

For full multi-agent operations (orchestration, dashboards, automation workflows, and team command center), pair it with **ClawStation**:

- https://clawstation.dev
