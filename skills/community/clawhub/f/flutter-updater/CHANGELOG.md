# Changelog

## 1.0.0 — 2026-04-13

Initial release.

### Features
- Flutter SDK version monitoring via GitHub Releases API
- `dart pub outdated --json` based dependency analysis with safe/breaking classification
- Safe updates applied automatically via `dart pub upgrade`
- Breaking change updates: changelog fetch, codebase impact analysis, user confirmation, auto-fix, rollback
- `dart fix --dry-run` preview + `dart fix --apply`
- QA pipeline: `flutter analyze` → `flutter test` → `flutter build` (platform auto-detected)
- Structured Markdown result report
- Flags: `--sdk-only`, `--deps-only`, `--qa-only`
- Path/git dependencies are never modified
- Automatic rollback per-package if breaking change fix fails after 3 attempts
