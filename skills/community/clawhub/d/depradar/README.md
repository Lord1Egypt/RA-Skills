<div align="center">

# /depradar

**Dependency breaking-change intelligence — for every agent, every terminal, every CI pipeline.**

Scan your project's dependencies for breaking changes, find exactly which files in *your* codebase will break, and surface what the community has already reported — all scored and ranked so you fix the most dangerous upgrade first.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/deps-stdlib%20only-green)](scripts/depradar.py)
[![Tests](https://img.shields.io/badge/tests-838%20passing-brightgreen)](#running-tests)
[![Platforms](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](scripts/sync.sh)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-blueviolet)](https://claude.ai/code)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-compatible-orange)](agents/openai.yaml)

</div>

---

## What It Does

`/depradar` goes far beyond `npm outdated` or `pip list --outdated`. It answers the question every developer dreads after an upgrade: **"what exactly broke, and where in my codebase?"**

```
/depradar

╔════════════════════════════════════════════════════════════╗
║  /depradar — Dependency Breaking Change Report             ║
╚════════════════════════════════════════════════════════════╝

▸ Scanned 24 packages · 2 major bumps · 5 minor · 17 up-to-date

### stripe  7.0.0 → 8.2.0  [MAJOR]  Score: 87 ████████▋
  Breaking changes (3):
    1. [removed/high]  `constructEvent()` removed — use `stripe.webhooks.constructEvent()`
    2. [renamed/med]   `Stripe.Error` → `StripeError`
    3. [behavior/med]  Default timeout changed from 80s to 30s

  Impact: 4 files use changed symbols
    - src/payments/checkout.py:42   (AST · high confidence)
    - src/payments/checkout.py:91   (AST · high confidence)
    - src/webhooks/handler.py:18    (AST · high confidence)
    - tests/test_billing.py:204     (AST · high confidence)

  Community signals (8 reports)
    GitHub Issues · Stack Overflow · Reddit · Hacker News
```

**Seven things happen in one command:**

1. **Reads your dependency files** — `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, and their lock files
2. **Checks every registry** — npm, PyPI, crates.io, Maven Central, RubyGems, and GitHub Releases for new versions
3. **Extracts breaking changes** — 4-pass parser: `## Breaking Changes` section headers → Conventional Commits (`BREAKING CHANGE:`, `feat!:`) → keyword heuristics → plain-English breaking phrases
4. **Scans your codebase** — Python: full AST (high confidence) · JS/TS: import-tracking + optional Node.js AST · All others: grep fallback
5. **Searches the community** — GitHub Issues, Stack Overflow, Reddit, and Hacker News for migration pain reports
6. **Scores and ranks** — `0.35 × severity + 0.25 × recency + 0.30 × impact + 0.10 × community` (0–100)
7. **Delivers an actionable report** — what broke, where it broke in your code, what others did to fix it

---

## Table of Contents

- [Who Can Use This](#who-can-use-this)
- [Supported Ecosystems](#supported-ecosystems)
- [Installation](#installation)
  - [Claude Code](#option-1-claude-code-recommended)
  - [OpenAI Codex CLI](#option-2-openai-codex-cli)
  - [Direct CLI — No AI Required](#option-3-direct-cli--no-ai-required)
  - [CI/CD Pipelines](#option-4-cicd-pipelines)
- [Quick Start](#quick-start)
- [All Flags and Options](#all-flags-and-options)
- [API Keys and Configuration](#api-keys-and-configuration)
  - [Zero-Config Mode](#zero-config-mode-no-keys-needed)
  - [Optional API Keys](#optional-api-keys)
  - [Configuration Layers](#configuration-layers)
- [Output Formats](#output-formats)
- [Scoring System](#scoring-system)
- [Codebase Impact Scan](#codebase-impact-scan)
- [Community Signals](#community-signals)
- [Ignore Packages](#ignore-packages)
- [Session-Start Hook](#session-start-hook)
- [Architecture](#architecture)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Who Can Use This

**This is not Claude-only.** `/depradar` is a standalone Python tool with AI agent integration layered on top.

| User type | How they use it |
|-----------|-----------------|
| **Claude Code** | Type `/depradar` — Claude reads `SKILL.md`, runs the script, presents results conversationally |
| **OpenAI Codex CLI** | Same `/depradar` slash command, installed via `agents/openai.yaml` compatibility manifest |
| **Terminal user** | `python scripts/depradar.py` — no AI framework, no internet account needed |
| **CI/CD pipeline** | `python ... --emit=json --fail-on-breaking` — machine-readable, exit-code-driven |
| **Generic AI agent** | Any agent that follows the `~/.agents/skills/` convention picks it up automatically |

**Requirements:** Python 3.8+ · No pip packages · No external runtime

---

## Supported Ecosystems

| Ecosystem | Dependency files read | Lock files | Registry queried |
|-----------|-----------------------|------------|-----------------|
| **Node.js / TypeScript** | `package.json` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | npm registry (private registries via `.npmrc`) |
| **Python** | `requirements.txt`, `requirements-*.txt`, `pyproject.toml`, `Pipfile`, `setup.cfg`, `setup.py` | — | PyPI JSON API |
| **Rust** | `Cargo.toml` | `Cargo.lock` | crates.io API |
| **Java** | `pom.xml`, `build.gradle`, `build.gradle.kts` | — | Maven Central |
| **Ruby** | `Gemfile`, `.gemspec` | `Gemfile.lock` | RubyGems API |
| **Go** | `go.mod` | `go.sum` | GitHub Releases (Go modules) |

A single run handles multi-ecosystem projects automatically — Python backend + Node.js frontend is one command.

---

## Installation

### Option 1: Claude Code (recommended)

```bash
git clone https://github.com/depradar/depradar-skill
cd depradar-skill
bash scripts/sync.sh
```

`sync.sh` copies the skill to `~/.claude/skills/depradar-skill/`. Claude Code auto-discovers any skill in that directory. Open a new Claude Code session and `/depradar` is ready — no registration, no config.

**What `sync.sh` does:**
1. Validates Python 3.8+ is available
2. Creates `~/.claude/skills/depradar-skill/` if it doesn't exist
3. Copies all skill files (uses `rsync --delete` if available, otherwise `cp -r`)
4. Removes `__pycache__/` and `.pyc` files
5. Makes hook scripts executable
6. Optionally installs the `acorn` JS parser via `npm install` (enables JS/TS AST analysis; falls back to regex if unavailable)
7. Prints API key setup instructions

```
✓ Python 3.12.5 OK
  → Installing to /home/user/.claude/skills/depradar-skill ...
✓ Installed to /home/user/.claude/skills/depradar-skill

Optional: Add API keys for better coverage
  Create /home/user/.config/depradar/.env
```

**Dry run** (see what would be installed without doing it):
```bash
bash scripts/sync.sh --dry-run
```

**Uninstall:**
```bash
bash scripts/sync.sh --uninstall
```

---

### Option 2: OpenAI Codex CLI

Same install command. `sync.sh` detects `~/.codex/skills/` and installs there too. The `agents/openai.yaml` manifest declares full flag compatibility so Codex knows how to invoke the skill.

```bash
bash scripts/sync.sh
# Installs to:
#   ~/.claude/skills/depradar-skill/   (Claude Code)
#   ~/.codex/skills/depradar-skill/    (OpenAI Codex CLI)
#   ~/.agents/skills/depradar-skill/   (generic agents)
```

---

### Option 3: Direct CLI — No AI Required

Clone and run directly. No install step needed:

```bash
git clone https://github.com/depradar/depradar-skill
cd /your/project
python /path/to/depradar-skill/scripts/depradar.py
```

Or after installing via `sync.sh`:

```bash
# Shorthand alias (add to your .bashrc / .zshrc)
alias depradar='python ~/.claude/skills/depradar-skill/scripts/depradar.py'

# Then anywhere:
cd /your/project && depradar
cd /your/project && depradar stripe --deep
cd /your/project && depradar --emit=json | jq '.packages_with_breaking_changes[].package'
```

---

### Option 4: CI/CD Pipelines

#### GitHub Actions

```yaml
name: Dependency Audit
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1'   # Every Monday at 9am

jobs:
  depradar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install /depradar
        run: |
          git clone https://github.com/depradar/depradar-skill /tmp/depradar-skill
          bash /tmp/depradar-skill/scripts/sync.sh

      - name: Check for breaking changes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python ~/.claude/skills/depradar-skill/scripts/depradar.py \
            --emit=json \
            --fail-on-breaking \
            --no-community \
            --days=7 \
            --min-score=50
```

`--fail-on-breaking` returns exit code `1` when any breaking changes are found, causing the CI step to fail. `--no-community` skips the slower community signal search (not needed for automated checks). `--min-score=50` filters out low-confidence signals.

#### Pre-commit Hook

```bash
# .git/hooks/pre-push
#!/usr/bin/env bash
python ~/.claude/skills/depradar-skill/scripts/depradar.py \
  --quick --fail-on-breaking --no-community --no-scan 2>&1
```

#### Save Reports to Slack

```bash
python ~/.claude/skills/depradar-skill/scripts/depradar.py \
  --notify=slack://https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## Quick Start

### In Claude Code

```
/depradar                      # Scan current project
/depradar stripe               # Check one package by name
/depradar stripe openai        # Check multiple packages
/depradar --quick              # Fast scan (60 seconds)
/depradar --deep               # Thorough scan (300 seconds)
/depradar --diagnose           # Check API key setup
/depradar --mock               # Demo mode — no network calls
```

### In your terminal

```bash
cd /your/project

# Basic scan
python ~/.claude/skills/depradar-skill/scripts/depradar.py

# Check specific package
python ~/.claude/skills/depradar-skill/scripts/depradar.py stripe

# JSON output for scripts
python ~/.claude/skills/depradar-skill/scripts/depradar.py --emit=json > report.json

# Save a Markdown report
python ~/.claude/skills/depradar-skill/scripts/depradar.py --emit=md

# Verify your API keys are working
python ~/.claude/skills/depradar-skill/scripts/depradar.py --diagnose
```

---

## All Flags and Options

### Package Selection

| Flag | Description |
|------|-------------|
| *(no packages)* | Scan all production dependencies in current project |
| `stripe openai ...` | Check only the named packages |
| `--all` | Include `devDependencies`, `extras_require`, test deps |
| `--path=PATH` | Scan a different project directory (default: current directory) |

### Depth and Timing

| Flag | Description |
|------|-------------|
| `--quick` | 60-second timeout · top 5 packages by severity · fewer community results |
| `--deep` | 300-second timeout · exhaustive community search · all packages |
| `--days=N` | Look back N days for new releases (default: `30`) |
| `--refresh` | Bypass the 6-hour cache — always fetch fresh data from registries |
| `--min-score=N` | Only show packages with score ≥ N (default: `0`, shows everything) |

### Output

| Flag | Description |
|------|-------------|
| `--emit=compact` | Human-readable terminal output (default) |
| `--emit=json` | Machine-readable JSON to stdout — suitable for scripts and dashboards |
| `--emit=md` | Saves a full Markdown report to `~/Documents/DepRadar/YYYY-MM-DD_project.md` |
| `--emit=context` | Compact JSON formatted for Claude's context window |
| `--save` | Auto-save a Markdown report (same result as `--emit=md`) |
| `--save-dir=PATH` | Save the Markdown report to a custom directory |
| `--verbose` | Show detailed per-step progress including registry calls and parse results |
| `--version` | Print skill version and exit |

### Skipping Phases (Performance)

| Flag | Description |
|------|-------------|
| `--no-scan` | Skip the codebase impact scan — faster, no file:line results |
| `--no-community` | Skip GitHub/SO/Reddit/HN community signal search — much faster |

### Automation and Alerting

| Flag | Description |
|------|-------------|
| `--fail-on-breaking` | Exit with code `1` if any breaking changes are found — use in CI/CD |
| `--notify=slack://WEBHOOK` | POST the report to a Slack incoming webhook URL |
| `--notify=file:///PATH` | Write the JSON report to a file path |
| `--show-ignored` | Show packages suppressed by `.depradar-ignore` |

### Utility

| Flag | Description |
|------|-------------|
| `--diagnose` | Show API key status, test GitHub auth, print config file locations |
| `--mock` | Use bundled fixture data — zero network calls (demos and offline testing) |
| `--setup` | Interactive wizard to configure API keys and write config files |

---

## API Keys and Configuration

### Zero-Config Mode (no keys needed)

`/depradar` works completely without any API keys. You get:

- npm, PyPI, crates.io, Maven Central, RubyGems registry lookups (all public, no auth)
- GitHub Releases (unauthenticated, 60 requests/hour)
- Stack Overflow search (300 requests/day)
- Hacker News via Algolia (historical data, no auth)
- Codebase impact scan (local only, no network)

This is enough for the majority of use cases.

---

### Optional API Keys

Add keys to unlock full coverage:

| Key | What it unlocks | Where to get it | Free? |
|-----|----------------|-----------------|-------|
| `GITHUB_TOKEN` | GitHub API: 5,000 req/hr (vs 60 without), private repos, release notes | [github.com/settings/tokens](https://github.com/settings/tokens) — no scopes needed for public repos | ✅ Free |
| `STACKOVERFLOW_API_KEY` | Stack Overflow: 10,000 req/day (vs 300) | [stackapps.com](https://stackapps.com) | ✅ Free |
| `XAI_API_KEY` | Twitter/X signals via xAI Grok (LLM-recalled from training data) | [console.x.ai](https://console.x.ai) | Paid |
| `SCRAPECREATORS_API_KEY` | Reddit community signals | [scrapecreators.com](https://scrapecreators.com) | Paid |

> **Note on Twitter/X signals:** The `XAI_API_KEY` integration uses the xAI Grok language model to recall tweets from its training data — it is not a live Twitter search API. Signals are displayed for context but are excluded from community pain scoring to avoid inflating scores with approximate data.

---

### Configuration Layers

Configuration is loaded from three sources in priority order — later sources override earlier ones:

```
Priority 1 (lowest)  →  ~/.config/depradar/.env          Global, all projects
Priority 2           →  .claude/depradar.env              Per-project (walk up to git root)
Priority 3 (highest) →  Shell environment variables        export GITHUB_TOKEN=...
```

#### Global config — applies to all projects

```bash
mkdir -p ~/.config/depradar
cat > ~/.config/depradar/.env << 'EOF'
# GitHub API — free, no scopes needed for public repos
# Get one at: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Stack Overflow — raises limit from 300/day to 10,000/day
# Register an app at: https://stackapps.com
STACKOVERFLOW_API_KEY=your_so_key

# xAI Grok — Twitter/X signal recall from training data
# Get one at: https://console.x.ai
XAI_API_KEY=xai-xxxxxxxxxxxxxxxxxxxx

# Reddit via ScrapeCreators — community signal search
# Sign up at: https://scrapecreators.com
SCRAPECREATORS_API_KEY=sc_xxxxxxxxxxxx
EOF
```

#### Per-project config — commit this to share settings with your team

```bash
mkdir -p .claude
cat > .claude/depradar.env << 'EOF'
# Project-level settings — safe to commit (no secrets here)
# GITHUB_TOKEN and other secrets should stay in ~/.config/depradar/.env
EOF
```

> **Security:** Never commit API keys to `.claude/depradar.env`. Keep secrets in `~/.config/depradar/.env` (user-level) or in environment variables.

#### Check your configuration

```bash
python ~/.claude/skills/depradar-skill/scripts/depradar.py --diagnose
```

Output:
```
/depradar v2.3.0 — Configuration

  Config source:  global:/home/user/.config/depradar/.env
  Cache dir:      /home/user/.cache/depradar

  GitHub API      ✓ Authenticated  (5,000 req/hr)
  Stack Overflow  ✓ API key set    (10,000 req/day)
  Reddit          ✗ No key         (disabled)
  Twitter/X       ✗ No key         (disabled)
```

---

## Output Formats

### `--emit=compact` (default)

Human-readable terminal output with colour. Designed for reading in a Claude Code session or terminal.

```
### stripe  7.0.0 → 8.2.0  [MAJOR]  Score: 87
  Breaking changes (3):
    1. [removed/high]  `constructEvent()` removed — use `stripe.webhooks.constructEvent()`
    2. [renamed/med]   `Stripe.Error` → `StripeError`
    3. [behavior/med]  Default timeout changed from 80s to 30s

  Impact: 4 files use changed symbols
    - src/payments/checkout.py:42  (AST · high confidence)
    - src/webhooks/handler.py:18   (AST · high confidence)

  Community signals (8 reports)
    [GI1] stripe webhook breaking change · GitHub Issues · 2026-03-15
    [SO1] stripe v8 constructEvent migration · Stack Overflow · 2026-03-10
```

### `--emit=json`

Full machine-readable JSON on stdout. Parse it with `jq`, feed it to dashboards, store it in databases.

```bash
python ... --emit=json | jq '.packages_with_breaking_changes[] | {package, score, semver_type}'
```

JSON structure:
```json
{
  "project_path": "/path/to/project",
  "generated_at": "2026-03-28T10:00:00Z",
  "packages_scanned": 24,
  "packages_with_breaking_changes": [
    {
      "id": "P1",
      "package": "stripe",
      "ecosystem": "npm",
      "current_version": "7.0.0",
      "latest_version": "8.2.0",
      "semver_type": "major",
      "has_breaking_changes": true,
      "score": 87,
      "subs": {
        "severity": 95,
        "recency": 82,
        "impact": 100,
        "community": 60
      },
      "breaking_changes": [
        {
          "symbol": "constructEvent",
          "change_type": "removed",
          "description": "constructEvent() removed — use stripe.webhooks.constructEvent()",
          "migration_note": "Use `stripe.webhooks.constructEvent` instead.",
          "confidence": "high",
          "source": "changelog"
        }
      ],
      "impact_locations": [
        {
          "file_path": "src/payments/checkout.py",
          "line_number": 42,
          "symbol": "constructEvent",
          "detection_method": "ast"
        }
      ],
      "impact_confidence": "high",
      "changelog_url": "https://github.com/stripe/stripe-node/releases/tag/v8.0.0"
    }
  ],
  "packages_with_minor_updates": [...],
  "github_issues": [...],
  "stackoverflow": [...],
  "reddit": [...],
  "hackernews": [...]
}
```

### `--emit=md`

Saves a full Markdown report to `~/Documents/DepRadar/YYYY-MM-DD_projectname.md`. Each package gets its own section with a breaking changes table, impact file list, and community signal links. Share with your team, open in Obsidian, commit to a wiki.

### `--emit=context`

Compact JSON optimised for Claude's context window — used internally when Claude calls the skill as part of a larger conversation.

---

## Scoring System

Every package update receives a score from 0–100. Breaking changes are ranked so you fix the most dangerous upgrade first.

### Package score formula

```
score = 0.35 × severity + 0.25 × recency + 0.30 × impact + 0.10 × community
```

Plus a **staleness bonus** (0–18 points) for old-but-unfixed breaking changes — so a dependency you've ignored for 6+ months doesn't quietly drop off the radar:

| Package age | Bonus |
|-------------|-------|
| < 30 days | 0 — normal recency applies |
| 1–3 months | +3 |
| 3–6 months | +8 |
| 6–12 months | +12 |
| 1+ year | +18 |

### Severity weights

| Change type | Severity |
|-------------|----------|
| API/function **removed** | 100 |
| API/function **renamed** | 80 |
| **Signature changed** (params/return type) | 70 |
| **Behaviour changed** (same call, different result) | 60 |
| **Type changed** | 50 |
| **Deprecated** (not yet removed) | 40 |
| Other breaking change | 30 |

### Recency

Scores decay from 100 (released today) to 0 (released more than 365 days ago) using a log-decay curve. This keeps very new releases prominent while letting old news fade — unless the staleness bonus intervenes.

### Impact confidence

| Impact confidence | Points |
|-------------------|--------|
| High (AST-detected usage) | 100 |
| Medium (regex/grep-detected) | 70 |
| Low (scan ran, no usage found) | 40 |
| Not scanned | 50 (neutral) |

### Community score

Derived from the weighted count of community signals (GitHub Issues · Stack Overflow · Reddit · Hacker News) that match the package version, using `log1p` to dampen the effect of outlier packages with hundreds of reports.

---

## Codebase Impact Scan

When a breaking change is found, the scanner locates every place in *your* codebase where the changed symbol is used.

### Detection methods by language

| Language | Method | Confidence |
|----------|--------|------------|
| **Python** | Full AST (`ast.parse`) — tracks `import X`, `from X import Y as Z`, alias resolution across files | High |
| **JavaScript / TypeScript** | Import-tracking regex (`import`, `require`, `await import()`), dynamic imports, destructured imports | Medium |
| **JS/TS with Node.js** | Full AST via `acorn` (installed by `sync.sh`) | High |
| **Rust, Go, Java, Ruby** | `grep` fallback — searches for symbol name in source files | Low-Medium |

### What it finds

For each breaking symbol:
- Exact file path and line number
- Detection confidence level
- Symbol alias tracking (e.g. `import stripe as s` → scans for `s.charge()`)

### Scan exclusions

Automatically skips:
- `node_modules/`, `.venv/`, `vendor/`, `dist/`, `build/`, `.git/`
- Minified files (detected by line length > 500 chars)
- Files larger than 1MB
- Binary files

### Scan timeout

The scan respects the depth timeout (quick: 60s, default: 90s, deep: 300s). Files scanned so far are always returned even if the timeout fires.

---

## Community Signals

Five community sources are searched for migration pain reports about each package version:

| Source | What's fetched | API |
|--------|---------------|-----|
| **GitHub Issues** | Open and closed issues mentioning the package version | GitHub REST API (unauthenticated or with `GITHUB_TOKEN`) |
| **Stack Overflow** | Questions about breaking changes, migration errors, import failures | StackExchange API — ecosystem-specific queries (`stripe breaking change javascript` for npm, `stripe breaking change python` for PyPI) |
| **Reddit** | Posts in developer subreddits about the package | ScrapeCreators API (`SCRAPECREATORS_API_KEY` required) |
| **Hacker News** | Stories and discussions mentioning the package | HN Algolia API (historical data, pre-Feb 2026) + Firebase HN API for fresh vote/comment counts |
| **Twitter/X** | Developer posts about breaking changes | xAI Grok LLM (`XAI_API_KEY` required) — recalled from training data, not live search |

All community results are:
- **Version-filtered** — only signals that mention the relevant major version are counted toward the score (avoids counting old v6 complaints when you're upgrading to v8)
- **Quality-weighted** — closed + answered issues score 2.0×, open + no-comments score 0.8×
- **Relevance-filtered** — off-topic titles like "Flutter Pre-Launch Checklist" are rejected for commander.js
- **Cached** for 6 hours to avoid hammering APIs

---

## Ignore Packages

Create a `.depradar-ignore` file in your project root to suppress packages you've consciously decided not to upgrade:

```
# .depradar-ignore

# Exact version — ignore only this specific version of lodash
lodash@4.17.21

# All versions — always ignore this package
legacy-adapter

# Wildcard — ignore all @internal packages
@internal/*

# Comment explaining why
moment          # migrating to date-fns in Q3 — tracked in JIRA-1234
```

Run with `--show-ignored` to see which packages are being suppressed and why.

---

## Session-Start Hook

When installed as a Claude Code skill, a hook runs automatically at the start of every session (`hooks/hooks.json`, event: `SessionStart`). It checks your API key configuration and prints a one-line tip if `GITHUB_TOKEN` is missing:

```
[/depradar] Tip: Add GITHUB_TOKEN to ~/.config/depradar/.env for 5,000 GitHub API req/hr
            (currently 60). Run '/depradar --diagnose' for setup instructions.
```

- Runs once per session, silent when all keys are configured
- Never blocks Claude from starting (always exits 0)
- Timeout: 5 seconds

---

## Architecture

```
/depradar invocation
        │
        ▼
scripts/depradar.py          ← Main orchestrator
        │
        ├── lib/dep_parser.py        Parse dependency files → DepInfo list
        │       └── lock file resolution (package-lock.json, yarn.lock, pnpm-lock.yaml)
        │
        ├── lib/{npm,pypi,crates,maven,gem}_registry.py
        │       └── Fetch latest versions from each registry
        │
        ├── lib/github_releases.py   Fetch GitHub release notes
        │       ├── lib/changelog_parser.py   4-pass breaking change extraction
        │       │       ├── Pass 1: ## Breaking Changes section headers
        │       │       ├── Pass 2: BREAKING CHANGE: footer, feat!: syntax
        │       │       ├── Pass 3: keyword scan (medium confidence, requires code symbol)
        │       │       └── Pass 3b: strong plain-English phrases (low confidence)
        │       └── parse_all_version_sections() for multi-major jumps
        │
        ├── lib/usage_scanner.py     Scan codebase for symbol usage
        │       ├── Python: ast.parse with alias tracking
        │       ├── JS/TS: import regex + dynamic imports + lib/js_ast_helper.js (acorn)
        │       └── Fallback: grep for symbol names
        │
        ├── lib/impact_analyzer.py   Map scan results to ImpactLocation objects
        │       └── Broad scan (package name) when no specific symbols extracted
        │
        ├── Community signal pipeline (concurrent):
        │       ├── lib/github_issues.py    GitHub Issues search
        │       ├── lib/stackoverflow.py    SO search (ecosystem-aware cache key)
        │       ├── lib/reddit_sc.py        Reddit via ScrapeCreators
        │       ├── lib/hackernews.py       HN Algolia + Firebase enrichment
        │       └── lib/twitter_x.py        xAI Grok recall (display only, not scored)
        │
        ├── lib/score.py            Scoring engine (severity/recency/impact/community)
        │       └── lib/normalize.py  Score normalization (passthrough for [0,100] scores)
        │
        ├── lib/dedupe.py           De-duplicate community signals
        │
        ├── lib/render.py           Output rendering
        │       ├── compact renderer (terminal)
        │       ├── JSON renderer
        │       ├── Markdown renderer (file save)
        │       └── context renderer (Claude's context window)
        │
        ├── lib/cache.py            File-based TTL cache (~/.cache/depradar/)
        │       ├── Registry data: 6-hour TTL
        │       └── Community signals: 6-hour TTL
        │
        ├── lib/env.py              3-layer config loading
        ├── lib/semver.py           SemVer parsing with pre-release support
        ├── lib/http.py             HTTP client with retry + exponential backoff
        ├── lib/notify.py           Slack / file notification dispatch
        ├── lib/ignores.py          .depradar-ignore parser
        └── lib/ui.py               Terminal UI (spinners, colours, machine mode)
```

**All Python. Zero pip dependencies. Everything in the standard library.**

---

## Running Tests

```bash
cd scripts
python -m pytest ../tests/ -v
```

The test suite covers every module with 838 tests across 38 test files:

```
tests/
├── test_changelog_parser.py       Breaking change extraction (section headers, CC, keywords)
├── test_changelog_parser_v2.py    Extended parser edge cases
├── test_dep_parser.py             Dependency file parsing (all ecosystems)
├── test_dep_parser_lockfiles.py   Lock file version resolution
├── test_dep_parser_monorepo.py    Monorepo workspace support
├── test_semver.py                 SemVer parsing, pre-release ordering, bump classification
├── test_score.py                  Scoring formulas and staleness bonus
├── test_github_releases.py        Release note fetching and CHANGELOG parsing
├── test_github_issues.py          GitHub Issues search and filtering
├── test_stackoverflow.py          SO search with ecosystem-aware cache keys
├── test_hackernews.py             HN Algolia + Firebase enrichment
├── test_reddit_sc.py              Reddit signal fetching
├── test_npm_registry.py           npm registry lookups and private registries
├── test_pypi_registry.py          PyPI registry lookups
├── test_impact_analyzer.py        Codebase impact scan, broad scan fallback
├── test_usage_scanner.py          Python AST and JS import tracking
├── test_usage_scanner_v2.py       Dynamic imports, minified file detection
├── test_render.py                 Output rendering (compact, JSON, MD)
├── test_cache.py                  Cache TTL, key collision, 32-char keys
├── test_schema_roundtrip.py       Data model serialization / deserialization
├── test_ignores.py                .depradar-ignore parsing and wildcard matching
├── test_multi_version_jump.py     starknet v7→v9 CHANGELOG multi-section extraction
├── test_production_fixes.py       All changes5.txt production fixes (14 fixes)
├── test_changes6_fixes.py         All changes6.txt production fixes (9 fixes)
└── ...                            20+ more
```

**Run a specific test file:**
```bash
python -m pytest ../tests/test_semver.py -v
```

**Run only the production fix tests:**
```bash
python -m pytest ../tests/test_production_fixes.py ../tests/test_changes6_fixes.py -v
```

**Mock mode — test the full pipeline with no network:**
```bash
cd /any/project && python ~/.claude/skills/depradar-skill/scripts/depradar.py --mock
```

---

## Troubleshooting

### "No dependency files found"

You're not in a project directory, or your dependency file has a non-standard name.

```bash
# Try specifying the project path directly
python ... --path=/path/to/your/project

# Or run from the project root
cd /path/to/your/project && python ...
```

### "Rate limited by GitHub API"

You're hitting the unauthenticated limit of 60 requests/hour.

```bash
# Add your token
echo "GITHUB_TOKEN=ghp_your_token_here" >> ~/.config/depradar/.env

# Verify it works
python ... --diagnose
```

### "Package X not found" for a Python package

The skill defaults to checking npm first when you specify a package by name and it's not in your dependency files.

```bash
# Try specifying the ecosystem:
python ... requests --ecosystem=pypi

# Or cd to your Python project directory first so dep files are auto-detected
cd /your/python/project && python ... requests
```

### JSON output has extra text before the JSON

Make sure you're not mixing human-readable output with machine-readable. Always use `--emit=json` explicitly when piping:

```bash
# Wrong — compact mode with color codes will break JSON parsers
python ... | jq .

# Correct
python ... --emit=json | jq .
```

### Breaking changes found but no impact locations

Either:
1. Your codebase doesn't use the changed symbols directly (transitive dependency)
2. The scanner couldn't find the import pattern (dynamic imports, re-exports)
3. The symbols weren't extracted from sparse release notes

Try `--deep` for more thorough extraction, or check the changelog URL shown in the output.

### Hacker News returns no results for recent packages

The HN Algolia search index was archived in February 2026. Historical results (pre-2026) are still returned and enriched with fresh vote/comment counts from the Firebase HN API. Post-2026 HN results are not available.

### Cache is returning stale data

Force a fresh fetch:
```bash
python ... --refresh
```

Cache is stored in `~/.cache/depradar/`. Delete it to clear everything:
```bash
rm -rf ~/.cache/depradar/
```

---

## Project Structure

```
depradar-skill/
├── SKILL.md                    ← AI agent instructions (Claude reads this)
├── CLAUDE.md                   ← Quick-start for Claude Code users
├── README.md                   ← This file
├── LICENSE                     ← MIT
│
├── scripts/
│   ├── depradar.py             ← Main entry point
│   ├── sync.sh                 ← Install script (Claude Code / Codex / terminal)
│   └── lib/                   ← All library modules (stdlib only)
│       ├── dep_parser.py       Dependency file parser (all ecosystems)
│       ├── github_releases.py  GitHub Releases API + CHANGELOG fetching
│       ├── changelog_parser.py 4-pass breaking change extractor
│       ├── usage_scanner.py    Codebase scanner (AST + regex + grep)
│       ├── impact_analyzer.py  Impact location mapper
│       ├── npm_registry.py     npm registry client
│       ├── pypi_registry.py    PyPI JSON API client
│       ├── crates_registry.py  crates.io API client
│       ├── maven_registry.py   Maven Central client (with pagination)
│       ├── github_issues.py    GitHub Issues search
│       ├── stackoverflow.py    Stack Overflow API (ecosystem-aware)
│       ├── reddit_sc.py        Reddit via ScrapeCreators
│       ├── hackernews.py       HN Algolia + Firebase enrichment
│       ├── twitter_x.py        xAI Grok signal recall
│       ├── score.py            Scoring engine
│       ├── normalize.py        Score normalization
│       ├── render.py           Output rendering (compact/JSON/MD/context)
│       ├── schema.py           Data model (dataclasses)
│       ├── semver.py           SemVer parsing with pre-release support
│       ├── cache.py            File-based TTL cache (32-char SHA-256 keys)
│       ├── env.py              3-layer config loading
│       ├── http.py             HTTP client (stdlib, retry + backoff)
│       ├── dates.py            Date utilities and recency scoring
│       ├── dedupe.py           Community signal deduplication
│       ├── ignores.py          .depradar-ignore file parser
│       ├── notify.py           Slack / file notification dispatch
│       ├── ui.py               Terminal UI (machine mode, spinners)
│       ├── verbose_log.py      Verbose progress logging
│       └── js_ast_helper.js    Optional Node.js AST helper (acorn)
│
├── tests/                      ← pytest test suite (838 tests, 38 files)
├── fixtures/                   ← Test fixture data (real API response samples)
│
├── hooks/
│   ├── hooks.json              ← SessionStart hook definition
│   └── scripts/
│       └── check-config.sh     Config validator (prints tip if GITHUB_TOKEN missing)
│
├── agents/
│   └── openai.yaml             ← OpenAI Codex CLI compatibility manifest
│
└── .claude-plugin/
    ├── plugin.json             ← Plugin manifest (version, entry point, engines)
    └── marketplace.json        ← ClawHub marketplace metadata
```

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Built to work everywhere. Requires nothing but Python.**

`/depradar` in Claude Code · `python scripts/depradar.py` in your terminal · `--fail-on-breaking` in CI

</div>
