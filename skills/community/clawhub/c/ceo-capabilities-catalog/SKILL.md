---
name: ceo-capabilities-catalog
description: Catalog the current OpenClaw instance's installed skills, custom skills, and coordination-oriented capabilities. Use when the user asks what this agent can do, what skills are installed, or needs a backup inventory of current capabilities.
---

# CEO Capabilities Catalog

Use this skill to summarize the current instance's capabilities rather than to execute external systems directly.

## Include in summaries

- Installed builtin skills from the OpenClaw package
- Installed user skills from `~/.openclaw/skills`
- Coordination role: task dispatch, progress tracking, reporting, risk spotting
- Current connected workflow highlights if known from local workspace memory

## Source of truth

Read from:

- Local workspace memory files
- `capabilities-inventory.md` backup file if present
- Installed `SKILL.md` files when needed

## Do not

- Claim unavailable channels or API keys are working unless verified
- Expose secrets from scripts or config files in the summary
