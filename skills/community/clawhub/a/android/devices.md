# Devices — ADB, Emulators, OEMs, and Form Factors

The device is where the abstraction ends. Two apps ship identically and behave differently because of the hardware, the skin, and the settings the user changed.

**Contents:** [ADB Connection Problems](#adb-connection-problems) · [Install Failures](#install-failures) · [Wireless Debugging](#wireless-debugging) · [Emulator or Real Device](#emulator-or-real-device) · [A Device Matrix Worth Owning](#a-device-matrix-worth-owning) · [OEM Behavior](#oem-behavior) · [Form Factors](#form-factors) · [Wear, TV, and Auto](#wear-tv-and-auto) · [Device Traps](#device-traps)

**Before choosing a test device**, read `~/Clawic/data/devices/devices.md` — the shared inventory says what hardware exists, at which API level, and which one carries the OEM battery manager that explains most background bug reports (`background.md`).

## ADB Connection Problems

In order; each takes seconds:

| Symptom | Cause | Fix |
|---|---|---|
| `no devices/emulators found` | USB debugging off, or the cable is charge-only | Enable developer options and USB debugging; try a known data cable |
| Device listed as `unauthorized` | The RSA authorization prompt was never accepted | Reconnect and accept on the device; revoke authorizations in developer options and retry if the prompt never appears |
| Device listed as `offline` | Stale daemon state after a sleep, an OS update or a mode change | Kill and restart the ADB server; unplug and replug |
| Appears then disappears repeatedly | USB mode set to charging only, a hub, or a failing cable | Set the USB mode to file transfer; try a direct port |
| Two entries for one device | A wireless and a wired connection at once | Address commands with an explicit serial |
| Works for one user account, not another | Another ADB server instance owns the connection | One server per machine; stop the other |

- Always target an explicit serial when more than one device is attached; a command that silently ran on the wrong device is a debugging session lost.
- The device list with the long-form flag shows model and product names, which is how you tell two identical serial-number-shaped strings apart.

## Install Failures

The package manager's error string names the cause exactly:

| Error | Cause | Fix |
|---|---|---|
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | The installed copy was signed with a different key | Uninstall first locally; if it happens to users, the signing identity changed and that is a serious release bug (`release.md`) |
| `INSTALL_FAILED_VERSION_DOWNGRADE` | Lower versionCode than what is installed | Uninstall locally; on the store there is no downgrade at all |
| `INSTALL_FAILED_TEST_ONLY` | The APK is flagged test-only, as IDE-run builds are | Install with the test-only flag, or build the real debug artifact |
| `INSTALL_FAILED_INSUFFICIENT_STORAGE` | Genuinely full, or a stale copy of a large app | Clear space; the reported figure includes the temporary copy during install |
| `INSTALL_FAILED_NO_MATCHING_ABIS` | The APK has no native library for this device's architecture | Build the right ABI, or use a universal build for local testing |
| `INSTALL_PARSE_FAILED_NO_CERTIFICATES` | Unsigned artifact | Sign it, even for local installs |
| `INSTALL_FAILED_USER_RESTRICTED` | The OEM blocks installs over USB by default | Enable "install via USB" in the OEM's developer settings |

Uninstalling is destructive: it deletes the app's data on that device. On a device holding real user data, confirm before running it.

## Wireless Debugging

- Modern devices pair over the network from developer options with a pairing code, and then connect by address and port. This is the supported path and survives reboots better than the older approach.
- The older route enables a TCP port over USB first, then connects over the network — still useful, but the port resets on reboot and after a USB reconnection.
- Wireless debugging is slower for large installs and unreliable across VLANs and guest networks. Use it for testing gestures, foldables and physical interactions; use USB for anything install-heavy.
- Pairing codes are one-time credentials for that session. They are not something to keep in any file.

## Emulator or Real Device

| Question | Emulator | Real device |
|---|---|---|
| Behavior of a platform API at a given API level | Correct and cheap | Also correct |
| Layout across screen sizes and densities | Excellent | Limited to what you own |
| Performance numbers | Meaningless | The only source (`performance.md`) |
| Background work, Doze, battery managers | Approximate; no OEM extras | The only source (`background.md`) |
| Camera, sensors, biometrics, NFC, Bluetooth | Simulated at best | Required |
| OEM skin bugs | Impossible | The only source |
| Push delivery under real conditions | Optimistic | Realistic |
| Automated test matrix breadth | Cheap and scalable | Expensive |

Rule: emulators for breadth of platform versions and screen sizes, real hardware for anything about speed, battery or an OEM. A test plan that is emulator-only will pass while the app is unusable on a popular mid-range phone.

## A Device Matrix Worth Owning

Small, cheap and sufficient:

1. **One current mid-range phone at the newest OS** — matches most users better than a flagship does, and shows new-platform behavior.
2. **One low-end phone a few generations old, near `min_sdk`** — the performance and memory truth-teller.
3. **One device from an OEM with an aggressive battery manager** — the background-work truth-teller.
4. **One tablet or foldable**, if either form factor is supported.
5. **Emulators for everything else**: the oldest supported API level, one intermediate, the newest, plus a small-width and a large-width profile.

Write each of them into the shared `~/Clawic/data/devices/devices.md` with its API level and its quirks, so the next investigation starts on the right hardware instead of the nearest one (`memory-template.md`).

## OEM Behavior

Differences that are real, undocumented, and reported as app bugs:

- **Battery managers** kill background work, delay push and cancel alarms for apps the user has not opened recently. Behavior differs by manufacturer, regional firmware and a per-app setting buried in the OEM settings app (`background.md`).
- **Notification handling** varies: some skins collapse, deprioritize or silently drop notifications from apps in a restricted state, and some have their own per-app notification categories layered over channels.
- **Permission dialogs and auto-revocation** can differ in wording and in additional confirmation steps, which breaks UI tests that match on system dialog text.
- **Default fonts, display density and gesture navigation** vary, which is why layouts that are fine on a reference device overflow elsewhere.
- **Pre-installed launchers and app-management tools** may restrict background start or clear apps from recents aggressively, producing "the app restarts every time" reports (`lifecycle.md`).

When a bug report comes from exactly one manufacturer, the manufacturer is the hypothesis until disproven, and the finding belongs in `## Pain Points` because it will be reported again.

## Form Factors

- **Window size classes** are the supported way to be adaptive: compact, medium and expanded width, decided from the *window*, not the physical screen — a phone-sized window on a tablet in split screen is compact, and so is a folded foldable.
- Never branch on a device type ("is tablet") or on a hardcoded dp threshold outside the size-class boundaries. Multi-window, foldables and desktop-mode windows all break that assumption.
- Foldables change configuration when folded, unfolded, or placed half-open, which means a configuration change mid-interaction is a normal event, not an edge case. Everything in `lifecycle.md` about state survival applies at a much higher frequency here.
- Resizing must not lose state, and the hinge is a real obstruction: content placed under it is invisible. The window-layout information exposes the hinge's position and orientation for layouts that care.
- Test resizing by dragging a split-screen divider, not only by rotating. Continuous resize is the case that breaks layouts assuming a stable width.
- From recent target levels, apps can no longer force portrait orientation on large screens; a layout that only works in portrait becomes a visible defect rather than a preference (`sdk-upgrades.md`).

## Wear, TV, and Auto

Each is a separate target with its own module, its own store listing requirements and its own review checklist. Common threads:

- **Wear**: the app runs on a small screen with a battery measured in hours, often paired and sometimes standalone. Complications and tiles matter more than the app's own screens; background work is even more restricted than on phones; and the store has separate quality requirements.
- **TV**: no touch. Every interaction must work with a directional pad, focus must be visible at all times, and the leanback navigation model replaces scrolling-with-a-finger. A phone layout on a TV is unusable rather than merely ugly.
- **Auto**: heavily restricted interaction models with their own approved app categories and templates, designed to limit driver distraction. It is not a place to port a phone UI.
- Shared code lives in modules with no phone-UI dependency; a shared `:core:data` and separate UI modules is the standard shape (`gradle.md`).
- If the user targets any of these, record the form factors in `config.yaml` under the platform preference area so every layout recommendation accounts for them.

## Device Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Testing only on a flagship at the newest OS | Fastest device, no OEM extras, newest behavior — the least representative device available | Mid-range and low-end, plus one OEM skin |
| Emulator-only verification of background work | No battery manager, no thermal limits, unlimited allowances | A real device, unplugged, with the bucket forced |
| Branching on "is tablet" | Wrong for multi-window, foldables and desktop windows | Window size classes |
| Forcing portrait | No longer permitted on large screens at recent target levels, and hostile on tablets | Support both orientations |
| Rotating instead of resizing | Continuous resize is where adaptive layouts break | Drag a split-screen divider |
| Running a command with two devices attached | It runs on the wrong one, silently | Always address an explicit serial |
| Uninstalling to fix an install error on a user's device | Deletes their data | Understand the error string first; confirm before anything destructive |
| Assuming a wireless debugging session survives a reboot | Ports and pairings reset | Re-pair, or use USB for install-heavy work |
| A device matrix with no low-end phone | Performance and memory problems are invisible | One deliberately slow device |

## Write Down What It Was

- **Every device and emulator used for testing** gets its row in the shared `~/Clawic/data/devices/devices.md`: name, kind, model, OS and API level, identifier, and a note for its quirks — the OEM battery manager, an unusual density, a missing sensor (`memory-template.md`).
- **A retired or sold device**: delete its row and note the date in `## Pain Points`. An inventory that only grows is not an inventory.
- **An OEM-specific behavior and the workaround** is a line in `## Pain Points`, naming the manufacturer and OS version.
- **Supported form factors**, once the user states them, are a `config.yaml` key under the platform preference area, not an observation.
