# Cognitive Debt Guard 🧠

> AI tools doubled code churn and pushed PR incident rates up 23.5%. Not because the code is bad — because teams shipped it faster than they understood it.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-green.svg)]()
[![Skill](https://img.shields.io/badge/type-agent--skill-blue.svg)]()

## The Numbers

| Metric | Impact | Source |
|--------|--------|--------|
| Incident rate per PR | **+23.5%** | Cortex 2026 Benchmark |
| Code churn | 3.1% → **5.7%** (nearly doubled) | GitClear |
| Developer speed (experienced) | **-19%** slower | METR 2025 RCT |
| Trust in AI output | **33%** | Stack Overflow 2025 |

## The Core Problem

Technical debt is code you *know* is bad. **Cognitive debt is code you don't even know is bad** — because you never fully understood it.

```
Active ✅:  Prompt → Read → Understand → Modify → Ship
            Comprehension maintained ✓

Passive ❌: Prompt → Accept → Ship → Forget
            Cognitive debt accumulates ✗
```

The scary part: cognitive debt is invisible. Your codebase looks fine, tests pass, but **no one on the team can explain what 40% of the code does.** That's the incident spike waiting to happen.

## 5 Patterns That Prevent Cognitive Debt

### 1. 📝 Maintain MEMORY.md

Living architecture context — for humans and AI agents.

```markdown
# MEMORY.md — Project Knowledge

## Architecture
- Auth: JWT tokens, refresh in /api/auth/refresh
- DB: PostgreSQL, migrations in db/migrate/
- Queue: Redis + Bull, workers in src/workers/

## Critical Paths (know these cold)
- Payment flow: cart → stripe → webhook → order
- Auth flow: login → JWT → refresh → logout

## AI-Generated Code Zones
- src/utils/ — LLM-generated helpers (high cognitive debt risk)
- src/api/ — Human-reviewed, well-understood
```

### 2. 🚦 Comprehension Gate

3 questions before accepting AI-generated code:

```
1. Can I explain what this code does?     → If NO → STOP. Read it.
2. Can I trace the data flow?             → If NO → STOP. Map it.
3. If this breaks, would I know where?    → If NO → STOP. Add logging.
```

### 3. 🤝 Pair with Agents, Don't Delegate

```
❌ Bad:  "Write the auth module" → Accept 500 lines → Ship
✅ Good: "Write the auth module" → Read every line → Rewrite unclear parts → Ship
```

Rule: **Never accept >50 lines of AI code without reading every line.**

### 4. 💥 Shrink the Blast Radius

| Rule | Limit | Why |
|------|-------|-----|
| Max lines per AI PR | 200 | Easier to understand |
| Concerns per PR | 1 | Isolate changes |
| Test coverage on AI paths | 100% | Catch what you didn't understand |

### 5. 📅 Quarterly Comprehension Audit

90-minute ceremony every quarter:
1. Identify AI-heaviest PRs from last quarter
2. For each: Can the author explain it? Can someone else?
3. Flag code no one understands → refactor or rewrite
4. Update MEMORY.md with findings

## Code Review Framework (5 Layers)

```
Layer 1: Comprehension   → Can I understand this?
Layer 2: Correctness     → Does it do what it claims?
Layer 3: Integration     → Fits existing patterns?
Layer 4: Security        → AI-free zones respected?
Layer 5: Maintainability → Will I understand this in 6 months?
```

## AI-Free Zones

Some code paths are too consequential for cognitive debt. AI may **draft**, but a human must **own, understand, and rewrite**:

- 🔒 Authentication & authorization
- 🔒 Payment processing
- 🔒 Data deletion (compliance/legal)
- 🔒 Database migrations (irreversible)
- 🔒 Security-critical paths

## Quick Start

```bash
# Claude Code
cp SKILL.md .claude/skills/cognitive-debt-guard/

# OpenClaw
cp SKILL.md ~/.openclaw/workspace/skills/cognitive-debt-guard/

# Cursor
cp SKILL.md .cursor/rules/cognitive-debt-guard.mdc
```

## What's Included

- **SKILL.md** — Complete framework with comprehension gates and review rules
- **DEBT_INDICATORS.md** — 11K+ word reference of cognitive debt patterns and anti-patterns

## Works With

- [OpenClaw](https://openclaw.ai)
- Claude Code
- Cursor
- Codex
- Any agent framework

## Related Skills

| Skill | Purpose |
|-------|---------|
| [Prompt Guard](https://github.com/aptratcn/prompt-guard) | Block prompt injection attacks |
| [Error Recovery](https://github.com/aptratcn/skill-error-recovery) | Systematic error handling |
| [EVR Framework](https://github.com/aptratcn/evr-framework) | Verify completions before claiming done |
| [Systematic Debugging](https://github.com/aptratcn/systematic-debugging) | When cognitive debt causes incidents |

## License

MIT — Understand before you ship.
