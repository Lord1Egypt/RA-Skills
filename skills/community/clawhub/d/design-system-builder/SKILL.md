---
name: design-system-builder
description: >
  Comprehensive guide for building enterprise-grade component libraries and design systems from scratch.
  Use this skill when a frontend engineer needs to: (1) set up a component library monorepo with build tooling,
  (2) establish a Design Token system (colors, typography, spacing, shadows), (3) define component development
  standards (naming, Props API, TypeScript types, documentation), (4) configure Storybook for interactive docs,
  (5) implement a theme system with dark mode support, (6) plan component testing strategy (visual regression,
  interaction tests), or (7) set up a release pipeline (versioning, changelog, npm publishing).
  Primary stack: React + TypeScript. Also covers Vue 3 patterns where applicable.
---

# Design System Builder

A structured guide for building production-ready component libraries and design systems. Covers architecture,
tokens, components, documentation, theming, testing, and publishing.

## Quick Decision Map

| Goal | Start here |
|---|---|
| Set up monorepo + build | [Architecture](#1-architecture--monorepo-setup) |
| Define design tokens | [references/tokens.md](references/tokens.md) |
| Build components | [references/component-patterns.md](references/component-patterns.md) |
| Storybook setup | [references/storybook-setup.md](references/storybook-setup.md) |
| Theming / dark mode | [references/theming.md](references/theming.md) |
| Testing strategy | [references/testing-strategy.md](references/testing-strategy.md) |
| Release pipeline | [references/release-pipeline.md](references/release-pipeline.md) |

---

## 1. Architecture & Monorepo Setup

### Recommended Structure

Use **pnpm workspaces** + **Turborepo** for monorepo management.

```
my-design-system/
├── packages/
│   ├── tokens/          # Design tokens (CSS vars, JS objects)
│   ├── icons/           # SVG icon components
│   ├── components/      # Core UI components
│   ├── themes/          # Theme definitions
│   └── utils/           # Shared utilities (cn, clsx, etc.)
├── apps/
│   └── docs/            # Storybook documentation site
├── package.json         # Root workspace config
├── pnpm-workspace.yaml
├── turbo.json
└── tsconfig.base.json
```

### Bootstrap Commands

```bash
# Initialize monorepo
mkdir my-design-system && cd my-design-system
pnpm init
pnpm add -D turbo -w

# Create workspace config
echo "packages:\n  - 'packages/*'\n  - 'apps/*'" > pnpm-workspace.yaml
```

**`turbo.json`** — task pipeline:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "dev": { "cache": false, "persistent": true },
    "test": { "dependsOn": ["^build"] },
    "lint": {}
  }
}
```

### Build Tooling Choice

| Tool | Best for | Notes |
|---|---|---|
| **Vite + vite-plugin-dts** | React/Vue components | Fast, ESM-first |
| **tsup** | Utility packages | Zero-config, dual CJS/ESM |
| **Rollup** | Fine-grained control | More config overhead |

**Recommended `packages/components/package.json`:**

```json
{
  "name": "@myds/components",
  "version": "0.1.0",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch"
  }
}
```

---

## 2. Design Tokens

Design tokens are the single source of truth for visual decisions.

> **Read [references/tokens.md](references/tokens.md)** for the complete token schema, naming conventions,
> CSS variable patterns, and multi-brand token examples.

### Quick Start

```bash
# Install Style Dictionary (token transformation tool)
pnpm add -D style-dictionary -w
```

Token files live in `packages/tokens/src/`. Style Dictionary transforms them to CSS variables, JS/TS constants,
and platform-specific outputs (iOS, Android).

Core token categories: `color`, `typography`, `spacing`, `border-radius`, `shadow`, `z-index`, `motion`.

---

## 3. Component Development Standards

Every component should follow consistent conventions for long-term maintainability.

> **Read [references/component-patterns.md](references/component-patterns.md)** for detailed patterns:
> file structure, Props API design, compound components, polymorphic components, accessibility requirements,
> and documentation templates.

### Non-Negotiable Rules

1. **TypeScript first** — all props typed with explicit interfaces, no `any`
2. **`forwardRef`** for all leaf elements (React)
3. **`aria-*` attributes** — never ship an inaccessible component
4. **Controlled + Uncontrolled** — support both patterns for form components
5. **`data-testid`** — include for E2E testability

### Component File Structure

```
Button/
├── Button.tsx          # Component implementation
├── Button.types.ts     # Props interface & type exports
├── Button.test.tsx     # Unit + interaction tests
├── Button.stories.tsx  # Storybook stories
└── index.ts            # Public barrel export
```

---

## 4. Storybook

Storybook is the primary documentation and development environment.

> **Read [references/storybook-setup.md](references/storybook-setup.md)** for full configuration:
> addon setup, autodocs, MDX pages, controls, theming the Storybook UI, and deployment.

### Bootstrap

```bash
cd apps/docs
pnpm dlx storybook@latest init
# Select React + Vite when prompted
```

Essential addons:
- `@storybook/addon-essentials` (controls, actions, docs, viewport)
- `@storybook/addon-a11y` (accessibility audit)
- `@storybook/addon-themes` (theme switching)
- `storybook-addon-pseudo-states` (hover/focus/active states)

---

## 5. Theme System

> **Read [references/theming.md](references/theming.md)** for full theming architecture:
> CSS custom properties strategy, dark mode implementation (media query vs. class-based),
> ThemeProvider pattern for React, and Vue 3 provide/inject approach.

### Core Concept

Tokens define **semantic aliases** that point to primitive values:

```css
/* Primitive */
--color-blue-500: #3b82f6;

/* Semantic (theme-aware) */
[data-theme="light"] { --color-primary: var(--color-blue-500); }
[data-theme="dark"]  { --color-primary: var(--color-blue-400); }
```

Components reference semantic tokens only — never primitives directly.

---

## 6. Testing Strategy

> **Read [references/testing-strategy.md](references/testing-strategy.md)** for the full pyramid:
> unit tests (Vitest), interaction tests (Testing Library), visual regression (Chromatic/Percy),
> and accessibility automation.

### Test Pyramid for Component Libraries

```
        [Visual Regression]     ← Chromatic / Percy
       [Interaction Tests]      ← @testing-library/react
      [Unit / Logic Tests]      ← Vitest
```

**Minimum bar per component:**
- Renders without errors
- Props produce expected output
- Interactive states (hover, focus, disabled) work
- No critical a11y violations (axe-core)

---

## 7. Release Pipeline

> **Read [references/release-pipeline.md](references/release-pipeline.md)** for the complete release flow:
> Changesets setup, versioning strategy, automated changelog, CI/CD pipeline, and npm publishing.

### Tool: Changesets

```bash
pnpm add -D @changesets/cli -w
pnpm changeset init
```

Workflow:
1. `pnpm changeset` — create a changeset (describe changes)
2. `pnpm changeset version` — bump versions + update CHANGELOG.md
3. `pnpm changeset publish` — publish to npm

---

## Vue 3 Notes

Most patterns apply to Vue 3 with minor adaptations:
- Props: use `defineProps<T>()` with TypeScript generics
- `expose()` replaces React's `forwardRef`
- Theme injection: `provide/inject` replaces React Context
- Testing: `@vue/test-utils` + Vitest
- See [references/component-patterns.md](references/component-patterns.md) for Vue-specific examples

---

## Recommended Tech Stack Summary

| Layer | React | Vue 3 |
|---|---|---|
| Monorepo | pnpm + Turborepo | pnpm + Turborepo |
| Build | tsup / Vite | tsup / Vite |
| Tokens | Style Dictionary | Style Dictionary |
| Docs | Storybook 8 | Storybook 8 |
| Unit tests | Vitest + Testing Library | Vitest + @vue/test-utils |
| Visual regression | Chromatic | Chromatic |
| Release | Changesets | Changesets |
| CSS | CSS Modules / CSS-in-JS | CSS Modules / scoped SFC |
