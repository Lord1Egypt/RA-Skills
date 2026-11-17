---
name: flutter-master
description: >-
  Comprehensive Flutter & Dart mobile development skill — use for ANY Flutter
  task, not just when explicitly asked for "best practices" or an "audit".
  Trigger whenever the user mentions Flutter, Dart, pubspec.yaml, widgets,
  BLoC/Riverpod/Provider/GetX, .dart files, or mobile app architecture, or asks
  to build, review, refactor, debug, optimize, or ship a Flutter app.
  Especially trigger for auditing an existing project (code quality,
  architecture, performance, security, dependency health), setting up a new
  project correctly, choosing/reviewing state management, performance or
  build-size problems, pre-release checks (obfuscation, signing, store
  readiness), and testing strategy (unit/widget/integration/golden). Covers
  Material 3, null safety, effective Dart, clean architecture, and current
  Flutter ecosystem conventions. Use proactively even for small requests — a
  "quick fix" is still a chance to catch anti-patterns.
---

# Flutter Master

A deep, opinionated toolkit for building, reviewing, and auditing Flutter applications to a professional standard. This skill is intentionally thorough — Flutter has a huge surface area (widgets, state management schools, platform channels, build pipelines, store requirements), and mediocre Flutter code often *looks* fine while quietly accumulating performance, maintainability, and security debt. The goal is to catch that debt before it ships.

## How to use this skill

Flutter work generally falls into one of four modes. Identify which mode you're in first, since that determines which reference files matter.

1. **Auditing an existing project** → go to [Project Audit Workflow](#project-audit-workflow) below, then pull in reference files as findings surface.
2. **Building something new (feature, screen, app)** → skim [references/architecture.md](references/architecture.md) and [references/code-style.md](references/code-style.md) before writing code, so the first draft is already idiomatic instead of needing a rewrite.
3. **Fixing a specific problem** (performance, a bug, a crash, jank) → jump straight to the relevant reference file (see table below).
4. **Pre-release / shipping** → [references/release-checklist.md](references/release-checklist.md).

Don't try to hold all reference files in your head at once — they exist precisely so you only load what's relevant to the task in front of you. Read a reference file when its topic becomes relevant, not preemptively.

| Topic | Reference file |
|---|---|
| Folder structure, layering, Clean Architecture, feature-first vs layer-first | `references/architecture.md` |
| BLoC/Cubit, Riverpod, Provider, GetX — when to use which, common mistakes | `references/state-management.md` |
| Effective Dart, naming, null safety, immutability, formatting, linting | `references/code-style.md` |
| Jank, rebuilds, const, ListView performance, images, isolates, startup time | `references/performance.md` |
| Unit/widget/integration/golden tests, mocking, coverage | `references/testing.md` |
| Secrets, secure storage, obfuscation, cert pinning, permissions | `references/security.md` |
| App signing, obfuscation flags, store metadata, versioning, CI/CD | `references/release-checklist.md` |
| Accessibility (a11y), localization (i10n/l10n), responsive/adaptive layout | `references/ux-quality.md` |
| The full audit checklist itself (used by the workflow below) | `references/audit-checklist.md` |

A bundled script, `scripts/audit_scan.sh`, automates the mechanical parts of an audit (running `flutter analyze`, `flutter pub outdated`, grepping for anti-patterns). Use it as a first pass — it's fast and objective — then layer human judgment on top using the reference files.

## Project Audit Workflow

When asked to audit, review, or "check" a Flutter project — or when you're about to make non-trivial changes to an unfamiliar codebase and want to understand its health first — follow this sequence. Don't skip straight to opinions; ground them in what's actually in the repo.

### Step 1 — Orient
```
flutter --version
cat pubspec.yaml
find lib -type f -name "*.dart" | wc -l
```
Confirm the Flutter/Dart SDK version, check `pubspec.yaml` for `sdk:` constraints, and get a rough sense of project size. A 15-file app and a 400-file app warrant very different depths of review — don't apply enterprise-architecture critique to a weekend prototype unless the user is trying to grow it into one.

### Step 2 — Run the automated scan
```bash
bash <path-to-this-skill>/scripts/audit_scan.sh <project_root>
```
(`<path-to-this-skill>` is wherever this `flutter-master` skill directory is mounted, e.g. `/mnt/skills/.../flutter-master`.)
This runs `flutter analyze`, `dart format --set-exit-if-changed --output=none .`, `flutter pub outdated`, and a battery of grep-based checks (print statements left in, hardcoded strings/colors, missing const, deprecated APIs, TODO/FIXME density, oversized files, missing error handling around async calls). It writes a plain-text report. Read the whole report before drawing conclusions — don't cherry-pick the first few findings.

### Step 3 — Structural review
Open `lib/` and evaluate against `references/architecture.md`:
- Is there a discoverable, consistent structure (feature-first or layer-first), or does it look ad hoc?
- Is business logic separated from widgets, or is everything crammed into `build()` methods and `StatefulWidget`s?
- Is there a single, consistent state-management approach, or a mix of three different ones fighting each other?
- Are there god-files (a single `main.dart` with 2000 lines, a single `HomePage` doing everything)?

### Step 4 — State management review
Cross-check against `references/state-management.md`. Look specifically for: `setState` calls buried deep in widget trees that should be lifted or replaced; providers/blocs that leak (`dispose()` not called, `StreamSubscription`s never cancelled); business logic living inside widget classes instead of notifiers/blocs/controllers; unnecessary rebuilds from context reads that are too broad (e.g. `context.watch` on a whole object when only one field is needed).

### Step 5 — Performance pass
Cross-check against `references/performance.md`. Prioritize by user-visible impact: janky scrolling (missing `const`, expensive `build()` work, `ListView` instead of `ListView.builder` for long lists) matters more than micro-optimizations. Check image handling (are large images being decoded at full resolution for thumbnail-sized widgets?) and startup time (heavy synchronous work in `main()` before `runApp`).

### Step 6 — Testing & quality gates
Cross-check against `references/testing.md`. Is there any test coverage at all? Are tests actually exercising logic, or are they trivial smoke tests? Is there a CI pipeline running `flutter analyze` and `flutter test` on every PR, or does quality depend entirely on manual review?

### Step 7 — Security & data handling
Cross-check against `references/security.md`. This is the one category where issues are often silent until exploited, so give it real attention even in a quick audit: hardcoded API keys/secrets committed to the repo, sensitive data in `SharedPreferences` instead of secure storage, missing certificate pinning for apps handling sensitive data, overly broad permission requests, debug logging of sensitive info (tokens, PII) that ships to production builds.

### Step 8 — Synthesize findings
Don't just dump a checklist back at the user. Produce a prioritized report:
1. **Critical** — will cause crashes, data loss, security exposure, or store rejection.
2. **High-impact** — visible performance/UX problems, architectural issues that will slow the team down as the app grows.
3. **Polish** — style/lint issues, minor inconsistencies.

For each finding, name the file/line where possible, explain *why* it matters (not just "this is bad practice"), and give a concrete fix — ideally a code snippet, not just a description. A good audit teaches, it doesn't just grade. If the project is small or early-stage, calibrate: don't recommend a full Clean Architecture rewrite for a 10-screen MVP unless the user is planning to scale it — mention the tradeoff and let them decide (see `references/audit-checklist.md` for a full severity-tagged checklist to work from).

## General principles when writing or editing Flutter code

- **Null safety is non-negotiable.** Never suggest `!` (force-unwrap) as a fix for a null-safety error without first checking whether the null case is actually reachable and should be handled properly.
- **Prefer composition over configuration.** Small, focused widgets extracted into their own classes/methods beat giant parameterized `build()` methods — this is also what makes `const` and selective rebuilds possible.
- **Every `StatefulWidget` with a controller, stream subscription, or animation controller needs a `dispose()` that cleans it up.** This is one of the most common Flutter memory leaks; check for it every time you touch lifecycle code.
- **Don't fight the state management library the project already uses.** If it's BLoC, don't introduce Provider for one feature "because it's simpler" — consistency is worth more than local convenience. Flag inconsistency as an audit finding rather than silently adding to it.
- **Async code needs error handling.** A bare `await someFuture()` with no try/catch and no error UI is a silent-failure trap. At minimum, surface errors to the user or log them.
- Always sanity-check the target Flutter/Dart version before recommending an API — Flutter's APIs move fast (e.g. `Material 3` is now default, some older widgets are deprecated). If uncertain about current API surface or a package's latest version, use web search rather than relying on training data, since Flutter/pub.dev packages update frequently.
