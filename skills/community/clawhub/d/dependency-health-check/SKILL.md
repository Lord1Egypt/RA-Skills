---
name: dependency-health-check
description: Multi-ecosystem dependency audit — find outdated, vulnerable, unused, and license-incompatible packages across npm, pip, cargo, go, and composer. Use when asked to check dependency health, audit packages, or plan upgrades.
---

# Dependency Health Check

Audit project dependencies across ecosystems for security, freshness, license compliance, and unused bloat. Produces a prioritized upgrade plan with risk assessment.

Use when: "check our dependencies", "are we up to date", "audit packages", "plan an upgrade", "find unused deps".

## Step 1 — Detect Ecosystem

```bash
# Auto-detect package managers
ls package.json package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null   # Node.js
ls requirements.txt Pipfile pyproject.toml setup.py 2>/dev/null           # Python
ls Cargo.toml Cargo.lock 2>/dev/null                                       # Rust
ls go.mod go.sum 2>/dev/null                                               # Go
ls composer.json composer.lock 2>/dev/null                                 # PHP
ls Gemfile Gemfile.lock 2>/dev/null                                        # Ruby
```

## Step 2 — Outdated Packages

### Node.js
```bash
npm outdated --json 2>/dev/null | jq 'to_entries[] | {name: .key, current: .value.current, wanted: .value.wanted, latest: .value.latest}'
# or
yarn outdated --json 2>/dev/null
pnpm outdated --format json 2>/dev/null
```

### Python
```bash
pip list --outdated --format json 2>/dev/null | jq '.[] | {name, version, latest_version}'
# or with pip-audit
pip-audit --format json 2>/dev/null
```

### Rust
```bash
cargo outdated -R --format json 2>/dev/null
```

### Go
```bash
go list -u -m -json all 2>/dev/null | jq 'select(.Update) | {Path, Version, Update: .Update.Version}'
```

### PHP
```bash
composer outdated --format json 2>/dev/null
```

## Step 3 — Vulnerability Scan

```bash
# Node.js
npm audit --json 2>/dev/null | jq '.vulnerabilities | to_entries[] | {name: .key, severity: .value.severity, fixAvailable: .value.fixAvailable}'

# Python
pip-audit --format json 2>/dev/null
# or
safety check --json 2>/dev/null

# Rust
cargo audit --json 2>/dev/null

# Go
govulncheck ./... 2>/dev/null

# Universal (if installed)
trivy fs --format json --scanners vuln . 2>/dev/null | jq '.Results[].Vulnerabilities[]? | {PkgName, Severity, Title}'
```

## Step 4 — Unused Dependencies

### Node.js
```bash
# depcheck finds unused deps
npx depcheck --json 2>/dev/null | jq '{unused: .dependencies, devUnused: .devDependencies, missing: .missing}'
```

### Python
```bash
# Check imports vs requirements
pip install pipreqs 2>/dev/null
pipreqs . --print 2>/dev/null > /tmp/actual-imports.txt
diff <(sort requirements.txt | sed 's/[>=<].*//' | tr '[:upper:]' '[:lower:]') \
     <(sort /tmp/actual-imports.txt | sed 's/[>=<].*//' | tr '[:upper:]' '[:lower:]')
```

### Rust
```bash
cargo udeps 2>/dev/null  # requires nightly
```

## Step 5 — License Audit

```bash
# Node.js
npx license-checker --json 2>/dev/null | jq 'to_entries[] | {pkg: .key, license: .value.licenses}' | head -40

# Python
pip-licenses --format json 2>/dev/null | jq '.[] | {Name, License}'

# Universal
trivy fs --format json --scanners license . 2>/dev/null
```

Flag: GPL in MIT projects, AGPL in SaaS, unknown/unlicensed packages, dual-license packages.

## Step 6 — Risk Assessment

For each outdated dependency, evaluate:

1. **Severity**: critical (known CVE) > high (>2 major versions behind) > medium (minor behind) > low (patch behind)
2. **Breaking changes**: check the changelog/release notes for breaking changes between current and latest
3. **Usage frequency**: grep for imports — a heavily-used dep is riskier to upgrade
4. **Test coverage**: if the dep's area has good tests, the upgrade is safer

## Output Template

```markdown
# Dependency Health Report

**Project:** [name]
**Scanned:** [date]
**Ecosystems:** Node.js, Python, etc.

## Summary
- Total dependencies: X
- Outdated: X (Y critical, Z major behind)
- Vulnerabilities: X (Y critical, Z high)
- Unused: X (safe to remove)
- License issues: X

## Critical (fix now)
| Package | Current | Latest | Issue | Risk |
|---------|---------|--------|-------|------|
| lodash | 4.17.20 | 4.17.21 | CVE-2021-23337 (prototype pollution) | High — used in 47 files |

## Recommended Upgrades (this sprint)
| Package | Current | Latest | Breaking Changes | Effort |
|---------|---------|--------|-----------------|--------|
| react | 17.0.2 | 18.3.1 | Yes — concurrent mode, new root API | 2-4 hours |

## Safe Quick Wins (patch updates)
Packages that can be bumped with minimal risk:
- `axios`: 1.6.0 → 1.7.2 (bug fixes only)
- `dotenv`: 16.3.1 → 16.4.5 (no breaking changes)

## Unused (remove)
- `moment` — imported nowhere, replaced by date-fns
- `@types/express` — no Express code found

## License Flags
- `gpl-package@1.0`: GPL-3.0 in MIT project — review compatibility
```

## Upgrade Workflow

After the audit:
1. Fix critical vulnerabilities first (`npm audit fix`, `pip-audit --fix`)
2. Remove unused dependencies
3. Batch patch updates into one PR
4. Plan major upgrades individually with dedicated PRs
5. Run tests after each upgrade batch

## Notes

- Always run the project's test suite after upgrades
- For monorepos, audit each workspace separately
- `npm audit fix --force` can introduce breaking changes — prefer targeted fixes
- Check `CHANGELOG.md` or GitHub releases for each major version jump
