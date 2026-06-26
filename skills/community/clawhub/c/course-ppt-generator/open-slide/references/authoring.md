# open-slide Slide Authoring Reference

This reference covers the technical rules and conventions for writing open-slide pages. Read this before authoring any slide content.

## File Contract

Each deck lives under `slides/<kebab-case-id>/`. The entry is `slides/<id>/index.tsx`. Assets (images, video, fonts) sit alongside in `slides/<id>/assets/`.

```tsx title="slides/my-deck/index.tsx"
import type { DesignSystem, Page, SlideMeta } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#0f172a', text: '#f8fafc', accent: '#fbbf24' },
  fonts: {
    display: 'system-ui, -apple-system, sans-serif',
    body: 'system-ui, -apple-system, sans-serif',
  },
  typeScale: { hero: 180, body: 40 },
  radius: 12,
};

const muted = '#94a3b8';

const fill = {
  width: '100%',
  height: '100%',
  fontFamily: 'var(--osd-font-body)',
} as const;

const Cover: Page = () => (
  <div
    style={{
      ...fill,
      background: 'var(--osd-bg)',
      color: 'var(--osd-text)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      padding: '0 160px',
    }}
  >
    <div style={{ fontSize: 28, color: 'var(--osd-accent)', letterSpacing: '0.2em' }}>
      CHAPTER 01
    </div>
    <h1
      style={{
        fontFamily: 'var(--osd-font-display)',
        fontSize: 'var(--osd-size-hero)',
        fontWeight: 900,
        margin: '32px 0',
        lineHeight: 1.05,
      }}
    >
      The Big Idea
    </h1>
    <p style={{ fontSize: 'var(--osd-size-body)', color: muted, maxWidth: 1200 }}>
      A short subtitle that explains what this slide is about.
    </p>
  </div>
);

const Content: Page = () => (
  <div style={{ ...fill, background: 'var(--osd-bg)', color: 'var(--osd-text)', padding: 120 }}>
    <h2 style={{ fontFamily: 'var(--osd-font-display)', fontSize: 80, fontWeight: 800, margin: 0 }}>
      Section heading
    </h2>
    <ul style={{ fontSize: 'var(--osd-size-body)', lineHeight: 1.6, marginTop: 64, paddingLeft: 48 }}>
      <li>One clear point per line</li>
      <li>Keep to 3–5 bullets</li>
      <li>Let the space breathe</li>
    </ul>
  </div>
);

export const meta: SlideMeta = { title: 'The Big Idea' };
export default [Cover, Content] satisfies Page[];
```

## The Canvas: 1920 × 1080

Every page renders into a fixed 1920×1080 box. The runtime scales it uniformly to fit the viewport. The canvas does NOT scroll — anything below 1080px is silently cropped.

### Layout Strategies

1. **Absolute positioning.** Place items with `position: absolute` and pixel values. Predictable, easy for agents to write.
2. **Flex/Grid centering.** When elements should flow, use `display: 'flex'` and center them. Avoid responsive breakpoints — the canvas is fixed.

### Two Hard Rules

1. The default export is an array of React components — one per page.
2. Each component fills its container: `width: '100%'` and `height: '100%'`.

## Vertical Budget — Content MUST Fit 1080px

This is the #1 cause of broken slides. Before writing JSX, do the math:

**Usable height** = `1080 − top_padding − bottom_padding`.
- With 120px padding each side → **840px** usable
- With 160px padding each side → **760px** usable

**Element height** = `font_size × line_height × number_of_lines`. Add gaps (32–64px) between elements.

**Worked example (120px padding, budget = 840px):**

| Element | Height |
|---------|--------|
| Heading: 80px × 1.2 × 1 line | 96px |
| Gap | 64px |
| Body: 40px × 1.6 × 3 lines | 192px |
| Gap | 48px |
| 5 bullets: 40px × 1.6 × 1 line each | 320px |
| 4 gaps between bullets: 24px each | 96px |
| **Total** | **816px ✅ fits** |

If you're close to the limit, **split into two pages**. Never use `overflow: hidden/auto/scroll` to hide overflow.

## Design System (Use This By Default)

Every new slide should declare a `design` const so it's tweakable from the Design panel after generation:

```tsx
import type { DesignSystem, Page } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#0f172a', text: '#f8fafc', accent: '#fbbf24' },
  fonts: {
    display: 'system-ui, -apple-system, sans-serif',
    body: 'system-ui, -apple-system, sans-serif',
  },
  typeScale: { hero: 180, body: 40 },
  radius: 12,
};
```

### Consuming Design Tokens

Use **CSS variables** for visual properties (instant updates in Design panel):

```tsx
<div style={{
  background: 'var(--osd-bg)',
  color: 'var(--osd-text)',
  fontFamily: 'var(--osd-font-body)',
  fontSize: 'var(--osd-size-hero)',
}}>
```

Available vars: `--osd-bg`, `--osd-text`, `--osd-accent`, `--osd-font-display`, `--osd-font-body`, `--osd-size-hero`, `--osd-size-body`, `--osd-radius`.

Use **direct `design.X` reads** only when you need a JS number for arithmetic.

Only skip the `design` const for one-off slides whose palette is intentionally locked.

## Type Scale

| Role | Size (px) | Weight | Letter Spacing | Line Height |
|------|-----------|--------|----------------|-------------|
| Hero / Cover headline | 140–200 | 800–900 | -0.04em | 1.0–1.1 |
| Section heading | 80–120 | 800 | -0.02em | 1.1–1.2 |
| Page heading | 56–80 | 700 | 0 | 1.2 |
| Body text | 32–44 | 400 | 0 | 1.5–1.7 |
| Caption / Label | 22–28 | 500 | 0.02em | 1.4 |

## Spacing Conventions

- **Content padding:** 100–160px from canvas edges. Never let text touch the edge.
- **Section gap:** 48–64px between heading and body
- **Item gap:** 24–32px between list items
- **Line-height:** 1.2 for headings, 1.5–1.7 for body

## Visual Direction

Pick ONE coherent look and hold it across every page:

- **Palette** — 1 background, 1 primary text, 1 accent, 1 muted. Define in `design` const.
- **Typography** — one display font + one body font. System stack unless the user specifies.
- **Layout grid** — pick a single content padding (e.g. 120px) and stick to it.
- **Aesthetic** — choose ONE: minimal, editorial, retro, brutalist, soft, neon, paper. Don't mix.

## Image Placeholders

When a page genuinely needs a real image the user must provide, use:

```tsx
import { ImagePlaceholder } from '@open-slide/core';

<ImagePlaceholder hint="Product hero screenshot" width={1280} height={720} />
```

Use placeholders ONLY for content the user owns (product screenshots, team photos, data charts). Do NOT use them for decoration or generic stock-photo filler — those are typography/SVG problems.

## Assets

Place images, videos, and fonts in `slides/<id>/assets/`. Import them in the component:

```tsx
import heroImg from './assets/hero.jpg';

<img src={heroImg} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
```

## Anti-Patterns

- ❌ Walls of text (>40 words per page). Split instead.
- ❌ Using `vw`/`vh`/`rem`/`em` for layout. Use `px` or `%`.
- ❌ Overflowing 1080px vertically. Split the page.
- ❌ `overflow: auto/scroll/hidden` to hide content.
- ❌ Shrinking type below scale lower bound or padding below 100px to cram more in.
- ❌ Body type under 28px — unreadable on a projector.
- ❌ Installing npm packages. Only `react` and standard web APIs.
- ❌ CSS files or className-based styling. Inline styles only.
- ❌ Editing `package.json`, `open-slide.config.ts`, or other slides.
- ❌ Sprinkling `<ImagePlaceholder>` for visual interest — only for real content the user must supply.
- ❌ Bullets that wrap to a second line — shorten or give them their own page.

## Self-Review Checklist

Before considering a page done:

- [ ] `export default`s a non-empty `Page[]`
- [ ] Every page root fills `100% × 100%`
- [ ] Content lives inside padding (no text touches the edge)
- [ ] **For every page, sum heights + gaps + 2×padding ≤ 1080px.** If close, split.
- [ ] No bullet wraps to a second line at the chosen font size
- [ ] One coherent visual direction across every page
- [ ] Slide declares `export const design: DesignSystem = { … }` and uses `var(--osd-X)`
- [ ] One idea per page
- [ ] All imported assets exist under `slides/<id>/assets/`
- [ ] Every `<ImagePlaceholder>` is for real content the user must supply
- [ ] Nothing outside `slides/<id>/` was edited

## Themes

A theme is a markdown file under `themes/<id>.md`. When a user references a theme, read it before authoring — its palette, typography, and layout override defaults.

```md
# Theme Name

## Palette
- ink: #hex
- accent: #hex

## Typography
- display: 'Font Name', fallback
- mono: 'Font Name'

## Voice
- Tone and style notes.
```
