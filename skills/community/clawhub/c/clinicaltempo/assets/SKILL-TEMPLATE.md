# Skill templates (Clinical Tempo / ClawHub)

Fork **this** skill or scaffold with **`scripts/extract-skill.sh`**. Follow the [Agent Skills](https://agentskills.io/specification) convention: YAML frontmatter, **`SKILL.md`** entry, no secrets.

---

## Full `SKILL.md` skeleton

```markdown
---
name: your-skill-slug
description: >-
  One paragraph: product, when to use, concrete triggers (like self-improving-agent),
  key paths (e.g. llm-full.txt, CLAWHUB.md), and out-of-repo links.
metadata: {}
---

# Your skill title

## Quick reference

| Situation | Action |
| --- | --- |
| … | … |

## OpenClaw / ClawHub

- Install: see your README; publish zip to [clawhub.ai](https://clawhub.ai/)
- Optional `_meta.json`: copy `_meta.sample.json` after publish

## Repository map

…

## Best practices

…

## Files in this package

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Entry |
| `README.md` | Manifest + publish notes |
| `references/` | Deep dives |
| `assets/` | Templates |
| `scripts/` | Helpers |
| `hooks/openclaw/` | Optional OpenClaw hook |

## See also

- Reference implementation: **Clinical Tempo** `.cursor/skills/clawhub/`
```

---

## Minimal skeleton

```markdown
---
name: your-skill-slug
description: "What this does and when to activate."
metadata: {}
---

# Title

## Quick reference

| Situation | Action |
| --- | --- |
| … | … |

## Solution

…
```

---

## Naming

- **Slug:** lowercase, hyphens (`clinicaltempo-clawhub`, `api-timeout-patterns`)
- **Description:** lead with triggers (“Use when: (1) … (2) …”)

---

## Extraction checklist

- [ ] `description` lists **triggers** and **files**
- [ ] Quick reference table is actionable
- [ ] No secrets; env names only from **`.env.example`**
- [ ] `README.md` explains zip layout for ClawHub upload
