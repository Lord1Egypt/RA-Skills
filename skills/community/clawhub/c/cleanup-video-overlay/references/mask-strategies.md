# Mask Strategies

## Region Format

The scripts accept one or more `x:y:w:h` regions.
Each value can be pixels or percentages.

Examples:

- `0:0:100%:7%`
- `0:90%:100%:10%`
- `78%:2%:20%:12%`
- `40:24:180:64`

## Presets

Current presets are intentionally simple and conservative:

- `iphone-status-bar`: top 7 percent
- `android-status-bar`: top 6 percent
- `bottom-nav-bar`: bottom 8 percent
- `notification-banner`: top 16 percent
- `subtitle-strip`: bottom 18 percent

These are starting points, not truth. Tighten the region when possible.

## Good Mask Habits

- Keep the mask close to the overlay edge
- If a logo has padding, mask only the visible mark plus a small margin
- For edge bars, avoid spilling deep into the active picture area
- For frame-edit workflows, reuse one fixed mask only when the overlay truly stays put

## When To Avoid Oversized Masks

Oversized masks increase:

- blur and texture washout
- incorrect hallucinated detail
- visible temporal instability
- editing cost for frame-by-frame model calls

## Debugging A Bad Result

If the output looks wrong, check in this order:

1. Mask too large
2. Overlay is not actually fixed
3. Source compression is already too noisy
4. `removelogo` is insufficient and needs frame-edit mode
5. The external editor is changing unmasked parts of the frame
