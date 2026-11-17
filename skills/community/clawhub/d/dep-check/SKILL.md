---
name: dep-check
description: Use when user wants to check for outdated npm dependencies.
triggers: ["dep", "dependencies", "过期", "outdated", "npm check"]
version: 1.0.0
author: VBot
---

# Dependency Checker

> Check for outdated npm packages

## Usage

```bash
npm outdated
```

Or for detailed info:

```bash
npm audit
```

## Parse Output

| Column | Meaning |
|--------|---------|
| Current | Installed version |
| Wanted | Semver range max |
| Latest | Latest published |

## Action Thresholds

| Priority | Condition | Action |
|----------|-----------|--------|
| 🔴 High | Major version behind | Update soon |
| 🟡 Medium | Minor version behind | Update when convenient |
| 🟢 Low | Patch version behind | Optional |

## Safe Update

```bash
# Update all
npm update

# Update specific
npm update package-name
```

## Before Update

1. Check breaking changes in CHANGELOG
2. Run tests after update
3. Commit before major updates
