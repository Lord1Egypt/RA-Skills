# Remotion Layered UI Checklist

Use this checklist when implementing or reviewing an AI SaaS product demo as Remotion code, especially when the video rebuilds product UI as layers instead of animating screenshots.

## When To Use Layered UI

Use layered UI when the shot needs any of these:

- Precise focus boxes around buttons, rows, cards, charts, or side panels.
- Cursor movement, hover, click, typing, or drag behavior.
- Data animation: counters, bars, lines, status steps, generated fields.
- Foreground carry: a row, file, document, or result card lifting out of the UI.
- Camera movement that tracks a real product operation.
- Editable text and layout that must stay sharp in 1080p or 4K.

Screenshots are acceptable only for broad context, background texture, or a quick product establishing shot. Do not rely on screenshot overlays for precision-critical highlights.

## Component Structure

Build the screen from stable primitives:

```text
AppShell
Sidebar / TopBar
Card / Panel / TableRow
Button / Input / Tag / StatusBadge
FocusWrap / Pointer / Caption
KpiCard / Chart / ProgressStep
ForegroundCard / DocumentPreview / ApprovalOverlay
```

Rules:

- Store shared layout values close to the component that owns them: x/y/width/height, grid columns, row heights, card padding, border radius.
- Reuse those values for both the UI element and its focus state.
- Prefer props for state (`active`, `selected`, `progress`, `start`) over duplicate components for each animation state.
- Keep foreground objects as separate components with clear start/end frames.
- Use actual text layers for captions, UI labels, KPIs, and buttons; avoid raster text when possible.

## Focus Box Precision

Before using a focus outline, ask:

```text
Is this focus box attached to the target component's actual dimensions?
Would it still align if the card width, padding, or scale changes?
Does it highlight exactly one action or information group?
```

Implementation rules:

- Wrap the actual component with `FocusWrap` when possible.
- Use `inset: -pad` or component-relative padding, not hard-coded screenshot coordinates.
- Use 8-16px padding for buttons/cards and 16-28px for larger sections.
- Keep focus radius close to the target radius.
- Avoid drawing large rectangles over dense UI sections. Use camera zoom, dimming, or component-level focus instead.
- If the focus box is off by more than a few pixels in a rendered frame, fix the component layout or remove the focus box.

## Cursor / Pointer QA

Cursor motion should prove causality:

- Cursor appears before the UI changes.
- Hover state appears before click.
- Click response lasts 4-8 frames.
- New UI state appears 3-12 frames after click.
- Cursor does not cover the text, number, or button label the viewer must read.
- Cursor exits or fades during dense reading moments.
- Cursor and camera move toward the same active target.

Do not use the pointer as decoration. Every pointer entrance should imply an operation.

## Camera And Smart Zoom QA

For each camera move, write the target in plain language:

```text
Target: search input
Target: selected client row
Target: generated document preview
Target: +8.3% KPI
Target: send for approval button
```

Rules:

- No static perspective on text-heavy product UI.
- Use flat UI for reading and data inspection.
- Use cinematic push/pan only when it moves toward an active UI action.
- Use Smart Zoom when an active target occupies less than roughly 25% of the frame.
- Keep normal product camera scale subtle (`1.02x-1.09x`) unless doing Smart Zoom.
- Do not rotate dense tables, forms, dashboards, or documents.
- Stop or slow the camera when viewers need to read the result.

## Overlay And Foreground Card Safety

Foreground cards must represent real workflow objects:

- selected client
- uploaded file
- generated report
- extracted fields
- recommendation
- approval request
- completed status

Safety rules:

- Do not cover the next required line of product text.
- Do not stack a card inside another card unless it is a real modal or popover.
- If the underlying UI remains important, dim or blur it slightly and place the foreground object in open space.
- If there is no open space, split the shot, move the camera, or convert the overlay into a side panel.
- Let foreground cards enter with position/scale/opacity, not decorative rotation on text-heavy cards.

## Data Animation QA

Data should reveal the change, not just decorate the dashboard:

- Counters tween from old value to new value.
- Bars grow from zero or from previous state.
- Lines draw left-to-right.
- Status rows complete in sequence.
- Only one main data insight is emphasized at a time.
- The final value holds for at least 30-45 frames.
- Labels explain the changed value, not every metric on screen.
- Use real dashboard layouts when the product has them. Important analytics should be a main scene, not a small overlay, unless the overlay is only a transitional proof point.
- For line charts, use explicit chart constants: label gutter, plot left, plot right, baseline, x step, and tooltip anchor. Render-check the first and final points.

Avoid animating all metrics at once. It makes the dashboard feel busy and reduces comprehension.

## Brand And Asset Fidelity

Use real product assets whenever available:

- Import provided logos, icons, screenshots, or marks through Remotion assets instead of approximating recognizable brand marks with CSS.
- Reconstruct UI as layers for motion, but keep source colors, navigation labels, product terms, and typography close to the captured product.
- If an asset is missing or approximated, mark it as a temporary placeholder in notes and replace it before production export.
- Check rendered frames for missing logos, distorted aspect ratios, clipped marks, or placeholder blocks.

## Performance And Flicker QA

If preview playback flashes, stutters, or render time jumps:

- Remove heavy SVG filters such as large blurs/glows and replace them with simple secondary strokes, opacity, or box-shadow.
- Avoid stacking multiple full-screen translucent scenes. Fade or remove the outgoing scene before the incoming one becomes dominant.
- Prefer one opaque product page background for major page transitions.
- Keep large SVGs simple: gradients, paths, and basic strokes are usually fine; filter chains are the first thing to remove.
- Render a short final segment and compare file size/render time before adding more effects.

## Text And Caption QA

Captions should be shorter than the product action:

- 2-7 words for the main beat.
- One supporting line only when needed.
- Text appears just before or as the matching product action begins.
- Text fades or stays still during dense UI reading.
- Captions do not overlap the active UI target.
- Final benefit copy appears only after a visible result state.

If the caption explains a feature that the UI does not show, rewrite the shot or remove the caption.

## Rendered-Frame Check

Render stills before final video export. Minimum checks:

```text
opening hook
first product operation
AI transformation
data result
human approval/control
final value/outro
```

For each still, check:

- Focus target is precise.
- Cursor is visible only when useful.
- Overlay does not cover required text.
- Caption does not compete with UI.
- Data is readable.
- Chart gutters and terminal points are spaced correctly.
- Camera target is obvious.
- No decorative sweep/glow/tilt is carrying the shot.
- Brand marks are real assets or explicitly accepted placeholders.

If possible, also check one mid-transition frame for each important scene change.

## Remotion Implementation Habits

- Use clamped interpolations for all animated values.
- Derive several properties from one progress value when they belong to the same action.
- Keep scene timing constants named or grouped by scene.
- Render stills with the same composition, resolution, and browser used for final export.
- Use TypeScript checks before render.
- Copy final renders and key frames into the project output folder.
- Update the storyboard when the implemented motion changes.

## Final Pass

Before calling the demo done, answer yes to all:

```text
Can the viewer understand the workflow without reading dense UI?
Does each scene show a real product operation or state change?
Are focus boxes component-attached, not approximate screenshot boxes?
Are overlays purposeful and nonblocking?
Does camera motion have a target?
Are data changes progressively revealed and held?
Are analytics shown at the right scale for their importance?
Are chart labels, first points, final points, and tooltips non-overlapping?
Are real brand assets used where available?
Was flicker/stutter checked after removing heavy filters and stacked translucent layers?
Did rendered frames confirm the layout?
Were decorative effects removed unless they explain product state?
```
