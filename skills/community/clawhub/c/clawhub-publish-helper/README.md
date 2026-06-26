# Publish Skill

An OpenClaw skill that guides the process of preparing and publishing skills to [ClawHub](https://clawhub.ai).

## What It Does

Walks through the complete publish workflow:
1. **Audit** the live skill for secrets, PII, and hardcoded values
2. **Create** a separate publishable copy (never modifies the live skill)
3. **Generalize** all content (env vars, generic config, no personal data)
4. **Verify** clean state with grep-based scanning
5. **Git init** and commit
6. **Publish** to ClawHub with confirmation

## Setup

Install into your OpenClaw workspace and reference when you need to publish a skill.

## Usage

Just say "publish this skill" or "prepare for publishing" and follow the workflow in SKILL.md.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full workflow instructions |
| `references/checklist.md` | Quick audit checklist |
| `README.md` | This file |

## License

MIT-0
