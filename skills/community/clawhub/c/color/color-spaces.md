# Color Spaces and Conversion

## Core Rule

- Pick the color space that matches the job: editing, interpolation, screen delivery, or print handoff are not the same problem.

## Practical Space Guide

| Space | Best for | Watch out for |
|-------|----------|---------------|
| HEX / RGB | Final web and UI values | Poor for reasoning about perceived lightness |
| HSL / HSV | Quick exploration and rough tweaks | Equal steps do not look visually equal |
| LAB / LCH | Editing and device-independent reasoning | Can still feel less intuitive than OK spaces for UI ramps |
| OKLab / OKLCH | Perceptual ramps, theme derivation, token systems | Some tools still need conversion support |
| CMYK | Print production | Smaller gamut and device dependence |
| Spot color systems | Brand-critical print inks | Cost and production constraints |

## RGB and HEX

- RGB and HEX are good output formats for digital products.
- They are weak design-thinking tools when you need visually even ramps.
- Two colors can be numerically close in RGB and still feel very different in brightness.

## HSL and HSV

- Useful for ideation because hue, saturation, and lightness are easy to reason about.
- Dangerous when building full ramps because equal lightness steps do not stay perceptually even.
- Fine for quick mocks, not enough for production-grade palette systems on their own.

## LAB, LCH, OKLab, and OKLCH

- Better for generating ramps, deriving tints and shades, and keeping lightness changes more predictable.
- OKLCH is especially practical for UI systems because lightness and chroma changes feel more stable.
- High chroma values can leave the display gamut quickly, so check conversions back to sRGB.
- Perceptual spaces reduce guesswork, but they do not remove the need for visual review.

## Gamut and Conversion

- Not every color visible in Display P3 or a design tool survives conversion to sRGB or CMYK.
- "Same hex" does not protect a color from looking different across displays with different profiles and brightness.
- Brand-critical colors should be validated after conversion, not assumed safe.
- When a color clips during conversion, lightness and saturation relationships often shift first.

## Interpolation Rules

- Interpolate ramps in a perceptual space when possible.
- RGB interpolation often creates muddy or unexpectedly dark midpoints.
- HSL interpolation can create strange saturation or brightness behavior.
- Diverging scales, heatmaps, and theme ramps benefit most from perceptual interpolation.

## Common Conversion Traps

- Designing in a wide-gamut tool and forgetting the final app or browser is effectively sRGB.
- Converting bold digital colors to CMYK and being surprised by the dull result.
- Building a ramp in HSL and wondering why the middle steps feel uneven.
- Treating print conversions as administrative cleanup instead of a design decision.
