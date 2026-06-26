---
name: code-check
description: Run project quality checks and security reviews, fixing all errors by priority until all pass.
---

# Code Quality & Security Checks

Run comprehensive project checks and fix all issues by priority.

## Use Cases

Use when users need "check code", "run check", "fix lint errors", or "code quality check".

## Core Task

Run the project check command and resolve all errors. Loop: check → fix → re-check until all pass.
## Important Rules

- Do not commit any code
- Do not change version numbers
- Only fix issues identified by checks

## Check Types

| Type | Description | JS/TS | Python | Rust | Go |
|------|-------------|-------|--------|------|-----|
| Lint | Code style & syntax | ESLint | flake8 | clippy | golint |
| Type Check | Type errors | tsc | mypy | cargo check | go vet |
| Tests | Failing cases | jest/vitest | pytest | cargo test | go test |
| Security | Vulnerability detection | npm audit | bandit | cargo audit | govulncheck |
| Formatting | Style consistency | prettier | black | rustfmt | gofmt |
| Build | Compilation errors | tsc --noEmit | — | cargo check | go build |

## Workflow

1. Run the check command
2. Analyze output for errors and warnings
3. Fix by priority:
   - 🔴 Build-breaking errors (highest priority)
   - 🔴 Test failures
   - 🟡 Linting errors
   - 🟢 Warnings
4. Re-run checks after each fix
5. Continue until all checks pass

## Multi-Project Types

- **JavaScript/TypeScript**: `npm run check` or `yarn check`
- **Python**: `black` → `isort` → `flake8` → `mypy`
- **Rust**: `cargo check` → `cargo clippy`
- **Go**: `go vet` → `golint`
- **Swift**: `swift-format` → `swiftlint`

If the project has no `check` script, execute the above commands individually.