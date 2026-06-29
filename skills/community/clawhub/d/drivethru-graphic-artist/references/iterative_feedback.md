# Iterative feedback & rule tuning

Mockups are a conversation. The first compose is a starting point; the user
will react ("bigger", "move it up", "rotate it"). Translate plain-language
feedback into deltas layered on top of the *previous* run's arguments.

## Feedback → flags

| User says | You run (added to the last run's args) |
|---|---|
| "Make it ~10% bigger" | `--width-delta-pct +10` |
| "Make it ~15% smaller" | `--width-delta-pct -15` |
| "Move it up a little" | `--offset-y-pct -5` |
| "Move it down" | `--offset-y-pct +5` |
| "Shift left" | `--offset-x-pct -5` |
| "Shift right" | `--offset-x-pct +5` |
| "Rotate 5° clockwise" | `--rotate-deg 5` |
| "Rotate 5° counter-clockwise" | `--rotate-deg -5` |

Keep a running record of the current flags so each turn composes on top of the
last, not from the original defaults. A delta of `±5` percentage points is a
good "a little" nudge; `±10–15%` is a good "noticeably" nudge for width.

## Promoting a tuned result to a default

When the user is happy and says something like "save that as the new default
for hoodie full-front," bake the *effective* ratios from the last compose
receipt's `applied` block into the catalog:

```bash
python3 scripts/edit_placement_rule.py update hoodie full_front \
    --width-ratio 0.58 --y-top-ratio 0.20
```

## Adding a brand-new category or placement

When the user asks for a placement/category that isn't in the catalog yet:

```bash
python3 scripts/edit_placement_rule.py add tote front \
    --width-ratio 0.45 --x-center-ratio 0.50 --y-top-ratio 0.30
```

Then re-compose with that `--category`/`--placement`.

## Coordinate model recap

All rule fields are ratios against the **detected garment bounding box**, not
the full image:

- `width_ratio` — decoration width ÷ garment bbox width (0.01–1.5).
- `x_center_ratio` — decoration center X within the bbox (0 = left, 1 = right).
- `y_top_ratio` — decoration top Y within the bbox (0 = top, 1 = bottom).
- `rotation_deg` — clockwise rotation in degrees (−180…180).

Because they're ratios, the same rule yields a visually matching print across
resolutions, crops, and garment sizes (a youth tee and an adult tee line up).
