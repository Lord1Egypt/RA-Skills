# 8-bit quantisation budget

## The arithmetic

On 8-bit material the quantisation step is:

```
step = 1 / base
```

| base | step |
|---|---|
| 200 | 0.005 |
| 220 | 0.0045 |
| 240 | 0.00417 |

Every output value is rounded to a multiple of this step. A change is only visible if it crosses at least one step — and in practice, one or two levels is below the threshold anyone can see.

## Worked examples

**Decay constant 6 → 5.** The resulting change is about one quantisation level. Indistinguishable. The change did not happen, as far as any viewer is concerned.

**Peak 1.03 → 1.06.** Moves the result by one or two levels. Also not a visible difference.

Both of these consumed a full render cycle to discover.

## Decision rule

Before any parameter change, estimate the visible delta:

```
levels_moved = |change_in_output_value| / step
```

- `levels_moved < 1` — the change is guaranteed invisible. Do not make it.
- `levels_moved` in the low single digits — treat as invisible. Do not spend a render on it.
- Larger — worth an **A/B frame**, still not a full re-render.

## What this is really about

The failure mode is not bad arithmetic. It is building a rigorous set of criteria, tuning parameters until every criterion reads green, and producing a finished piece that looks identical to the previous one.

Green criteria mean the change was applied correctly. They do not mean it was worth applying.

## When a change genuinely is needed

If the look has to change and parameters cannot move it far enough, the change is on the picture layer: composition, camera, depth of field, lighting, colour grading. Those move output by many levels at once, and they are visible.

Parameters are for correctness. The picture layer is for looks.
