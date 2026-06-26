# Data Animation and Before / After Rules

Use this reference when the demo includes dashboards, KPIs, analytics, reports, trends, measurable impact, before/after proof, workflow compression, or AI-generated improvements.

## Data Animation Rules

Animate data to explain change, not to decorate the screen.

```text
Make data change visible as a process.
Do not simply reveal the final number or final chart.
```

### Data Story Sequence

| Step | Goal | Common animation language |
|---|---|---|
| Context | Establish what data space the viewer is seeing. | Dashboard fades in, chart frame/axes appear, empty cards settle. |
| Build | Generate the data progressively. | Bars grow from zero, line draws left-to-right, pie/donut sweeps, KPI counts up. |
| Highlight | Emphasize one key point. | One bar changes color, one number scales up, label pops, other values dim. |
| Explain change | Show what changed and by how much. | `+20%`, delta arrow, before -> after comparison, old value fades into new value. |
| Summarize | Let the insight register. | Values stop, conclusion/title appears, camera slightly zooms out. |

### Data Motion Techniques

| Technique | Use for | Timing at 30fps |
|---|---|---|
| Number tweening | KPIs, revenue, users, time saved, error reduction. | 24-45 frames (`0.8s-1.5s`), ease-out. |
| Bar growth | Comparisons, volume, category metrics. | 18-36 frames (`0.6s-1.2s`), grow from baseline/zero. |
| Line draw | Trends over time. | 24-45 frames, draw left-to-right in time order. |
| Pie/donut sweep | Share or distribution. | 18-36 frames, sweep clockwise with clear labels. |
| Before/after comparison | Showing improvement. | 24-45 frames, old state dims or slides away as new state resolves. |
| Stagger | Multiple bars, table rows, metric cards. | 2-5 frame delay (`0.05s-0.15s`) between items. |
| Emphasis pulse | The one metric that matters. | scale `1 -> 1.1/1.2 -> 1`, 8-14 frames, use once or twice. |

### Data Focus Rules

- Emphasize only one primary metric at a time.
- Animate background data first and quickly; animate key data later and slower.
- Dim, blur, or desaturate secondary data when highlighting the main insight.
- Keep demo data to no more than three key takeaways unless the user explicitly asks for a dense analytics demo.
- Use labels to explain deltas: prefer `+20% faster`, `3 errors avoided`, or `12 hours saved` over raw numbers alone.
- Make the causal logic visible when possible: input/action -> data update -> insight/result.
- If the product has a real analytics page, use it as a full product scene. Do not shrink high-value dashboard proof into a corner badge unless the scene is only a quick transition.

### Chart Layout Rules

For line charts, trend charts, and finance dashboards:

- Reserve a fixed left gutter for Y-axis labels. The first plotted point must start to the right of the labels, never on top of them.
- Reserve a modest right gutter for the final point and tooltip, but do not leave a visibly empty chart tail. Prefer anchoring the tooltip leftward from the final point.
- Keep the plot area, grid lines, month labels, area fill, and line path using the same coordinate constants.
- Render a final-state frame and check: first point does not overlap Y labels, final point is close to the chart edge, month labels are readable, and the tooltip does not force blank space.
- Avoid heavy SVG filters for chart glow in video. Use a lightweight secondary stroke or simple opacity instead if playback flickers or stutters.

### Data Rhythm Formula

```text
background fast -> data build medium -> highlight slow -> conclusion hold
```

Practical defaults:

```text
KPI cards count up: 24-45 frames, staggered by 6-10 frames
axis/grid appears: 10-18 frames
line draws: 30-45 frames
tooltip appears: 12-18 frames
insight cards stagger in: 10-16 frames each
conclusion hold: 30-60 frames
```

Avoid animating all chart elements at once, moving key metrics too quickly, showing charts with no explicit change, using more than three focal metrics in a short demo, or letting decorative motion compete with the insight.

## Before / After Comparison Rules

Use before/after scenes when the demo must prove improvement: manual vs automated, messy vs organized, slow vs fast, uncertain vs clear, fragmented vs unified, or old workflow vs AI-assisted workflow.

```text
Do not just show two states.
Show the transformation from old state to better state.
```

### Comparison Patterns

| Pattern | Use when | Motion language |
|---|---|---|
| Split screen | Two states need direct visual comparison. | Left side dims as right side sharpens; divider slides or locks center. |
| Wipe reveal | The after state replaces the before state in the same space. | Horizontal/vertical mask moves across the UI, revealing the improved state. |
| Overlay replacement | The same object changes quality or status. | Old card fades down while new card aligns on top and resolves. |
| Side-by-side metrics | Improvement is numeric. | Old number appears first, new number counts up/down, delta label pops last. |
| Workflow compression | AI removes steps. | Multiple manual steps collapse into one automated action or generated result. |
| Mess-to-structure | AI organizes unstructured input. | Scattered items align into columns/cards/fields with staggered motion. |
| Error-to-resolution | AI fixes or detects a problem. | Warning state highlights, then resolves into checkmark/status success. |

### Before / After Sequence

```text
before context -> pain/friction cue -> transformation action -> after state -> delta/value label -> hold
```

Practical timing at 30fps:

```text
before state: 30-45 frames
transformation: 18-36 frames
after state: 30-45 frames
delta/value label: 12-18 frames
final hold: 30-60 frames
```

### Design Rules

- Keep before and after layouts spatially related. The viewer should understand what changed without rereading everything.
- Change one dominant variable at a time: time, accuracy, status, volume, clarity, cost, or completion.
- Use visual hierarchy to make the after state feel cleaner: sharper contrast, fewer elements, clearer labels, calmer layout.
- Use the same data scale for both states; do not exaggerate improvement through chart manipulation.
- Prefer explicit deltas over vague claims: `5 steps -> 1 step`, `12 min -> 30 sec`, `8 errors -> 0 errors`.
- Let the after state hold long enough to register. Do not rush away immediately after the transformation.
- Do not overload the comparison with more than three before/after differences in one short scene.

### Storyboard Wording

```text
Manual workflow appears as five stacked steps; AI action compresses them into one generated draft card.
Before metric holds for one beat, then a wipe reveals the improved dashboard with the delta label appearing last.
Scattered inputs snap into structured fields; old labels dim while the completed result receives a soft highlight.
Warning badge flips to resolved status, then the success metric scales gently to 1.12x and holds.
```
