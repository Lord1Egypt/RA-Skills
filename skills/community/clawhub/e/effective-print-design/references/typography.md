# Typography Reference

Detailed CSS for print typography. See SKILL.md for principles.

## Font Sizes

CSS `pt` and Word `pt` are identical: 1 pt = 1/72 inch. Different fonts at the same pt size appear visually different — always verify; adjust by half-points (10.5pt, 11.5pt) if needed.

| Element | Size | Line-height | Notes |
|---------|------|-------------|-------|
| Body text | 11pt | 1.35–1.4 | Serif or sans — depends on CI |
| h1 | 22–24pt | 1.05–1.1 | Below 1.0 OK for all-caps display |
| h2 | 16–18pt | 1.1–1.15 | |
| h3 | 13–14pt | 1.15–1.2 | |
| h4 | 11pt bold | 1.2–1.3 | Same size as body, bold |
| Sidenotes / marginalia | 8pt | 1.2–1.25 | |
| Captions / footnotes | 8–9pt | 1.2–1.25 | Never below 75% of body size |
| Code blocks | 9pt | 1.3–1.4 | Monospace |

**Heading line-height below 1.0** is acceptable for large display headings (24pt+). Touching ascenders and descenders creates visual cohesion. For all-caps headings there are no descenders, so line-height can go even tighter.

**Line-height validation:** Look at a capital H, mentally double its height. If the doubled letter reaches the baseline of the line above, line-height is too small for body text (van Aaken's "double cap-height" test).

**Typographic color:** Heavier/darker typefaces need more line-height; lighter ones need less. The fixed 1.35–1.4 range is a starting point — adjust by squinting at the text block and evaluating its overall gray value.

**Low x-height as space saver:** Fonts with small x-heights optically increase line spacing without changing the value. For tight page budgets (resumes, dense reports), deliberately choose a low-x-height font.

**Functional text** (captions, labels, footnotes) should never be smaller than 75% of body size. Choose faces with open, distinct letterforms where I/l/1 and O/0 are clearly distinguishable.

### Document-Type Variations

| Property | Resume / CV | Article / Blog | Book / Report |
|----------|-------------|----------------|---------------|
| Body size | 9.5–10.5 pt | 11 pt | 11–12 pt |
| Line-height | 1.3–1.4 | 1.35 | 1.4–1.5 |
| Body font | Serif or Sans (CI) | Serif preferred | Serif preferred |
| Heading font | Contrasting pair | Sans-serif | Sans-serif or matching serif |
| Text-align | Left (not justified) | Justify | Justify |
| Hyphens | No | Yes | Yes |

## Modular Scale Ratios

Use named musical intervals as type scale ratios for intentional hierarchy:

| Ratio | Name | Use case |
|-------|------|----------|
| 1.125 | Major second | Compact/dense (resumes, data-heavy) |
| 1.200 | Minor third | General print (default recommendation) |
| 1.250 | Major third | Slightly more dramatic |
| 1.333 | Perfect fourth | Editorial, magazine layouts |
| 1.414 | Augmented fourth | Academic papers, formal publications |

For print, **minor third (1.2)** or **major second (1.125)** work best — print needs less size contrast than screen.

**Double-stranded scale:** For more nuanced sizing, use two meaningful values — e.g., body size (11pt) and column width (in pt) — with your chosen ratio to generate sizes with built-in relationships to the page geometry (Tim Brown's technique).

## Font Choice

Both serif and sans-serif work well in print. The choice depends on brand identity. Classic pairings:

- **Serif body + sans-serif headings** — traditional, bookish
- **Sans-serif body + serif headings** — modern, clean
- **All-serif** — academic, literary
- **All-sans** — corporate, technical

### Selection Criteria for Body Text

- **Stroke contrast:** Low-to-medium contrast creates smooth reading rhythm. High contrast (Bodoni, Didot) produces uneven texture — reserve for display/headlines only.
- **Aperture openness:** Open counters and apertures (the openings in c, e, s, a) aid legibility, especially at small sizes (8–9pt). Closed apertures (Helvetica) make letterforms hard to distinguish.
- **Typographic color:** Aim for a medium gray value when squinting at a text block. Too dark (heavy strokes) or too light (thin strokes) both reduce readability.
- **Personality restraint:** Body type must be restrained — any visual quirk (whimsical tail on g, unusual ligatures) repeats thousands of times and becomes a distraction. Save personality for display type.

### Headlines

- **Condensed or slightly narrow typefaces** fit more characters per line on fixed-width print pages, preventing single-word orphan lines and awkward breaks that `text-wrap: balance` cannot always solve.
- Condensed widths also create strong visual contrast with regular-width body text.

## Font Pairing Rules

- **Match x-heights** between paired typefaces — if x-heights differ, fonts look mismatched even at correct point sizes
- **Match historical period** — pair humanist serif with humanist sans (e.g., Palatino + Gill Sans), not with geometric sans (Futura)
- **Match structural skeleton** — typefaces sharing the same geometry (dynamic/rational/geometric) pair well regardless of serif/sans classification (Rutter's skeleton/flesh/skin model)
- **Contrast on one axis only** — vary serif/sans *or* weight *or* width, not all three
- **Max 2–3 typefaces** per document — each additional font dilutes hierarchy
- **Superfamilies** are the safest pairing: Source Sans + Source Serif, Noto Sans + Noto Serif, Lucida Sans + Lucida Serif
- **Same designer** — typefaces from the same designer often share subtle stylistic thumbprints (e.g., Eric Gill's Joanna + Gill Sans)
- **Same foundry** — some foundries explicitly design complementary families and list recommended pairings
- **Never pair two similar fonts** — two different serifs next to each other creates tension without clear hierarchy

## Font Safety

Never declare `font-weight: bold` or `font-style: italic` unless the loaded font actually includes that weight/style variant. Browsers synthesize **faux bold** (by geometrically thickening strokes) or **faux italic** (by slanting) when the real variant is missing — the result looks crude, especially at 300 DPI on paper.

```css
/* Prevent browser from generating faux bold/italic */
body { font-synthesis: none; }
```

Verify in DevTools that every `font-weight`/`font-style` request is matched by an actual font file.

## Font Stacks (System Fonts)

```css
@media print {
  /* Serif */
  body {
    font-family: Charter, 'Bitstream Charter', 'Sitka Text', Cambria, Georgia, serif;
    font-size: 11pt;
    line-height: 1.35;
    font-size-adjust: 0.465;           /* normalize x-height across fallbacks */
    font-optical-sizing: auto;          /* enable optical size axis on variable fonts */
    font-synthesis: none;               /* prevent faux bold/italic */
  }
  /* Sans-serif (alternative) */
  body {
    font-family: Inter, Roboto, 'Helvetica Neue', 'Arial Nova', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.4;
  }
  code, pre {
    font-family: 'Courier New', Courier, monospace;
    font-size: 9pt;
  }
}
```

## Selective Glyph Substitution

Use `unicode-range` to mix decorative glyphs from a different typeface — a classic typographic technique (e.g., a distinctive ampersand):

```css
@font-face {
  font-family: DecorativeAmpersand;
  src: url(spumante.woff2) format("woff2");
  unicode-range: U+26;  /* only the & character */
}
h1, h2 {
  font-family: DecorativeAmpersand, Charter, serif;
}
```

The browser uses the decorative font only for matching characters; everything else falls through to the next font in the stack.

## Optical Sizing

Variable fonts with an `opsz` axis automatically adapt stroke weight and detail to the rendered size. German typography distinguishes three size categories:

- **Konsultationsgrößen** (6–8pt) — captions, footnotes: thicker strokes, open counters
- **Lesegrößen** (9–13pt) — body text: balanced for sustained reading
- **Schaugrößen** (14pt+) — headings, display: refined details, tighter letterfitting

```css
body { font-optical-sizing: auto; }        /* default — enable for all sizes */

/* Manual control for variable fonts */
h1      { font-variation-settings: 'opsz' 48; }
caption { font-variation-settings: 'opsz' 8; }

/* Custom axes (beyond standard wght/wdth/opsz/ital/slnt) */
.display { font-variation-settings: 'opsz' 48, 'XHGT' 1.0, 'CONT' 50; }
```

Fonts with good optical sizing: **Roboto Flex**, **Source Serif 4**, **Fraunces**, **Recursive**.

## `font-size-adjust`

Normalizes x-height across fallback fonts. If Charter is missing and Georgia loads, the browser adjusts Georgia's size to match Charter's x-height ratio. Now in Baseline (Chrome 127+, Firefox 3+, Safari 17.4+).

```css
body {
  font-family: Charter, Cambria, Georgia, serif;
  font-size-adjust: 0.465;  /* Charter's x-height / font-size ratio */
}
```

Even 0.5pt differences in apparent size matter on paper — `font-size-adjust` prevents this.

## Text Wrapping & Hyphenation

```css
@media print {
  /* Headings: balanced lines (prevents single-word last line) */
  h1, h2, h3, h4, h5, h6 {
    text-wrap: balance;
    hyphens: none;
  }

  /* Body: pretty wrapping (multi-line optimizer like InDesign's paragraph composer) */
  p, li, dd, blockquote {
    text-wrap: pretty;
    text-align: justify;
    hyphens: auto;
    -webkit-hyphens: auto;
    hyphenate-limit-chars: 6 3 2;       /* word min 6, 3 before / 2 after hyphen */
    -webkit-hyphenate-limit-before: 3;
    -webkit-hyphenate-limit-after: 2;
    hyphenate-limit-lines: 2;           /* max 2 consecutive hyphenated lines */
    -webkit-hyphenate-limit-lines: 2;
    hyphenate-limit-zone: 8%;           /* allow slight rag to reduce hyphenation */
    hyphenate-limit-last: always;       /* prevent stub of hyphenated word as last line */
  }

  /* Captions: balanced like headings */
  figcaption, caption, summary {
    text-wrap: balance;
  }
}
```

**`text-wrap: pretty`** — Chrome 117+, Safari 19+. **`text-wrap: balance`** — Chrome 114+, Firefox 121+, Safari 17.5+. **`hyphens: auto`** requires `lang` attribute on `<html>`.

**`<wbr>`** (word break opportunity) — insert in HTML where long unbreakable strings (URLs, chemical names, identifiers) may break across lines *without* inserting a hyphen. Useful for print where long strings must fit within the measure.

**`&shy;`** (soft hyphen, U+00AD) — suggests a break point where a hyphen *will* appear if the browser breaks there. Use for compound words, technical terms, or proper nouns that `hyphens: auto` gets wrong. The hyphen is invisible unless the break occurs. For large-scale automation, server-side hyphenation libraries (e.g., Hypher, Hyphenopoly) can insert soft hyphens at build time.

### Justified Text: Mandatory Preconditions

Justify **only** when both conditions are met:

1. **Line length ≥ 50 characters** (ideally 60+)
2. **Functioning hyphenation** (`hyphens: auto` + `lang` attribute)

Without both, word-spacing rivers are unacceptable. For narrow columns (sidebars, captions), always use `text-align: left`.

### Word Spacing for Justified Text

A small negative `word-spacing` reduces rivers in justified text, mimicking InDesign's "desired word spacing" (~85–90% of default).

```css
p {
  text-align: justify;
  word-spacing: -0.05em;  /* tighten default word gaps slightly */
}
```

## Paragraph Separation

Two conventions — choose based on document type:

### Spacing (Web/Article Convention)

```css
p { margin-bottom: 0.8em; }
```

Default for articles, reports, resumes. Familiar from screen.

### Indentation (Book/Literary Convention)

Traditional European/German book typography. Saves vertical space, better for long-form reading.

```css
p { margin: 0; }
p + p { text-indent: 1em; }  /* indent all paragraphs except the first */
```

**Rules:**
- First paragraph after heading, figure, blockquote, or list: **no indent** (`p + p` handles this automatically)
- Indent size: **1em** (Bringhurst standard). For optical precision, match the line-height (e.g., if line-height is 15.4pt, use `text-indent: 15.4pt`) to create a "neat square of white space."
- Never combine indentation with vertical spacing — use one or the other

### Standfirst / Lead Paragraph

A short opening paragraph set in a larger or different style to introduce the article. Common in editorial/magazine design.

```css
article > p:first-of-type {
  font-size: 1.25em;
  line-height: 1.3;
  font-weight: 300;    /* or a different typeface */
}
```

### Hanging Indent for Bibliographies

For reference lists, use a hanging indent so the first line protrudes while continuation lines are indented:

```css
.bibliography li {
  text-indent: -1.5em;
  margin-left: 1.5em;
}
```

## OpenType Features

```css
@media print {
  body {
    font-variant-ligatures: common-ligatures;
    font-kerning: normal;
  }

  /* Old-style (lowercase) figures for body text */
  p, li {
    font-variant-numeric: oldstyle-nums proportional-nums;
  }

  /* Lining (uppercase) figures for tables and headings */
  table {
    font-variant-numeric: lining-nums tabular-nums;
  }
  h1, h2, h3 {
    font-variant-numeric: lining-nums;  /* old-style looks wrong next to capitals */
  }

  /* Proper subscripts and superscripts (font glyphs, not browser shrink/shift) */
  sub { font-variant-position: sub; }
  sup { font-variant-position: super; }
  @supports (font-variant-position: sub) {
    sub, sup { vertical-align: baseline; font-size: inherit; }
  }

  /* Small caps for abbreviations */
  abbr {
    font-variant-caps: all-small-caps;
    letter-spacing: 0.05em;
  }

  /* Hanging punctuation (Safari only — progressive enhancement) */
  article p {
    hanging-punctuation: first allow-end last;
  }
  /* Cross-browser fallback: negative indent sized in ch units */
  blockquote p { text-indent: -1ch; }

  /* Drop cap */
  article > p:first-of-type::first-letter {
    initial-letter: 3;
    -webkit-initial-letter: 3;
    font-weight: bold;
    margin-right: 0.05em;
  }
  /* Variants: sunken cap (extends above text) and raised cap */
  /* initial-letter: 3 2;  — spans 3 lines, baseline on line 2 (sunken) */
  /* initial-letter: 3 1;  — spans 3 lines from baseline of line 1 (raised) */

  /* Alternative opening: first-line run-in with small caps */
  /*
  article > p:first-of-type::first-line {
    font-variant-caps: small-caps;
  }
  */
}
```

**Warning:** The `font` shorthand property resets `font-kerning` to its initial value. If you use `font:`, re-declare `font-kerning: normal` afterward.

## Stylistic Alternates

For fonts with OpenType alternates — stylistic sets, swash, contextual alternates:

```css
@font-feature-values "My Font" {
  @styleset { clean: 1; }       /* map name to ss01 */
}

body {
  font-variant-alternates: styleset(clean);  /* use named set */
  font-variant-alternates: contextual;       /* context-sensitive alternates */
}

/* Or directly via font-feature-settings */
h1 { font-feature-settings: 'ss01' 1, 'swsh' 1; }
```

## Special Characters

- **Hyphen** `-` only for compound words and hyphenation
- **En dash** `–` for ranges without spaces: 10–20, Jan.–Mar. Prevent orphaned dashes with `&nbsp;` before the dash
- **Narrow no-break space** (U+202F, `&#8239;`) between numbers and units (38 cm, 128 kB/s, § 21), abbreviation parts (z. B., d. h.), and initials (D. H. Lawrence). Prefer U+202F (non-breaking) over U+2009 (breaking thin space)
- **Multiplication sign** `×` (U+00D7, `&times;`) for dimensions: 210 × 297 mm — never the letter x
- **Minus sign** `−` (U+2212, `&minus;`) for subtraction — not a hyphen (shorter, sits higher)
- **Ellipsis** `…` (U+2026), not three periods
- **Apostrophe** `'` (U+2019), never a prime `'`
- **Brackets in italic text:** Keep parentheses and brackets upright — italic brackets have an awkward unbalanced stance

Locale-specific conventions (quotation marks, dashes, number formatting, French spacing) and typographic preprocessing tools — see [locale.md](locale.md).

## Letter-Spacing

- **Body text:** `normal` (never track lowercase body)
- **ALL CAPS / small-caps:** `letter-spacing: 0.05em` to `0.12em` + `font-variant-ligatures: no-common-ligatures` (ligatures must be disabled when letter-spacing is applied — a ligature is a single glyph whose internal spacing doesn't change with tracking, causing uneven gaps)
- **Large display headings:** `letter-spacing: -0.01em` (tighten)
- **Big, bold, wide display:** `letter-spacing: -0.03em` (the bigger/bolder/wider the font, the tighter the tracking)
- **Centered tracked text:** Apply `margin-right` equal to the negative `letter-spacing` to compensate for the trailing space on the last character:

```css
h1 {
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-right: -0.1em;  /* eliminate trailing space for true centering */
}
```

## Hierarchy Principles

1. Use **fewer heading levels** in print than on screen (3 usually suffice)
2. Differentiate by **weight, style, caps, or spacing** — not just size
3. **More space before** headings than after to group them with following content
4. **Gestalt law of proximity:** A multi-line heading's internal line-height must always be tighter than its margin-top/margin-bottom — otherwise readers mis-group heading lines with surrounding content
5. Modest scale (~1.2x between levels); print needs less contrast than screen
6. Use **`text-box-trim`** (Chrome 133+, Safari 18.2+) for optically precise vertical spacing

## Resume Typography

```css
h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.01em; }           /* Name: 18–22pt */
h2 { font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.08em;    /* Sections: 11–12pt */
     border-bottom: 0.5pt solid #000; }
h3 { font-size: 1rem; font-weight: 700; }                                     /* Job titles: 10–11pt */
.dates { font-size: 0.9rem; color: #555; text-align: right; }                 /* 9–10pt */
.contact { font-size: 0.9rem; }
```

## rem Scaling Trick

Set everything in `rem` so one root change scales the entire document. If the layout overflows, reduce to `9.5pt` — everything shrinks proportionally.

```css
html { font-size: 10pt; }
h1 { font-size: 2rem; }       /* 20pt */
h2 { font-size: 1.2rem; }     /* 12pt */
h3 { font-size: 1rem; }       /* 10pt */
p  { font-size: 1rem; }
.entry { margin-bottom: 0.6rem; }
```

## ATS (Applicant Tracking) Optimization

For resumes parsed by automated systems:

- Use semantic HTML5 (`<section>`, `<article>`, `<header>`)
- Avoid images for text content
- Disable ligatures: `text-rendering: optimizeSpeed`
- Use standard heading hierarchy (h1 for name, h2 for sections, h3 for entries)
