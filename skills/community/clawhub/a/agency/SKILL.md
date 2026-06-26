---
name: Agency
slug: agency
version: 1.0.1
description: Build and operate a service agency with client management, project tracking, pricing, and team coordination.
metadata: {"clawdbot":{"emoji":"🏢","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User wants to start or scale a service agency: marketing, development, design, consulting, content, automation, or any service business. Agent handles operations so human focuses on clients and strategy.

## Quick Reference

| Area | File |
|------|------|
| Client onboarding | `onboarding.md` |
| Pricing and proposals | `pricing.md` |
| Project management | `projects.md` |
| Client communication | `communication.md` |
| Deliverables workflow | `deliverables.md` |
| Team coordination | `team.md` |
| Agency-type specifics | `by-type.md` |
| Learning system | `feedback.md` |

## Workspace Structure

Agency data lives in ~/agency/:

```
~/agency/
├── clients/           # One file per client
│   ├── index.md       # Client list with status
│   └── [name].md      # Client profile, history, preferences
├── projects/          # Active project tracking
├── templates/         # Reusable proposals, briefs, reports
├── knowledge/         # SOPs, learnings, case studies
└── config.md          # Rates, margins, team structure
```

## Core Operations

**Client intake:** Brief arrives (audio, email, doc) → Extract scope, budget, timeline → Generate structured brief → Flag red flags (scope creep, unrealistic deadlines) → Create client folder.

**Pricing:** Given scope → Apply rate card from config → Calculate estimate with complexity multipliers → Generate proposal PDF → Compare with historical similar projects.

**Project tracking:** Maintain unified board of all active projects → Alert on deadlines → Detect stalled projects → Generate weekly status by client.

**Deliverables:** Transform rough notes/input → Structured deliverable → Review against brief → Adapt to multiple formats if needed.

## Critical Rules

- Never send proposals or communicate with clients without human approval
- Track time/cost vs estimates — alert when project is losing money
- Learn from corrections — update templates and knowledge base
- Maintain client context across sessions — refer to history

## Config Fields

Create ~/agency/config.md with rates, team, and margins. See `pricing.md` for format.
