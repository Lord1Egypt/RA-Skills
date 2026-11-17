---
name: fec-legacy-to-modern-migration
description: Use when planning or implementing an intentional migration from JavaScript, jQuery, HTML/CSS, server-rendered templates, MPA legacy frontend code, or older framework code toward a modern frontend stack while preserving behavior. Do not use for routine legacy bug fixes that stay in the old stack; Chinese triggers include legacy projects, technology stack upgrades, jQuery migration.
---

# Migration from traditional front-end to modern framework

Suitable for scenarios where you are gradually migrating JavaScript + jQuery + HTML/CSS multi-page applications (MPA), server-side template rendering projects, or legacy framework code to React, Vue, Next.js, Nuxt, TypeScript, or retaining MPA form but modernizing modules, builds, types, and tests.

## Purpose

Guide the gradual migration of traditional front-end projects to the target modern stack, provide migration strategies, concept mapping, phased steps and implementation constraints to ensure functional equivalence and controllable risks.

## Procedure

1. First identify the target stack, migration boundaries and whether to retain the MPA/server template form.
2. Load [references/migration-strategy-and-mapping.md](references/migration-strategy-and-mapping.md), select a progressive or one-time rewrite strategy, and clarify the mapping of legacy patterns to the target stack.
3. Load [references/migration-execution-checklist.md](references/migration-execution-checklist.md) to complete inventory inventory, dependency analysis, prioritization and phased migration plan.
4. When writing a migration analysis or migration plan report, load [references/migration-report-template.md](references/migration-report-template.md).
5. Advance in the order of preparation, base layer, module/page migration, and closing, migrating one verifiable unit at a time.
6. Each migration unit verifies functional equivalence, visual consistency, type safety, accessibility, i18n, resource and style boundaries.

## Constraints

- Before migration, a migration analysis report must be output to clarify strategies, priorities and risks.
- Do not change the architecture, UI, and interfaces at the same time in one migration.
- Prioritize functional equivalence before considering optimization and modernization.
- Keep the old system operational during the migration process to avoid a big bang rollout.
- When there is no ready replacement for the jQuery plug-in, you can temporarily embed it using iframe or micro-front-end and wait for subsequent replacement.
- The target stack first identifies React/Vue/Next/Nuxt, modern MPA or partial modernization targets, and does not force the change to SPA by default.
- Images use original project resources; the icon system prefers to use the original project or target project specifications; inline SVG exceptions must have accessibility, componentization or maintenance reasons.
- The style refers to the original project effect but does not copy CSS. The target project style system is preferred; inline style exceptions must be local and interpretable.
- The goal is to have consistent visuals and interactions, make the code simpler and easier to maintain, and business functions must not be missing.
- For migrations involving pages, components, routing, forms, pop-ups, navigation or key user processes, a list of behaviors before and after refactoring must be established, and the critical paths must be compared and verified using Playwright or an equivalent real browser verification method.
- For visually sensitive pages, screenshot comparison or manual screenshot acceptance should be supplemented; dynamic content, animation, fonts and environmental differences need to be clearly blocked, stabilized or explained.
- For pure logic, type, build or UI-less migrations, Playwright is not forced and a validation layer closer to risk should be chosen: type-check, unit test, component test, build or lint.
- The verification goal is not to be completely consistent at the pixel level, but to confirm that there are no missing business functions, key interactions are equivalent, there are no unexpected deviations in the main visual layout, and the code is clearer and maintainable than the old implementation.

## Expected Output

- The migration analysis report is saved as `reports/migration-plan-YYYY-MM-DD-HHmmss.md`, including strategy selection, inventory inventory, dependencies, phased steps, risks and rollback plans.
- The migrated business functions are completely equivalent to those of the original project, with no missing functions.
- The visuals and interactions are consistent with the original project, and there is no perceived difference for users.
- Complete type definition, no `any` abuse, unified API calls and type safety.
- Images use original project resources, and styles enter the target project style system. Exceptions for icons and inline styles have clear reasons.
- The new code copy has been i18n, and the critical path is covered by tests.
