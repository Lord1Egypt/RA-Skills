---
name: deadcode
description: Dead code and unused export detector — scans JavaScript/TypeScript, Python, Go, Java, and CSS for dead code, orphan files, unused exports, and code cruft
homepage: https://deadcode.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udc80",
      "primaryEnv": "DEADCODE_LICENSE_KEY",
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

# DeadCode -- Dead Code & Unused Export Detector

DeadCode scans source files for dead code, unused exports, orphan files, unreachable code paths, and code cruft across JavaScript/TypeScript, Python, Go, and CSS/SCSS. It uses regex-based pattern matching against 60+ dead code patterns, lefthook for git hook integration, and produces markdown reports with actionable cleanup recommendations.

## Commands

### Free Tier (No license required)

#### `deadcode scan [file|directory]`
One-shot dead code scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects language types (JavaScript/TypeScript, Python, Go, CSS/SCSS)
3. Finds all source files matching known patterns
4. Runs 60+ dead code patterns against each file
5. Runs file-level checks for orphan detection and structural issues
6. Calculates a dead code score (0-100) per file and overall
7. Outputs findings with: file, line number, check ID, severity, description, recommendation
8. Exit code 0 if score >= 70, exit code 1 if too much dead code found
9. Free tier limited to 5 source files per scan

**Example usage scenarios:**
- "Scan my code for dead code" -> runs `deadcode scan .`
- "Check this file for unused exports" -> runs `deadcode scan src/utils.ts`
- "Find dead code in my Python project" -> runs `deadcode scan src/`
- "Are there orphan files in my repo?" -> runs `deadcode orphans .`

### Pro Tier ($19/user/month -- requires DEADCODE_LICENSE_KEY)

#### `deadcode hooks install`
Install git pre-commit hooks that scan staged source files before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged source files for dead code, blocks commit if critical/high findings, shows cleanup advice

#### `deadcode hooks uninstall`
Remove DeadCode git hooks.

```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" hooks uninstall
```

#### `deadcode report [directory]`
Generate a markdown dead code report with findings, severity breakdown, and cleanup steps.

```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report from template
4. Includes per-file breakdowns, dead code scores, cleanup priority
5. Output suitable for code reviews and tech debt tracking

#### `deadcode orphans [directory]`
Find orphan files that are never imported or referenced by any other file.

```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" orphans [directory]
```

**What it does:**
1. Validates Pro+ license
2. Builds an import/reference graph across all source files
3. Identifies files that are never imported/required/referenced
4. Excludes entry points (index files, main files, test files, config files)
5. Reports orphan files with confidence levels

### Team Tier ($39/user/month -- requires DEADCODE_LICENSE_KEY with team tier)

#### `deadcode ignore [pattern]`
Manage ignore rules for dead code detection.

```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" ignore [pattern]
```

**What it does:**
1. Validates Team+ license
2. Adds/removes patterns to the ignore list in ~/.openclaw/openclaw.json
3. Patterns can be file globs or check IDs
4. Supports per-project and global ignore rules

#### `deadcode sarif [directory]`
Generate SARIF output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" sarif [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan of the directory
3. Outputs findings in SARIF v2.1.0 format
4. Compatible with GitHub Code Scanning, Azure DevOps, and other CI systems
5. Includes rule definitions, locations, and severity mappings

#### `deadcode status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/deadcode.sh" status
```

## Detected Dead Code Patterns

DeadCode detects 60+ dead code patterns across 5 language categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **JavaScript/TypeScript** | Unused exports, console.log left in code, commented-out blocks, unreachable code after return/throw, empty function bodies, unused variables, dead switch cases, deprecated markers, empty catch blocks | Critical/High |
| **Python** | Functions defined but never called, unused imports, pass-only bodies, commented-out code, dead code after return/raise, __all__ mismatches, empty except blocks | Critical/High |
| **Go** | Unused imports, unexported dead functions, dead code after return/panic, empty function bodies, commented-out code, empty init() functions | High/Medium |
| **CSS/SCSS** | Unused CSS classes/IDs, empty rule blocks, duplicate selectors, commented-out styles, !important overuse, unused CSS variables, empty media queries, vendor prefixes | Medium/Low |
| **General** | Orphan files, large comment blocks, TODO/FIXME density, debug/test code in production, placeholder text, feature flag remnants | High/Medium |

## Configuration

Users can configure DeadCode in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "deadcode": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.spec.*"],
          "ignoreChecks": [],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies
- Supports scanning multiple language types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean (score >= 70), 1 = too much dead code (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://deadcode.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no source files found in target, report clean scan with info message
- If language type cannot be determined, skip the file gracefully

## When to Use DeadCode

The user might say things like:
- "Scan my code for dead code"
- "Find unused exports in my project"
- "Are there orphan files in my repo?"
- "Check for unreachable code"
- "Find commented-out code blocks"
- "Detect unused imports in my Python code"
- "Generate a dead code report"
- "Set up pre-commit hooks for dead code detection"
- "Check for console.log statements left in production"
- "Find empty function bodies"
- "Are there any unused CSS classes?"
- "Scan for TODO/FIXME comments"
- "Find placeholder code"
- "Check for debug code left in production"
- "Generate SARIF output for my CI pipeline"
