---
name: dead-code-finder
description: >
  Find and remove dead code in JavaScript/TypeScript projects. Detects unused exports,
  unreferenced files, orphaned components, unused dependencies, and dead functions/variables.
  Supports monorepos, path aliases, barrel exports, and dynamic imports.
  Use when asked to find dead code, detect unused exports, clean up unused files,
  find orphaned modules, audit code for unused functions, remove dead code,
  identify unused dependencies, or reduce bundle size by removing unused code.
  Triggers on "dead code", "unused exports", "unused files", "orphan", "tree shake",
  "unused imports", "unused dependencies", "code cleanup", "reduce bundle".
---

# Dead Code Finder

Detect and report dead code in JavaScript/TypeScript projects.

## Quick Start

```bash
# Full scan — unused exports, files, and dependencies
python3 scripts/find_dead_code.py /path/to/project

# Exports only
python3 scripts/find_dead_code.py /path/to/project --mode exports

# Unused files only
python3 scripts/find_dead_code.py /path/to/project --mode files

# Unused dependencies only
python3 scripts/find_dead_code.py /path/to/project --mode deps

# JSON output for programmatic use
python3 scripts/find_dead_code.py /path/to/project --json
```

## What It Detects

### 1. Unused Exports
Exported functions, classes, constants, types, and interfaces never imported anywhere.
- Named exports (`export function foo`, `export const bar`)
- Re-exports (`export { x } from './y'`)
- Type exports (`export type`, `export interface`)
- Barrel file analysis (index.ts re-exports)

### 2. Unreferenced Files
Files never imported by any other file in the project.
- Skips entry points (configurable)
- Skips test files, config files, and scripts by default
- Handles path aliases (tsconfig paths)

### 3. Unused Dependencies
npm packages in package.json never imported in code.
- Checks `dependencies` and `devDependencies`
- Recognizes CLI tools as potentially used
- Handles scoped packages and subpath imports

## Configuration

Default entry points: `src/index.{ts,tsx,js,jsx}`, `src/main.*`, `src/app.*`, `pages/**/*`, `app/**/*`.

Default ignores: `node_modules`, `dist`, `build`, `.next`, `coverage`, `__tests__`, `*.test.*`, `*.spec.*`, `*.config.*`, `*.d.ts`.

Override via flags:
```bash
--entry "src/main.ts,src/worker.ts"
--ignore "generated,vendor"
```

## Interpreting Results

```
=== Dead Code Report ===

UNUSED EXPORTS (12 found):
  src/utils/helpers.ts: formatDate, parseQuery, slugify
  src/components/Button.tsx: ButtonProps (type)
  src/api/client.ts: createClient

UNREFERENCED FILES (3 found):
  src/legacy/oldAuth.ts
  src/utils/deprecated.ts
  src/components/unused/Card.tsx

UNUSED DEPENDENCIES (2 found):
  moment
  lodash.merge
```

## Workflow

1. Run scan on the project
2. Review report — some findings may be false positives (dynamic imports, reflection)
3. Verify each finding before removing
4. Remove confirmed dead code
5. Run tests to confirm nothing broke

## Limitations

- Dynamic imports with variable paths may cause false positives
- Code consumed by external packages (libraries) shows as unused
- CSS/SCSS imports not tracked
- `export *` partially supported
