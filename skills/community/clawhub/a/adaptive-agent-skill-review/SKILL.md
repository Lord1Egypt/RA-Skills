---
name: skill-review
description: |
  Review all skills for staleness, missing gotchas, and improvement opportunities.
  Run periodically or after a series of tasks to keep procedural memory accurate.
  Trigger words: "review skills", "skill audit", "check skills", "skill maintenance".
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# Skill Review

Periodic review of all skills to keep procedural memory accurate and up-to-date.

## When to Run

- After completing a batch of tasks across multiple skills
- When you notice a skill has outdated steps or missing context
- Proactively every ~2 weeks as maintenance

## Step 1: Inventory

List all skills and their last-modified dates:

```bash
for d in skills/*/SKILL.md; do echo "$(stat -f '%Sm' -t '%Y-%m-%d' "$d" 2>/dev/null || date -r "$d" '+%Y-%m-%d') $d"; done | sort -r
```

Read each `SKILL.md` briefly (first 30 lines) to understand scope.

## Step 2: Cross-Reference with Memory

Check memory files and `shared/gotchas.md` (if they exist) for lessons that should have flowed into skills but didn't.

For each gotcha or feedback memory:
- Does it relate to a specific skill?
- Is that lesson already captured in the skill's steps or `## Gotchas` section?
- If not, patch the skill

## Step 3: Check for Staleness

For each skill, check:

| Check | How |
|-------|-----|
| References valid paths? | Grep for file paths mentioned in SKILL.md, verify they exist |
| References valid commands? | Check if CLI tools or scripts mentioned still work |
| Steps still accurate? | Compare with actual workflow from recent git history |
| Gotchas section exists? | If skill has been used multiple times, it should have accumulated lessons |

## Step 4: Check for Gaps

Look for recurring multi-step patterns that don't have a skill yet:

```bash
git log --oneline -30
```

If a workflow has been done 3+ times manually, propose creating a skill for it.

## Step 5: Consolidate Duplicates

Check for skills with overlapping scope. If two skills cover similar ground, propose merging or clarifying boundaries.

## Step 6: Report

Output a summary table:

```
| Skill | Status | Action Taken |
|-------|--------|-------------|
| /typefully | Updated | Added gotcha about image requirements |
| /codebase | OK | No changes needed |
| /deploy-flow | NEW | Created from repeated manual workflow |
```

## Key Rules

- **Read before edit** — never patch a skill you haven't read
- **Minimal patches** — only change what's wrong or missing, don't restructure working skills
- **Preserve voice** — each skill has its own style; don't homogenize
- **Commit after** — stage and commit all skill changes with `chore: skill-review — update N skills`
