# Remotion Motion Parameters

Use this reference when the user wants Remotion-ready output, animation parameters, frame timing, easing, Smart Zoom, cursor behavior, or implementation guidance. Default to `fps = 30`.

Use `<Sequence>` or `<Series>` for simple scene timing. Use `<TransitionSeries>` from `@remotion/transitions` when scene transitions should overlap. Transitions shorten total duration because adjacent scenes play simultaneously during the transition.

## Defaults

```text
fps: 30
composition: 1920x1080 unless another format is requested
microInteraction: 6-12 frames
sceneTransition: 12-24 frames
logoReveal: 24-36 frames
textReveal: 12-24 frames per phrase
uiPanelEntrance: 18-30 frames
aiScanOrExtract: 24-45 frames
successHold: 45-75 frames
brandEndHold: 60-90 frames
```

## Easing Presets

| Preset | Remotion easing | Use for |
|---|---|---|
| `uiOut` | `Easing.bezier(0.16, 1, 0.3, 1)` | Crisp UI entrances, cards, panels, cursor-guided reveals. |
| `editorialInOut` | `Easing.bezier(0.45, 0, 0.55, 1)` | Slow fades, value text, brand outro. |
| `pop` | `Easing.bezier(0.34, 1.56, 0.64, 1)` | Logo accent, status badge pop, final checkmark. Use sparingly. |
| `exitIn` | `Easing.in(Easing.cubic)` | Elements leaving before a cut. |
| `linear` | `Easing.linear` | Progress rings, scans, loading paths. |

Always clamp interpolations:

```tsx
const progress = interpolate(frame, [start, end], [0, 1], {
  easing: Easing.bezier(0.16, 1, 0.3, 1),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

## Smart Zoom Rules

Use Smart Zoom when the viewer needs to read or understand a specific UI area while preserving context.

| Use case | Scale | Notes |
|---|---|---|
| Light guidance | `1.2x-1.3x` | Cursor follow, gentle area focus. The viewer should barely notice the zoom. |
| Standard feature explanation | `1.3x-1.5x` | Button clicks, feature panels, normal product walkthrough beats. This is the safest range. |
| Key operation emphasis | `1.5x-1.8x` | Important input fields, primary CTA, complex detail. Use when the viewer must notice the action. |
| Extreme detail | `2.0x+` | Avoid by default. Only use for tiny code, dense data, or very small UI. Risk: lost context and cheap-looking magnification. |

Universal formula:

```text
default follow: 1.25x
click emphasis: 1.4x
key focus: 1.6x
maximum normal demo zoom: 1.8x
```

Dynamic zoom:

```text
mouse moves -> gentle follow at ~1.2x
click starts -> quick push to ~1.4x
viewer reads -> settle back slightly, e.g. 1.4x -> 1.32x
next action -> pan or zoom to next focus target
```

Focus lock:

- Lock zoom center to the cursor or the active UI element.
- Do not zoom into empty space or leave the target off-center.
- Preserve enough surrounding UI to keep orientation.
- Prefer smooth x/y camera movement over recentering with a visible jump.

Comfort target:

```text
If target occupies <10% of frame, zoom until it occupies roughly 20-30%.
If target occupies 10-25% of frame, zoom until it occupies roughly 30-40%.
If target already occupies ~40% of frame, do not zoom; use highlight or cursor motion instead.
```

Use 9-18 frames at 30fps for zoom-in (`0.3s-0.6s`). Use `uiOut` easing by default.

## Cursor / Pointer Rules

Use the cursor as an attention guide, not as a decoration. The cursor should show user intent before the UI changes.

```text
desktop pointer size: 28-44px at 1920x1080
cursor move: 12-30 frames for short moves, 30-45 frames for long moves
hover pre-hold: 6-12 frames
click down/up: 4-8 frames
post-click hold: 8-15 frames before the next major UI state
```

Motion behavior:

- Move the pointer before the UI responds.
- Use curved or slightly eased paths for long moves; avoid perfectly linear mechanical travel.
- Use `uiOut` easing for pointer arrival and `linear` only for very short direct moves.
- Slow down near the target element.
- Pair cursor movement with Smart Zoom when the target is small: cursor leads, camera follows.
- Keep pointer speed consistent with distance.

Click and hover:

- Hover: target receives a subtle state change before click, such as tint, outline, shadow, or tooltip.
- Click: cursor scales `1 -> 0.92 -> 1` or the button depresses for 4-8 frames.
- After click: hold briefly so the viewer registers causality, then reveal the new state.
- For important actions, add a small ripple, pulse, or button glow under 12 frames.
- Avoid repeated click ripples on routine actions.

Readability:

- Do not let the cursor cover the exact text or number the viewer must read.
- Move the cursor away if a tooltip, label, or result appears underneath.
- When showing typed input, either hide the cursor or park it outside the text field after the click.
- Use cursor opacity reduction or removal during dense reading moments if it distracts.

Storyboard wording:

```text
Cursor glides to the primary button, button hover state appears, click depresses for 6 frames, then the generated result panel opens.
Cursor leads the camera toward the metric card; Smart Zoom settles at 1.35x as the card highlight appears.
Pointer clicks into the input, moves aside, typed text appears with a short caret animation.
```

## Property Ranges

| Element | Property range |
|---|---|
| Text reveal | opacity `0 -> 1`, y `12 -> 0`, blur `8 -> 0px` |
| UI panel entrance | opacity `0 -> 1`, scale `0.96 -> 1`, y `24 -> 0` |
| Floating card | scale `0.92 -> 1`, y `20 -> 0`, shadow increases subtly; avoid rotation for text-heavy cards |
| Cursor move | x/y linear or `uiOut`, click scale `1 -> 0.92 -> 1` over 6-10 frames |
| Field highlight | border opacity `0 -> 1`, background tint `0 -> 8%`, hold 20-40 frames |
| AI scan | mask/gradient x `-20% -> 120%`, opacity peak in middle; use only for extraction/status progress |
| Status badge | text swap on cut, badge scale `0.9 -> 1`, optional `pop` easing |
| Success check | progress ring `0 -> 100%` over 24-36 frames, checkmark draw 10-18 frames |
| Smart zoom camera | scale `1.2 -> 1.4` for normal focus, up to `1.6-1.8` for key operations, duration 9-18 frames |
| Cinematic camera move | translate max `24-80px`, scale max `1.04` when not doing Smart Zoom, avoid fast rotations on text-heavy shots |

Static perspective rule:

```text
Do not apply perspective/rotateX/rotateZ to a product screen as a static style.
Use flat UI for reading. Use perspective only during a deliberate camera move
and keep text-heavy product surfaces readable.
```

## Layered UI Implementation Rules

Use layered UI when product operation precision matters:

- Recreate the product screen as React components with shared layout constants for cards, rows, buttons, captions, and focus states.
- Attach focus boxes to component coordinates, not screenshot pixels. Use the same x/y/width/height source as the target UI element.
- Keep focus padding consistent: 8-16px for buttons/cards, 16-28px for sections.
- Put callouts outside dense UI when they are explanatory; put them inside the product surface only when they represent a real product object.
- Verify 3-5 key frames per scene after rendering. Check focus alignment, overlay collisions, caption readability, and cursor coverage.
- If an overlay covers important text, move the camera, reduce the overlay, split the scene, or convert the overlay into a side panel.

## Transition Parameter Map

| Story transition | Remotion implementation |
|---|---|
| Text-to-UI reveal | `<Sequence>` overlap or `fade()` transition, 12-18 frames |
| Match cut | End scene A and start scene B with same card coordinates; no heavy transition needed |
| Card morph | Shared component with interpolated size/position, 18-30 frames |
| Cursor-led cut | Trigger next scene 3-6 frames after click-down |
| Status-change cut | Text/status changes on a hard cut, badge pop 8-12 frames |
| Light/dark contrast cut | `fade()` or `wipe()`, 15-24 frames |
| Processing scan | Overlay component for 12-24 frames; use only over the element being processed and do not obscure UI text |
| Hold/fade to brand | `fade()`, 18-30 frames, then brand hold 60-90 frames |

## Timeline Output Example

```text
fps: 30
duration: 1440 frames / 48s

PainPointIntro        0-144f     textReveal 18f, backgroundCards drift
ProductReveal         144-234f   logoReveal 30f, subtitle fade 18f
InputScene            234-435f   uiPanelEntrance 24f, cursor-led action 8f
AITransformScene      435-660f   cardMorph 24f, aiScan 36f, fieldHighlights stagger 8f
ReviewScene           660-1020f  dashboard push-in, field focus 24f
ApprovalScene         1020-1230f cursor click, approver rows stagger 10f each
SuccessScene          1230-1320f progressRing 30f, checkmark 12f, hold
ValueOutro            1320-1440f value text fade stagger 18f
```

If code is requested, prefer normalized progress values and derive multiple properties from them instead of duplicating timing logic.
