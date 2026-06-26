# Skill Health Monitor

> Automated health checks for your agent skill collection

## Purpose

Audit, score, and maintain the health of your AI agent skills. Catch rotting skills, missing files, broken triggers, and outdated content before they cause silent failures.

## When to Use

- "check skill health", "audit my skills", "skill inventory"
- Periodic maintenance (weekly/monthly)
- Before adding new skills to a collection
- When agents start behaving unexpectedly

## Health Score Dimensions (0-100 each)

### 1. Structure (25%)
- [ ] Has SKILL.md or equivalent config file
- [ ] Has README.md with usage instructions
- [ ] File structure follows agent skill conventions
- [ ] No orphaned or dangling file references

### 2. Content (25%)
- [ ] Description is clear and specific (not vague)
- [ ] Trigger words/phrases are defined
- [ ] Examples are provided
- [ ] Edge cases and failure modes documented

### 3. Activity (20%)
- [ ] Updated within last 30 days
- [ ] Commit history shows maintenance
- [ ] Issues/PRs are addressed
- [ ] Dependencies are current

### 4. Compatibility (15%)
- [ ] Works with current agent framework version
- [ ] No deprecated API usage
- [ ] Cross-platform tested (if applicable)
- [ ] Dependencies listed and version-pinned

### 5. Discoverability (15%)
- [ ] Has relevant topics/tags
- [ ] Description contains searchable keywords
- [ ] Listed in skill directories
- [ ] README has quick-start section

## Health Rating

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | 🟢 Healthy | Maintain |
| 70-89  | 🟡 Needs Attention | Minor fixes |
| 50-69  | 🟠 Degrading | Schedule update |
| 0-49   | 🔴 Critical | Rewrite or retire |

## Audit Commands

```bash
# Check single skill directory
check-skill-health ./path/to/skill

# Scan entire skill collection
scan-skills ./skills/ --report=health-report.md

# Compare health over time
skill-health diff --baseline=health-report-2026-03.md --current=health-report-2026-04.md
```

## Quick Audit Checklist

Run this on each skill:

1. `cat SKILL.md` — Does it exist? Is the description clear?
2. `grep -r "TODO\|FIXME\|HACK"` — Any technical debt markers?
3. `git log --since="30 days ago" --oneline` — Any recent activity?
4. `grep -i "trigger\|when to use\|example"` SKILL.md — Are triggers and examples defined?
5. Check for hard-coded paths, URLs, or deprecated tool names

## Report Format

```markdown
## Skill Health Report — 2026-04-22

### Summary
- Total skills: 16
- 🟢 Healthy: 8 (50%)
- 🟡 Needs Attention: 5 (31%)
- 🟠 Degrading: 2 (13%)
- 🔴 Critical: 1 (6%)
- Average score: 74/100

### Issues Found
1. **prompt-guard** (🔴 35/100) — Missing README, no trigger words
2. **evr-framework** (🟠 55/100) — SKILL.md only, no examples
3. ...
```

## Anti-Patterns to Watch

- ❌ "Good skill" with no evidence of testing
- ❌ Skills that duplicate existing functionality
- ❌ Over-engineered skills with 50+ rules nobody follows
- ❌ Skills referencing removed or renamed tools
- ❌ Copy-pasted descriptions that don't match content

## License

MIT
