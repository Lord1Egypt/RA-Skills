# Permissions, privacy and data (P1–P9)

## P1 Declarations match use on every platform — P0

**Rule.** Map each operation to its actual API, OS / target SDK and package
model. Add only the declarations that path needs on each shipped platform;
using a system picker often avoids broad resource access. Remove unused
permissions and background modes, including entries merged by dependencies.

Android names below omit the `android.permission.` prefix. Consent and
availability checks still apply when no declaration is needed.

| Capability | Android (manifest / API path) | iOS / iPadOS (Info.plist unless noted) |
|---|---|---|
| Internet | `INTERNET`; `ACCESS_NETWORK_STATE` only when inspecting connectivity | No generic Internet permission; transport-security rules still apply |
| LAN / discovery | `INTERNET`; Wi-Fi / LAN rules below | `NSLocalNetworkUsageDescription`; `NSBonjourServices` for applicable Bonjour browsing / registration; multicast entitlement when required |
| Direct camera | `CAMERA`; optional hardware features below | `NSCameraUsageDescription`; recording audio also needs microphone access |
| Microphone | `RECORD_AUDIO`; make `android.hardware.microphone` optional if nonessential | `NSMicrophoneUsageDescription` |
| Photos / media | Prefer Photo Picker. Broad reads of other apps' media: API 33+ / target 33+ `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_MEDIA_AUDIO` as needed; older paths may need `READ_EXTERNAL_STORAGE`. API 34+ selected-access handling below | Prefer `PHPickerViewController` / `PhotosPicker`. Direct library read / write: `NSPhotoLibraryUsageDescription`; add-only authorization: `NSPhotoLibraryAddUsageDescription` |
| User-selected documents | Storage Access Framework, without broad storage permission; retain grants for later use (P6) | Document picker, without broad document-library permission; security-scoped access as applicable (P6) |
| Location | `ACCESS_COARSE_LOCATION`; request `ACCESS_FINE_LOCATION` with coarse when precise access is needed on Android 12+. API 29+ background location: `ACCESS_BACKGROUND_LOCATION`, separately staged | `NSLocationWhenInUseUsageDescription`; Always requests also need `NSLocationAlwaysAndWhenInUseUsageDescription`. Continuous background updates need the appropriate location background configuration; Always and background execution are separate decisions |
| Notifications | API 33+: `POST_NOTIFICATIONS` runtime permission for nonexempt notifications. Full-screen intents: `USE_FULL_SCREEN_INTENT` with eligibility / special-access checks | UserNotifications authorization for alerts / sounds / badges; remote notification registration also needs the Push Notifications capability (`aps-environment` entitlement), not a usage string |
| Bluetooth | API 31+ / target 31+: request only needed `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, `BLUETOOTH_ADVERTISE`; legacy permissions for older OS paths | Core Bluetooth: `NSBluetoothAlwaysUsageDescription`; legacy deployment paths may also require `NSBluetoothPeripheralUsageDescription` |
| Contacts | `READ_CONTACTS`; `WRITE_CONTACTS` only for writes; prefer a supported system selection flow for one contact | `NSContactsUsageDescription` for contact-store access; handle limited authorization on iOS 18+ |
| Calendars | `READ_CALENDAR` / `WRITE_CALENDAR` for provider access; delegating event creation to a calendar app can avoid them | iOS 17+: `NSCalendarsFullAccessUsageDescription` or `NSCalendarsWriteOnlyAccessUsageDescription` with the matching EventKit API; retain `NSCalendarsUsageDescription` for older supported OSs. An iOS 17+ `EKEventEditViewController` creation flow can avoid requesting calendar access |
| Motion / steps | API 29+: `ACTIVITY_RECOGNITION` for step counter / detector and protected activity recognition; don't request it for every accelerometer use | `NSMotionUsageDescription` for protected Core Motion APIs, including pedometer / motion activity |
| Biometrics | `USE_BIOMETRIC`; check authenticator availability / enrollment | `NSFaceIDUsageDescription` for Face ID; check `LAContext.canEvaluatePolicy` and support cancellation / fallback |
| Vibration | `VIBRATE`; hardware / settings can still suppress it | No general usage string; capability varies by hardware |
| Background work | Actual service type and permissions, not blanket `WAKE_LOCK` / `RECEIVE_BOOT_COMPLETED`; inspect scheduler dependency declarations | Only the applicable `UIBackgroundModes` and scheduler identifiers; see [lifecycle.md, B4](lifecycle.md#b4-background-limits--p0) |

Desktop requirements depend on the distribution and security model:

| Capability | macOS | Windows | Linux |
|---|---|---|---|
| Network / LAN | App Sandbox `com.apple.security.network.client` / `com.apple.security.network.server` as needed; macOS 15+ LAN privacy also needs `NSLocalNetworkUsageDescription` and applicable `NSBonjourServices` | AppContainer: `internetClient` / `internetClientServer` / `privateNetworkClientServer` as appropriate; desktop firewall policy is separate and may block without a prompt | Flatpak `--share=network` for direct network use; other packages have their own policy |
| Camera | `NSCameraUsageDescription` + `com.apple.security.device.camera` for sandbox / hardened-runtime resource access | AppContainer `webcam`; desktop camera privacy settings also apply | Camera portal / PipeWire where supported; direct device access has separate sandbox / device rules |
| Microphone | `NSMicrophoneUsageDescription`; enable Audio Input for the applicable sandbox / hardened-runtime configuration (see below) | AppContainer `microphone`; desktop-wide microphone privacy setting also applies | PulseAudio / PipeWire path; Flatpak `--socket=pulseaudio` permits audio access, not a per-app runtime consent guarantee |
| Photos / files | Sandbox file selection: `com.apple.security.files.user-selected.read-only` / `com.apple.security.files.user-selected.read-write` and P6. Direct PhotoKit: `NSPhotoLibraryUsageDescription` (or add-only key) plus applicable resource entitlement, including hardened-runtime `com.apple.security.personal-information.photos-library`; Pictures-folder access is not Photos-library access | AppContainer `picturesLibrary` for broad library access where required; system file selection can avoid broad access | Prefer FileChooser / document portal over blanket filesystem access |
| Location | `NSLocationUsageDescription` + `com.apple.security.personal-information.location` where required by sandbox / hardened runtime | `location` capability for applicable APIs / app model; also handle system consent / disabled location | Location portal / GeoClue where available |
| Notifications | UserNotifications authorization, no generic usage-description key; remote APNs registration uses `com.apple.developer.aps-environment` | Registration depends on notification API and package identity; see [media-devices.md, M6](media-devices.md) | Notification portal for sandboxed apps or supported desktop notification service |
| Bluetooth | `NSBluetoothAlwaysUsageDescription` for protected Bluetooth access; App Sandbox `com.apple.security.device.bluetooth` as needed | `bluetooth` device capability for applicable APIs / app model | BlueZ / D-Bus or Bluetooth sockets; sandbox permissions and service policy differ |
| Contacts | `NSContactsUsageDescription` + `com.apple.security.personal-information.addressbook` where required | `contacts` capability for applicable contact APIs / app model | No universal desktop contacts permission; check the provider |
| Calendars | macOS 14+: matching full-access / write-only usage key and EventKit API; retain legacy keys for older deployments. `com.apple.security.personal-information.calendars` for sandbox / hardened-runtime access | `appointments` capability for applicable calendar APIs / app model | No universal calendar permission; check the provider |
| Biometrics | LocalAuthentication / Touch ID; no Face ID usage string for Touch ID | Windows Hello availability / policy checks | No universal biometric API / consent model |

**Traps.**

- Consent, declarations, entitlements, hardware presence and service / global
  privacy switches are separate gates. Missing an Apple usage string can
  terminate the app for protected APIs; other failures may deny access.
  A plugin does not supply the host app's user-facing explanation by itself.
- Localize usage descriptions through the platform's Info.plist localization
  resources, such as `InfoPlist.strings`; explain the specific feature.
- macOS hardened-runtime resource entitlements are needed even outside the
  App Sandbox. `com.apple.security.device.audio-input` is documented for
  hardened-runtime audio input; current App Sandbox documentation also lists
  `com.apple.security.device.microphone`. Use Xcode's applicable Audio Input
  controls and inspect the emitted, signed entitlements for the deployment
  target. Verify both debug and distributed release builds, including helpers.
- MSIX packaging does not itself mean AppContainer. Full-trust desktop apps
  have different capability requirements; adding UWP capabilities does not
  override desktop privacy settings or firewall policy.
- Optional Android hardware must not silently become a store filter.
  `CAMERA` implies back-camera / autofocus requirements unless explicitly
  overridden: set `android.hardware.camera` and
  `android.hardware.camera.autofocus` to `required="false"` when optional;
  also mark optional camera.any / flash / microphone features accordingly.
  `camera.any` alone does not cancel an implied back-camera requirement.
  Audit iOS `UIRequiredDeviceCapabilities` for the same over-filtering risk.
- A portal backend / audio service can be absent on Linux. Detect this and
  offer a usable fallback; a successful unsandboxed development run does not
  verify the Flatpak / Snap package.

**LAN / nearby rules.**

- Android `CHANGE_WIFI_MULTICAST_STATE` enables multicast-lock operations;
  it is not a universal LAN permission. `NEARBY_WIFI_DEVICES` (API 33+,
  target 33+) protects specified Wi-Fi management APIs. Wi-Fi
  `startScan()` / `getScanResults()` still have location / Wi-Fi-state
  requirements; do not replace them blindly with nearby-device permission.
- Android 16 LAN protection is an opt-in compatibility test. Android 17+
  requires `ACCESS_LOCAL_NETWORK` for direct LAN access when targeting
  API 37+, unless the operation qualifies for system-mediated selection.
  Do not request that new permission on lower-target paths; test discovery
  and direct sockets with the permission denied as well as granted.
- Apple LAN privacy covers direct local connections as well as Bonjour.
  iOS / iPadOS multicast operations may additionally require
  `com.apple.developer.networking.multicast`; that entitlement is not
  required on macOS. The first operation can fail while the consent prompt
  is pending; wait for connectivity or retry safely after consent.
- Android Bluetooth `neverForLocation` is an assertion about actual use,
  not an optimization to add by default; it can filter some BLE beacons.
  Keep legacy Bluetooth permissions version-bounded for older devices.

**Verify.** Inventory feature API paths and inspect the merged Android
manifest, packaged `Info.plist` / localized strings, signed entitlements,
Windows package / trust level and Linux sandbox permissions. Run the signed
release package on a fresh permission state, including optional-hardware
devices. CI declaration checks support this; they do not prove runtime consent.

Sources: [Android permission reference](https://developer.android.com/reference/android/Manifest.permission),
[hardware filtering](https://developer.android.com/guide/topics/manifest/uses-feature-element),
[Wi-Fi permissions](https://developer.android.com/develop/connectivity/wifi/wifi-permissions),
[LAN protection](https://developer.android.com/privacy-and-security/local-network-permission),
[Bluetooth permissions](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions),
[Apple protected resources](https://developer.apple.com/documentation/bundleresources/protected-resources),
[APNs environment entitlements](https://developer.apple.com/documentation/bundleresources/entitlements/aps-environment),
[Apple LAN privacy](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy),
[hardened runtime](https://developer.apple.com/documentation/xcode/configuring-the-hardened-runtime),
[sandbox microphone entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.device.microphone),
[Photos-library entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.personal-information.photos-library),
[Calendar access migration](https://developer.apple.com/documentation/technotes/tn3152-migrating-to-the-latest-calendar-access-levels),
[Windows app models and capabilities](https://learn.microsoft.com/en-us/windows/apps/get-started/intro-pack-dep-proc),
[Windows capability reference](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations),
[Flatpak permissions](https://docs.flatpak.org/en/latest/sandbox-permissions.html),
[camera portal](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Camera.html).

## P2 Runtime flow — P0

**Rule.** Ask in context from a foreground Activity / scene after a user
action, serialize requests, and handle the result on the original attempt.
Keep an alternative path available rather than requesting everything at launch.

- Distinguish not-yet-requested, denied, restricted by policy / parental
  controls, limited and granted states. Settings cannot necessarily fix a
  managed restriction; don't promise that it can.
- Explain when useful or when Android
  `shouldShowRequestPermissionRationale()` recommends it. Its `false` result
  also occurs before the first request; it does not alone prove permanent
  denial. Combine documented status and request history. Don't loop prompts
  or send users to Settings automatically after they decline.
- Apple re-prompt rules depend on the resource and authorization level;
  camera / microphone denials generally require Settings. Don't generalize
  "iOS prompts only once" to all permissions. Pre-prompts must not imitate
  the system dialog or pressure the user into consent.
- On Android, one-time grants and unused-app permission resets can remove
  earlier access. Re-check before each protected operation and on return
  from Settings; handle a failure even after a successful check. Permission
  revocation can terminate the process, so restoration must work
  ([lifecycle.md, B3](lifecycle.md#b3-process-death-and-cold-start--p1)).
- Keep the pending action across rotation / Activity recreation and guard
  double taps. After the result, continue once if allowed; on the first
  denial, explain why the requested action did not run. Do not require a
  second tap to compensate for a stale plugin permission cache.
- Distinguish a missing camera / microphone from denial, a physical mute
  switch, another app owning the device, and a system privacy toggle.
  On Windows, some desktop-app controls are shared across desktop apps.
  Offer actionable diagnostics without assuming every failure is denial.
- Special access (exact alarms, full-screen intents, battery exemptions)
  uses its own status / Settings flow; do not pass it through a generic
  dangerous-permission request loop.

**Verify.** Fresh install: grant, deny once, deny again where applicable,
cancel / dismiss, limited / approximate, one-time grant, policy restriction,
and later Settings revocation. Rotate or resize with the prompt open,
double-tap the trigger, and return from Settings. Each case must produce a
single action or a clear usable fallback, with no prompt loop or crash.

Sources: [Android request flow](https://developer.android.com/training/permissions/requesting),
[one-time permissions and reset](https://developer.android.com/about/versions/11/privacy/permissions),
[Apple permission-request design](https://developer.apple.com/design/human-interface-guidelines/privacy),
[Windows camera / microphone privacy controls](https://support.microsoft.com/en-us/windows/manage-app-permissions-for-your-camera-in-windows-87ebc757-1f87-7bbf-84b5-0686afb6ca6b).

## P3 Degraded paths — P1

**Rule.** Treat reduced access as a supported feature state, not as a
binary failure or evidence that the user's data has been deleted.

- Notifications denied / channel muted: provide in-app unread state and
  explain the missed background alert behavior. Check actual notification
  settings; token registration is not authorization to display an alert
  ([media-devices.md, M6](media-devices.md)).
- Photos: use a system picker without broad library access. For a custom
  Android gallery targeting API 34+, handle `READ_MEDIA_VISUAL_USER_SELECTED`
  and reselection; a previously granted media permission / cached list can
  become stale. For iOS PhotoKit limited access, show only the authorized
  subset and offer supported selection management. Add-only access does not
  authorize reading the library.
- Contacts: handle iOS 18+ limited access; an empty or reduced query is not
  permission to erase remotely synced contacts. Offer a supported contact
  selection / access-management UI without demanding the full address book.
- Location: approximate / reduced accuracy must work at reduced precision.
  On iOS, temporary precise requests need a purpose entry in
  `NSLocationTemporaryUsageDescriptionDictionary`; ask only for a feature
  that needs it. Stage background authorization after foreground permission;
  on Android 11+ for apps targeting API 30+, a simultaneous foreground-and-
  background request is ignored.
- No hardware, disabled radios / location services, unavailable biometric
  enrollment, or no sensor: keep the rest of the app usable. Tablets and
  desktops need not have telephony, GPS, haptics, NFC or the expected camera.
  Permission success never proves hardware presence; use availability APIs.

**Verify.** Select only a few photos / contacts, then reduce the set in
Settings while the app is away. Test coarse location, global privacy
switches, missing hardware and an unavailable portal. Check data is neither
silently deleted nor presented as still accessible.

Sources: [Android selected photos](https://developer.android.com/about/versions/14/changes/partial-photo-video-access),
[Apple limited Photos access](https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app),
[limited contacts](https://developer.apple.com/documentation/contacts/cnauthorizationstatus/limited),
[temporary precise location purpose](https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationtemporaryusagedescriptiondictionary),
[Android staged background location](https://developer.android.com/develop/sensors-and-location/location/permissions/runtime).

## P4 Store privacy requirements — P0 for release

**Rule.** Review the shipped binary and SDK behavior against the current
submission rules; permission prompts, privacy manifests and store disclosures
are separate obligations. Record the policy check date and applicable app type.
Select the actual store / territory / package model using the
[store release guide](stores.md) ([简体中文](stores.zh-CN.md)); it also covers
publisher verification, submission access and channel-specific evidence.

- **Apple:** bundle valid `PrivacyInfo.xcprivacy` files where required for
  the app / SDK, including SDKs on Apple's required list and applicable SDK
  signatures. Declare actual approved reasons for covered APIs such as file
  timestamps, `UserDefaults`, boot time, disk space and active keyboards;
  do not copy a reason that doesn't describe the use. Verify the archive's
  privacy report, not just the presence of a source file.
- App Store privacy disclosures must include relevant SDK collection and
  tracking. Where App Tracking Transparency applies, include
  `NSUserTrackingUsageDescription`, request authorization using ATT, and
  honor denial. A privacy manifest does not replace ATT or resource consent.
- **Google Play:** reconcile Data safety and the privacy policy with actual
  collection / sharing, retention and SDK behavior, including the data
  deletion answers and deletion URL (the deletion flows themselves are in
  [P9](#p9-store-feature-and-audience-requirements--p0-for-release)). Check
  declarations / eligibility for background location, foreground-service
  types, full-screen intents, exact alarms, all-files access and SMS / call
  log access. Occasional photo / video selection must use a system picker
  rather than retain broad `READ_MEDIA_IMAGES` / `READ_MEDIA_VIDEO` access;
  broad access requires an eligible core use case and Play review.
- Check the current Play target-API requirements and Apple submission SDK
  requirements at release time; deadlines vary by app type and submission.
  Don't encode a past year's deadline as a timeless checklist rule.
- **Microsoft Store:** capabilities and any restricted-capability
  justifications must match the Windows app model and actual behavior.
- **Apple encryption export compliance:** set
  `ITSAppUsesNonExemptEncryption` according to the app's actual exemption
  status; using encryption does not by itself mean the value is `true`.

**Trap.** A dependency upgrade adds collection, a required-reason API or a
merged broad-media permission; the app's own code and privacy form appear
unchanged, but the submitted binary no longer matches them.

**Verify.** Diff dependency / permission changes, inspect the release archive
and privacy report, exercise opted-out network behavior, and compare store
answers to data flows and retention / deletion behavior. Capture policy
links and review evidence; a local test cannot guarantee store approval.
Payment, login, UGC, age-rating, children's and listing rules are in
[P8](#p8-purchases-subscriptions-and-entitlements--p0-if-monetized) and
[P9](#p9-store-feature-and-audience-requirements--p0-for-release).

Sources: [Apple privacy manifests](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files),
[required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api),
[SDK requirements](https://developer.apple.com/support/third-party-SDK-requirements/),
[ATT and privacy disclosures](https://developer.apple.com/app-store/user-privacy-and-data-use/),
[Play photo / video policy](https://support.google.com/googleplay/android-developer/answer/15800983?hl=en),
[Play sensitive-permission policy](https://support.google.com/googleplay/android-developer/answer/16558241?hl=en),
[Play Data safety policy](https://support.google.com/googleplay/android-developer/answer/18258653),
[Play target-API requirements](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en),
[Apple submission requirements](https://developer.apple.com/news/upcoming-requirements/),
[encryption compliance key](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption).

## P5 Data at rest and backup — P1

**Rule.** Choose secret accessibility, migration and backup behavior together;
encryption without a recoverable key / reauthentication path can lose data.

- Apple: store secrets in Keychain and deliberately choose accessibility,
  access groups, synchronizability and `ThisDeviceOnly` behavior. Handle
  locked-device / biometric-policy failures without replacing valid data
  with empty defaults. File protection is covered in [lifecycle.md, B2](lifecycle.md#b2-persist-before-suspension--p0).
- Android Keystore stores cryptographic keys, not arbitrary token strings.
  Use appropriate Keystore-backed encryption for stored secrets; handle
  invalidated / missing keys and require reauthentication when necessary.
  `EncryptedSharedPreferences` is deprecated in AndroidX Security Crypto
  1.1.0; do not introduce it as the default new design or replace encrypted
  storage with plaintext simply because it is deprecated.
- Windows: use DPAPI / Credential Manager as appropriate to the user and
  app model. Linux: use Secret Service / a supported credential-store
  backend; a missing or locked keyring needs a cancellable, bounded wait and
  a clear fallback, never silent plaintext storage.
- Keychain items can remain after iOS app deletion, but uninstall persistence
  is not a documented lifetime guarantee. Implement explicit logout / account
  reset and server token revocation. A missing `UserDefaults` first-launch
  flag alone is not a safe reason to clear an entire Keychain access group:
  restoration and other apps / extensions can share state. Scope any cleanup
  to items the app owns and to an explicit account / installation policy.
- Android Auto Backup is normally enabled for participating apps; decide
  `android:allowBackup` explicitly. Use `android:fullBackupContent` for older
  backup rules and, for apps targeting API 31+ on Android 12+,
  `android:dataExtractionRules` for separate cloud / device-transfer rules.
  On some manufacturers' devices, `allowBackup="false"` alone does not stop
  device-to-device transfer. Exclude device-bound ciphertext / identifiers
  that cannot be meaningfully restored, or provide a safe recovery path.
- Apple app-container backup does not include every file: caches / temporary
  data are not durable backup storage. Set `isExcludedFromBackupKey` for
  deliberately excluded files; reapply / verify it after replacements that
  can reset the attribute, and handle existing files when changing policy.
  That file attribute does not control Keychain-item migration.

**Verify.** Test update, uninstall / reinstall, clear-data where supported,
backup restore and transfer to another device. Include restored ciphertext
without its key, changed biometric enrollment, a locked keyring and an
account switch. User documents should recover according to policy; secrets
must neither leak across accounts nor cause an unrecoverable startup loop.

Sources: [Apple Keychain accessibility](https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility),
[Apple DTS on uninstall semantics](https://developer.apple.com/forums/thread/36442),
[Android Keystore](https://developer.android.com/privacy-and-security/keystore),
[EncryptedSharedPreferences deprecation](https://developer.android.com/reference/androidx/security/crypto/EncryptedSharedPreferences),
[Windows DPAPI](https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata),
[Secret Service locking](https://specifications.freedesktop.org/secret-service/latest/unlocking.html),
[Android backup / transfer rules](https://developer.android.com/identity/data/autobackup),
[Apple backup exclusion](https://developer.apple.com/documentation/foundation/urlresourcekey/isexcludedfrombackupkey).

## P6 Selected files and persistent access — P1

**Rule.** A picker result is scoped access, not ownership of a permanent
local path. Before deferred work, either copy into app-owned durable storage
or retain the grant / bookmark supported by that API.

- Android: consume `content://` URIs with `ContentResolver`; do not guess a
  filesystem path from them. For Photo Picker / `ACTION_OPEN_DOCUMENT`, take
  a persistable URI grant when supported and needed, with only granted
  read / write modes. `ACTION_GET_CONTENT` and arbitrary shared URIs do not
  promise persistable access. Release grants no longer needed; even a
  persisted grant cannot resurrect a moved / deleted or revoked document.
- iOS / macOS: balance a successful
  `startAccessingSecurityScopedResource()` with
  `stopAccessingSecurityScopedResource()` after asynchronous work completes.
  For supported persistent access, store / resolve bookmark data, handle
  stale bookmarks and use the required sandbox bookmark entitlement where
  applicable. Respect document-provider coordination / download behavior.
  A temporary item-provider file must be copied while its callback permits
  access, before returning it to a background job.
- Windows: file-picker access and retained access lists depend on API / app
  model; sandboxed apps must not assume a path string retains the grant.
  Linux: use the document portal when retaining sandbox access and handle
  missing backends or revoked access. Cloud / removable documents can become
  unavailable on any platform; offer reselection without losing the draft.

**Trap.** An attachment works immediately, then fails after restart because
the app retained only a temporary path / URI instead of the content or grant.

**Verify.** Select local, cloud and removable content; background, terminate
and reboot before upload / reopen. Remove or revoke the original and verify
reselection or a clear recoverable failure. Check that granting one file
does not broaden access to its directory and that completed work releases
unused access and temporary copies ([lifecycle.md, B6](lifecycle.md#b6-durable-transfers-and-retry-ownership--p1)).

Sources: [Android Photo Picker persistence](https://developer.android.com/training/data-storage/shared/photo-picker),
[Storage Access Framework grants](https://developer.android.com/training/data-storage/shared/documents-files),
[Apple security-scoped access](https://developer.apple.com/documentation/foundation/url/startaccessingsecurityscopedresource()),
[temporary item-provider files](https://developer.apple.com/documentation/foundation/nsitemprovider/loadfilerepresentation(fortypeidentifier:completionhandler:)),
[Windows retained file access](https://learn.microsoft.com/en-us/windows/uwp/files/how-to-track-recently-used-files-and-folders).

## P7 Sensitive content and screen capture — P1

**Rule.** Define what can appear in task-switcher snapshots, screenshots,
recordings and external-display sharing. Apply protection per window / scene
before sensitive content becomes capturable; do not promise universal
capture prevention across platforms.

- Android `WindowManager.LayoutParams.FLAG_SECURE` blocks ordinary
  screenshots and display on nonsecure outputs for that window. Apply it
  to sensitive dialogs / additional windows too and test casting / Recents.
  It does not prevent every overlay attack or external photography.
- iOS / iPadOS: cover sensitive scenes before background snapshots. Use
  scene capture state (`UITraitCollection.sceneCaptureState` on supported
  systems) for active recording / mirroring responses; use availability
  checks for older APIs. A screenshot notification arrives after capture;
  it cannot retroactively hide the image. There is no general iOS equivalent
  of `FLAG_SECURE` for arbitrary application UI; avoid unsupported secure
  text-field rendering tricks.
- Snapshot covers and capture handling must work on every scene and recover
  after authentication / foregrounding. Do not tear down a legitimate call
  merely because a permission dialog made a window inactive
  ([lifecycle.md, B1](lifecycle.md#b1-lifecycle-states-differ-per-platform--p0)).
- Windows: `SetWindowDisplayAffinity` with `WDA_EXCLUDEFROMCAPTURE` is
  supported on Windows 10 version 2004+ for the process's own top-level
  windows under DWM composition; check the return value and older-version
  behavior. It is not a security / DRM guarantee. On macOS / Linux, verify
  the actual capture API / compositor; a framework's shared protection flag
  does not establish equivalent protection on every desktop.

**Verify.** Take real-device screenshots, start / stop recording and
mirroring, lock / unlock, open a system permission dialog and inspect the
app switcher. Check all windows / scenes, including dialogs, and confirm
privacy covers neither expose a frame nor remain stuck after return.

Sources: [Android sensitive Activities](https://developer.android.com/security/fraud-prevention/activities),
[Apple scene capture handling](https://developer.apple.com/documentation/swiftui/protecting-sensitive-content-when-screen-sharing),
[Apple background snapshot preparation](https://developer.apple.com/documentation/uikit/preparing-your-ui-to-run-in-the-background),
[Windows display affinity](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowdisplayaffinity).

## P8 Purchases, subscriptions and entitlements — P0 if monetized

**Rule.** Choose the payment mechanism per product type, distribution
channel and storefront, then keep one server-side entitlement record that
every shipped platform reads. Grant access only for a verified, completed
transaction; process completion, restoration, renewal, refund and revocation
idempotently, from any device and while the app is not running.

- **Which mechanism.** Digital content and features generally require the
  store's billing: App Store in-app purchase (Guideline 3.1.1) and Google
  Play Billing (Payments policy). Check exclusions separately per store:
  Apple lets physical goods and services consumed outside the app, and
  qualifying real-time one-to-one services, use other payment methods, but
  one-to-few and one-to-many real-time services require IAP (3.1.3(d) /
  (e)); Play Billing must not be used for peer-to-peer payments or its
  listed physical-goods and physical-services categories. Exceptions and steering rules differ by
  storefront and programme: Apple's US-storefront link rule, reader-app and
  multiplatform-service exceptions (3.1.3(a) / (b)), Play's regional
  alternative-billing and external-offer programmes. Record the rule, its
  check date and the storefront; do not ship one global "buy on our website"
  button. Microsoft Store (policy 10.8.1) requires its purchase API for
  digital goods in games and Xbox products, except games (and their
  in-app purchases) offered through a PC gaming subscription product
  (10.8.6); non-game PC apps may use a secure third-party API.
- **Cross-platform access.** Apple 3.1.3(b) allows access on iOS to content
  bought on other platforms or the web only when those items are also
  offered as in-app purchases in the app. Apple 3.1.2(a) requires
  subscriptions to be available across all of the user's devices. Key the
  entitlement to the app account, not to the device or store receipt alone,
  and decide what an account bought on one store sees on the others.
- **Transaction lifecycle.**
  - Google Play: grant only in the `PURCHASED` state, never `PENDING`;
    acknowledge (or consume) within three days of reaching `PURCHASED`, or
    the purchase is refunded automatically. Call `queryPurchasesAsync()`
    after connecting and in `onResume()`; use Real-time developer
    notifications and the Voided Purchases API for server state.
  - Apple StoreKit: listen to `Transaction.updates` from launch, verify the
    transaction, deliver, then `finish()`. Unfinished transactions are
    redelivered. Handle Ask to Buy / Family Sharing, refunds and
    `revocationDate`, and use App Store Server Notifications on the backend.
  - Provide a visible restore action for restorable purchases (Apple
    3.1.1). Consumables are not restorable from either store; keep their
    balance on your server if it must survive reinstall or device change.
- **Subscriptions.** Cancellation normally keeps access until the end of
  the paid period; billing retry / grace periods, account hold, pauses,
  upgrades / downgrades and family sharing change entitlement on their own
  schedule. Describe what the user gets for the price before purchase
  (Apple 3.1.2(c)) and prevent duplicate subscriptions to variants of the
  same thing (3.1.2(b)).
- **Platform coverage.** Check each purchase integration's supported
  platforms and methods. Unsupported targets need an implementation
  permitted by their distribution channel (a separate store API or an
  allowed web checkout) or a disabled purchase UI. See
  [Flutter purchase notes](flutter.md).

**Traps.** Unlocking on a `PENDING` / deferred purchase; an Android purchase
silently refunded because the app crashed before acknowledging; trusting the
client's "success" callback without server verification; losing paid access
after reinstall because entitlement lived only in local storage; a consumable
credited twice when consumption / finish failed and was retried; revoking
access the moment a user cancels; a "manage subscription" link to the wrong
store for a user who subscribed on another platform; the web price shown in
an app storefront where steering is not allowed.

**Verify.** Use store sandbox / license-tester accounts on release-signed
builds. Exercise successful, cancelled, pending-then-approved,
pending-then-declined and duplicate purchases; kill the app after payment
but before acknowledgement / finish and relaunch; restore on a fresh
install and a second device; refund, revoke, renewal failure, grace period
and expiry; account switch and sign-out. Confirm the entitlement appears on
every other shipped platform for the same account and that server state
matches store notifications ([lifecycle.md, B6](lifecycle.md#b6-durable-transfers-and-retry-ownership--p1)
covers durable retry ownership).

Sources: [Apple payment guidelines](https://developer.apple.com/app-store/review/guidelines/#payments),
[StoreKit transaction updates](https://developer.apple.com/documentation/storekit/transaction/updates),
[App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications),
[Play Payments policy](https://support.google.com/googleplay/android-developer/answer/9858738),
[Play Billing integration and purchase lifecycle](https://developer.android.com/google/play/billing/integrate),
[Microsoft Store policies, 10.8](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies),
[Flutter in_app_purchase](https://pub.dev/packages/in_app_purchase).

## P9 Store feature and audience requirements — P0 for release

**Rule.** Keep a dated channel × territory × feature inventory and check,
for each shipped store, the review rules triggered by what the app does:
account deletion, third-party login, user-generated content, age rating,
children's audience and localized store metadata. These are separate from
privacy declarations ([P4](#p4-store-privacy-requirements--p0-for-release))
and from the binary's own localization ([display.md, D2](display.md)).
For publisher / listing ownership, review credentials, store release controls
and desktop / regional channels, use [stores.md](stores.md). A passed unit
test does not establish that a required store-console answer was completed.

- **Account deletion.** If the app supports account creation, users must be
  able to start deletion of the account and its associated data in the app
  (Apple 5.1.1(v); Play account-deletion policy, which also covers accounts
  created through an external flow the app links to).
  - Apple: easy to find (typically account settings); temporary deactivation
    is insufficient; a link out only when the website completes the
    process; outside highly regulated industries do not require a call,
    email or support chat. Guest / auto-created accounts are included.
    Sign in with Apple accounts must revoke tokens through the Sign in with
    Apple REST API. Warn that App Store subscription billing continues until
    the user cancels it.
  - Google Play: an in-app path **and** a web resource where users can
    request deletion without reinstalling the app, naming the app or
    developer as listed on Play; enter that URL in the Data safety form.
    Non-mobile Play targets need only the web resource. Delete associated
    data, including copies at service providers; disclose any data retained
    for security, fraud prevention or regulatory reasons.
  - Tell users how long deletion takes and confirm completion.
- **Third-party login (Apple 4.8).** An app that uses a third-party or
  social login as the primary account must also offer an equivalent login
  option that limits collection to name and email, lets users keep their
  email private and does not collect interactions for advertising without
  consent. Sign in with Apple satisfies this. Exceptions include apps that
  use only the developer's own account system, education / enterprise /
  business apps requiring an existing account, government or
  industry-backed ID, and clients of a specific third-party service. Apply
  the same login set on iPadOS and macOS builds. If accounts can be created
  with Sign in with Apple, the non-Apple builds still need a way into the
  same account (for example Apple's web-based sign-in or an account
  recovery path) and the same deletion handling.
- **User-generated content.** Apple 1.2 requires filtering of
  objectionable material, reporting with timely responses, blocking abusive
  users and published contact information. Google Play requires accepted
  terms before posting, ongoing moderation, in-app reporting of content and
  users, and blocking where users interact one-to-one or publicly. Chat,
  comments, profiles and shared media all count.
- **Age ratings.** Answer each store's questionnaire honestly and update it
  when features change: App Store Connect's questionnaire (Apple 2.3.6),
  IARC for Google Play and Microsoft Store (Store policy 11.11). Apple's
  updated system (4+, 9+, 13+, 16+, 18+, shown on OS 26 devices) required
  answers to the new questions by 2026-01-31 to avoid submission
  interruptions; its social-media-capability questions (added 2026-07-09)
  became required for new submissions and updates from September 2026.
  Store screenshots and previews must still suit a 4+ audience (Apple
  2.3.8). Ratings can differ per region.
- **Children and families.** Apple Kids Category / 5.1.4: no third-party
  analytics or advertising except the narrow allowances in 1.3, no device
  data or PII to third parties, and links out, purchases or other
  distractions only behind a parental gate. Google Play Families: declare
  the target audience accurately. Apps solely for children use only APIs /
  SDKs approved for child-directed services. Mixed-audience apps may use
  other SDKs only behind a neutral age screen, or without collecting data
  from children, and child content must not depend on them. Ads served to
  children or users of unknown age use Families self-certified ads SDK
  versions with no interest-based targeting or remarketing, and no AAID or
  other prohibited identifier is transmitted from children or users of
  unknown age. SDK behaviour must follow the audience decision at runtime,
  not just the listing.
- **Store listing localization.** Store metadata is translated separately
  from the app. Where no localization matches the user's language, Apple
  may pick the next most relevant one, otherwise the primary language; new
  localizations start with the primary language's screenshots. Play shows default-language graphics without
  localized assets and may offer users a machine translation of untranslated
  text. Localize name, description, keywords, screenshots with text and
  in-app product names for each language the app claims to support.

**Traps.** "Deactivate account" or "email us" offered as deletion; deleting
the login but keeping messages, media or server-side copies; a Sign in with
Apple user deleted without token revocation; a deletion web page that needs
the app installed; Google login added to the iOS build without an
equivalent option; chat shipped without report / block; an age-rating
answer left from before UGC or chat was added; an analytics or ads SDK that
keeps sending identifiers after a neutral age screen classifies the user as
a child; the app translated into ten languages while the listing and
screenshots stay English-only.

**Verify.** For each store: create and delete an account in the release
build (including guest and Sign in with Apple accounts) and confirm server
data, tokens and provider copies are gone or retained as disclosed; use the
Play deletion web resource from a device without the app. Report and block a
test user end to end and confirm a moderator receives the report. Record the
rating answers and check them against current features. Audit SDK
versions and configurations, then run the child and unknown-age paths
through a proxy and confirm no prohibited identifiers and only certified
ads SDK traffic. Inspect every listing language and screenshot set in the store
consoles. Record policy links and check dates; a local test cannot
guarantee store approval.

Sources: [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/),
[Apple account-deletion guidance](https://developer.apple.com/support/offering-account-deletion-in-your-app/),
[Play account-deletion requirements](https://support.google.com/googleplay/android-developer/answer/13327111),
[Play User Generated Content policy](https://support.google.com/googleplay/android-developer/answer/9876937),
[Play Families policies](https://support.google.com/googleplay/android-developer/answer/9893335),
[Apple age ratings](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating),
[Apple age-rating update (deadline 2026-01-31)](https://developer.apple.com/news/upcoming-requirements/?id=07242025a),
[Apple social-media age-rating questions](https://developer.apple.com/news/?id=tlur8uvi),
[Microsoft Store policies, 11.11 / 11.12](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies),
[Apple metadata localization](https://developer.apple.com/help/app-store-connect/manage-app-information/localize-app-information/),
[Play listing translation](https://support.google.com/googleplay/android-developer/answer/9844778).
