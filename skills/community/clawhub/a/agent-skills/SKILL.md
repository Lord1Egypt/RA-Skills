---
name: agent-skills
description: Agent Skills standard reference guide. Covers SKILL.md specification format, progressive loading, skill discovery and activation, authoring best practices, quality evaluation, description optimization, and more. 
---

# Agent Skills Standard

> A standardized way to equip AI Agents with new capabilities and domain expertise. Adopted by 35+ Agent products.

## Use Cases

Use when creating new skills, validating skill formats, optimizing existing skills, or learning about standardized skill system design.

## Reference File Routing

| Need | Read |
|------|------|
| Quick skill creation (5-step guide) | [quick-start.md](references/quick-start.md) |
| SKILL.md format spec + Agent integration | [spec.md](references/spec.md) |
| Authoring best practices + quality eval + description optimization | [authoring.md](references/authoring.md) |
| Common anti-patterns and fixes | [anti-patterns.md](references/anti-patterns.md) |
| Script binding and design | [using-scripts.md](references/using-scripts.md) |
| Supported product list | [products.md](references/products.md) |

## Minimal Example

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
---

## Workflow
1. Extract: `python scripts/extract.py input.pdf`
2. Fill: `python scripts/fill.py template.pdf data.json`

## Gotchas
- Scanned PDFs need OCR first — use `scripts/ocr.py`
```

## Validation

```bash
skills-ref validate ./my-skill
```
