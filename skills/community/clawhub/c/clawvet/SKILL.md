---
name: clawvet
version: 0.6.3
description: Code quality and safety linter for OpenClaw skills. Runs 6 analysis passes before you install.
author: MohibShaikh
license: MIT
homepage: https://github.com/MohibShaikh/clawvet
repository: https://github.com/MohibShaikh/clawvet
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
      env: []
    category: security
    tags:
      - security
      - linter
      - supply-chain
      - code-quality
---

# clawvet

Safety linter for OpenClaw skills. Analyzes skills for issues before installation.

## Usage

Scan a local skill:

```bash
npx clawvet scan ./skill-folder/
```

JSON output for CI/CD:

```bash
npx clawvet scan ./skill-folder/ --format json
```

Audit all installed skills:

```bash
npx clawvet audit
```

Watch mode — auto-block risky installs:

```bash
npx clawvet watch --threshold 50
```

Submit feedback or get alerts:

```bash
npx clawvet feedback
```

## Analysis Passes

1. **Skill Parser** — Extracts YAML frontmatter, code blocks, URLs, and domains
2. **Static Analysis** — 54 pattern rules across multiple categories
3. **Metadata Validator** — Checks for undeclared binaries, env vars, missing descriptions
4. **Dependency Checker** — Flags auto-install and global package installs
5. **Typosquat Detector** — Levenshtein distance against popular skill names
6. **Semantic Analysis** — AI-powered contextual analysis (Pro)

## What's New in v0.6

- **Reliable telemetry** — Telemetry now awaits before exit, so no data is lost.
- **CI-safe** — Opt-in prompt is skipped in non-TTY environments (piped stdin, CI).
- **Less noise** — Feedback CTA shows every 5th scan instead of every scan.
- **Trust badges** — Generate trust badges for skill READMEs with `npx clawvet badge`.
- **Ban lists** — Block skills by name/author/slug via `.clawvetban` files.
- **Confidence scores** — Each finding shows a confidence percentage. Risk scores are weighted accordingly.
- **Fix suggestions** — Every finding includes an actionable remediation in terminal and SARIF output.
- **Content-hash caching** — Repeat scans of unchanged files are near-instant.
- **Feedback form** — Run `npx clawvet feedback` to share what you think.

## Risk Grades

| Score | Grade | Action |
|-------|-------|--------|
| 0-10 | A | Safe to install |
| 11-25 | B | Safe to install |
| 26-50 | C | Review before installing |
| 51-75 | D | Review carefully |
| 76-100 | F | Do not install |
