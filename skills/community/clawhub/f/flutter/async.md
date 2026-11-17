# Async — Futures, Streams, Isolates, and Cancellation

Dart is single-threaded per isolate with an event loop. "Async" buys you non-blocking waiting, never parallelism: an `await` yields the thread while something else (I/O, a timer, the platform) works, but a synchronous loop between two awaits still freezes the frame (SKILL.md rule 6).

## The Async Gap

Every `await` is a gap during which the widget may be disposed, the route popped, and the context invalidated.

```dart
Future<void> _load() async {
  final data = await repo.fetch();      // the gap
  if (!mounted) return;                 // the gate (SKILL.md rule 2)
  setState(() => _data = data);
}
```

- The `use_build_context_synchronously` lint catches `context` after a gap. It does NOT catch a controller write, an animation start, or a `ScaffoldMessenger` call — those need the same guard with no warning.
- Need navigation or a snackbar after the gap? Capture the object BEFORE awaiting: `final nav = Navigator.of(context); await save(); nav.pop();`. This survives the widget going away in a way that a late `Navigator.of(context)` does not.
- `context.mounted` (`flutter >=3.7`) is the check inside a `StatelessWidget` callback where there is no `State.mounted`.
- Two rapid taps start two overlapping requests. Guard with a `bool _busy` set before the await and cleared in a `finally`, or debounce at the source (`forms.md`).

## FutureBuilder

- **Store the future in a field, never create it in `build`.** `FutureBuilder(future: repo.fetch(), ...)` re-fires the request on every rebuild — including rebuilds caused by the keyboard, the theme, or a parent's `setState`. Create it in `initState`, and recreate it in `didUpdateWidget` when the input prop changes (`state.md`).
- Always handle three states: `snapshot.hasError` first, then `connectionState != done`, then data. A builder that only checks `hasData` renders the loading spinner forever when the future throws.
- `snapshot.data` is null on the first frame even for a completed future — `initialData` removes the flash of empty state.
- Errors inside a `FutureBuilder` do not reach `runZonedGuarded` or the error reporter unless you forward them: log in the builder's error branch, or attach a `.catchError` that reports before rethrowing.
- For pull-to-refresh, `RefreshIndicator`'s `onRefresh` must return a future that completes when the new data is in. With a `FutureBuilder`, assign a new future inside `setState` and return it — never return the old one, or the spinner ends before the data arrives.

## StreamBuilder and Subscriptions

- A plain `Stream` from `async*` or `Stream.fromFuture` is **single-subscription**: listening twice throws `Bad state: Stream has already been listened to`. Rebuilding a `StreamBuilder` with a stream created in `build` produces exactly that. Store the stream in a field; use `.asBroadcastStream()` or a broadcast controller when there are genuinely multiple listeners.
- A broadcast stream has no replay: a listener that subscribes after an event never sees it. Screens that can be reopened need the last value cached (a `ValueNotifier`, a `BehaviorSubject`-style controller, or a repository field).
- Manual `listen()` returns a `StreamSubscription` — store it and `cancel()` in `dispose` (SKILL.md rule 3). This is the most common leak in Flutter code, and it is invisible until the callback fires on a dead widget.
- `StreamController` also needs `close()`; a controller owned by a repository closes when the repository is disposed, not when a widget leaves.
- `await for` inside a method holds the method open until the stream closes; it cannot be cancelled from outside. For anything a widget owns, use `listen` + `cancel`.

## Cancellation

Dart has no built-in future cancellation. The three real options:

| Mechanism | Use |
|---|---|
| A `CancelToken` supported by the client (`dio`) | HTTP requests: cancel in `dispose`, and on a new search keystroke |
| `StreamSubscription.cancel()` | Anything stream-shaped, including converted futures (`future.asStream().listen`) |
| A guard flag (`if (!mounted) return;`, or a request id compared on completion) | Everything else: the work still runs, but its result is ignored |

For search-as-you-type, the id comparison matters: responses can arrive out of order, and the last response is not necessarily for the last query. Store an incrementing `_requestId`, capture it before the await, and drop the result if it no longer matches.

`Future.timeout(Duration(...))` bounds the wait, not the work — the underlying request continues. Combine it with a client-level timeout (`data.md`).

## Isolates

Use one when a single synchronous unit of work can exceed the frame budget (SKILL.md rule 6): parsing a large JSON payload, image manipulation, crypto, compression, sorting tens of thousands of items.

```dart
final parsed = await Isolate.run(() => jsonDecode(body) as Map<String, dynamic>); // dart >=2.19
final parsed2 = await compute(_parse, body);                                      // any version
```

- Arguments and results are COPIED between isolates (except immutable data and `TransferableTypedData`). A payload big enough to need an isolate is also big enough that the copy costs something — measure the whole round trip, not just the parse.
- The isolate entry point must be a top-level or static function, and its captured state must be sendable: no `BuildContext`, no widgets, no platform plugin objects, no open database handles.
- An isolate hop costs spawn plus two copies. Below one frame's worth of work it is a net loss — keep small parsing on the main isolate.
- Platform channels from a background isolate need `BackgroundIsolateBinaryMessenger.ensureInitialized(rootIsolateToken)` (`flutter >=3.7`), with the token obtained on the root isolate and passed in (`platform.md`).
- Long-lived worker isolates (`Isolate.spawn` + `SendPort`) are for repeated work; they must be killed explicitly or they outlive the screen that made them.

## Timers, Debounce, Throttle

- `Timer.periodic` keeps firing after the widget is gone until you `cancel()` it (SKILL.md rule 3) — and it keeps firing while the app is backgrounded, which is a battery bug (`state.md`, app lifecycle).
- Debounce (act after quiet): cancel the pending timer on each event, start a new one. Typical for search input at a few hundred milliseconds — tune against the backend's cost, not a folklore number.
- Throttle (act at most every N): ignore events while a flag is set, clear it on a timer. Typical for scroll-driven loads.
- Both must cancel their timer in `dispose`, and both must re-check `mounted` in the callback.

## Error Handling

- `runZonedGuarded` catches uncaught async errors in the zone; `FlutterError.onError` catches framework errors. Wire both to the crash reporter at startup, or a whole class of production failures never reaches you.
- `PlatformDispatcher.instance.onError` is the modern catch-all for uncaught async errors outside the framework.
- An unawaited future that throws produces an unhandled-exception log and nothing else. Mark deliberate fire-and-forget with `unawaited(...)` and attach a `.catchError`, so the intentional case is distinguishable from the forgotten one.
- Rethrow with `Error.throwWithStackTrace(e, st)` to preserve the original stack across a boundary; a bare `throw e` in a catch block resets it and loses the origin.
