# BundlePhobia

[![License: Proprietary](https://img.shields.io/badge/license-proprietary-blue.svg)](https://bundlephobia.pages.dev)
[![Platform: macOS | Linux | Windows](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()
[![Patterns: 90+](https://img.shields.io/badge/patterns-90%2B-green.svg)]()
[![Offline: 100%](https://img.shields.io/badge/offline-100%25-brightgreen.svg)]()

**Bundle size & dependency bloat analyzer for JS/TS projects.**

BundlePhobia scans your JavaScript and TypeScript projects for oversized dependencies, duplicate packages, tree-shaking failures, barrel file anti-patterns, and bundle configuration issues. 90+ detection patterns. 100% local. Zero telemetry.

## Quick Start

```bash
# Free — one-shot scan (5 file limit)
bundlephobia scan .

# Free — scan a specific file
bundlephobia scan src/index.ts

# Pro — install pre-commit hooks
bundlephobia hooks install

# Pro — generate a full report
bundlephobia report .

# Team — enforce size budgets in CI
bundlephobia budget .
```

## What It Detects

BundlePhobia scans for **90+ patterns** across 5 categories:

### 1. Oversized Dependencies (20 patterns)
Known bloated packages that have lighter alternatives:
- `moment.js` (use `date-fns` or `dayjs`)
- Full `lodash` import (use `lodash-es` or cherry-pick)
- `faker.js` in production dependencies
- `aws-sdk` v2 (use modular `@aws-sdk/*`)
- `chart.js` imported fully (use tree-shakeable import)
- `underscore.js` (use native ES methods)
- `jquery` in modern frameworks
- Full `rxjs` import (use pipeable operators)
- `crypto-browserify` (use Web Crypto API)
- `jsdom` in frontend bundles
- And 10 more...

### 2. Duplicate & Redundant Packages (18 patterns)
Multiple packages serving the same purpose:
- Both `axios` and `node-fetch`
- Both `moment` and `dayjs`
- Both `lodash` and `underscore`
- Both `express` and `koa`
- Both `jest` and `mocha`
- Multiple CSS-in-JS libraries
- Duplicate polyfill packages
- And more...

### 3. Tree-Shaking Failures (20 patterns)
Code patterns that prevent dead-code elimination:
- `import * as _ from 'lodash'`
- `require()` instead of ES `import`
- Dynamic `require()` calls
- Barrel file `export *` re-exports
- CommonJS `module.exports` mixed with ESM
- Side-effect imports of large libraries
- Namespace imports of tree-shakeable libraries
- And more...

### 4. Bundle Configuration Issues (18 patterns)
Missing or incorrect bundler configuration:
- Missing webpack `splitChunks` configuration
- No code splitting / dynamic imports for routes
- Missing minification (terser/esbuild)
- Source maps shipped to production
- No bundle analyzer configured
- Missing `externals` for server-side bundles
- And more...

### 5. Dependency Hygiene (14+ patterns)
Package.json and dependency management issues:
- Pinned exact versions without `^` or `~`
- Deprecated or unmaintained packages
- `devDependencies` incorrectly in `dependencies`
- Missing `.browserslistrc`
- Unused dependencies
- And more...

## Comparison

| Feature | BundlePhobia | bundlesize | size-limit | bundlephobia.com | webpack-bundle-analyzer | depcheck |
|---------|:----------:|:----------:|:----------:|:----------------:|:-----------------------:|:--------:|
| Oversized dep detection | Yes | No | No | Partial | No | No |
| Duplicate dep detection | Yes | No | No | No | No | Partial |
| Tree-shaking analysis | Yes | No | No | No | No | No |
| Bundle config audit | Yes | No | Partial | No | No | No |
| Dependency hygiene | Yes | No | No | No | No | Yes |
| Pre-commit hooks | Yes | No | Partial | No | No | No |
| SARIF output | Yes | No | No | No | No | No |
| Size budget enforcement | Yes | Yes | Yes | No | No | No |
| Offline / local only | Yes | Yes | Yes | No | Yes | Yes |
| No build required | Yes | No | No | Yes | No | Yes |
| 90+ patterns | Yes | N/A | N/A | N/A | N/A | N/A |

## Pricing

| Feature | Free | Pro ($19/mo) | Team ($39/mo) |
|---------|:----:|:------------:|:-------------:|
| One-shot scan | 5 files | Unlimited | Unlimited |
| Pattern detection (90+) | Yes | Yes | Yes |
| Pre-commit hooks | -- | Yes | Yes |
| Markdown reports | -- | Yes | Yes |
| Deep dependency audit | -- | Yes | Yes |
| Size budget enforcement | -- | -- | Yes |
| SARIF output | -- | -- | Yes |
| CI mode | -- | -- | Yes |

Get your license at [bundlephobia.pages.dev](https://bundlephobia.pages.dev).

## Configuration

Create or edit `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "bundlephobia": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "maxBundleSize": "500KB",
          "ignoredPackages": ["some-necessary-large-pkg"],
          "severityThreshold": "high",
          "checkTreeShaking": true,
          "checkDuplicates": true
        }
      }
    }
  }
}
```

Or set the environment variable:

```bash
export BUNDLEPHOBIA_LICENSE_KEY="your-key-here"
```

## How Scoring Works

BundlePhobia calculates a **0-100 bloat score** based on findings:

| Severity | Points Deducted |
|----------|:--------------:|
| Critical | 25 |
| High | 15 |
| Medium | 8 |
| Low | 3 |

| Grade | Score Range | Meaning |
|-------|:----------:|---------|
| A | 90-100 | Excellent — minimal bloat |
| B | 80-89 | Good — minor improvements possible |
| C | 70-79 | Acceptable — review recommended |
| D | 50-69 | Poor — significant bloat detected |
| F | 0-49 | Failing — immediate action needed |

**Pass threshold:** Score >= 70 (exit code 0). Below 70: exit code 1.

## Ecosystem

- **Website:** [bundlephobia.pages.dev](https://bundlephobia.pages.dev)
- **Docs:** [bundlephobia.pages.dev/docs](https://bundlephobia.pages.dev/docs)
- **Pricing:** [bundlephobia.pages.dev/pricing](https://bundlephobia.pages.dev/pricing)
- **Support:** [bundlephobia.pages.dev/support](https://bundlephobia.pages.dev/support)

## Privacy

- **100% local** — all analysis happens on your machine
- **Zero telemetry** — no data sent anywhere, ever
- **Offline license** — JWT-based validation, no phone-home
- **No build required** — static analysis only, no compilation needed
- **Open patterns** — all detection rules visible in `scripts/patterns.sh`
