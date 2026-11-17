# Source policy

Last audited: 2026-07-06.

Prefer official documentation and current package repositories. For FSD, prefer official Feature-Sliced Design v2.1 docs and the official FSD Skill. For Effector code semantics, prefer official Effector/Farfetched/Atomic Router/Next integration docs.

## Primary FSD sources

- Feature-Sliced Design overview: https://feature-sliced.design/
- FSD overview / applicability: https://fsd.how/docs/get-started/overview/
- FSD layers: https://feature-sliced.design/docs/reference/layers
- FSD slices and segments: https://feature-sliced.design/docs/reference/slices-segments
- FSD public API: https://feature-sliced.design/docs/reference/public-api
- FSD Next.js guide: https://feature-sliced.design/docs/guides/tech/with-nextjs
- FSD desegmentation issue: https://feature-sliced.design/docs/guides/issues/desegmented
- FSD migration from custom architecture: https://feature-sliced.design/docs/guides/migration/from-custom
- FSD docs for LLMs / official Skill: https://feature-sliced.design/docs/llms
- Steiger: https://github.com/feature-sliced/steiger

## Primary Effector ecosystem sources

- Effector docs: https://effector.dev
- Effector explicit app start: https://effector.dev/en/resources/explicit-start/
- Effector React `useUnit`: https://effector.dev/en/api/effector-react/useUnit/
- Effector React + TypeScript example with feature-sliced structure: https://effector.dev/en/typescript/usage-with-effector-react/
- Farfetched docs: https://ff.effector.dev
- Farfetched Atomic Router integration: https://ff.effector.dev/api/routers/atomic-router
- Atomic Router protected route example: https://atomic-router.github.io/examples/protected-route.html
- `@effector/next`: https://github.com/effector/next

## Trust rules

- Use official docs over blog posts.
- Treat community examples as useful signals, not normative rules.
- Treat old FSD examples as potentially outdated; official docs and Steiger rules win.
- Treat exact Farfetched/Atomic Router/Next APIs as version-sensitive; verify current docs before generating exact code.
- If FSD and a framework conflict, keep framework files as adapters and preserve FSD ownership inside `src` or renamed layers.
- If FSD and Effector semantics conflict, preserve both: FSD decides ownership/imports; Effector decides reactive flow, Scope, and startup.
