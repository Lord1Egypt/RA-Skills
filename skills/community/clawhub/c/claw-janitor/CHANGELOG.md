# Changelog

## 1.1.0
- Added strict subtree blacklist sealing (workspace/CWD-sensitive trees)
- Hardened mount-point-safe deletion path
- Added recursive defense-in-depth safety recheck in `safeRemoveDir`
- Added command existence checks before execution (`which/where`)
- Added `--no-color` output mode for CI/log snapshots
- Added stable JSON sorting for deterministic audits
- Added `--only` / `--skip` group control
- Added `--report-file` JSON audit output
- Added `--help`
- Added/expanded automated tests (`test-janitor.js`)
- Added `SECURITY.md`
