# Lifecycle — State Survival, Navigation, and the Back Stack

Android can destroy your UI at any moment and rebuild it from a Bundle. Every lifecycle bug is a disagreement about what "any moment" includes.

**Contents:** [The Three Deaths](#the-three-deaths) · [Testing Process Death](#testing-process-death) · [Callback Order, and What Is Guaranteed](#callback-order-and-what-is-guaranteed) · [Saved State Budget](#saved-state-budget) · [Navigation and the Back Stack](#navigation-and-the-back-stack) · [Launch Modes and Task Affinity](#launch-modes-and-task-affinity) · [Predictive Back](#predictive-back) · [Deep Links](#deep-links) · [Background Start Restrictions](#background-start-restrictions) · [Lifecycle Traps](#lifecycle-traps)

**Before diagnosing a "state disappears" report**, read `## Pain Points` in `~/Clawic/data/android/memory.md`: this class of bug repeats per screen, and the previous instance names the tier that was wrong.

## The Three Deaths

Every piece of state must survive the right one (SKILL.md Rule 4):

1. **Recomposition / redraw** — constant, cheap. `remember`, a field on the ViewHolder, a local variable.
2. **Configuration change** — rotation, dark mode, font scale, window resize on a foldable or in split screen, language change. The Activity is destroyed and recreated in milliseconds; the process lives. `ViewModel` and `rememberSaveable` survive; anything in the Activity or Fragment does not.
3. **Process death** — the system reclaims your process while the app is in the background, then restores the task when the user returns. The ViewModel is gone; only `SavedStateHandle`, `onSaveInstanceState`, `rememberSaveable` and persistent storage survive. The user sees the same screen with the same arguments, so the app must be able to rebuild from ids.

The failure mode that reaches production: state survives rotation (tested) and dies on process death (never tested), so the screen returns blank or crashes on a null argument after the user spent twenty minutes in another app.

## Testing Process Death

Three steps, and all three are needed:

1. Enable "Don't keep activities" in developer options for the configuration-change path, then turn it back off — it exaggerates and does not simulate real process death.
2. Background the app, then `adb shell am kill <package>` (kills as the system would; `force-stop` is different and also stops alarms and jobs), then return to the app from Recents.
3. Verify: the screen renders with its data, no crash on a null argument, scroll position and in-progress text preserved, and no duplicate network call storm on restore.

Put this on the release checklist for every screen with meaningful state. It takes under a minute and it is the single highest-yield manual test on Android.

## Callback Order, and What Is Guaranteed

- Going away: `onPause` → `onStop` → `onDestroy`. Only `onPause` is effectively guaranteed to run before the process can be killed; `onStop` and `onDestroy` may never happen. Anything that must not be lost is committed by the time `onPause` returns, and `onPause` must be fast because it blocks the next activity's appearance.
- `onSaveInstanceState` runs before the activity becomes stoppable — on modern versions after `onStop` in ordering terms, which is why transactions after it throw.
- Coming back: `onRestart` → `onStart` → `onResume` for a stopped activity; a recreated one runs the full `onCreate` with a non-null saved state Bundle.
- Lifecycle-aware components remove most of this: `repeatOnLifecycle(Lifecycle.State.STARTED)` starts collection at STARTED and *cancels* it at STOPPED. The deprecated `launchWhenStarted` suspends rather than cancels, which leaves the upstream flow hot and producing — that distinction is invisible in a demo and expensive on battery (`architecture.md`).
- `DefaultLifecycleObserver` on the owner beats overriding callbacks in the Activity: the component that needs to know registers itself.

## Saved State Budget

- Saved state crosses a Binder transaction, and the transaction buffer is about 1 MB **shared across the whole process** — concurrent transactions eat the same budget, so the practical safe size for one screen's state is tens of kilobytes, not hundreds.
- Exceeding it throws `TransactionTooLargeException`, often not at the moment of saving but later, on an unrelated call, which makes it look random.
- What belongs in saved state: ids, selected indices, a query string, scroll position, an in-progress form's fields. What does not: lists of model objects, bitmaps, parsed responses. Save the id; load the object again.
- The same budget applies to intent extras: passing a large object between screens is the other way apps hit this. Pass the id.

## Navigation and the Back Stack

- The back stack belongs to the *task*, not to the app's memory. It survives process death, which is why every destination must be rebuildable from its arguments alone.
- A single-Activity architecture with a navigation graph means the whole app shares one task entry, one saved-state owner and one place where deep links resolve — that consolidation is the actual benefit, not the reduced Activity count.
- Arguments are typed and part of the destination; anything not in the arguments is not available after restore. A "pass the selected object through a shared ViewModel" shortcut works until process death.
- Nested graphs scope a ViewModel to a flow (checkout, onboarding) so it clears when the flow ends. A ViewModel scoped to the whole graph is a global by another name.
- Up (the app's hierarchy) and Back (the user's history) are different. A deep link that lands mid-hierarchy needs a synthesized back stack, or Up leaves the app.

## Launch Modes and Task Affinity

| Mode | Behavior | Legitimate use |
|---|---|---|
| `standard` | A new instance every launch | Almost everything |
| `singleTop` | Reuses the instance if it is already on top; delivers `onNewIntent` | Search or notification targets that must not stack |
| `singleTask` | One instance in the task; clears everything above it on relaunch | An app-wide entry point, rarely |
| `singleInstance` | Alone in its own task | Genuinely separate surfaces; a frequent source of Recents weirdness |

- With `singleTop` or `singleTask`, the new intent arrives at `onNewIntent`, **not** `onCreate` — a deep link handled only in `onCreate` silently does nothing when the activity is already open. Handle both paths through one function.
- Flags on the intent (`FLAG_ACTIVITY_CLEAR_TOP`, `NEW_TASK`) interact with the manifest mode; when the two disagree, the behavior is hard to reason about. Choose one place to express the intent.

## Predictive Back

- The system back gesture can show an animated preview of the destination. Participating means declaring support and replacing legacy `onBackPressed` overrides with the back-callback API, registered against the lifecycle owner so it is only enabled when it should intercept.
- A callback that is always enabled swallows back and traps the user. Enable it exactly while there is something to intercept (unsaved changes, an open sheet) and disable it immediately after.
- Intercepting back to show an "are you sure" dialog on every exit is a dark pattern and reads as a bug; intercept for unsaved work only.

## Deep Links

- Declare the intent filter with the exact scheme, host and path pattern. Test resolution from the shell with a VIEW intent rather than by tapping links in a chat app, which rewrites URLs.
- App Links (verified `https` links that open the app directly, with no chooser) require `android:autoVerify="true"` plus an assetlinks JSON file served over HTTPS at the domain's well-known path, containing the app's signing certificate fingerprint. With Play App Signing, that fingerprint is the *app signing* certificate's, not the upload key's — using the wrong one is the most common reason verification silently fails (`release.md`).
- Verification status is inspectable per package on the device; a failed verification degrades the link to a chooser, which users read as the app being broken.
- Unverified custom schemes can be claimed by any app on the device. Never carry an auth token in one (`security.md`).

## Background Start Restrictions

- Starting an activity from the background is blocked with narrow exemptions (a visible foreground service with a full-screen intent, a recent notification interaction, a system-granted exemption). An app that "opens itself" on an event will not on a modern release.
- The supported pattern is a notification: high-importance channel, a full-screen intent only for genuine alarm-and-call cases, and the user chooses.
- Foreground service starts from the background are equally restricted, with their own exemption list — the work goes to WorkManager expedited work instead (`background.md`).

## Lifecycle Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Testing only rotation | Rotation keeps the process; the real bug is process death | `am kill` from Recents (→ Testing Process Death) |
| `android:configChanges` to "fix" rotation state loss | Suppresses recreation, so the app keeps resources for the old configuration and the state bug persists for process death | Use the right state tier instead |
| Holding an Activity reference in a singleton or a static | Leaks every rotation; memory grows visibly | Application context, or nothing |
| Deep link handled only in `onCreate` | Nothing happens when the activity is already running | Handle `onNewIntent` too |
| An always-enabled back callback | Back stops working and users force-quit | Enable only while there is something to intercept |
| Passing objects through the back stack or intent extras | `TransactionTooLargeException` at an unrelated moment | Pass ids |
| Work started in `onResume` without cancellation in `onPause` | Duplicated on every return, and runs while invisible | Lifecycle-scoped collection with `repeatOnLifecycle` |
| Assuming `onDestroy` runs | It may never be called | Persist by `onPause` |

## Write Down What It Was

- **A state-loss bug and the tier that was wrong** goes to `## Pain Points` in `~/Clawic/data/android/memory.md`, naming the screen — the same mistake recurs per screen until the pattern is written down (`memory-template.md`).
- **A navigation or task-mode decision** (single-Activity, nested graph scoping, a non-standard launch mode and its reason) is an `artifacts/adr-<name>.md` with its `## Boxes` line; launch modes are re-litigated by everyone who touches them.
- **The process-death check** belongs on the release checklist artifact, so it is not remembered only when it fails.
