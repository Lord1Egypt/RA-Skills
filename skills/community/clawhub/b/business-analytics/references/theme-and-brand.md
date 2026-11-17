# Theme and brand adaptation

## Priority

1. Explicit user color or style direction.
2. User-provided brand guide.
3. User-provided logo or reference image.
4. Business-mode defaults.

## Image-derived theme

Run:

```bash
python3 scripts/extract_theme.py /absolute/path/to/image.png
```

Use dominant saturated colors for primary and categorical accents. Use pale versions for plot fills, selected states, and decorative backgrounds. Derive neutral page, card, border, and text colors independently so the interface remains readable.

Do not sample skin, photography, or large white areas as the sole brand color. Inspect the image and favor repeated graphic elements, logo marks, headings, and deliberate color blocks.

## Logo handling

- Use the user's actual logo when supplied and preserve its aspect ratio.
- If the only image is a broad visual reference, use its palette and mood without pretending it is the business logo.
- Provide a clear logo replacement point in the HTML configuration when the output is meant as a reusable template.

## Contrast and charts

- Ensure normal text contrast remains readable on card and page backgrounds.
- Use hue plus line style, marker, label, or pattern so charts do not rely on color alone.
- Keep grid lines visible against the plot background.
- Reserve the strongest accent for the most important series or action.
- Use a stable color assignment for the same metric across tabs.

The target is brand coherence, not literal extraction of every dominant pixel.
