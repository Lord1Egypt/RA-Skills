# Input Handler — Screenshot / Image

## Applies to
- Screenshots of existing UI
- Design mockup images
- Any visual input to reverse-engineer

## Precision characteristics

Screenshot input has inherent measurement limitations:
- Dimensions: ±5–10px typical error
- Colors: approximate (use sampled hex, mark as `[SAMPLED]`)
- Typography: visual estimation only
- Grayscale screenshots: colors unknown, mark as `[UNKNOWN]`

**Sketch/Figma source files are always preferred** for precise work. Screenshots are a fallback.

## Process

### Step 1 — Visual decomposition

Before extracting values, describe what you see:
- Overall layout structure (single column / sidebar / grid / tabs)
- Major sections, top to bottom
- Key components visible
- Color palette (dominant colors)
- Platform (infer from screen width, safe areas, navigation patterns)

### Step 2 — Establish anchors

Use known fixed measurements to calibrate visual estimation:
```
iOS status bar:     44px
iOS navigation bar: 44px
iOS bottom safe area: 34px
Android status bar: 24px
Standard touch target: 44px minimum
Standard button height: 44–56px
```

Scale all other measurements proportionally from these anchors.

### Step 3 — Token matching

After measuring, map values to tokens:
```
Measured: ~16px padding → var(--spacing-md)
Measured: ~#0055EE color → var(--color-primary)  [mark as SAMPLED]
Measured: ~14px font → var(--font-size-body-sm)
```

If a measured value doesn't match any token, use the closest token and note the discrepancy.

### Step 4 — Mark all uncertainty

Every value extracted from a screenshot must be marked:
```
[EXACT]      → matches a token exactly (spacing, standard heights)
[ESTIMATED]  → visual measurement with possible error, note the range
[SAMPLED]    → color sampled from image, may differ from intended
[UNKNOWN]    → cannot determine (color in grayscale, value hidden)
```

Never omit a value. Write `? [UNKNOWN - verify]` for truly indeterminate values.

### Step 5 — Color extraction

For sampled colors:
1. Sample the most representative pixel
2. Note the hex value: `#FF6600 [SAMPLED from CTA button]`
3. Check if it matches a universal token — if so, use the token name
4. If not, write the hex value and mark as `[SAMPLED]` in assumptions.log
