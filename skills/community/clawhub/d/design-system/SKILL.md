---
name: Design System
slug: design-system
version: 1.0.0
homepage: https://clawic.com/skills/design-system
description: Build design systems with tokens, components, and documentation that scale across teams and products.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines. All preferences are stored in `~/design-system/memory.md`.

## When to Use

User needs to create, maintain, or extend a design system. Agent handles token architecture, component patterns, documentation structure, and cross-platform consistency.

## Architecture

Memory lives in `~/design-system/`. See `memory-template.md` for structure.

```
~/design-system/
├── memory.md         # Status + context + decisions
└── tokens/           # Token definitions if exported
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |

## Core Rules

### 1. Tokens First, Components Second

Design tokens are the foundation. Before building any component:
- Define color tokens (semantic, not raw hex)
- Define spacing scale (consistent multiplier)
- Define typography scale (modular)

Components consume tokens. Never hardcode values.

### 2. Semantic Over Literal Naming

| Bad | Good |
|-----|------|
| `blue-500` | `primary` |
| `14px` | `text-sm` |
| `8px` | `space-2` |

Semantic names survive rebrand. Literal names break everything.

### 3. Three-Tier Token Architecture

```
Primitive → Semantic → Component
   ↓           ↓          ↓
 gray-900   text-primary  button-text
```

- **Primitive**: Raw values (colors, sizes)
- **Semantic**: Meaning-based (primary, danger, muted)
- **Component**: Specific use (button-bg, card-border)

### 4. Document Decisions, Not Just Specs

Every token and component needs:
- **What**: The value or pattern
- **When**: Usage context
- **Why**: The decision behind it
- **When NOT**: Anti-patterns to avoid

### 5. Platform-Agnostic Source of Truth

Design tokens should export to:
- CSS custom properties
- Tailwind config
- iOS/Android native
- Figma variables

One source, many outputs. Use Style Dictionary or similar.

### 6. Component API Consistency

All components follow the same patterns:
- Same prop naming (`variant`, `size`, `disabled`)
- Same size scale (`sm`, `md`, `lg`)
- Same variant names (`primary`, `secondary`, `ghost`)

Predictability beats cleverness.

### 7. Versioning and Migration

Breaking changes need:
- Version bump (semver)
- Migration guide
- Deprecation warnings before removal
- Codemods when possible

## Common Traps

- **Premature abstraction** → Build 3 instances before extracting a pattern
- **Token explosion** → 50 grays is not a system, it is chaos
- **Skipping documentation** → Undocumented patterns get reimplemented wrong
- **Designing for edge cases first** → Cover 80% well before 100% poorly
- **No dark mode strategy** → Retrofit is 10x harder than planning upfront
- **Inconsistent spacing** → Use a scale (4px base), not arbitrary values
- **Component prop sprawl** → More than 10 props means split the component

## Security & Privacy

**Data that stays local:**
- Design decisions in ~/design-system/
- Token definitions and component specs

**This skill does NOT:**
- Access files outside ~/design-system/
- Make network requests
- Store sensitive data

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `css` — Styling fundamentals
- `tailwindcss` — Utility-first CSS
- `frontend` — Frontend development
- `ui` — User interface patterns
- `design` — Design principles

## Feedback

- If useful: `clawhub star design-system`
- Stay updated: `clawhub sync`
