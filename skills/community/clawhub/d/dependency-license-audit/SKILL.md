---
name: dependency-license-audit
description: Scan project dependencies for license compatibility issues, GPL contamination, and compliance violations. Supports npm, pip, Go, Rust, and Ruby ecosystems. Use when asked to audit licenses, check license compliance, find GPL contamination, verify dependency licensing, generate license reports, or ensure open-source compliance before shipping. Also use for CI/CD license gates.
---

# Dependency License Audit

Scan project dependencies for license compatibility issues across multiple ecosystems.

## Quick Start

```bash
# Basic scan (permissive policy)
python3 scripts/license_audit.py /path/to/project

# Strict enterprise scan with CI exit codes
python3 scripts/license_audit.py /path/to/project --policy permissive --ci --format markdown

# Allow weak copyleft (LGPL, MPL)
python3 scripts/license_audit.py /path/to/project --policy weak-copyleft

# Include transitive deps (npm)
python3 scripts/license_audit.py /path/to/project --include-transitive

# JSON output for tooling
python3 scripts/license_audit.py /path/to/project --format json
```

## Supported Ecosystems

| Ecosystem | Files Parsed | License Source |
|-----------|-------------|----------------|
| npm | package.json, package-lock.json, node_modules/*/package.json | Package metadata |
| pip | requirements.txt, Pipfile, pyproject.toml | Installed package metadata |
| Go | go.mod | Manual/UNKNOWN (no local metadata) |
| Rust | Cargo.toml | Manual/UNKNOWN (no local metadata) |
| Ruby | Gemfile | Manual/UNKNOWN (no local metadata) |

npm and pip auto-detect licenses from installed packages. Go/Rust/Ruby report UNKNOWN unless packages are installed — review manually.

## Policies

| Policy | Allows | Use When |
|--------|--------|----------|
| `permissive` (default) | MIT, Apache-2.0, BSD, ISC, etc. | Proprietary/commercial projects |
| `weak-copyleft` | + LGPL, MPL, EPL | Library consumers (dynamic linking) |
| `any-open` | All OSI-approved | Open-source projects |
| `custom` | User-defined | Enterprise with specific requirements |

For custom policy setup, see [references/custom-policy.md](references/custom-policy.md).

## Output Formats

- `text` — Human-readable terminal output (default)
- `json` — Machine-readable for CI pipelines and tooling
- `markdown` — Report with tables, suitable for PRs or documentation

## CI Exit Codes

With `--ci` flag:
- `0` — No issues
- `1` — Warnings only (unknown licenses)
- `2` — Policy violations found

## License Classifications

The scanner classifies licenses into categories:

- **permissive** — MIT, Apache-2.0, BSD, ISC, Unlicense, CC0, etc.
- **weak-copyleft** — LGPL, MPL, EPL, CDDL (modifications must be shared, but linking is OK)
- **strong-copyleft** — GPL, AGPL, SSPL (derivative works inherit the license)
- **proprietary** — UNLICENSED or commercial indicators
- **unknown** — Not recognized; manual review needed

SPDX expressions (`MIT OR Apache-2.0`, `MIT AND BSD-3-Clause`) are evaluated: OR picks most permissive, AND picks most restrictive.

## Workflow

1. Run audit against project directory
2. Review violations and warnings in output
3. For each violation, follow the recommendations provided
4. Optionally create `.license-policy.json` for custom rules
5. Add `--ci` flag to CI pipeline for automated enforcement
