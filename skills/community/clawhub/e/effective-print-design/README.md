# Effective Print Design

Print CSS that doesn't look like print CSS.

A [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code) that turns Claude into an InDesign operator — fluent in Bringhurst, Butterick, and Tschichold, building with pure HTML/CSS.

## The Problem

Most printed web pages look terrible. Chopped headings, orphaned lines, invisible backgrounds, raw URLs nobody will type, rivers of whitespace in justified text. Print is an afterthought — and it shows.

## What This Skill Does

Gives Claude deep knowledge of print typography, paged media, and web-to-print production. Ask for a resume, invoice, article, book, or report and get CSS that holds up at 300 DPI.

**Typography** — proper `pt` sizing, optical sizing, OpenType features, hyphenation, justified text done right, locale-correct quotation marks for 12 Western languages.

**Layout** — `@page` rules, page simulation on screen, baseline grids, fragmentation control, sidebar + main grid patterns.

**Page Features** — running headers/footers, CSS counters, crop marks, footnote-style links, table header repetition, drop caps.

## Install

Via [skill.sh](https://skill.sh):

```bash
npx skill.sh install sebastian-software/effective-print-design
```

Or directly via Claude Code:

```bash
claude skill add effective-print-design
```

Activates automatically when you mention `@media print`, `@page`, print stylesheets, or ask for a document that needs to look good on paper.

## What's Inside

| File | What it covers |
|------|----------------|
| `SKILL.md` | Core principles, quick decision guide, print vs. screen |
| `references/typography.md` | Font stacks, sizing, OpenType, text-wrap, hyphenation, hierarchy |
| `references/layout.md` | @page, page simulation, grids, fragmentation, baseline rhythm |
| `references/page-features.md` | Headers/footers, counters, bleed, links, tables, code blocks |
| `references/locale.md` | Quotes, dashes, number formatting, spacing for 12 locales |

## Built On

Bringhurst's *Elements of Typographic Style*, Butterick's *Practical Typography*, Rutter's *Web Typography*, van Aaken's *Webtypobuch*, Stein's *Webfont Handbook*, Santa Maria's *On Web Typography* — plus MDN, Smashing Magazine, A List Apart, and years of collective print CSS pain.

## License

[MIT](LICENSE.md) — Copyright (c) 2026 [Sebastian Software GmbH](https://sebastian-software.de)
