---
name: dependency-impact-analyzer
description: Analyze the blast radius of upgrading, removing, or replacing a dependency — trace imports, find affected files, check test coverage of impacted code, detect breaking API changes, and generate safe upgrade plans.
---

# Dependency Impact Analyzer

Before upgrading or removing a dependency, understand exactly what will be affected. Traces all imports, finds every file that uses the package, checks test coverage of impacted code, and identifies potential breaking changes.

Use when: "what happens if I upgrade X", "impact of removing lodash", "can I safely update this", "dependency blast radius", "which files use package X", "upgrade risk assessment", or before major dependency changes.

## Commands

### 1. `trace` — Trace All Usages of a Dependency

Find every file that imports or requires the package, and how it's used.

```bash
PACKAGE="${1:?Usage: trace <package-name>}"

echo "=== Tracing usage of: $PACKAGE ==="

# Direct imports (JS/TS)
echo "--- Direct Imports ---"
rg -n "from ['\"]$PACKAGE['\"/]|require\(['\"]$PACKAGE['\"/]\)|import ['\"]$PACKAGE['\"]" \
  -g '*.{js,ts,jsx,tsx,mjs,cjs}' -g '!node_modules' -g '!dist' -g '!build' 2>/dev/null

# Subpath imports
echo "--- Subpath Imports ---"
rg -n "from ['\"]$PACKAGE/" \
  -g '*.{js,ts,jsx,tsx}' -g '!node_modules' -g '!dist' 2>/dev/null

# Python imports
rg -n "^import $PACKAGE|^from $PACKAGE" \
  -g '*.py' -g '!vendor' -g '!dist' 2>/dev/null

# Go imports
rg -n "\".*$PACKAGE" \
  -g '*.go' -g '!vendor' 2>/dev/null

# Count total usage
USAGE_COUNT=$(rg -c "$PACKAGE" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.lock' -g '!package-lock.json' \
  --type-not binary 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
FILE_COUNT=$(rg -l "$PACKAGE" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.lock' -g '!package-lock.json' \
  --type-not binary 2>/dev/null | wc -l)

echo ""
echo "Total: $USAGE_COUNT references across $FILE_COUNT files"
```

Extract which specific exports/APIs are used:

```bash
# What functions/classes are imported from this package?
rg -o "import \{([^}]+)\} from ['\"]$PACKAGE['\"]" \
  -g '*.{ts,js,tsx,jsx}' -g '!node_modules' 2>/dev/null | \
  sed "s/.*{//;s/}.*//" | tr ',' '\n' | sed 's/^\s*//;s/\s*$//' | sort | uniq -c | sort -rn

rg -o "const \{([^}]+)\} = require\(['\"]$PACKAGE['\"]\)" \
  -g '*.{js,ts}' -g '!node_modules' 2>/dev/null | \
  sed "s/.*{//;s/}.*//" | tr ',' '\n' | sed 's/^\s*//;s/\s*$//' | sort | uniq -c | sort -rn
```

### 2. `impact` — Full Impact Assessment

Comprehensive analysis of what upgrading this dependency means.

#### Current Version and Target

```bash
PACKAGE="${1:?Usage: impact <package-name> [target-version]}"
TARGET_VERSION="${2:-latest}"

# Current version
if [ -f "package.json" ]; then
  CURRENT=$(python3 -c "
import json
d = json.load(open('package.json'))
v = d.get('dependencies',{}).get('$PACKAGE') or d.get('devDependencies',{}).get('$PACKAGE') or 'not found'
print(v)
" 2>/dev/null)
  echo "Current: $PACKAGE@$CURRENT"
fi

if [ -f "requirements.txt" ]; then
  grep -i "^$PACKAGE" requirements.txt 2>/dev/null
fi
```

#### Breaking Changes Detection

```bash
# Check package changelog/releases for breaking changes
echo "--- Checking for breaking changes ---"

# For npm packages: check if major version changed
if [ -f "package.json" ]; then
  npm info "$PACKAGE" versions --json 2>/dev/null | python3 -c "
import json, sys, re
try:
    versions = json.load(sys.stdin)
    current = '$CURRENT'.lstrip('^~>=')
    current_major = current.split('.')[0] if current != 'not found' else '0'
    latest = versions[-1] if isinstance(versions, list) else versions
    latest_major = latest.split('.')[0]
    if current_major != latest_major:
        print(f'⚠️  MAJOR version change: {current} → {latest} (likely breaking changes)')
    else:
        print(f'✅ Same major version: {current} → {latest} (should be backward compatible)')
except Exception as e:
    print(f'Could not check versions: {e}')
" 2>/dev/null
fi

# Check npm deprecation
npm info "$PACKAGE" deprecated 2>/dev/null | grep -v "^$" && echo "⚠️  Package is DEPRECATED"
```

#### Affected Test Coverage

```bash
# Find files that import the package
AFFECTED_FILES=$(rg -l "$PACKAGE" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.lock' -g '!*.test.*' -g '!*.spec.*' \
  -g '*.{js,ts,jsx,tsx,py,go}' --type-not binary 2>/dev/null)

echo "--- Test Coverage of Affected Files ---"
for f in $AFFECTED_FILES; do
  BASE=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")
  # Look for corresponding test file
  TEST=$(find "$DIR" -maxdepth 2 \( -name "${BASE}.test.*" -o -name "${BASE}.spec.*" -o -name "test_${BASE}.*" \) \
    -not -path '*/node_modules/*' 2>/dev/null | head -1)
  if [ -n "$TEST" ]; then
    echo "✅ $f → $TEST"
  else
    echo "❌ $f → NO TEST (upgrade risk!)"
  fi
done
```

#### Dependency Tree Impact

```bash
# What other packages depend on this one?
echo "--- Reverse Dependencies ---"
if [ -f "package-lock.json" ]; then
  python3 -c "
import json
lock = json.load(open('package-lock.json'))
pkg = '$PACKAGE'
rdeps = []
packages = lock.get('packages', lock.get('dependencies', {}))
for name, info in packages.items():
    deps = info.get('dependencies', {})
    if pkg in deps:
        clean_name = name.replace('node_modules/', '')
        rdeps.append(f'{clean_name} (requires {pkg}@{deps[pkg]})')
if rdeps:
    print(f'{len(rdeps)} packages also depend on {pkg}:')
    for r in rdeps[:20]:
        print(f'  {r}')
else:
    print(f'No other packages depend on {pkg} (leaf dependency)')
" 2>/dev/null
fi
```

### 3. `remove` — Safe Removal Analysis

What happens if you completely remove this dependency?

```bash
PACKAGE="${1:?Usage: remove <package-name>}"

echo "=== Removal Impact: $PACKAGE ==="

# All files that would break
BREAKING_FILES=$(rg -l "from ['\"]$PACKAGE|require\(['\"]$PACKAGE|import $PACKAGE|from $PACKAGE" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.lock' 2>/dev/null)

FILE_COUNT=$(echo "$BREAKING_FILES" | grep -c "." 2>/dev/null || echo "0")
echo "Files that would break: $FILE_COUNT"
echo "$BREAKING_FILES" | head -20

# Suggest alternatives
echo ""
echo "--- Alternative Packages ---"
echo "Use AI reasoning to suggest alternatives based on:"
echo "1. What specific features of $PACKAGE are used (from trace output)"
echo "2. Whether native/stdlib alternatives exist"
echo "3. What the community has migrated to"
```

### 4. `replace` — Migration Plan for Swapping Packages

Generate a migration plan for replacing one package with another.

```bash
OLD="${1:?Usage: replace <old-package> <new-package>}"
NEW="${2:?Usage: replace <old-package> <new-package>}"

echo "=== Migration Plan: $OLD ��� $NEW ==="

# Trace old package usage
echo "--- Current API Usage ($OLD) ---"
rg -o "import \{[^}]+\} from ['\"]$OLD['\"]" \
  -g '*.{ts,js,tsx,jsx}' -g '!node_modules' 2>/dev/null | head -20

echo ""
echo "--- Files to Modify ---"
rg -l "$OLD" -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.lock' 2>/dev/null
```

Generate AI-powered migration plan:
1. Map old API → new API (function name equivalents)
2. Identify APIs with no direct equivalent (need rewrite)
3. Estimate effort per file
4. Suggest migration order (tests first, then source)

### 5. `audit` — Dependency Portfolio Risk

Assess the overall risk profile of all dependencies.

```bash
echo "=== Dependency Risk Audit ==="

if [ -f "package.json" ]; then
  python3 -c "
import json, subprocess, re
from datetime import datetime

d = json.load(open('package.json'))
all_deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}

print(f'Total dependencies: {len(all_deps)}')
print(f'  Production: {len(d.get(\"dependencies\",{}))}')
print(f'  Dev: {len(d.get(\"devDependencies\",{}))}')

# Known deprecated packages
deprecated = {
    'request': 'Use fetch, axios, or got',
    'node-uuid': 'Use uuid package',
    'nomnom': 'Use commander or yargs',
    'optimist': 'Use yargs',
    'jade': 'Renamed to pug',
    'istanbul': 'Use nyc or c8',
    'coffee-script': 'Migrate to JavaScript/TypeScript',
    'bower': 'Use npm/yarn/pnpm',
    'grunt': 'Use npm scripts or modern bundlers',
    'moment': 'Use date-fns, dayjs, or Temporal',
    'left-pad': 'Use String.padStart()',
    'underscore': 'Use lodash or native JS',
}

print()
found_deprecated = []
for pkg, alt in deprecated.items():
    if pkg in all_deps:
        found_deprecated.append(f'  ⚠️  {pkg}@{all_deps[pkg]} → {alt}')

if found_deprecated:
    print(f'Deprecated packages ({len(found_deprecated)}):')
    for f in found_deprecated:
        print(f)
else:
    print('✅ No known deprecated packages')

# Pinning analysis
print()
unpinned = [(k,v) for k,v in all_deps.items() if v.startswith('^') or v.startswith('~')]
exact = [(k,v) for k,v in all_deps.items() if re.match(r'^\d', v)]
wildcard = [(k,v) for k,v in all_deps.items() if '*' in v]
print(f'Version pinning: {len(exact)} exact, {len(unpinned)} range (^/~), {len(wildcard)} wildcard')
if wildcard:
    print('  ❌ Wildcard versions (dangerous):')
    for k,v in wildcard:
        print(f'    {k}: {v}')
" 2>/dev/null
fi

# Check for security advisories
echo ""
echo "--- Security Advisories ---"
npm audit --json 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    v = d.get('metadata',{}).get('vulnerabilities',{})
    total = sum(v.values())
    if total > 0:
        print(f'Vulnerabilities: {v.get(\"critical\",0)} critical, {v.get(\"high\",0)} high, {v.get(\"moderate\",0)} moderate, {v.get(\"low\",0)} low')
    else:
        print('✅ No known vulnerabilities')
except: print('Could not parse audit output')
" 2>/dev/null

# Dependency size impact
echo ""
echo "--- Size Impact (top 10 heaviest) ---"
if command -v npx &>/dev/null; then
  echo "Run 'npx package-size <package>' for individual sizes"
fi
```

## Output Formats

- **text** (default): Human-readable with status indicators
- **json**: `{package, current_version, usage: {files, imports, apis}, tests: {covered, uncovered}, breaking_changes: [], alternatives: []}`
- **markdown**: Report suitable for PR descriptions or ADRs

## CI Integration

Exit codes:
- 0: Low impact (< 5 files, all tested)
- 1: High impact (> 20 files or untested code paths)
- 2: Critical (deprecated, vulnerable, or major breaking changes)

## Notes

- Supports JS/TS (npm), Python (pip), Go (go mod), Rust (cargo) projects
- Does not execute tests — reports coverage gaps for manual verification
- Breaking change detection relies on semver conventions and npm registry metadata
- For accurate reverse dependency analysis, a lock file must be present
- Alternative package suggestions use AI reasoning based on actual usage patterns, not generic recommendations
