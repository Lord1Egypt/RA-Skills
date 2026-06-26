---
name: accesslint
description: Web accessibility & WCAG compliance scanner — detects WCAG 2.1 violations, missing ARIA attributes, color contrast issues, keyboard navigation problems, and semantic HTML failures across HTML, JSX, Vue, and Svelte
homepage: https://accesslint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\u267f",
      "primaryEnv": "ACCESSLINT_LICENSE_KEY",
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

# AccessLint — Web Accessibility & WCAG Compliance Scanner

AccessLint scans codebases for WCAG 2.1 violations, missing ARIA attributes, color contrast issues, keyboard navigation problems, form accessibility failures, and semantic HTML anti-patterns. It uses regex-based pattern matching against 95+ accessibility patterns across HTML, JSX, Vue, and Svelte templates. Lefthook integration for git hooks, markdown accessibility reports with WCAG success criterion mapping.

## Commands

### Free Tier (No license required)

#### `accesslint scan [file|directory]`
One-shot accessibility scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects file type from extensions (HTML, JSX, TSX, Vue, Svelte)
3. Finds all template/component files that contain markup
4. Runs 95+ accessibility patterns against each file
5. Calculates an accessibility score (0-100) per file and overall
6. Outputs findings with: file, line number, check ID, severity, WCAG criterion, description, recommendation
7. Exit code 0 if passing (score >= 70), exit code 1 if issues found
8. Free tier limited to 5 files per scan

**Example usage scenarios:**
- "Scan my code for accessibility issues" -> runs `accesslint scan .`
- "Check this component for WCAG violations" -> runs `accesslint scan src/components/Button.tsx`
- "Audit my templates for missing ARIA attributes" -> runs `accesslint scan src/`
- "Are there any accessibility problems in my frontend?" -> runs `accesslint scan .`

### Pro Tier ($19/user/month -- requires ACCESSLINT_LICENSE_KEY)

#### `accesslint hooks install`
Install git pre-commit hooks that scan staged files for accessibility issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged template files for accessibility violations, blocks commit if critical/high findings, shows remediation advice

#### `accesslint hooks uninstall`
Remove AccessLint git hooks.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" hooks uninstall
```

#### `accesslint report [directory]`
Generate a markdown accessibility report with findings, severity breakdown, and WCAG criterion mapping.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report from template
4. Includes per-file breakdowns, accessibility scores, WCAG 2.1 success criterion references
5. Output suitable for accessibility reviews and compliance audits

#### `accesslint audit [directory]`
Deep accessibility audit with component analysis and ARIA coverage checks.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" audit [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs all 95+ patterns including framework-specific and dynamic content patterns
3. Analyzes component-level accessibility coverage
4. Reports ARIA attribute completeness across the codebase
5. Provides heading hierarchy and landmark region analysis

### Team Tier ($39/user/month -- requires ACCESSLINT_LICENSE_KEY with team tier)

#### `accesslint policy [directory]`
Enforce organization-specific accessibility policies on codebases.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" policy [directory]
```

**What it does:**
1. Validates Team+ license
2. Loads custom policies from ~/.openclaw/openclaw.json (accesslint.config.customPolicies)
3. Enforces organization-specific rules (e.g., required ARIA patterns, banned inaccessible patterns, mandatory alt text)
4. Combines custom policies with built-in patterns for comprehensive scanning
5. Outputs SARIF-compatible results

#### `accesslint sarif [directory]`
Generate SARIF JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" sarif [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan of the directory
3. Outputs findings in SARIF 2.1.0 JSON format
4. Compatible with GitHub Code Scanning, Azure DevOps, and other SARIF consumers

#### `accesslint wcag [directory]`
Generate WCAG 2.1 AA/AAA compliance report.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" wcag [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan with all patterns
3. Maps findings to WCAG 2.1 success criteria (Level A, AA, AAA)
4. Generates comprehensive compliance report with pass/fail per criterion
5. Includes executive summary, detailed findings, and remediation roadmap

#### `accesslint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/accesslint.sh" status
```

## Detected Violations

AccessLint detects 95+ accessibility patterns across 6 categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **Missing ARIA & Roles** | Images without alt, buttons without accessible names, inputs without labels, icon-only buttons without aria-label, SVG without title/role, links with no text content | Critical/High |
| **Semantic HTML Issues** | div/span used as button/link, nested interactive elements, heading hierarchy violations, multiple h1 tags, missing lang attribute, missing document title | Critical/High |
| **Keyboard Navigation** | Click handlers without keyboard equivalent, mouseOnly events, missing focus styles, tabindex misuse, focus traps without escape | High/Medium |
| **Form Accessibility** | Inputs without associated labels, missing fieldset/legend, placeholder-only labels, required fields without aria-required, error messages not linked | Critical/High |
| **Color & Visual** | Color-only information, potential low contrast patterns, missing prefers-reduced-motion, animations without motion preference | High/Medium |
| **Dynamic Content** | Live regions without aria-live, loading states without announcements, modals without focus management, toast/notification without role=alert | High/Medium |

## Configuration

Users can configure AccessLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "accesslint": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "customPolicies": [],
          "excludePatterns": ["**/test/**", "**/examples/**", "**/storybook/**"],
          "wcagLevel": "AA",
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
- Supports scanning multiple template formats in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = passing (score >= 70), 1 = issues found (for CI/CD integration)
- Addresses WCAG 2.1 Level A, AA, and AAA success criteria

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://accesslint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If file type cannot be determined from extension, skip the file gracefully

## When to Use AccessLint

The user might say things like:
- "Scan my code for accessibility issues"
- "Check for WCAG violations in my frontend"
- "Are there any missing ARIA attributes in my components?"
- "Audit my templates for accessibility problems"
- "Check if my forms have proper labels"
- "Scan for keyboard navigation issues"
- "Check my React components for a11y issues"
- "Generate an accessibility report"
- "Set up pre-commit hooks for accessibility"
- "Check for missing alt text on images"
- "Are there any heading hierarchy problems?"
- "Scan for color contrast issues"
- "Run WCAG compliance checks on my templates"
