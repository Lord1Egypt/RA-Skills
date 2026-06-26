# Skill Design Patterns

## Anatomy of a Great Skill

### Frontmatter (Required)

```yaml
---
name: skill-name
description: Clear description of what AND when. This is the PRIMARY triggering mechanism.
---
```

**Description should include:**
- What the skill does
- Specific triggers (file types, query patterns, languages)
- Edge cases it handles

### Body Structure

1. **Quick Start** — Minimal example to get going
2. **Core Workflow** — Step-by-step process
3. **Details** — Progressive disclosure with links to references/

## Freedom Levels

| Level | When to Use |
|-------|-------------|
| High (text) | Multiple valid approaches, context-dependent |
| Medium (pseudocode) | Preferred pattern exists, some variation OK |
| Low (script) | Fragile operations, consistency critical |

## Progressive Disclosure

```
SKILL.md (<500 lines)
├── Core workflow
└── "See REFERENCES/xxx.md for details"

references/
├── xxx.md  (loaded on demand)
├── yyy.md
└── zzz.md
```

## Common Patterns

### Pattern 1: High-level + References

```markdown
# PDF Processing

## Quick Start

[basic example]

## Advanced

See [FORMS.md](references/FORMS.md) for form filling.
```

### Pattern 2: Multi-Domain

```
bigquery/
├── SKILL.md (overview)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Conditional Details

```markdown
## Simple Edits

Modify XML directly.

**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
```
