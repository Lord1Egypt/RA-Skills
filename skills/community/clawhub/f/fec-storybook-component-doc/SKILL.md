---
name: fec-storybook-component-doc
description: Use when setting up or reviewing Storybook component documentation, design-system presentation, isolated component state previews, stories, addons, decorators, MDX docs, component-state interaction checks, visual baselines, or Chromatic. For real-browser cross-page journeys or broader coverage planning, choose the matching testing workflow first; Chinese triggers include Storybook, component documentation, Design System, visual regression.
---

# Storybook component documentation

## Purpose

Establish documentation, design system display and isolated state preview environment for UI components; interaction and visual testing only cover component states within the Storybook scene.

## Procedure

1. Initialize or identify an existing Storybook configuration, inheriting the project framework adapter, stories globs, themes, and build commands.
2. Each component's Story covers default state, main variant, size, semantic tone, disabled, loading, error, empty, selected, invalid and key edge states.
3. Components that rely on Router, Store, i18n, and ThemeProvider are wrapped with decorators and do not copy the application entry in Story.
4. Use MDX to supplement complex components with usage instructions, Props, slots/children, variant matrices, status examples, accessibility requirements and source code display.
5. When automation is required, connect interaction tests, addon-a11y, Chromatic or Storybook Test Runner; these capabilities serve component documentation and design system display and do not undertake cross-page business journeys.
6. Design system components should record token sources, Tailwind/class variants, dark modes, responsive sizes, and unsupported combinations to avoid consumers guessing at assembly.

## Detailed reference

- Load [references/story-patterns.md](references/story-patterns.md) when you need `main.ts`, `preview.ts`, stories, decorators, MDX, interaction tests and visual regression examples.

## Constraints

- Story needs to be updated synchronously with component prop changes.
- Provider dependencies must be completed through decorators.
- Storybook build product `storybook-static/` should not be committed to Git.
- Storybook is used for development and component documentation and is not a replacement for production page SEO.
- Storybook visual baseline for component state; cross-page screenshots and real routing processes are offloaded to E2E workflow.
- Large component libraries need to control stories glob and addon overhead.
- Don’t use Storybook to hide component API issues; if variant combinations explode, you should first converge component responsibilities or split components.

## Expected Output

Interactive component documentation and design system showcase site with isolated previews of each component state, Props tables to generate, and key Storybook scenes with optional play testing or visual regression baselines.
