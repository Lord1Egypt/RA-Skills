# Views — XML Layouts, Fragments, RecyclerView, and Interop

The View system still runs most shipped Android code. It is not deprecated, it is finished: the bugs are known and the fixes are stable.

**Contents:** [Binding Views](#binding-views) · [Fragments](#fragments) · [RecyclerView](#recyclerview) · [Layouts That Perform](#layouts-that-perform) · [Custom Views](#custom-views) · [Interop With Compose](#interop-with-compose) · [Migration Order](#migration-order) · [View Traps](#view-traps)

Applies when `ui_toolkit` is `views` or `both`. Compose-side rules: `compose.md`.

**Before proposing a migration or a new screen**, read `## App Context` in `~/Clawic/data/android/memory.md` and any `artifacts/adr-*.md` its `## Boxes` index names for the Compose/View boundary: which screens stay XML, and why, is a decision that was made once and should not be reopened by accident.

## Binding Views

- ViewBinding generates a typed class per layout and is the default: no annotation processor, no findViewById, null-safe for views absent in a configuration variant (they become nullable).
- DataBinding adds expressions in XML and two-way binding, and costs an annotation processor plus errors that surface as generated-code compile failures. Take it only if two-way binding is genuinely used; ViewBinding for everything else.
- In a Fragment, the binding must be released: hold it in a nullable backing field, assign in `onCreateView`, and null it in `onDestroyView`. The Fragment instance outlives its view, so a retained binding is a retained view hierarchy — the most common leak in View-based apps.
- `findViewById` in new code is a bug in waiting: it compiles against a layout it does not know, and a renamed id fails at runtime.

## Fragments

- **`viewLifecycleOwner`, not `this`.** Observing a LiveData or launching a repeat-on-lifecycle collection with the Fragment as the owner registers a new observer for every view recreation while the old ones are still alive: the callback fires two, three, five times and the "duplicate network call" bug appears. The Fragment lifecycle and the Fragment *view* lifecycle are two different things, and view-scoped work uses the view one.
- Transactions after `onSaveInstanceState` throw `IllegalStateException`. The fix is to perform the transaction from a lifecycle state where it is legal — `commitAllowingStateLoss` converts a crash into a screen that silently does not appear, which is strictly worse to debug.
- Results between fragments go through the Fragment Result API or a shared ViewModel scoped to the navigation graph. Direct references between fragments outlive the fragments.
- Arguments arrive in the `arguments` Bundle and nowhere else: a constructor parameter is lost on recreation, because the system recreates the fragment with the no-arg constructor.
- The Navigation component gives typed arguments, a back stack that survives recreation, and deep-link handling that matches what the manifest declares. Manual `FragmentTransaction` stacks are legitimate but must reimplement all three.

## RecyclerView

- `ListAdapter` with a `DiffUtil.ItemCallback` is the default. `areItemsTheSame` compares identity (the id); `areContentsTheSame` compares displayed content. Getting the first one wrong makes every update a full rebind and kills animations.
- `notifyDataSetChanged()` rebinds everything, cancels animations and loses scroll anchoring. It exists for a genuine full replacement of an unrelated dataset, which is rare.
- ViewHolders are recycled with whatever the previous item left in them. Every `onBindViewHolder` sets **every** mutable property, including visibility and text that "is always there" — a conditional set produces content bleeding between rows, which reads as a data bug.
- Cancel per-row asynchronous work in `onViewRecycled`: an image load or a coroutine started in bind will otherwise land on a row now showing something else.
- `setHasFixedSize(true)` when the list's size does not change with content — it skips layout passes on every update.
- Nested RecyclerViews share a `RecycledViewPool` to avoid re-inflating identical inner rows; horizontal-in-vertical lists without one inflate constantly during scroll.

## Layouts That Perform

- ConstraintLayout flattens hierarchies: `0dp` on a dimension means "match constraints", chains distribute space, and barriers and guidelines remove wrapper views. A flat ConstraintLayout beats nested LinearLayouts with weights, which force a double measure pass per nesting level.
- Measure depth, not opinion: the layout inspector shows the tree, and a hierarchy more than about ten levels deep on a list row is a scroll-performance problem.
- `merge` as a root in an included layout removes the redundant wrapper; `ViewStub` defers inflation of rarely shown branches until first use.
- Overdraw: a window background, plus an opaque root background, plus a card background paints the same pixels three times. The device's developer options have an overdraw debug view; two layers is normal, four is a scrolling problem.
- Every touchable element is at least 48 dp in both dimensions, and every non-decorative view has a content description or is explicitly marked as decorative. Accessibility scanning belongs in the pre-release checklist, not in a later cleanup pass.

## Custom Views

- `onMeasure` must call `setMeasuredDimension` on every path and must honor the `MeasureSpec` mode: `EXACTLY` means take that size, `AT_MOST` means do not exceed it, `UNSPECIFIED` means the parent is asking what you want.
- Zero allocations in `onDraw`. A `Paint`, a `Path`, a `Rect` or a lambda created per frame turns into GC pressure during scroll — allocate as fields and reuse.
- `invalidate()` redraws; `requestLayout()` re-measures the whole branch. Calling the second when the first suffices is a common source of jank in custom components.
- Save and restore instance state: override `onSaveInstanceState`/`onRestoreInstanceState` and give the view an id, or its state disappears on rotation while its neighbors survive.
- Hardware acceleration is on by default; a handful of canvas operations are unsupported or slow on the GPU path, and the symptom is a view that renders correctly in a preview and blank on a device.

## Interop With Compose

- `ComposeView` puts Compose inside a View hierarchy; `AndroidView` puts a View inside Compose. Both are supported and both are the right answer during a migration.
- Inside a Fragment, a `ComposeView` needs the correct `ViewCompositionStrategy` — the default disposes on window detach, which is wrong for a Fragment whose view is detached and reattached, and produces a composition that never comes back.
- `AndroidView` takes a `factory` (called once) and an `update` block (called on every recomposition that touches its reads). Doing setup work in `update` re-runs it constantly.
- Theming does not cross the boundary automatically: a Compose island inside a Material Components theme needs a Compose theme that mirrors it, and a View island inside Compose keeps its XML theme. A design system that exists only on one side is the real cost of a half-migration.
- Two scroll containers across the boundary (a Compose lazy list inside a `NestedScrollView`) do not cooperate. Keep scrolling ownership on one side.

## Migration Order

When moving a View codebase to Compose, order by risk:

1. New screens in Compose, hosted in the existing navigation. No migration, just a boundary.
2. Leaf components with no state (rows, chips, empty states) — highest reuse, lowest risk.
3. Whole screens whose state is already in a ViewModel; the ViewModel does not change.
4. Screens with custom drawing or complex gestures — last, because they are where the View system is genuinely strong and where Compose requires new skills.
5. The navigation host — only after most destinations are Compose, because a mixed navigation graph is worse than either pure form.

Never migrate a screen that is about to be redesigned, and never migrate as a side effect of a bug fix. Record the boundary decision in `artifacts/adr-<name>.md` so the answer to "why is this screen still XML" survives the person who decided it.

## View Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Observing with `this` in a Fragment | Duplicate observers after every view recreation | `viewLifecycleOwner` |
| Keeping the ViewBinding past `onDestroyView` | Leaks the whole view hierarchy | Null the backing field in `onDestroyView` |
| Fragment constructor parameters | Lost when the system recreates the fragment | `arguments` Bundle |
| `commitAllowingStateLoss` to stop a crash | Turns a crash into a missing screen | Do the transaction at a legal lifecycle point |
| Conditional property setting in `onBindViewHolder` | Recycled holders show the previous row's content | Set every mutable property on every bind |
| `notifyDataSetChanged` for a single-item update | Full rebind, lost animations and scroll anchor | `ListAdapter` with a correct DiffUtil callback |
| Allocating in `onDraw` | GC pauses exactly during scroll | Fields, reused |
| Nested weighted LinearLayouts | Double measure per nesting level | ConstraintLayout with chains |
| A `ComposeView` in a Fragment with the default composition strategy | The composition disposes and never returns | Set the strategy that matches the fragment view lifecycle |
| Static or Activity-context references held by a View or adapter | Leaks the Activity across rotation | Application context for anything longer-lived than the view |

## Write Down What It Was

- **A leak or duplicate-callback bug and its cause** goes to `## Pain Points` in `~/Clawic/data/android/memory.md` — the `viewLifecycleOwner` class of bug recurs in every new screen until the team has seen it once (`memory-template.md`).
- **The Compose/View boundary decision** — which screens stay XML and why — is `artifacts/adr-<name>.md` with its `## Boxes` line, not a chat message.
- **A per-screen migration status list**, once it exists, is a section of `memory.md` and splits to its own box past ~15 screens.
