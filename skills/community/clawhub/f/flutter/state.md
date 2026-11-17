# State — Lifecycle, Keys, and Preservation

The `State` object outlives the `StatefulWidget` that created it. A widget is a throwaway configuration rebuilt constantly; the `State` persists as long as the `Element` at that tree position is reused. Every "my state vanished" and "my state went to the wrong row" bug is a question about Element reuse.

## Lifecycle, in Order

| Hook | Runs | What belongs here |
|---|---|---|
| `createState` | Once per Element | Nothing but `=> _MyState()` |
| `initState` | Once, before the first build | Controllers, subscriptions, `addListener`, kicking off the initial fetch |
| `didChangeDependencies` | After `initState`, and again whenever an inherited dependency changes | Anything needing `context`-derived values: `Theme`, `MediaQuery`, an inherited repository |
| `build` | Every frame the element is dirty | Pure widget construction. Nothing else (SKILL.md rule 8) |
| `didUpdateWidget(old)` | The parent rebuilt with a new widget of the same type | React to changed `widget.*` props: re-subscribe, restart an animation, swap a controller |
| `deactivate` | Removed from the tree, may be reinserted in the same frame | Rare; reparenting through a `GlobalKey` goes through here |
| `dispose` | Removed for good | Cancel and dispose everything `initState` created, in reverse order (SKILL.md rule 3) |

- `context` works in `initState` for reading, but not for inherited-widget subscriptions: `Theme.of(context)` there returns a value and never rebuilds you when it changes. Anything that must track a change belongs in `didChangeDependencies`.
- `initState` cannot `await`. Kick the work off and handle completion behind a `mounted` guard; use `WidgetsBinding.instance.addPostFrameCallback` when you need the first frame to exist first (showing a dialog, measuring a `RenderBox`).
- **`didUpdateWidget` is the hook most codebases forget.** A `StatefulWidget` whose `userId` prop changes will NOT re-fetch unless you compare `oldWidget.userId != widget.userId` and act — the `State` is reused and `initState` never runs again. Symptom: navigating from user A to user B shows A's data.
- `dispose` runs after `deactivate`; touching `context` there is invalid. Capture what you need (a `NavigatorState`, a `ScaffoldMessengerState`) into a field earlier.

## Element Reuse: the Matching Algorithm

When a parent rebuilds, Flutter walks the new child list against the old Elements at the same positions and reuses an Element when **`runtimeType` matches AND `key` matches** (two null keys count as matching). Otherwise the old Element is deactivated, its `State` destroyed, and a new one inflated.

Consequences worth memorizing:

- Swapping a `Container` for a `Padding` at the same position destroys everything below it — scroll offsets, text field contents, animation progress.
- Toggling `if (cond) A() else B()` destroys A's state when the condition flips. If that state must survive, keep both alive (`Offstage`, `IndexedStack`) or lift the state above the conditional.
- Wrapping a subtree in a new widget (adding a `Center`) rebuilds it from scratch once: harmless for stateless trees, destructive for stateful ones.
- Two children of the same type at the same position always match — which is exactly why a reordered list without keys keeps the OLD state in each slot and only swaps the incoming data.

## Keys

| Key | Use it for | Trap |
|---|---|---|
| `ValueKey(v)` | List items keyed by a domain id | The value must be stable and unique within that list; index-based keys break on reorder |
| `ObjectKey(o)` | Items whose identity is the object itself, not a field | Identity-based; a rebuilt model instance is a different key |
| `UniqueKey()` | Deliberately forcing one fresh subtree | Inside a builder it recreates the subtree every frame (SKILL.md rule 4) |
| `PageStorageKey(v)` | Preserving scroll offset per tab or page | Required inside `TabBarView`/`PageView`, whose children are rebuilt |
| `GlobalKey()` | Reaching a `State`, or reparenting a subtree across the tree | App-wide unique; blocks subtree reuse; throws "multiple widgets used the same GlobalKey" on duplication |

- **Where the key goes**: on the outermost widget of the item, at the same level as its siblings. A key on an inner child does nothing for the sibling-matching pass.
- The canonical demonstration: two stateful colored boxes in a `Row`, swapped on tap. Without keys the colors swap and the internal state stays put; with a `ValueKey` on each, the state travels with the item.
- `AnimatedList` and `ReorderableListView` require stable keys as a hard precondition — reorders corrupt silently without them.
- `GlobalKey<FormState>` is the one routinely justified `GlobalKey`: `Form` exposes no other access path (`forms.md`).

## Preserving State Deliberately

| Situation | Mechanism |
|---|---|
| Scroll offset inside a tab or page | `PageStorageKey` on the scrollable |
| Tab content must not rebuild when you leave the tab | `AutomaticKeepAliveClientMixin`: `wantKeepAlive => true`, and call `super.build(context)` |
| Several screens alive at once | `IndexedStack` — every child is built and retained |
| State across app restarts | Persist it (`data.md`); no widget mechanism survives process death |
| State across a hot reload | Hot reload preserves `State`; hot restart does not (`debug.md`) |
| Restore after Android kills a backgrounded app | `RestorationMixin` + `restorationId`, verified with "Don't keep activities" enabled |

`AutomaticKeepAliveClientMixin` and `IndexedStack` both trade memory for retention: every retained page keeps its widget tree, its decoded images, and its subscriptions alive. Inside a list, keeping items alive defeats the viewport's recycling entirely — set `addAutomaticKeepAlives: false` on long lists whose items do not need it.

## `setState` Discipline

- `setState` marks this Element dirty; the whole subtree below rebuilds except `const` subtrees and children passed through unchanged (SKILL.md rule 5). Narrow the widget, not the callback.
- Mutating a field WITHOUT `setState` is a silent no-op that appears to work whenever something else happens to rebuild the widget — the worst class of UI bug, because it is intermittent. Every mutation of rendered state goes inside the closure.
- Mutating a list in place (`_items.add(x)`) then calling `setState(() {})` satisfies `setState` and breaks every consumer that compares old and new by identity: `didUpdateWidget` prop checks, `AnimatedList`, most state management libraries. Assign a new list instead: `_items = [..._items, x]`.
- `setState` during `build` or inside `dispose` throws; both point at a side effect in the wrong place (SKILL.md rule 8).
- The closure should contain only the mutation. Work inside `setState(() async {...})` is worse than useless — the callback is synchronous, and an async closure returns before mutating.

## App Lifecycle

`WidgetsBindingObserver.didChangeAppLifecycleState` reports `resumed`, `inactive`, `paused`, `hidden`, and `detached`. Use it to pause timers, cameras, and location streams: a `Timer.periodic` keeps firing in the background and drains battery until the OS suspends the process.

- `paused` is the last reliable point to persist unsaved user input; `detached` may not run at all.
- Register in `initState` (`WidgetsBinding.instance.addObserver(this)`) and remove in `dispose` — a missed removal leaves a dead `State` receiving callbacks for the life of the app.
- On resume, re-check anything the OS may have revoked while you were away: permissions, Bluetooth state, an expired auth token (`platform.md`).
