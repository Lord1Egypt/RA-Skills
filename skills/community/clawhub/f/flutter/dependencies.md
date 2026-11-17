# Dependencies — pub, Versions, Plugins, and Codegen

Flutter apps carry two dependency graphs: Dart packages resolved by pub, and native dependencies (Gradle, CocoaPods) pulled in by whichever of those packages are plugins. Most "dependency hell" in Flutter is the second graph reacting to a change in the first.

## Constraints and the Lockfile

- `^1.2.3` means `>=1.2.3 <2.0.0`. That is the right default for an application: it takes patches and minors, and refuses a breaking major.
- `pubspec.lock` records the exact resolution. **Commit it for applications** so every machine and CI runner builds the same graph; do not commit it for published packages, whose consumers resolve their own.
- `flutter pub get` respects the lockfile. `flutter pub upgrade` moves within the constraints and rewrites the lock. `flutter pub upgrade --major-versions` rewrites the CONSTRAINTS too — a deliberate act, one that belongs in its own commit.
- `flutter pub outdated` shows current, upgradable, and resolvable versions per package. Read the "Resolvable" column: a package stuck below its latest is usually blocked by one other constraint, and that column names the wall.
- `flutter pub deps` prints the tree. When two packages disagree, that tree tells you which one to pressure.

## When Resolution Fails

Read the error: pub names both constraints and the package caught between them.

| Situation | Move |
|---|---|
| Two packages require incompatible versions of a third | Upgrade the more actively maintained one first; if neither moves, one of them must be replaced |
| A package requires a newer Dart or Flutter SDK | Upgrade the SDK, or pin the package below that release — and record why |
| A transitive plugin blocks everything | `flutter pub deps` to find who depends on it; the direct dependency is what you upgrade |
| Everything looks right and still fails | Delete `pubspec.lock` and re-resolve — the destructive option, and only after reading the constraint error (`destructive_confirm`) |
| Nothing resolves | `dependency_overrides`, as a temporary, commented, dated escape |

`dependency_overrides` bypasses the solver entirely: it forces a version regardless of what any package declared it can work with. That is occasionally the only way forward and always a debt — the overridden package may be silently incompatible, and the failure appears at runtime rather than at resolve time. Every override gets a comment saying why it exists and what would let it be removed.

## Choosing a Package

Before adding a dependency, check, in this order:

1. **Is it a plugin?** A pure Dart package is a version bump; a plugin adds native build configuration, per-platform behavior, and store-review surface (permissions).
2. **Last publish and open-issue trend.** An unmaintained plugin blocks your next SDK upgrade for the whole app.
3. **Platform support** against `target_platforms` (SKILL.md Configuration) — a plugin missing web or desktop fails to compile or throws `UnimplementedError` the day that platform is added.
4. **What it drags in.** One convenience package can pull a dozen transitive dependencies and megabytes of native code (`release.md`, size).
5. **Whether you would write it in an afternoon.** For a formatter, a debouncer, or a small extension, the dependency costs more over time than the code.

Wrap third-party plugins behind your own interface in the data layer: they are the most churn-prone dependency in a Flutter app, and a wrapper turns a migration into one file (`architecture.md`).

## Native Dependency Layers

- Android: each plugin contributes Gradle configuration. A plugin upgrade that requires a newer Android Gradle Plugin, Kotlin version, or compile SDK forces an app-wide bump — that is the most common Flutter upgrade tax. Gradle's error names the module; start there.
- iOS: plugins arrive through CocoaPods. After adding, removing, or upgrading any plugin, run `pod install` in `ios/`. A stale `Podfile.lock` produces "works after a clean checkout, fails on mine" reports.
- Minimum OS versions come from the strictest plugin in the graph. Raising them drops real users — check the store's device report before accepting a bump that a single convenience package forced.
- Native transitive conflicts (two plugins embedding different versions of the same SDK) surface as duplicate-symbol or manifest-merger errors, not as pub errors. The fix is at the plugin level: upgrade, or drop one.

## Upgrading Flutter Itself

- Pin the SDK version for the whole team and CI. Analyzer rules, generated code, goldens, and default theming all move between releases (`testing.md`).
- Upgrade deliberately, on its own branch: bump the SDK, run `dart fix --apply` for mechanical deprecations, then `flutter pub outdated` and move the packages that were waiting on it.
- Read the release notes' breaking-change section before debugging: a widget that "suddenly looks different" after an upgrade is usually a documented default change, not a regression in your code (`widgets.md`, theming).
- Keep the previous SDK installed until the upgraded build ships. Rolling back an SDK mid-release is otherwise its own incident.

## Codegen

Only when `codegen: allowed` (SKILL.md Configuration).

- `dart run build_runner build --delete-conflicting-outputs` for a one-shot; `watch` during development. The `--delete-conflicting-outputs` flag is what clears the stale-output error most people hit first.
- Generated files (`*.g.dart`, `*.freezed.dart`) are either committed or generated in CI — pick one and enforce it. The mixed state, where some are committed and some are not, produces the classic "compiles locally, fails in CI" failure (`debug.md`).
- Generation runs over the whole package: in a large app it is slow enough to belong in a watch process, not in the edit-run loop.
- A generator that fails after a dependency upgrade usually needs its own upgrade in lockstep (`json_serializable` with `build_runner`, `freezed` with `freezed_annotation`) — bump the pair together.
- Codegen failures often mask a real analyzer error: run `flutter analyze` first, because the generator's message rarely names the actual broken annotation.

## Monorepos and Local Packages

- Split into local packages (`path:` dependencies) when a boundary is real — a design system, a shared client, a feature that another app will consume. Splitting for its own sake multiplies pubspec maintenance without buying anything.
- A local package has its own `pubspec.yaml` and its own constraints; a version conflict between two local packages resolves the same way as any other.
- Tooling that runs a command across every package (melos and equivalents) is what makes this bearable at scale; without it, a dependency bump is a manual pass over N directories.
