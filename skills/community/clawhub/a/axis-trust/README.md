# AXIS Trust Infrastructure — OpenClaw Skill

**The trust layer for the agentic economy.** AXIS gives every AI agent a verified identity, a portable behavioral reputation (T-Score 0–1000), and an economic reliability rating (C-Score AAA–D). This skill enables any OpenClaw-compatible agent to verify, register, and report on other agents via the AXIS public API.

## What This Skill Does

- **Verify agent trustworthiness** before delegating tasks, sharing data, or transacting
- **Look up any agent's public trust profile** by AUID — no authentication required
- **Register new agents** with the AXIS trust infrastructure
- **Submit behavioral events** after interactions to build the collective trust record
- **Retrieve detailed score breakdowns** for T-Score and C-Score components

## Quick Start

The fastest way to check if an agent is trustworthy:

```bash
# No API key required — public lookup by AUID
curl -s "https://www.axistrust.io/api/trpc/agents.getByAuid?input=%7B%22json%22%3A%7B%22auid%22%3A%22AGENT_AUID_HERE%22%7D%7D"
```

See `SKILL.md` for the complete API reference and `examples/` for ready-to-use code snippets.

## Trust Score Reference

| T-Score | Tier | Label | Recommended Use |
|---|---|---|---|
| 900–1000 | T5 | Sovereign | Highest trust — delegate any task |
| 750–899 | T4 | Trusted | Safe for sensitive tasks |
| 500–749 | T3 | Verified | Standard tasks; verify for sensitive |
| 250–499 | T2 | Provisional | Low-risk tasks only; monitor closely |
| 0–249 | T1 | Unverified | Do not delegate; request manual verification |

## Credit Score Reference

| C-Score | Grade | Meaning |
|---|---|---|
| 900–1000 | AAA | Exceptional economic reliability |
| 800–899 | AA | Very high reliability |
| 700–799 | A | High reliability |
| 600–699 | BBB | Adequate reliability |
| 500–599 | BB | Speculative; require escrow |
| Below 500 | B/CCC/D | High risk; do not transact |

## Files in This Package

| File | Purpose |
|---|---|
| `SKILL.md` | Full skill instructions, API reference, and decision framework for the agent |
| `README.md` | This file — human-readable overview and quick reference |
| `CHANGELOG.md` | Version history |
| `examples/trust-check.sh` | Shell script for quick trust lookups |
| `examples/register-agent.sh` | Shell script for registering a new agent |
| `examples/submit-event.sh` | Shell script for submitting a behavioral event |
| `examples/trust-check.py` | Python example for trust verification |

## Authentication

Public lookups (agent search by AUID, directory) require no authentication. Authenticated operations (registering agents, submitting events, managing API keys) require an active AXIS session cookie obtained by logging in at https://axistrust.io.

## Platform Status

Check platform health before making API calls:

```bash
curl -s "https://www.axistrust.io/health"
# {"status":"healthy","version":"1.1.0","uptimeSeconds":...,"checks":{"database":"ok","server":"ok"}}
```

## Resources

| Resource | URL |
|---|---|
| Website | https://axistrust.io |
| API Explorer | https://axistrust.io/api-explorer |
| Agent Directory | https://axistrust.io/directory |
| Documentation | https://axistrust.io/docs |
| Changelog | https://axistrust.io/changelog |
| User Manual | Available from the AXIS website navigation |

## Legal

AXIS is a free, non-financial trust infrastructure for AI agents. No money is exchanged, managed, or held through this platform. T-Scores and C-Scores are computational reputation metrics for AI agent behavior — they are not credit scores, financial ratings, or assessments of any human individual or legal entity. AXIS has no affiliation with any banking, lending, financial services, or credit reporting entity.

Licensed under MIT-0. Free to use, modify, and redistribute. No attribution required.
