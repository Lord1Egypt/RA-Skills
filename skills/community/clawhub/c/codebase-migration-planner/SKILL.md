---
name: codebase-migration-planner
description: Plan complex codebase migrations — framework upgrades, language transitions, architecture refactors. Analyze dependencies, estimate effort, map migration paths, generate phased plans, and track progress.
---

# Codebase Migration Planner

Plan and execute large-scale codebase migrations systematically. Whether it's React class→hooks, Express→Fastify, Python 2→3, monolith→microservices, or JavaScript→TypeScript — this skill maps the current state, identifies migration paths, estimates effort, and generates a phased execution plan.

Use when: "plan a migration", "migrate from X to Y", "upgrade from v1 to v2", "rewrite this in TypeScript", "how much work to migrate", "migration effort estimate", or planning a major framework/language change.

## Commands

### 1. `assess` — Migration Assessment

Analyze the current codebase to understand migration scope.

#### Step 1: Inventory Current State

```bash
echo "=== Codebase Inventory ==="

# Language distribution
echo "--- Language Distribution ---"
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.rb" \
  -o -name "*.vue" -o -name "*.svelte" -o -name "*.css" -o -name "*.scss" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/dist/*' -not -path '*/.git/*' 2>/dev/null | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn

# Total lines of code
echo "--- Lines of Code ---"
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/dist/*' 2>/dev/null | \
  xargs wc -l 2>/dev/null | tail -1

# Framework/library detection
echo "--- Frameworks & Libraries ---"
if [ -f "package.json" ]; then
  python3 -c "
import json
d = json.load(open('package.json'))
deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
frameworks = {
    'react': 'React', 'next': 'Next.js', 'vue': 'Vue.js', 'nuxt': 'Nuxt',
    'angular': 'Angular', 'svelte': 'Svelte', '@sveltejs/kit': 'SvelteKit',
    'express': 'Express', 'fastify': 'Fastify', 'koa': 'Koa', 'hapi': 'Hapi',
    'jest': 'Jest', 'vitest': 'Vitest', 'mocha': 'Mocha', 'cypress': 'Cypress',
    'webpack': 'Webpack', 'vite': 'Vite', 'esbuild': 'esbuild', 'rollup': 'Rollup',
    'tailwindcss': 'Tailwind CSS', 'styled-components': 'styled-components',
    'prisma': 'Prisma', 'typeorm': 'TypeORM', 'sequelize': 'Sequelize',
    'redux': 'Redux', 'zustand': 'Zustand', 'mobx': 'MobX',
}
found = [(v, deps[k]) for k, v in frameworks.items() if k in deps]
for name, ver in sorted(found):
    print(f'  {name}: {ver}')
" 2>/dev/null
fi

# Test count
TEST_COUNT=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" \) \
  -not -path '*/node_modules/*' 2>/dev/null | wc -l)
echo "Test files: $TEST_COUNT"

# Configuration files
echo "--- Configuration ---"
for f in tsconfig.json jsconfig.json .babelrc babel.config.* webpack.config.* vite.config.* \
         rollup.config.* .eslintrc* eslint.config.* biome.json prettier* jest.config.* \
         vitest.config.* next.config.* nuxt.config.* svelte.config.*; do
  ls $f 2>/dev/null
done
```

#### Step 2: Migration Target Analysis

Based on what the user wants to migrate to, analyze:
- API surface differences between old and new
- Configuration changes needed
- Incompatible patterns that need rewriting
- Available codemods or migration tools

#### Step 3: Scope Estimation

```bash
echo "=== Migration Scope ==="

# Count files that need migration (depends on migration type)
# Example: JS → TS migration
echo "--- Files Requiring Migration ---"
find . -name "*.js" -o -name "*.jsx" | \
  grep -v node_modules | grep -v dist | grep -v build | wc -l

# Group by directory (to plan phases)
echo "--- Files by Directory ---"
find . \( -name "*.js" -o -name "*.jsx" \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' 2>/dev/null | \
  xargs -I{} dirname {} | sort | uniq -c | sort -rn | head -20

# Complexity per directory (rough effort indicator)
echo "--- Complexity by Directory ---"
for dir in $(find . -maxdepth 2 -type d -not -path '*/.git*' -not -path '*/node_modules*' -not -path '*/dist*' 2>/dev/null); do
  LOC=$(find "$dir" -maxdepth 1 -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) 2>/dev/null | \
    xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  [ "$LOC" -gt 0 ] 2>/dev/null && echo "  $dir: $LOC lines"
done | sort -t: -k2 -rn | head -15
```

### 2. `plan` — Generate Migration Plan

Produce a phased migration plan with effort estimates.

```markdown
# Migration Plan: [From] → [To]
Generated: [date]
Estimated total effort: X person-weeks

## Phase 0: Preparation (Week 1)
- [ ] Set up new tooling alongside old (dual support)
- [ ] Add configuration for target framework
- [ ] Ensure CI runs both old and new test suites
- [ ] Create migration tracking document
- Effort: 2-3 days

## Phase 1: Foundation (Week 2-3)
Target: shared utilities, types, constants
- [ ] Migrate `src/utils/` (N files, ~X lines)
- [ ] Migrate `src/types/` (N files, ~X lines)
- [ ] Migrate `src/constants/` (N files, ~X lines)
- Effort: N days
- Risk: Low (leaf modules, no dependents to break)

## Phase 2: Core Libraries (Week 4-5)
Target: internal libraries used by features
- [ ] Migrate `src/lib/` (N files, ~X lines)
- [ ] Update imports in consuming files
- [ ] Run full test suite after each library
- Effort: N days
- Risk: Medium (other code depends on these)

## Phase 3: Features (Week 6-8)
Target: feature modules, one at a time
- [ ] Migrate `src/features/auth/` (N files)
- [ ] Migrate `src/features/users/` (N files)
- [ ] ... (ordered by dependency — leaf features first)
- Effort: N days
- Risk: Medium-High (user-facing code)

## Phase 4: Cleanup (Week 9)
- [ ] Remove old tooling and configuration
- [ ] Update CI to remove dual-support
- [ ] Update documentation
- [ ] Final integration testing
- Effort: 2-3 days

## Rollback Strategy
At any phase, the old code still works alongside the new:
- Revert the phase's commits
- Restore old configuration
- No data migration needed (this is code-only)
```

### 3. `codemods` — Find Available Codemods

Search for automated migration tools:

```bash
echo "=== Available Codemods ==="

# Common migration codemods
# React
if rg -q "from ['\"]react['\"]" -g '*.{tsx,jsx}' 2>/dev/null; then
  echo "React codemods:"
  echo "  - npx @codemod/cli --transform react/19/migration"
  echo "  - npx react-codemod rename-unsafe-lifecycles"
  echo "  - npx react-codemod update-react-imports"
fi

# TypeScript adoption
if [ -f "jsconfig.json" ] || find . -name "*.js" -not -path '*/node_modules/*' 2>/dev/null | head -1 | grep -q .; then
  echo "JS → TS codemods:"
  echo "  - npx ts-migrate setup ."
  echo "  - npx @codemod/cli --transform js-to-ts"
fi

# Express → Fastify
if rg -q "require\(['\"]express['\"]\)|from ['\"]express['\"]" 2>/dev/null; then
  echo "Express → Fastify migration:"
  echo "  - Manual migration (no automated codemod)"
  echo "  - Key changes: app.get → fastify.get, middleware → hooks/plugins"
fi

# Vue 2 → Vue 3
if rg -q "from ['\"]vue['\"]" -g '*.{vue,js,ts}' 2>/dev/null; then
  echo "Vue codemods:"
  echo "  - npx @vue/compat"
  echo "  - gogocode-cli -s ./src -t vue2-to-vue3 -o ./src"
fi
```

### 4. `track` — Migration Progress Tracking

Update a `MIGRATION.md` tracking file:

```markdown
# Migration Progress: JS → TypeScript

| Directory | Files | Migrated | Remaining | Status |
|-----------|-------|----------|-----------|--------|
| src/utils/ | 12 | 12 | 0 | ✅ Complete |
| src/lib/ | 8 | 5 | 3 | 🔄 In Progress |
| src/features/auth/ | 6 | 0 | 6 | ⏳ Pending |
| src/features/users/ | 15 | 0 | 15 | ⏳ Pending |
| src/pages/ | 22 | 0 | 22 | ⏳ Pending |
| **Total** | **63** | **17** | **46** | **27%** |

Last updated: 2026-04-28
```

### 5. `risks` — Risk Assessment

Analyze migration risks:

- **Dependency compatibility**: Do all dependencies support the target?
- **Test coverage**: Which migrated files lack tests?
- **API surface**: Which public APIs might change?
- **Data compatibility**: Any serialization/deserialization changes?
- **Performance**: Known performance differences between old/new?

```bash
# Check if major dependencies support the target
echo "=== Dependency Compatibility ==="
if [ -f "package.json" ]; then
  python3 -c "
import json
d = json.load(open('package.json'))
deps = list(d.get('dependencies', {}).keys())
print(f'Production dependencies to verify: {len(deps)}')
for dep in deps[:20]:
    print(f'  {dep} — check compatibility with target')
" 2>/dev/null
fi
```

### 6. `effort` — Effort Estimation

Estimate person-hours based on file analysis:

| Factor | Weight | Notes |
|--------|--------|-------|
| Lines of code | 1 hr per 200 LOC | Mechanical changes |
| Complex files (>300 LOC) | 2x multiplier | Need careful migration |
| Files without tests | 1.5x multiplier | Need manual verification |
| API boundary files | 2x multiplier | Risk of breaking consumers |
| Configuration files | 2 hrs each | Need deep understanding |

```
Estimated effort:
  Simple files (< 100 LOC, with tests): 35 files × 0.5 hr = 17.5 hrs
  Medium files (100-300 LOC): 20 files × 1.5 hr = 30 hrs
  Complex files (> 300 LOC): 8 files × 4 hr = 32 hrs
  Config/build files: 5 files × 2 hr = 10 hrs
  Testing/verification: 20% buffer = 18 hrs

  Total: ~108 hours (~2.7 person-weeks)
```

## Output Formats

- **text** (default): Human-readable plan with tables
- **json**: `{assessment: {}, plan: {phases: []}, risks: [], effort: {}, codemods: []}`
- **markdown**: Stakeholder-ready document with Gantt-style timeline

## Common Migration Types

This skill handles any migration, but excels at:
- **JS → TypeScript**: File-by-file, incremental adoption
- **React class → hooks**: Component-by-component
- **Express → Fastify**: Route-by-route
- **Webpack → Vite**: Config rewrite + plugin mapping
- **Jest → Vitest**: Near-drop-in with config changes
- **Vue 2 → Vue 3**: Composition API + breaking changes
- **REST → GraphQL**: Schema-first, resolver mapping
- **Monolith → Microservices**: Domain-driven decomposition

## Notes

- Does not execute migrations — generates plans and tracks progress
- Effort estimates are based on heuristics and should be validated with team knowledge
- Codemod recommendations may have version-specific availability
- For large migrations (>100 files), recommend incremental approach with dual-support period
- Migration tracking file (`MIGRATION.md`) should be committed for team visibility
