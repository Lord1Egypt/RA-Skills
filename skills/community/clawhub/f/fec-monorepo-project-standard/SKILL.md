---
name: fec-monorepo-project-standard
description: Use when creating, reviewing, or restructuring frontend monorepos with pnpm workspace, Turborepo, Nx, multi-package dependency boundaries, task orchestration, package naming, or package publishing; Chinese triggers include monorepo, workspace, multi-package.
---

# Monorepo Project Specifications

For multi-package front-end repositories using pnpm workspace, Turborepo or Nx.

## Purpose

Standardize the directory structure, dependency management, task orchestration and package release process of the Monorepo project to ensure the build efficiency and version consistency of multi-package collaboration.

## Procedure

1. First confirm whether the repository has used pnpm workspace, Turborepo or Nx, and continue to use the existing package naming and task conventions.
2. Place applications in `apps/` and shared libraries, configuration and tools in `packages/` or existing equivalent directories.
3. Internal dependencies use `workspace:*` to drive the build sequence through the dependency graph.
4. Configure cacheable, parallelizable, and incremental root tasks for build, lint, and test, and specify input, output, and environment variables.
5. Configure the affected/changed range command in Turborepo/Nx. CI will run the affected packages first while retaining the backbone full verification entry.
6. Check package boundaries, circular dependencies, exports, peer dependencies and version policies before publishing the package.

## Tool selection

| Tools | Applicability | Features |
| ------------------ | ---- | -------------------------- |
| **pnpm workspace** | Basics | Dependency promotion, linking, script aggregation |
| **Turborepo** | Recommended | Caching, parallelism, dependency graph |
| **Nx** | Large | Incremental build, cloud cache, plug-in ecology |

## Directory structure

### pnpm + Turborepo

```
├── package.json # Root package, workspace configuration
├── pnpm-workspace.yaml # workspace package list
├── turbo.json # Turborepo configuration
│
├── apps/
│ ├── web/ # Main application
│   │   ├── package.json
│   │   └── ...
│ ├── admin/ # Management background
│ └── docs/ # Documentation site
│
├── packages/
│ ├── ui/ # Shared UI components
│   │   ├── package.json
│   │   └── src/
│ ├── utils/ # Utility function
│ ├── config-eslint/ # Shared ESLint configuration
│ └── config-typescript/ # Shared TS configuration
│
└── tooling/ # Build/test tools (optional)
    └── scripts/
```

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

## Dependency management

- Internal packages use the `workspace:*` protocol
- The root `package.json` unifies some dependency versions and can be overridden by sub-packages
- Disable circular dependencies, check via `pnpm why`

```json
{
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*"
  }
}
```

## Turborepo task orchestration

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
```

- `^build` means executing the build of dependent packages first
- `outputs` is used for cache hit judgment
- `inputs` should include source code, configuration, lock files and environment-related files; do not write the `.env` secret value into the cache key
- Remote caching should distinguish between trusted CI and local development to avoid uploading products containing sensitive information.

## Nx task orchestration

```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"],
      "cache": true
    }
  }
}
```

## Package naming

- Internal package: `@org/package-name` or `@repo/package-name`
- Publish to npm: follow the `@scope/name` specification

## Constraints

- Sub-packages are referenced through `workspace:*` and are not published to npm and then installed.
- Shared configurations (ESLint, TS) are placed in `packages/config-*`, and sub-packages extend
- The build order is determined by the dependency graph, without manually specifying irrelevant dependencies
- When executing `pnpm -r build` or `turbo run build` in the root directory, all packages will be built in order
- Disable circular dependencies, use `pnpm why` to check the dependency chain when adding a new package
- CI cache only caches dependent installation directories and task products, and does not cache unverified build status
- Affected builds cannot replace full verification before release; the trunk or release branch still requires complete quality control

## Expected Output

- Monorepo directory structure is clear (`apps/` applications, `packages/` shared packages, `tooling/` tools)
- `pnpm-workspace.yaml` and `turbo.json` / `nx.json` are configured correctly
- Internal packages use `workspace:*` protocol, no circular dependencies
- Build, lint, and test tasks can be executed with one click through the root command, and the cache hit rate is high
- CI can distinguish between affected quick feedback and release full verification, and the cache configuration will not leak keys or hide dependency boundary issues
