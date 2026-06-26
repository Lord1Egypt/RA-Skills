---
name: dependency-autopsy
version: 1.0.0
description: >
  Deep health analysis of your dependency tree — not just "is it outdated"
  but "is it abandoned? Is the maintainer still active? Is 95% of the package
  dead weight for your use case? Is it one mass-deletion away from taking
  your app down?" The difference between 'npm audit' and actually understanding
  what you're trusting with your production system.
author: J. DeVere Cooley
category: everyday-tools
tags:
  - dependencies
  - supply-chain
  - health
  - risk-assessment
metadata:
  openclaw:
    emoji: "🔬"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - security
---

# Dependency Autopsy

> "Every dependency is a bet: you're betting that someone you've never met will maintain code you've never read for as long as you need it. How much do you actually know about those bets?"

## What It Does

`npm audit` tells you about known vulnerabilities. `npm outdated` tells you about version drift. Neither tells you the things that actually matter:

- Is the maintainer still actively working on this?
- When was the last meaningful commit (not just a CI config tweak)?
- How many of this package's 14,000 lines do you actually use?
- If this package disappears tomorrow, how hard is the replacement?
- Does this package pull in 47 transitive dependencies for one utility function?
- Is this package's bus factor literally 1?

Dependency Autopsy performs a **full health examination** of every dependency in your tree and produces a risk-adjusted report.

## The Autopsy Report Card

Each dependency receives a health score across seven vital signs:

### Vital 1: Pulse (Activity)

Is this project alive?

| Signal | Healthy | Warning | Critical |
|---|---|---|---|
| Last meaningful commit | < 3 months | 3-12 months | > 12 months |
| Open issue response time | < 1 week | 1-4 weeks | > 4 weeks or never |
| Release frequency | Regular | Slowing | Stopped |
| CI status | Passing | Flaky | Failing or absent |
| Open PRs with no review | < 5 | 5-20 | > 20 |

```
"Last meaningful commit" means a commit that changes source code.
Dependency bumps, CI tweaks, and README updates don't count.
A project can look active while being effectively abandoned.
```

### Vital 2: Bus Factor (Maintainer Health)

How many people would need to disappear for this project to die?

| Signal | Healthy | Warning | Critical |
|---|---|---|---|
| Unique committers (last year) | > 5 | 2-5 | 1 |
| Has org ownership (not personal) | Yes | - | No (personal repo) |
| Has multiple npm/PyPI publishers | Yes | - | No (single publisher) |
| Corporate backing | Yes | Informal | None |
| Succession plan visible | Yes | Unclear | No |

### Vital 3: Bloat Factor (Weight)

How much of this package do you actually use?

```
ANALYSIS:
├── Total package size: 2.4 MB
├── Exports used by your code: 3 of 147 (2%)
├── Tree-shakeable: No
├── Transitive dependencies: 23
├── Transitive dependencies YOU also use directly: 2
│   └── (the other 21 exist solely because of this package)
├── Estimated bundle impact: +340 KB
└── Could be replaced with: ~30 lines of code

VERDICT: You imported an aircraft carrier to cross a creek.
```

### Vital 4: Replacement Difficulty

If this dependency vanished today, how hard is the swap?

| Difficulty | Description | Example |
|---|---|---|
| **Trivial** | Drop-in alternative exists, or you can inline the code | `left-pad` → 1 line of code |
| **Easy** | Alternative exists with minor API differences | `moment` → `date-fns` (well-documented migration) |
| **Moderate** | Alternatives exist but require meaningful refactoring | `Express` → `Fastify` (different middleware model) |
| **Hard** | Few alternatives, deeply integrated | `React` → `Vue` (rewrite) |
| **Critical** | No alternative, deeply embedded, you're locked in | `Terraform` → ? (vendor lock-in) |

### Vital 5: Version Health

Is your version current, and is upgrading safe?

```
ANALYSIS:
├── Your version: 3.2.1
├── Latest stable: 5.1.0
├── Versions behind: 2 major, 0 minor
├── Breaking changes between yours and latest: 14
├── Deprecated APIs you use: 3 (removed in v4+)
├── Security patches you're missing: 1 (medium severity)
├── Estimated upgrade effort: 8 hours
└── Risk of staying: Medium (deprecated APIs may break with Node upgrade)
```

### Vital 6: License Health

Are you legally safe?

```
ANALYSIS:
├── Direct dependency license: MIT ✓
├── Transitive dependency licenses:
│   ├── MIT: 19 packages ✓
│   ├── Apache-2.0: 3 packages ✓
│   ├── ISC: 1 package ✓
│   └── GPL-3.0: 1 package ⚠ (copyleft — may require your code to be GPL)
└── License compatibility with your project: WARNING — GPL transitive dep
```

### Vital 7: Dependency Depth

How deep does the rabbit hole go?

```
YOUR PACKAGE
└── dependency-a (you chose this)
    ├── dep-a-1 (you didn't choose this)
    │   ├── dep-a-1-1 (you definitely didn't choose this)
    │   │   └── dep-a-1-1-1 (nobody chose this)
    │   └── dep-a-1-2
    ├── dep-a-2
    └── dep-a-3
        └── dep-a-3-1
            └── dep-a-3-1-1
                └── dep-a-3-1-1-1 (8 levels deep. Welcome to JavaScript.)

STATS:
├── Direct dependencies you chose: 24
├── Total dependency tree: 847 packages
├── Maximum depth: 11 levels
├── Packages with 0 weekly downloads: 3 (why do these exist?)
├── Packages last published > 3 years ago: 12
└── Packages with install scripts (potential risk): 2
```

## The Full Autopsy Report

```
╔══════════════════════════════════════════════════════════════╗
║                  DEPENDENCY AUTOPSY                         ║
║            24 direct / 847 total dependencies               ║
║            Overall Health: B+ (Good, with concerns)         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CRITICAL FINDINGS (2):                                      ║
║  ├── 🔴 image-tools@1.3.0                                    ║
║  │   ├── Pulse: DEAD (last commit 26 months ago)             ║
║  │   ├── Bus Factor: 1 (personal GitHub repo)                ║
║  │   ├── You use: 1 of 23 functions (4%)                     ║
║  │   ├── Known vulns: 1 (high — prototype pollution)         ║
║  │   └── RECOMMENDATION: Replace with sharp (actively        ║
║  │       maintained, covers your use case). ~2h effort.      ║
║  │                                                           ║
║  │── 🔴 GPL-3.0 license found in transitive dependency       ║
║  │   ├── Package: obscure-xml-parser@0.1.2                   ║
║  │   ├── Required by: dep-a → dep-a-1 → obscure-xml-parser  ║
║  │   └── RECOMMENDATION: Confirm GPL compatibility or find   ║
║  │       alternative XML parser in dep-a-1.                  ║
║                                                              ║
║  WARNINGS (4):                                               ║
║  ├── 🟡 lodash@4.17.21 — you use 3 functions. Consider      ║
║  │   individual imports or native replacements (-340KB).     ║
║  ├── 🟡 auth-lib@2.1.0 — 2 major versions behind.           ║
║  │   3 deprecated APIs in your code. Upgrade: ~8h.           ║
║  ├── 🟡 date-formatter@3.0.0 — bus factor 1, slowing pulse.  ║
║  │   Consider date-fns as insurance.                         ║
║  └── 🟡 config-parser@1.0.0 — pulls 21 transitive deps      ║
║      for a 40-line utility. Consider inlining.               ║
║                                                              ║
║  HEALTHY (18):                                               ║
║  All vitals green. Active maintenance, healthy bus factor,   ║
║  appropriate usage, compatible licenses.                     ║
║                                                              ║
║  TREE STATS:                                                 ║
║  ├── Duplicate packages (different versions): 7              ║
║  ├── Total install size: 148 MB                              ║
║  ├── Estimated used code: 12 MB (8% of installed)            ║
║  └── Potential size reduction: 89 MB (remove bloat + dupes)  ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- **Before adding a new dependency** — full autopsy before you `npm install`
- Monthly health check on existing dependencies
- When evaluating whether to upgrade or replace a library
- Before a security audit or compliance review
- When investigating unexpected bundle size growth
- After any `npm audit` report (to go deeper than just CVE numbers)

## Why It Matters

The average JavaScript project has 800+ transitive dependencies. The average Python project has 40+. Each one is code you didn't write, didn't review, and don't control — running with the same permissions as your code.

`npm audit` tells you about *known* vulnerabilities. Dependency Autopsy tells you about *likely future* problems — abandoned projects, single-maintainer risk, license landmines, and bloat. The vulnerability that hasn't been discovered yet is in the package that nobody's looking at.

Zero external dependencies. Zero API calls. Pure package manifest and registry analysis.
