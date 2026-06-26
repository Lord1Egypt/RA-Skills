---
name: agent-collab-protocol
description: Standardized agent collaboration protocol for multi-agent systems. Defines L0/L1/L2 hierarchy, task contracts, error handling, agent templates, and a new-agent creation checklist — ready to use with OpenClaw or any agent framework.
tags: protocol, agent-collaboration, template, checklist, openclaw
---

# Agent Collaboration Protocol

A **complete protocol layer** for building structured, multi-agent systems.  
Provides the rules, templates, and operational procedures to ensure agents work together consistently.

## What's Included

| Component | Description |
|-----------|-------------|
| **AGENT_COLLAB_PROTOCOL.md** | Core protocol: L0/L1/L2 hierarchy, JSON task contracts, `<agent-response>` format, error handling, spawn vs send patterns |
| **OPERATIONS.md** | Operational guide: how to add/remove domains, file ownership matrix, protocol change propagation |
| **NEW_AGENT_CHECKLIST.md** | 8-step mandatory checklist for creating new sub-agents (no skip, no placeholder) |
| **TEMPLATE_AGENTS.md** | Standard AGENTS.md template with protocol implementation table |
| **TEMPLATE_IDENTITY.md** | Identity card template (Agent ID, layer, upstream/downstream, model) |
| **TEMPLATE_SOUL.md** | Values and red lines template (core belief, values, anti-patterns) |
| **TEMPLATE_USER.md** | Service object template (upstream, downstream consumers, service standards) |
| **scaffold-domain.sh** | Shell script to auto-generate a new domain workspace from templates |

## Quick Start

### Install from ClawHub
```bash
npx clawhub install agent-collab-protocol
```

### Or use locally
```bash
# Protocol files are in: skill/agent-collab-protocol/references/
# Copy to your protocol directory:
cp -r skill/agent-collab-protocol/references/ ~/.openclaw/protocol/
```

### Create a new business domain
```bash
cd ~/.openclaw/protocol
bash scaffold-domain.sh fintech 金融产品经理 "fintech-analyzer:金融分析师"
```

## Architecture Overview

```
Layer 0 (Orchestrator)          Identify domain → dispatch to Manager → verify
    ↓ (natural language)
Layer 1 (Manager)               Understand → decompose → dispatch → aggregate
    ↓ (JSON Task Package)
Layer 2 (Specialist)            Execute → deliver via <agent-response>
```

### Key Protocol Rules

- **L0** dispatches to L1 Managers via natural language
- **L1** decomposes tasks into JSON Task packages for L2 Specialists
- **L2** executes and returns `<agent-response>` blocks
- Tasks that fail: retry 1 time → downgrade → report as partial/failed
- 3-layer maximum depth (L0 → L1 → L2)

## Usage

### For Framework Authors
Reference `AGENT_COLLAB_PROTOCOL.md` to implement protocol compliance in your agent runtime.

### For Agent Developers
1. Copy the relevant TEMPLATE_*.md files
2. Fill in your agent's business-specific content
3. Register in your domain configuration
4. Follow NEW_AGENT_CHECKLIST.md for new agents

### For Team Leads
Use `NEW_AGENT_CHECKLIST.md` as a mandatory gating process — each team member must check off all 8 steps before a new agent is considered complete.

## Files

```
agent-collab-protocol/
├── SKILL.md                       ← This file
├── _meta.json                     ← Package metadata
└── references/
    ├── AGENT_COLLAB_PROTOCOL.md   ← Core protocol (413 lines)
    ├── OPERATIONS.md              ← Operational guide
    ├── NEW_AGENT_CHECKLIST.md     ← Mandatory checklist (156 lines, 64 checks)
    ├── TEMPLATE_AGENTS.md         ← AGENTS.md template
    ├── TEMPLATE_IDENTITY.md       ← Identity card template
    ├── TEMPLATE_SOUL.md           ← Values & red lines template
    ├── TEMPLATE_USER.md           ← Service object template
    └── scaffold-domain.sh         ← Domain scaffolding script
```

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-06-04 | Initial public release |
