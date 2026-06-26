---
name: depradar
description: Dependency breaking-change radar. Use this skill when the user wants to check for breaking changes, outdated dependencies, upgrade risks, or migration issues. Triggers on /depradar, or when users ask about dependency updates, breaking changes, semver bumps, or safe upgrade paths. Scans package.json, requirements.txt, pyproject.toml, go.mod, Cargo.toml, Gemfile, pom.xml for outdated packages, extracts breaking changes from release notes, finds impacted files in the codebase, and surfaces community pain signals from GitHub Issues, Stack Overflow, Reddit, and Hacker News.
---

# /depradar

> Scan your project's dependencies for breaking changes, find which files in YOUR codebase will break, and surface community reports from GitHub, Stack Overflow, Reddit, and Hacker News — all in one command.

---

## What This Skill Does

`/depradar` is a dependency intelligence tool that goes far beyond `npm outdated` or `pip list --outdated`. When you run it:

1. **Reads your dependency files** — `package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, and more
2. **Checks every registry** — npm, PyPI, GitHub Releases, crates.io, Maven Central — for new versions
3. **Extracts breaking changes** — parses release notes and CHANGELOGs using section-header detection, Conventional Commits (`feat!:`, `BREAKING CHANGE:`), and keyword heuristics
4. **Scans YOUR codebase** — Python: full AST analysis (high confidence). JS/TS: import-tracking regex with package context (medium confidence) + optional true AST via Node.js if available (high confidence). Other languages: grep fallback
5. **Searches the community** — GitHub Issues, Stack Overflow, Reddit, and Hacker News for migration pain reports
6. **Scores and ranks** — severity × recency × codebase impact × community pain (0-100 scale)
7. **Delivers an actionable report** — tells you what broke, where it broke in your code, and what others did to fix it

---

## Invocation

```
/depradar                           # Scan current project, all production deps
/depradar stripe openai             # Check only these specific packages
/depradar --all                     # Include devDependencies / dev extras
/depradar --quick                   # 60s timeout, top 5 packages by severity
/depradar --deep                    # 300s, exhaustive community search
/depradar --days=7                  # Changes in last 7 days (default: 30)
/depradar --refresh                 # Bypass 6-hour cache, force fresh data
/depradar --emit=json               # Output: compact (default) | json | md | context
/depradar --emit=md                 # Save full markdown report to ~/Documents/DepRadar/
/depradar --diagnose                # Show API key status + test validity
/depradar --mock                    # Use fixtures (testing, no network calls)
/depradar --no-scan                 # Skip codebase impact scan (faster)
/depradar --no-community            # Skip community signal search
/depradar --save                    # Auto-save markdown report
/depradar --save-dir=PATH           # Save report to custom directory
/depradar --path=PATH               # Scan a different project directory
/depradar --verbose                 # Show detailed per-step progress
/depradar --fail-on-breaking        # Exit code 1 if breaking changes found (CI/CD)
/depradar --min-score=N             # Only show packages with score >= N (default: 0)
/depradar --notify=slack://WEBHOOK  # Send report to Slack webhook
/depradar --notify=file:///PATH     # Write JSON report to file
/depradar --show-ignored            # Show packages suppressed by .depradar-ignore
/depradar --version                 # Show version
```

---

## Step-by-Step Instructions for Claude

This section describes exactly how Claude should execute this skill. Follow each step in order.

---

### Step 0: Understand What the User Wants

Before running anything, parse the invocation to understand:

**Package filtering:** If the user named specific packages (e.g., `/depradar stripe openai`), note these. The script will filter to only those packages.

**Flag mapping:**
- `--quick` → `--depth=quick` (60s timeout, top 5 packages)
- `--deep` → `--depth=deep` (300s timeout, exhaustive)
- `--days=N` → look back N days for new releases (default: 30)
- `--refresh` → bypass cache
- `--no-scan` → skip codebase impact scan
- `--no-community` → skip community signal search
- `--emit=FORMAT` → output format (compact, json, md, context)
- `--save` → save markdown to ~/Documents/DepRadar/
- `--diagnose` → show config status and exit
- `--mock` → use fixture data, no network calls

**User intent signals:** If the user says "check if openai is broken" — that means `/depradar openai`. If they say "what needs updating in this project" — that's `/depradar`. If they say "why is my stripe code failing after update" — that's `/depradar stripe --deep`.

---

### Step 1: Locate the Script

The skill's main Python script is at:
```
{SKILL_ROOT}/scripts/depradar.py
```

Where `{SKILL_ROOT}` is the directory containing this `SKILL.md` file.

To find `SKILL_ROOT` dynamically:
```bash
SKILL_ROOT="$(dirname "$(realpath "${BASH_SOURCE[0]:-$0}")")"
```

If Claude is running this directly (not via bash), find the skill root by looking for the directory that contains both `SKILL.md` and `scripts/depradar.py`.

The typical installed locations are:
- `~/.claude/skills/depradar-skill/` (Claude Code)
- `~/.codex/skills/depradar-skill/` (OpenAI Codex)
- `~/.agents/skills/depradar-skill/` (generic)

---

### Step 2: Check Prerequisites

Before running, verify Python 3.8+ is available:
```bash
python3 --version
```

If Python is not available, tell the user:
> "Python 3.8+ is required. Please install it from python.org or via your package manager."

No external pip packages are required — the skill uses only Python stdlib.

---

### Step 3: Run the Script

**Basic invocation:**
```bash
cd "{PROJECT_ROOT}" && python3 "{SKILL_ROOT}/scripts/depradar.py" {ARGS}
```

**Important:** Always `cd` to the project root first. The script uses the current working directory to find dependency files and scan the codebase.

**Examples:**

Run with default settings:
```bash
cd /path/to/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py
```

Check specific packages only:
```bash
cd /path/to/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py stripe openai
```

Quick scan with JSON output:
```bash
cd /path/to/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py --quick --emit=json
```

Show config status:
```bash
python3 ~/.claude/skills/depradar-skill/scripts/depradar.py --diagnose
```

Test with mock data (no network):
```bash
cd /path/to/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py --mock
```

---

### Step 4: Parse the Output

The script outputs to stdout. The output format depends on `--emit`:

**`compact` (default):** Human-readable terminal output. Parse it by looking for:
- Lines starting with `### ` → package name + version bump
- Lines containing `**Impact:**` → codebase impact count
- Lines starting with `    -` under `**Impact:**` → file:line references
- Lines starting with `    N.` under `**Breaking changes:**` → individual breaking changes
- Lines under `**Community signals:**` → external reports

**`json`:** Full machine-readable JSON. The structure is `DepRadarReport`:
```json
{
  "project_path": "/path/to/project",
  "packages_scanned": 23,
  "packages_with_breaking_changes": [
    {
      "id": "P1",
      "package": "stripe",
      "current_version": "7.0.0",
      "latest_version": "8.0.0",
      "semver_type": "major",
      "has_breaking_changes": true,
      "score": 87,
      "breaking_changes": [...],
      "impact_locations": [...],
      "impact_confidence": "high"
    }
  ],
  "packages_with_minor_updates": [...],
  "packages_current": ["axios", "lodash", ...],
  "github_issues": [...],
  "stackoverflow": [...],
  "reddit": [...],
  "hackernews": [...],
  "from_cache": false,
  "cache_age_hours": null,
  "depth": "default",
  "days_window": 30
}
```

**`context`:** Minimal snippet for passing to other skills or continuing a conversation.

**`md`:** Full markdown — best for saving to file.

---

### Step 5: Synthesize and Present to the User

After the script completes, Claude should present the findings in a clear, actionable way. Follow these principles:

**Lead with the action items.** The user needs to know: "Do I need to update anything? Will it break my code? How hard is the migration?"

**Structure your response:**

1. **One-line summary** — "Found 2 packages with breaking changes affecting 7 files in your codebase."

2. **For each breaking package** (in score order):
   - Package name, current → latest version, days since release
   - Files in their codebase that will break (from `impact_locations`)
   - What specifically changed (from `breaking_changes`)
   - Migration guidance (from `migration_note` fields or community signals)
   - Community pain level (how many others hit this)

3. **Minor updates table** — brief, just show what's available

4. **Follow-up offers** — see Step 6

**What to emphasize:**
- Impact locations in THEIR code (most actionable)
- Packages with score > 70 (high priority)
- Migration notes from the release notes
- StackOverflow questions that are ANSWERED (solved problems)
- GitHub issues that are CLOSED (resolved)

**What to de-emphasize:**
- Packages not found in registry (usually private packages)
- Community signals for packages with score < 30
- Minor/patch updates unless they contain security fixes

**Tone:** Be specific, not alarming. "stripe v8 removed `webhooks.constructEvent()` — replace it with `webhooks.verify()` on line 47 of `src/payments/webhook.ts`" is much better than "Breaking changes detected!"

---

### Step 6: Offer Follow-up Actions

After presenting the report, always offer one or more of these follow-up actions:

**For packages with breaking changes:**
- "Would you like me to help you migrate `src/payments/webhook.ts` from `stripe.webhooks.constructEvent()` to the new API?"
- "I can show you the diff between stripe v7 and v8 for the methods you're using."
- "Want me to run `npm update stripe` and then fix the breaking usages automatically?"

**For the full report:**
- "Shall I save this as a markdown report to `~/Documents/DepRadar/`? Run `/depradar --emit=md`."
- "Want me to create a GitHub issue tracking these breaking changes?"
- "I can add `/* TODO: migrate stripe v8 */` comments to the affected lines."

**For configuration:**
- "Add `GITHUB_TOKEN` to `~/.config/depradar/.env` to get 80x more GitHub API requests and better issue search."
- "Add `SCRAPECREATORS_API_KEY` to enable Reddit community signal search."

---

### Step 7: Handle Errors Gracefully

**No dependency files found:**
> "No dependency files found in `{PROJECT_ROOT}`. Make sure you're in your project root directory. Supported files: `package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`."

**All packages up to date:**
> "All {N} dependencies are up to date — no action needed."

**GitHub rate limit (60/hour without token):**
> "GitHub API rate limit reached. Add `GITHUB_TOKEN` to `~/.config/depradar/.env` for 5,000 requests/hour. Run `/depradar --diagnose` to check your config."

**Script not found:**
> "Could not find `depradar.py`. Make sure the skill is installed: copy the `depradar-skill/` directory to `~/.claude/skills/`. Run `bash ~/.claude/skills/depradar-skill/scripts/sync.sh` to install."

**Python not found:**
> "Python 3.8+ is required. Install from python.org or via: `brew install python3` (Mac) / `sudo apt install python3` (Linux)."

**Cache is stale:**
> "Using cached results from {N} hours ago. Run `/depradar --refresh` to fetch fresh data."

---

## Configuration

`/depradar` works out of the box with no configuration. API keys unlock additional sources and higher rate limits.

### Config File Location

Create either of:
- `.claude/depradar.env` — project-level (check this into `.gitignore`)
- `~/.config/depradar/.env` — global (applies to all projects)

### API Keys Reference

| Key | Purpose | Without Key | With Key |
|-----|---------|------------|---------|
| `GITHUB_TOKEN` | GitHub Releases + Issues | 60 req/hr | 5,000 req/hr |
| `SCRAPECREATORS_API_KEY` | Reddit search | ❌ disabled | ✅ enabled |
| `XAI_API_KEY` | X/Twitter via Grok | ❌ disabled | ✅ enabled |
| `AUTH_TOKEN` + `CT0` | X/Twitter via cookies | ❌ disabled | ✅ enabled |
| `STACKOVERFLOW_API_KEY` | Stack Overflow | 300/day | 10,000/day |

### Example Config File

```bash
# ~/.config/depradar/.env

# Strongly recommended — free at github.com/settings/tokens
# Scopes needed: (none — public repos only)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# From scrapecreators.com — enables Reddit community signals
SCRAPECREATORS_API_KEY=sc_xxxxxxxxxxxx

# From x.ai — enables X/Twitter signals
XAI_API_KEY=xai_xxxxxxxxxxxx

# From stackapps.com — 33x rate limit increase for Stack Overflow
STACKOVERFLOW_API_KEY=xxxxxxxxxxxx
```

### Suppressing Known-Safe Breaking Changes

Create a `.depradar-ignore` file in your project root to suppress evaluated breaking changes:

```
# .depradar-ignore
# Format: package[@version]  # optional reason comment
chalk@5          # ESM-only, evaluated 2026-03-27 — only used in CLI output
dotenv@17        # uses config() only, unchanged API
stripe           # all versions suppressed (use with care)
```

- `chalk@5` — suppresses chalk at any 5.x.x version
- `chalk@5.3.0` — exact version only
- `chalk` — suppress all versions (use carefully)

A global ignore file at `~/.config/depradar/ignore` applies to all projects.
Run `--show-ignored` to see what's being suppressed.

---

### Zero-Config Coverage

Without any API keys, `/depradar` still covers:
- ✅ All dependency file parsing (local, no network)
- ✅ npm Registry (no auth required, very high rate limits)
- ✅ PyPI API (no auth required)
- ✅ crates.io API (no auth required)
- ✅ Maven Central (no auth required)
- ✅ GitHub Releases (60 req/hr — enough for 10-15 packages)
- ✅ GitHub Issues search (60 req/hr shared with above)
- ✅ Stack Overflow (300/day — limited but functional)
- ✅ Hacker News (historical data, no auth)
- ❌ Reddit (requires SCRAPECREATORS_API_KEY)
- ❌ X/Twitter (requires XAI_API_KEY or cookies)

**Zero-config covers ~80% of the skill's value.**

---

## Dependency File Support

| File | Ecosystem | Notes |
|------|-----------|-------|
| `package.json` | npm | Production deps; add `--all` for devDependencies |
| `package-lock.json` | npm | Exact locked versions (v2/v3 format) |
| `yarn.lock` | npm | Exact locked versions (v1 format) |
| `pnpm-lock.yaml` | npm | Exact locked versions (v5/v6/v8 format) |
| `requirements.txt` | PyPI | Handles `==`, `>=`, `~=`, `!=` specifiers |
| `pyproject.toml` | PyPI | PEP 621 `[project].dependencies` |
| `Pipfile` | PyPI | Pipenv format |
| `setup.cfg` | PyPI | Legacy `install_requires` and `extras_require` |
| `go.mod` | Go | Standard Go modules |
| `Cargo.toml` | Rust/crates.io | Standard Cargo format |
| `Gemfile` | Ruby/rubygems | Handles `gem` directives |
| `pom.xml` | Java/Maven | `<dependency>` elements |

The script searches from the current directory upward to the git root, collecting all dep files found.

---

## Scoring System

Every package and community signal is scored 0-100.

### Package Score (Breaking Changes)

```
score = 0.35 × severity + 0.25 × recency + 0.30 × impact + 0.10 × community
```

**Severity** (based on change_type):
| Change Type | Score |
|-------------|-------|
| `removed` | 100 |
| `renamed` | 80 |
| `signature_changed` | 70 |
| `behavior_changed` | 60 |
| `type_changed` | 50 |
| `deprecated` | 40 |
| `other` | 30 |

**Recency** (days since release):
| Age | Score |
|-----|-------|
| 0-7 days | 100 |
| 8-14 days | 85 |
| 15-30 days | 65 |
| 31-60 days | 40 |
| 61-90 days | 25 |
| 91+ days | 10 |

**Impact** (YOUR codebase):
| Detection | Score |
|-----------|-------|
| High-confidence (AST) | 100 |
| Med-confidence (grep) | 70 |
| Low-confidence | 40 |
| Not scanned | 50 |
| Not found after scan | 10 |

**Community pain:**
```
community = min(100, log1p(weighted_pain_signals) × 12)
```
Where `weighted_pain_signals` sums `quality_weight` for each signal (closed+answered=2.0, closed=1.5, open+no comments=0.8). Only signals mentioning the same major version are counted (version-range filtered).

**Two-phase scoring:** Community signals (GitHub Issues, SO, Reddit, HN) are fetched in parallel AFTER the initial registry scan. The final score is calculated once all signals are available. Minor/patch releases are also checked for breaking changes — if found, they are flagged with a SEMVER VIOLATION badge.

**Staleness bonus:** If a breaking change has been available >30 days and you haven't upgraded, the urgency score increases (0-40 bonus points). Packages with 90+ day-old unaddressed breaking changes get a ⚡ STALE badge.

### Interpreting Scores

| Score | Meaning |
|-------|---------|
| 80-100 | 🔴 Critical — breaking change directly hits your code, recently released, widely reported |
| 60-79 | 🟠 High — significant breaking change, likely affects your code |
| 40-59 | 🟡 Medium — breaking change in this major, but impact uncertain |
| 20-39 | 🟢 Low — older or obscure breaking change |
| 0-19 | ⚪ Minimal — very minor or unconfirmed |

---

## Output Formats

### compact (default)

Best for reading in the terminal. Shows:
- Package summary header with scan stats
- Breaking packages section with full details
- Minor updates table (capped at 10)
- Up-to-date count
- Registry errors

### json

Full machine-readable JSON dump of the `DepRadarReport` dataclass. Use this when:
- Passing results to another script or tool
- Building automation pipelines
- Debugging the skill

### md

Full markdown report. Suitable for:
- Saving to a file: `/depradar --emit=md` auto-saves to `~/Documents/DepRadar/`
- Pasting into GitHub issues or PRs
- Sharing with a team

### context

Minimal snippet for Claude-to-Claude passing. Use this when:
- Another skill needs to know about breaking changes
- You want to reference the results without the full report

---

## Depth Profiles

| Flag | Timeout | Packages | Community depth | Use case |
|------|---------|----------|-----------------|---------|
| `--quick` | 60s | Top 5 by severity | Minimal | CI/CD, quick check |
| (default) | 180s | All | Standard | Regular use |
| `--deep` | 300s | All | Exhaustive | Before a major release |

---

## Caching

Results are cached to avoid hammering APIs:
- Reports: 6-hour TTL (`~/.cache/depradar/reports/`)
- Registry data: 6-hour TTL
- Community signals: 24-hour TTL
- Codebase scan: 1-hour TTL

Use `--refresh` to bypass all caches.

The cache key includes a project path hash to prevent cache collisions across different projects with the same packages. Registry data (package info) is project-agnostic and shared; scan/report caches are project-specific.

---

## Examples

### Example 1: Default scan of a Node.js project

```
/depradar
```

Claude runs:
```bash
cd /current/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py
```

Expected output includes:
- How many packages were scanned (from `package.json`)
- Any major version bumps with breaking changes
- File:line impact in the project
- Community reports

---

### Example 2: Check a specific package before upgrading

User: "Is it safe to upgrade stripe to v8?"

Claude runs:
```bash
cd /current/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py stripe --deep
```

Then synthesizes the result into:
- What changed in stripe v8 that will break things
- Which files in the project will be affected
- Community reports on migration difficulty
- Concrete migration steps

---

### Example 3: CI/CD integration — check before deploy

User: "Add depradar to my CI pipeline"

Claude suggests adding to `.github/workflows/ci.yml`:
```yaml
- name: Check for breaking dependency changes
  run: |
    python3 ~/.claude/skills/depradar-skill/scripts/depradar.py \
      --quick --emit=json --no-community \
      | python3 -c "
    import json, sys
    report = json.load(sys.stdin)
    breaking = report['packages_with_breaking_changes']
    if breaking:
        print(f'BREAKING: {len(breaking)} packages have breaking changes')
        for pkg in breaking:
            print(f'  - {pkg[\"package\"]}: {pkg[\"current_version\"]} → {pkg[\"latest_version\"]}')
        sys.exit(1)
    print('All dependencies OK')
    "
```

---

### Example 4: Check config

```
/depradar --diagnose
```

Claude runs:
```bash
python3 ~/.claude/skills/depradar-skill/scripts/depradar.py --diagnose
```

Output shows which API keys are configured and what coverage they unlock.

---

### Example 5: Save full report

```
/depradar --emit=md
```

Claude runs:
```bash
cd /current/project && python3 ~/.claude/skills/depradar-skill/scripts/depradar.py --emit=md
```

The script saves `~/Documents/DepRadar/myproject-2026-03-27.md` and prints the path.

---

### Example 6: Check multiple ecosystems at once

In a project with both `package.json` and `requirements.txt`:
```
/depradar
```

The script auto-detects both files, combines the dependency list, checks npm + PyPI registries in parallel, and presents a unified report.

---

### Example 7: Use context mode for chaining with other skills

```
/depradar --emit=context
```

Output is a compact snippet like:
```
[/depradar context — 2 breaking change(s) detected]

• stripe 7.0.0→8.0.0 (major)
  - removed: stripe.webhooks.constructEvent — Method removed
  - Impact: 2 file(s) in your codebase

• openai 0.28.0→1.35.0 (major)
  - removed: openai.Completion.create — Class removed in v1
  - Impact: 5 file(s) in your codebase
```

Claude can then use this context to automatically open the affected files and propose migrations.

---

## Troubleshooting

### "No dependency files found"

Make sure you're in the project root:
```bash
ls package.json requirements.txt pyproject.toml go.mod Cargo.toml
```

Pass the project path explicitly:
```bash
/depradar --path=/path/to/project
```

### "GitHub API rate limit"

Without a token, GitHub allows 60 requests/hour. Each package needs 1-3 requests.

Fix: Add `GITHUB_TOKEN` to `~/.config/depradar/.env`:
```bash
echo "GITHUB_TOKEN=ghp_yourtoken" >> ~/.config/depradar/.env
```

Get a token at: github.com/settings/tokens (no scopes needed for public repos)

### Results look stale

The 6-hour cache might be serving old results. Force refresh:
```bash
/depradar --refresh
```

### A package shows as "not found"

This happens for:
- Private/internal packages (not on public registries)
- Packages with non-standard names (e.g., `@company/internal-lib`)
- Go packages (requires GitHub token to look up)

These are listed in the "Not found in registry" section and can be ignored.

### Python import errors

If you see `ModuleNotFoundError` for lib modules, make sure you're running from the correct directory or using the full path to `depradar.py`:
```bash
cd /path/to/project && python3 /full/path/to/depradar-skill/scripts/depradar.py
```

### "Permission denied" on check-config.sh

```bash
chmod +x ~/.claude/skills/depradar-skill/hooks/scripts/check-config.sh
```

---

## Privacy and Security

- `/depradar` only reads dependency file names and version numbers, NOT your code contents (beyond scanning for symbol names)
- No code is sent to any external service
- Community searches use only the package name and version number as queries
- API tokens are read from local files only and never transmitted except as Authorization headers to their respective APIs
- The codebase scan runs entirely locally using Python's `ast` module and file reading

---

## Architecture Overview

```
/depradar invocation
      │
      ▼
 dep_parser.py          ← Reads package.json, requirements.txt, etc.
      │
      ▼
 [Phase 1: Registry] ──────────────────────────────────────── PARALLEL
 github_releases.py     ← Primary: full release notes + CHANGELOG.md
 npm_registry.py        ← npm metadata + latest version
 pypi_registry.py       ← PyPI metadata + latest version
 crates_registry.py     ← crates.io metadata
 maven_registry.py      ← Maven Central metadata
      │
      ▼
 changelog_parser.py    ← Extract BreakingChange[] from release notes
      │
      ▼
 [Phase 2: Codebase Scan] ──────────────────────────────────── PARALLEL (per package)
 usage_scanner.py       ← AST (Python/JS) + grep fallback
 impact_analyzer.py     ← Cross-reference symbols with your code
      │
      ▼
 [Phase 3: Community] ──────────────────────────────────────── PARALLEL
 github_issues.py       ← GitHub Issues Search API
 stackoverflow.py       ← Stack Exchange API
 reddit_sc.py           ← Reddit via ScrapeCreators
 hackernews.py          ← HN Algolia (historical) + Firebase API
 twitter_x.py           ← X/Twitter via xAI Grok (optional)
      │
      ▼
 score.py               ← Severity × Recency × Impact × Community (0-100)
 normalize.py           ← Min-max normalization per source
 dedupe.py              ← Trigram Jaccard deduplication
      │
      ▼
 render.py              ← compact | json | md | context output
```

---

## Version History

See `CHANGELOG.md` for detailed release notes.

Current version: **2.0.0**

---

## License

MIT — see `LICENSE` file.

---

## Related Skills

- `/last30days` — Search what happened on the internet in the last 30 days about any topic
- `/security-audit` — Scan for known CVEs in your dependencies (pairs well with /depradar)

---

## Contributing

Issues and PRs welcome. See `SPEC.md` for the full architecture specification.

---

*Built with the Claude Code Skills architecture. Modeled after the `/last30days` skill pattern.*
