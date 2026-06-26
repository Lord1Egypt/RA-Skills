# Color Implementation Commands

These examples are for cases where the strategy is already clear and the user needs a concrete implementation.

## CSS Tokens

### Semantic Token Pattern

```css
:root {
  --gray-0: oklch(0.99 0.01 255);
  --gray-1000: oklch(0.16 0.02 255);

  --brand-500: oklch(0.63 0.18 255);
  --brand-600: oklch(0.56 0.18 255);

  --surface-page: var(--gray-0);
  --surface-card: oklch(0.97 0.01 255);
  --text-primary: var(--gray-1000);
  --text-secondary: oklch(0.45 0.02 255);
  --border-subtle: oklch(0.9 0.01 255);
  --action-primary-bg: var(--brand-500);
  --action-primary-text: white;
  --status-danger: oklch(0.58 0.2 25);
}
```

### Dark Mode Surface Strategy

```css
[data-theme="dark"] {
  --surface-page: oklch(0.18 0.01 255);
  --surface-card: oklch(0.23 0.01 255);
  --text-primary: oklch(0.95 0.01 255);
  --text-secondary: oklch(0.8 0.01 255);
  --border-subtle: oklch(0.34 0.01 255);
}
```

- Raise surface lightness gradually instead of relying only on big shadows.
- Keep semantic names stable so the theme can swap values cleanly.

## JavaScript Helpers

### `colorjs.io`

```bash
npx colorjs.io oklch "0.63 0.18 255" --to srgb
npx colorjs.io srgb "#2563eb" --to oklch
```

- Useful for conversions during design-token work.
- Treat `npx` examples as remote-code execution from the package registry and use them only in trusted environments.

### Tiny Contrast Check

```js
import Color from "colorjs.io";

const fg = new Color("#1f2937");
const bg = new Color("#ffffff");

console.log(fg.contrast(bg, "WCAG21"));
```

## Tailwind Example

```js
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef6ff",
          100: "#d9ebff",
          500: "#2b6ff2",
          600: "#1f5ed8",
          700: "#1849a8"
        }
      }
    }
  }
};
```

- Keep these as primitives or marketing colors, then map semantic aliases elsewhere.

## Sass Mixin

```scss
@mixin interactive-colors($bg, $fg) {
  background: $bg;
  color: $fg;

  &:hover {
    background: color-mix(in oklab, $bg 88%, black);
  }

  &:disabled {
    background: color-mix(in oklab, $bg 40%, white);
    color: color-mix(in oklab, $fg 60%, white);
  }
}
```

- `color-mix()` is useful, but still verify the resulting contrast in every state.

## CLI and Utility Notes

### ImageMagick Color Profile Conversion

```bash
magick input.tif -profile sRGB.icc output.png
magick input.jpg -colorspace sRGB output.jpg
```

### Extract Dominant Colors

```bash
magick input.jpg -resize 200x200 -colors 8 -unique-colors txt:-
```

- Useful for building a first-pass palette from a logo, product photo, screenshot, or campaign reference.
- Treat the extracted set as raw material; prune duplicates and rebalance neutrals before using it as a system palette.

### Generate a Quick Ramp

```js
import Color from "colorjs.io";

const start = new Color("oklch(0.95 0.02 255)");
const end = new Color("oklch(0.35 0.08 255)");

for (let i = 0; i < 5; i++) {
  const t = i / 4;
  console.log(start.range(end, { space: "oklch" })(t).to("srgb").toString({ format: "hex" }));
}
```

## Command Traps

- Do not generate ramps mechanically and skip visual review.
- Do not convert profiles without checking the target environment.
- Avoid naming tokens directly from generated values if they are meant to stay semantic.
- Spot-check real contrast and export behavior after any automated conversion.
