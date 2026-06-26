---
name: flutter-updater
version: 1.0.0
description: |
  Keep Flutter/Dart projects automatically up-to-date.
  Detects new Flutter/Dart SDK releases, updates pubspec.yaml dependencies with
  safe breaking-change handling (reads changelogs, auto-fixes code, rolls back
  per-package if unfixable), runs dart fix, and performs full QA
  (flutter analyze → flutter test → flutter build).
  Use when asked to "update flutter", "update dependencies", "upgrade packages",
  or "keep flutter up to date". Flags: --sdk-only, --deps-only, --qa-only.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebFetch
  - AskUserQuestion
---

## Preamble (run first, always)

```bash
# Self-update check (silent if up to date)
_SKILL_DIR="$(dirname "$(which flutter-updater-config 2>/dev/null)" 2>/dev/null || echo "$HOME/.claude/skills/flutter-updater/bin")"
_SKILL_BASE="$(dirname "$_SKILL_DIR" 2>/dev/null || echo "$HOME/.claude/skills/flutter-updater")"
_UPD=$("$_SKILL_BASE/bin/flutter-updater-version-check" 2>/dev/null || true)
[ -n "$_UPD" ] && echo "$_UPD" || true

# Load config
_INTERVAL=$(   "$_SKILL_BASE/bin/flutter-updater-config" get check_interval_hours 2>/dev/null || echo "12")
_IGNORED=$(    "$_SKILL_BASE/bin/flutter-updater-config" get ignored_packages      2>/dev/null || echo "")
_AUTO_SAFE=$(  "$_SKILL_BASE/bin/flutter-updater-config" get auto_apply_safe       2>/dev/null || echo "true")
_CHANNEL=$(    "$_SKILL_BASE/bin/flutter-updater-config" get track_channel         2>/dev/null || echo "stable")
echo "CONFIG: interval=${_INTERVAL}h channel=${_CHANNEL} auto_safe=${_AUTO_SAFE}"
[ -n "$_IGNORED" ] && echo "CONFIG: ignored_packages=${_IGNORED}"

# Project state
_LAST_CHECK=$("$_SKILL_BASE/bin/flutter-updater-state" get-last-check 2>/dev/null || echo "")
_SLUG=$(      "$_SKILL_BASE/bin/flutter-updater-state" slug 2>/dev/null || echo "unknown")
echo "PROJECT: $_SLUG"
[ -n "$_LAST_CHECK" ] && echo "LAST_CHECK: $_LAST_CHECK" || echo "LAST_CHECK: never"

# Detect build targets
_TARGETS=$("$_SKILL_BASE/bin/flutter-updater-detect-targets" 2>/dev/null || echo "")
echo "TARGETS: ${_TARGETS:-none}"

# Parse flags
_FLAG="${1:-}"
echo "FLAG: ${_FLAG:-none}"
```

After running the preamble:
- Store `$_SKILL_BASE` for use in later phases.
- Store `$_IGNORED`, `$_AUTO_SAFE`, `$_CHANNEL`, `$_TARGETS`, `$_FLAG`.
- If `$_LAST_CHECK` is within `$_INTERVAL` hours AND `$_FLAG` is empty, ask the user: "Already checked `$_INTERVAL`h ago. Run again?" before proceeding.

---

## PHASE 0: Environment Validation

```bash
# Verify Flutter project
[ -f pubspec.yaml ] || { echo "ERROR: No pubspec.yaml found. Run from Flutter/Dart project root."; exit 1; }

# Run dart pub outdated --json (used in Phase 2)
dart pub outdated --json 2>/dev/null
```

If `pubspec.yaml` is missing, stop and tell the user. Do not proceed.

---

## PHASE 1: Flutter SDK Update Check

Skip if `$_FLAG` is `--deps-only` or `--qa-only`.

```bash
"$_SKILL_BASE/bin/flutter-updater-sdk-check" "$_CHANNEL" 2>&1
```

Parse output lines:
- `CURRENT:<version>` → current Flutter version
- `LATEST:<version>` → latest available
- `UPDATE_AVAILABLE` → upgrade is needed
- `UP_TO_DATE` → skip this phase, note "Flutter SDK is current (vX.Y.Z)"
- `ERROR:...` → warn user, skip phase

If `UPDATE_AVAILABLE`:
> Use AskUserQuestion: "Flutter SDK update: vCURRENT → vLATEST. Upgrade now?"
> Options: a) Yes, upgrade   b) Skip

If user chooses (a):
```bash
flutter upgrade
```
Then re-run the sdk-check to confirm new version.

---

## PHASE 2: Dependency Classification

Skip if `$_FLAG` is `--sdk-only` or `--qa-only`.

Run the classifier using the `dart pub outdated --json` output from Phase 0:

```bash
echo "<OUTDATED_JSON_FROM_PHASE_0>" | "$_SKILL_BASE/bin/flutter-updater-classify" pubspec.yaml "$_IGNORED"
```

Parse each output line:
- `SAFE:<name>:<current>:<target>` → safe update list
- `BREAKING:<name>:<current>:<latest>` → breaking update list
- `UP_TO_DATE:<name>:<version>` → already current
- `SKIP_PATH:<name>` / `SKIP_GIT:<name>` / `SKIP_SDK:<name>` / `SKIP_IGNORED:<name>:<v>` → skip

Print a summary table to the user:
```
Dependency Analysis
  Safe updates    (N): package_a 1.0→1.2, package_b 3.1→3.1.4
  Breaking updates(N): package_c 0.13→1.2, package_d 6.0→7.0
  Up to date      (N): ...
  Skipped         (N): path/git/sdk/ignored
```

If there are no updates at all (all UP_TO_DATE or SKIP), jump directly to Phase 5 (dart fix) unless `--deps-only`.

---

## PHASE 3: Safe Updates

Skip if `$_FLAG` is `--sdk-only` or `--qa-only`.
Skip if no SAFE packages were found.

If `$_AUTO_SAFE` is `true`, apply automatically.
If `$_AUTO_SAFE` is `false`, ask the user first.

```bash
dart pub upgrade 2>&1
```

After applying, run:
```bash
dart analyze 2>&1 | head -60
```

If `dart analyze` shows errors after safe updates, read each error and fix with Edit tool.
These should be minor issues (API changes within the same major version).

---

## PHASE 4: Breaking Change Updates (one package at a time)

Skip if `$_FLAG` is `--sdk-only` or `--qa-only`.
Skip if no BREAKING packages were found.

For each BREAKING package, do the following in sequence:

### 4a — Backup (once before first breaking update)

```bash
cp pubspec.yaml pubspec.yaml.fu_bak
cp pubspec.lock pubspec.lock.fu_bak
```

### 4b — Fetch Changelog

```bash
"$_SKILL_BASE/bin/flutter-updater-changelog" "<PACKAGE_NAME>" "<TARGET_VERSION>" 2>&1
```

Read the changelog output. Identify:
- Removed classes or methods (exact names)
- Renamed classes or methods (old → new)
- Changed constructors or method signatures
- Any migration guide mentioned

### 4c — Scan Codebase for Affected APIs

Use Grep to find every usage of the removed/changed APIs in `lib/`, `test/`, `bin/`:
```bash
grep -rn "OldClassName\|removedMethod\|changedSignature" lib/ test/ bin/ 2>/dev/null
```

Build a file:line map of what needs changing.

### 4d — Confirm with User

> Use AskUserQuestion:
> "**PACKAGE_NAME** vCURRENT → vLATEST (Breaking)
>
> Changelog summary:
> - [key breaking changes from 4b]
>
> Affected in your code:
> - lib/foo.dart:42 — OldClassName
> - lib/bar.dart:17 — removedMethod()
>
> Attempt automatic migration?"
>
> Options: a) Yes, migrate   b) Skip this package

If user skips → record `SKIP` for this package, continue to next.

### 4e — Apply Update

```bash
dart pub upgrade --major-versions "<PACKAGE_NAME>" 2>&1
```

If this fails (non-zero exit), do NOT modify pubspec.yaml. Record as failed, skip to next package.

### 4f — Fix Compilation Errors (up to 3 rounds)

```bash
dart analyze 2>&1
```

For each error:
1. Read the affected file with Read tool.
2. Cross-reference with changelog from 4b to determine the correct replacement.
3. Apply fix with Edit tool.
4. Re-run `dart analyze`. Repeat up to 3 times.

Common fix patterns:
- `Undefined class 'OldName'` → rename to `NewName` everywhere (use Grep to find all uses, Edit to replace)
- `Method 'removedMethod' not found` → replace with new API equivalent
- `Too many positional arguments` → update call signature
- `The named parameter 'oldParam' isn't defined` → rename or remove parameter

### 4g — Rollback if Unfixable

If errors remain after 3 fix rounds:

Read `pubspec.yaml.fu_bak`, find the original constraint for this package, and restore just that line in `pubspec.yaml` using Edit tool. Then:

```bash
dart pub get 2>&1
```

Tell the user:
> "Rolled back **PACKAGE_NAME** to vCURRENT.
> Auto-migration failed after 3 attempts.
>
> Manual migration needed:
> - [specific breaking APIs that still need fixing]
> - [official migration guide URL if found in changelog]
> - Affected files: [list]"

### 4h — Continue to Next Breaking Package

After all breaking packages: clean up backups.
```bash
rm -f pubspec.yaml.fu_bak pubspec.lock.fu_bak
```

---

## PHASE 5: dart fix

Skip if `$_FLAG` is `--sdk-only` or `--qa-only`.

```bash
dart fix --dry-run 2>&1
```

If fixes are available:
> Use AskUserQuestion: "dart fix can repair N issues. Apply?"
> Options: a) Yes   b) Skip

If (a):
```bash
dart fix --apply 2>&1
```

Run `dart analyze` once more to confirm no regressions.

---

## PHASE 6: QA

Skip if `$_FLAG` is `--sdk-only` or `--deps-only`.

### 6a — Static Analysis

```bash
flutter analyze 2>&1
```

If errors: read each, attempt Edit fixes, re-run (up to 2 rounds).
Warnings are acceptable — note them but do not block.

### 6b — Tests

```bash
flutter test 2>&1
```

If tests fail:
- If failure is directly caused by a dependency API change (verified against changelog): read test file, update to new API, re-run once.
- If failure is a genuine regression (unrelated to update): record as failed, do NOT silently fix test assertions.

### 6c — Build Verification

Use `$_TARGETS` from preamble. Pick the first available in order: `android` → `web` → `macos` → `linux` → `ios` → `windows`.

| Target | Command |
|--------|---------|
| android | `flutter build apk --debug 2>&1 \| tail -30` |
| web | `flutter build web 2>&1 \| tail -30` |
| macos | `flutter build macos --debug 2>&1 \| tail -30` |
| linux | `flutter build linux --debug 2>&1 \| tail -30` |
| ios | `flutter build ios --debug --no-codesign 2>&1 \| tail -30` |
| windows | `flutter build windows --debug 2>&1 \| tail -30` |
| dart_only | `dart compile exe bin/main.dart -o /tmp/flutter_updater_build_check 2>&1 \| tail -10` |

If build fails: apply same fix-analyze loop as 6a (up to 2 rounds). If still failing: record in report.

---

## PHASE 7: Update State & Save Report

```bash
# Record this run in project state
"$_SKILL_BASE/bin/flutter-updater-state" set-last-check

"$_SKILL_BASE/bin/flutter-updater-state" log-update '{
  "sdk_updated": "<NEW_SDK_VERSION_OR_EMPTY>",
  "updated": ["<list of successfully updated packages>"],
  "skipped": ["<list of rolled-back packages>"],
  "dart_fix_applied": true_or_false,
  "qa_analyze": "pass|fail",
  "qa_test": "pass|fail|N/N",
  "qa_build": "pass|fail|skipped"
}'
```

### 7a — Compose the Report

Compose the full Markdown report (see template below) and write it to a temp file:

```bash
cat > /tmp/flutter_updater_report_$$.md << 'REPORT'
<full markdown report content>
REPORT
```

### 7b — Save Report to Project

Determine the current Flutter version (use the post-update version if SDK was upgraded).

```bash
_FLUTTER_VER=$(flutter --version --machine 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('frameworkVersion','unknown'))" 2>/dev/null || echo "unknown")

# Default save location: .flutter_updater/reports/ inside the project
# User can override by setting FLUTTER_UPDATER_REPORT_DIR in their shell
_REPORT_DIR="${FLUTTER_UPDATER_REPORT_DIR:-.flutter_updater/reports}"

"$_SKILL_BASE/bin/flutter-updater-save-report" "$_FLUTTER_VER" "/tmp/flutter_updater_report_$$.md" "$_REPORT_DIR"
```

After saving, tell the user the exact file path where the report was saved.
Also print the report contents to the conversation.

Clean up:
```bash
rm -f /tmp/flutter_updater_report_$$.md
```

### Report Template

The report file must follow this structure:

```markdown
# Flutter Update — v<FLUTTER_VERSION> (<YYYY-MM-DD>)

Project: <project name from pubspec.yaml>
Run at: <ISO timestamp>

---

## Flutter SDK
- Before: v<OLD>  →  After: v<NEW>  (or: Already current / Skipped)

## Dependency Updates

| Package | Before | After | Type | Result |
|---------|--------|-------|------|--------|
| http | 0.13.5 | 1.2.2 | Breaking | ✅ Updated + auto-fixed (3 files) |
| provider | 6.1.2 | 6.1.4 | Safe | ✅ Updated |
| dio | 4.0.6 | 5.4.0 | Breaking | ⚠️ Rolled back — see below |
| path | 1.8.3 | 1.8.3 | — | ⏭ Up to date |

## Code Changes Applied

### Auto-fixed (dart fix)
- N issues fixed  (or: No fixes needed / Skipped)

### Breaking Change Migrations
For each auto-fixed breaking package, list:
- **<package_name>** v<old> → v<new>
  - Changed: `OldClass` → `NewClass` in lib/foo.dart:42, lib/bar.dart:17
  - Changed: `oldMethod()` → `newMethod()` in lib/service.dart:88

## QA Results

| Check | Result | Details |
|-------|--------|---------|
| flutter analyze | ✅ Pass | 0 errors, 2 warnings |
| flutter test | ✅ Pass | 47/47 tests passed |
| flutter build (android) | ✅ Pass | Build succeeded |

## Manual Action Required

### <package_name> — Could Not Auto-Migrate
- **Version**: v<old> → v<latest> (rolled back to v<old>)
- **Breaking change**: `Options` class removed; use `RequestOptions` instead
- **Your affected files**:
  - `lib/api/client.dart` lines 34, 89
  - `test/api_test.dart` line 12
- **Migration guide**: <URL if found in changelog>

---
*Generated by flutter-updater v1.0.0*
```

---

## Error Recovery Rules

- **Network failures** (GitHub, pub.dev): Retry once silently. If still failing, skip that step and note it in the report. Never abort the full run.
- **`dart pub upgrade` resolution failure**: Do not touch pubspec.yaml. Report conflict and skip that package.
- **Fix loop cap**: Max 3 rounds of analyze → fix per package. After 3, rollback.
- **Flaky test**: Re-run `flutter test` once. If it fails again, record as failed.
- **Unrelated build failure**: Report but do not attempt to fix issues not caused by the update.
- **git**: Do NOT run any git commands (stash, commit, checkout). Use only file backup/restore strategy.
