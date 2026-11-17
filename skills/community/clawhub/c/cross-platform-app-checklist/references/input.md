# Input and interaction (I1–I9)

Platform details checked against the linked primary sources on 2026-10-22.
Input capabilities can coexist and change while running: a tablet may have
a keyboard, a desktop may have touch, and a stylus may support hover.

## I1 Touch targets — P1

**Rule.** Use at least 44 × 44 pt hit areas for ordinary iOS / iPadOS touch
controls and 48 × 48 dp for Android touch controls as this checklist's
baseline. These are design recommendations, not a universal store-rejection
threshold. Separate adjacent targets enough to avoid accidental activation;
8 dp can be a starting spacing choice, not a rule for every platform widget.
See [Apple buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
and [Android touch targets](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views).

**Traps.**

- Padding lies outside the gesture detector: a visible 44 pt button has only
  a text-sized hit area. Test the actual hit region, including its edges.
- Invisible hit-area expansion overlaps a neighbour, or an ancestor clips
  it. The nearest visual control must receive the tap predictably.
- A desktop classification selects tiny controls on a touch-capable laptop.
  Keep touch usable when devices coexist; do not permanently choose density
  from the last pointer event.
- A disabled-looking label still intercepts taps, or a transparent overlay
  blocks controls below it. Verify enabled state and hit-test behavior agree.

**Verify.** Tap corners, padding and gaps between adjacent controls at
normal and maximum text size. Check touch and mouse on a hybrid device;
measure accessibility bounds as well as hit-test bounds.

## I2 Pointer and keyboard — P1 on desktop and keyboard-equipped mobile devices

**Rule.** Complete the main flows with keyboard and pointer wherever those
inputs are available. Use control-specific platform conventions rather
than treating every control as a generic clickable container.

| Input | Expected behavior / failure prevented |
|---|---|
| Hover | Indicate interactive state and explain icon-only actions, while keeping every essential action available without hover. Hover capability is not an OS classification. |
| Secondary click | Offer appropriate context actions through right-click / two-finger click and a keyboard or visible-menu path; touch long-press can expose the same actions. |
| Scrolling | Support mouse wheel, high-resolution trackpad deltas, inertia and relevant horizontal scroll. Follow the OS scrollbar visibility setting; always-visible scrollbars are not a universal desktop convention. |
| Keyboard focus | Predictable Tab / Shift-Tab traversal, visible focus and control-appropriate activation (for example Space for a button, arrows within a menu). Keep focus visible when scrolled or covered by an overlay. |
| Shortcuts | Use Command for standard Apple editing / app shortcuts and Control for their Windows / Linux equivalents. Preserve system, assistive-technology and text-editor shortcuts; publish supported commands in menus or shortcut help. |
| Drag and drop | Accept supported types with clear feedback; reject unsupported drops safely and provide a picker / other path. File-access lifetime and sandbox rules belong to [P1](permissions.md) and [W3](desktop.md). |

See [Apple keyboard guidance](https://developer.apple.com/design/human-interface-guidelines/keyboards)
and [Android input compatibility](https://developer.android.com/develop/ui/views/touch-and-input/input-compatibility-on-large-screens).

**Traps.**

- Handling a shortcut in both parent and child submits twice; a global
  handler steals copy, undo or arrows from the focused editor. Scope commands
  to the active window and control, and consume them once.
- Single-letter shortcuts fire while typing or using an IME. Use deliberate
  modifiers / focus scope and preserve the text input path under I3.
- Removing a focused item leaves focus nowhere. Move it to a logical
  neighbour; modal dialogs contain focus and restore it on dismissal.
- Mouse drag-to-scroll prevents selecting text. Provide native scrolling
  and selection behavior unless a deliberate canvas interaction needs dragging.
- iPad Full Keyboard Access exposes focus defects absent in ordinary Tab
  testing. Test it explicitly; keyboard support is not a niche-only tablet
  enhancement. See [Full Keyboard Access](https://developer.apple.com/videos/play/wwdc2021/10120/).
- iPadOS 26 gives every iPad app a menu bar, revealed by moving the pointer
  to the top edge or swiping down, with or without a hardware keyboard.
  Audit toolbar-only and shortcut-only commands for menu coverage. Build it with `UIMainMenuSystem` (iOS / iPadOS 26+); list every
  app command, including those without shortcuts, and show unavailable
  commands dimmed rather than hiding items or whole menus. Storyboard-defined
  menu bars are no longer supported. See [What's new in UIKit](https://developer.apple.com/videos/play/wwdc2025/243/)
  and [iPad app design](https://developer.apple.com/videos/play/wwdc2025/208/).
- A menu command acts on the wrong window or selection. Resolve commands
  through the focused scene / responder chain (for example focus-based
  deferred menu elements) and validate enabled / checked state per responder;
  make destructive key commands non-repeating. Give each scene a distinct
  title, because the Window menu lists open scenes. The menu bar is not always
  present, so every command still needs an in-app path.
- A cross-platform menu abstraction is assumed to reach iPad. Check that
  the framework integration populates the native iPad menu bar; see
  [flutter.md](flutter.md). Window-control clearance in the toolbar belongs to
  [L4](layout.md).
- Native commands can arrive after a route, scene or controller is replaced.
  Validate the current owner at invocation, and reject stale queued requests.
  A late asynchronous result must not overwrite a newer authoritative
  enabled state. Keep one owner for keyboard dispatch when both native
  menus and framework shortcuts exist; opening a menu is not proof that the
  command reaches the live application action exactly once.

**Verify.** Complete sign-in, navigation, editing and one modal flow without
touch. Repeat using trackpad and mouse, with auto-hidden scrollbars, and
connect / disconnect a keyboard while an editor is focused. Test non-US
keyboard layouts, held-key repeat, and simultaneous touch / pointer use. On
iPadOS 26+, reveal the menu bar by touch and by pointer, change focus and
selection, open a second scene where the app supports multiple scenes, and
invoke commands from each window;
check dimmed state and that the target is the active scene.

## I3 Text input — P0

**Rule.** Treat committed text, composition, selection and keyboard commands
as separate parts of the platform text-input protocol. Prefer native /
toolkit editors over reconstructing text from key-down events.

**Traps.**

- Enter confirms a CJK candidate and also sends the message. Respect the
  editor's composition state and commit lifecycle, not only a raw Enter
  event. UIKit exposes `markedTextRange`; Android editors use composing
  spans / `InputConnection`. A soft keyboard, dictation or handwriting may
  commit text without matching hardware-key events. See [UIKit marked text](https://developer.apple.com/documentation/uikit/uitextinput/markedtextrange)
  and [Android composition](https://developer.android.com/reference/android/view/inputmethod/InputConnection).
- A hardware-key handler submits before the editor receives the last text
  update. Submit from the editor's supported action / committed state; an
  arbitrary delay or a second global Enter handler is not a reliable fix.
- Newline / send semantics are imposed as a universal desktop rule. Choose
  them for the field and product, expose an unambiguous send / submit action,
  and document any newline modifier. Preserve multiline input and do not
  submit on held-key repeats.
- Replacing the entire text value on each keystroke resets the composing
  range, selection, undo or native selection toolbar. Apply supported editor
  updates and let system copy / paste / selection coexist with app menus.
- A custom paste hook accepts only the left modifier, fires on key-up too,
  or inserts text alongside the toolkit's default paste action. Test left
  and right Command / Control, key-down and key-up, plain and supported rich
  clipboard content in the real editor. Assert one insertion and preserve
  composition, selection and the normal editor action path.
- Numeric keyboards may lack a sign, decimal separator or Return key.
  Provide reachable actions and validate pasted / hardware-keyboard input;
  keyboard type is a hint, not an input-validation boundary.
- UTF-16 / code-point length is mistaken for user-perceived characters.
  Use appropriate grapheme-aware handling for limits and truncation; keep
  platform selection offsets in the units its API requires. Test combining
  marks and joined emoji, not only ASCII. See [Unicode text segmentation](https://www.unicode.org/reports/tr29/).
- Autofill / password-manager / one-time-code completion is broken by a
  custom field or disabled paste. Supply correct content types / autofill
  hints and preserve secure-entry behavior. Do not log secret field values.
- On iOS 16+, programmatic reads of another app's pasteboard can prompt.
  A custom button calling `UIPasteboard.general.string` is not guaranteed
  prompt-free merely because it follows a tap. Prefer the system paste menu
  or `UIPasteControl` where applicable; do not read the clipboard at launch
  or on every focus change. See [UIPasteControl](https://developer.apple.com/documentation/uikit/uipastecontrol).
  Permission denial handling belongs to [P2–P3](permissions.md).

**Verify.** Use real CJK IMEs to compose, select a candidate, cancel and
submit; repeat with a hardware keyboard and rapid typing. Check dead keys,
accented text, dictation / handwriting where supported, multiline paste,
undo / redo, autofill and paste denial. Assert exactly one complete committed
value is submitted and that an in-progress composition never submits.

## I4 Back navigation — P0

**Rule.** Each platform's back / dismiss input resolves the topmost eligible
surface without duplicate navigation or lost work. Keep one route / modal
policy shared by toolbar buttons, gestures, shortcuts and system callbacks.

**Traps.**

- Android Back pops a route underneath an open keyboard, popup or dialog.
  Let the IME / active surface handle its own dismissal, then navigate.
  Root Back normally leaves the task according to system conventions; a
  forced home-tab detour or double-back-to-exit is a product choice, not an
  Android requirement. See [Android Back principles](https://developer.android.com/guide/navigation/principles).
- For target 36+ on Android 16+, predictive system back animations are
  enabled by default, and legacy `onBackPressed()` / `KEYCODE_BACK` handling
  is unavailable on that default path. Use AndroidX `OnBackPressedCallback`
  / the supported platform API or the framework equivalent. The
  `android:enableOnBackInvokedCallback` manifest flag alone does not migrate
  custom interception. See [Android 16 Back changes](https://developer.android.com/about/versions/16/behavior-changes-16)
  and [predictive Back migration](https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture).
  For Flutter APIs see [the framework reference](flutter.md).
- A predictive / interactive gesture mutates data before it commits. A
  cancelled gesture must restore the same route, draft and focus; avoid
  irreversible work on gesture start.
- A custom iOS navigation shell loses the native interactive pop gesture,
  or assumes every back gesture starts at the physical left edge. Preserve
  current platform navigation behavior and provide a visible back action.
- Desktop Esc first belongs to the active context, such as an IME candidate
  or menu; it must not also close the underlying dialog. Support history
  shortcuts / mouse back where the product has history, not for every pane.
- Always prompting to leave is disruptive; silently discarding a changed
  form is worse. Confirm genuinely destructive abandonment or save a draft,
  consistently across all departure paths. Running background sessions use
  [B1–B4](lifecycle.md), not an unconditional stop-on-back policy.

**Verify.** Exercise toolbar Back, Android button and predictive gestures,
iOS interactive pop, keyboard history / Esc and mouse back where supported.
Cancel a gesture halfway. Repeat with the keyboard, a dialog and an unsaved
draft open, then at the root; assert no double pop or accidental exit.

## I5 Screen readers and assistive input — P1

**Rule.** Expose names, roles, state, actions and sensible reading order
through the platform accessibility tree. Use native semantics where possible;
a visible label or a clickable canvas alone is not an accessible control.
The same tree drives voice and switch input, so main flows must also be
operable with those, not only with a screen reader.

**Traps.**

- Icon-only controls are unnamed, or a wrapper and its child both announce
  the same button. Give each actionable element a meaningful, localised
  name; do not include redundant role words in every name.
- Custom controls expose a name but omit selected / checked / expanded /
  disabled state, range values or available actions. Match semantics to
  behavior; avoid merging distinct child actions into one inaccessible node.
- Informative images have no equivalent description; decorative images
  clutter the reading order. Provide a useful alternative only when needed.
- An overlay leaves its background reachable, moves focus on every rebuild,
  or does not return focus when dismissed. Distinguish keyboard focus from
  screen-reader focus and preserve a logical destination under [L3](layout.md).
- Errors, progress and incoming content update visually but are not announced,
  or announce every frame / keystroke. Use appropriate status / live-region
  mechanisms with restrained updates; keep error text associated with its field.
- A virtualised list removes the focused node, changes item identities or
  auto-scrolls away while being read. Preserve context and accessible scroll /
  item actions; test long lists, not just the first screenful.
- A screen-reader pass is taken as proof for voice and switch input. Voice
  Control (Apple), Voice Access (Android; Windows 11 22H2+) and Switch
  Control / Switch Access drive the same tree differently: users speak a
  visible name or a number overlay, or scan through elements. Keep the
  accessible name consistent with the visible text ("End call" on screen
  must not be named "Leave call"), and supply alternative spoken names where
  useful, such as UIKit's `accessibilityUserInputLabels`. See
  [Apple Voice Control criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/voice-control-evaluation-criteria/)
  and [Windows voice access](https://support.microsoft.com/en-US/accessibility/windows/voice-access/use-voice-to-interact-with-items-on-the-screen).
- Switch scanning visits each child of a large card separately, or a merged
  node hides its distinct actions. Group related elements so scanning is
  efficient, while each action stays individually reachable; each item
  should be highlighted once. Auto-hiding controls and timed toasts with
  actions must stay long enough to reach by scanning or voice.

See [Apple accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility)
and [Android accessible app guidance](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views);
also check [Windows accessibility](https://learn.microsoft.com/en-us/windows/apps/develop/accessibility)
and [Orca's supported accessibility infrastructure](https://gnome.pages.gitlab.gnome.org/orca/help/introduction.html).

**Verify.** Complete the main flows with VoiceOver (iOS / iPadOS / macOS),
TalkBack (Android), Narrator (Windows) and Orca on supported Linux desktop /
toolkit combinations. Include modals, errors, long lists and custom drawing
surfaces. Tree inspection catches missing semantics but does not replace
an actual screen-reader pass; record untested combinations as to do. Then
repeat onboarding, editing, an error and a modal with only Voice Control /
Voice Access ("Show names", "Show numbers", tap by name) and only Switch
Control / Switch Access scanning. Run these interaction passes on physical
devices and record the OS, toolchain and environment; automated audits do
not replace them. See [Apple's
assistive-technology testing guide](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app)
and [Android accessibility testing](https://developer.android.com/guide/topics/ui/accessibility/testing).

## I6 System formats — P1

**Rule.** Format for the user's locale, calendar, time zone and explicit
regional preferences. App language alone does not determine time format,
measurement units or the first day of the week. Store and compute time
values by meaning (instant, date-only, wall-clock schedule in a named zone)
and define how nonexistent and repeated local times resolve.

**Traps.**

- A hard-coded `HH:mm` ignores the chosen 12-hour setting. Android's
  `DateFormat.getTimeFormat(context)` accounts for locale and the user's
  12 / 24-hour preference; `is24HourFormat(context)` exposes the choice.
  See [Android date formatting](https://developer.android.com/reference/android/text/format/DateFormat).
- Apple date / time output is built from manually concatenated fields.
  Use localised styles / templates and the appropriate user preferences;
  cached formatters need refreshing when relevant settings change. See
  [Foundation DateFormatter](https://developer.apple.com/documentation/foundation/dateformatter).
- A calendar assumes Sunday, the Gregorian calendar or the app language's
  region despite a user override. Query calendar / regional preferences;
  test non-Gregorian calendars if the UI supports them.
- Currency is inferred solely from UI locale. Preserve the value's actual
  currency code and localise its presentation. Parse user-entered decimal /
  grouping separators appropriately instead of stripping punctuation.
- An instant, local date and wall-clock appointment are stored as the same
  thing. Never sort by localised display strings or use them as a wire
  format. Store three kinds of value distinctly:

  | Value | Store as | Failure prevented |
  |---|---|---|
  | Instant (message sent, log event) | UTC instant / epoch; render in the viewer's zone | Order and age change with the viewer's zone or DST |
  | Date-only (birthday, due date) | Calendar date without time or zone | Midnight-UTC encoding shows the previous day west of UTC |
  | Wall-clock schedule (09:00 daily alarm, meeting) | Local date / time plus an IANA zone ID (or "floating" local time), recurrence rule | A stored UTC offset is wrong after the next DST change or a zone-rule update |

- "Same time tomorrow" is computed by adding 24 hours. A fixed duration is
  not a calendar day across a DST change; Dart's
  [`DateTime.add`](https://api.dart.dev/dart-core/DateTime/add.html) warns
  that the local time of day can shift. Use calendar arithmetic in the
  intended zone. Dart's `DateTime` is only UTC or the device's local zone, so
  schedules in another named zone need a time-zone database.
- A local time falls in a DST gap (does not exist) or overlap (occurs
  twice). Decide and document the resolution for each: for example shift
  forward through a gap and choose the earlier or later offset in an
  overlap, as [`java.time.ZonedDateTime`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/ZonedDateTime.html)
  does. Do not let recurring notifications fire twice or be skipped silently.
- Stored future schedules are not recomputed when the device zone or zone
  rules change. Recompute occurrences and re-register OS notifications from
  the stored local time and zone. Clock jumps, elapsed-time timers and
  persisted deadlines belong to [B4](lifecycle.md); notification scheduling
  to [M6](media-devices.md).

**Verify.** Change 12 / 24-hour time independently of language, switch region
and first weekday where supported, and exercise decimal commas, negative
values and multiple currencies. Resume after a time-zone / calendar change;
check forms, pickers and already-open views, not just newly formatted labels.
For time values, unit-test a spring gap, an autumn overlap, a zone with a
non-hour offset (for example `Asia/Kathmandu`) and a date-only value viewed
in zones on both sides of UTC; assert recurrence and display results
explicitly.

## I7 Gesture alternatives and cancellation — P1

**Rule.** Keep essential actions usable without a complex gesture, pressure,
hover, haptics or a specific pointing device. Cancelled input must leave no
accidental activation or stuck interaction state.

**Traps.**

- Reordering, swipe actions or pinch-only zoom have no visible / keyboard /
  accessibility alternative. Offer controls such as Move up / down, an
  actions menu or zoom buttons. For web surfaces, WCAG 2.2's [dragging rule](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements)
  requires a single-pointer alternative without dragging, unless excepted;
  keyboard support alone is not that alternative.
- A destructive action commits on pointer-down; dragging away or receiving
  cancellation still activates it. Prefer the native control's release /
  cancellation behavior and undo / confirmation where appropriate. See
  [pointer cancellation](https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation).
- Pointer capture, a press-and-hold timer or a drag remains active after a
  modal, focus loss, resize or cancelled touch. Clear temporary state on
  every supported cancellation path; do not convert cancellation to release.
- Stylus pressure / tilt / hover is assumed to exist on all devices. Detect
  capabilities, preserve ordinary touch / mouse operation, and handle palm
  rejection. On Android, handle `ACTION_CANCEL` and, on API 33+, relevant
  `FLAG_CANCELED` pointer-up events; roll back cancelled strokes. See
  [Android palm rejection](https://developer.android.com/develop/adaptive-apps/cookbook/stylus-palm-rejection).
- Custom drag, swipe, long-press or hover handling may leave actions
  unreachable through Voice Control, Voice Access, Switch Control / Switch
  Access or dwell input. Expose labelled semantic / custom actions under I5 (Apple's Voice Control
  criteria expect swipes, long presses and secondary clicks to be reachable,
  for example through "Show actions"); test speech-only scrolling, zooming
  and hidden controls too.
  Provide visible feedback when haptics are absent or disabled; capability
  and permission declarations belong to [P1–P3](permissions.md).
- Ordinary focused input is implemented using a global hook. Use local
  event / command APIs; review any genuinely required global monitoring or
  automation privileges separately under [permissions](permissions.md).

**Verify.** Complete gesture-based actions using visible controls, keyboard
and the supported assistive input. Start a drag / press, then cancel it by
moving away, switching windows or opening a modal. Test touch plus stylus
with palm contact on hardware, a mouse without hover-dependent actions,
and operation with haptics disabled; record hardware checks under [X4](testing.md).

## I8 Verified HTTPS links — P1 when web links should open the app

**Rule.** When `https` links to your site should open the app, configure the
platform's verified association at both ends: the packaged app declaration
and an association file served on each explicitly declared host (for a
wildcard declaration, at the platform's documented parent-host location).
Check it against the installed release identity, and keep a working web page for every linked
URL, because the app can be absent, unverified or turned off by the user.
Custom URL schemes are not verified; register them under [W4](desktop.md).
In-app routing on cold / warm start belongs to [B3](lifecycle.md).

| Platform | App declaration | Website file | Behavior to know |
|---|---|---|---|
| Android | `VIEW` intent filter with `BROWSABLE` + `DEFAULT`, `http` / `https`, `android:autoVerify="true"` | `https://<host>/.well-known/assetlinks.json`: package name and SHA-256 signing-certificate fingerprints, `application/json`, no redirects | From Android 12 a generic web intent opens the app only if it is approved for that domain; otherwise the default browser opens it. |
| iOS / iPadOS / macOS | Associated Domains entitlement `applinks:<host>` (no path or port; `*.` wildcard for subdomains) | `apple-app-site-association`, no file extension, in `/.well-known/` on each explicitly named host (or the parent host for a wildcard entry), HTTPS, no redirects | Since iOS 14 / macOS 11 devices get the file from an Apple-managed CDN, not from your server. |
| Windows | Packaged app (MSIX or package with external location) with a `windows.appUriHandler` extension and one `uap3:Host` per host | `windows-app-web-link`, no file extension, at the root or `/.well-known/`, listing the package family name | Microsoft documents that links clicked in Chromium Edge, Firefox and similar browsers stay in the browser. Shell launches (`ShellExecuteEx`, `LaunchUriAsync`, Run) open the app. |
| Linux | No verified-website association in the freedesktop desktop-entry / MIME model; `.desktop` files register schemes and MIME handlers | — | Treat `https` links as browser links and do not report parity with mobile. |

Sources: [Android verification](https://developer.android.com/training/app-links/verify-applinks),
[assetlinks.json rules](https://developer.android.com/training/app-links/configure-assetlinks),
[Android 12 web-intent resolution](https://developer.android.com/about/versions/12/web-intent-resolution),
[Apple associated domains](https://developer.apple.com/documentation/xcode/supporting-associated-domains),
[TN3155 debugging universal links](https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links)
and [Windows app URI handlers](https://learn.microsoft.com/en-us/windows/apps/develop/launch/web-to-app-linking).

**Traps.**

- `assetlinks.json` lists only the debug or upload-key fingerprint. With
  Play App Signing, Google re-signs the app, so a local `keytool`
  fingerprint usually does not match users' devices. Copy the app signing
  key certificate's SHA-256 (or the generated snippet) from Play Console, and
  list each other signing identity you test (debug, internal builds). See the
  [App Links FAQ](https://developer.android.com/training/app-links/faq).
- The association file is behind a redirect (apex to `www`, HTTP to HTTPS),
  sign-in, a WAF, geo or user-agent blocking, or has the wrong content type.
  Serve it directly at the host the declaration requires; Apple's CDN must
  reach it from any IP address. Explicit declarations for `www.example.com`
  and `example.com` are different hosts on every platform and each needs
  its own file.
- On Android 11 and lower the app becomes the default handler only if
  **every** host in its manifest verifies, so one broken host disables all
  of them.
- File changes appear to have no effect. Android 14 and lower do not
  re-verify periodically, so website changes are normally picked up on
  install / update (or a manual re-verify); Android 15+ also re-verifies in
  the background, which can take up to seven days. Apple devices check the CDN about once a week, and
  the CDN cannot be invalidated on request. Reinstall to test, and use Apple's
  `?mode=developer` alternate mode only for development builds against hosts
  the CDN cannot reach.
- The test bypasses link resolution. Typing a URL into Safari's address bar
  never opens the app, a link to the domain you are already browsing stays
  in the browser, and third-party browsers may not support universal links.
  On Android, `adb shell am start` with an explicit package or component
  skips domain verification. Tap a real link from another app instead.
- A sideloaded Windows package gets validated links on install even without
  a hosted file, so a local pass does not prove the website file works.
- Users can turn links off: Android's per-domain "Open supported links",
  the Apple choice made from a link's long-press / Control-click menu,
  Windows Settings > Apps > Apps for websites. Redirect tricks to force the
  app are not a fix; the web fallback must work.
- Link paths and query parameters are untrusted input. Validate them before
  routing, and exclude paths the app cannot handle (`excludePaths`, AASA
  exclusions, narrower intent filters) instead of opening a dead screen.

**Verify.** Install a release-signed build (Play internal test track,
TestFlight / App Store, signed MSIX) on a clean device. Android 12+:
reset with `adb shell pm set-app-links --package <package> 0 all`, run
`adb shell pm verify-app-links --re-verify <package>`, wait a few minutes,
then check that `adb shell pm get-app-links <package>` shows `verified`
for each host. Apple: on a Mac run `sudo swcutil dl -d <host>` and
`sudo swcutil verify -d <host> -j <aasa-json> -u <URL>`; on iOS enable
Developer Mode and use the Universal Links diagnostics under Settings >
Developer. Windows: run
`AppHostRegistrationVerifier.exe <host> <package family name> <file>`.
Then on each platform tap links from another app for a matched path, an
excluded path, each host, cold and warm start, with links turned off by the
user, and with the app not installed.

## I9 Clipboard, sharing and cross-app drag — P1 when content moves between apps

**Rule.** For each platform, decide which directions the app supports (copy
out / paste in, share out / share target in, drag out / drop in) and which
typed representations it sends and accepts (MIME type, UTType, clipboard
format). Offer the richest supported representation plus a plain fallback;
read incoming content asynchronously while its access grant is still valid,
and copy it into app storage before deferred work. Text-field paste and
clipboard-read prompts belong to I3; drop feedback and a picker
alternative to I2; retained file access to [P6](permissions.md).

**Traps.**

- Android shares a file path or `file://` URI. Share a `FileProvider`
  `content://` URI with `FLAG_GRANT_READ_URI_PERMISSION` on the intent;
  that grant expires when the receiver's task finishes. Avoid
  `Context.grantUriPermission()`, whose grant lasts until explicitly
  revoked or the device reboots. See
  [Android secure file sharing](https://developer.android.com/training/secure-file-sharing/share-file).
- Android drag and drop between apps does nothing. The source must set
  `DRAG_FLAG_GLOBAL` and `DRAG_FLAG_GLOBAL_URI_READ` / `_WRITE`; the target
  calls `requestDragAndDropPermissions()` before reading, and the grant ends
  on `release()` or when the activity is destroyed, so a rotation or
  deferred job can lose access. When forwarding to another Activity,
  forward the clip data and the Intent grant flags; copy files into
  app-owned storage before enqueueing deferred work, because a URI string
  passed to WorkManager does not keep its grant. See [Android multi-window drag and drop](https://developer.android.com/develop/ui/views/touch-and-input/drag-drop/multi-window).
- Paste, keyboard image insertion and drop take separate code paths and
  accept different types. On Android use `OnReceiveContentListener`
  (AndroidX Core 1.7+ / AppCompat 1.4+) with declared MIME types, keep the
  payload referenced during immediate processing, and finish copying
  incoming files before releasing access or scheduling deferred work. See [Android rich content](https://developer.android.com/develop/ui/views/receive-rich-content).
- An Apple item provider's file is read after the callback returns.
  `NSItemProvider.loadFileRepresentation` writes a temporary copy that the
  system deletes when the completion handler returns; stage it inside the
  handler before deferred processing ([P6](permissions.md#p6-selected-files-and-persistent-access--p1)).
  Loading can be slow (for example cloud-backed items), so show
  progress and support cancellation. See [`loadFileRepresentation`](https://developer.apple.com/documentation/foundation/nsitemprovider/loadfilerepresentation%28fortypeidentifier%3Acompletionhandler%3A%29).
- Copied secrets leak. On Android 13+ mark sensitive clips with
  `ClipDescription.EXTRA_IS_SENSITIVE` (required of all apps whatever their
  target) so the system preview hides them, and skip the app's own "Copied"
  toast there, because the system already confirms the copy. With
  `UIPasteboard`, write secrets with the `localOnly` and `expirationDate`
  options to keep them off other devices and clear them later; native macOS
  apps using `NSPasteboard` call
  `prepareForNewContents(with: .currentHostOnly)` before writing content
  that must stay on this Mac. See [Android copy and paste](https://developer.android.com/develop/ui/views/touch-and-input/copy-paste)
  and [`UIPasteboard` local-only option](https://developer.apple.com/documentation/uikit/uipasteboard/optionskey/localonly).
- The app is missing from the system share sheet. Receiving needs a native
  entry point: Android `ACTION_SEND` / `ACTION_SEND_MULTIPLE` intent filters,
  an Apple Share Extension, or on Windows a `windows.shareTarget` declaration,
  which needs package identity. Declare only the types the app handles
  (Windows warns against `SupportsAnyFileType` outside file-mover apps).
  Windows desktop share sources use `IDataTransferManagerInterop` per window.
  See [Windows share target](https://learn.microsoft.com/en-us/windows/apps/develop/windows-integration/integrate-sharesheet-receive)
  and [Windows share source](https://learn.microsoft.com/en-us/windows/apps/develop/windows-integration/integrate-sharesheet-send).
- A sandboxed Linux app (for example Flatpak) receives a file path it
  cannot open. File drag / copy between sandboxed apps goes through the
  [FileTransfer portal](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.FileTransfer.html)
  (`application/vnd.portal.filetransfer`); by default the session closes
  after the first `RetrieveFiles()` call.
- Incoming content is trusted. Sanitise dropped or pasted HTML / rich text,
  do not trust a declared MIME type, file name or extension, strip path
  components from names, and cap item counts and sizes before decoding.
- Outgoing content is produced lazily (promised files, a provider callback)
  and the source state is gone when the receiver asks. Keep it producible
  until the transfer completes or is cancelled, or provide the data eagerly.

**Verify.** Per platform and direction, exchange plain text, rich text, an
image and several files with a system app and a third-party app. Include a
cloud-backed item, cancellation mid-load, an unsupported type, a large
file, a read after the source app is backgrounded, a rotation / window
recreation during a drop, and a sensitive copy. Check that the received
content is complete and that no access errors appear after deferred
processing.
