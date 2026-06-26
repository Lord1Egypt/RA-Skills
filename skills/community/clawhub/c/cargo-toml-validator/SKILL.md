---
name: cargo-toml-validator
description: Validate Rust Cargo.toml manifests for dependency issues, missing metadata, feature conflicts, workspace config, and crates.io publishing readiness. Use when validating Rust project configs, auditing dependencies, or preparing crates for publishing.
---

# Cargo.toml Validator

Validate Rust `Cargo.toml` manifest files for structural correctness, dependency hygiene, feature configuration, workspace setup, and crates.io publishing readiness. Uses Python 3.11+ `tomllib` for native TOML parsing — no external dependencies.

## Commands

### validate — Full validation with all rules

```bash
python3 scripts/cargo_toml_validator.py validate Cargo.toml
python3 scripts/cargo_toml_validator.py validate Cargo.toml --strict
python3 scripts/cargo_toml_validator.py validate Cargo.toml --format json
```

### check — Quick check (errors and warnings only)

```bash
python3 scripts/cargo_toml_validator.py check Cargo.toml
python3 scripts/cargo_toml_validator.py check Cargo.toml --format summary
```

### explain — Show all rules with descriptions

```bash
python3 scripts/cargo_toml_validator.py explain Cargo.toml
python3 scripts/cargo_toml_validator.py explain Cargo.toml --format json
```

### suggest — Run validation and propose fixes

```bash
python3 scripts/cargo_toml_validator.py suggest Cargo.toml
python3 scripts/cargo_toml_validator.py suggest Cargo.toml --format json
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Treat warnings as errors — exit code 1 (CI-friendly) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format summary` | Compact summary with counts |

## Validation Rules (24)

### Structure (5)

| Rule | Severity | Description |
|------|----------|-------------|
| S1 | error | File not found or unreadable |
| S2 | error | Empty file |
| S3 | error | Invalid TOML syntax |
| S4 | error/warning | Missing [package] section (error for bins/libs, warning for virtual workspaces) |
| S5 | error/warning | Missing required fields: name, version (error), edition (warning) |

### Package Metadata (4)

| Rule | Severity | Description |
|------|----------|-------------|
| M1 | warning | Missing edition field (defaults to 2015) |
| M2 | info | Outdated edition (2015/2018 when 2021/2024 available) |
| M3 | warning | Missing license or license-file for crates.io |
| M4 | warning | Missing description for crates.io |

### Dependencies (6)

| Rule | Severity | Description |
|------|----------|-------------|
| D1 | error | Wildcard version `*` |
| D2 | warning | Unpinned dependency without version specifier |
| D3 | warning | Git dependency without rev/tag/branch pin |
| D4 | info | Path dependency (blocks crates.io publish) |
| D5 | warning | Duplicate dep in [dependencies] and [dev-dependencies] with different versions |
| D6 | info | Deprecated crate name (failure, error-chain, iron, rustc-serialize, old hyper/tokio/actix-web/rocket/time) |

### Features (3)

| Rule | Severity | Description |
|------|----------|-------------|
| F1 | error | Feature enables non-existent dependency |
| F2 | warning | Empty feature (no deps or sub-features) |
| F3 | error | Circular feature dependencies |

### Workspace (3)

| Rule | Severity | Description |
|------|----------|-------------|
| W1 | warning | [workspace] with no members |
| W2 | info | Both [package] and [workspace] without members (ambiguous) |
| W3 | info | [workspace.dependencies] detected — hint about workspace = true in members |

### Best Practices (3+)

| Rule | Severity | Description |
|------|----------|-------------|
| B1 | info | Missing documentation link for published crates |
| B2 | info | Build script without [build-dependencies] |
| B3 | info | Very large number of dependencies (>30) |
| B4 | info | Missing repository/homepage URL |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings allowed unless `--strict`) |
| 1 | Errors found (or warnings in `--strict` mode) |
| 2 | File not found / parse error |

## Example Output

```
Cargo.toml validate — Cargo.toml
=================================
[ERROR  ] S5: Missing required field: package.version
         Set version directly or use version.workspace = true.
[WARNING] M1: Missing edition field — defaults to 2015
         Add edition = "2021" or edition = "2024" to [package].
[WARNING] D3: Git dependency 'my-fork' in [dependencies] is not pinned
         Pin to a rev, tag, or branch for reproducibility. URL: https://github.com/user/fork
[INFO   ] D4: Path dependency 'utils' in [dependencies] — blocks crates.io publish
         Path: ../utils. Fine for local dev, but won't work on crates.io.
[INFO   ] B4: Missing repository and homepage URL
         Add repository = "https://github.com/..." to [package] for crates.io visibility.

Result: INVALID
Summary: 1 error(s), 2 warning(s), 2 info
```
