# FounderClaw

**Multi-agent engineering team for OpenClaw.**

FounderClaw transforms your OpenClaw into a complete engineering organization — a CEO that orchestrates 5 specialist departments, 29 skills, structured workspace, and automated workflows.

**This is not a skill pack. It's a system.**

## What it installs

| Component | What |
|---|---|
| 29 Skills | code review, QA, design, security, debugging, shipping, browser testing... |
| 6 Agents | CEO (orchestrator) + Strategy, Shipper, Tester, Safety, Observer |
| Workspace | `~/.openclaw/founderclaw/` — shared projects + private department desks |
| Tool Policies | each agent only gets the tools it needs |
| Model Config | 3 tiers: Fast, Best, Vision |

## Install

### Chat (recommended)

Paste this into any OpenClaw chat:

> I'd like you to set up FounderClaw, the multi-agent engineering team for OpenClaw.
> 
> Clone it: `git clone --depth 1 https://github.com/ashish797/FounderClaw.git ~/.agents/skills/founderclaw`
> 
> Then run the installer: `cd ~/.agents/skills/founderclaw && bash install.sh`

Or just say: **"install founderclaw"**

The agent will:
1. Explain what FounderClaw is
2. Ask for your model preferences
3. Install 29 skills + create workspace
4. Ask permission to modify your OpenClaw config
5. Add 6 agents with proper tool policies
6. Restart the gateway

### Terminal

```bash
curl -fsSL https://raw.githubusercontent.com/ashish797/FounderClaw/main/install.sh | bash
```

Then say "install founderclaw" in chat to complete the multi-agent config.

### Landing page

Visit https://founderclaw.hashqy.com for copy-paste setup instruction.

## The Team

| Agent | Emoji | Role |
|---|---|---|
| CEO | 🎯 | Orchestrates everything. Talks to you. |
| Strategy | 📐 | Product thinking, design, architecture |
| Shipper | 🚀 | Code review, deployment, releases |
| Tester | 🔍 | QA, browser testing, bug detection |
| Safety | 🛡️ | Security audits, guardrails |
| Observer | 📊 | Debugging, retrospectives, second opinions |

## Skills (29)

### Strategy & Planning
- office-hours — brainstorm with 6 forcing questions
- plan-ceo-review — CEO-level scope and strategy review
- plan-eng-review — architecture, data flow, edge cases
- plan-design-review — UI/UX plan review
- design-consultation — create a design system
- design-review — visual QA
- design-shotgun — rapid visual exploration (3 variants)
- autoplan — auto-select and chain the right reviews

### Code Quality
- review — two-pass code review (CRITICAL + INFORMATIONAL)
- investigate — systematic debugging, root cause first
- codex — independent second opinion via sub-agent

### Design
- design-consultation — create a design system (typography, color, layout)
- design-review — visual QA (spacing, hierarchy, accessibility)
- design-shotgun — rapid visual exploration (3 variants)

### Shipping
- ship — merge, test, version bump, changelog, create PR
- land-and-deploy — merge, tag, deploy, verify
- canary — post-deploy monitoring
- document-release — release notes and changelogs
- benchmark — performance regression detection

### Quality Assurance
- qa — systematic testing + iterative bug fixing
- qa-only — QA report only (no fixing)
- browse — headless browser (~100ms per command)
- setup-browser-cookies — import cookies for auth testing
- connect-chrome — real Chrome with Side Panel

### Safety
- cso — OWASP + STRIDE security audit
- careful — warns before destructive commands
- freeze — restrict edits to a directory
- guard — careful + freeze combined
- unfreeze — remove edit restriction

### Retrospectives
- retro — weekly engineering retrospective

### Setup
- gstack-upgrade — self-update
- setup-deploy — configure deployment platform
- install-founderclaw — install/repair/uninstall

## Uninstall

Say: **"uninstall founderclaw"**

Or manually:
```bash
bash ~/.agents/skills/founderclaw/uninstall.sh
```

## Inspired By

[gstack](https://github.com/garrytan/gstack) by Garry Tan — MIT License. Rebuilt for OpenClaw.

## License

MIT
