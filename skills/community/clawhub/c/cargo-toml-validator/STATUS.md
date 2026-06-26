# cargo-toml-validator — Status

- **Status:** Published
- **ClawHub ID:** k978fd8h25zhd4ztj7hhtanhm185a68w
- **Price:** $49
- **Built:** 2026-04-23
- **Published:** 2026-04-23
- **Rules:** 25
- **Lines:** ~1060
- **Dependencies:** Pure Python stdlib (tomllib)

## Tests Passed

- [x] S1: File not found or unreadable
- [x] S2: Empty file
- [x] S3: Invalid TOML syntax
- [x] S4: Missing [package] section (error for bins, warning for virtual workspaces)
- [x] S5: Missing required fields (name, version, edition)
- [x] M1: Missing edition field
- [x] M2: Outdated edition detection
- [x] M3: Missing license/license-file
- [x] M4: Missing description
- [x] D1: Wildcard version '*'
- [x] D2: Unpinned dependency without version
- [x] D3: Git dependency without rev/tag/branch
- [x] D4: Path dependency detection
- [x] D5: Duplicate dep across sections with different versions
- [x] D6: Deprecated crate name detection (9 crates)
- [x] F1: Feature enables non-existent dependency
- [x] F2: Empty feature detection
- [x] F3: Circular feature dependency detection (DFS)
- [x] W1: Empty workspace
- [x] W2: Ambiguous package + workspace
- [x] W3: workspace.dependencies hint
- [x] B1: Missing documentation link
- [x] B2: Build script without build-dependencies
- [x] B3: Dependency bloat (>30)
- [x] B4: Missing repository/homepage URL
- [x] All 4 commands (validate, check, explain, suggest)
- [x] All 3 output formats (text, json, summary)
- [x] --strict flag (warnings become errors, exit 1)
- [x] CI-friendly exit codes (0=pass, 1=errors, 2=parse fail)
- [x] target-specific dependency extraction
- [x] workspace = true inheritance detection
- [x] dep: prefix and crate/feature syntax in features

## Next Steps

- [ ] Publish to ClawHub
