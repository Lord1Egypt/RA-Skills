# Complete checklist catalog

All 65 stable IDs; load for full release coverage or when selecting an unfamiliar
area. Detailed rules and verification recipes remain in the linked area files.

### Layout and screens — [references/layout.md](layout.md)

- **L1 Size range.** Usable at the smallest supported phone / window size
  through a maximised desktop window, including phone landscape, tablet
  panes, resizable iPad windows and foldables. Include narrow stress cases
  such as 320 pt / dp; that is a test width, not a universal OS minimum.
- **L2 Breakpoints by available width.** Layout decisions read the window's
  available size, never the OS or a "device type" guess; every component
  that has its own idea of "mobile vs desktop" agrees with the shell.
- **L3 Breakpoint crossing at runtime.** Rotation, split-screen resize, fold
  / unfold, desktop window resize and moving between displays (including
  Android connected displays and display removal) keep the open screen,
  drafts, selection, scroll position, focus and running media; metrics come
  from the current window's context.
- **L4 Safe areas and system bars.** Nothing important under the notch /
  Dynamic Island / cutout, rounded corners, home indicator, Android
  edge-to-edge status, navigation and caption bars (including side insets
  where present), Android desktop-window caption bars, iPadOS 26 window
  controls in custom toolbars, or macOS full-size-content title bar controls.
- **L5 Soft keyboard.** Inputs and their actions stay visible with the
  keyboard open, in landscape, with supported iPad floating / split
  keyboards; keyboard avoidance is applied exactly once and handles
  keyboards that do not occupy the bottom edge.
- **L6 Orientation.** Declarations match the intended orientations; layouts
  also handle OS-imposed rotation and resizing. Check runtime and target-SDK
  rules for iPad and Android large screens in the layout reference.
- **L7 Overlays.** Dialogs, sheets, menus, snackbars and FABs obey the same
  rules as screens: they scroll, respect safe areas, have a max width on wide
  windows and do not cover content at the end of a list.
- **L8 Fold hinges and posture.** Account for separating folds and occluding
  hinges in window coordinates; posture changes preserve the active flow
  even without a width breakpoint.

### Text, density and assets — [references/display.md](display.md)

- **D1 Large text.** No overflow, clipping, silent fade or ellipsised
  essential text through the supported OS's largest text settings, including
  Android 14+ non-linear scaling up to 200 % and iOS accessibility Dynamic
  Type categories. Labels wrap, rows become columns and containers grow;
  one multiplier cannot represent every text style's scaling curve. Bold
  Text is included.
- **D2 Localised and long text.** Longest shipped language, CJK, RTL; no
  string concatenation that breaks word order; missing translations are
  detected, with any intentional fallback recorded.
- **D3 Pixel density.** Raster assets at every density the platform asks
  for (or vectors); layout uses logical units, with deliberate pixel
  alignment for fine strokes; hairlines and icons stay sharp at supported
  fractional scales such as 125 % / 150 % / 175 %.
- **D4 Scale changes at runtime.** Moving a window between monitors with
  different scale factors, or changing display scaling while running,
  re-lays out and re-rasterises without blur or stale sizes.
- **D5 Platform icons.** App, tray / menu-bar, notification and window icons
  follow the platform's format rules; launch screens follow their separate
  platform requirements.
- **D6 Theme and contrast.** Light / dark follows the system or an explicit
  saved preference, including startup; secondary text meets contrast in
  both; state is never shown by colour alone, including under colour
  filters, greyscale and inversion.
- **D7 Reduced motion.** Follow animation preferences for custom and native
  content; navigation, progress, cancellation and focus still work with
  animations disabled.

### Input and interaction — [references/input.md](input.md)

- **I1 Touch targets.** Use the recommended touch hit areas of at least
  44 × 44 pt (iOS / iPadOS) / 48 × 48 dp (Android), measured rather than
  inferred from padding; check the input reference for context.
- **I2 Pointer and keyboard.** Hover states, right-click / secondary-click
  menus, scroll wheel and trackpad, drag-and-drop, focus traversal, visible
  focus and platform shortcut conventions (including Cmd vs Ctrl) — on
  desktop and on tablets with a keyboard / trackpad, including the iPadOS 26
  menu bar (every command listed, dimmed when unavailable, targeted at the
  active scene).
- **I3 Text input.** Enter-to-send never fires during IME composition;
  hardware-keyboard handling does not race the characters typed before it;
  long-press menus do not fight the system text-selection menu.
- **I4 Back navigation.** Android back / predictive back and supported iOS
  back gestures follow the route stack; desktop Esc follows the platform's
  dismissal conventions. No action pops past the root unexpectedly.
- **I5 Screen readers and assistive input.** Every control has an
  accessible name and role; VoiceOver / TalkBack / Narrator / Orca, Voice
  Control / Voice Access and Switch Control / Switch Access can complete the
  main flows.
- **I6 System formats and time values.** 12 / 24-hour time, locale date and
  number formats, first day of week come from the system setting; instants,
  date-only values and wall-clock schedules in a named zone are stored
  distinctly, with defined DST gap / overlap handling.
- **I7 Gesture alternatives and cancellation.** Essential actions do not
  depend only on complex gestures, pressure, hover or one pointing device;
  cancelled input leaves no accidental activation or stuck state.
- **I8 Verified HTTPS links.** App Links / Universal Links / Windows app URI
  handlers are verified at both ends against the installed release signing
  identity (including Play App Signing); every linked URL keeps a working
  web fallback.
- **I9 Clipboard, sharing and cross-app drag.** Typed representations per
  direction; incoming content is read while its access grant is valid and
  copied before deferred work; native share-target entry points; outgoing
  data stays available until the receiver reads it.

### Lifecycle and background — [references/lifecycle.md](lifecycle.md)

- **B1 Lifecycle states mean different things per platform.** Focus loss,
  visibility, scene activation and background execution are distinct.
  Choose camera, audio, rendering and privacy behaviour per resource and
  platform; do not treat every blur as backgrounding or defer all privacy
  protection until hidden.
- **B2 Persist before suspension.** Checkpoint user data during use and on
  supported lifecycle transitions; recover committed data after background
  process death without relying on a final callback.
- **B3 Process death and cold start.** After the OS reclaims the process the
  app restores the supported state and recovers or safely retries a pending
  system picker / camera operation; a notification tap on cold start is not
  dropped or doubled.
- **B4 Background limits.** Work that must run in background respects iOS
  suspension and background-task budgets, Android foreground-service types
  and time limits, Doze and OEM battery killers; desktop sleep / resume,
  wall-clock jumps and persisted deadlines across sleep / reboot are
  handled.
- **B5 Single instance and multiple windows.** A second launch, an Android
  multi-instance window or an iPad second scene does not contend for the
  same data; ownership is established before stores open, with activation
  queued until the owning window is ready.
- **B6 Durable transfers and retry ownership.** Persist operation ownership
  and reconcile background jobs after restart; retries, cancellation and
  account changes cannot duplicate or misattribute results.
- **B7 Local-data migrations.** Versioned, atomic or resumable upgrades from
  every supported earlier release, including skipped releases; no
  destructive fallback for user data and a safe answer for data written by
  a newer version in either the primary store or backup (downgrade,
  restore), on both reads and writes.
- **B8 Offline state and sync conflicts.** Offline reads / writes are
  documented; local edits carry a durable sync state; edit / edit and
  edit / delete conflicts follow a defined rule based on server versions,
  not device clocks; deletions propagate and accounts stay isolated.

### Permissions, privacy and data — [references/permissions.md](permissions.md)

- **P1 Declarations match use on every platform.** Inspect the declarations
  required by the actual API and distribution model: Android manifest,
  Apple usage strings / entitlements, Windows package capabilities, or Linux
  sandbox permissions / portals. Use localised purpose strings where
  required; remove unused access. Not every capability needs every kind of
  declaration, and unpackaged apps may have no package manifest.
- **P2 Runtime flow.** Ask in context, in the foreground, following the
  platform's request sequence without repeated-prompt loops; explain denial,
  restriction and revocation mid-use, and offer settings recovery where the
  user can change access; the first denial is never silent.
- **P3 Degraded paths.** The feature still works or explains itself when a
  permission is denied (notifications off, limited photo access, approximate
  location).
- **P4 Store privacy requirements.** Applicable Apple privacy manifests,
  required-reason API declarations and privacy labels, Play Data safety,
  sensitive-permission / foreground-service declarations, and submission
  SDK / target-API requirements match the shipped app and bundled SDKs.
- **P5 Data at rest and backup.** Use the OS credential store for secrets;
  on Android protect encrypted secrets with Keystore-backed keys. Decide
  backup inclusion. Handle both retained and missing credentials after
  reinstall; iOS Keychain retention after uninstall is an
  [implementation detail](https://developer.apple.com/forums/thread/36442).
- **P6 Selected files and persistent access.** A picker result is scoped
  access, not a permanent path; copy into app storage or retain the
  supported grant / bookmark before deferred work.
- **P7 Sensitive content and screen capture.** Decide what may appear in
  app-switcher snapshots, screenshots, recordings and mirroring; apply the
  per-platform protection before sensitive content is shown.
- **P8 Purchases and entitlements.** Use each channel's required billing and
  storefront exceptions; grant only verified, completed transactions;
  restore, refund, revoke and expire one server-side entitlement that every
  shipped platform reads.
- **P9 Store feature and audience rules.** Account deletion where triggered
  (Play mobile: in-app and web; non-mobile Play: web), third-party login
  equivalents, user-generated content report / block, current age-rating
  answers, children's SDK and ads rules, and localised store listings —
  checked per store, with a dated policy source.

### Media, audio and devices — [references/media-devices.md](media-devices.md)

- **M1 Audio session and focus.** Playback and recording choose the right
  iOS audio session category and Android audio focus; silent switch,
  interruptions (calls, alarms, other apps) and resumption behave as users
  expect; components sharing one session do not undo each other.
- **M2 Audio routes.** Speaker / earpiece / wired / Bluetooth routes, and
  devices connecting or disconnecting mid-use.
- **M3 Camera.** Front / back switch, mirroring, rotation, release after use
  (verify this app stops capture in OS privacy UI), a clear state when the OS
  takes the camera away (multitasking, background, another app).
- **M4 Formats crossing platforms.** Media and files produced on one
  platform open on the others (HEIC / HEVC to Windows / Linux, path
  separators and case in archives, line endings).
- **M5 Memory.** Decode previews near their rendered physical size
  (logical size × device pixel ratio); reserve full-resolution decoding for
  features that need it; stream large files and handle low storage.
- **M6 Notifications.** Channels, badges, grouping, lock-screen content
  privacy, tap routing, and platform behaviour when notifications are off.
- **M7 Optional hardware and device capabilities.** Detect hardware and
  service availability separately from permissions; absent or disconnected
  devices have a usable fallback and intentional store filtering; ChromeOS,
  Android TV and Android XR reach is decided and tested with each
  category's input.
- **M8 Screen and system-audio capture.** Treat screen, microphone, system
  audio and remote input as separate capabilities; verify consent, capture
  dimensions, interruption and cleanup for each supported backend.

### Desktop specifics — [references/desktop.md](desktop.md)

- **W1 Window management.** Sensible default and minimum size clamped to the
  work area; size / position restored only onto a display that still
  exists; full screen, maximise, snap layouts; Wayland restrictions.
- **W2 Close vs quit vs tray.** Platform-correct semantics for closing the
  last window, quitting (Cmd+Q, taskbar, logout / shutdown), and
  minimising to tray; tray / menu-bar support gaps per desktop environment
  never crash startup; a cancelled quit cannot leave teardown running.
- **W3 File system.** Per-OS app data, cache and documents directories;
  separators, case-insensitive and case-preserving file systems, long paths,
  non-ASCII user names; never write next to the executable.
- **W4 Packaging and distribution.** Apply the signing, notarization,
  installer and update requirements of each distribution channel; register
  file associations and URL schemes per platform. iPad apps on Apple silicon
  Macs and Vision Pro are separate shipping surfaces with their own
  availability, plugin support and data-continuity checks.

### Performance, size and energy — [references/performance.md](performance.md)

- **F1 Frame pacing.** Frame-time and missed-frame budgets are measured
  against the active refresh rate (ProMotion, Android 90 / 120 Hz,
  mixed-refresh desktop monitors), not a fixed 60 Hz; animation is driven by
  timestamps.
- **F2 Size and startup.** Download, installed and installer size, and cold /
  warm start to usable content, are budgeted per release, artifact and
  architecture, and measured on release builds with realistic data.
- **F3 Energy and thermal load.** Idle screens do no unnecessary repeated
  work and hidden work stays within what B4 allows; wake locks and sleep
  inhibitors are released; optional work drops under Low Power Mode,
  battery saver or thermal pressure and recovers without oscillating.

### Process and parity — [references/testing.md](testing.md)

- **X1 Device matrix.** The change was exercised on the profiles in the
  testing reference that it can reach, not only on the developer's machine —
  including surfaces it reaches by default store availability (Android
  connected displays, ChromeOS, XR, iPad apps on Mac / visionOS, web if
  shipped).
- **X2 Automated layout sweep.** Screens and overlays are rendered across
  sizes × text scales × locales × safe-area profiles with detectors for
  overflow, clipping, ellipsis and lost state.
- **X3 Rotation / resize test.** Real-app tests on every affected platform
  rotate or resize through OS controls across a breakpoint in both
  directions and assert state survives.
- **X4 Real-device-only behaviour is labelled.** Items that need hardware
  (headsets, available silent controls, cellular handover, real camera) are
  marked "needs device" with a plan, never reported as verified from a
  simulator.
- **X5 Parity.** A bug fixed on one platform is checked on the others; the
  answer is recorded either way.
- **X6 Packaged release verification.** Inspect and exercise the actual
  release artifacts, declarations, architectures and install / upgrade
  paths, gated by release-build CI for every shipped target plus installed
  smoke tests or documented device-lab evidence; debug-build success does
  not establish release compatibility.
- **X7 Interrupted flows and access changes.** Test recreation, background
  process death, permission revocation and interrupted system UI separately,
  with explicit state and result-delivery assertions.
- **X8 Network environments.** Exercise offline recovery, address-family
  coverage and relevant network changes using a documented network setup;
  a connection indicator is insufficient evidence of service reachability.
- **X9 Production diagnostics.** Release builds on every shipped platform
  report application errors and applicable native crashes with readable
  stacks from archived per-build symbols or source maps; logs are redacted,
  rotated and retained to a documented policy.
