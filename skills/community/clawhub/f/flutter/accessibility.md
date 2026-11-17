# Accessibility — Semantics, Text Scaling, and Targets

Flutter paints to a canvas: the platform's screen reader sees nothing except the semantics tree the framework builds. Standard widgets populate it well; custom painting, custom gestures, and icon-only controls populate it not at all.

## Text Scaling Is a Layout Input

The user's system font size multiplies your text sizes. On both platforms the accessibility settings reach well beyond the default, and a design that only works at 1.0× is broken for a large group of real users.

- `MediaQuery.textScalerOf(context)` returns the current `TextScaler` (`flutter >=3.16`; it replaced the numeric `textScaleFactor`, which is why older snippets no longer compile).
- Fixed-height containers around text are the number-one scaling bug: the text grows, the box does not, and it clips or throws a `RenderFlex overflowed` (`layout.md`). Use intrinsic height or `minHeight` instead of a hard `height`.
- `maxLines` + `TextOverflow.ellipsis` prevents overflow and hides content; that is a real tradeoff for a title and unacceptable for an error message or a price. Let critical text wrap.
- Do not clamp scaling globally to "fix" the layout. If a specific surface genuinely cannot scale (a dense data table, a chart axis), clamp it there with a documented reason and provide another path to the same information.
- Test at the largest supported setting, not at 1.5×. Screens with a form, a dialog, and a bottom bar are where it breaks first.

## Tap Targets

- Material's minimum interactive dimension is 48 × 48 logical pixels; Apple's HIG specifies 44 × 44 points. A 24 px icon needs padding or an `IconButton`, which applies the minimum for you.
- `MaterialTapTargetSize.shrinkWrap` removes that guarantee — it exists for dense desktop layouts, not for a tighter phone design.
- The visual size and the hit area can differ: wrap a small visual in a larger `GestureDetector` with `behavior: HitTestBehavior.opaque`, or use `SizedBox` around the button.
- Adjacent targets need spacing, not just size: two 48 px buttons touching produce mis-taps at the boundary.
- Flutter's own widget tests can assert this: `meetsGuideline(androidTapTargetGuideline)` and `iOSTapTargetGuideline` (`testing.md`).

## The Semantics Tree

- Inspect it: `debugDumpSemanticsTree()`, DevTools' semantics view, or `SemanticsDebugger` as a widget wrapper. That is what a screen reader receives — read it before claiming a screen is accessible.
- `Semantics(label:, hint:, button:, ...)` annotates a subtree. `IconButton` and friends take a `tooltip`, which doubles as the semantic label; an `Icon` inside a bare `GestureDetector` announces nothing at all.
- `MergeSemantics` collapses a group into one node — right for a row that reads as a single item ("Price, 12 dollars"). `ExcludeSemantics` hides decoration from the reader.
- Images: `Image(semanticLabel:)` for meaningful images, and `ExcludeSemantics` for decorative ones. An unlabeled image is announced as nothing, which is the worst outcome for a photo that carries meaning.
- Live updates (a countdown, a validation result, an async completion) do not announce themselves. `SemanticsService.announce(message, textDirection)` speaks them, sparingly — an announcement per keystroke makes a form unusable.
- Custom painting is a blank rectangle to the reader. Wrap a `CustomPaint` chart in a `Semantics` node with a text summary, or provide a data table alternative.

## Order and Focus

- Reading order follows the widget tree and the visual position Flutter derives from it, which is why a `Stack`-based layout can read in an order nobody expects. Verify with the semantics tree, and reorder with `Semantics(sortKey: OrdinalSortKey(n))` when the tree cannot be restructured.
- Keyboard focus and screen-reader focus are different systems. Keyboard traversal matters on web and desktop (`adaptive.md`); `FocusTraversalGroup` groups a region so Tab moves through it coherently.
- When a dialog or sheet opens, focus must move into it and be trapped there until it closes — otherwise the reader keeps walking the page behind it.
- After an action that changes the page (a filter applied, a step completed), move or announce focus. Silence is indistinguishable from a failed tap.

## Color and Contrast

- WCAG 2 level AA requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text (18 pt, or 14 pt bold) and for meaningful UI components. Check the pairs your theme actually renders, in both light and dark.
- Color must never be the only signal: an error field needs an icon or text, a chart series needs a label or a pattern, a status dot needs a word.
- `MediaQuery.highContrastOf(context)` reports the OS high-contrast setting; provide a stronger palette rather than ignoring it.
- Dark mode is not a contrast strategy. Pure black text on pure white and pure white on pure black both fail comfort tests before they fail ratios — check the ratio on the actual theme colors.

## Motion and Timing

- `MediaQuery.disableAnimationsOf(context)` reflects "reduce motion". Honor it by cross-fading or cutting instead of sliding, and never make content unreachable until an animation ends (`animations.md`).
- Auto-advancing carousels, toasts that vanish, and timed dialogs are all barriers. Provide a pause or a persistent path to the same content.
- A snackbar is not an accessible error report: it is transient and often unannounced. Attach errors to the field or the region they belong to (`forms.md`).

## Making It Stick

- Add the checks to the test suite once and they stop regressing: `expect(tester, meetsGuideline(textContrastGuideline))`, plus the tap-target guidelines and `labeledTapTargetGuideline` (`testing.md`).
- Every icon-only control gets a label at the moment it is written — retrofitting labels across a shipped app is an order of magnitude more work.
- A screen counts as verified when it has been driven end to end with the platform's own screen reader (TalkBack, VoiceOver). The semantics tree tells you what exists; only the reader tells you whether it makes sense.
