# Skill template (fork from `clawhub`)

Use this when publishing a **variant** skill (e.g. org-specific). Replace bracketed fields.

---

## `SKILL.md` skeleton

```markdown
---
name: your-skill-slug
description: >-
  One paragraph: product, when to use, key files (llm-full.txt, CLAWHUB), and out-of-repo links.
metadata: {}
---

# Your skill title

## Quick reference

| Situation | Action |
| --- | --- |
| … | … |

## Installation

/path or git clone …

## References

- `references/examples.md`
```

## Checklist

- [ ] `description` lists **concrete triggers** (like self-improving-agent).
- [ ] **Quick reference** table at top.
- [ ] **Files** table at bottom listing package paths.
- [ ] No secrets; env names only from **`.env.example`**.
