# AGENTS.md - Agave Coding Guidelines

This file provides guidelines for AI coding agents working on the Agave codebase.

## Project Overview

**Agave** is a Solana blockchain validator implementation maintained by Anza. It's a large Rust workspace with 137+ interconnected crates.

- **Language:** Rust (edition 2021)
- **Rust Version:** 1.93.0 (pinned)
- **License:** Apache-2.0
- **Repository:** https://github.com/anza-xyz/agave

## Build / Test / Lint Commands

### Building
```bash
# Build the entire workspace
cargo build

# Build in release mode
cargo build --release

# Build a specific package
cargo build -p solana-core
```

### Testing
```bash
# Run all tests
cargo test

# Run a single test by name
cargo test test_name_here

# Run tests in a specific package
cargo test -p solana-core

# Run tests with single thread (for flaky tests)
cargo test -- --test-threads=1

# Run a specific test with output
cargo test test_name_here -- --nocapture
```

### Linting and Formatting
```bash
# Run all checks (run before committing)
./ci/test-checks.sh

# Run sanity checks
./ci/test-sanity.sh

# Run clippy
./scripts/cargo-clippy.sh

# Check formatting
cargo fmt --all -- --check

# Fix formatting
cargo fmt --all

# Run clippy on all targets
cargo clippy --all-targets
```

### Other Useful Commands
```bash
# Sort Cargo.toml dependencies
./scripts/cargo-for-all-lock-files.sh -- +nightly sort --workspace

# Check for outdated lock files
./scripts/cargo-for-all-lock-files.sh tree

# Run coverage analysis
./scripts/coverage.sh
```

## Code Style Guidelines

### General
- All code must pass `cargo fmt` and `cargo clippy`
- No trailing whitespace (enforced by CI)
- Maximum ~1,000 lines per PR for functional changes
- 90%+ test coverage required for new code paths

### Naming Conventions
- **Functions/variables:** `snake_case`
- **Types/structs/enums:** `CamelCase`
- **Constants:** `SCREAMING_SNAKE_CASE`
- **Traits:** `CamelCase` (often suffixed with `Trait` or descriptive word)
- **Modules:** `snake_case`

### Imports and Formatting
```rust
// Imports are grouped and consolidated (rustfmt.toml: imports_granularity = "One")
use std::{collections::HashMap, sync::Arc};

use solana_sdk::pubkey::Pubkey;

use crate::some_module::SomeType;
```

### Error Handling
- **NEVER use `unwrap()`** in production code unless you can prove it won't panic
- Use `expect()` with a descriptive message when panic is desirable
- Prefer proper error propagation with `?` operator
- Use `std::num::Saturating<T>` instead of deprecated saturating_add_assign macro

```rust
// Good
let value = hashmap.get(key).expect("key must exist in hashmap");

// Bad
let value = hashmap.get(key).unwrap();
```

### Unsafe Code
- Minimize usage of `unsafe` blocks
- Document safety invariants with comments
- Prefer safe abstractions when possible

### Lint Configuration (from clippy.toml)
- Maximum 9 arguments per function (`too-many-arguments-threshold = 9`)
- Disallowed methods: `std::net::UdpSocket::bind`, `tokio::net::UdpSocket::bind`, `lazy_static::initialize`
- Disallowed macros: `lazy_static::lazy_static`, `saturating_add_assign`

## PR Guidelines

### Before Submitting
```bash
# Run these before every PR
./ci/test-sanity.sh
./ci/test-checks.sh
./ci/feature-check/test-feature.sh
```

### PR Requirements
- Open PRs as **Draft** first, convert to "Ready for Review" after CI passes
- PR title: Imperative mood, capitalized first word, no trailing period
- Include detailed problem statement and proposed changes
- Small, focused PRs (~1,000 lines max for functional changes)
- Don't mix refactoring with logical changes
- All changes must have unit and integration tests
- Benchmark performance-critical code

### Consensus Changes
- Must be behind a feature gate
- Must have a merged SIMD (Solana Improvement Document)
- Activate on testnet before mainnet

## Testing Standards

### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_something() {
        // Arrange
        let input = ...;
        
        // Act
        let result = some_function(input);
        
        // Assert
        assert_eq!(result, expected);
    }
}
```

### Integration Tests
- Place in `tests/` directory or use `local-cluster` for cluster tests
- Use `solana-program-test` for program testing
- Avoid flaky tests; use `serial_test` when needed

## Documentation
- Use `///` for public API documentation
- Document complex algorithms and business logic
- Add changelog entries for user-facing features

## Additional Resources

- [CONTRIBUTING.md](./CONTRIBUTING.md) - Detailed contribution guidelines
- [SECURITY.md](./SECURITY.md) - Security policies
- CI scripts in `ci/` directory for automation reference

---

**Note:** This codebase follows strict quality standards. When in doubt, prefer safety, clarity, and thorough testing over clever optimizations.
