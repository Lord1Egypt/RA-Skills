# Layout Reference

Detailed CSS for print layout and page structure. See SKILL.md for principles.

## CSS Layer Strategy

Use `@layer` to cleanly separate print overrides from screen styles. Layer order trumps specificity — eliminates `!important` wars.

```css
@layer base, components, print;

/* Or import a dedicated print stylesheet into its layer */
@import url("print.css") layer(print) print;
```

All print styles go inside `@media print { @layer print { ... } }`.

## Print Reset

Start every print stylesheet with a clean-slate reset.

```css
@media print {
  @layer print {
    *,*::before,*::after {
      color: #000;
      background: transparent;
      box-shadow: none;
      text-shadow: none;
      filter: none;
      -webkit-filter: none;
    }

    body {
      background: #fff;
      margin: 0;
      padding: 0;
    }
  }
}
```

Then selectively restore backgrounds with `print-color-adjust: exact`. If not using `@layer`, use `!important` on reset properties.

## Page Setup

```css
@page {
  size: A4 portrait;       /* or: letter, A3, legal, 210mm 297mm */
  margin: 20mm 25mm;       /* top/bottom  left/right */
}

@page :first {
  margin-top: 35mm;        /* extra space for title page */
}

/* Book-style asymmetric margins (gutter for binding) */
@page :left  { margin-left: 20mm; margin-right: 30mm; }
@page :right { margin-left: 30mm; margin-right: 20mm; }
```

**Paper sizes:** A4 = 210 x 297 mm, Letter = 8.5 x 11 in, A3 = 297 x 420 mm, Legal = 8.5 x 14 in.

**Margins:** Office documents 20–25 mm. Minimum safe 5 mm (printer hardware limit). Book interiors 20 mm outer, 30 mm gutter.

## Page Simulation on Screen

Show exact page boundaries on screen so the design matches print 1:1.

```css
@media screen {
  body { background: #e0e0e0; padding: 10mm 0; }
  .page {
    background: white;
    width: 210mm; min-height: 297mm;
    margin: 10mm auto;
    padding: 20mm 25mm;
    box-sizing: border-box;
    box-shadow: 0 0 5mm rgba(0,0,0,.2);
  }
}

@media print {
  @page { size: A4; margin: 20mm 25mm; }
  body { background: white; margin: 0; padding: 0; }
  .page {
    width: auto; min-height: auto; margin: 0; padding: 0;
    box-shadow: none;
    page-break-after: always;
  }
  .page:last-child { page-break-after: auto; }
}
```

## Hide / Show Elements

Blacklist approach — explicitly hide what doesn't belong on paper.

```css
@media print {
  nav, .sidebar, .comments, .ads, .cookie-banner,
  .social-share, footer nav, video, audio, button,
  .no-print { display: none !important; }
}
.print-only { display: none; }
@media print { .print-only { display: block; } }
```

## Fragmentation

```css
@media print {
  h1, h2, h3, h4, h5, h6 { break-after: avoid; }

  figure, table, pre, blockquote, img,
  .card, .entry, .job-entry { break-inside: avoid; }

  p { orphans: 3; widows: 3; }

  .chapter { break-before: page; }
  .chapter-start { break-before: right; }  /* book-style: right page */
}
```

## Baseline Grid / Vertical Rhythm

All vertical spacing should be multiples of the base line-height. This creates the "invisible grid" that makes a page cohesive — exactly like InDesign's baseline grid. More achievable in print than on screen because page dimensions are fixed.

**The technique:** Pick a base unit = body line-height. All margins, paddings, and line-heights for every element must be exact multiples.

```css
@media print {
  :root { --rhythm: 15.4pt; }  /* 11pt * 1.4 line-height */

  body     { font-size: 11pt; line-height: var(--rhythm); }
  p        { margin: 0 0 var(--rhythm); }
  h2       { font-size: 16pt; line-height: calc(2 * var(--rhythm));
             margin-top: calc(2 * var(--rhythm)); margin-bottom: var(--rhythm); }
  h3       { font-size: 13pt; line-height: var(--rhythm);
             margin-top: calc(2 * var(--rhythm)); margin-bottom: 0; }
  figure   { margin: var(--rhythm) 0; }
  blockquote { margin: var(--rhythm) 0; padding: 0 var(--rhythm); }
}
```

Headings with larger font-sizes get `line-height` set to 2x or 3x the rhythm unit. This ensures body text baselines across adjacent columns stay aligned.

**Duplex printing:** When printing on both sides of translucent paper (especially ≤80 gsm), baseline-aligned text on recto and verso prevents show-through distortion. Without alignment, faint reversed text bleeds through and degrades readability.

**Don't be slavish:** Images, figures, and embedded media may have natural dimensions that break the rhythm. Let them — resume the grid beneath. The baseline grid governs text flow, not every element on the page.

## Resume: Sidebar + Main Grid

```css
.resume {
  display: grid;
  grid-template-columns: 1fr 2fr;
  width: 210mm;
  min-height: 297mm;
  padding: 15mm 20mm;
  box-sizing: border-box;
}

@media screen {
  body { background: #e0e0e0; display: flex; justify-content: center; padding: 2rem 0; }
  .resume { background: white; box-shadow: 0 4px 20px rgba(0,0,0,.15); }
}

@media print {
  body { background: none; margin: 0; padding: 0; }
  .resume { box-shadow: none; max-width: none; }
}
```

## Sidebar Patterns

```css
/* Border separator */
.sidebar { border-right: 0.5pt solid #ccc; padding-right: 15mm; }

/* Or with background */
.sidebar {
  background: #f5f5f5;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  padding: 15mm;
}
```

## Grid for Structured Sections

CSS Grid is reliable in print. Use it for structured sections (bio, metadata, figure+text).

```css
@media print {
  .two-col-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15pt;
    break-inside: avoid;
  }

  .figure-text {
    display: grid;
    grid-template-columns: 2fr 3fr;
    gap: 12pt;
    break-inside: avoid;
    align-items: start;
  }
}
```

**Avoid CSS `column-count`** for flowing text — page breaks inside columns are fragile. Use Grid with `break-inside: avoid` instead.

## Linearize Screen Layouts

Multi-column layouts from screen should collapse to single-column for print.

```css
@media print {
  .grid-layout { display: block; }
  .flex-layout { flex-direction: column; }
  main { width: 100%; margin: 0; padding: 0; }
}
```

## Chapter Starts (Books/Reports)

```css
.chapter { break-before: right; }

.chapter h1 {
  margin-top: 30%;
  text-align: center;
  font-size: 28pt;
  line-height: 1.1;
  text-wrap: balance;
  break-after: avoid;
}
```

## Responsive Fallback for Mobile Viewing

```css
@media screen and (max-width: 65rem) {
  .resume, .page {
    grid-template-columns: 1fr;
    width: auto;
    min-height: auto;
    padding: 2rem;
  }
}
```
