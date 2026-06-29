# 5 Steps to Create a Skill

## 1. Create Directory

```bash
mkdir -p my-skill/references
```

Directory name = skill name, kebab-case. Prefer verb-noun phrases (`pdf-processing`, `weather-check`).

## 2. Write SKILL.md

```markdown
---
name: my-skill
description: What it does + when to trigger. Use when...
---

## Workflow
1. First step
2. Second step

## Gotchas
- Common pitfalls
```

`description` determines trigger accuracy — clearly state "what" and "when".

## 3. Split Large Files

Body > 500 lines → split to `references/`, keep skeleton + routing table in main file:

```markdown
| Need | Read |
|------|------|
| Detailed API reference | [references/api.md](references/api.md) |
```

## 4. Add Resources (Optional)

- `scripts/` — executable scripts the Agent can call directly
- `assets/` — templates, config files

Scripts should be self-contained with clear I/O interfaces.

## 5. Validate

```bash
skills-ref validate ./my-skill
```

---

Next: [spec.md](spec.md) — Format spec | [authoring.md](authoring.md) — Authoring guide
