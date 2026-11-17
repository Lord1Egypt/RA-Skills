# Full Audit Checklist

Severity tags: **[CRIT]** ship-blocking (crash/security/data-loss/store-rejection risk), **[HIGH]** real user/dev impact, **[POLISH]** worth fixing but low urgency. Use these tags when reporting findings back to the user so they can prioritize.

## Project setup
- [ ] [HIGH] `pubspec.yaml` SDK constraint is reasonable/current, not left at an ancient default.
- [ ] [HIGH] `analysis_options.yaml` extends `flutter_lints` (or stricter) — not just default/empty.
- [ ] [CRIT] No secrets/API keys hardcoded in committed source or `pubspec.yaml`.
- [ ] [HIGH] `.gitignore` covers `.env`, key/signing files, build output.
- [ ] [POLISH] README explains how to run/build the project (setup steps, required env vars).

## Architecture
- [ ] [HIGH] Consistent folder structure (feature-first or layer-first) applied uniformly.
- [ ] [HIGH] Business logic separated from widgets (testable without pumping a widget tree).
- [ ] [HIGH] Single, consistent state-management approach — not 2-3 mixed together.
- [ ] [POLISH] No god-files/god-widgets (very large `build()` methods, 1000+ line files).
- [ ] [HIGH] Dependencies point one direction (data/domain don't import presentation/widgets).

## State management
- [ ] [CRIT] All controllers/subscriptions/animation controllers disposed in `dispose()`.
- [ ] [HIGH] `mounted` checked before `setState` after an `await`.
- [ ] [HIGH] Context reads (`watch`/`Consumer`/`BlocBuilder`) scoped narrowly, not over-broad.
- [ ] [POLISH] No leftover `setState`-only patterns for state that's actually shared/cross-widget.

## Code quality
- [ ] [POLISH] `const` used wherever possible (check `dart fix --apply` output as a start).
- [ ] [HIGH] No `!` force-unwraps on values whose nullness is actually reachable.
- [ ] [POLISH] No bare `print()` — real logger or removed.
- [ ] [HIGH] Async calls wrapped with error handling (no silent `catch (e) {}`).
- [ ] [POLISH] Naming follows Effective Dart conventions.

## Performance
- [ ] [HIGH] Long lists use `.builder` constructors, not eager `children: [...]`.
- [ ] [HIGH] Network/asset images sized appropriately (`cacheWidth`/`cacheHeight`), not full-res for thumbnails.
- [ ] [HIGH] `main()` lean before `runApp()`; no blocking I/O before first frame.
- [ ] [HIGH] CPU-heavy work (large JSON, image processing) off the main isolate (`compute()`).
- [ ] [POLISH] App size checked (`--analyze-size`), no obviously bloated bundled assets.

## Testing
- [ ] [HIGH] Any test coverage exists at all beyond the default counter-app test.
- [ ] [HIGH] Error/failure paths tested, not just happy path.
- [ ] [CRIT] CI runs `flutter analyze` + `flutter test` on every PR (if team project).
- [ ] [POLISH] Critical user flows covered by at least one integration test.

## Security
- [ ] [CRIT] No sensitive data (tokens, PII) in unencrypted `SharedPreferences`.
- [ ] [CRIT] All network calls over HTTPS.
- [ ] [HIGH] Release builds use `--obfuscate --split-debug-info`, symbols archived.
- [ ] [HIGH] Permissions requested are actually used; requested contextually.
- [ ] [HIGH] Dependencies checked for staleness/known vulnerabilities (`flutter pub outdated`).
- [ ] [POLISH] Debug logging doesn't leak tokens/PII, and is stripped/guarded in release.

## UX quality
- [ ] [HIGH] Interactive elements have accessible labels (screen-reader usable).
- [ ] [POLISH] Tap targets ≥48x48; text scales without breaking layout.
- [ ] [HIGH] User-facing strings not hardcoded if multi-language is plausible.
- [ ] [POLISH] Layout tested on more than one screen size; no overflow errors in logs.

## Release readiness
- [ ] [CRIT] Proper release signing (not debug keys) for both platforms.
- [ ] [CRIT] Version/build number bumped per release.
- [ ] [HIGH] Privacy policy + store data-safety disclosures match actual data collection.
- [ ] [HIGH] Crash reporting wired up and verified to actually report.
- [ ] [POLISH] Store metadata/screenshots reflect current app state.

## How to use this in a report

Don't paste this whole checklist back verbatim as the deliverable — it's a working tool for you to check against, not the final report. The final report to the user should be a prioritized, narrative summary: Critical items first with concrete fixes, then High-impact, then Polish, each with file references and code snippets where relevant. Calibrate depth to project size — a checklist item that doesn't apply (e.g. no team/CI for a solo hobby project) isn't a finding, just skip it silently rather than listing it as "N/A" clutter.
