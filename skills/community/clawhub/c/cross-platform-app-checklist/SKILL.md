---
name: cross-platform-app-checklist
description: Review multi-platform app changes and release readiness for UI, lifecycle, permissions, media and distribution risks. Produces platform-specific findings, evidence gaps and test plans for iOS/iPadOS, Android and desktop apps. Use for compatibility or app-release reviews, not standalone API explanations or prose edits without app-behavior or distribution impact.
license: MIT-0
metadata:
  version: "0.1.1"
---

# Cross-platform app checklist

Review app changes and release candidates for failures caused by differences
between platforms: layouts after resize, large text, input methods, lifecycle,
permissions, device capabilities and native distribution. The result is a scoped,
per-platform review with stable checklist IDs, prioritized findings,
evidence gaps and next actions, plus physical-device plans and release blockers.

Use the app's actual targets among **iOS, iPadOS, Android, macOS, Windows and
Linux**, including phone, tablet, foldable and desktop-window scenarios. The
rules come from defects encountered while shipping Flutter apps; platform rules
also apply to other frameworks and separate native implementations, with
Flutter API/plugin notes available
on demand. This is a review guide, not an automated test runner or a claim that
every framework/target has been tested.

## What it reviews

The **65 stable IDs** connect each rule to the failure it prevents and a
verification recipe. Read the relevant sections of these references on demand:

| Capability | IDs | Reference |
|---|---|---|
| Layout across sizes, breakpoints, runtime resize, safe areas, keyboards, rotation and folds | L1–L8 | [layout](references/layout.md) |
| Large/localized text, pixel density, live scale changes, icons, theme, contrast and motion | D1–D7 | [display](references/display.md) |
| Touch, pointer, keyboard/IME, navigation, assistive input, system formats, links and sharing | I1–I9 | [input](references/input.md) |
| Lifecycle, persistence, process death, background work, instances, transfers, migrations and sync | B1–B8 | [lifecycle](references/lifecycle.md) |
| Permission declarations/denial, privacy, data at rest, file grants, capture, billing and audience rules | P1–P9 | [permissions](references/permissions.md) |
| Audio sessions/routes, camera, cross-platform formats, memory, notifications and optional hardware | M1–M8 | [media/devices](references/media-devices.md) |
| Desktop windows, close/quit/tray behavior, filesystem paths, packaging and Apple compatibility surfaces | W1–W4 | [desktop](references/desktop.md) |
| Frame pacing, size/startup budgets, energy and thermal behavior | F1–F3 | [performance](references/performance.md) |
| Device matrix, layout/OS-resize tests, parity, release artifacts, interruptions, networks and diagnostics | X1–X9 | [testing](references/testing.md) |

For the chosen distribution channels, review publisher/package identity,
privacy/content declarations, listing materials and review access, signed
artifacts, release tracks and safe updates. The [store guide](references/stores.md)
([中文](references/stores.zh-CN.md)) selects rules by channel, package model,
territory and app type under **P4/P8/P9/W4/X6**, without a second checklist.

## Two review modes

- **Change (`change`):** the default for a daily UI or platform change. Select
  affected IDs and reachable dependencies; always consider X1 (reach), X4 (device
  evidence) and X5 (parity), adding X6 for artifact, native-dependency, signing or
  distribution changes. Explain excluded areas; do not turn unreviewed areas
  into N/A or expand a narrow diff into 65 boilerplate rows.
- **Release (`release`):** for assessing whether an app candidate is ready to ship
  or submit. Use the [complete catalog](references/checklist.md) to account for
  **all 65 IDs on every shipped target**. Missing evidence stays outstanding.
  If both change findings and release readiness are requested, use full coverage
  and highlight the changed areas rather than duplicating two review records.

Honor an explicit narrow mode. A reference to a “release build” or “next release”
alone does not request a full release review. Standalone API explanations and
prose-only edits with no app-behavior or distribution change do not need this
checklist; answer those requests directly.

## Review and report

1. **Scope:** identify project/revision, diff or candidate, framework, shipped
   targets/form factors and relevant channels; add package model/territory for
   store rules. Infer from artifacts, label assumptions and bundle consequential
   unknowns into a focused question. Missing project/shipping scope permits
   provisional findings, not invented targets or complete release coverage.
   Missing channel details need not delay a scoped layout review.
2. **Inspect:** follow the selected references' verification recipes. Shared
   changes reach every shipped target; separate native implementations also
   need parity review (X5). Check default store reach (X1). In change mode load
   only affected sections; in release mode read every area's applicable details
   and the chosen-channel store sections. Use [Flutter notes](references/flutter.md) for Flutter and
   [sources](references/sources.md) for version gates. Recheck current official
   policies and record URL/date; runtime OS, build/target SDK, deployment minimum
   and channel are distinct. Historical reference dates are not fresh evidence.
3. **Report:** state the resolved scope, mode, selected IDs, exclusions and
   assumptions, followed by prioritized findings:

   `Priority | ID | platform | status | evidence / gap | next step`

   Split partly proven items by case/target; a passing case leaves the others
   outstanding. Change review says release readiness was not assessed; release
   review retains full per-target coverage. Separately list **physical-device
   plan**, **release blockers** and **limitations**, explaining empty sections.
   Distinguish code defects, product decisions, owner materials and hardware
   qualification. Use the
   [testing evidence template](references/testing.md#report-template) and
   [store record](references/stores.md#report-record) for their applicable scope.

## Status and evidence

- **verified:** actual test/inspection supports the named case; record result,
  evidence link, revision/build and relevant OS, size, scale and settings. Source
  declarations alone cannot close packaged or runtime requirements.
- **to do:** a defect, missing decision/material, unrun check or unknown scope,
  with a next action. CI claims, skips and absent artifacts are not success.
- **needs device:** untested hardware behavior with a physical-device scenario,
  expected observation and evidence to retain; simulators do not prove it.
- **not applicable:** a scope-backed feature/platform/channel reason. Missing
  access/evidence, time pressure or “desktop only” alone does not qualify.

Keep **required / conditionally required / recommended**, issue priority and
verification status distinct. **P0** breaks a core function or applicable required
rule; **P1** degrades a common scenario; **P2** is enhancement/niche. Derive release
blockers from the applicable rule and unresolved risk; a recommendation is not
a universal submission requirement.

Screenshot goldens do not prove native UI, OS resize or process-death recovery.
X6 release evidence binds to final reviewed head, actual job/step outcomes,
executed tests, conditional skips and final artifact hashes. Final app/engine/
plugin headers, package metadata, applicable signing checks and target-machine
install/load tests are separate evidence; host CPU, tool ABI, source labels and
filenames do not substitute for them. Local tests do not establish store approval.

## Authorization boundary

Default to **read-only review**. Code changes, commits, builds that modify the
project, tool installation, signing, uploads and deployment need user
authorization; this skill adds none. Honor existing authorization and recommend
fixes at their cause with
parity checks. An owner/account gap need not stop independent analysis. Record
material names, purpose and acquisition location, never secret values. Account
creation and new platform agreements require their own authorization.
