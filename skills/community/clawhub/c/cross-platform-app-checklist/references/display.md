# Text, density and assets (D1–D7)

Platform details checked against the linked primary sources on 2026-10-22.
Logical text size, display density and application zoom are independent;
exercise them separately and in combination.

## D1 Large text — P0

**Rule.** Support the platform's native text-size settings, including its
largest accessibility category. Use 1.0, 1.3 and 2.0 as additional synthetic
layout tests, not as a replacement for native settings.

- Android 14+ supports font scaling up to 200 % with **non-linear** scaling:
  larger source sizes grow less than smaller ones. Use `sp` and the toolkit's
  current conversion / text-measurement APIs; multiplying by `fontScale` or
  `scaledDensity` is not an equivalent conversion. See [Android font scaling](https://developer.android.com/about/versions/14/features).
- iOS / iPadOS: test through Dynamic Type's largest accessibility category,
  `accessibilityExtraExtraExtraLarge`. The ratio depends on the text style;
  there is no universal 310 % scale. Scale custom fonts through the native
  text-style mechanism too. See [Dynamic Type](https://developer.apple.com/documentation/uikit/scaling-fonts-automatically)
  and [size categories](https://developer.apple.com/documentation/uikit/uicontentsizecategory).
- Desktop: test OS text enlargement separately from display scaling and any
  in-app zoom. Scaling the whole window bitmap does not establish that text
  enlargement works.

**Traps.**

- Fixed-height tiles, chips, segments and app bars clip text; use content
  sizing, wrapping and a minimum height instead of a fixed height.
- A label and value share a row with no flexible space; switch to a column
  when measured content no longer fits.
- Shrink-to-fit, ellipsis, fades and arbitrary font-size floors hide essential
  text or defeat the requested size. Reflow first; provide an accessible way
  to reach any intentionally abbreviated content.
- Clamping tab / FAB labels to an arbitrary 1.3× is not an accessibility
  guarantee. Adapt navigation or use an equivalent labelled control.
- Fonts or cached measurements do not update when the setting changes.
  Re-measure line height, baselines and wrapping while the app is running.
- Bold Text, fallback fonts and accents can increase glyph bounds even at
  the same nominal font size.
- Custom text renderers and cached layouts miss Bold Text. Check whether
  the framework already applies the preference before adding an
  adjustment. Apple exposes
  [`UIAccessibility.isBoldTextEnabled`](https://developer.apple.com/documentation/uikit/uiaccessibility/isboldtextenabled);
  Android 12+ (API 31) reports the weight increase as
  `Configuration.fontWeightAdjustment`. Canvas or custom-drawn text must
  select an available heavier weight (keep one bundled) and invalidate
  measurements when the setting changes while running. See
  [Android `Configuration`](https://developer.android.com/reference/android/content/res/Configuration#fontWeightAdjustment)
  and [Flutter text notes](flutter.md) for framework handling.

**Verify.** Run [X2](testing.md) with real fonts and native maximum settings;
inspect clipping and fading as well as reported overflow. Repeat with Bold
Text on at the largest size. Change text size and Bold Text with a detail,
dialog and editor open. Read every primary label and error
without shrinking it; ensure actions remain reachable under [L5–L7](layout.md).

## D2 Localised and long text — P1

**Rule.** Test actual shipped translations, expanded pseudolocalisation,
CJK, RTL and mixed-direction content. Text expansion is string-dependent;
no fixed percentage or one language is a reliable worst case.

**Traps.**

- Generated accessors catch missing identifiers, but may still allow missing
  translations to fall back. Add a locale-completeness check appropriate to
  the resource format and flag deliberate fallbacks explicitly.
- Concatenating translated fragments breaks word order, plurals and gender.
  Use the localisation system's complete messages, plural rules and named
  placeholders; avoid manually inserting Western digits or punctuation.
- Hard-coded left / right padding or double-mirrored arrows break RTL.
  Use leading / trailing geometry; mirror directional navigation, not logos,
  photos or every media symbol. Mixed-direction filenames, URLs and user
  content need the toolkit's bidi isolation. See [Android RTL guidance](https://developer.android.com/training/basics/supporting-devices/languages).
- Language, script and region are distinct: `zh-TW`, `zh-HK` and `zh-Hant`
  must resolve to the intended supported resources. Do not assume Android
  always includes or always omits a script subtag; test locale negotiation.
- Chinese / Japanese text can wrap without spaces; Arabic joining,
  combining marks and fallback glyphs need real shaping. A CI font that
  renders replacement boxes is not layout evidence.
- Android 15+ with target 35+ defaults `TextView.elegantTextHeight` to true;
  Android 16+ with target 36+ ignores the attribute. Allow taller script metrics
  instead of forcing the old height. See [Android 16 font behavior](https://developer.android.com/about/versions/16/behavior-changes-16).
- Permission purpose strings are bundle resources, not automatically the
  app's UI translations: localise `InfoPlist.strings` or `InfoPlist.xcstrings`
  and inspect the built app. See [Apple protected-resource strings](https://developer.apple.com/documentation/uikit/requesting-access-to-protected-resources)
  and [P1](permissions.md).
- Notification channel names, tray tooltips and other strings outside the
  view tree stay stale after a locale change unless updated through their
  platform API. Respect system / user ownership of those surfaces.

**Verify.** Render the longest actual strings, pseudolocalisation, Arabic
with embedded numbers / URLs, CJK and an unbroken filename. Switch app
language while running or resume after changing it in Settings. Inspect
system prompts and platform surfaces separately from the app screens.

## D3 Pixel density — P0

**Rule.** Lay out in logical units (pt / dp / framework logical pixels), and
allocate raster surfaces in physical pixels. Provide appropriately sized
assets or supported vectors; an individual raster file for every possible
scale is not universally required.

| Platform | Density / resource handling |
|---|---|
| iOS / iPadOS | Asset catalogs select applicable scales, commonly @2x / @3x on current devices. Keep @1x when the supported target needs it; it is not a special rule for legacy iPad alone. |
| Android | Primary buckets: ldpi 0.75×, mdpi 1×, hdpi 1.5×, xhdpi 2×, xxhdpi 3×, xxxhdpi 4×. Runtime density can fall between buckets; Android scales the selected resource. `nodpi` disables resource density scaling. |
| macOS | Common backing scales are 1× / 2×. Read the window's backing conversion; display resolution modes are not a universal promise about the app's render / downsample pipeline. |
| Windows | Per-monitor scale can be fractional (for example 125 / 150 / 175 %); do not treat a fixed list of settings as exhaustive. |
| Linux | Behavior depends on compositor, toolkit and X11 / Wayland backend. Test the shipped combinations, including XWayland if supported; neither backend implies universal fractional-scaling support. |

See [Android densities](https://developer.android.com/training/multiscreen/screendensities),
[Apple window backing scale](https://developer.apple.com/documentation/appkit/nswindow/backingscalefactor)
and [Qt's platform DPI notes](https://doc.qt.io/qt-6/highdpi.html).

**Traps.**

- A logical 1-unit line is not necessarily one physical pixel. For intentional
  hairlines, align both position and stroke coverage in physical space;
  vectors alone do not fix fractional-position blur.
- Windows desktop apps need a DPI-awareness mode supported by their toolkit,
  preferably Per-Monitor V2 for compatible Win32 apps. Declare it through
  the toolkit / manifest before creating windows; do not unconditionally
  override a framework's process DPI mode afterward. See [Windows DPI awareness](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows).
- Raster caches and custom canvas / GPU buffers use logical dimensions and
  look soft, or apply device scaling twice and consume excess memory. Size
  them for their destination scale; see [M5](media-devices.md).
- Native / plugin pointer events, captures and view geometry may use different
  coordinate units. Check each API's contract and convert consistently for
  hit testing, crops and overlays; do not multiply all input by scale blindly.
- A native Android vector drawable is not an arbitrary SVG; convert / test
  unsupported vector features in the actual renderer.

**Verify.** Inspect icons, text, borders and canvas hit testing at 1×, 2×,
3× and supported fractional scales, including 125 / 150 / 175 %. Compare
logical bounds and actual raster dimensions; check a packaged release so
resource qualifiers and asset selection are exercised.

## D4 Scale changes at runtime — P1

**Rule.** Scale is window-specific and can change while running. Recreate
scale-dependent raster resources and update geometry without losing state.
Two open windows may have different effective scales at the same time.

**Traps.**

- A process-global scale cached at launch makes a second window blurry or
  breaks its pointer coordinates on another monitor.
- A Win32 runner ignores `WM_DPICHANGED` or its suggested window rectangle;
  an AppKit view ignores backing-property changes. Use framework hooks, or
  the relevant [Windows notification](https://learn.microsoft.com/en-us/windows/win32/hidpi/wm-dpichanged)
  / [AppKit backing notification](https://developer.apple.com/documentation/appkit/nswindow/didchangebackingpropertiesnotification).
- Drag images, menus, tooltips, web views and native child windows retain
  stale scale even though the main window is sharp.
- Changing Android display size / density can recreate the Activity.
  Relayout and state restoration both matter; see [L3](layout.md).
- Display removal or a remote-session scale change leaves pixel-sized
  resources stale. Handle the current target display, not only initial docking.

**Verify.** Move an open editor and popover between differently scaled
monitors, then change scale in Settings and dock / undock. Test two windows
at once. Verify sharpness, caret position, hit testing and retained drafts.
A simulated scale tests rendering but does not prove monitor-transition
behavior; record the distinction under [X4](testing.md).

## D5 Platform icons and launch assets — P1; required launch configuration P0

**Rule.** Export and inspect each platform surface independently. Source
artwork can be shared, but launcher, taskbar, tray, notification and launch
assets have different masks, sizes and appearance rules.

| Asset | Rule / failure prevented |
|---|---|
| Apple app icons | Current layered icons use Icon Composer and system-applied effects. Follow current templates and preview all supported appearances; retain compatible catalog assets for older OS versions. For legacy flattened iOS icon submissions, keep the final square opaque and let the system mask it. A blanket no-alpha rule does not describe layered foreground artwork. |
| macOS app icon | Use the current Apple template / Icon Composer output, with legacy fallbacks where needed. Do not hard-code a Big Sur-era artwork inset as an enduring OS requirement. |
| macOS menu-bar icon | Use `NSImage.isTemplate` for monochrome artwork that should be system-tinted; preserve intentional color artwork where appropriate. Check selected and disabled states too. |
| Android launcher | Adaptive foreground / background icons are supported from Android 8.0/API 26; keep required legacy fallbacks. Provide a monochrome layer for themed launchers on Android 13+ and test several masks. Android 16 QPR2+ can auto-theme icons without that layer; preview the result rather than depending on its quality. Keep essential artwork within the documented safe zone. |
| Android notification small icon | Supply the dedicated monochrome silhouette with transparent background; Android uses its alpha mask. A full-color launcher bitmap can become a solid block. Verify release shrinking retains dynamically referenced resources; notification behavior belongs to [M6](media-devices.md). |
| Windows | Supply sizes for small / large shell and taskbar surfaces, using multi-image ICO or the package's required assets. `Shell_NotifyIcon` takes an `HICON`; it does not require that the source file be ICO rather than a bitmap decoded by the framework. |
| Linux | Install a correctly named icon in `hicolor` and match the desktop entry's `Icon` name. Include a PNG fallback when relying on optional SVG support; window / taskbar association must match the app's identity. Integration belongs to [W4](desktop.md). |
| Launch / splash | Match first-frame layout and light / dark appearance. For uploads built with the iOS 27 SDK+, App Store Connect requires launch configuration via `UILaunchStoryboardName`, `UILaunchStoryboards`, `UILaunchScreen` or `UILaunchScreens`. Do not rely on legacy launch images alone. |

Sources: [Apple icon design](https://developer.apple.com/design/human-interface-guidelines/app-icons),
[Icon Composer](https://developer.apple.com/icon-composer/),
[template images](https://developer.apple.com/documentation/appkit/nsimage/istemplate),
[Android adaptive icons](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive),
[notification icons](https://developer.android.com/develop/ui/compose/notifications/create-notification),
[Windows notification-area icons](https://learn.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataw),
[freedesktop icon theme specification](https://specifications.freedesktop.org/icon-theme/)
and [Apple launch-screen submission rule](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements).

**Traps.** Transparent edges exported with the wrong alpha convention or
matte leave halos. Keep the decoder / renderer's premultiplication contract
consistent; inspect the same asset on light and dark backgrounds. Launchers
and system surfaces may cache assets, so hot reload is insufficient evidence.

**Verify.** Inspect installed release icons in the launcher, app switcher,
Dock / taskbar, tray / menu bar and a real notification. Check small sizes,
several masks and light / dark / themed appearances. Cold-launch a fresh
install in both themes and inspect the final plist / packaged assets.

## D6 Theme and contrast — P1

**Rule.** Follow system appearance by default, allow a deliberate app
preference where appropriate, and update open windows and overlays when the
setting changes. Use semantic colors with a tested high-contrast fallback.

**Traps.**

- Text uses a semantic foreground on a hard-coded background, or transparent
  chrome changes contrast over images. Measure the composited result.
- Use WCAG AA as an explicit test baseline: ordinary text 4.5:1, qualifying
  large text 3:1, and necessary control / state graphics 3:1 against adjacent
  colors. WCAG defines exceptions; these are not blanket app-store rules.
  See [text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
  and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
- Status and selection are conveyed only by color. Add text, shape, icon
  or another distinguishable cue, and expose the state under [I5](input.md).
- Windows contrast themes, Apple Increase Contrast / Reduce Transparency,
  or web-content forced colors remove a custom focus ring or boundary.
  Use system colors and an opaque fallback where needed.
- System bars, native dialogs and embedded web content remain in the old
  theme after only the main view updates.
- Colour filters, greyscale and inversion erase a colour-only distinction
  that passed review in normal colour: red / green status, a coloured
  selection, chart series. These filters apply system-wide, so the app
  cannot rely on hue; the redundant cue from the colour-alone trap above
  must survive them. Apple's
  [`UIAccessibility.isGrayscaleEnabled`](https://developer.apple.com/documentation/uikit/uiaccessibility/isgrayscaleenabled)
  reports the grayscale preference; do not infer general colour-filter
  coverage from that Boolean. Differentiate Without Color is a separate
  setting. Under Smart Invert,
  photos, video and similar content can opt out with
  [`accessibilityIgnoresInvertColors`](https://developer.apple.com/documentation/uikit/uiview/accessibilityignoresinvertcolors).
  Android has colour correction, greyscale and colour inversion; see
  [Android display settings](https://support.google.com/accessibility/android/answer/11183305).
  Windows 11 has colour filters in its accessibility settings.

**Verify.** Measure secondary text, errors, selection, focus and disabled
states in both themes and over realistic content. Toggle appearance and
contrast settings with dialogs open; inspect native and web surfaces too.
Run the main flows under greyscale and one red / green filter (Apple Color
Filters, Android colour correction, Windows colour filters) and with colour
inversion; every state and chart must stay distinguishable, and under
Apple Smart Invert photos and video must not appear inverted (Android's
inversion applies to everything, media included). See
[Apple display settings](https://support.apple.com/en-us/111773)
and the [Apple accessibility testing guide](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app).

## D7 Reduced motion and animated content — P1

**Rule.** Honor reduced-motion / animation preferences without hiding
information or preventing completion of an action. Prefer a static state or
subtle transition when large movement, parallax or zoom is unnecessary.

**Traps.**

- Only native transitions honor the setting; custom canvas animations,
  skeleton shimmer and animated backgrounds keep moving. Observe changes
  while running, including UIKit's [Reduce Motion setting](https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled)
  and web content's [`prefers-reduced-motion`](https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion).
- Code commits navigation or enables a button only after an animation that
  is disabled or cancelled. Final state must be correct with zero duration.
- Essential progress disappears when an animation is removed. Preserve
  a static status and the accessibility announcement under [I5](input.md).
- Own custom pulse / flash timers as well as animation controllers. On a
  live preference change, stop repeated motion, retain static feedback and
  preserve any independent operation deadline; do not restart or strand it.
  Cancel pending callbacks at disposal and handle a late feedback request
  safely. Completion and repeated visual motion may need separate timers.
- Auto-scrolling / animated content cannot be paused, or flashes rapidly.
  Review applicable [pause / stop / hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
  and [flash thresholds](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html)
  rather than treating reduced motion alone as protection.

**Verify.** Toggle reduced motion / animation settings during navigation,
loading and scrolling. Disable animations entirely where supported. Confirm
that completion, focus return, progress and cancellation still work, and
that custom / embedded animations follow the selected preference.
