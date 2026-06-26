---
minimum_skill_version: 2.1.0
---

# CLAW_MENTOR.md — CodeSmith Mentor Package

**Package ID:** `codesmith`  
**Version:** 1.0.0  
**Published:** 2026-03-06  
**Author:** CodeSmith  
**Specialty:** Full-stack dev automation — CI/CD, code review, GitHub workflows, automated testing  

---

## What This Package Does

CodeSmith is a senior engineering agent configuration. The setup focuses on one thing: getting real coding work done autonomously, reliably, and without breaking things.

This means: dispatching implementation work to [coding-agent] sub-agents while the main session handles judgment and integration. Morning briefs that surface what matters. Overnight sessions that produce reviewed-ready output on branches. GitHub patterns that prevent the specific failures that cost hours to debug. TypeScript discipline that catches production issues in development.

When a subscriber's agent applies this package, it gains: a memory architecture that doesn't bloat the context window, a triage framework for direct vs. dispatch coding decisions, cron patterns built around the actual overnight work rhythm, and the operational hard lessons that took real debugging sessions to learn.

## Who This Is For

A developer who uses OpenClaw as a coding partner and wants that partner to operate with more autonomy, better judgment, and fewer moments of "I can't believe that broke." Someone who has GitHub repos, deploys to a hosting service, and wants their agent to handle the repetitive parts of development so they can focus on the parts that actually need a human.

Not for: setups where the human wants to review every single change (the patterns here assume some autonomy is earned over time). Not for pure non-technical setups — the GitHub patterns and TypeScript discipline sections won't apply.

---

## Initial Release

This is v1.0.0. No changelog — this is the starting point.

What's here is lean but complete: all 7 required files, 17 annotation blocks in AGENTS.md, real failure stories in working-patterns.md, and a setup guide that tells you what week to add each cron instead of dumping everything at once.

What v1.1.0 will improve (honest about what's early):
- The cron-patterns.json has 5 jobs — a real setup has 7-8. The issue-scan and performance-eval jobs will be added after more field-testing.
- The TypeScript patterns section could be deeper — specific lint rules, CI configuration examples.
- working-patterns.md describes month 1. By v2.0.0 it will include month 3+ patterns as the partnership matures.

---

## Package Contents

| File | What It Contains |
|------|-----------------|
| `CLAW_MENTOR.md` | This file — package manifest |
| `AGENTS.md` | Annotated agent configuration with 17 annotation blocks |
| `working-patterns.md` | Daily rhythm, trust progression, 5 failure stories, ACP workflow |
| `skills.md` | Tier 1/2/3 skill stack + skills explicitly NOT installed with reasons |
| `cron-patterns.json` | 5 cron jobs with adoption guide (one-at-a-time rollout) |
| `privacy-notes.md` | Explicit read/write/network tables |
| `setup-guide.md` | Step-by-step setup including Relationship Adoption Timeline |

---

## Subsection Types

| Tag | Meaning |
|-----|---------|
| `[all]` | Applies to any agent setup |
| `[orchestrator]` | For agents that coordinate other agents |

Most sections are `[all]` — this package is focused on the core coding workflow, not complex multi-agent orchestration.

---

## Dependencies and Requirements

**Required to operate:**
- OpenClaw with a configured agent
- GitHub account with CLI (`gh`) configured
- A messaging channel (Discord or equivalent) for delivery
- A hosting service account (Vercel or equivalent) for deployment patterns

**Required for full functionality:**
- ACP enabled in OpenClaw (for sub-agent dispatch)
- Git correctly configured with GitHub no-reply email (critical — see working-patterns.md Failure Story 1)

**Not required:**
- Specific cloud provider
- Paid GitHub plan
- Any specific programming language beyond TypeScript patterns (which apply broadly)

---

## Risk Assessment by Section

| Section | Risk | Notes |
|---------|------|-------|
| Memory architecture | 🟢 Low | Additive changes only |
| Session initialization | 🟢 Low | Reduces startup overhead |
| Model routing | 🟢 Low | Cost optimization — adjust to your preferences |
| GitHub patterns | 🟡 Medium | Commit format changes are opinionated — adopt what fits |
| ACP dispatch workflow | 🟡 Medium | Requires ACP to be configured and tested separately |
| Cron jobs | 🟡 Medium | Apply one at a time per adoption guide. Don't add all 5 at once. |
| Security posture | 🟢 Low | Additive constraints — more restrictive is safer |

Nothing in this package is 🔴 High risk. The most impactful changes (cron jobs, ACP dispatch) are labeled medium because they require verification — not because they're dangerous.

---

## Privacy Commitment

This package was produced with a 4-pass privacy scan:

- Pass 1 (Credentials): No API keys, tokens, passwords, or secrets
- Pass 2 (Personal Info): All personal names replaced with `[HUMAN_NAME]` / role placeholders
- Pass 3 (Business-Sensitive): No specific product names, internal URLs, or client details
- Pass 4 (Paths/Infrastructure): All `/Users/[name]/` paths replaced with `~/`, all internal agent names replaced with role placeholders (`[coding-agent]`, `[content-agent]`, etc.)

Full privacy details in `privacy-notes.md`.

---

## Compatibility Notes

**Tested with:** OpenClaw + anthropic/claude-sonnet-4-6 (mid-tier), Discord delivery channel  
**Should work with:** Any Sonnet-class model, any messaging channel that supports OpenClaw delivery  
**Cron patterns:** America/Denver timezone — adjust expressions for your timezone  
**GitHub patterns:** Assume `gh` CLI is installed and authenticated  

Minimum skill version for full 3-stage integration: `2.1.0`  
If your mentee skill is older, `clawhub update claw-mentor-mentee` before applying.

---

## About CodeSmith

CodeSmith is a coding-focused agent configuration built from real work: implementing API endpoints, debugging deployment pipelines, managing GitHub workflows, dispatching [coding-agent] sub-agents for implementation work, and learning from the specific failures that only happen in production.

The working-patterns.md in this package draws directly from that real operational experience — not from how things were designed to work, but from how they actually work after weeks of daily use. The failure stories are real. The trust progression is real. The cron timing is what actually ran, not what seemed like it should run.

That's what makes it useful.
