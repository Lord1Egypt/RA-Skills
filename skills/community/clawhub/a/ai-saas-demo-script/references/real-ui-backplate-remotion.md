# Real UI Backplate Remotion Workflow

Use this reference when a product demo must stay visually faithful to a real website or app, but still needs cursor actions, focus rings, data animation, foreground carry cards, and HyperFrames-style motion.

## When To Use This Pattern

Use a real UI backplate when:

- The user says the UI must match the real website or product.
- A code recreation is visibly different in spacing, typography, sidebar density, tables, charts, cards, or active states.
- Cursor and selection boxes are drifting because they live in transformed containers.
- The demo needs real product trust more than fully editable UI.

Do not keep polishing an inaccurate full-code UI. If one correction pass still looks unlike the real product, switch to:

```text
real screenshot/backplate
+ code overlays
+ motion artifacts
+ rendered QA frames
```

## Layer Model

Use four layers:

```text
Layer 1: Real UI backplate
Layer 2: Functional overlays
Layer 3: Foreground workflow artifacts
Layer 4: Captions / brand close
```

### Layer 1: Real UI Backplate

Use the captured product frame as the visual truth:

```tsx
<AbsoluteFill>
  <Img
    src={staticFile("product/screen.png")}
    style={{width: "100%", height: "100%", objectFit: "cover"}}
  />
</AbsoluteFill>
```

Prefer 1920x1080 screenshots when the composition is 1920x1080. If the aspect ratio changes, centralize the scale/offset math in one helper and test every overlay.

### Layer 2: Functional Overlays

Only overlay what must move or explain an action:

- cursor
- click ripple
- focus ring
- typed text
- selected row highlight
- chart peak marker
- toast/status
- data result ribbon

Keep these overlays in the same coordinate system as the screenshot.

### Layer 3: Foreground Workflow Artifacts

Use these for HyperFrames-style continuity:

- selected client card
- selected segment card
- generated document preview
- matched product row
- recommendation card
- approval card

The artifact must come from a real product action. Do not float generic decorative cards.

### Layer 4: Captions

Captions should not cover:

- the clicked element
- focus ring
- selected row/card
- chart line or axis labels
- product table headers
- important product copy

If the UI is dense, use a compact caption lane with semi-opaque background and short text.

## Native Coordinate Rule

For a 1920x1080 backplate in a 1920x1080 composition:

```ts
type Rect = {
  left: number;
  top: number;
  width: number;
  height: number;
};

const target = {
  search: {left: 226, top: 14, width: 402, height: 37},
};
```

The focus box and pointer should both derive from the same `Rect`:

```ts
const centerOf = (rect: Rect) => ({
  x: rect.left + rect.width / 2,
  y: rect.top + rect.height / 2,
});
```

Never maintain separate hard-coded cursor coordinates and focus coordinates for the same target.

## Pointer Lifecycle

The pointer should behave like an intention cue:

```text
enter -> click -> fade out
```

Recommended timing:

- Enter: 0.2-0.4s before the state change.
- Click pulse: 0.1-0.2s.
- Fade out: within 0.4-0.7s after click.

Do not let a cursor remain visible near an old target while a new focus ring appears somewhere else.

## Focus Lifecycle

The focus ring should behave like a temporary spotlight:

```text
focus in -> hold while explained -> fade before next target
```

Recommended timing:

- Focus in: 0.2-0.35s.
- Hold: only for the current explanatory beat.
- Fade out: 0.25-0.45s before or during the transition to the next target.

Avoid two unrelated focus rings on screen at the same time.

## Data Overlay Rules

If a real Insights/dashboard screenshot already has a chart, avoid rebuilding the entire data panel unless you can match it exactly.

Good overlays:

- peak pulse on the real terminal point
- tooltip anchored near the real chart marker
- integrated result ribbon
- subtle line trace only if it aligns perfectly with the real chart

Bad overlays:

- small detached chart window over the product
- line chart that collides with existing axis labels
- data ribbon covering month labels or tooltip
- decorative scan effects that do not explain data generation

## Caption Placement

Use the smallest text that can carry the beat.

Good:

```text
Find the client.
Run holdings look-through.
Segment, then match.
Prioritize next action.
```

Avoid full-sentence captions over dense product UI. If necessary, put captions in a bottom-left or side lane with:

- max width 25-30% of frame
- semi-opaque background
- 1 headline + 1 short support line
- no overlap with the active UI target

## QA Frames

Render at least these frames:

```text
Search: cursor on search field, click faded after selection
Analysis: focus on real task card, generated artifact visible
Data: chart/tooltip/ribbon without axis or label overlap
Segment: selected segment and matched product row
Pipeline: selected board/card and approval overlay
```

Check both:

- a settled frame
- a mid-action frame after the click

## Failure Modes And Fixes

| Problem | Likely Cause | Fix |
|---|---|---|
| Cursor and box disagree | Pointer did not fade, or coordinates differ. | Derive both from one rect and fade pointer after click. |
| Overlay drifts from UI | Backplate is scaled/cropped differently from coordinate assumptions. | Match composition ratio or centralize transform math. |
| UI still feels fake | Code recreation differs from real product. | Use screenshot backplate. |
| Caption covers product | Caption is placed before target is known. | Reserve caption lane after target selection. |
| Data feels decorative | Overlay is detached from product chart. | Anchor to real chart marker or use integrated ribbon. |
| Too many things move | Cursor, focus, card, caption all animate at once. | Make one primary action and delay secondary elements. |

## Production Checklist

Before rendering the final video:

```text
Backplate is the real product UI.
Overlay coordinates use the same native coordinate system.
Pointer and focus share the same target rect.
Pointer fades out after click.
Focus fades before the next unrelated target.
Captions do not cover active UI.
Foreground artifacts come from real workflow objects.
Data overlays are anchored to real chart or metric areas.
Mid-action QA frames are checked.
Settled QA frames are checked.
```
