---
name: founderclaw
description: >
  FounderClaw — Multi-agent engineering team for OpenClaw. 29 skills,
  6 agents (CEO + 5 departments), structured workspace, auto mode,
  vision sub-agent routing. Build startups with AI agents.
---

# FounderClaw

Multi-agent engineering team for OpenClaw. 29 skills. 6 agents. One install.

## IMPORTANT: Post-Install Setup Required

After installing this package (via ClawHub or git clone), you MUST run the installer to:
1. Symlink individual skills to `~/.agents/skills/`
2. Create the workspace at `~/.openclaw/founderclaw/`
3. Apply multi-agent config (6 agents)
4. Build the headless browser

Run from this directory:
```bash
bash install.sh
```

This is REQUIRED. Without it, only the package directory exists — skills won't be discovered by OpenClaw.

## What FounderClaw Adds

**Agents:**
| Agent | Role |
|---|---|
| CEO (🎯) | Orchestrates everything |
| Strategy (📐) | Product thinking & design |
| Shipper (🚀) | Code review & deploy |
| Tester (🔍) | QA & browser testing |
| Safety (🛡️) | Security & guardrails |
| Observer (📊) | Debug & retrospectives |

**Skills (29):**
Strategy: office-hours, plan-ceo-review, plan-eng-review, plan-design-review, design-consultation, design-review, design-shotgun, autoplan
Shipping: review, ship, land-and-deploy, canary, benchmark, document-release
Testing: qa, qa-only, browse, setup-browser-cookies, connect-chrome
Safety: cso, careful, freeze, guard, unfreeze
Debugging: investigate, retro, codex
Setup: gstack-upgrade, setup-deploy, install-founderclaw, founderclaw-status

## Links
- GitHub: https://github.com/ashish797/FounderClaw
- Landing: https://founderclaw.hashqy.com

## License
MIT
