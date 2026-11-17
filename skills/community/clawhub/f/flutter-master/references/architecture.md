# Architecture

## Picking a structure

Two dominant conventions. Pick one per project and enforce it consistently — a mixed structure is worse than either applied purely.

**Feature-first** (recommended default for most apps, especially team projects):
```
lib/
  core/                  # shared utilities, theming, routing, DI setup
  features/
    auth/
      data/              # repositories, data sources, DTOs
      domain/            # entities, use cases (optional layer, see below)
      presentation/      # widgets, screens, controllers/blocs
    profile/
    checkout/
  main.dart
```
Everything a feature needs lives together. Scales well — deleting a feature is deleting a folder. Best when the app has clear feature boundaries and/or multiple people work on different features in parallel.

**Layer-first** (fine for small apps or single-developer projects):
```
lib/
  models/
  screens/
  widgets/
  services/
  main.dart
```
Simpler to start with, but tends to become unwieldy past ~15-20 screens because unrelated features' files interleave in the same folders.

Don't recommend migrating a working small app to feature-first just for purity — the cost of a big structural refactor should be weighed against actual pain the team is feeling.

## Layering within a feature

Full Clean Architecture (data / domain / presentation with use-case classes) is valuable when:
- Business logic is complex enough to warrant testing in isolation from both UI and data sources.
- Multiple data sources need to be swapped or combined (e.g. local cache + remote API).
- The team is large enough that strict boundaries prevent stepping on each other.

It's overkill when:
- The app is mostly CRUD screens with thin logic.
- A single developer is moving fast and the extra indirection (use case classes that just call one repository method) adds files without adding clarity.

A pragmatic middle ground many production apps use successfully: **data + presentation only**, folding "domain" logic into the repository or into the state-management layer (bloc/notifier) itself. Don't insist on the full three-layer split as if it's mandatory — explain the tradeoff and let the complexity of the actual app drive the decision.

## Dependency direction

Regardless of which layering you use, keep dependencies pointing one way: presentation depends on domain/data, never the reverse. A repository should never import a widget. A bloc/notifier should never import `package:flutter/material.dart` for anything beyond `ChangeNotifier`/basic types — this is what makes business logic testable without pumping a widget tree.

## Dependency injection

For anything beyond a trivial app, avoid manually threading dependencies through constructors many levels deep, and avoid global mutable singletons accessed as static fields (hard to test, hidden coupling). Common good options:
- `get_it` — simple service locator, widely used, low ceremony.
- Riverpod's own provider graph — if already using Riverpod for state, it doubles as DI and is often the cleanest choice (no separate DI library needed).
- Constructor injection + a root-level composition in `main.dart` for small apps — perfectly fine, don't over-engineer.

## Routing

For apps with more than a handful of screens, avoid ad hoc `Navigator.push(MaterialPageRoute(...))` scattered everywhere — it makes deep linking, web URL support, and route guards painful to retrofit later. Prefer a declarative router (`go_router` is the current de facto standard for Flutter) configured in one place. Flag scattered manual navigation as a maintainability finding in audits, but don't force a routing migration on a 5-screen app with no deep-linking needs.

## God files / god widgets

Watch for:
- A single file over ~300-400 lines doing many unrelated things (common culprit: `main.dart` containing the whole app, or a `HomeScreen` with 10 nested widget-building methods instead of extracted widget classes).
- A single `build()` method over ~100 lines. Extract sub-widgets — this isn't just style, it directly affects rebuild granularity (see performance.md).

There's no hard line, but when a file makes you scroll a lot to find the thing you're editing, that's the signal to split it.
