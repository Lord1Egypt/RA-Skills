---
name: bundlephobia
description: Bundle size & dependency bloat analyzer — scans JS/TS projects for oversized dependencies, duplicate packages, tree-shaking failures, and bundle configuration issues
homepage: https://bundlephobia.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "📦",
      "primaryEnv": "BUNDLEPHOBIA_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# BundlePhobia — Bundle Size & Dependency Bloat Analyzer

BundlePhobia scans your JavaScript and TypeScript projects for oversized dependencies, duplicate packages, tree-shaking failures, barrel file anti-patterns, and bundle configuration issues. It uses 90+ detection patterns covering 5 categories of bundle bloat. 100% local, zero telemetry.

## Commands

### Free Tier (No license required)

#### `bundlephobia scan [file|dir]`
One-shot bundle bloat scan of your project (5 file limit on free tier).

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" scan [file|dir]
```

**What it does:**
1. Detects project type (npm/yarn/pnpm/monorepo)
2. Discovers JS/TS source files, package.json, and bundler configs
3. Scans for oversized dependencies, duplicate packages, tree-shaking failures
4. Checks bundle configuration (webpack, vite, rollup, esbuild)
5. Analyzes dependency hygiene in package.json
6. Calculates a 0-100 bloat score with letter grade (A-F)

**Example usage scenarios:**
- "Scan my project for bundle bloat" -> runs `bundlephobia scan .`
- "Check if I have oversized dependencies" -> runs `bundlephobia scan .`
- "Find tree-shaking issues in my code" -> runs `bundlephobia scan src/`
- "Analyze my package.json for bloat" -> runs `bundlephobia scan package.json`

#### `bundlephobia status`
Show license info and current configuration.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" status
```

#### `bundlephobia patterns`
List all 90+ detection patterns.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" patterns
```

### Pro Tier ($19/user/month — requires BUNDLEPHOBIA_LICENSE_KEY)

#### `bundlephobia hooks install`
Install git hooks that scan for bundle bloat on every commit.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Installs lefthook pre-commit hook targeting JS/TS files and package.json
3. On every commit: scans staged files for bundle bloat patterns, blocks commit if critical/high issues found

#### `bundlephobia hooks uninstall`
Remove BundlePhobia git hooks.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" hooks uninstall
```

#### `bundlephobia report [dir]`
Generate a detailed markdown bundle health report.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" report [dir]
```

#### `bundlephobia audit [dir]`
Deep dependency audit — analyzes every dependency for size, alternatives, and optimization opportunities.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" audit [dir]
```

### Team Tier ($39/user/month — requires BUNDLEPHOBIA_LICENSE_KEY with team tier)

#### `bundlephobia budget [dir]`
Enforce size budgets — fails if bundle exceeds configured thresholds.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" budget [dir]
```

#### `bundlephobia sarif [dir]`
Generate SARIF JSON output for CI/CD integration (GitHub Code Scanning, etc.).

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" sarif [dir]
```

#### `bundlephobia ci [dir]`
CI mode — non-interactive scan with machine-readable output and exit codes.

```bash
bash "<SKILL_DIR>/scripts/bundlephobia.sh" ci [dir]
```

## Detection Categories (90+ patterns)

| Category | Patterns | What It Detects |
|----------|----------|-----------------|
| Oversized Dependencies | 20 | moment.js, lodash full import, faker in prod, aws-sdk v2, etc. |
| Duplicate & Redundant | 18 | axios + node-fetch, moment + dayjs, jest + mocha, etc. |
| Tree-Shaking Failures | 20 | import *, require(), barrel re-exports, namespace imports, etc. |
| Bundle Configuration | 18 | Missing splitChunks, no code splitting, missing externals, etc. |
| Dependency Hygiene | 14+ | Pinned versions, deprecated packages, devDeps in deps, etc. |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "bundlephobia": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "maxBundleSize": "500KB",
          "ignoredPackages": [],
          "severityThreshold": "high",
          "checkTreeShaking": true,
          "checkDuplicates": true
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately — no configuration needed
- **All scanning happens locally** using grep-based pattern matching
- **License validation is offline** — no phone-home, no telemetry
- Works with npm, yarn, pnpm, and monorepos
- Supports webpack, vite, rollup, esbuild, parcel, and next.js configs
- POSIX-compatible — runs on macOS, Linux, and Windows (WSL/Git Bash)

## When to Use BundlePhobia

The user might say things like:
- "Scan my project for large dependencies"
- "Check my bundle size"
- "Find unnecessary packages in my project"
- "Are there any tree-shaking issues?"
- "Audit my dependencies for bloat"
- "Set up bundle size monitoring"
- "Check if I have duplicate packages"
- "Generate a bundle health report"
- "Enforce size budgets in CI"
