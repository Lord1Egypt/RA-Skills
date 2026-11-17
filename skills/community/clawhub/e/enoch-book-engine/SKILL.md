---
name: enoch-book-engine
description: Create or edit books with the Enoch Book Engine, including strict B5 pages, inline SVG diagrams, and mandatory screenshot-based visual QA.
---

# Enoch Book Engine

Use this skill when creating or editing a book in an Enoch Book Engine repository. The
engine makes fixed-layout B5 books from one-concept-per-page HTML, `book.json`, and
inline SVG diagrams or photographs.

## Source rules

- Edit `books/<slug>/<slug>.html`, `book.json`, `VOICE.md`, and `blocks.md`.
- Never hand-edit generated `book.html`.
- Books live exactly at `books/<slug>/` so their `../../engine/` links work.
- Keep one concept per `<section class="sheet bb">`.
- Keep diagrams as inline SVG. Give every SVG `<text>` an explicit `fill`.
- Put logos and brand lockups in a `.logo` band with an `<img>` or inline `<svg>`; its
  `contain` styling keeps the whole mark visible. Do not put a logo in `.photo`.
- Do not invent facts, numbers, quotations, or personal stories.
- Never add print CSS that changes sizes, fonts, or images.

## Required verification

After every page or layout change, run:

```bash
npm run verify -- books/<slug>
```

This builds the book, checks that every page is `0 mm` overflow-free, creates a PNG for
every page, and runs structural checks on diagrams. The first run intentionally stops
with exit code 2 and lists the screenshots that require review.

Open every listed block screenshot. Give extra attention to pages marked `[DIAGRAM]` or
`[LOGO]`: check card alignment, arrow routing, label clipping, spacing, colour roles,
logo containment, and whether the picture communicates the same idea as the prose. Also
inspect photo crops when a page has a photograph. Do not claim the book is finished
until the visual review is complete, then run:

```bash
npm run verify -- books/<slug> --ack-visual
```

The acknowledgement is a workflow gate, not proof that a machine can judge design.

## Authoring guidance

Read `AGENTS.md` and the relevant references in `.claude/skills/block/` before writing a
new page. Trim words when a page is full. Never shrink a diagram's `viewBox` to hide an
overflow or clip a drawing.

## Provenance

Keep the repository's MIT license and upstream notice intact when distributing a
derivative. Rebranding and new code are fine; do not remove or falsify authorship,
license, or source history.
