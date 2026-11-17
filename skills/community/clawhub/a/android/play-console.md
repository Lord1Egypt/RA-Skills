# Play Console — Tracks, Rollout, Policy, and Rejections

The store is a gate with its own rules, its own timing and its own reviewers. Most rejections are declaration problems, not code problems.

**Contents:** [Volatile Facts, Verified](#volatile-facts-verified) · [Tracks](#tracks) · [Staged Rollout](#staged-rollout) · [Halting and Rolling Back](#halting-and-rolling-back) · [The Declaration Surface](#the-declaration-surface) · [Data Safety](#data-safety) · [Common Rejection Causes](#common-rejection-causes) · [Appealing and Resubmitting](#appealing-and-resubmitting) · [Pre-Launch Report and Vitals](#pre-launch-report-and-vitals) · [Store Traps](#store-traps)

Store listing copy, screenshots, keyword research and conversion optimization belong to `google-play-store`; this file is the release-engineering and policy side.

**Before any submission**, read `artifacts/play-declarations.md` if the `## Boxes` index in `~/Clawic/data/android/memory.md` names it: the text previously approved is what the new submission must be consistent with, and contradicting it is a rejection.

## Volatile Facts, Verified

Four numbers here change on the store's schedule, not yours. Verify each on the store's own documentation before designing around it, and note the date you checked:

| Fact | What is stable | What to verify |
|---|---|---|
| Target API requirement | New apps and updates must target within about a year of the latest major release, enforced annually at the end of August | The exact API level required this year, and any extension process |
| Compressed download cap | There is a cap, and exceeding it forces asset packs or on-demand delivery | The current figure |
| Testing requirement for new personal developer accounts | New personal accounts must run a closed test with a minimum number of testers for a minimum period before production access | The current tester count and duration |
| Vitals bad-behavior thresholds | Play publishes crash and ANR thresholds above which store visibility can suffer | The current percentages (`crashes.md`) |

Everything else in this file is mechanism, and mechanisms have been stable for years.

## Tracks

| Track | Audience | Review | Use for |
|---|---|---|---|
| Internal testing | A small list of testers, by email | Fastest available | Every build; the fastest way to test the real signed artifact |
| Closed testing | Named lists or a group | Reviewed | Pilot groups, and the required testing period for new personal accounts |
| Open testing | Anyone who opts in | Reviewed | Scale testing before production, and the beta badge on the listing |
| Production | Everyone, subject to rollout percentage | Reviewed | The release |

- Promote the *same artifact* up the tracks rather than rebuilding: a rebuild is a different artifact, and everything you verified was verified on the old one.
- Review times vary with the account's history, the app's category and the changes made; a submission that adds a sensitive permission takes longer than one that changes a string. Plan the calendar around a variable review, never around a remembered figure.
- Internal testing is the correct destination for "does the signed release build actually work" and should be part of the normal loop, not a special event.

## Staged Rollout

- Ship to a percentage, watch, widen. A conservative ladder for a consequential release: a small single-digit percentage, then roughly a fifth, then half, then everything, with a hold long enough at each step for vitals to become meaningful — hours at minimum, a day for anything risky.
- Governed by `distribution_track` and the user's rollout preference. A tiny app with a hundred users gains nothing from a 1% stage; the point of the ladder is to have enough sessions at each step to see a regression, and too small a slice of too few users produces noise, not signal.
- The percentage applies to devices that *check for updates*, so the actual adopted share lags the number you set. Read adoption, not the setting, when judging whether a stage has enough data.
- Watch, at each stage: crash-free rate, ANR rate, and the app-specific metric that would show a broken flow (sign-ins, syncs, purchases). Vitals alone will not catch a screen that renders empty.
- Record the ladder actually used in the release row, not the one that was planned (`memory-template.md`).

## Halting and Rolling Back

- **There is no downgrade.** Halting a rollout stops *new* users receiving the build; everyone who already has it keeps it. That is the single most important operational fact about the store.
- The sequence when a release goes wrong: halt the rollout immediately (it costs nothing and is reversible), diagnose, then ship a fix as a **new build with a higher versionCode**, built from the previous tag plus the fix, and roll it out on an accelerated ladder.
- Because affected users keep the bad build until they update, a genuinely damaging bug may also need a server-side mitigation or a remote flag — the client fix reaches people over days, not minutes.
- A remote configuration flag around any risky new feature turns a release incident into a switch. That is worth building before the release that needs it.
- Every halt goes in the release row with the reason. A halted rollout is the most informative row in `releases/<year>.md`, and the pattern across several of them is a process finding.

## The Declaration Surface

Rejections cluster here, not in the code. Every one of these is a form whose answers must match the running app:

- **Permissions declarations** for policy-restricted permissions, often with a demonstration video (`permissions.md`)
- **Foreground service types**, one justification per declared type, matching observable behavior (`background.md`)
- **Data safety**: what data is collected, whether it is shared, whether it is encrypted in transit, whether users can request deletion
- **Ads declaration**, and the families policy if the audience includes children
- **Target audience and content rating**, which changes which policies apply to you
- **Account deletion**: apps that allow account creation must offer deletion, including a route that does not require installing the app
- **Financial, health, and other category-specific declarations** where they apply

Keep the exact submitted text, the date and the outcome in `artifacts/play-declarations.md`. Rewriting a declaration from memory produces a version that contradicts the approved one, and that is a rejection with a slower review.

## Data Safety

- The answers must cover **every SDK** in the app, not only your own code. An analytics, ads, crash-reporting or attribution SDK collects data on your behalf and it is your declaration.
- Re-check after every dependency addition or major upgrade. A library that started collecting an identifier in its new version silently invalidates your form.
- "Collected" and "shared" are defined by the store, not by intuition: data leaving the device to your own server is collection; data going to a third party is sharing, including to an SDK provider.
- Inconsistency between the form and observable network traffic is detectable and is treated as a misrepresentation, which is a heavier sanction than an ordinary rejection.
- Keep the completed answers in the same declarations artifact, so the next update starts from the last approved state rather than from scratch.

## Common Rejection Causes

| Cause | What actually triggers it |
|---|---|
| Policy-restricted permission without an approved declaration | The permission in the merged manifest, including from a dependency |
| Declaration text that does not match the app | A reviewer installs it and cannot find the described feature |
| Data safety inconsistent with observed behavior | Network traffic to an undeclared destination |
| Broken or unreviewable build | Crash on launch on the reviewer's device, or a login wall with no test credentials provided |
| Missing account deletion route | Account creation without a deletion path, including a web route |
| Target API level below the current requirement | The annual deadline passed |
| Misleading listing or functionality | The app does materially less than the listing claims |
| Background location without justification | The permission present at all, whatever the app does with it |

Two operational habits prevent most of these: diff the merged manifest after every dependency change, and give reviewers working test credentials plus a one-paragraph note on where the sensitive feature is.

## Pre-Launch Report and Vitals

- The pre-launch report runs the app automatically on a set of physical devices before release and reports crashes, ANRs, accessibility findings, security warnings and screenshots per device. It is free signal on hardware you do not own, and it is routinely ignored.
- Read it for the crash list first, then the accessibility findings — the latter are the ones that also affect real users and never get filed as bugs.
- Vitals after release are the release gate (`crashes.md`); the pre-launch report is the gate before it.
- Neither replaces a manual pass on a real low-end device (`devices.md`), because both are automated exploration and neither knows what your app is supposed to do.

## Store Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Rebuilding between tracks | A different artifact from the one that was verified | Promote the same build |
| Treating a halt as a rollback | Existing users keep the bad build | Halt, then ship a higher versionCode with the fix |
| Rewriting a declaration from memory | Contradicts the approved text; slower review, likely rejection | Keep the text in `artifacts/play-declarations.md` |
| Ignoring permissions a dependency added | They are declared as yours and reviewed as yours | Diff the merged manifest every dependency change (`build-failures.md`) |
| Data safety answered once | A dependency upgrade invalidates it silently | Re-check on every dependency change |
| A rollout ladder too fast for the user base to produce signal | Full rollout before any regression is visible | Hold each stage until vitals are meaningful |
| No test credentials for a login-gated app | Reviewer cannot use it; rejected as broken | Provide credentials and a note in the submission |
| Planning a launch date around a remembered review time | Review duration varies by account and change | Submit early, to internal testing first |
| Designing around a remembered size or API-level number | Both change on the store's schedule | Verify against the store's documentation (→ Volatile Facts) |

## Write Down What It Was

- **Every declaration submitted** — the exact text, date and outcome — is `artifacts/play-declarations.md` with its `## Boxes` line reading "read before any submission that touches permissions or data safety" (`memory-template.md`).
- **Every rollout, including halts and their reasons**, is a row in `releases/<year>.md`, written before the rollout starts.
- **A rejection and what resolved it** goes into the declarations artifact next to the text it changed, not into a chat log.
- **The annual target-level deadline** and the verification date of the volatile facts above are rows in `## Due` of `~/Clawic/data/android/memory.md`.
