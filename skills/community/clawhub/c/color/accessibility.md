# Color Accessibility

## Core Rule

- A color choice is only successful if users can still read, distinguish, and act on it in the real interface.

## Contrast Roles

Different checks solve different problems:

| Role | Typical target | Why |
|------|----------------|-----|
| Body text | 4.5:1 or better | Small text fails quickly |
| Large text | 3:1 or better | Bigger text tolerates lower contrast |
| UI boundaries | 3:1 or better | Inputs, dividers, and buttons still need separation |
| Icons carrying meaning | 3:1 or better | Function disappears before the icon shape does |
| Over-photo text | Check manually even if ratio passes | Local image variation breaks theoretical contrast |

- The same foreground may pass on white and fail on tinted cards or dark mode surfaces.
- Hover, focus, disabled, and pressed states need separate validation.
- Text inside gradients or photos needs manual preview, not only a ratio checker.

## Non-Color Cues

- Pair state colors with labels, icons, patterns, underlines, borders, or placement.
- Success vs error should still be understandable in grayscale.
- Selected vs unselected should not rely only on tint changes when the shapes are identical.
- If color disappears, the interface still needs to explain what changed.

## Colorblind-Safe State Design

- Red and green can exist in the same system, but never as the only distinction.
- Blue and orange are often safer opposites than red and green.
- Test categorical palettes for deuteranopia and protanopia before finalizing them.
- Error and success need different shapes or copy if the stakes are real.

## Color Vision Deficiency Simulation

- Simulate at least the common failure modes: deuteranopia, protanopia, and deuteranomaly.
- Run the simulation on full components or charts, not only on isolated swatches.
- Two colors that look distinct in a palette strip can collapse once labels, borders, or thin lines are applied.
- If a critical pair becomes too similar under simulation, change hue, lightness, pattern, or labeling instead of hoping copy will save it later.

## Text Over Color

- Brand colors that work as fills often fail as text colors.
- White text needs darker or controlled backgrounds; it collapses fast on bright fills.
- Small text inside saturated chips usually needs darker fills or lighter tints than teams expect.
- Contrast on pills, banners, and badges should be checked at the smallest likely size, not just in the design file.

## Charts and Data

- Legends, labels, and series lines need contrast against the chart background and against each other.
- Thin lines and pale fills disappear first on projectors, dashboards, and screenshots.
- Use direct labeling when possible so users do not rely entirely on color-coded legends.
- Diverging scales should keep the midpoint visually distinct, not muddy.

## Common Accessibility Traps

- Picking a gray that barely passes on white and then reusing it everywhere.
- Using transparency to create states without rechecking the resulting contrast.
- Assuming a contrast plugin solves text over images.
- Marking required fields, errors, or status only with color.
- Designing a palette that passes AA in isolation but fails in component states.

## Quick Checks

```
□ Body text passes on every real surface
□ Important states have non-color cues
□ Charts and legends still work in grayscale
□ Text over imagery checked on the actual image
□ Small badges, pills, and labels tested at production size
```
