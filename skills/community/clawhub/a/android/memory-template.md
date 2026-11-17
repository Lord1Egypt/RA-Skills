# Working File Templates — Android

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/android/config.yaml` | Key by key, read-modify-write |
| App context, toolchain set, modules, release setup, pain points, build health, due dates, box index | `~/Clawic/data/android/memory.md` | Rewritten in place; stays small |
| The app itself, when it has a goal, a status and milestones | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, from the first |
| Test devices and emulator profiles | `~/Clawic/data/devices/devices.md` (**shared**) | One row per device, every kind of device in one inventory |
| A client, an account owner, an external tester | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person; named from here, never copied here |
| A second app in the same workspace | `## App Context` in `memory.md` while there is one; `~/Clawic/data/android/apps.md` from the second | One row per app |
| Every shipped build and its rollout | `~/Clawic/data/android/releases/<year>.md` | Append-only, cut by year |
| Measured numbers not tied to a release — startup, jank, bundle size, build time | `~/Clawic/data/android/benchmarks/<year>.md` | Append-only series, one row per measurement, cut by year |
| Things you produced that get re-read — runbooks, keep-rule sets that finally worked, architecture decisions, targetSdk migration plans, Play declaration texts | `~/Clawic/data/android/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/android/<plural-noun>.md`, or `~/Clawic/data/android/artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line, with its read condition, in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

The last row is the one that gets used most, because no list of boxes is complete. Three questions, in order:

1. **Would another skill want to read it?** A device, a person, a project, a bill — it belongs in the shared box for that kind of thing, in the format below, not in an Android file.
2. **Is it a text read whole when its subject comes up** — a procedure, a decision and its reasoning, a set of keep rules, a declaration text, a diagram, a plan? → `artifacts/`, its own file from the first one.
3. **Is it one more row of something that accumulates?** → a section of `memory.md` until the split threshold, then its own box.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A build shipped to any track | Its row in `releases/<year>.md`, before the rollout starts |
| Crash-free and ANR numbers came in after a rollout | The same release row, appended |
| A toolchain set finally built green, or one axis moved | `## Toolchain` |
| A build or runtime failure took real effort to explain | `## Pain Points` — and `artifacts/runbook-<symptom>.md` the second time it appears |
| A module was added, removed, or renamed | `## Modules` |
| Signing, track, or package facts were established or changed | `## Release Setup` (pointers only, never key material) |
| Startup, jank, size or build time was measured | `benchmarks/<year>.md`, or the release row if it belongs to a release |
| A device or emulator profile was used for testing | Its row in `~/Clawic/data/devices/devices.md` (**shared**) |
| A keep-rule set, a migration plan, an architecture decision, or a Play declaration text was produced | `artifacts/` |
| A permission or policy declaration was submitted to Play | `artifacts/play-declarations.md` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except releases, benchmarks, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. **You**, the agent about to add the entry, run this — nobody else will. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/android/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a runbook, a keep-rule set or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:android-upload-key` · `1password:Work/Android/keystore` · `env:PLAY_SERVICE_ACCOUNT_JSON` · `file:~/keystores/upload.jks` · `vault:ci/android/signing` · `profile:release`

Android pastes carry secrets more often than most: a `gradle.properties` holds signing passwords, a `local.properties` holds SDK paths and sometimes keys, a logcat dump holds auth headers and user data, a CI log holds decoded environment. Replace each secret value before writing and leave the pointer visible: `storePassword=<keychain:android-upload-key>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: application id and package name, versionCode and versionName, keystore *alias* and keystore file *path*, certificate SHA-1/SHA-256 fingerprints (they ship inside every APK and are printed in Play Console), Play developer account id, Firebase or backend *project* ids, device models and serials, emulator AVD names, API base URLs, ABI and locale lists, module names, permission and foreground-service-type names, certificate *pin hashes*. **Secrets, strip them**: keystore and key passwords, the keystore file's contents, any private key, Play service-account JSON, push server keys, OAuth client secrets and refresh tokens, API keys of any service, database encryption passphrases, and any bearer token or user identifier that appears in pasted logcat output.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared devices inventory](#shared-devices-inventory) · [shared project file](#shared-project-file) · [shared contacts](#shared-contacts) · [apps.md](#appsmd) · [releases/](#releases) · [benchmarks/](#benchmarks) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/android/` if it does not exist.

```yaml
ui_toolkit: compose
min_sdk: 26
target_sdk: 35
build_language: kotlin-dsl
di_framework: hilt
module_layout: by-feature
ci_platform: github-actions
crash_reporting: crashlytics
distribution_track: closed
size_budget_mb: 60
cold_start_budget_ms: 800
destructive_confirm: true

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
platform:
  form_factors: [phone, tablet, foldable]
  test_matrix: [pixel-6-api34, galaxy-a14-api33]
conventions:
  version_code_scheme: "YYMMDD0 + build counter"
  release_branch: "release/<versionName>"
constraints:
  banned_libraries: [rxjava]
  privacy_regime: families
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Android Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Releases 2026 (14) → `releases/2026.md`; read before planning any release or rollback
- Startup and size series 2026 (22) → `benchmarks/2026.md`; read before claiming a performance change worked
- R8 keep rules for the payments SDK (1 set) → `artifacts/keep-rules-payments.md`; read whenever a release-only crash mentions a missing class
- Play declaration texts (4) → `artifacts/play-declarations.md`; read before any submission that touches permissions or data safety
- targetSdk 35 migration plan (18 items) → `artifacts/targetsdk-35-migration.md`; read while the upgrade is in flight

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| targetSdk deadline check | year, before 31 August | 2026-05-02 | 2027-05-02 |
| Dependency + BOM sweep | month | 2026-07-06 | 2026-08-06 |
| Baseline profile regeneration | per release with UI change | 2026-07-19 | next release |
| Keystore backup restore test | year | 2025-11-10 | 2026-11-10 |
| Vitals review | week while rolling out | 2026-07-24 | 2026-07-31 |

## App Context
com.acme.field — field-service app, Kotlin + Compose, minSdk 26, targetSdk 35, single Play developer account, distributed on closed track to 40 pilot users.

## Toolchain
AGP 8.6.1 · Gradle 8.9 · JDK 17 (temurin) · Kotlin 2.0.21 · Compose BOM 2024.12.01 · KSP. Green as of 2026-07-19; JDK 21 breaks the Hilt processor here, do not move it alone.

## Modules
:app · :core:data · :core:ui · :feature:jobs · :feature:sync

## Release Setup
Play App Signing on. Upload key `keychain:android-upload-key`, alias `upload`, file `file:~/keystores/upload.jks`. Upload cert SHA-256 fingerprint recorded in `releases/2026.md` header. Service account for CI uploads: `env:PLAY_SERVICE_ACCOUNT_JSON`. versionCode scheme: date-based, see config.

## Pain Points
2026-06-11: sync silently stopped on Xiaomi devices — OEM battery manager killed the worker; fixed by moving to a foreground service for the user-initiated sync path.
2026-04-02: release-only crash in the payments screen, R8 stripped a Moshi adapter; keep rules in artifacts.

## Build Health
Clean build 4m10s, incremental 38s (2026-07-19, M2 Pro). Configuration cache on. CI clean build 9m with cache hit.

## How They Work
Ships every second Friday. Wants the diff, not the whole file. Reads Gradle output fluently, new to R8.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here. The targetSdk row is dated from Play's annual deadline, not from a fixed API number.
- **`## Toolchain`**: one line per aligned set, plus the one-line reason any obvious upgrade is blocked. This is the section that stops the next session re-deriving a version matrix that took an afternoon.
- **`## Pain Points`**: date, symptom, actual cause, what changed. One line each. The second appearance of the same symptom promotes it to `artifacts/runbook-<symptom>.md`.
- **`## Release Setup`**: paths, aliases, fingerprints and pointers only. If a password ever appears here, it is a bug — replace it with its pointer and say so.
- **`## Build Health`**: clean and incremental times with the date and the machine, because a number without a machine cannot be compared next quarter.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their app, toolchain and release habits |
| `complete` | Know the app, the module layout and the release path well |

## Shared devices inventory

Lives at `~/Clawic/data/devices/devices.md` and is shared with every other skill that knows about the user's hardware — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Devices

| Name | Kind | Model | OS / API | Identifier | Location | Notes |
|------|------|-------|----------|------------|----------|-------|
| pilot-pixel | phone | Pixel 6 | Android 14 / API 34 | serial 1A2B3C4D | desk | main debug device |
| cheap-a14 | phone | Galaxy A14 | Android 13 / API 33 | serial 9F8E7D6C | drawer | low-end perf baseline, One UI battery manager |
| avd-api30 | emulator | Pixel 2 AVD | API 30, x86_64 | avd Pixel_2_API_30 | local | used by the instrumented test job |
```

- **Identity is `Name`** — the network name the device answers to, or its MAC when it has no stable hostname. That is the key the shared box uses, so a home-automation skill and this one land on the same row instead of writing the same hardware twice. A phone or an emulator takes the label you address it by (`pilot-pixel`, `avd-api30`); its serial, AVD name and MAC go in `Identifier`, never in the key. Read the file before adding and look the device up by that key: if it is there, update the row in place — it is yours. Rows written by other skills (a thermostat, a laptop, a router) are never touched.
- **Foreign columns win.** If you arrive and the shared file already has a different column set, **match its columns and never rewrite its header** — put the device label in whatever the key column is and add anything missing as trailing columns. Two parallel layouts of `~/Clawic/data/devices/devices.md` is the failure to avoid.
- **Retirement is part of the inventory.** When a device is sold, wiped or retired, delete its row and note the date in `## Pain Points` of `memory.md`. An inventory that only grows stops being an inventory.
- **Identifiers are serials and AVD names, never credentials.** A device serial identifies; an ADB pairing code or a wireless-debugging token does not belong in any file.
- **Scale cut**: one row per device while there are ≤15. Past that, one file per device at `~/Clawic/data/devices/<name>.md` with the same fields, and `~/Clawic/data/devices/devices.md` becomes the index (`Name | Kind | Model | → file`). If the folder already looks like that, follow it — do not start a parallel inventory.
- Any measurement taken on a device (cold start, jank) goes to `benchmarks/<year>.md` with the device `Name` in its own column, not into this row. This file says what exists; the series says what it did.

## Shared project file

When the app is a piece of work with a goal, a status and milestones — a client build, a launch, a rewrite — it lives at `~/Clawic/data/projects/<project>.md`, shared with every planning and delivery skill.

```markdown
# Field Service App

status: active
goal: replace the paper job sheets for 200 field techs by Q4
milestones:
- 2026-05-01 closed track with 40 pilot users — done
- 2026-09-01 production rollout at 20% — in progress
decisions:
- 2026-04-12 Compose over XML for new screens; interop kept for the map screen (see android/artifacts/adr-compose-adoption.md)
```

- **Identity is the file name** (kebab-case project slug). One file per project, from the first. Read it before adding; if it exists, update in place.
- **Baja**: never delete the file. Set `status: done | cancelled — <date>` inside it; past roughly 20 closed projects, move it to `projects/archive/<project>.md` without renaming.
- **Only the summary lives there.** The technical artifact — the ADR, the diagram, the migration plan — stays in `~/Clawic/data/android/artifacts/` and is referenced by file name, so it is not duplicated and cannot drift.
- If the project file already exists with different headings, adopt its shape and add your lines under it; never restructure a file another skill owns.

## Shared contacts

A client whose app this is, a Play account owner, a named external tester or a reviewer contact is a person, and people live at `~/Clawic/data/contacts/contacts.md`:

`Name | Key | Role | Preferred channel | Context | Last contact | File`

- **Identity is `Key`**: lowercase email if there is one, otherwise a handle, otherwise `<kebab-name>` with a stable disambiguator. The key is a column of the row — never implicit.
- Read before adding; if the key exists, update that row in place. Never touch a row this skill did not write.
- Past 15 people, or as soon as one does not fit in a row, split to `~/Clawic/data/contacts/<name>.md` per person and leave `contacts.md` as the index with the `File` pointer.
- **From the Android side, only the name travels.** `apps.md` and the project file name the person; the person's details never get copied into an Android file. Duplicating a person is how two skills end up contradicting each other.

## apps.md

One app lives in `## App Context`. From the second, this file:

```markdown
# Apps

| Application id | Name | Toolkit | minSdk / targetSdk | Track | Owner / client | Signing |
|----------------|------|---------|--------------------|-------|----------------|---------|
| com.acme.field | Field Service | compose | 26 / 35 | closed | us | Play App Signing, upload key `keychain:android-upload-key` |
| com.brightco.pos | BrightCo POS | views | 24 / 34 | production | BrightCo (see contacts) | client-held keystore, `1password:Clients/BrightCo/keystore` |
```

When an app belongs to a client, the client goes in the shared `~/Clawic/data/contacts/contacts.md` and is referenced here by name only. Never duplicate the client record inside the Android box.

## releases/

Born as its own file with the first release, cut by year. The row is written **before** the rollout starts; the vitals columns are filled in after.

```markdown
# Releases — 2026

Upload cert SHA-256: AB:CD:… (public fingerprint, printed in Play Console)

| Date | versionName | versionCode | Track | Rollout | Tag / commit | Mapping file | Crash-free % | ANR % | Notes |
|------|-------------|-------------|-------|---------|--------------|--------------|--------------|-------|-------|
| 2026-07-10 | 3.4.0 | 2607100 | closed | 100% | v3.4.0 / 9f2c1ab | uploaded to Play + `artifacts/` | 99.7 | 0.21 | — |
| 2026-07-24 | 3.5.0 | 2607240 | production | 20% → halted | v3.5.0 / a41b7e2 | uploaded to Play | 98.9 | 0.55 | halted at 20%, sync crash on API 30; fixed in 3.5.1 |
```

- One row per uploaded build, including builds that were halted — a halted rollout is the most useful row in the file.
- `Rollout` records the ladder actually used, not the plan.
- Vitals percentages carry no more precision than Play reports, and the date they were read goes in `Notes` if it is not roughly 48 hours after the row's date.
- A rollback is a new row with a higher versionCode, never an edit of the old one (SKILL.md Rule 9).

## benchmarks/

Measurements not tied to a release, so a claim like "startup got better" can be checked. Born as its own file with the first measurement and **cut by year**, exactly like `releases/`: a measurement series grows without end and is read by date, so the current year is the file you open and the closed years stay readable beside it. Never a single flat file that accumulates forever.

```markdown
# Benchmarks — 2026

| Date | Metric | Value | Device | Build variant | Baseline profile | Note |
|------|--------|-------|--------|---------------|------------------|------|
| 2026-07-19 | cold start p50 | 940 ms | cheap-a14 | release | yes | after profile regeneration |
| 2026-07-19 | download size | 41 MB | — | release AAB | — | arm64 split |
| 2026-07-19 | clean build | 4m10s | M2 Pro laptop | — | — | configuration cache on |
```

- Append to the current year's file; the first measurement of January creates the new one and the old year is never edited again. Its `## Boxes` line goes in the same turn.
- Device names match the shared inventory. A measurement without its device and build variant is not comparable to anything and should not be written.
- Comparing across a year boundary means opening both files — that is the cost of the cut, and it is cheaper than a file nobody can scroll.
- If you find a flat `benchmarks.md` from an earlier version, move its rows into `benchmarks/<year>.md` by their dates, delete it, and fix its `## Boxes` line.

## artifacts/

One file per thing, at `~/Clawic/data/android/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **runbook** for a symptom that recurred, **keep-rule set** that fixed a release-only failure, **architecture decision**, **targetSdk migration plan**, **Play declaration text**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Keep rules — payments SDK
*Read when a release build throws ClassNotFoundException or a JSON model comes back empty. Written 2026-04-02.*

Why each rule exists, then the rules themselves. A keep rule with no reason gets deleted by
the next person cleaning up, and the crash comes back.
```

```markdown
# Play declarations — permissions and data safety
*Read before any submission that adds a permission, a foreground service type, or a data category. Updated 2026-07-10.*

The exact text submitted for each declaration, the date, and the outcome. Resubmitting a
declaration that differs from the approved one is a rejection.
```

```markdown
# Architecture decision — Compose for new screens
*Read before starting a new screen or proposing a rewrite of an old one. 2026-04-12.*

Decision: ...one sentence...
Rejected: ...and why, with the number that decided it...
Consequences: ...what this makes harder...
```

If the user tracks this work as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by file name.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`pain-points.md` — `## Pain Points`, oldest first. The reason this file exists is that the same three bugs come back every year on new devices; without dates the pattern is invisible.

`modules.md` — `## Modules`, one line per module with its dependencies and why it exists. Only worth extracting past ~15 modules, at which point the dependency direction matters more than the list.

`toolchain-history.md` — `## Toolchain`, one dated line per version set. Extract only when the upgrade history itself is being used to plan the next upgrade; otherwise the current set alone belongs in `memory.md`.
