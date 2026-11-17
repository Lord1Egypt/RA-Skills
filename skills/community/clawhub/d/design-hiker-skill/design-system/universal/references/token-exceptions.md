# Token Exceptions

The default rule is strict: generated product UI must use `var(--*)` tokens for
colors, spacing, typography, radius, shadows, durations, and component sizes.
This file lists the few values that are allowed to remain literal because they
are platform constants, SVG geometry, or preview chrome rather than product
design decisions.

## Product UI Defaults

Use tokens for:

- `color`, `background`, `border-color`, `box-shadow`
- `padding`, `margin`, `gap`, layout offsets
- `font-size`, `font-weight`, `line-height`, `letter-spacing`
- `border-radius`
- component heights and widths when a token exists
- transitions, animation durations, and easing

If a value does not have a token and is part of product UI, add a project token
or log it in `assumptions.log` as `[CHOSEN]`, `[SAMPLED]`, or `[UNKNOWN]`.

## Allowed Literal Values

### Platform Constants

These values are allowed as hardcoded pixels because replacing them with a
nearby token makes the platform feel wrong:

- macOS traffic-light dots: `12px`
- macOS traffic-light gap: `6px`
- macOS titlebar height: `36px`
- macOS compact toolbar controls: `26px` to `28px`
- macOS table header height: `28px`
- iPhone 15/16 preview frame: `393px x 852px`, radius `47px`
- iPhone 16 Pro Max preview frame: `440px x 956px`, radius `55px`
- iPhone SE preview frame: `375px x 667px`, radius `39px`
- iOS home indicator area: `34px`
- known OS status bar / safe-area measurements from platform references

### SVG Geometry

Inline SVG icon geometry may use literal values:

- `viewBox`, `path d`, `cx`, `cy`, `r`, `x`, `y`, `width`, `height`
- `stroke-width` when needed for optical alignment

Still use `currentColor` for icon color unless a multicolor brand asset is
explicitly required.

### Preview Chrome

Device frames, browser frames, macOS window shells, preview controls, and
deck stages are preview scaffolding. Their bezel sizes, traffic lights, canvas
grid, and label controls may use literal values.

Rules:

- Keep preview chrome visually separate from product UI.
- Do not copy preview chrome values into product components.
- Add comments when a block is preview-only.

### CSS Syntax Constants

These values may remain literal:

- `0`
- `1`, opacity values, and unitless line-height multipliers
- percentages such as `100%`, `50%`, `100vh`, `100vw`
- keyword values such as `auto`, `none`, `transparent`, `currentColor`,
  `inherit`, `unset`
- `env(safe-area-inset-*)`
- media query breakpoints when they reference existing token values is not
  possible in CSS

## Required Logging

For every literal value outside this allowlist:

1. Prefer adding a token to `tokens.css` or `component-tokens.css`.
2. If the value is one-off but intentional, add a comment next to it and record
   it in `assumptions.log`.
3. If the value came from an image or screenshot, mark it `[SAMPLED]` or
   `[ESTIMATED]`.

## QA Expectations

L4 QA should report hardcoded product UI values. It should not report the
allowed exceptions above unless they appear inside product UI where a token
exists.
