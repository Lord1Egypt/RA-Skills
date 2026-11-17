# Sources, version gates and related projects

The checklist IDs are this skill's own; this file maps them to the official
guidelines they align with, lists dated platform / store gates, and points
to related projects. Last checked: **2026-10-22**. Dates and thresholds
change: re-check the linked source before relying on one, and record the
date you checked in the evidence (see the entrypoint’s version-gate guidance).

## Official guidelines

| Source | Covers | Checklist IDs |
|---|---|---|
| [Android core app quality](https://developer.android.com/docs/quality-guidelines/core-app-quality) | Back navigation, state preservation, runtime permissions, notifications, backup, 48 dp targets, contrast | I1, I4, B2–B3, P2, P5, M6 |
| [Android adaptive app quality tiers](https://developer.android.com/docs/quality-guidelines/large-screens-app-quality) ([tier 3](https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/tier-3)) | Configuration changes and combinations (resize then rotate, rotate then fold), multi-window, multi-resume, camera preview, keyboard / mouse / stylus, reference device sizes | L1–L3, L6, L8, I2, B1, M3, X1, X3 |
| [Android 15 behaviour changes](https://developer.android.com/about/versions/15/behavior-changes-15), [Android 16 behaviour changes](https://developer.android.com/about/versions/16/behavior-changes-16) | Edge-to-edge, `Configuration` sizes incl. system bars, foreground-service limits, large-screen orientation / resizability, predictive back, `elegantTextHeight`, locale code changes | L2, L4, L6, D2, I4, B4 |
| [Android foreground-service changes](https://developer.android.com/develop/background-work/services/fgs/changes) | Service types, permissions, timeouts and start restrictions per version | B4, P1 |
| [Android 16 KB page sizes](https://developer.android.com/guide/practices/page-sizes) | Native library alignment and testing | X6 |
| [Android / Material window size classes](https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes) | Breakpoints | L2 |
| [Google Play Data safety](https://support.google.com/googleplay/android-developer/answer/10787469), [target API requirements](https://support.google.com/googleplay/android-developer/answer/11926878) | Store privacy declarations, target SDK deadlines | P4 |
| [Apple HIG: layout](https://developer.apple.com/design/human-interface-guidelines/layout), [multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking), [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) | Safe areas, size classes, 44 pt targets, resizable windows | L1–L4, I1, I5 |
| [TN3192: migrating from `UIRequiresFullScreen`](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key) | iPadOS 26 resizable windows, scene size restrictions | L2, L6 |
| [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) | 2.4.1 iPhone apps on iPad, 2.5.4 background modes only for their purpose, 5.1.1 purpose strings, pickers over full library access, alternatives when consent is denied | L1, B4, P1–P3 |
| [Apple privacy manifest](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files), [required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api) | `PrivacyInfo.xcprivacy`; file timestamp, system boot time, disk space, active keyboards and `UserDefaults` categories | P4 |
| [Apple upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) | Submission SDK and minimum-target gates | P4, W4 |
| [Windows high-DPI desktop development](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows) | Per-Monitor V2, `WM_DPICHANGED`, mixed-DPI test list | D3–D4, W1 |
| [Windows breakpoints](https://learn.microsoft.com/en-us/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design), [app capability declarations](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations) | Effective-pixel breakpoints and scale plateaus; packaged capabilities, restricted capabilities | L2, D3, P1 |
| [GNOME HIG: adaptive](https://developer.gnome.org/hig/guidelines/adaptive.html), [KDE HIG](https://develop.kde.org/hig/) | Linux minimum sizes, adaptive layouts | L1, W1 |
| [Flatpak sandbox permissions](https://docs.flatpak.org/en/latest/sandbox-permissions.html), [Flathub quality guidelines](https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines/quality-guidelines) | Portals over broad filesystem access, Wayland socket with X11 fallback; square SVG or PNG icon ≥ 256 × 256 px, metadata and screenshots | P1, D5, W4 |
| [freedesktop Desktop Entry](https://specifications.freedesktop.org/desktop-entry-spec/latest/) and [Icon Theme](https://specifications.freedesktop.org/icon-theme-spec/latest/) specs | `.desktop` files, MIME / URL handlers, hicolor icons | D5, W4 |
| [Flutter adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive) ([best practices](https://docs.flutter.dev/ui/adaptive-responsive/best-practices)) | Don't lock orientation, don't branch on device type, `MediaQuery.sizeOf` / `LayoutBuilder`, input, capabilities | L1–L3, L6, I2 |
| [Flutter accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility) | Release checklist: targets, contrast, screen readers, large scale factors | D1, D6, I1, I5 |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WCAG2Mobile](https://www.w3.org/TR/wcag2mobile-22/) (informative draft guidance) | Contrast, WCAG 2.2 SC 2.5.8 target size (24 × 24 CSS px minimum at AA, subject to its exceptions), orientation, reflow, text resize, motion | D1, D6, D7, I1, I7, L6 |
| [Android vitals](https://developer.android.com/topic/performance/vitals) ([rendering](https://developer.android.com/topic/performance/vitals/render), [launch time](https://developer.android.com/topic/performance/vitals/launch-time)), [Apple ProMotion](https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays), [MetricKit](https://developer.apple.com/documentation/metrickit), [Android thermal APIs](https://developer.android.com/games/optimize/adpf/thermal) | Slow / frozen frames, startup TTID / TTFD and bad-behaviour thresholds, wake-lock metric, refresh-rate ranges, thermal state | F1–F3 |
| [Android App Links verification](https://developer.android.com/training/app-links/verify-applinks), [Apple associated domains](https://developer.apple.com/documentation/xcode/supporting-associated-domains) ([TN3155](https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links)), [Windows web-to-app linking](https://learn.microsoft.com/en-us/windows/apps/develop/launch/web-to-app-linking) | Verified link setup and debugging | I8 |
| [Android secure file sharing](https://developer.android.com/training/secure-file-sharing/share-file), [receive rich content](https://developer.android.com/develop/ui/views/receive-rich-content), [Windows share sheet](https://learn.microsoft.com/en-us/windows/apps/develop/windows-integration/integrate-sharesheet-receive), [FileTransfer portal](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.FileTransfer.html) | Clipboard, share and drag between apps | I9 |
| [Apple Voice Control evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/voice-control-evaluation-criteria/), [Android accessibility testing](https://developer.android.com/guide/topics/ui/accessibility/testing) | Voice and switch input passes | I5, I7 |
| [Room migrations](https://developer.android.com/training/data-storage/room/migrating-db-versions), [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html), [Android offline-first](https://developer.android.com/topic/architecture/data-layer/offline-first), [Flutter offline-first](https://docs.flutter.dev/app-architecture/design-patterns/offline-first) | Schema migration, offline writes and sync | B7, B8 |
| [Dart file locks](https://api.dart.dev/dart-io/RandomAccessFile/lock.html), [Windows byte-range locks](https://learn.microsoft.com/en-us/windows/win32/fileio/locking-and-unlocking-byte-ranges-in-files), [Dart `Future.timeout`](https://api.dart.dev/dart-async/Future/timeout.html) | Process / handle lock ownership and a wait deadline's lack of cancellation | B5, W2 |
| [Apple TN2206](https://developer.apple.com/library/archive/technotes/tn2206/_index.html), [Android app signing](https://developer.android.com/studio/publish/app-signing), [Git index modes](https://git-scm.com/docs/git-update-index) | Final artifact signing, upload vs distribution keys, clean-checkout helper execution | W4, X6 |
| [Flutter current / historical support](https://docs.flutter.dev/reference/supported-platforms#previous-flutter-versions), [Windows target selection discussion](https://github.com/flutter/flutter/issues/186730), [PE headers](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#machine-types), [Mach-O slices](https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary), [ELF headers](https://sourceware.org/binutils/docs/binutils/readelf.html) | Host vs tool ABI vs target, SDK / engine availability and final native-payload architecture; checked 2026-10-23. Pinned Flutter source links and the verification recipe are in [flutter.md](flutter.md) / [testing.md](testing.md). | W4, X6 |
| [MSI Template Summary](https://learn.microsoft.com/en-us/windows/win32/msi/template-summary), [MSIX Identity](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-identity) | Installer / package architecture metadata compared with payload and store target, separately from filenames; checked 2026-10-23 | W4, X6 |
| [Play Billing integration](https://developer.android.com/google/play/billing/integrate), [Play Payments policy](https://support.google.com/googleplay/android-developer/answer/9858738), [App Review 3.1 payments](https://developer.apple.com/app-store/review/guidelines/#payments), [Microsoft Store policies](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies) | Required billing per channel, transaction lifecycle | P8 |
| [Apple account deletion](https://developer.apple.com/support/offering-account-deletion-in-your-app/), [Play account deletion](https://support.google.com/googleplay/android-developer/answer/13327111), [Play UGC](https://support.google.com/googleplay/android-developer/answer/9876937), [Play Families](https://support.google.com/googleplay/android-developer/answer/9893335) | Deletion, user-generated content, children's rules | P9 |
| [Android connected displays](https://developer.android.com/develop/adaptive-apps/guides/support-connected-displays), [desktop windowing](https://developer.android.com/develop/ui/compose/layouts/adaptive/support-desktop-windowing), [ChromeOS](https://developer.android.com/develop/devices/chromeos/learn), [TV quality](https://developer.android.com/docs/quality-guidelines/tv-app-quality), [Android XR readiness](https://developer.android.com/develop/xr/check-mobile-app-readiness) | New Android form factors | L3, L4, M7, X1 |
| [iPhone / iPad apps on Apple silicon Macs](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-macs-with-apple-silicon/), [visionOS compatibility](https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos), [WWDC25 iPad windowing and menus](https://developer.apple.com/videos/play/wwdc2025/208/) | Apple compatibility surfaces, iPadOS 26 window controls and menu bar | L4, I2, W4, X1 |
| [Flutter error handling](https://docs.flutter.dev/testing/errors), [obfuscation and symbols](https://docs.flutter.dev/deployment/obfuscate), [Apple debug information](https://developer.apple.com/documentation/xcode/building-your-app-to-include-debugging-information), [Android native symbols](https://developer.android.com/build/include-native-symbols), [log information disclosure](https://developer.android.com/privacy-and-security/risks/log-info-disclosure) | Crash capture, symbolication, private logs | X9 |
| [OWASP MASVS](https://mas.owasp.org/MASVS/) (MASVS-STORAGE, MASVS-PRIVACY) | Data at rest, privacy disclosures matching store declarations | P4, P5, P7 |

## Dated gates (checked 2026-10-22)

Confidence: **high** — read on the official page; **medium** — official
page partly unreadable or history inconsistent.

| Gate | Date / threshold | Confidence |
|---|---|---|
| Google Play: new apps and updates must target API 36 (Wear OS / Automotive 35, TV / XR 34) | 2026-08-31, extension to 2026-11-01 on request | high |
| [Google Play 16 KB page-size compatibility](https://developer.android.com/guide/practices/page-sizes): updates targeting API 35+ on 64-bit devices | 2027-02-01 for updates | high |
| Android 16, target 36: orientation / resizability / aspect-ratio restrictions ignored on sw ≥ 600 dp; temporary opt-out property | Opt-out removed for target 37 (Android 17); boundary wording differs between pages, see [L6](layout.md) | high (behaviour), medium (boundary) |
| Android 16, target 36: predictive back animations on by default; `onBackPressed` / `KEYCODE_BACK` no longer delivered unless opted out | Target 36 | high |
| Android 15, target 35: edge-to-edge enforced; Android 16 target 36 removes the opt-out attribute | Target 35 / 36 | high |
| Android 15, target 35: `dataSync` / `mediaProcessing` foreground services limited to 6 h per 24 h in background | Target 35 | high |
| Android local network permission | Opt-in testing on 16; enforced for target 37 (see [P1](permissions.md)) | medium |
| App Store Connect uploads for iOS / iPadOS / tvOS / visionOS / watchOS: Xcode 26+ and the respective OS 26+ SDK (macOS not listed) | 2026-04-28 | high |
| [App Store Connect uploads: iOS / iPadOS deployment target must be iOS 13+](https://developer.apple.com/news/upcoming-requirements/) | 2026-09-09 | high |
| `UIRequiresFullScreen` deprecated in iPadOS 26; built with the iOS 27 SDK and run on iOS / iPadOS 27 it no longer prevents resizing and can select discrete scene resizing ([TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key), see [L6](layout.md)) | SDK 27 / OS 27 | high |
| Apple required-reason API declarations | Enforced since 2024-05-01 | high |
| Apple age ratings: updated questionnaire answers required for app updates (new 13+ / 16+ / 18+ tiers) | 2026-01-31 | high |
| [Apple social-media age-rating answers](https://developer.apple.com/news/?id=tlur8uvi) required for new apps, updates and alternative-distribution notarization | From September 2026 (exact day not stated) | high |
| [Play excessive partial wake locks](https://developer.android.com/google/play/vitals/excessive-wakelock): 2 or more cumulative hours of non-exempt locks in 24 h while backgrounded or in a foreground service; more than 5 % of sessions over 28 days can affect visibility | From [2026-03-01](https://developer.android.com/blog/posts/raising-the-bar-on-battery-performance-excessive-partial-wake-locks-metric-is-now-out-of-beta) | high |

## Store release source map

Use [stores.md](stores.md) ([简体中文](stores.zh-CN.md)) for dated, directly
linked official sources and evidence under **P4 / P8 / P9 / W4 / X6**:

| Scope | Source families / applicability |
|---|---|
| Apple App Store | App Store Connect, App Review; iOS / iPadOS / macOS, with Mac App Store separated from outside-Store Developer ID / notarization |
| Google Play | Play Console setup, access, declarations, testing / production eligibility, signing and release controls |
| Microsoft Store | Partner Center and current formal Store Policies; MSIX/AppX re-signing is separate from non-game PC hosted MSI/EXE rules |
| Flathub / Snap Store | Inclusion / confinement / permission and submission rules; optional quality / promotion measures are labelled separately |
| Selected mainland China Android channels | Huawei, Xiaomi, OPPO official submission / review sources and MIIT scope; partial public access is explicitly marked for owner portal follow-up |
| Other chosen channels | WinGet, Homebrew Cask, F-Droid and direct downloads / distro repositories; none is required merely because it is listed |

The guide records a **2026-10-22** public-source check, including access
limitations. Recheck live policies and the selected console for each
release. These document checks are not evidence of an app submission,
legal applicability determination or store approval.

## Related projects

| Project | Worth borrowing | Licence |
|---|---|---|
| [flutter/agent-plugins](https://github.com/flutter/agent-plugins) | Flutter team's agent skills (responsive layout, layout fixes, localisation, integration tests); complementary, task-level rather than a compatibility checklist | BSD-3-Clause |
| [OWASP MASVS](https://mas.owasp.org/MASVS/) / [MASTG](https://mas.owasp.org/MASTG/) | Control phrasing and linked privacy tests; the historical checklist spreadsheet was [retired in MASTG v2](https://mas.owasp.org/news/2026/07/14/checklists-removal/) | CC BY 4.0 for current website content; check historical artifacts separately |
| [gskinnerTeam/flutter-adaptive-demo](https://github.com/gskinnerTeam/flutter-adaptive-demo), [Wonderous](https://github.com/gskinnerTeam/flutter-wonderous-app) | Reference adaptive Flutter implementations | see repositories |
| [oisin/app-release-checklist](https://github.com/oisin/app-release-checklist) | Store and localisation pre-release items (dated) | see repository |
| [bbc/bbc-a11y](https://github.com/bbc/bbc-a11y), [BBC Mobile Accessibility Guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/) | Which accessibility checks can be automated | see repository |
