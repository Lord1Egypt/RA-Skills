---
name: "cloud-file-hydration-nudge"
description: "Hydrate visible but unreadable cloud placeholder files with provider-aware read verification."
---

# Cloud File Hydration Nudge

## Purpose

When a cloud-synced file is visible but unreadable, hydrate it only after proving the read failure and identifying the provider/path behavior. Do not assume a previous provider's workaround applies to the current file.

## Core Rule

Metadata visibility is not readability. Provider state is diagnostic, not proof. The proof is a successful bounded content read by a normal process.

Quick Look is deprecated for automated hydration workflows. Do not use Quick Look as a routine nudge.

If provider sync is paused, offline, quit, or otherwise unavailable, stop and inform the user. Do not start OneDrive, resume sync, or change provider sync state without explicit consent.

## Required Workflow

1. Identify the exact file path and source folder.
2. Confirm the file is visible without modifying it.
3. Run a bounded read probe, normally:

```bash
dd if="/path/to/file" of=/dev/null bs=64k count=1
```

4. If the read succeeds, do not nudge hydration; continue with the downstream parser/check.
5. If the read fails, capture the error and inspect provider state when available:

```bash
ls -laO@ "/path/to/file"
fileproviderctl evaluate "/path/to/file"
```

6. Determine the provider before selecting a nudge. Use path clues, File Provider state, and platform resource values where available.
7. Check for paused/offline/unavailable sync state. If found, report it and request consent before changing provider state.
8. Use the least-invasive provider-native or provider-UI hydration method first.
9. Repeat the exact same bounded read probe.
10. Continue downstream only after that read succeeds.
11. Leave a short note with pre-read result, provider determination, nudge action, post-read result, and downstream outcome.

## Permission Boundary

Keep broad runtimes narrow. Do not grant general Node, shell, or scheduler processes broad Accessibility, Screen Recording, Full Disk Access, or equivalent macOS privacy powers just to hydrate cloud files.

Constrained boundary rule:

- Safe generic automation may enumerate narrow approved folders, classify provider paths, inspect filesystem flags, call non-UI diagnostics, and run bounded read probes.
- Privacy-gated UI actions, Finder Accessibility automation, previews, screen access, or provider UI button presses belong in a trusted helper application or another narrow user-approved automation host.
- If the trusted helper application or approved host is not available, leave unreadable files pending and report that provider/manual hydration is needed.
- Do not fall through to Quick Look because a trusted helper application is unavailable.

## Intake Workflow Boundary

Folder watchers or Automator Folder Actions may acknowledge or enqueue a visible file before it is hydrated. That acknowledgement is not a delivery signal.

For intake workflows, use two phases:

1. **Enqueue:** record the path when a folder action, watcher, or scan sees it.
2. **Deliver:** copy/import only after bounded read proves the file is hydrated.

Dataless files should remain pending/retry candidates. Do not repeatedly full-scan large folders just to rediscover the same pending placeholders.

Observed Automator result: a temporary Folder Action on a disposable OneDrive folder fired for a newly added file, but did not fire its `adding folder items` handler when the existing file was later offloaded with `/unpin` or hydrated with Finder cloud-button `AXPress`. Do not depend on Automator Folder Actions to notice hydration state changes for existing placeholders.

## iCloud Drive Workflow

For iCloud-visible/dataless files, use Apple's ubiquitous-item download API before any UI-based fallback.

1. Confirm the file is an iCloud ubiquitous item.
2. Request native hydration with `startDownloadingUbiquitousItem`.
3. Poll the same bounded read until it succeeds or times out.
4. Optionally re-check provider state after success.

Example Swift shape:

```swift
import Foundation

let url = URL(fileURLWithPath: "/path/to/file")
let values = try url.resourceValues(forKeys: [
    .isUbiquitousItemKey,
    .ubiquitousItemDownloadingStatusKey,
    .ubiquitousItemIsDownloadingKey
])

if values.isUbiquitousItem == true {
    try FileManager.default.startDownloadingUbiquitousItem(at: url)
}
```

Then poll externally with the same bounded read:

```bash
for i in {1..30}; do
  if dd if="/path/to/file" of=/dev/null bs=64k count=1; then
    exit 0
  fi
  sleep 1
done
exit 1
```

Do not use Quick Look for iCloud hydration. If native iCloud download fails or times out, explain the failure and ask the user how they want to proceed.

## OneDrive Workflow

For OneDrive File Provider-backed folders, prefer a real provider download/materialization control and verify with a bounded read. Do not treat policy state, badges, command output, or pinning as proof that bytes are local.

Observed provider signals for dataless OneDrive placeholders may include:

```text
filesystem flags: compressed,dataless
isDownloaded = 0
isDownloadRequested = 0
isMostRecentVersionDownloaded = 0
bounded read: Resource deadlock avoided
```

### Preferred OneDrive Nudge Order

1. Confirm the file is OneDrive-backed by path and/or File Provider state.
2. Run the bounded read and record the exact failure.
3. Inspect provider state with `fileproviderctl evaluate`.
4. If File Provider reports `isSyncPaused = 1`, OneDrive is quit, or sync appears offline/unavailable, stop and ask before changing sync state.
5. If a trusted helper application or approved narrow user-context automation host is available, use the Finder/provider cloud-status download button for the target file or folder.
6. Poll File Provider state and the same bounded read until every target file is readable.
7. Only continue downstream after bounded read success.
8. If no trusted helper application or approved user-context host exists, leave the file pending and tell the user provider/manual hydration is needed.

### Finder Cloud Button Automation

In macOS Finder list view, OneDrive may expose the not-downloaded cloud glyph as an Accessibility button inside the selected row's Name cell:

```text
role = AXButton
description = Not downloaded
actions = AXPress
```

When this control is present, pressing `AXPress` invokes the same provider UI download action as clicking the Finder cloud icon. This is the first proven non-Quick-Look OneDrive automation fallback in the observed macOS File Provider test environment.

Safety requirements:

- Use only after an actual bounded-read failure.
- Select or reveal the exact target path before looking for the button.
- Force Finder list view before locating the selected-row Name cell; the observed list-path AX traversal did not work in icon, column, or gallery/flow view.
- Confirm the button description is `Not downloaded` or equivalent provider cloud-download state.
- Press only that button; do not open or preview the file.
- Poll `fileproviderctl evaluate`, filesystem flags, and bounded read afterward.
- For folder-level hydration, poll every intended child file; do not trust the folder button press, folder `isDownloaded = 1`, or the first folder state alone.
- Treat broad Accessibility grants, especially to general runtimes such as `node`, as temporary test permissions. Prefer a trusted helper application or constrained automation host for production.

Implementation guidance:

- Pass paths to AppleScript as arguments, such as `osascript - "$path"`, rather than embedding paths into generated AppleScript text. This avoided quoting bugs with apostrophes, spaces, ampersands, and Unicode accents in observed tests.
- Missing cloud button is not automatically failure. If the bounded read succeeds, report already hydrated and do nothing.
- Revealing a dataless file and switching Finder to list view did not by itself hydrate the file in a control test; the download button press was still needed.

Observed successful file pattern:

```text
pre: compressed,dataless; isDownloaded = 0; bounded read failed
nudge: Finder selected-row cloud AXButton, AXPress
post: isDownloaded = 1; isMostRecentVersionDownloaded = 1; bounded read succeeded
```

### OneDrive Edge Cases To Handle

- Already-hydrated files may expose no cloud download button. First run a bounded read; if it succeeds, report already hydrated and do not press anything.
- Filenames with apostrophes, spaces, ampersands, Unicode accents, and duplicate-looking names worked when Finder selection used exact path/alias and AppleScript received paths as arguments.
- A 25 MB test file hydrated successfully through Finder `AXPress`; no long-lived `isDownloading = 1` state was observed at that size.
- `/Applications/OneDrive.app/Contents/MacOS/OneDrive /unpin <file>` may print a failure such as `status=-1895824895` while still offloading the file. Verify post-state instead of trusting command output.
- `/Applications/OneDrive.app/Contents/MacOS/OneDrive /pin <file>` may fail or may set policy without materializing bytes. It is not proof of hydration.
- `/unpin <folder>` did not recurse in observed tests. If offload testing is needed, operate per file and verify each child.
- Folder cloud-button hydration can work recursively, including nested child files, but a helper must poll every target child with bounded reads until success or timeout.
- A folder may report `isDownloaded = 1` while `isRecursivelyDownloaded = 0`; do not treat folder `isDownloaded` as proof that child bytes are available.
- Temporary FSEvents observation saw events during offload and hydration, suggesting event-driven intake is plausible. Automator Folder Action testing separately showed `adding folder items` did not fire for offload/hydration of an existing file.
- Paused/offline/quit sync should be treated as a user-controlled state. Do not start, resume, or unpause OneDrive without consent.

### OneDrive Paths That Are Not Proof Of Hydration

The following may be useful diagnostics or policy controls, but must not be treated as confirmed hydration unless the bounded read succeeds afterward:

- Opening or updating the OneDrive folder in Finder.
- `fileproviderctl evaluate com.microsoft.OneDrive.FileProviderActions.MarkPinned <file>`; observed macOS rejected this custom action as invalid even when listed by evaluation output.
- `/Applications/OneDrive.app/Contents/MacOS/OneDrive /pin <file>`; observed behavior either failed or set pinned/Always Available policy while leaving the file `compressed,dataless` and unreadable.
- Finder `Always Keep on This Device`; this may set policy but still requires bounded-read verification.

## Other File Provider Workflows

For Dropbox, Google Drive, Box, or other File Provider-backed folders:

1. Prefer the provider's supported download/materialization mechanism if present.
2. Use visible UI automation only when native APIs or documented provider actions are unavailable or blocked, and the workflow explicitly permits it.
3. Verify with the same bounded read; provider metadata alone is not enough.

## Quick Look Deprecation

Quick Look is deprecated for automated cloud-file hydration. It should not be built into intake scripts, scheduled retry loops, provider nudges, or parser workflows as an automated fallback.

Reason: Quick Look opens UI and invokes preview parsers. That makes it broader and riskier than provider-native or provider-UI hydration controls.

If all provider-native, provider-UI, and approved trusted-helper approaches fail, tell the user plainly that a manual Quick Look attempt may hydrate the file. Present it as a user-operated recovery option, not as an automated step:

```text
The safer provider hydration methods did not materialize this file. Quick Look is deprecated for automated hydration because it opens a preview parser, but you can manually try Quick Look in Finder if you accept that risk. Afterward, I will re-check with the same bounded read before continuing.
```

After any manual Quick Look attempt, always repeat provider-state checks and the same bounded read. Do not continue downstream based only on the user seeing a preview.

## Logging Template

Use a compact local note:

```text
File: <relative/private-safe path>
Pre-read: failed/succeeded, error if failed
Provider evidence: iCloud ubiquitous / File Provider downloaded/current flags / dataless flags
Nudge: native iCloud download / Finder cloud-button AXPress / provider-native action / other
Post-read: failed/succeeded
Downstream: parser/import/report result
Quick Look: not used; or manual user attempt after deprecated warning
Security: approved automation host if UI automation was used; or trusted-helper boundary
```

## Caution

Do not delete, move, or overwrite user files during hydration testing. If a hydrated file conflicts with prior work, compare it against the current authoritative baseline before replacing any parsed export or downstream classification surface.
