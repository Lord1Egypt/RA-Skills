# SDK Upgrades — Raising compileSdk, targetSdk and minSdk

Three numbers, three different risks. Confusing them is the most expensive mistake in Android maintenance.

**Contents:** [What Each Number Does](#what-each-number-does) · [The Upgrade Procedure](#the-upgrade-procedure) · [Testing a Behavior Change Before You Opt In](#testing-a-behavior-change-before-you-opt-in) · [Per-Level Detail](#per-level-detail) · [Raising minSdk](#raising-minsdk) · [The Play Deadline](#the-play-deadline) · [Upgrade Traps](#upgrade-traps)

**Before starting an upgrade**, read `## App Context` and `## Due` in `~/Clawic/data/android/memory.md`, and open `artifacts/targetsdk-<n>-migration.md` if the `## Boxes` index names one — an upgrade in flight has a plan, and restarting it from scratch loses the list of what was already verified.

## What Each Number Does

| Number | Meaning | Risk of raising it | Safe cadence |
|---|---|---|---|
| `compileSdk` | Which APIs you can *compile against* | Almost none: new warnings and new lint checks | Raise freely, usually first |
| `targetSdk` | Which behavior changes the OS *applies to you* | High: every change up to that level activates at once | One level per release, deliberately |
| `minSdk` | The oldest OS you *run on* | Loses users; gains simpler code | Only against install-base data |

Compile against the newest SDK and target one level at a time. Compiling high and targeting low is a supported, normal state — it is how you get new lint checks and new APIs while choosing when to accept new behavior.

## The Upgrade Procedure

1. **Read the official behavior-changes list for the level**, in both its flavors: changes for *all apps* (they apply on the new OS regardless of target) and changes for *apps targeting* that level. The first set is already affecting your users; the second is what you are about to opt into.
2. **Raise `compileSdk` alone and ship that.** New lint errors and deprecation warnings arrive here, decoupled from behavior. Fix them while nothing has changed at runtime.
3. **Write the plan** to `artifacts/targetsdk-<n>-migration.md`: one line per behavior change, each marked *not applicable*, *needs work*, or *verified*. This is the file that makes the upgrade resumable and the reason the next upgrade takes a day instead of a week.
4. **Test each change with its compatibility toggle** while still targeting the old level (below) — this is the step that turns a risky release into a boring one.
5. **Raise `targetSdk`, run the full instrumented suite on at least one device on the new OS and one several versions older**, and re-check the permission, background-work and display paths by hand. Emulators are adequate for behavior changes and inadequate for OEM behavior (`devices.md`).
6. **Ship to an internal or closed track first**, watch vitals for a rollout window, then widen (`play-console.md`).
7. **Update `## App Context`** with the new levels and mark the `## Due` deadline row done.

## Testing a Behavior Change Before You Opt In

The platform ships a per-app compatibility framework: individual behavior changes are toggleable on a debuggable app, so you can activate exactly one change and test it in isolation while `targetSdk` is unchanged.

- The toggles are visible in the device's developer options under app compatibility changes, and settable from the shell with the app-compat command against your package and the change's id or name.
- Test one change at a time. The whole point is attribution: if you flip five and the app breaks, you learned nothing.
- Toggles only work on debuggable builds and only for changes that are gated by target level. Anything in the "all apps" list is already live and cannot be toggled off — those need real fixes now, not at upgrade time.
- Strict mode with the relevant detectors on catches a further class of upcoming problems (unsafe intent launches, non-SDK API usage, disk on main thread) before the platform starts enforcing them (`debug.md`).

## Per-Level Detail

The headline table lives in `SKILL.md` (→ Target SDK Breakage). This is what each one actually costs.

**23 — runtime permissions.** Every dangerous permission needs a request at the point of use plus a denied path that still works. The rationale state machine is the subtle part (`permissions.md`).

**24 — `FileUriExposedException`.** Any `file://` URI handed to another app throws. A `FileProvider` with an authority and an paths XML replaces it, and the receiving app needs the URI permission granted on the intent.

**26 — background limits and channels.** Background services stop being startable while the app is in the background; implicit broadcasts mostly stop being delivered to manifest-registered receivers. Every notification needs a channel, and the channel's importance is immutable after creation (`background.md`).

**28 — cleartext off, non-SDK restrictions.** HTTP without TLS is blocked unless a network security config allows it per-domain. Reflection into hidden platform APIs starts being restricted, with warnings before enforcement (`networking.md`).

**29 — scoped storage arrives.** Media goes through MediaStore, app files go to the app-specific directories, and everything else needs the Storage Access Framework. Background location becomes a separate second prompt, and starting an activity from the background is blocked with a short list of exemptions.

**30 — scoped storage enforced, package visibility.** The opt-out is gone. Querying other installed packages requires `<queries>` entries; `QUERY_ALL_PACKAGES` is a policy-restricted permission and a rejection risk (`play-console.md`). Unused-permission auto-reset begins.

**31 — mutability and exported.** Every `PendingIntent` must specify `FLAG_IMMUTABLE` or `FLAG_MUTABLE` or the app crashes on creation; immutable is the default choice, mutable only when a system component must fill in the intent (a notification reply). Every activity, service and receiver with an intent filter must declare `android:exported` explicitly, and the build fails without it. Exact alarms become permission-gated; the splash-screen API applies to every cold launch, so a custom splash activity now shows twice unless it is removed.

**33 — notifications and media.** `POST_NOTIFICATIONS` becomes a runtime permission: an app that never requests it simply stops being seen, and the request must be justified in context or it is denied by reflex. `READ_EXTERNAL_STORAGE` splits into per-type media permissions; the photo picker needs no permission at all and is the better answer for most apps (`permissions.md`).

**34 — foreground service types.** Every foreground service declares a type in the manifest and holds the matching permission; the type must genuinely match the work, and Play asks you to justify it. Runtime-registered broadcast receivers must pass an exported flag. Implicit intents to internal components stop working.

**35 — edge-to-edge and time caps.** Your content draws behind the system bars by default; anything laid out without insets handling suddenly sits under the status bar or the navigation bar. Handle window insets properly rather than re-adding a fitsSystemWindows shim, because the direction of travel is one-way. Long-running `dataSync` foreground services gain a per-day time budget, which breaks designs that used one as a permanent background worker.

**Beyond 35.** Recent levels have continued along the same three roads — display insets and predictive back, further background-work limits, and large-screen or orientation behavior. Read the current behavior-changes page rather than trusting any table's last edit, and add the new level's row to the migration artifact.

## Raising minSdk

- Decide from the install-base distribution for *your* app, not the global one: Play Console reports the API level split of your actual users, and it is often nothing like the market average.
- Each level dropped removes compatibility branches, `if (SDK_INT >= …)` forks, and sometimes an entire support library. The saving is real but one-off; the user loss is permanent.
- Below API 21 you pay legacy multidex and its startup cost; below 24 you pay core library desugaring for modern Java APIs. Those two thresholds are where the tax is visible in the build.
- Practical rule: raise minSdk when the affected slice is small enough that you would not build a feature for it. Announce it in release notes — users on the old version simply stop receiving updates, silently, which is a support ticket you can prevent.

## The Play Deadline

- The mechanism is stable and the number is not: new apps and updates must target an API level within roughly a year of the latest major release, enforced on an annual date at the end of August. Existing apps that miss it stop being discoverable to new users on newer devices rather than being removed.
- Extensions are available on request in some circumstances, and a Wear or TV target has its own level. Verify the current requirement on Play's official target-level page before planning the year (`play-console.md` carries the number with its verification date).
- Treat it as a calendar item, not a surprise: the `## Due` row is "targetSdk deadline check, every year, before 31 August", and the check is one page load.

## Upgrade Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Raising `compileSdk` and `targetSdk` in one commit | Compile errors and behavior changes arrive together and cannot be attributed | Ship the compileSdk bump first |
| Skipping levels ("we were on 31, go to 35") | Four levels of behavior changes activate simultaneously | Still do the work level by level in the plan, even if the number moves once |
| Testing the upgrade only on the newest emulator | The changes you opted into apply on *older* devices too, where your fallback code runs | Test on the new OS and on a device near `min_sdk` |
| Assuming `compileSdk` changes runtime behavior | It does not; only `targetSdk` does — this confusion produces both false alarms and missed work | Read the two lists separately (step 1) |
| Adding `tools:overrideLibrary` to keep a library that requires a higher minSdk | Compiles, then crashes on exactly the devices the library excluded | Raise minSdk or drop the library |
| Re-adding legacy behavior with a compat shim (fitsSystemWindows, opting out of edge-to-edge) | Buys one release and makes the next upgrade harder | Do the insets/permission/type work once |
| Losing the migration checklist in chat | The next level's upgrade starts from zero and re-tests what was already verified | `artifacts/targetsdk-<n>-migration.md` with its `## Boxes` line |

## Write Down What It Was

- **The migration plan and its per-change status** is `artifacts/targetsdk-<n>-migration.md`, created when the upgrade starts, with its `## Boxes` line reading "read while the upgrade is in flight" (`memory-template.md`).
- **The new levels** update `## App Context` in `~/Clawic/data/android/memory.md` when the upgrade ships.
- **A behavior change that broke something** is a line in `## Pain Points` with the level, the symptom and the fix — the next app you upgrade will hit the same one.
- **The annual deadline check** is a row in `## Due`, dated from Play's calendar, not from the API number.
