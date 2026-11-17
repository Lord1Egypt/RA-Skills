---
name: checkly-playwright
description: Configure Playwright test suites with Checkly including playwright.config.ts integration, multiple projects, and full test suite deployment. Use when running complete Playwright test suites as checks, managing multiple browsers, or leveraging Playwright's full feature set. Triggers on playwright config, test suite, playwright project, multiple browsers.
---

# checkly playwright

Run full Playwright test suites as Checkly checks.

## Playwright Check Suite

Deploy entire Playwright test suite:

```typescript
// checkly.config.ts
export default defineConfig({
  bundle: {
    packages: {
      embed: ['@acme/**', '!@acme/public-*'],
    },
  },
  checks: {
    playwrightConfigPath: './playwright.config.ts',
    playwrightChecks: [
      {
        logicalId: 'e2e-test-suite',
        name: 'E2E Test Suite',
        frequency: 10,
        testCommand: 'npm run test:e2e',
        locations: ['us-east-1', 'eu-west-1'],
        tags: ['e2e'],
      },
    ],
  },
})
```

## Structured check intent

`PlaywrightCheck` supports durable intent for Checkly root-cause analysis and check repair:

```typescript
import { PlaywrightCheck } from 'checkly/constructs'

new PlaywrightCheck('critical-browser-journey', {
  name: 'Critical Browser Journey',
  playwrightConfigPath: './playwright.config.ts',
  intent: {
    goal: 'Verify that users can complete the critical browser journey.',
    constraints: [
      {
        type: 'MUST_PRESERVE',
        statement: 'Do not weaken the final success assertion.',
      },
    ],
  },
})
```

The shorthand `checks.playwrightChecks` entries do not expose `intent`; use an explicit `PlaywrightCheck` construct when intent is required. Intent does not replace Playwright assertions. Omit it to preserve existing backend-authored intent, provide an object to set/update it, or use `intent: null` to clear it deliberately. A goal is required and limited to 2,000 trimmed characters. Constraints use exact uppercase types `REQUIRED_OUTCOME` or `MUST_PRESERVE`, with at most 20 of each type and 1,000 trimmed characters per statement.

## Playwright configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
})
```

### Runtime engine auto-detection

When an explicit `engine` is omitted from a `PlaywrightCheck`, the CLI resolves Node and Bun candidates separately. It reads `.node-version`, `.nvmrc`, `.tool-versions`, `.bun-version`, and `package.json` `engines` only from the project root (`Session.basePath`); member-level copies beside a nested Checkly config are ignored. Only Volta lookup starts at the package containing the Checkly config. A Node candidate always wins over a Bun candidate, so `.bun-version` or `engines.bun` selects Bun only when no Node source resolves. Among Node sources, `.node-version`, `.nvmrc`, and the `nodejs` entry in `.tool-versions` override Volta, which overrides `engines.node`.

For Volta, the CLI walks from the config package toward the project root and stops at the nearest `package.json` with a `volta` object, even if that object and its `volta.extends` chain provide no `node` pin; a member-level block that only pins a package manager therefore hides a root Volta Node pin. A valid semver range in `volta.node` or `engines.node` resolves to its minimum major (`>=22` selects Node 22). Non-semver values fall through, as do `.nvmrc` aliases `lts/*`, `lts`, `node`, `stable`, and `latest`. Volta does not select Bun. For an explicit override, import `Engine` from `checkly/constructs` and set `engine: Engine.node(...)` or `Engine.bun(...)` when repository metadata is ambiguous or the Checkly runtime must intentionally differ from local tooling.

## Multiple projects

```typescript
playwrightChecks: [
  {
    logicalId: 'chromium-tests',
    name: 'Chromium Tests',
    testCommand: 'npx playwright test --project=chromium',
    frequency: 5,
  },
  {
    logicalId: 'cross-browser-tests',
    name: 'Cross-Browser Tests',
    testCommand: 'npx playwright test',
    frequency: 30,
  },
]
```

## Private package registries

For Playwright Check Suites, Checkly automatically bundles `.npmrc` from the workspace root and each workspace-member package root. Do not add those files to `include`. pnpm 11 credentials from the global `auth.ini` are also available to CLI-side package downloads. Keep credentials as environment-variable references, never plaintext:

```ini
@company:registry=https://registry.example.com/
//registry.example.com/:_authToken=${NPM_TOKEN}
```

Runner-side installs resolve the reference from Checkly environment variables. CLI-side work such as embedded-package downloads and lockfile pruning applies `npm_config_*` variables first, followed by `.npmrc` files in per-key precedence: project, workspace root, then pnpm's global `auth.ini` before the user `.npmrc` for pnpm lockfiles—or the user `.npmrc` before `auth.ini` for other lockfiles. These sources are read on the machine running `checkly deploy` or `checkly test`, so provide referenced variables through local or CI secrets too. Bun or Yarn credentials stored only in `bunfig.toml` or `.yarnrc.yml` are not used for these CLI-side downloads; duplicate registry/auth settings in `.npmrc` or `npm_config_*` variables.

### Automatic lockfile pruning

For monorepos whose bundle includes only part of the workspace, Checkly automatically prunes the bundled lockfile to the bundle's dependency graph. The workspace files are unchanged. Supported inputs are pnpm lockfile versions 6/9, npm lockfile versions 2/3, text `bun.lock`, and Yarn Berry `yarn.lock`; Yarn Classic is unsupported, and for binary `bun.lockb` regenerate a text lockfile with `bun install --save-text-lockfile`. pnpm 12 lockfiles that lead with a package-manager environment document are supported; pnpm emits this document when `package.json` declares a `packageManager` field. Version detection, pruning, and subset verification read only the application document, pnpm's regenerated output ships whole, and the `patchedDependencies` rewrite carries the environment document over verbatim. The workspace package-manager binary must be available on the CLI machine. npm and pnpm prefer cached registry metadata and contact the registry only for cache misses; pnpm also pins pruning to the workspace's own content-addressable store so a temporary directory on another filesystem does not silently use an empty store.

The prune budget defaults to 30 seconds. Set `CHECKLY_LOCKFILE_PRUNE_TIMEOUT=<seconds>` when a cold or slow registry legitimately needs more time; `0` disables the timeout, while invalid values are ignored. Whenever pruning is required but cannot run or its result cannot be verified—including when the package-manager binary is unavailable or the pnpm store directory cannot be determined—the original lockfile ships unchanged and the CLI emits a warning or note explaining why. For a timeout, the diagnostic names the timeout override and package-manager partial output is logged; for a subset-verification failure, the diagnostic names unexpected entries and the full list is logged. Enable these details with `DEBUG='checkly:cli:services:check-parser:*'`. `CHECKLY_LOCKFILE_PRUNE=0` disables pruning only as a last resort. Prefer fixing cache/store access or including the workspace member the checks actually import rather than carrying unrelated dependencies.

For pnpm projects with `patchedDependencies`, Checkly filters out patches that only apply to unbundled workspace members. If the CLI names stale patch declarations, the lockfile is out of date with the config; refresh it with a regular install.

### Embedding private package tarballs

Use top-level `bundle.packages.embed` when runners cannot fetch specific Playwright Check Suite packages:

```typescript
bundle: {
  packages: {
    embed: [
      '@acme/**',
      '!@acme/public-*',
      '@vendor/legacy-client@2.1.0',
    ],
  },
}
```

Entries resolve against the workspace-root lockfile. A name embeds every selected version; `name@version` pins one version. `*` stays within a package-name segment, while `**` crosses `/` and can select scoped and unscoped names. A `!` entry subtracts from selections made before it, so order matters. A positive entry that contributes no embeddable package fails validation unless later exclusions deliberately remove its whole selection; unmatched exclusions are no-ops, and a final empty selection warns.

The CLI verifies tarballs against lockfile integrity, or registry metadata for Yarn Berry. For embedded packages resolved from a Yarn Berry lockfile, every deploy needs registry access—even with a warm cache—to fetch package metadata before cache lookup. List every unreachable private dependency, including transitive ones; selecting a package does not automatically embed its private dependencies. Workspace, git, file, URL, and unverifiable entries must remain available through normal bundling or runner registry access. Pruned-out lockfile packages are not embedded because the runner will not install them.

The cache defaults to `node_modules/.cache/checkly`; use `CHECKLY_CACHE_DIR` only for a deliberate writable/shared cache. Changing the embedded set invalidates the runner dependency cache.

### Pruning bundled package manifests

Use `bundle.packages.prune` to remove dependencies from uploaded `package.json` copies without modifying files on disk. This is useful for unused peer dependencies that pnpm `auto-install-peers` would otherwise install:

```typescript
bundle: {
  packages: {
    prune: [
      { member: '.', remove: { devDependencies: ['docs-*'] } },
      {
        member: '@acme/e2e',
        keep: { dependencies: ['@acme/test-utils', 'playwright'] },
      },
    ],
  },
}
```

The top-level value may instead be a global pattern array or a dependency-class map over `dependencies`, `devDependencies`, `peerDependencies`, and `optionalDependencies`; `true` removes a whole class. Patterns use the embed wildcard and ordered `!` exclusion grammar, but not `name@version`. Use `**`, not `*`, to include scoped names.

Member-scoped entries select manifest names; `.` selects the workspace root. `remove` composes with other removals. `keep` declares the member's entire remaining dependency set, empties unmentioned classes, and overrides removals for that member, so prefer exact member names. Pruning is not checked against imported code: never remove a runtime dependency. When a lockfile is bundled, manifest pruning is applied only if lockfile pruning succeeds in the same run; otherwise original manifests ship with a warning.

### Runner registry routing

When registry URLs work on the CLI machine but not from Checkly runners, configure runner-only routing:

```typescript
runner: {
  registries: {
    upstreams: {
      npmjs: { url: 'https://registry.npmjs.org/' },
      internal: {
        url: 'https://npm.example.com/',
        auth: { type: 'bearer', token: '${INTERNAL_NPM_TOKEN}' },
      },
    },
    packages: [
      { pattern: '@acme/**', upstreams: ['internal'] },
      { pattern: '**', upstreams: ['npmjs'] },
    ],
  },
}
```

Rules are first-match-wins and must end with the exact `**` catch-all. Upstreams within one rule are attempted in order; failure does not fall through to a later broader rule, preventing private package-name leakage. Routing patterns support `*`/`**`, but not `!` or version pins. Bearer tokens must be exactly one `${VAR}` reference resolved from Checkly environment variables. Embedded packages take priority. This routing does not affect CLI-side downloads or lockfile pruning, which still use local registry configuration.

## Dependency cache invalidation

Checkly keys installed dependencies from the workspace's dependency inputs—the lockfile plus every workspace member's `package.json` and `.npmrc`, whether or not that member is in the bundle—plus the bundle's own install inputs, including registry configuration and the resolved embedded/pruned package sets. The key can therefore change without a file edit when a different set of workspace members lands in the bundle. If those inputs are unchanged but a deployed or scheduled Playwright Check Suite needs a persistent reinstall, change `runner.cache.install.version` in `checkly.config.ts`:

```typescript
export default defineConfig({
  projectName: 'My monitoring project',
  logicalId: 'my-monitoring-project',
  runner: {
    cache: {
      install: {
        version: '2', // string or safe integer; change to invalidate
      },
    },
  },
})
```

Do not place cache configuration on an individual suite or check: one uploaded code bundle serves all Playwright Check Suites. Unset and empty-string versions leave the key unchanged. The deprecated `caching.dependencyCache.version` alias still works with a warning; upgrade every CLI environment before migrating, then remove the old property because declaring it together with `runner.cache.install.version` fails config loading. For a one-off reinstall during an ad-hoc run, use `--refresh-cache` on `checkly test`, `checkly pw-test`, `checkly trigger`, or `checkly checks run` instead.

## Related Skills

- See `checkly-checks` for individual browser checks
- See `checkly-test` for testing Playwright checks
