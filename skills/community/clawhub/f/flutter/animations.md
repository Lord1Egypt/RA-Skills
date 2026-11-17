# Animations — Implicit, Explicit, and Transitions

Choose the weakest mechanism that expresses the motion. Every rung up adds a lifetime you now own.

| Need | Use | Owns |
|---|---|---|
| A property changes and should ease to its new value | `AnimatedContainer`, `AnimatedOpacity`, `AnimatedAlign`, `AnimatedPadding` | Nothing — the widget owns the controller |
| Any single value, animated implicitly | `TweenAnimationBuilder` | Nothing |
| Swap one child for another with a transition | `AnimatedSwitcher` | Nothing; requires differing keys |
| One driver, several animated properties or widgets | `AnimationController` + `FadeTransition`/`SlideTransition`/`ScaleTransition` | A controller and a ticker |
| Animation that must reverse, repeat, or be scrubbed | `AnimationController` with explicit `forward`/`reverse`/`repeat` | A controller and a ticker |
| Shared element across routes | `Hero` | Nothing; requires matching tags |
| Physics-driven (fling, spring, drag release) | `AnimationController.animateWith` + a simulation | A controller |
| List insert and remove | `AnimatedList` / `SliverAnimatedList` | Stable keys and a removal builder |
| Anything else | An implicit widget first; escalate only when it cannot express it | — |

## Implicit Animations

- They animate when the VALUE changes between builds. Passing the same value, or rebuilding with a `const` widget, animates nothing — this is why "my AnimatedContainer doesn't animate" is nearly always a state problem, not an animation problem.
- `duration` is required; `curve` defaults to linear, which reads as mechanical. `Curves.easeOut` for entering, `Curves.easeIn` for exiting, `Curves.easeInOut` for a change in place.
- `AnimatedSwitcher` decides "is this a new child" by key. Two `Text` widgets with different strings and no keys are the same widget type at the same position, so nothing transitions — give each a `ValueKey(text)`.
- `AnimatedContainer` cannot animate between decorations of different shapes (a `BoxDecoration` and a `ShapeDecoration`); it snaps instead. Keep the decoration type constant across states.
- `TweenAnimationBuilder` covers everything the named widgets miss: any `Tween`, any value, still with no controller to dispose.

## Explicit Animations

```dart
class _S extends State<X> with SingleTickerProviderStateMixin {
  late final _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 300));
  late final _fade = CurvedAnimation(parent: _c, curve: Curves.easeOut);
  @override void dispose() { _c.dispose(); super.dispose(); }   // SKILL.md rule 3
}
```

- `SingleTickerProviderStateMixin` for one controller, `TickerProviderStateMixin` for several. Using the plural form for one controller is harmless; using the singular for two throws.
- A `Ticker` fires every frame while the controller runs. An undisposed controller keeps ticking after the widget is gone and Flutter reports "A Ticker was started and is still running" in debug — treat that message as a leak, not a warning.
- `CurvedAnimation` created without being disposed holds a listener on the parent; dispose it too when the controller outlives it.
- **`AnimatedBuilder`'s `child:` is the whole point.** Everything inside the builder closure rebuilds every frame — 60 or 120 times per second. Anything static goes in `child` and is built once (Rebuild Scope Ladder rung 2). The same applies to `ValueListenableBuilder` and every `*Transition` widget.
- Prefer a `*Transition` widget over `AnimatedBuilder` + `setState`: transitions rebuild nothing, they only re-paint.
- Staggering: one controller, several `Interval` curves — `CurvedAnimation(parent: c, curve: Interval(0.0, 0.5, curve: Curves.easeOut))`. Multiple controllers for one visual sequence drift out of sync.
- `TickerMode` is what pauses animations in an off-screen route; a manual `Timer`-driven "animation" ignores it and keeps burning frames behind the current screen.

## Hero and Route Transitions

- `Hero` requires the same `tag` on both routes. A tag repeated twice on the same screen throws "There are multiple heroes that share the same tag".
- Hero flights are built from a snapshot: a hero whose child depends on `MediaQuery` or a provider can flash mid-flight. Keep the hero child simple, and use `flightShuttleBuilder` when it must change during the flight.
- Heroes across nested navigators need the flight to happen on the navigator that owns both routes (`navigation.md`).
- Custom route transitions come from `PageRouteBuilder(transitionsBuilder:)`. Building one loses the platform-adaptive defaults, including the iOS swipe-back gesture — re-add it deliberately (`adaptive.md`).
- `PageTransitionsTheme` sets transitions app-wide per platform; that beats overriding the transition on every route.

## Performance of Motion

- An animation that drops frames is a raster-thread problem more often than a UI-thread one: check for `Opacity`, clipping, shadows, and `BackdropFilter` inside the animating subtree (`performance.md`).
- Wrap the animating subtree in a `RepaintBoundary` so the static background does not repaint with it — this is one of the few places a boundary always pays for itself.
- Animating layout properties (width, padding, position in a flex) forces a layout pass on every frame; animating transform, opacity, or color only repaints. Prefer `SlideTransition`/`ScaleTransition` over animating `Padding` or `Positioned` when the visual result is the same.
- Implicit animations on many list items at once means many controllers ticking simultaneously — stagger them or animate the container instead.
- Lottie and Rive files can be arbitrarily expensive; measure them like any other widget, and prefer a designer-optimized export over a scaled-down large one.

## Motion and Accessibility

- `MediaQuery.disableAnimationsOf(context)` reports the OS "reduce motion" setting. Respect it: replace slides and scales with a cross-fade or an immediate change, and never gate content behind an animation that may not play (`accessibility.md`).
- Duration discipline: short interface feedback in the low hundreds of milliseconds, longer for full-screen transitions. Anything past roughly half a second reads as sluggish in a tap-driven interface; match the platform's own transitions rather than inventing timings.
- An infinitely repeating animation (`controller.repeat()`) makes `pumpAndSettle` never settle in tests — this is the number-one cause of a hanging widget test (`testing.md`).
