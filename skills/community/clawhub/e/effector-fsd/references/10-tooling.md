# Tooling for FSD + Effector

Use this file when configuring automated checks.

## Contents

- Steiger
- Common Steiger rules to care about
- When to disable a rule
- ESLint with Effector
- Path aliases
- Next.js tooling
- CI checks

## Steiger

Use `steiger` with `@feature-sliced/steiger-plugin` for FSD structure/import checks.

Install:

```bash
npm i -D steiger @feature-sliced/steiger-plugin
```

Run:

```bash
npx steiger ./src
npx steiger ./src --watch
```

Basic config:

```ts
// steiger.config.ts
import { defineConfig } from 'steiger';
import fsd from '@feature-sliced/steiger-plugin';

export default defineConfig([
  ...fsd.configs.recommended,
]);
```

Steiger is active/beta tooling and can evolve. Pin versions and document disabled rules.

## Common Steiger rules to care about

- `fsd/forbidden-imports` — imports from higher layers and sibling slices.
- `fsd/no-public-api-sidestep` — direct imports from slice internals.
- `fsd/public-api` — missing public APIs.
- `fsd/no-layer-public-api` — layer-level barrels.
- `fsd/no-segments-on-sliced-layers` — segments directly under sliced layers.
- `fsd/no-segmentless-slices` — slices without segments.
- `fsd/no-ui-in-app` — UI segment on App layer.
- `fsd/no-processes` — deprecated Processes layer.
- `fsd/segments-by-purpose` — discourages technical dump names.
- `fsd/shared-lib-grouping` — keeps `shared/lib` grouped by purpose.

## When to disable a rule

Allowed only with a reason:

```ts
export default defineConfig([
  ...fsd.configs.recommended,
  {
    files: ['./src/shared/**'],
    rules: {
      'fsd/public-api': 'off',
    },
  },
]);
```

Document why the exception exists and whether it is temporary.

## ESLint with Effector

Use `eslint-plugin-effector` for Effector-specific code quality:

- `recommended`
- `react`
- `scope`
- `patronum`
- `future` only intentionally

Steiger checks structure. ESLint checks Effector usage. Use both in serious Effector/FSD apps.

## Path aliases

Use one clear alias to `src`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

Inside a slice, prefer relative imports even if alias works. Across slices, use alias + public API.

## Next.js tooling

When using Next.js with FSD:

- keep framework `app`/`pages` outside `src` when possible
- rename FSD layers to `_app` and `_pages`
- configure Steiger for the real FSD root
- separate `index.server.ts` when server/client exports differ
- configure Effector Babel/SWC plugin for SIDs/factories if SSR/hydration is used

## CI checks

Recommended gates:

```bash
npm run typecheck
npm run lint
npx steiger ./src
npm test
```

For Next.js with `_app`/`_pages`, run Steiger against `src`, not root framework folders unless your config intentionally covers them.
