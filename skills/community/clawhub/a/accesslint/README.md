# accesslint

<p align="center">
  <img src="https://img.shields.io/badge/patterns-95+-blue" alt="95+ patterns">
  <img src="https://img.shields.io/badge/formats-4-purple" alt="4 formats">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
  <img src="https://img.shields.io/badge/WCAG-2.1-orange" alt="WCAG 2.1">
</p>

<h3 align="center">Catch accessibility failures before your users do.</h3>

<p align="center">
  <a href="https://accesslint.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-formats">Formats</a> &middot;
  <a href="https://accesslint.pages.dev/#pricing">Pricing</a>
</p>

---

## Accessibility is not optional. In 2025.

It happens on every project. An image without alt text. A button made from a div. A form input with no label. A click handler with no keyboard equivalent. A modal that traps focus with no escape.

WCAG 2.1 is the global standard for web accessibility, and lawsuits for non-compliance have increased 300% since 2018. The automated scanner catches it in staging. After the complaint.

**AccessLint catches accessibility violations before they leave your machine.** Pre-commit hooks. Local scanning. 95+ patterns across HTML, JSX, Vue, and Svelte. Zero data leaves your laptop.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install accesslint

# 2. Scan your repo
accesslint scan

# 3. Install pre-commit hooks (Pro)
accesslint hooks install
```

That's it. Every commit is now scanned for accessibility violations.

## What It Does

### Scan templates for accessibility violations
One command to scan any file, directory, or your entire repo. 95+ regex patterns detect missing ARIA attributes, semantic HTML failures, keyboard navigation gaps, form accessibility issues, color/visual problems, and dynamic content failures across HTML, JSX, Vue, and Svelte.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged template file. If an accessibility violation is detected, the commit is blocked with a clear remediation message.

### Generate accessibility reports
Produce markdown reports with severity breakdowns, WCAG 2.1 success criterion mapping, and remediation steps. Ideal for accessibility reviews and compliance audits.

### Deep accessibility audits
Analyze component-level accessibility, ARIA coverage, heading hierarchy, landmark regions, and form labeling patterns with the deep audit command.

### Enforce accessibility policies
Define organization-specific policies (required alt text, banned inaccessible patterns, mandatory ARIA labels) and enforce them alongside the built-in 95+ patterns.

### WCAG 2.1 compliance reports
Generate comprehensive reports mapping findings to WCAG 2.1 success criteria (Level A, AA, AAA) with executive summaries, detailed findings, and remediation roadmaps.

## How It Compares

| Feature | AccessLint | axe-core ($0/$$) | pa11y ($0) | WAVE ($0/$$) | Lighthouse ($0) | eslint-plugin-jsx-a11y ($0) |
|---------|:----------:|:-----------------:|:----------:|:------------:|:---------------:|:---------------------------:|
| Static template scanning | Yes | No (runtime) | No (runtime) | No (runtime) | No (runtime) | JSX only |
| HTML file scanning | Yes | No | Yes | Yes | Yes | No |
| JSX/TSX scanning | Yes | No | No | No | No | Yes |
| Vue SFC scanning | Yes | No | No | No | No | No |
| Svelte scanning | Yes | No | No | No | No | No |
| Missing ARIA detection | Yes | Yes | Partial | Yes | Partial | Yes |
| Semantic HTML checks | Yes | Yes | Partial | Yes | Partial | Partial |
| Keyboard navigation | Yes | Partial | Partial | Partial | Yes | Partial |
| Form accessibility | Yes | Yes | Partial | Yes | Partial | Yes |
| Dynamic content a11y | Yes | Yes | No | Partial | No | No |
| Pre-commit hooks | Yes | No | No | No | No | Yes |
| Zero config scan | Yes | Config needed | Config needed | N/A | N/A | Config needed |
| WCAG criterion mapping | Yes | Yes | Yes | Yes | Partial | Partial |
| Offline license validation | Yes | N/A | N/A | N/A | N/A | N/A |
| Local-only (no browser) | Yes | No | No | No | No | Yes |
| Zero telemetry | Yes | Yes | Yes | No | No | Yes |
| ClawHub integration | Yes | No | No | No | No | No |
| Price (individual) | Free/$19/mo | Free/$400+/yr | Free | Free/$100/yr | Free | Free |

## Supported Formats

AccessLint detects 95+ accessibility patterns across 4 template formats:

### HTML

| Check | Severity | WCAG | Description |
|-------|----------|------|-------------|
| Missing img alt | Critical | 1.1.1 | Images without alt attribute |
| Missing lang attribute | Critical | 3.1.1 | HTML document without lang |
| Missing document title | High | 2.4.2 | Page without title element |
| Heading hierarchy skip | High | 1.3.1 | Skipping heading levels (h1 to h3) |
| Form input without label | Critical | 1.3.1 | Input elements without associated labels |

### JSX / TSX (React)

| Check | Severity | WCAG | Description |
|-------|----------|------|-------------|
| onClick without onKeyDown | High | 2.1.1 | Click handlers missing keyboard equivalent |
| Missing key on list items | Medium | 4.1.1 | Dynamic lists without unique keys |
| aria-hidden on focusable | Critical | 4.1.2 | Hidden elements that remain focusable |
| Icon button without label | Critical | 4.1.2 | Buttons with only icon content, no accessible name |

### Vue Single File Components

| Check | Severity | WCAG | Description |
|-------|----------|------|-------------|
| v-html accessibility | High | 4.1.1 | v-html may inject inaccessible content |
| Missing template lang | Medium | 3.1.1 | Missing lang on root element |
| @click without @keydown | High | 2.1.1 | Click binding without keyboard equivalent |

### Svelte Components

| Check | Severity | WCAG | Description |
|-------|----------|------|-------------|
| on:click without on:keydown | High | 2.1.1 | Click event without keyboard event |
| Missing a11y attributes | High | 4.1.2 | Interactive elements without ARIA |
| {@html} accessibility | High | 4.1.1 | Raw HTML injection may be inaccessible |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot accessibility scan | 5 files | Unlimited | Unlimited |
| 95+ detection patterns | Yes | Yes | Yes |
| Auto-detect file types | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Accessibility reports | | Yes | Yes |
| Deep accessibility audit | | Yes | Yes |
| Policy enforcement | | | Yes |
| WCAG compliance reports | | | Yes |
| SARIF output | | | Yes |
| CI/CD integration | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "accesslint": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "wcagLevel": "AA",
          "customPolicies": [
            {
              "regex": "<img[^>]*(?!alt=)",
              "severity": "critical",
              "description": "All images must have alt attributes"
            }
          ],
          "excludePatterns": ["**/test/**", "**/examples/**"]
        }
      }
    }
  }
}
```

## Ecosystem

AccessLint is part of the ClawHub quality suite:

- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[SQLGuard](https://sqlguard.pages.dev)** -- SQL query safety & injection risk scanning
- **[AccessLint](https://accesslint.pages.dev)** -- Web accessibility & WCAG compliance scanning

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies

## License

MIT
