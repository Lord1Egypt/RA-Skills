# AGENTS.md - Cerebro-First Skill

## Purpose

Operational guardrail skill to enforce Cerebro-first execution and continuity.

## Current Version

- `2.1.0` (working version in local workspace)

## Pre-Publish Checklist

1. Ensure `SKILL.md` frontmatter has `version: 2.1` or newer
2. Verify references exist:
   - `references/cerebro-index-v2.1.md`
   - `references/domain-routing-v2.1.md`
3. Confirm README acceptance checklist is accurate
4. Update changelog text in release notes/commit message

## GitHub Push (if repo exists)

```bash
cd <path-to-your-skill>/cerebro-first
git add -A
git commit -m "cerebro-first: v2.1 retrieval + domain router"
git push
```

## ClawHub Publish Template

```bash
clawhub publish <path-to-your-skill>/cerebro-first \
  --slug cerebro-first \
  --name "Cerebro-First" \
  --version 2.1.0 \
  --changelog "v2.1: added lightweight retrieval index, domain router matrix, and explicit write-back/output requirements"
```

## Post-Publish Verification

1. Run: `clawhub info cerebro-first` (or equivalent lookup)
2. Confirm version and changelog are visible
3. Save publish proof (command output) to daily memory note
