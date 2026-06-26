# Skill Health Monitor 🏥

> Automated health checks for your AI agent skill collection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/type-agent--skill-blue)](SKILL.md)

**Why this exists:** Most AI agent operators have 10-50 skills. Over time, skills rot — descriptions become vague, triggers stop working, dependencies drift. Silent failures follow. This skill makes maintenance systematic.

## The Problem

- ❌ No visibility into skill health across a collection
- ❌ Rotting skills cause silent agent failures
- ❌ No standard way to evaluate skill quality
- ❌ Duplicate skills waste context window space

## The Solution

A structured health scoring system with 5 dimensions:
- **Structure** (25%) — File completeness and conventions
- **Content** (25%) — Description quality and documentation
- **Activity** (20%) — Recent maintenance and updates
- **Compatibility** (15%) — Framework version alignment
- **Discoverability** (15%) — Tags, searchability, quick-start

## Quick Start

```
# Install as an agent skill
# Claude Code: Copy SKILL.md to .claude/skills/skill-health-monitor/
# Cursor: Copy SKILL.md to .cursor/rules/skill-health-monitor.mdc
# OpenClaw: Copy to ~/.openclaw/workspace/skills/skill-health-monitor/

# Then tell your agent:
"Run a health check on all my skills"
"Audit my skill collection"
"Which skills need attention?"
```

## Health Ratings

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | 🟢 Healthy | Maintain |
| 70-89  | 🟡 Needs Attention | Minor fixes |
| 50-69  | 🟠 Degrading | Schedule update |
| 0-49   | 🔴 Critical | Rewrite or retire |

## What Makes This Different

1. **Structured scoring** — Not "looks good to me" but a repeatable 100-point scale
2. **5 dimensions** — Catches both surface issues (missing README) and deep ones (outdated dependencies)
3. **Action-oriented** — Every score comes with concrete next steps
4. **Collection-aware** — Designed for managing 10+ skills, not just one
5. **Trackable** — Diff reports show improvement or degradation over time

## Works With

- [OpenClaw](https://openclaw.ai)
- Claude Code
- Cursor
- Codex
- Gemini CLI
- Any agent framework that reads skill files

## License

MIT
