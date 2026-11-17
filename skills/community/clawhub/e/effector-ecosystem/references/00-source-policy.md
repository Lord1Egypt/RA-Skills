# Source policy

Last audited: 2026-07-06. Prefer current official docs for version-sensitive APIs.

Prefer official documentation and package repositories. For version-specific APIs, check current docs before answering.


## Version-sensitive checks

Before giving code for these APIs, verify the installed/current docs when the answer depends on exact shape:

- Farfetched `createJsonQuery`, `createJsonMutation`, `response.mapError` argument shape, `concurrency`, `keepFresh`, `cache`, `update`, `createBarrier`, `applyBarrier`, and `@farfetched/atomic-router`
- Effector Scope APIs: `fork`, `allSettled`, `serialize`, `hydrate`, `scopeBind`
- `@effector/next` App Router/Pages Router examples and caveats
- Atomic Router `chainRoute`, protected routes, SSR support, and SWC plugin factory configuration
- Effector Babel/SWC plugin `factories` configuration for local factories and ecosystem factories

## Primary sources

- Effector LLM source: https://effector.dev/en/llms-full.txt
- Effector docs: https://effector.dev
- Effector ecosystem: https://effector.dev/en/introduction/ecosystem/
- Effector best practices: https://effector.dev/en/guides/best-practices/
- Effector React `useUnit`: https://effector.dev/en/api/effector-react/useUnit/
- Effector Store API: https://effector.dev/en/api/effector/Store/
- Effector `sample`: https://effector.dev/en/api/effector/sample/
- Effector Scope/Fork API: https://effector.dev/en/api/effector/fork/
- Effector `scopeBind`: https://effector.dev/en/api/effector/scopeBind/
- Effector explicit app start: https://effector.dev/en/guides/explicit-start/
- Effector `allSettled`: https://effector.dev/en/api/effector/allSettled/
- Effector `serialize`: https://effector.dev/en/api/effector/serialize/
- Effector `hydrate`: https://effector.dev/en/api/effector/hydrate/
- Next.js router recipe: https://effector.dev/en/recipes/nextjs/router/
- Next.js `scopeBind` recipe: https://effector.dev/en/recipes/nextjs/scope-bind/
- Effector Babel/SWC plugins: https://effector.dev/en/api/effector/swc-plugin/
- `@effector/next`: https://github.com/effector/next

## Ecosystem sources

- Farfetched docs: https://ff.effector.dev
- Farfetched createJsonQuery: https://ff.effector.dev/api/factories/create_json_query
- Farfetched createJsonMutation: https://ff.effector.dev/api/factories/create_json_mutation
- Farfetched contracts: https://ff.effector.dev/tutorial/contracts
- Farfetched concurrency ADR/operator: https://ff.effector.dev/adr/concurrency
- Farfetched cache/refresh/update/barriers: https://ff.effector.dev/api/operators/cache, https://ff.effector.dev/api/operators/keep_fresh, https://ff.effector.dev/api/operators/update, https://ff.effector.dev/api/operators/apply_barrier
- With Ease contracts: https://withease.effector.dev/contracts/
- With Ease factories: https://withease.effector.dev/factories/
- With Ease i18next: https://withease.effector.dev/i18next/
- With Ease Web API: https://withease.effector.dev/web-api/
- Patronum docs: https://patronum.effector.dev
- Atomic Router docs: https://atomic-router.github.io
- Atomic Router + Farfetched integration: https://ff.effector.dev/api/routers/atomic-router
- Farfetched `createBarrier`: https://ff.effector.dev/api/factories/create_barrier
- Farfetched `applyBarrier`: https://ff.effector.dev/api/operators/apply_barrier
- Farfetched `keepFresh`: https://ff.effector.dev/api/operators/keep_fresh
- Farfetched `cache`: https://ff.effector.dev/api/operators/cache
- Farfetched `update`: https://ff.effector.dev/api/operators/update
- Farfetched Atomic Router `freshChain`/`startChain`/`barrierChain`: https://ff.effector.dev/api/routers/atomic-router
- Atomic Router protected route example: https://atomic-router.github.io/examples/protected-route.html
- Atomic Router `chainRoute`: https://atomic-router.github.io/api/chain-route.html
- effector-storage: https://github.com/yumauri/effector-storage
- effector-action: https://github.com/siberiacancode/effector-action
- effector-forms: https://github.com/42-px/effector-forms
- `@effector/reflect`: https://reflect.effector.dev
- `@withease/redux`: https://withease.effector.dev/redux/

## Architecture and tooling

- eslint-plugin-effector: https://eslint.effector.dev
- eslint-plugin-effector rules: https://eslint.effector.dev/rules/

## Trust rules

- Use official docs over blog posts.
- Treat README examples as package-specific, not universal architecture advice.
- If docs conflict, prefer current package docs for API shape and Effector docs for lifecycle, Scope, and reactive architecture.
- Do not invent package APIs. If an API is not confirmed, describe the architectural approach and tell the user to check current package docs.


## Project-structure boundary

This skill intentionally does not own Feature-Sliced Design rules. For FSD layers, slices, public APIs, import boundaries, Steiger, and placement decisions in Effector projects, use the separate `effector-fsd` skill. Path examples in this skill are illustrative only.
