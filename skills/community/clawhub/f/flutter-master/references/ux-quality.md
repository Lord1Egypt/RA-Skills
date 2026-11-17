# UX Quality: Accessibility, Localization, Responsiveness

## Accessibility (a11y)

- Interactive elements need semantic labels for screen readers — `Semantics(label: ...)` or, more often, the built-in labeling on `IconButton(tooltip: ...)`, `Text` (auto-labeled), etc. An icon-only button with no `tooltip`/label is invisible to a screen reader user.
- Tap targets should be at least 48x48 logical pixels (Material guideline) — flag custom-sized tappable widgets smaller than that.
- Check color contrast for text, especially custom theme colors — don't rely on "looks fine to me," since color-vision differences and low-light outdoor use both reduce effective contrast.
- Test with a screen reader occasionally (TalkBack on Android, VoiceOver on iOS) if the app has any accessibility requirement (increasingly a store/legal requirement for many app categories) — inspection alone misses real issues.
- Respect system text-scaling (`MediaQuery.textScaler`) — layouts that break or clip text when the user increases system font size are a common, easily-missed a11y failure. Test at larger text scale factors, not just default.

## Localization (i10n/l10n)

- Hardcoded UI strings scattered through widget code are a strong audit finding even for apps currently shipping only one language — retrofitting localization later means hunting down every literal string. Use Flutter's `intl`-based localization (`flutter gen-l10n` + `.arb` files) from early on if there's any chance of adding a language later.
- Don't just translate text — check date/number/currency formatting uses locale-aware formatting (`intl`'s `DateFormat`/`NumberFormat`), not hardcoded formats.
- Watch for layout assumptions that break under longer translated strings (German and Finnish text runs notably longer than English) or RTL languages (Arabic, Hebrew) if those are in scope — `Directionality`-aware widgets (`EdgeInsetsDirectional` instead of `EdgeInsets`) avoid this class of bug for free.

## Responsive / adaptive layout

- Don't hardcode pixel dimensions for layout that needs to work across phone/tablet/foldable/web — use `LayoutBuilder`, `MediaQuery`, or a breakpoints package to adapt.
- Distinguish *responsive* (same layout, fluidly resized) from *adaptive* (different layout per form factor, e.g. bottom nav on phone vs side rail on tablet) — know which one the app actually needs before recommending a solution.
- Test on at least one small phone and one tablet/large-screen size if the app targets both; layouts that "just work" on the developer's device often clip or overflow elsewhere. `RenderFlex overflowed` errors in logs are an easy, concrete flag to check for during an audit.

## Platform conventions

Flutter apps that visually match neither iOS nor Android conventions feel foreign to users on both platforms. Consider whether the app should adapt per-platform (Cupertino widgets on iOS, Material on Android) or intentionally use one consistent branded look everywhere — either is valid, but it should be a deliberate choice, not an accident of using whichever widget was first found in a tutorial.
