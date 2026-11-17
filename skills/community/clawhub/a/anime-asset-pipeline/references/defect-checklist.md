# Per-region defect checking

## Method

Walk the image region by region and name each region. Vague impressions ("something's off with the hair") do not produce fixes. Named regions do.

Check in this order:

1. **Head** — face shape, eye shape, eye colour, expression
2. **Hair** — silhouette, colour, any local treatment, strands crossing the face
3. **Hands** — count, pose, occlusion. The most frequently wrong region in generated art.
4. **Costume** — closures, symmetry, accessory placement
5. **Contact and grounding** — feet on the floor, objects actually held, shadow direction consistent
6. **Edges** — cut-off limbs, clipped accessories, abrupt terminations

Record a pass or a specific defect per region. Do not record "ok" for a region you did not actually look at.

## Animation-specific checks

For sprite sequences and animated loops, three checks catch most real defects:

**Missing intermediate frames.** Look at where a motion changes phase — a skirt settling, a limb reversing. Compare consecutive frames in that window directly, not in a timeline scrub. Missing transitions hide exactly at phase changes.

**Loop seam.** Compare the last frame against the first. Any discontinuity is visible as a stutter on every cycle.

**Area jitter.** For a loop, measure the silhouette area per frame. Uncontrolled jitter reads as a wobble.

### Example thresholds

Recorded from a 1372-sprite project, as illustration of what a measured value looks like — **not universal pass/fail targets**:

| Asset | Metric | Measured | Reading |
|---|---|---|---|
| sleep loop | IoU | 0.39 | failing |
| land | area jitter | 22.83% | failing |
| idle | skirt frames 6→9 | transition missing | failing |

Set your own thresholds by measuring a known-good asset in your own project first. A number from someone else's project is a starting point for your own measurement, not a criterion.

## Reporting defects

State the region and the defect. "Frame 7, left hand, five fingers where four are expected." Not "hand issue."

When several defects exist, list all of them. Do not fix one, re-render, and discover the next.
