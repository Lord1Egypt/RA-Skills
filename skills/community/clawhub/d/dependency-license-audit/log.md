# dependency-license-audit — Log

## 2026-03-29

### Done
- Built complete license audit scanner (pure Python stdlib)
- 5 ecosystems: npm (package.json + lock + node_modules), pip (requirements.txt + Pipfile + pyproject.toml), Go (go.mod), Rust (Cargo.toml), Ruby (Gemfile)
- 80+ license aliases mapped to SPDX identifiers
- License classification: permissive, weak-copyleft, strong-copyleft, proprietary, unknown
- SPDX expression evaluation (OR → most permissive, AND → most restrictive)
- 4 policies: permissive, weak-copyleft, any-open, custom (.license-policy.json)
- 3 output formats: text, JSON, markdown
- CI exit codes: 0 clean, 1 warnings, 2 violations
- Actionable recommendations per license classification
- Fixed: SPDX parenthesized expressions like `(MIT OR GPL-3.0-or-later)`
- Tested against real OpenClaw package (70 deps) + multi-ecosystem fixture
- Packaged to dist/dependency-license-audit.skill ✅

### Decisions
- $69 pricing — matches log-analyzer, addresses enterprise compliance need
- Pure Python stdlib — no deps, maximum compatibility
- UNKNOWN = warning (not error) — less noise for Go/Rust/Ruby where local metadata unavailable
- Custom policy supports exceptions list — critical for enterprise adoption
