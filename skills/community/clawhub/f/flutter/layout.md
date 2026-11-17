# Layout — Constraints, Flex, Overflow, and Slivers

One rule generates every layout behavior and every layout exception: **constraints go down, sizes go up, the parent sets position** (SKILL.md rule 1). A widget never picks its size in a vacuum; it picks a size the incoming `BoxConstraints` allow, and the parent then decides where that box lands.

## Reading Constraints

- Print them where the confusion is: `LayoutBuilder(builder: (context, c) { debugPrint('$c'); ... })` shows the exact `BoxConstraints(minW, maxW, minH, maxH)` arriving at that point. This beats any amount of reasoning about who is squeezing whom.
- **Tight** (`min == max`) means the child has no choice — it will be that size even if it asks for another. A `SizedBox(width: 100, height: 100)` passes tight constraints down.
- **Loose** (`min == 0`) means "up to max". `Center` and `Align` loosen the constraints they received, which is why a `Container(color:)` fills the screen alone but shrinks to nothing inside a `Center`.
- **Unbounded** (`max == double.infinity`) means "as much as you want" — and a widget that wants everything (`Expanded`, `double.infinity`, an unconstrained `ListView`) then has no answer. This is the source of most layout crashes.
- Where unbounded constraints come from, exhaustively: the main axis of a `Column`/`Row` inside a scrollable, the scroll axis of any scrollable, `UnconstrainedBox`, `OverflowBox`, `SingleChildScrollView`, `IntrinsicWidth`/`IntrinsicHeight` measurement passes, and a `Stack`'s non-positioned children under a loose parent.

## Row and Column

- Cross axis first: `crossAxisAlignment: CrossAxisAlignment.stretch` gives children tight cross-axis constraints; the default `center` gives them loose ones. A `Column` child that "won't go full width" is usually this, not a width bug.
- Main axis: a `Column` is as tall as its children by default (`MainAxisSize.max` still means "as tall as the incoming max, if bounded"). Inside a scrollable, `MainAxisSize.max` under unbounded height is what triggers `BoxConstraints forces an infinite height`.
- `Expanded` = `Flexible(fit: FlexFit.tight)`: takes exactly its share. `Flexible` alone (`FlexFit.loose`) lets the child be smaller than its share. Use `Flexible` for text that may be short, `Expanded` for panes that must fill.
- `flex:` values are ratios of the REMAINING space after non-flex children are laid out — not of the total. Two children at `flex: 1` and `flex: 2` beside a fixed 100 px sibling split `(width − 100)` as 1:2.
- `Spacer()` is `Expanded(child: SizedBox.shrink())`. In a scrollable axis it throws for the same unbounded reason.
- Long text inside a `Row` overflows because text asks for its natural width: wrap it in `Expanded` or `Flexible`, then set `overflow: TextOverflow.ellipsis` on the `Text` itself. Doing only the second does nothing — the `Text` still receives unbounded width.

## The Overflow Message

`A RenderFlex overflowed by N pixels` is a debug-only diagnostic (the yellow-black stripes never ship). Decide which of three cases you have:

| Case | Signal | Fix |
|---|---|---|
| Content is legitimately taller than the screen | Overflow grows with more items or with larger text | Make the axis scrollable (`SingleChildScrollView`, or a `ListView`) |
| One child wants more than its share | Overflow is stable, one child is a text or an image | `Expanded`/`Flexible` on that child |
| The keyboard shrank the viewport | Overflow appears only when a field is focused | `SingleChildScrollView` + `resizeToAvoidBottomInset` (`forms.md`) |

`SingleChildScrollView` + `Column` is the right answer for a form-shaped screen with a small, bounded number of children. For anything list-shaped it is the wrong answer: it builds all children eagerly.

## Nested Scrollables

- A `ListView` inside a `Column`: `Expanded` if it should take the leftover space; a `SizedBox(height:)` if it has a designed height; `shrinkWrap: true` only for a short, fixed list — it lays out every child on every scroll frame, so cost grows with item count.
- A `ListView` inside a `ListView` (same axis) is almost always a design error. Use one `CustomScrollView` with multiple slivers.
- `NestedScrollView` is for the collapsing-header pattern (a `SliverAppBar` above a `TabBarView`); it is not a general nesting mechanism and it has its own scroll-coordination bugs.
- Two scrollables that must move together: give them a shared `ScrollController` or link them with `ScrollControllerNotifier`-style listeners — never nest one to "sync" them.
- `physics: NeverScrollableScrollPhysics()` plus `shrinkWrap: true` is the correct combination for an inner list that should not scroll independently — and it is a strong hint that slivers are the right shape instead.

## Slivers

Reach for `CustomScrollView` the moment a screen mixes shapes in one scroll view.

| Need | Sliver |
|---|---|
| A plain widget in a sliver list | `SliverToBoxAdapter` |
| A list built lazily | `SliverList` + `SliverChildBuilderDelegate` |
| A grid built lazily | `SliverGrid` |
| An app bar that collapses or floats | `SliverAppBar` (`pinned`, `floating`, `snap`) |
| A header that sticks between sections | `SliverPersistentHeader` with a delegate |
| Padding around a sliver | `SliverPadding` — a plain `Padding` breaks the sliver protocol |
| Fill the remaining viewport (empty states) | `SliverFillRemaining` |

- Slivers speak `SliverConstraints`, boxes speak `BoxConstraints`: mixing them without an adapter produces `A RenderSliver expected a child of type RenderSliver`.
- `SliverChildBuilderDelegate(childCount: n)` is what makes the list lazy — omit `childCount` and the delegate must be told when to stop by returning `null`.

## Stack and Positioned

- Non-positioned children are sized by the stack's `fit` (`loose` by default) and aligned by `alignment`. The stack's own size comes from its largest non-positioned child; a stack with only `Positioned` children collapses to zero unless the parent constrains it.
- `Positioned` must be a direct child of `Stack` — a `Padding` or `Align` in between produces `Incorrect use of ParentDataWidget`.
- Children painted outside the stack's bounds are visible but **not hittable**: a button drawn half-outside receives no taps in the outside half. `clipBehavior: Clip.none` changes the painting, not the hit test. Resize the stack instead.
- `Positioned.fill` inside a stack is how you get an overlay that matches the largest child.

## Intrinsics and Baselines

- `IntrinsicHeight`/`IntrinsicWidth` run a speculative layout pass to ask children "how big would you like to be" — the Flutter docs mark it as relatively expensive, and it can reach O(N²) when nested. Use it for equal-height cards in a `Row` when nothing else works, never inside a list item.
- `Table` and `IntrinsicColumnWidth` have the same cost profile with the same justification.
- `Baseline` and `CrossAxisAlignment.baseline` require `textBaseline:` to be set, or the layout asserts.

## Sizing Toolkit

| Need | Widget | Note |
|---|---|---|
| Exact size | `SizedBox` | Passes tight constraints down |
| Fill the parent | `SizedBox.expand` | Fails under unbounded constraints (nothing to expand into) |
| Aspect ratio | `AspectRatio` | Needs at least one bounded axis |
| Cap a size but allow smaller | `ConstrainedBox(maxWidth:)` | Applies only where the parent's constraints permit |
| Ignore the parent's constraints | `UnconstrainedBox` | Creates unbounded constraints for the child — usually a new bug |
| Scale a fixed-size widget to fit | `FittedBox` | Also scales text; verify against text scaling (`accessibility.md`) |
| Percentage of the parent | `FractionallySizedBox`, or `LayoutBuilder` | Percentage of the SCREEN is `MediaQuery.sizeOf` — different thing, and it ignores insets |
| Anything else | `LayoutBuilder` and print the constraints | The answer is always in the constraints that arrive |
