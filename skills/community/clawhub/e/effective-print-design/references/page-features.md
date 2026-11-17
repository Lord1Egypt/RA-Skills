# Page Features Reference

Print-specific page features and element styles. See SKILL.md for principles.

## Page Headers, Footers, and Page Numbers

Chrome 131+.

```css
@page {
  margin: 20mm;

  @top-center {
    content: "Document Title";
    font-size: 9pt; color: #666;
  }

  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-size: 8pt;
  }
}

@page :first {
  @top-center { content: none; }
  @bottom-right { content: none; }
}
```

### Book-Style Running Headers

```css
@page :right {
  @top-right { content: "Document Title"; font-size: 9pt; font-style: italic; }
  @bottom-right { content: counter(page); font-size: 9pt; }
}

@page :left {
  @top-left { content: "Book Title"; font-size: 9pt; font-style: italic; }
  @bottom-left { content: counter(page); font-size: 9pt; }
}

@page :first {
  @top-left { content: none; }  @top-right { content: none; }
  @bottom-left { content: none; }  @bottom-right { content: none; }
}

@page :blank {
  @top-center { content: none; }
  @bottom-center { content: "This page intentionally left blank"; font-size: 9pt; color: #999; }
}
```

## Named Pages

Different sections can have different page configurations.

```css
.title-page { page: title; }
.chapter     { page: chapter; }
.appendix    { page: appendix; }

@page title {
  margin: 0;
  @top-center { content: none; }
  @bottom-center { content: none; }
}

@page chapter {
  @bottom-center { content: counter(page); }
}

@page appendix {
  @top-center { content: "Appendix"; font-size: 9pt; }
  @bottom-center { content: "A-" counter(page); font-size: 9pt; }
}
```

## CSS Counters

```css
body { counter-reset: chapternum figurenum tablenum; }

h1.chapter::before {
  counter-increment: chapternum;
  content: "Chapter " counter(chapternum) " — ";
}

figcaption::before {
  counter-increment: figurenum;
  content: "Figure " counter(chapternum) "." counter(figurenum) ". ";
}

.table-caption::before {
  counter-increment: tablenum;
  content: "Table " counter(chapternum) "." counter(tablenum) ". ";
}
```

## Bleed and Crop Marks (Professional Printing)

```css
@page {
  bleed: 3mm;
  marks: crop cross;
}

.full-bleed {
  width: calc(100% + 6mm);
  margin-left: -3mm;
  margin-right: -3mm;
}
```

## Links on Paper

**Never dump raw URLs inline.** Better approaches:

1. **Numbered footnotes** — superscript numbers, collected URL list at bottom. Use CSS counters. In React, render conditionally for print.
2. **QR code** — single QR code linking to the original page URL, shown via `.print-only`.
3. **Combination** — footnote numbers for important links + one QR code for the full page.

### Footnote Styling

```css
@media print {
  /* Sub/superscripts: see OpenType section in typography.md */

  sup.fnref {
    font-size: 75%;
    line-height: 0;
    vertical-align: super;
    padding-left: 0.1em;
  }

  .footnotes {
    margin-top: 2em;
    border-top: 0.5pt solid #000;
    padding-top: 1em;
    font-size: 8pt;
    break-inside: avoid;
  }

  .footnotes li { word-break: break-all; margin-bottom: 0.2em; }
}
```

### Abbreviations

```css
@media print {
  abbr[title]::after { content: " (" attr(title) ")"; }
}
```

## Images

```css
@media print {
  img {
    max-width: 100% !important;
    height: auto !important;
    break-inside: avoid;
  }
  figure { break-inside: avoid; margin: 8pt 0; }
  figcaption { font-size: 9pt; font-style: italic; margin-top: 4pt; }

  /* Hide decorative images */
  img[role="presentation"], img[alt=""] { display: none; }
}
```

Use `<picture>` with `media="print"` source for high-res print variants.

## Tables

**Design principles:** Size columns to their data, not the page width. Minimize borders — use rules in one direction only when needed. Group related rows with whitespace (Gestalt law of proximity), not zebra stripes.

```css
@media print {
  table { border-collapse: collapse; break-inside: auto; }
  thead { display: table-header-group; }
  tfoot { display: table-footer-group; }
  tr { break-inside: avoid; }
  caption { caption-side: bottom; font-size: 9pt; font-style: italic; margin-top: 4pt; }
  td, th {
    border-bottom: 0.5pt solid #ccc;
    padding: 0.125em 0.5em 0.25em 0.5em;  /* asymmetric: less top, more bottom */
    font-size: 10pt;
    line-height: 1;                         /* tight in cells — columns are narrow */
    font-variant-numeric: lining-nums tabular-nums;
  }
  thead th {
    border-bottom: 1pt solid #000;
    font-weight: 700;
  }
}
```

### Decimal Alignment (CSS Text Level 4)

```css
td.numeric { text-align: "." center; }  /* align on decimal point */
```

Not yet widely supported in browsers — works in Prince/WeasyPrint. Progressive enhancement.

### Oblique Column Headings

When headings are longer than data, rotate to save horizontal space:

```css
th.rotated {
  transform: rotate(-60deg);
  transform-origin: bottom left;
  white-space: nowrap;
}
```

## Code Blocks

```css
@media print {
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow: visible;
    break-inside: avoid;
    background: #f8f8f8 !important;
    color: #333 !important;
    border: 1px solid #ccc;
    padding: 8pt;
    font-size: 9pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  :not(pre) > code {
    background: #f0f0f0 !important;
    color: #333 !important;
    padding: 1pt 3pt;
    font-size: 90%;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
```

## Blockquotes

```css
@media print {
  blockquote {
    border-left: 3pt solid #333;
    padding-left: 12pt;
    margin-left: 0;
    font-style: italic;
    break-inside: avoid;
  }
}
```

## Section Breaks / Fleurons

For scene or section breaks within chapters, style `<hr>` as a decorative separator:

```css
@media print {
  hr {
    border: none;
    text-align: center;
    margin: 1.5em 0;
  }
  hr::after {
    content: "* * *";               /* or a fleuron: "❧" or "§" */
    letter-spacing: 0.5em;
    font-size: 12pt;
  }
}
```

## Print Source Notice

```css
.print-source-notice { display: none; }
@media print {
  .print-source-notice {
    display: block;
    margin-top: 2em;
    padding-top: 1em;
    border-top: 0.5pt solid #ccc;
    font-size: 8pt;
    color: #666 !important;
  }
}
```
