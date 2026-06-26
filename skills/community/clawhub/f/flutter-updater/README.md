# Flutter Updater

> A Claude Code skill that keeps your Flutter/Dart project automatically up-to-date — from SDK releases to pub.dev dependencies, with full QA verification.

## What It Does

`/flutter-updater` runs a full update pipeline on your Flutter or Dart project:

1. **Flutter SDK check** — Detects new stable releases via GitHub API and offers to upgrade
2. **Dependency analysis** — Runs `dart pub outdated` and classifies updates as safe or breaking
3. **Safe updates** — Applies minor/patch updates automatically (`dart pub upgrade`)
4. **Breaking change updates** — For major version bumps:
   - Fetches and reads the package's CHANGELOG
   - Searches your codebase for affected APIs
   - Applies `dart pub upgrade --major-versions` and auto-fixes compilation errors
   - Rolls back individual packages if auto-fix fails, with a clear migration guide
5. **dart fix** — Applies automated deprecated API migrations
6. **QA** — Runs `flutter analyze`, `flutter test`, and `flutter build` to verify everything works
7. **Report** — Prints a summary of what changed, what was fixed, and what needs manual attention

## Installation

```bash
clawhub install flutter-updater
```

## Usage

Run from the root of your Flutter or Dart project (where `pubspec.yaml` lives):

```
/flutter-updater
```

### Flags

| Flag | Description |
|------|-------------|
| `--sdk-only` | Only check and upgrade the Flutter SDK, skip dependency and QA steps |
| `--deps-only` | Only update dependencies, skip SDK check |
| `--qa-only` | Only run QA (analyze, test, build), skip updates |

## How Breaking Changes Are Handled

When a dependency has a major version available (e.g., `http 0.13.5 → 1.2.2`):

1. The changelog is fetched from the package's GitHub repository
2. Breaking changes are summarized and matched against your codebase
3. You confirm before the update is applied
4. Compilation errors from the update are auto-fixed based on the changelog
5. If errors can't be resolved after 3 attempts, the package is **rolled back** to its previous version and you receive a specific migration guide

Path and git dependencies are never touched.

## QA Details

After all updates are applied, the skill runs:

- `flutter analyze` — Static analysis (zero errors required)
- `flutter test` — Full test suite
- `flutter build` — Build verification for the first available platform (Android APK, Web, macOS, iOS)

If tests fail due to the update, the skill attempts to update the test code to match the new API. If the failure is unrelated to the update, it is reported but not silently "fixed."

## Requirements

- Flutter SDK installed and on `PATH` (or FVM configured)
- Claude Code with ClawHub skill support

## What It Won't Do

- Modify `path:` or `git:` dependencies
- Run `git` commands (stash, commit, etc.)
- Auto-fix test failures that are genuine regressions unrelated to the update
- Update packages that can't be resolved due to transitive conflicts

## License

MIT
