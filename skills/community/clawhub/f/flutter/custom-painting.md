# Custom Painting — CustomPainter, Canvas, and Custom RenderObjects

Reach for painting when composition genuinely cannot express the visual: charts, gauges, signatures, waveforms, connectors between nodes, decorative backgrounds. Reach for it too early and you have replaced accessible, testable widgets with a rectangle nobody can inspect.

## The Escalation Ladder

1. **Existing widgets.** A ring is a `CircularProgressIndicator`; a dashed border is a `DecoratedBox` with a border image; a gradient is a `BoxDecoration`.
2. **`ShapeDecoration` with a custom `ShapeBorder`.** Custom outlines and clips that still participate in Material ink and elevation.
3. **`CustomPaint`.** Full drawing control inside a box someone else sized.
4. **`CustomPainter` on a `CustomPaint` with a `child`.** Paint behind or in front of a normal widget subtree.
5. **A custom `RenderObject`** (`RenderBox` via `SingleChildRenderObjectWidget`). Only when you need custom LAYOUT — sizing and positioning children by your own rules — not merely custom painting.

## CustomPainter Essentials

```dart
class RingPainter extends CustomPainter {
  RingPainter(this.progress, this.color);
  final double progress;
  final Color color;

  @override
  void paint(Canvas canvas, Size size) { /* draw within (0,0)-(size.width,size.height) */ }

  @override
  bool shouldRepaint(RingPainter old) => old.progress != progress || old.color != color;
}
```

- **`shouldRepaint` is the performance contract.** Returning `true` unconditionally repaints on every parent rebuild; returning `false` when a field changed leaves stale pixels on screen. Compare exactly the fields `paint` reads.
- The painter is given a `Size`, not constraints. `CustomPaint` sizes to its `child`, or to `size:` when there is none, or to zero if it has neither — the "my painter draws nothing" bug is usually a zero-size box (`layout.md`).
- The canvas is not clipped to `size` by default: drawing outside it bleeds over siblings. Set `Canvas.clipRect` or `CustomPaint(isComplex:)`-adjacent properties deliberately, and remember that painting outside the box is still not hit-testable (`widgets.md`).
- Coordinates are logical pixels with the origin at the top-left of the paint box. Nothing converts device pixels for you; `MediaQuery.devicePixelRatioOf` only matters when you rasterize to an image.
- Create `Paint`, `Path`, `TextPainter`, and `Shader` objects OUTSIDE `paint` when they do not depend on the animated value. Allocating them per frame is the most common cost in a slow painter.
- `shouldRebuildSemantics` and `semanticsBuilder` exist because a painted chart is invisible to a screen reader; supply a summary or a data alternative (`accessibility.md`).

## Canvas Operations Worth Knowing

| Need | Call | Note |
|---|---|---|
| Lines and outlines | `drawPath` with `PaintingStyle.stroke` | `strokeWidth` is centered on the path: a 2 px stroke on the edge shows 1 px |
| Filled shapes | `drawPath`/`drawRRect` with `PaintingStyle.fill` | Fill and stroke need two `Paint`s or two passes |
| Arcs and pie segments | `drawArc` | Angles are RADIANS and start at 3 o'clock, not 12 — subtract π/2 for a clock-style start |
| Text | `TextPainter(...)..layout()` then `paint` | `layout()` is mandatory; skipping it throws. Reuse the painter across frames |
| Gradients | `Paint()..shader = LinearGradient(...).createShader(rect)` | The shader is bound to that rect; recreate it when the size changes |
| Images | `drawImageRect` | Decode once and cache; decoding per frame is a guaranteed jank source (`performance.md`) |
| Grouping with opacity or a blend | `saveLayer` + `restore` | Allocates an offscreen buffer — the single most expensive canvas operation |
| Transform a subsection | `save`, `translate`/`rotate`/`scale`, draw, `restore` | Every `save` needs its `restore`, or subsequent drawing inherits the transform |
| Shadows | `drawShadow`, or `Path` + `MaskFilter.blur` | Blur cost scales with radius and area |

## Hit Testing a Painted Surface

- A `CustomPaint` receives pointer events as one rectangle. Pointing at a specific slice, node, or data point means doing the math yourself: convert the local position (`GestureDetector` gives you `localPosition`) and test against your own geometry.
- `Path.contains(offset)` answers "is this point inside this shape" — the direct way to hit-test irregular regions.
- `CustomPainter.hitTest(Offset)` lets the painter itself claim or reject a point, which is how you make transparent regions pass taps through to widgets below.
- For a handful of interactive regions, overlaying invisible positioned widgets is simpler and gets accessibility for free; for hundreds, do the math.

## Animating a Painter

- Drive it with an `AnimationController` passed to the painter through `repaint:` — `CustomPainter(repaint: animation)` repaints on every tick WITHOUT rebuilding the widget tree, which is strictly cheaper than rebuilding a `CustomPaint` inside an `AnimatedBuilder` (`animations.md`).
- Wrap the `CustomPaint` in a `RepaintBoundary` so the surrounding UI does not repaint with it (`performance.md`).
- Keep `paint` allocation-free on the animated path: precompute paths and reuse `Paint` objects; a per-frame `Path` build over thousands of points is what turns a chart into a slideshow.

## When You Need a Custom RenderObject

Painting is not layout. Write a `RenderBox` only when you must decide how children are SIZED or POSITIONED by rules no existing widget expresses — a radial menu, a tag flow with custom wrapping, a timeline aligning children to a shared axis.

- Implement `performLayout` (size yourself within `constraints`, lay out and position children), `paint`, and `hitTestChildren`. Getting `size` from anything but the constraints is the standard first mistake (SKILL.md rule 1).
- Call `markNeedsLayout` when a property changes geometry, `markNeedsPaint` when it only changes appearance. Calling the former for a color change discards a layout pass every frame.
- `MultiChildRenderObjectWidget` with a `ContainerRenderObjectMixin` is the pattern for multiple children; parent data holds each child's computed offset.
- Before committing: `Flow` and `CustomMultiChildLayout` solve many custom-positioning problems with far less code, and `Wrap`, `Stack`, and slivers cover more than most people assume (`layout.md`).

## Testing Painted Output

- Golden tests are the natural fit here — the pixels ARE the contract, which is exactly the case where goldens pay for themselves (`testing.md`).
- Unit-test the geometry separately: a function mapping data to points is testable without a canvas, and it is where the bugs actually live.
- Verify the painter at several sizes and both text scales; a chart hardcoded around one width breaks on a tablet (`adaptive.md`).
