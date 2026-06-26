---
name: bun-workspace-optimizer
description: Optimize Bun workspaces and monorepos — analyze dependency hoisting, script performance, build pipelines, and workspace configuration for maximum speed.
metadata:
  tags: ["bun", "monorepo", "workspace", "performance", "javascript"]
---

# Bun Workspace Optimizer

Analyze and optimize Bun workspace configurations for monorepos. Audit dependency hoisting, script performance, build pipelines, and workspace settings. Use when setting up Bun workspaces, migrating from npm/yarn/pnpm workspaces, or optimizing monorepo build times.

## Usage

```
"Optimize my Bun workspace setup"
"Analyze dependencies across my monorepo packages"
"Find duplicate dependencies in my workspace"
"Speed up my monorepo builds with Bun"
"Migrate my pnpm workspace to Bun"
```

## How It Works

### 1. Workspace Discovery

Map the monorepo structure:

```bash
# Check Bun version and workspace config
bun --version
cat package.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
ws = d.get('workspaces', [])
if isinstance(ws, dict): ws = ws.get('packages', [])
for w in ws: print(f'  {w}')
"

# Find all package.json files
find . -name "package.json" -not -path "*/node_modules/*" -maxdepth 3
```

### 2. Dependency Analysis

- **Hoisting audit**: Which deps are properly hoisted to root?
- **Version conflicts**: Same package with different versions across packages
- **Duplicate installs**: Packages installed in multiple workspaces unnecessarily
- **Phantom dependencies**: Used but not declared in package.json
- **Circular dependencies**: Workspace packages depending on each other in cycles
- **Unused dependencies**: Declared but never imported

```bash
# Check for version mismatches
find . -name "package.json" -not -path "*/node_modules/*" -maxdepth 3 -exec python3 -c "
import json, sys, os
from collections import defaultdict
versions = defaultdict(set)
for f in sys.argv[1:]:
    try:
        d = json.load(open(f))
        pkg = d.get('name', f)
        for deps in [d.get('dependencies',{}), d.get('devDependencies',{})]:
            for k,v in deps.items():
                versions[k].add((v, pkg))
    except: pass
for pkg, vs in sorted(versions.items()):
    unique = set(v for v,_ in vs)
    if len(unique) > 1:
        print(f'⚠️  {pkg}: {dict((src,ver) for ver,src in vs)}')
" {} +
```

### 3. Build Pipeline Optimization

- **Script analysis**: Which scripts can run in parallel?
- **Bun build vs bundlers**: Where can `bun build` replace webpack/esbuild/rollup?
- **TypeScript compilation**: Using Bun's built-in TS support vs tsc?
- **Test runner**: Migrating to `bun test` from Jest/Vitest?
- **Cache utilization**: Are builds leveraging Bun's module cache?

### 4. Performance Profiling

Compare key operations:

- `bun install` time vs npm/yarn/pnpm
- `bun run` script startup overhead
- `bun build` vs alternative bundlers
- `bun test` vs existing test runner
- Cold start vs warm start times

### 5. Configuration Best Practices

Check `bunfig.toml` and workspace config:

- Install settings: `frozen-lockfile` for CI
- Registry configuration for private packages
- Scoped package settings
- Telemetry and logging preferences
- Module resolution settings

### 6. Migration Guide

For teams migrating from other package managers:

- **From npm**: Remove `package-lock.json`, run `bun install`
- **From yarn**: Handle `.yarnrc.yml` settings, yarn plugins
- **From pnpm**: Convert `pnpm-workspace.yaml` to `package.json` workspaces
- **CI updates**: Replace npm/yarn commands in CI config
- **Docker**: Use `oven/bun` base image

## Output

```
## Bun Workspace Analysis

**Packages:** 12 | **Total deps:** 847 | **Hoisted:** 91%

### 🔴 Issues (2)
1. Circular dependency: packages/core → packages/utils → packages/core
   → Extract shared types into packages/types
2. 3 packages pin react@18.2, root has react@18.3 → version conflict
   → Align all to ^18.3.0 and hoist to root

### 🟡 Optimizations (4)
3. packages/web still uses webpack — switch to `bun build`
   → Estimated build time: 12s → 0.8s
4. 23 duplicate devDependencies across packages
   → Move to root devDependencies, save 45MB node_modules
5. `bun test` would replace Jest + ts-jest setup (3 packages)
   → Remove 12 jest config files, gain native TS support
6. Missing `bunfig.toml` — no frozen lockfile in CI
   → Add [install] frozen-lockfile = true

### 📊 Performance Comparison
| Operation | Current | With Bun | Speedup |
|-----------|---------|----------|---------|
| Install   | 34s     | 2.1s     | 16x     |
| Build     | 18s     | 1.2s     | 15x     |
| Tests     | 45s     | 12s      | 3.7x    |
| CI Total  | 4m 12s  | 1m 05s   | 3.8x    |

### ✅ Good Practices
- Clean workspace boundaries
- Shared tsconfig via extends
- Root scripts properly delegate to workspace packages
```
