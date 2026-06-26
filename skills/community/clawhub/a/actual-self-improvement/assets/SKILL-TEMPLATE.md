# Skill Template

Use this when promoting a proven learning into a standalone Agent Skill.

```markdown
---
name: skill-name
description: What the skill does and when to use it. Include trigger phrases and scope boundaries.
compatibility: Optional environment requirements.
metadata:
  version: "1.0.0"
  source_learning: "LRN-YYYYMMDD-XXX"
---

# Skill Name

One-sentence statement of the problem this skill solves.

## When to use

Use this skill when:
- trigger or situation 1
- trigger or situation 2
- trigger or situation 3

Do not use it for:
- adjacent case 1
- adjacent case 2

## Workflow

1. Step one
2. Step two
3. Verify the result

## Quick commands

```bash
# preferred command or script
```

## Edge cases

- edge case 1
- edge case 2

## References

- `references/...`
- `scripts/...`

## Source

- Learning ID: LRN-YYYYMMDD-XXX
- Extraction date: YYYY-MM-DD
```

## Checklist

Before shipping a promoted skill:
- keep the description under 1024 characters
- keep `SKILL.md` under 500 lines where possible
- move long docs into `references/`
- bundle repeated logic into `scripts/`
- add trigger and output evals
