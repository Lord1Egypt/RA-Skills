# Media, audio and devices (M1–M8)

Use [permissions.md](permissions.md) for capability declarations and denial
flows, and [lifecycle.md](lifecycle.md) for background execution. A permission
grant does not prove hardware, a route or an encoder exists.

## M1 Audio session and focus — P0 for apps that play or record

**iOS / iPadOS (`AVAudioSession`)**
- Pick the category by intent: `ambient` mixes and obeys the Silent switch;
  `soloAmbient` is the default, interrupts other nonmixable audio and obeys
  the switch; `playback` continues in silent mode. Background playback also
  needs the `audio` value in `UIBackgroundModes` for a legitimate audio use.
  Use `playAndRecord` for simultaneous input and output. Choose
  `mixWithOthers` / `duckOthers` deliberately.
- `voiceChat` configures voice-oriented routing and equalisation; the mode
  alone does **not** supply echo cancellation. Use a voice-processing I/O
  path, such as Audio Unit Voice I/O or
  `AVAudioEngine` with `setVoiceProcessingEnabled(_:)`, and test speakerphone
  echo with the actual call engine. See Apple's
  [category guidance](https://developer.apple.com/documentation/avfaudio/avaudiosession)
  and [voiceChat requirements](https://developer.apple.com/documentation/avfaudio/avaudiosession/mode-swift.struct/voicechat).
- **The session is shared within the app.** Players, recorders and call
  engines can overwrite each other's configuration. Give one coordinator
  ownership of category, activation and restoration; serialise start / stop
  and avoid deactivating while another component still needs audio.
- Handle interruptions, route changes and media-services resets. In the
  interruption-notification API, `shouldResume` is a hint at interruption
  end, not an instruction to restart audio the user paused. Newer SDKs also
  expose resumption APIs; availability-check them against the supported OS
  rather than replacing the older path unconditionally. See Apple's
  [resumption guidance](https://developer.apple.com/documentation/avfaudio/avaudiosession/interruptionoptions/shouldresume).

**Android**
- Use `AudioAttributes` with the appropriate usage / content type and, on
  API 26+, `AudioFocusRequest`. Check the request result before playback;
  handle denied / delayed focus as well as loss, transient loss and ducking.
  Abandon focus when the session ends. On older supported APIs use the
  compatible focus API.
- On Android 15+ for apps targeting API 35+, a focus request requires the
  app to be the top app or running a foreground service; otherwise it
  returns `AUDIOFOCUS_REQUEST_FAILED`. A service must also satisfy its own
  start restrictions and type requirements; a screen wakelock grants none
  of these privileges. See [audio focus](https://developer.android.com/media/optimize/audio-focus)
  and [background limits](lifecycle.md).
- Calls use `MODE_IN_COMMUNICATION`, not the telephony-only `MODE_IN_CALL`.
  Restore audio mode at call end and check hardware volume-key behaviour.
  Notification sounds follow channel / ringer / Do Not Disturb policy;
  playing an alert through a media stream is not equivalent (M6).

**Desktop.** Observe device removal and default-device changes; explicitly
selected output and input may differ. Reopen or reroute streams according
to the backend's behaviour instead of assuming an active stream migrates.
Linux audio-server and codec dependencies depend on the shipped backend.

**Trap.** Keeping the screen awake for all audio drains the battery and
breaks screen-off listening. Request display wakefulness only for a visible
video or another session that needs it; release on exit / error. Background
audio and CPU wakefulness are separate platform concerns.

**Verify.** On devices: silent / vibrate, another app playing, focus denied,
call / assistant interruption, user pause during interruption, screen lock,
background / return, and player → recording → player. Assert correct
resumption, mode restoration and no leaked screen-on request.

## M2 Audio routes — P0 for calls

**Rule.** Discover available input / output routes; do not assume a phone
earpiece or a Bluetooth microphone exists. Choose a sensible initial call
route and expose the actual selected route, not just the last button tapped.

- Test speaker, earpiece where present, wired / USB audio, Bluetooth HFP,
  A2DP, LE Audio and hearing aids where supported. A2DP playback support
  does not establish a bidirectional call route. Opening a headset's
  microphone can change latency, sample rate, channel count and quality.
- Android API 31+: select from `getAvailableCommunicationDevices()` with
  `setCommunicationDevice()`. Check its Boolean result, observe device /
  communication-route changes and call `clearCommunicationDevice()` at call
  end. Do not maintain a separate hard-coded list of Bluetooth profiles.
  This replaces legacy SCO / speakerphone routing APIs; retain a
  version-gated fallback only for older supported Android releases. See
  [AudioManager](https://developer.android.com/reference/android/media/AudioManager)
  and [LE Audio routing](https://developer.android.com/develop/connectivity/bluetooth/ble-audio/overview).
- Bluetooth enumeration / connection APIs may need additional permissions;
  check the exact API and target SDK in [permissions.md](permissions.md).
  Do not request scanning permission merely to play to a system-selected
  headset.
- On Apple platforms, route changes can alter the audio format; re-query
  the session / engine. Pause private media on headphone disconnection
  rather than unexpectedly broadcasting through the speaker. See
  [route-disconnect behaviour](https://developer.apple.com/documentation/avfaudio/avaudiosession/setprefersinterruptiononroutedisconnect(_:)).
- Proximity blanking is useful only on a supported handheld voice route.
  Enable it conditionally and release it on route change / call end; a
  tablet, desktop or headset call must not be left with a black screen.

**Verify.** Needs physical devices: connect / remove each supported headset
mid-call, change the default route, deny relevant Bluetooth access, then
start another call. Check both microphone and output, UI selection,
speakerphone echo, volume keys and proximity cleanup. Simulated audio is
insufficient evidence for Bluetooth profile or proximity behaviour.

## M3 Camera — P0 for apps that use it

**Rule.** Enumerate cameras and their supported formats; handle zero, one,
several and hot-plugged devices. Camera permission, device discovery and
successful capture are separate states.

- Compatible UVC cameras can be discovered on USB-C iPads with iPadOS 17+;
  Android external-camera support depends on device implementation and the
  capture backend. Desktop plugins may also expose only a subset of OS
  devices. Never assume every USB camera appears. See Apple's
  [external-camera guidance](https://developer.apple.com/videos/play/wwdc2023/10106/)
  and Android's [camera feature declarations](https://developer.android.com/guide/topics/manifest/uses-feature-element).
- Android's `CAMERA` permission can imply required back-camera and
  autofocus features for Play filtering. Explicitly mark optional camera,
  autofocus and flash features `android:required="false"`; use
  `android.hardware.camera.any` when a required camera can face either way.
  See [front-only / Chromebook support](https://developer.android.com/develop/adaptive-apps/cookbook/chromebook-camera).
- Keep preview transform, sensor orientation, output orientation metadata
  and mirroring separate. A mirrored front-camera preview is common; make
  saved / transmitted mirroring deliberate, especially for text and QR
  codes. Rotation / window resize does not necessarily rotate the sensor.
  Check crop / letterbox transforms used to map a scan or focus point back
  to the captured frame.
- Release capture resources on actual session end and on unsupported
  background capture. Observe interruption and runtime errors; show a paused
  state, inform the remote side, and recover only when capture is available
  and the user still wants it. Contention, privacy switches, restrictions,
  thermal pressure and unplugged devices must not leave a frozen preview.
- For iPad multitasking, query
  `AVCaptureSession.isMultitaskingCameraAccessSupported` before enabling
  `isMultitaskingCameraAccessEnabled`. Support can come from eligible iPad
  configurations, eligible VoIP configuration or the
  `com.apple.developer.avfoundation.multitasking-camera-access` entitlement;
  that entitlement is **not** universally required. Support can change at
  runtime. Do not add `voip` solely to obtain camera access. Follow the
  [current support conditions](https://developer.apple.com/documentation/avfoundation/avcapturesession/ismultitaskingcameraaccesssupported)
  and the actual plugin's lifecycle contract, not a blanket focus rule.

**Verify.** Real camera: both front / back when available, front-only and
no-camera configurations, USB attach / detach, portrait / both landscapes,
tablet window resize, denied / revoked access, interruption and recovery.
Check recorded / received output, not just preview. On exit confirm capture
stops in backend diagnostics and privacy indicators clear when no other
session is using the resource.

## M4 Formats crossing platforms — P1

**Rule.** Negotiate / validate actual content and decoder support. Apple
devices and photo libraries can supply HEIF / HEIC and HEVC, but not every
capture uses them. Windows / Linux installations and app backends vary in
codec availability. A file extension is not a capability test. See
[Apple's format guidance](https://support.apple.com/en-us/116944).

- Offer a compatible export such as JPEG / H.264 when needed, including an
  audio codec and container the receiver supports. Check HDR / wide-gamut
  conversion, alpha, EXIF orientation and metadata policy; changing the
  extension or MIME type does not transcode content.
- Picked content may be cloud-backed, temporary, a content URI or a
  security-scoped resource rather than a durable filesystem path. Stream /
  copy it while access is valid, or retain access through the platform API;
  show download, cancellation and offline failures. See
  [file access](desktop.md#w3-file-system--p1) and [permission flows](permissions.md).
- Use the archive / protocol's defined separator (for example `/` in ZIP),
  not the producing OS separator. Reject traversal and absolute entries;
  detect case / normalisation collisions before extracting or syncing.
- Common macOS and Windows volumes are case-insensitive; either OS can also
  encounter case-sensitive volumes. Preserve names rather than lowercasing
  every path. Windows reserved characters, device names and trailing dots /
  spaces need a reversible mapping or an explicit conflict, not silent loss.
- Text exports: choose encoding and line endings deliberately. UTF-8 with a
  BOM can help some spreadsheet importers; it is not a universal CSV rule.

**Verify.** Round-trip fixtures between all shipping platforms: HEIC, HDR
video, rotated JPEG, unsupported codec, cloud-only item, interrupted import,
non-ASCII names, case collisions and platform-illegal names. Assert either
correct rendering / restore or an actionable unsupported-content result.

## M5 Memory and storage — P1

**Rule.** Decode previews near rendered logical size × device pixel ratio;
reserve full-resolution buffers for operations that need them. Stream large
files and bound concurrent decodes / transcodes. A 12-million
pixel image takes about 48 MB for an 8-bit four-channel pixel buffer alone;
compressed file size does not predict peak memory. HDR buffers, copies and
GPU textures can cost more. See [bitmap memory](https://developer.android.com/topic/performance/graphics/load-bitmap).

**Traps.** A cache limit does not bound images still retained by views,
animated-image frames or native video buffers. Several thumbnail requests
can decode full originals at once. A free-space precheck races other
writers; handle write failure as well, preserve the last valid file and
clean up partial output. Cache / temporary directories are reclaimable.

**Verify.** Profile peak memory on a lower-memory supported phone while
scrolling a photo grid, opening a large image and sending a video. Repeat
open / close and cancel cycles. Exercise low disk space during write,
partial download cleanup and recovery after process termination.

## M6 Notifications — P0 if used

- Android API 26+: channels need localised names. Re-register to update name
  / description on locale change; after creation, behavioural settings such
  as sound and importance are generally user-controlled. Do not churn
  channel IDs to bypass a user's mute; a genuinely new category may need a
  new channel. Check both app-level and channel-level blocking. See
  [channel rules](https://developer.android.com/develop/ui/views/notifications/channels).
- Android API 33+ notification permission, exact alarms and full-screen
  intents have distinct requirements; see [permissions.md](permissions.md)
  and [background limits](lifecycle.md). A running foreground service does
  not guarantee a notification-drawer entry when notification access is
  denied; media-session and eligible self-managed-call exemptions are
  specific, not a general exemption for chat / call apps. See
  [notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission).
- Use the right small icon and separate badge / grouping / thread support
  from guaranteed numeric counts; launchers and desktop shells differ.
  See [display.md D5](display.md).
- Offer lock-screen content privacy. On Apple platforms inspect alert,
  sound and badge settings separately; authorization does not guarantee an
  immediate banner (Focus and presentation settings still apply). Decide
  foreground presentation explicitly. See
  [notification authorization](https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications).
- Route taps and actions on cold / warm start, buffer until navigation is
  ready, deduplicate delivery, and re-check current account / item access.
  Cancel stale scheduled or delivered notifications when content is read,
  superseded or the user signs out. Already scheduled payloads may be posted
  by the OS without another app callback; cancel / replace them proactively.
- Windows setup depends on the notification API: legacy desktop toast
  routes can require an AUMID and Start-menu shortcut, while Windows App
  SDK `AppNotificationManager.Register()` supports unpackaged registration.
  Test the actual installed distribution and activation path. See
  [registration requirements](https://learn.microsoft.com/windows/windows-app-sdk/api/winrt/microsoft.windows.appnotifications.appnotificationmanager.register).
- Linux: query server capabilities before relying on actions / markup, and
  keep an in-app path when notifications are unavailable. See the
  [Desktop Notifications specification](https://specifications.freedesktop.org/notification/latest-single/).

**Verify.** Fresh install grant / denial, channel muted, quiet / Focus mode,
locked screen, grouped updates, action / tap after process exit, account
switch and sign-out. Scheduled reminders need reboot, time-zone / clock
change and cancellation tests. Verify the installed release on each desktop.

## M7 Optional hardware and device capabilities — P1 (P0 if core)

**Rule.** Feature-detect hardware and service availability independently of
OS and permission status. A tablet or desktop may lack an earpiece, flash,
GPS, NFC, cellular service, proximity sensor or haptics; a phone can lack
individual sensors too. Never infer natural sensor orientation from
"portrait phone"; transform sensor coordinates for current display / camera
use. See [Android sensor coordinates](https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview).

**Traps.** Optional Android `<uses-feature>` declarations default to
required unless specified otherwise, and some permissions imply hardware
requirements. Audit the merged manifest's camera, microphone, telephony,
Bluetooth and sensor requirements against the actual core function. Runtime
permission is not a substitute for `PackageManager.hasSystemFeature()` /
sensor enumeration. Do not advertise torch / zoom / vibration or an NFC
operation until the backend reports support. See
[feature filtering](https://developer.android.com/guide/topics/manifest/uses-feature-element).

**Other Android device categories.** The same APK / bundle can reach
categories the team never tested. Decide per category whether it is
supported, record actual Play availability, and meet that category's
input expectations; a wide phone layout is not acceptance evidence.

| Category | Reach | Input and capability expectations |
|---|---|---|
| ChromeOS | Android apps are offered through Play; declare `android.hardware.touchscreen` `required="false"` when touch is not core, because some Chromebooks have no touchscreen | Full keyboard, mouse and trackpad support; declare `android.hardware.type.pc` with `required="false"` to disable mouse / touchpad input compatibility behaviour while keeping phone availability (without it, distribution can be limited to Chromebooks). Android runs in a container: IPv4 traffic passes through NAT while IPv6 unicast is routed; inbound connections are generally blocked and multicast / broadcast is not forwarded, but mDNS is forwarded, so use network service discovery and test LAN discovery separately. Custom IMEs, widgets, live wallpapers and launchers cannot be installed. See [ChromeOS](https://developer.android.com/develop/devices/chromeos/learn) and its [manifest compatibility](https://developer.android.com/develop/devices/chromeos/learn/manifest) |
| Android TV | Only treated and reviewed as a TV app with an `ACTION_MAIN` / `CATEGORY_LEANBACK_LAUNCHER` activity, touchscreen and other TV-unavailable hardware declared not required, and a localized 320 × 180 px banner supplied as an xhdpi resource | Everything navigable with a five-way D-pad (or standard game-controller keys if a controller is required and declared); no dependence on a Menu button; Back from the main screen returns home. See [TV app quality](https://developer.android.com/docs/quality-guidelines/tv-app-quality) |
| Android XR | Existing mobile-track apps are automatically discoverable on XR headsets / wired glasses unless they require an unsupported feature (for example telephony and several camera features); restrict devices in Play Console if needed. A dedicated XR track requires `android.software.xr.api.spatial` or `android.software.xr.api.openxr` | Compatible 2D apps must complete core flows with XR input: larger targets, virtual and external keyboards, game controllers. Query orientation instead of assuming portrait (many XR devices are naturally landscape); where a front-facing camera is available, handle its virtual avatar view and possible horizontal mirroring. See [XR readiness](https://developer.android.com/develop/xr/check-mobile-app-readiness) and [XR distribution](https://developer.android.com/develop/xr/package-and-distribute) |

Apple compatibility surfaces (iPad apps on Apple silicon Macs and on
visionOS) are covered in [W4](desktop.md); the device matrix in
[X1](testing.md).

**Verify.** Run a core flow with absent hardware, disabled system services,
permission denied and device removed mid-use. Check store device filtering,
fallback controls and explanation text. Hardware-dependent outcomes require
a physical device; emulated sensors do not prove real sensor / NFC behaviour.
For each Android category the app can reach, check the Play Console device
catalog, then complete the core flows with that category's normal input
only: keyboard and mouse on ChromeOS (and LAN discovery separately from
internet access), D-pad on TV, XR input on an XR device or emulator.

## M8 Screen and system-audio capture — P0 if used

**Rule.** Screen capture, microphone capture, system-audio capture and remote
input are separate capabilities. Probe the selected OS API / backend; do
not promise all of them because the app can capture its own view.

- Android: request MediaProjection consent for each session. For target
  API 34+ declare `FOREGROUND_SERVICE`,
  `FOREGROUND_SERVICE_MEDIA_PROJECTION` and service type `mediaProjection`;
  obtain consent before starting the service / projection. On Android 14+
  do not reuse a consent intent or call `createVirtualDisplay()` twice on
  one projection. Register `MediaProjection.Callback` and release surfaces
  / displays on `onStop()`. Resize capture output when the shared region
  changes. See [MediaProjection](https://developer.android.com/media/grow/media-projection).
- Apple: use ScreenCaptureKit where available for the chosen deployment
  targets; retain a ReplayKit path where required by older mobile releases.
  Check API availability, the selected SDK's usage descriptions and
  background configuration instead of assuming the two integrations have
  the same declarations. Handle chooser cancellation and recording access
  denied / revoked. See [ScreenCaptureKit](https://developer.apple.com/documentation/screencapturekit)
  and [ReplayKit](https://developer.apple.com/documentation/replaykit).
- Windows: use a supported capture API, check capture support and honour the
  system's selection / recording indicators. Borderless capture has separate
  consent / capability requirements; do not disable the indicator merely as
  a cosmetic preference. See
  [capture-border requirements](https://learn.microsoft.com/en-us/uwp/api/windows.graphics.capture.graphicscapturesession.isborderrequired).
- Linux / Wayland: use a supported portal / PipeWire integration rather
  than X11 screen-scraping assumptions. Query available source types; handle
  missing portal backends, cancellation and the portal closing a session.
  Persistence tokens are backend / version dependent, not permanent
  permission. See [ScreenCast](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html).

**Verify.** Share one window and a display, cancel the chooser, revoke /
stop from system UI, lock the device, unplug a shared monitor, resize /
rotate and switch scale factors. Check captured dimensions, pointer mapping,
audio routing, protected-content behaviour and that capture really stops.
