# Five Style Master Systems

Use style systems as complete design languages, not skins. **Every style in this file is bound to one or more named palette contracts with exact hex values.** The build must read the full `style-contract.json`; do not invent colors, font sizes, spacing, radius values, table styles, chart colors, connector widths, image crop rules, or footer styling at build time. If a style needs a new palette or token set, add it to this file first, then update the matching style contract fixture.

Reusable style contracts live under `styles/`:

- `consulting-light.json`
- `product-report.json`
- `technical-blueprint.json`
- `consulting-blueprint-hybrid.json`
- `editorial-knowledge.json`

Each fixture must pass:

```bash
python3 scripts/validate_contracts.py --style styles/<style-id>.json --strict
```

Global color usage rules (apply to every palette):

- `primary`: title bars, main color blocks, key structural elements, top-of-page header strips, large callout blocks.
- `accent`: data highlights, single-emphasis callouts, key numbers, focused labels. **Never use accent as a large fill or as a page background.**
- `background`: page base. The whole slide sits on this color.
- `neutrals` (3 grays): body text, secondary text, dividers, borders, subtle fills, table strokes. Choose values that harmonize with the palette.
- Reserve at least 70% of any slide for background + neutrals; primary and accent together should occupy at most ~30% of a slide's visual weight, with accent far less than primary.

---

## consulting-light

Boardroom, evidence-heavy, answer-first, decision-oriented. Use for formal reports, executive updates, market analysis, investor-style briefs, and McKinsey-like decks. White space, strong titles, restrained color, and clean proof components matter more than visual novelty.

Available palettes:

### `mckinsey` (default)

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#0A2233` | deep warm navy titles, header bars, primary structural blocks |
| accent | `#2C4A6E` | restrained steel blue single-emphasis data highlights, key callouts |
| background | `#FBFBF8` | micro-warm ivory page base |
| secondary-surface | `#F1EFEA` | warm neutral panel / table-header fills |
| neutral-900 (text) | `#2A2E35` | warm near-black body text, judgment titles |
| neutral-500 (muted) | `#7C7669` | warm muted text, source notes, captions |
| neutral-200 (border/fill) | `#E4E0D7` | warm dividers, table strokes, subtle card fills |

### `bcg`

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#0E3D28` | deep ink green titles, header bars, primary structural blocks |
| accent | `#3E7A55` | muted olive green single-emphasis data highlights, key callouts |
| background | `#FAF9F5` | micro-warm page base |
| neutral-900 (text) | `#2A2E35` | warm near-black body text, judgment titles |
| neutral-500 (muted) | `#7C7669` | warm muted text, source notes, captions |
| neutral-200 (border/fill) | `#E4E0D7` | warm dividers, table strokes, subtle card fills |

---

## product-report

Modern product strategy deck with metrics, roadmap, tradeoffs, operating decisions, and user/business evidence. Use for PRDs, MVP plans, retrospectives, roadmap proposals, and launch reviews.

Available palettes:

### `linear` (default)

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#232030` | warm near-black titles, header bars, primary structural blocks |
| accent | `#6B5B95` | muted lavender purple single-emphasis data highlights, key callouts |
| background | `#F6F5F2` | warm off-white page base |
| secondary-surface | `#EDEBE6` | warm neutral panel / table-header fills |
| neutral-900 (text) | `#2A2E35` | warm near-black body text, judgment titles |
| neutral-500 (muted) | `#7A746B` | warm muted text, source notes, captions |
| neutral-200 (border/fill) | `#E3DFD6` | warm dividers, table strokes, subtle card fills |

### `stripe`

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#14161A` | near-black titles, header bars, primary structural blocks |
| accent | `#3A5A8C` | restrained steel blue single-emphasis data highlights, key callouts |
| background | `#FAFAF7` | micro-warm page base |
| neutral-900 (text) | `#242526` | body text, judgment titles |
| neutral-500 (muted) | `#79746B` | warm muted text, source notes, captions |
| neutral-200 (border/fill) | `#E4E0D7` | warm dividers, table strokes, subtle card fills |

---

## technical-blueprint

Precise executable engineering deck with lanes, nodes, boundaries, failure modes, observability, and runbooks. Use when implementation detail is the audience's main need. Keep diagrams disciplined and avoid raw tool-screenshot aesthetics. Light-mode, formal technical whitepaper / RFC feel, print-friendly.

Available palettes:

### `ibm-whitepaper` (default)

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#2A5578` | restrained engineering blue titles, header bars, primary structural blocks, node outlines |
| accent | `#2A5578` | single-emphasis highlights (same as primary; rely on weight and isolation rather than a second hue) |
| background | `#FAFAF7` | micro-warm page base |
| secondary-surface | `#EFEDE7` | warm panel / code-block / table-header fills |
| neutral-900 (text) | `#2A2E35` | body text, judgment titles |
| neutral-500 (muted) | `#6E6A60` | secondary text, source notes, captions |
| neutral-200 (border/fill) | `#DAD5CB` | dividers, table strokes, subtle card fills |

When accent and primary are identical, use neutral-700 `#3B3A34` as the de-facto "second accent" for a second tier of emphasis (e.g. secondary nodes) so the deck does not collapse to monochrome.

---

## consulting-blueprint-hybrid

Formal consulting hierarchy with restrained technical blueprint accents. Use for Agent systems, automation workflows, architecture strategy, platform operating models, and technical decks for business audiences. The slide should feel like consulting output first and engineering blueprint second. Consulting-first, restrained amber-gold technical accent.

Available palettes:

### `deep-amber` (default)

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#1B2A42` | deep navy titles, header bars, primary structural blocks |
| accent | `#C69749` | muted bronze-gold single-emphasis highlights, key callouts |
| background | `#FAF9F5` | micro-warm page base |
| neutral-900 (text) | `#2D3340` | body text, judgment titles (slightly differentiated from primary navy) |
| neutral-500 (muted) | `#6E6A60` | warm secondary text, source notes, captions |
| neutral-200 (border/fill) | `#E4E0D7` | warm dividers, table strokes, subtle card fills |

Use accent `#C69749` sparingly: it is a highlight, not a fill. A small accent block, an underline beneath a number, or a single labeled arrow is enough.

---

## editorial-knowledge

Premium knowledge deck that turns longform writing into frameworks, contrasts, steps, mistakes, examples, and memorable ideas. Use for explainers, newsletters, courses, personal IP, and knowledge products. Paper texture, knowledge-blogger feel.

Available palettes:

### `warm-paper` (default)

| Token | Hex | Use |
| --- | --- | --- |
| primary | `#2B2621` | warm dark titles, header bars, primary structural blocks |
| accent | `#C65D3B` | muted terracotta single-emphasis highlights, key callouts |
| background | `#FBF8F1` | warm paper page base |
| neutral-900 (text) | `#4A423A` | body text, judgment titles (warm dark, harmonized with primary) |
| neutral-500 (muted) | `#857C70` | secondary text, source notes, captions |
| neutral-200 (border/fill) | `#E4DDCF` | dividers, table strokes, subtle card fills (warm beige) |
