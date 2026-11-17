# Desktop specifics (W1–W4)

Desktop apps must handle freely resized windows, several monitors, pointer
and keyboard input, visible files, and OS-specific installation / updates.
Use [layout.md](layout.md), [display.md](display.md) and [input.md](input.md)
for shared UI rules; the rules here concern desktop integration.

## W1 Window management — P1

**Rule.** Treat saved geometry as a preference to validate against today's
displays and work areas, not as an instruction to place a window off-screen.

- Clamp default / restored size and effective minimum to the available
  work area, allowing for window decorations, taskbar / Dock / menu bar.
  If the preferred minimum exceeds it, provide a compact / scrollable
  layout. Compare sizes in the same coordinate system; a display's physical
  resolution is not its usable logical size at 125 % or 200 % scaling.
- Persist normal restored bounds separately from maximised / full-screen
  state. Record enough monitor / scale context to convert the window API's
  units correctly; do not blindly persist raw pixels or convert twice.
  Revalidate after undocking, resolution / work-area changes and reconnect.
  Keep the title bar and a usable portion of content reachable; allow
  negative coordinates for displays left of / above the primary display.
- Windows `WINDOWPLACEMENT` can use workspace coordinates; do not feed them
  directly to screen-coordinate APIs such as `SetWindowPos`. Process DPI
  changes through the framework or native `WM_DPICHANGED` handling. See
  [placement coordinate rules](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowplacement)
  and [DPI changes](https://learn.microsoft.com/en-us/windows/win32/hidpi/wm-dpichanged).
- Test maximise, minimise, full screen, Windows snap and Linux tiling.
  macOS full-screen windows can occupy a separate Space; window managers
  may override size hints. Do not interpret refusal of a requested size as
  a fatal startup error.
- Standard Wayland `xdg-shell` lets the compositor place top-level windows;
  portable global placement / global-coordinate queries are unavailable.
  Treat positioning and always-on-top as backend-dependent capabilities,
  not startup prerequisites. Popups still need proper parent-relative
  anchors and configure-event handling. See the
  [xdg-shell protocol](https://wayland.app/protocols/xdg-shell).
- Custom title bars need drag / resize hit regions that exclude interactive
  controls, accessible caption buttons and native window-menu behaviour.
  Honour system double-click preferences and caption-button placement;
  macOS does not universally mean double-click-to-maximise. Keep traffic
  lights clear. On Windows preserve snap-layout and keyboard system-menu
  behaviour when replacing native chrome.
- Parent dialogs / popups to the owning window and open them on its monitor;
  keep them reachable after a scale change. Desktop can show software
  keyboards too; touch and pen do not disappear because there is a mouse.
  See [insets and keyboards](layout.md) and [scale changes](display.md).

**Traps.** Saving maximised dimensions as the normal size loses the user's
preferred window. Rejecting negative coordinates moves valid secondary
windows. Repeatedly rounding / rescaling persisted bounds causes drift.
Using pointer pixels directly as logical popup / capture coordinates shifts
controls on mixed-DPI monitors; see [screen capture M8](media-devices.md).

**Verify.** Start at the smallest supported work area, resize across each
breakpoint, snap / maximise / restore, then restart. Move between different
scales, change the taskbar edge / work area, disconnect the saved monitor,
and reopen a modal. Repeat on each supported X11 / native Wayland backend;
check reachability, stable normal bounds, crisp rendering and retained state.

## W2 Close, quit and tray — P1

| Platform | Expected behaviour |
|---|---|
| macOS | Many document / messaging apps remain running after the last window closes; choose deliberately. Cmd+Q and Dock Quit terminate. Reopen from Dock / Finder must show or restore a window; AppKit offers `applicationShouldHandleReopen(_:hasVisibleWindows:)`. |
| Windows | Closing the last primary window normally exits unless the app explicitly offers background / tray operation. Session end uses `WM_QUERYENDSESSION` / `WM_ENDSESSION`; save promptly and respect shutdown. |
| Linux | Last-window / background behaviour is an application choice consistent with the shell. StatusNotifierItem / legacy tray support depends on the desktop and installed extensions; a tray icon is not guaranteed. Keep a visible reopen / quit path when it is absent. |

See [AppKit reopen](https://developer.apple.com/documentation/appkit/nsapplicationdelegate/applicationshouldhandlereopen(_:hasvisiblewindows:))
and [Windows session end](https://learn.microsoft.com/en-us/windows/win32/shutdown/wm-queryendsession).

**Traps.**
- An unsupported tray operation, missing native library or shell restart
  must not abort startup. Handle expected capability / initialization
  errors with diagnostics and disable only the affected integration; do
  not silently swallow every exception and leave a half-initialised app.
- Close-to-tray without a working tray makes the app unreachable. Provide
  an explicit setting and explanation, and disable hiding when there is no
  reliable way back. Starting a second instance should reopen the existing
  window if that is the single-instance policy; see [B5](lifecycle.md).
- Distinguish window close from application quit. A quit request must not
  be intercepted by the close-to-tray handler. Route concurrent quit
  entry points through one shared completion. Separate a cancellable local
  checkpoint from irreversible resource disposal: a save failure may keep
  the session open only while its services are still usable. Once teardown
  starts, join it or reach an explicit terminal / recovery state; do not
  return to an apparently active UI backed by disposed services. A deadline
  on waiting does not itself cancel the work (see [Flutter notes](flutter.md)).
  Bound network-dependent work through actual cancellation / checkpointing,
  keep writer ownership until writers stop (B5), and persist important
  state during use since termination callbacks are not guaranteed.
- Use the platform's appropriate menu-bar / tray artwork; see
  [display.md D5](display.md).

**Verify.** Close the last window, reopen, quit from app menu / Dock / tray,
launch twice and end the OS session with unsaved state. Test tray missing,
initialisation failure and shell restart. Confirm the process exits on quit,
no capture continues and restart recovers saved work. Inject a failed save,
a disposal that completes after the wait deadline, and overlapping quit
requests. Assert one teardown, no late disposal after a cancelled quit,
and no second writer while the original is still shutting down. Native
session-end / forced termination is a separate case from a cancellable
framework exit request (B2, X7).

## W3 File system — P1

**Rule.** Resolve per-user locations with OS / framework directory APIs,
never the executable directory or current working directory. Installation
and mounted application images can be read-only; launch location varies.

| Platform | Persistent data / settings | Cache / logs |
|---|---|---|
| macOS | `FileManager` Application Support / Preferences locations; App Sandbox changes their resolved container paths | Caches / Library logs locations, resolved for the current app |
| Windows | Known Folder APIs: Roaming AppData for genuinely roamable settings; Local AppData for machine-local data | An app-specific local cache / log location; packaged apps may use package-managed application data |
| Linux | `$XDG_DATA_HOME` (default `~/.local/share`), `$XDG_CONFIG_HOME` (default `~/.config`), each with an app subdirectory | `$XDG_CACHE_HOME` (default `~/.cache`); persistent state / logs under `$XDG_STATE_HOME` (default `~/.local/state`) |

Linux XDG variables must contain absolute paths; ignore invalid relative
values and use defaults. Runtime sockets / locks belong in an appropriate
runtime location, often `$XDG_RUNTIME_DIR`, rather than durable synced
settings. Flatpak / Snap change filesystem visibility and app locations;
resolve from inside the packaged app. See the
[XDG specification](https://specifications.freedesktop.org/basedir/0.8/).

**Traps.**
- Join / parse paths with the local path API. Lexical normalisation does
  not establish identity through symlinks, junctions or hard links. Use
  filesystem identity / resolved handles when identity matters; handle a
  missing path and permission errors. Never use a simple string-prefix
  check as a sandbox or archive-extraction boundary (see [M4](media-devices.md)).
- File-system case behaviour belongs to the volume / directory, not just
  the OS. Test case-sensitive and insensitive locations, Unicode names,
  spaces, removable storage and redirected / network home directories.
  Avoid blindly lowercasing filenames or assuming local filesystem latency.
- Windows legacy APIs often have `MAX_PATH` = 260 limits. For affected
  Win32 APIs, extended-path support or both the system long-path setting
  and the app's `longPathAware` manifest opt-in are needed. Shells, plugins
  and dependencies may still impose their own limits. See
  [long-path rules](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation).
  Inspect the actual runtime / dependency path before prescribing a fix:
  a runtime that already supplies extended paths need not use the manifest
  mechanism. When relying on a manifest, inspect the compiled executable's
  embedded resource, not just its source XML. A native API probe must use
  the relevant source, ABI and release configuration; it does not replace
  an installed-app long-path round trip. For a negative control, establish
  that its short parent exists and is accessible, isolate the changed
  opt-in, and reject unrelated permission / missing-parent failures rather
  than accepting any nonzero exit as proof. Record the host policy without
  silently changing it to make a test pass.
- Windows open-file deletion / rename depends on access and share modes;
  it is not universally forbidden. Handles opened without
  `FILE_SHARE_DELETE` can block deletion. Close the app's streams and handle
  sharing / antivirus / sync-client failures without discarding the last
  valid file. Write replacements safely and handle cross-volume moves;
  rename is not a universal cross-volume atomic operation. See
  [DeleteFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew).
- Selected-file grants and persistent access follow
  [P6](permissions.md#p6-selected-files-and-persistent-access--p1); verify
  them under the shipped desktop sandbox.

**Verify.** Use a standard non-administrator account and the installed app.
Open / save / replace in Unicode and long nested paths, read-only and full
volumes, a file held open elsewhere, a removable / network location, and a
sandbox-selected directory after relaunch. Interrupt a write and verify the
last valid document survives. Check uninstall / update data-retention policy.

## W4 Packaging and distribution — P0 for release

**Rule.** Validate the artifact users install on a clean system, separately
for every distribution channel and architecture. A development runner
working on a machine with the SDK installed is insufficient evidence.
Use the [store release guide](stores.md) ([简体中文](stores.zh-CN.md)) to
distinguish Mac App Store / Developer ID, Microsoft Store MSIX / MSI/EXE,
Flathub / Snap and other selected repository paths. Their account, signing,
review and update rules differ.

- Record runner CPU / virtualization, tool-process ABI / emulation, build
  target and package / store architecture separately. Pin SDK / compiler / engine
  revisions and verify target artifacts exist. Missing assets must stop
  that required target, not silently fall back and relabel another build.
  Use cross-compilation only where supported and record it; an ARM64 runner
  or renamed output directory is not evidence of a native ARM64 payload.
- **macOS:** outside the Mac App Store, the standard Developer ID release
  path uses hardened runtime, signing, notarization and a stapled ticket
  where supported by the deliverable. Mac App Store signing / sandboxing is
  a different path and does not require a separate notarization submission.
  Finish bundle mutations (for example native-library copying,
  `install_name_tool`, stripping and privacy-resource generation) before
  final signing. Sign nested code from the inside out, then its containing
  frameworks / helpers and outer app; re-sign affected containers after
  any later mutation. `codesign --deep` is useful for recursive
  **verification**, not the normal signing strategy. Verify the app
  extracted / installed from the final deliverable, not just an earlier
  staging directory. See [Apple TN2206](https://developer.apple.com/library/archive/technotes/tn2206/_index.html)
  and
  [notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution).
- Match functional entitlements across build configurations, but retain
  deliberate differences: debugging entitlements such as `get-task-allow`
  do not belong in a normal distribution build. Test camera, microphone,
  file access and networking with release signing / sandboxing. See
  [declarations](permissions.md).
- macOS universal or per-architecture distribution is a product choice;
  every bundled native library / helper must support the selected CPU and
  minimum OS. `LSMinimumSystemVersion` cannot make a newer native API work
  on an older OS; test actual minimum-system launch and feature use.
- **Apple compatibility surfaces are separate shipping surfaces.** A native
  macOS app, a Mac Catalyst build, an unmodified iPhone / iPad app on Apple
  silicon Macs ("Designed for iPad"), a compatible iPad / iPhone app on
  Apple Vision Pro and a native visionOS app have different runtime,
  hardware and distribution constraints, even where a compatibility
  offering reuses the iOS binary. Record for each one whether it is offered,
  which build is distributed and whether every native plugin supports it.
  - Eligible iPhone / iPad apps reach the Mac App Store on Apple silicon
    Macs and the Apple Vision Pro App Store by default unless availability
    is turned off in App Store Connect (an app-level setting covering all
    versions); apps that have been in the Kids category cannot be offered on
    visionOS. An iOS release can therefore ship to Macs and Vision Pro that
    were never tested.
    See [iPad apps on Mac](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-macs-with-apple-silicon/)
    and [iPad apps on Vision Pro](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-apple-vision-pro).
  - Adding and releasing a macOS platform version under the same App Store
    Connect app record replaces the compatible iOS offering on the Mac App
    Store and updates existing users to it; a visionOS platform version on
    the same record likewise replaces it on Vision Pro. A separate native
    app on its own record does not. Apple documents the update, not
    what happens to local data: test whether local files, keychain items,
    settings, purchases and sign-in survive the switch to the native build,
    and plan a migration or server-side recovery where they do not.
  - Compatible apps on visionOS cannot use the device cameras for ordinary
    photo / video capture, but can capture Persona photos with
    `AVCaptureDevice` at position `.front` and use Continuity Camera. Core
    Motion, barometer / magnetometer data, HealthKit data and all location
    services except the standard one are unavailable; use availability
    checks and fallbacks (M7). See
    [visionOS compatibility](https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos).
  - Detect the environment explicitly: `ProcessInfo.isMacCatalystApp` is
    also true for an iOS app running on Apple silicon; use
    `isiOSAppOnMac` to tell them apart. `isiOSAppOnVision` identifies a
    compatible iOS app on visionOS; build with a 26.1+ SDK and guard the
    query with a runtime availability check when supporting earlier OS
    versions. Use `#if targetEnvironment(macCatalyst)` for
    compile-time Catalyst code. See [`isiOSAppOnMac`](https://developer.apple.com/documentation/foundation/processinfo/isiosapponmac).
  - For Flutter target and plugin support on these surfaces, see
    [flutter.md](flutter.md).
- **Windows:** choose installer / MSIX and per-user / machine scope. Sign
  the release appropriately; signing identifies a publisher but does not
  guarantee absence of SmartScreen warnings. Supply the required Visual C++
  runtime through the chosen supported deployment method when dynamically
  linked. Test architecture-specific dependencies, including Windows on
  ARM, without relying on an unrelated runtime installed by developer tools.
- **Linux:** each `.deb` / `.rpm` / AppImage / Flatpak / Snap has its own
  dependency / confinement model. Set a supported libc / distro baseline;
  building on a newer distribution can introduce unavailable symbols.
  Verify only the actual backend's dependencies (for example GTK, codecs,
  Secret Service or TLS libraries), not a universal dependency list. Check
  native Wayland and X11 / XWayland support actually claimed by the build.
- Register desktop URL schemes / file associations: macOS
  `CFBundleURLTypes` / `CFBundleDocumentTypes`, Windows installer registry /
  package declarations, Linux `.desktop` `MimeType` entries including
  `x-scheme-handler/<scheme>`. Linux desktop file identity / Wayland app ID
  and installed icons must agree for shell grouping. A parser alone does
  not register a handler. Treat incoming URLs / filenames as untrusted data;
  handle cold / warm activation through the app's instance policy (B3 / B5).
- Update through the distribution's mechanism: store-managed, package
  manager or a signed updater appropriate to the channel. Respect install
  permissions; test updates while running, interrupted downloads, native
  helper replacement and migration from previous data formats. Keep user
  data outside the replaceable application bundle. Do not assume every
  AppImage supports AppImageUpdate or every installation allows self-update.

**Verify.** Clean install, first launch, denied privileges, file / URL
activation while closed and running, previous-version update, interrupted
update, minimum supported OS / CPU, and uninstall with no orphan process.
On macOS validate signing and notarization of the distributed artifact; on
Windows verify dependencies and shell registration; on Linux install into
each supported package / sandbox and exercise file portals, tray and media.
For Apple compatibility surfaces, read the App Store Connect availability
settings for Macs and Vision Pro, then run the distributed build (not only
a simulator or Xcode "Designed for iPad" run) on an Apple silicon Mac /
Vision Pro with keyboard, pointer, file import / export and the missing
hardware. Before either same-record replacement (macOS or visionOS),
update a signed-in installation containing local files, credentials,
settings and purchases, and verify continuity or the documented recovery.
For mobile ABI / native-plugin release checks see [flutter.md](flutter.md)
and [testing.md](testing.md), rather than shipping simulator binaries.
