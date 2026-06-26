---
name: tech-debt-tracker
description: Identify, categorize, and prioritize technical debt across a codebase — analyze TODOs, complexity hotspots, dependency age, test coverage gaps, and code duplication.
metadata:
  tags: ["tech-debt", "code-quality", "maintenance", "refactoring", "engineering"]
---

# Tech Debt Tracker

Systematically identify, categorize, and prioritize technical debt across a codebase. Analyzes TODO comments, complexity hotspots, stale dependencies, test coverage gaps, code duplication, and architectural debt. Produces actionable debt inventory with estimated effort and business impact.

## Usage

```
"Scan this codebase for tech debt"
"Prioritize our technical debt backlog"
"Find the highest-risk areas in our code"
"Generate a tech debt report for the team"
```

## How It Works

### 1. TODO/FIXME/HACK Mining

```bash
# Find all debt markers
grep -rn "TODO\|FIXME\|HACK\|XXX\|WORKAROUND\|TEMP\|DEPRECATED" src/ --include="*.{ts,js,py,rb,go,java,rs}" | head -50
# Age analysis — when were they added?
for match in $(grep -rln "TODO\|FIXME" src/); do
  oldest=$(git log --format=%ci --diff-filter=A -- "$match" | tail -1)
  count=$(grep -c "TODO\|FIXME" "$match")
  echo "$match: $count markers, file created: $oldest"
done
```

Categorize each marker:
- **Deferred bugs**: FIXME, known issues, edge cases
- **Shortcuts**: HACK, WORKAROUND, temporary code
- **Missing features**: TODO for planned work
- **Deprecated code**: DEPRECATED markers, sunset dates

### 2. Complexity Hotspots

Identify files with highest change frequency AND highest complexity:

```bash
# Most changed files (git churn)
git log --format=format: --name-only --since="6 months ago" | sort | uniq -c | sort -rn | head -20
# Largest files (often correlate with complexity)
find src/ -name "*.ts" -exec wc -l {} + | sort -rn | head -20
```

High churn + high complexity = highest debt risk. These files change often and are hard to modify safely.

### 3. Dependency Analysis

- **Outdated packages**: Dependencies behind 2+ major versions
- **Deprecated packages**: Using packages with known replacements
- **Security vulnerabilities**: Unpatched CVEs in dependencies
- **Abandoned packages**: No commits in 12+ months
- **Heavy dependencies**: Large packages used for small features

### 4. Test Coverage Gaps

- Files with zero test coverage but high change frequency
- Critical paths (auth, payments, data mutations) without integration tests
- Tests that don't assert behavior (snapshot-only, no real assertions)
- Flaky tests that are skipped or disabled

### 5. Code Duplication

- Significant duplicated blocks (>10 lines)
- Similar functions that should be extracted
- Copy-paste patterns across modules
- Utility functions reimplemented in multiple places

### 6. Architectural Debt

- Circular dependencies between modules
- God classes/files (>500 lines of logic)
- Tight coupling between layers
- Missing abstractions (direct DB calls in controllers)
- Dead code (unreachable functions, unused exports)
- Inconsistent patterns (some services use repos, some use raw queries)

### 7. Debt Prioritization

Score each item on:
- **Impact**: How much does this slow down development? (1-5)
- **Risk**: What breaks if we don't fix it? (1-5)
- **Effort**: How long to fix? (hours/days/weeks)
- **Priority**: Impact × Risk / Effort

## Output

```
## Tech Debt Report

**Codebase:** 45K LOC across 312 files
**Scan date:** 2026-04-30
**Total debt items:** 87

### Debt Summary
| Category | Count | High Priority |
|----------|-------|---------------|
| TODO/FIXME markers | 34 | 8 |
| Complexity hotspots | 12 | 5 |
| Outdated dependencies | 18 | 3 |
| Test coverage gaps | 15 | 6 |
| Code duplication | 8 | 2 |

### 🔴 Top 5 Priority Items

1. **auth/session.ts** — 847 lines, 23 TODOs, changed 45 times in 6 months
   Impact: 5 | Risk: 5 | Effort: 3 days
   → Split into auth, session, and token modules

2. **Missing payment error handling** — FIXME on line 234
   Added 8 months ago, payment failures silently succeed
   Impact: 5 | Risk: 5 | Effort: 4 hours
   → Add proper error propagation and retry logic

3. **express@4.18 → 5.x migration** — 2 major versions behind
   Breaking changes in error handling middleware
   Impact: 3 | Risk: 4 | Effort: 2 days
   → Upgrade with middleware compatibility testing

4. **Zero test coverage on billing module** — 12 files, 2.3K LOC
   Changed 18 times in 6 months, no tests
   Impact: 4 | Risk: 5 | Effort: 1 week
   → Add integration tests for payment flows

5. **Duplicate user validation** — same logic in 4 controllers
   Impact: 3 | Risk: 2 | Effort: 2 hours
   → Extract to shared middleware

### 📊 Debt Trends
- New TODOs this month: 8 added, 3 resolved (net +5)
- Average TODO age: 4.2 months
- Oldest unresolved: 14 months (data-export.ts:67)
- Debt velocity: increasing (+2.3 items/month)

### 💡 Recommended Sprint Allocation
- Bug fixes: 60% of sprint
- Debt reduction: 20% of sprint (pick top 2-3 items)
- New features: 20% of sprint
```
