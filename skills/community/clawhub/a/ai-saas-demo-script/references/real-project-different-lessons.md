# Real Project Lessons: different. AI Fintech Demo

Use this reference when a demo is based on a real SaaS product, especially a dark-theme fintech/AI workspace with dashboards, product workflows, and data-heavy scenes.

## What Worked

The strongest version came from combining:

```text
real product vocabulary
+ real product screens/backplates when fidelity matters
+ code overlays for cursor, focus, carry cards, data ribbons, and state changes
+ HyperFrames-style camera continuity
+ full-scale data dashboard proof
+ rendered-frame QA
```

The video became stronger when it stopped presenting screenshots and started showing a causal product path:

```text
client signal
-> real task card
-> cursor click
-> AI Workgroup checklist
-> generated pack
-> full Insights dashboard
-> chart/data proof
```

## Reusable Shot Grammar

| Beat | Rule | Example Application |
|---|---|---|
| Signal | Use one workflow object that travels across scenes. | Client signal becomes current holdings task. |
| Operation | Camera pushes only toward an active product action. | Push to the `Current holdings look-through analysis` task. |
| AI process | Checklist/status steps should name real product work. | Read holdings, draft outline, prepare KYP shortlist. |
| Artifact | Generated output should be a tangible product object. | Holdings look-through pack lifts into foreground. |
| Data proof | Important analytics should become the main scene. | Full `Performance Trends + AI Insights` screen. |
| Value close | Benefits appear only after a visible result state. | Save time, avoid errors, stay in control. |

## Real UI Fidelity Rules

- Use captured product labels, navigation, and states. Generic copies like `Run analysis` are weaker than source terms like `Current holdings look-through analysis`.
- Use the real brand asset when provided. Do not ship approximated CSS logos for recognizable marks.
- Preserve the product's visual language: dark surfaces, border weights, accent colors, status colors, and typography hierarchy.
- Code-layered UI is useful for animation precision only when it matches the real product. If the recreation visibly differs after one correction pass, switch to real screenshot/backplate plus code overlays.
- Use screenshots as the animated surface when UI fidelity matters more than per-component reconstruction. Then animate only functional layers: cursor, focus, selected row, foreground carry card, generated artifact, data ribbon, or success state.
- Do not treat "real copy" as "real UI." Real UI fidelity includes sidebar density, topbar structure, active nav states, table rows, journey spacing, data grid/chart treatment, logo placement, and card hierarchy.

## V15 To V16 Correction

V15 failed because it used code-recreated UI with real labels but not enough real layout fidelity. It also let pointers remain visible after the click, so later focus boxes appeared while the cursor was still near an old target. This made the viewer read the scene as inaccurate even when some coordinates were technically intentional.

V16 corrected the approach:

```text
real 1920x1080 product screenshots as backplates
+ overlay coordinates stored in the same native screenshot coordinate system
+ pointer fade-out after click
+ focus boxes with explicit hold/fade lifecycle
+ code-only artifacts for generated cards, data ribbons, and approval feedback
```

Use this as the default fix when a real-product demo gets repeated feedback like "UI is not like the actual site" or "mouse and box selection do not match."

## Pointer And Focus Lifecycle

- The cursor should enter before the action, click, then fade out within roughly 0.4-0.7s unless it is visibly traveling to the next target.
- A focus box should enter, hold for the explanation, and fade before the next unrelated target appears.
- Avoid showing a pointer at one target while a focus ring highlights another target.
- For screenshot/backplate workflows, put all overlay coordinates in the screenshot's native coordinate system. Do not mix screenshot coordinates with transformed container coordinates unless one helper applies the transform.
- Render a mid-action frame after the click, not only a settled final frame.

## Data Dashboard Rules From This Project

The data section improved only after it became a full product page instead of a small overlay.

Use this structure for important analytics:

```text
section title
-> KPI grid with count-up
-> axis/grid fade-in
-> line/area chart draw
-> peak tooltip
-> AI insight cards stagger in
```

For line charts:

- Create a fixed left gutter for Y-axis labels.
- Start the plotted line to the right of those labels.
- Put the final point close to the chart edge.
- Anchor the tooltip leftward if it would create empty right-side space.
- Use one set of constants for grid, points, month labels, area fill, and tooltip.
- Render-check a final frame: no overlap at the first point, no empty tail after the final point.

## Animation And Performance Lessons

- Heavy SVG glow/blur filters can cause flicker, slow preview, or stutter. Prefer a simple secondary stroke or opacity layer.
- Do not stack multiple full-screen translucent scenes. Fade out the outgoing product page before the next page dominates.
- Use an opaque page background for major product page transitions.
- Render key frames before full export: opening/logo, operation click, AI process, data final state, and outro.
- When a rendered frame reveals a layout issue, fix the component coordinate system instead of nudging overlays by eye.

## Common Failure Modes

| Problem | Cause | Fix |
|---|---|---|
| Focus box is inaccurate | Rectangle drawn over screenshot or arbitrary coordinates. | Wrap the real component with a focus layer. |
| Focus box still drifts in code UI | Code recreation is inside camera/grid transforms or does not match real layout. | Use real screenshot/backplate and overlay in native screenshot coordinates. |
| Cursor and focus point at different things | Pointer remains visible after click or uses a different coordinate system. | Give pointer a fade-out lifecycle and derive pointer/focus from the same target. |
| Demo feels static | UI screenshots shown without operation/state change. | Add cursor-led action and product state transition. |
| Data feels decorative | Metrics shown as small badges. | Promote data to a full dashboard scene. |
| Chart overlaps labels | No chart label gutter. | Reserve a Y-axis label gutter and start plot after it. |
| Empty chart tail | Tooltip/final point requires too much right padding. | Move final point near edge and anchor tooltip leftward. |
| Playback flickers | Heavy filters or stacked translucent full-screen layers. | Remove filters, fade out previous scene, add opaque page background. |
| Brand feels wrong | Logo approximated with CSS or placeholder. | Use the real image asset with correct aspect ratio. |

## Production Checklist

Before calling a real-product demo production-ready:

```text
Real logo asset is used.
Source product terms appear in key UI labels.
Real UI screens or verified matching code recreations are used.
Camera motion has a target in every push.
Focus states are component-attached or native-backplate-coordinate overlays.
Pointers fade out after click before the next unrelated focus appears.
Data dashboard is large enough to read.
Chart label gutter and final point spacing are checked.
No important UI is hidden behind overlays.
No heavy SVG filters remain if playback stutters.
Rendered frames confirm layout before final export.
```
