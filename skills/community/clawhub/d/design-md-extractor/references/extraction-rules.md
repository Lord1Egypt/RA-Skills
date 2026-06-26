# Extraction Rules

The extractor is local and rule-based:

- Samples visible elements only.
- Uses computed styles, not screenshots.
- Prioritizes action colors from buttons, interactive elements, active states, CTA/action text, links, and brand-like class names.
- Detects backgrounds from body/html and large page surfaces.
- Detects typography from headings, body text, captions, buttons, and inputs.
- Clusters spacing, radius, and shadow values by observed computed styles.
- Detects basic components: button, card, input.
- Detects common design-system signatures from CSS variables and class names.

Known limits:

- Dynamic hover/focus/active/disabled states are inferred from static samples.
- Logged-in or personalized pages require the browser context to already expose that state.
- Cross-origin iframes, canvas-only UIs, screenshot-only designs, and heavily obfuscated styles may be incomplete.
- Web fonts may affect typography if they do not load before sampling.
