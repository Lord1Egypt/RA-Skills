# FeatureLint

> Feature flag hygiene analyzer that catches stale flags, SDK misuse, safety risks, and architecture problems before they reach production.

**Emoji:** flag
**Homepage:** [https://featurelint.pages.dev](https://featurelint.pages.dev)
**Product:** featurelint
**Accent:** #e84393

---

## What It Does

FeatureLint statically analyzes your codebase for feature flag hygiene issues across six categories:

- **Stale Flags (SF)** — Detects hardcoded booleans, TODO-annotated flags, commented-out conditionals, and flags with past date references
- **Flag Complexity (FC)** — Finds nested flag conditions, excessive branching, flag entanglement, and missing caching in loops
- **Flag Safety (FS)** — Warns when flags gate authentication, payments, encryption, data deletion, or audit logging paths
- **SDK Misuse (SM)** — Catches missing default values, loop evaluations, multiple SDK initializations, and missing error handling
- **Flag Lifecycle (FL)** — Identifies flags without cleanup dates, abandoned experiments, 100% rollouts, and missing owner annotations
- **Flag Architecture (FA)** — Detects wrong-layer evaluation, service coupling, missing registries, and leaked server-side state

90 total patterns with POSIX ERE regex matching, severity levels, and actionable recommendations.

---

## Installation

### As a Git Hook (Lefthook)

```yaml
# lefthook.yml
pre-commit:
  commands:
    featurelint:
      glob: "*.{js,jsx,ts,tsx,py,rb,java,go,rs}"
      run: bash path/to/featurelint/scripts/dispatcher.sh staged --severity error
```

### Direct CLI Usage

```bash
# Scan a directory
bash scripts/dispatcher.sh scan ./src

# Scan with JSON output
bash scripts/dispatcher.sh scan --format json --output report.json ./src

# Analyze staged files
bash scripts/dispatcher.sh staged

# Single file analysis
bash scripts/dispatcher.sh file ./src/flags.ts

# Health check
bash scripts/dispatcher.sh health
```

---

## Tier System

| Tier | Patterns | Categories                               | Price       |
|------|----------|------------------------------------------|-------------|
| Free | 30       | Stale Flags + Flag Complexity            | $0          |
| Pro  | 60       | + Flag Safety + SDK Misuse               | $9/month    |
| Team | 90       | + Flag Lifecycle + Flag Architecture     | $29/month   |

Activate a tier by setting your license key:

```bash
export FEATURELINT_LICENSE_KEY="FEATURELINT-XXXX-XXXX-XXXX-XXXX"
```

---

## Commands

| Command     | Description                                         |
|-------------|-----------------------------------------------------|
| `scan`      | Analyze a directory for feature flag issues          |
| `file`      | Analyze a single file                                |
| `staged`    | Analyze git staged files (for pre-commit hooks)      |
| `baseline`  | Create a baseline snapshot of current findings       |
| `compare`   | Compare current findings against the baseline        |
| `health`    | Run self-diagnostic health check                     |
| `version`   | Print version information                            |
| `help`      | Show usage and available options                     |

---

## Options

| Flag                    | Description                                    | Default    |
|-------------------------|------------------------------------------------|------------|
| `-f, --format <fmt>`    | Output format: text, json, csv, markdown       | `text`     |
| `-o, --output <file>`   | Write report to file                           | (stdout)   |
| `-s, --severity <lvl>`  | Minimum severity: error, warning, info, all    | `all`      |
| `-c, --category <cat>`  | Filter by category code                        | `all`      |
| `-t, --tier <tier>`     | License tier: free, pro, team                  | `free`     |
| `-j, --jobs <n>`        | Parallel scan workers                          | `4`        |
| `-i, --include <glob>`  | Include files matching pattern                 | (all)      |
| `-e, --exclude <regex>` | Exclude files matching pattern                 | (none)     |
| `-C, --context <n>`     | Context lines around findings                  | `2`        |
| `--scan-hidden`         | Include hidden files and directories           | `false`    |
| `--warn-exit`           | Exit code 1 on warnings                        | `false`    |
| `-v, --verbose`         | Increase verbosity (-vv for trace)             | `0`        |
| `-q, --quiet`           | Suppress non-essential output                  | `false`    |

---

## Environment Variables

| Variable                | Description                         |
|-------------------------|-------------------------------------|
| `FEATURELINT_LICENSE_KEY` | License key for tier activation   |
| `FEATURELINT_TIER`      | Override tier directly              |
| `FEATURELINT_FORMAT`    | Default output format               |
| `FEATURELINT_SEVERITY`  | Default severity filter             |
| `FEATURELINT_JOBS`      | Default parallel job count          |

---

## Output Formats

### Text (default)
Human-readable terminal output with color-coded severity, file grouping, code context, and actionable fix recommendations.

### JSON
Structured output for CI/CD integration. Includes metadata, summary counters, and a findings array with file, line, severity, check ID, description, and recommendation.

### CSV
Spreadsheet-compatible output for tracking and reporting. One row per finding with all fields.

### Markdown
Report template with summary tables, category breakdown, severity distribution, and a findings table. Uses the `report.md.tmpl` template when available.

---

## Supported Languages

JavaScript, TypeScript, Python, Ruby, Java, Kotlin, Scala, Go, Rust, C#, F#, PHP, Swift, Dart, Vue, Svelte, Elixir, Clojure, Lua, R, YAML, JSON, TOML, XML, Terraform/HCL, and Shell.

---

## Architecture

```
featurelint/
  scripts/
    dispatcher.sh    # CLI entry point and argument parsing
    analyzer.sh      # Core analysis engine and output formatters
    patterns.sh      # 90 patterns across 6 categories
    license.sh       # License validation and tier gating
  config/
    lefthook.yml     # Git hook configuration
  templates/
    report.md.tmpl   # Markdown report template
  SKILL.md           # This file
```

---

## Examples

### CI/CD Integration (GitHub Actions)

```yaml
- name: FeatureLint
  run: |
    bash featurelint/scripts/dispatcher.sh scan \
      --format json \
      --output featurelint-report.json \
      --severity warning \
      ./src
```

### Baseline Workflow

```bash
# Create initial baseline
bash scripts/dispatcher.sh baseline ./src

# After making changes, compare
bash scripts/dispatcher.sh compare ./src
```

### Pre-commit with Error-Only Blocking

```bash
bash scripts/dispatcher.sh staged --severity error
```

---

## Requirements

- Bash 4.0 or later
- Standard POSIX utilities: grep, sed, awk, find, sort, uniq, wc, cut
- Optional: curl (for online license validation), git (for staged analysis)

---

## License

Commercial software. Free tier available with 30 patterns.
See [https://featurelint.pages.dev](https://featurelint.pages.dev) for pricing and terms.
