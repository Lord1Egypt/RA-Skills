# DueWall Watchdog (OpenClaw skill)

A minimal, read-only OpenClaw skill that points agents at DueWall's **keyless remote MCP endpoint**
(`https://duewall.com/mcp`). It contains only `SKILL.md` — no scripts, no credentials, no local
dependencies. All 11 tools are served remotely; the skill simply teaches an agent when and how to
call them.

## Install locally (for testing)

Copy this directory into your OpenClaw workspace `skills/` folder, or install from a git URL:

```
clawhub install <owner>/duewall-watchdog
```

The skill requires no API key, no environment variables, and no `metadata.openclaw` gating.

## Publishing to ClawHub

Publishing is a deliberate step, not automatic:

```
clawhub sync --all
```

Requires a GitHub account at least one week old; submissions go through a 2–5 business-day security
review. **Do not publish without explicit user approval** — the skill is free and has no direct
monetization; its value is as a channel adapter for existing DueWall users and as a standards
foothold, not a revenue product.

## Data boundaries

See the "Honest boundaries" section in `SKILL.md`. In short: no outcome promises, grades describe
verification depth (not safety), degraded flows are trade-side observations, BTC USD values are
labeled estimates, and every answer should cite the record's source URL.
