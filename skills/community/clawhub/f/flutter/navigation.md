# Navigation — Routes, Results, Deep Links, and Back

Read `router` from config (SKILL.md Configuration); with `auto`, check `pubspec.yaml` — `go_router` present means URL-shaped routing, absent means imperative `Navigator`. Do not mix the two mental models in one app: a `Navigator.push` on top of a declarative router produces a route the router does not know about, and the URL and the stack disagree from then on.

## The Two Models

| | Imperative (`Navigator.push`) | Declarative (`go_router` and friends) |
|---|---|---|
| Stack is | Whatever you pushed | Derived from the current location |
| Deep links | Handled manually in `onGenerateRoute` | Free: a path maps to a stack |
| Web URL | Not reflected without work | The source of truth |
| Best for | Modals, wizards, self-contained flows | Apps with tabs, deep links, or a web target |
| Cost | Impossible to reason about after a dozen routes | Learning curve, and redirect logic that must stay pure |

Both can coexist inside one screen's local flow (a dialog stack, a nested wizard) as long as the app-level stack has a single owner.

## Push, Pop, and Results

- `Navigator.push<T>` returns `Future<T?>`. The result is `null` when the user backs out — handle it, do not force-unwrap.
- After awaiting a push, the widget may be gone: `mounted` check before touching anything (`async.md`).
- `pop` with a result must match the push's type parameter, or you get a runtime cast error nobody sees until that path runs. Typed helpers per route are worth the boilerplate.
- `pushReplacement` disposes the previous route immediately — its `State`, controllers, and scroll positions are gone. Use it for login → home, never for a step in a flow the user might return to.
- `pushAndRemoveUntil(route, (r) => false)` clears the whole stack; `(r) => r.isFirst` keeps the root. Getting this wrong strands the user with no back button, or with a back button into a logged-out screen.
- `popUntil` does not pop dialogs reliably — a dialog is a route too, so a stray `showDialog` becomes part of the stack. Use `rootNavigator: true` deliberately when popping past dialogs.
- Every push builds the new route while the old one stays alive in memory. A push loop (A → B → A → B) grows the stack forever; use `pushReplacement` or a router that dedupes.

## Passing Arguments

- Constructor arguments through a `MaterialPageRoute` builder are type-safe and the default choice.
- `RouteSettings.arguments` with named routes is dynamic: a wrong type crashes at cast time in the destination. If the app uses named routes, centralize the extraction in one place per route and validate there.
- Deep-link parameters are always strings from an untrusted source. Parse and validate at the boundary (`int.tryParse`, not `int.parse`); an unparseable id must route to a not-found screen, never crash.
- Never pass a whole model when an id will do: a stale object from a list screen renders outdated details, and it breaks deep-link entry into the same route.

## Back Button and Interception

- `PopScope` (`flutter >=3.16`) replaced `WillPopScope`. The modern shape is: `canPop: false` plus a pop-invoked callback that decides what to do (show a confirm dialog, then pop manually). Newer SDKs supply a result-aware callback (`onPopInvokedWithResult`) — check which one your SDK exposes and use that.
- The old `WillPopScope` returned a `Future<bool>`; that model is gone because it cannot support predictive back on Android, where the system needs to know up front whether the pop is allowed.
- Interception applies to the system back gesture, the hardware button, AND `Navigator.pop` from your own code. An unsaved-changes guard must therefore also cover the app bar's back button.
- On iOS the swipe-back gesture is provided by `CupertinoPageRoute`; a `MaterialPageRoute` on iOS still gets it through the platform-adaptive page transition, but a custom `PageRouteBuilder` does not unless you build it in (`adaptive.md`).

## Nested Navigators and Tabs

- Persistent bottom navigation with per-tab history needs a `Navigator` per tab (a `StatefulShellRoute` in go_router, or `IndexedStack` of `Navigator`s manually). Without it, switching tabs resets the inner stack.
- A nested `Navigator` swallows pops: the system back button pops the inner stack first. Wire the root's back handling to check the inner navigator's `canPop()`.
- `Navigator.of(context)` finds the NEAREST navigator. Pushing a full-screen route from inside a tab pushes it inside the tab (under the bottom bar) — `Navigator.of(context, rootNavigator: true)` is the fix, and it is what dialogs and full-screen modals want.
- Preserve scroll and form state across tab switches with `IndexedStack` or keep-alives (`state.md`), and be explicit about the memory cost.

## Deep Links and URLs

- Two platform pieces are required and are the usual cause of "the link opens the app but lands on home": Android `intent-filter` with `android:autoVerify` plus an `assetlinks.json` on the domain; iOS Associated Domains entitlement plus an `apple-app-site-association` file. Neither is Dart code (`platform.md`, `release.md`).
- Cold start vs warm start take different paths: the initial link arrives as the app's initial route, later links arrive as a stream. Handle both, or links work only while the app is already running.
- Test the cold path with the platform tools, not by tapping a link in a note app — the debug launch flow differs.
- On web, the browser URL is the state. Use path-based URLs (not the leading `#`) only if the host can serve `index.html` for every path, or refresh on a deep route 404s.
- Redirects (auth gates) must be pure functions of the location and the session, with no side effects: a redirect that also writes state can loop, and the loop presents as a frozen white screen.

## Route Observation

- `RouteObserver<PageRoute>` registered in `MaterialApp.navigatorObservers` plus `RouteAware` on a screen gives `didPush`/`didPopNext` — the correct hook for "refresh this screen when the user comes back to it". Subscribe in `didChangeDependencies` and unsubscribe in `dispose`.
- Analytics screen tracking belongs in an observer, not in every screen's `initState`: one place, no missed routes, and it survives new screens being added.
- `ModalRoute.of(context)?.isCurrent` answers "am I the visible route" — useful for suppressing work in screens buried under the stack.

## Dialogs, Sheets, and Overlays

- `showDialog`/`showModalBottomSheet` push a route and return a future with the dismissal result; `null` means barrier-dismissed. Treat that as "cancel", explicitly.
- The builder's context is a DIALOG context — `Navigator.pop(context)` there pops the dialog. Popping the underlying screen from inside a dialog requires the captured outer navigator.
- Showing a dialog from `initState` throws (no route yet): defer with `addPostFrameCallback` (`widgets.md`).
- A dialog opened during a route transition can end up on the wrong navigator; `useRootNavigator: true` is the predictable default for app-level dialogs.
- `Overlay` entries (tooltips, custom toasts, drag feedback) are not routes: the back button does not dismiss them, and they must be removed manually or they persist across navigation.
