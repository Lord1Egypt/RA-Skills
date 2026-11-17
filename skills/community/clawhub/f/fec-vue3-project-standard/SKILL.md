---
name: fec-vue3-project-standard
description: Use when designing or reviewing Vue 3 + TypeScript project structure, SFC/component boundaries, composables organization, route composition, Pinia ownership, API/error/styling defaults, directives, or repository-wide Vue conventions. Prefer narrower skills for forms, data fetching, tests, accessibility, virtualization, animation, or security deep dives; Chinese triggers include Vue 3 project specification, Vue component architecture.
---

# Vue 3 project specifications

For repositories using Vue 3 + TypeScript.

## Purpose

Provides project structure, component boundaries, Composables, and default implementation conventions for Vue 3 + TypeScript projects to ensure conventional development and type safety.

## Procedure

1. Identify the existing Vue conventions in the warehouse: directory, routing, Pinia, request layer, style system, component library and test framework.
2. Demarcate the boundaries between pages, business components, common components, composables, stores, services and utils.
3. Prioritize the existing automatic import/module export conventions of `<script setup lang="ts">`, composite API and warehouse.
4. Complete state ownership, API layer, error handling, style isolation and special skill offloading when outputting.
5. Pages and modules must have recoverable error UI; global `errorHandler`, `onErrorCaptured`, request error mapping and routing error page have clear division of labor.
6. Tailwind token/variant or responsive layout requirements should be diverted to corresponding special skills to avoid stuffing style system rules into Vue component specifications.
7. When the state ownership is complex, first make a state list; when the boundaries of DTO, public props, generic composable or `tsconfig` are complex, first use the TypeScript project specification process to converge cross-framework type contracts.
8. When designing reusable composables, clarify whether the input supports plain value, ref, computed or getter; when testing Vue components, cover the common boundaries of Pinia, Router, Teleport, Suspense and async setup.

## Detailed reference

Load more detailed reference files as needed:

- Project directory, component layering, component specifications, annotations, and TypeScript: Load [references/vue3-project-structure.md](references/vue3-project-structure.md).
- Composables, slots, Provide/Inject and routing organizations: Load [references/vue3-composables-routing.md](references/vue3-composables-routing.md).
- Pinia, API layer, error handling, directives, styles, tests, anti-patterns and output checklist: Loading [references/vue3-state-api-quality.md](references/vue3-state-api-quality.md).
- Lightweight performance conventions at the Vue project specification level: Load [references/vue3-performance-patterns.md](references/vue3-performance-patterns.md).

## Constraints

- Use `<script setup lang="ts">` to disable using Options API to add new components
- The size of the component file should be approximately **300 lines**; if it exceeds **500 lines** or is too complex, sub-components and Composables must be separated
- Props / Emits must be defined using the TypeScript interface, and `any` is prohibited
- Composable returns a `readonly` reference to prevent accidental external modifications
- Do not store UI temporary states (modal switches, form inputs, etc.) in the store
- Server-side data is first managed by the request library rather than manually stored in Pinia
- Avoid using `v-if` in `v-for` (extract to computed filtering)
- It is forbidden to import directly from the deep path inside the feature, bypassing `index.ts`
- No need for global error handling to swallow recoverable API, form or permission errors within components.
- Do not mistake function parameters for getter automatic calls; if composable parameters may be callbacks, avoid using getter input conventions.
- Do not rely on snapshots as the only assertions for Vue components; asynchronous components, Teleport and Pinia scenes must have user-visible behavior assertions.

## Expected Output

- The component uses `<script setup lang="ts">`, and the Props/Emits type is complete
- Reusable logic has been extracted to composable, returning `readonly` reference
- Loading / Error / Empty / Data status have been processed
- Routing components are loaded using dynamic import, and state management conforms to the proximity principle
- URL status, server status, form status and Pinia global status have clear boundaries
- API calls have type constraints and unified error handling
- Styles are isolated using scoped, and key behaviors are covered by tests
- The file structure is consistent with the project convention (pages/features/components are separated)
- Input responsiveness, Pinia/Router boundaries and asynchronous component testing strategies for reusable composables explained
