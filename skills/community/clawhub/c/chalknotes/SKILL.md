---
name: chalknotes
description: "Udemy course extraction + hand-drawn Excalidraw PDF notes."
category: note-taking
version: 1.0.0
author: Hermes Agent
license: MIT-0
metadata:
  hermes:
    tags: [udemy, curriculum, course-info, excalidraw, study-notes, pdf, education]
---

# Chalknotes

Extract any Udemy course's full curriculum and context, then turn lecture
transcripts into hand-drawn-style study notes (Excalidraw scene → PDF).
Two modes, one skill:

- **A — Extract course info**: sections, lectures, player-accurate numbering,
  instructor, objectives, free previews. No login required.
- **B — Generate notes**: paste a transcript → styled multi-page PDF notes
  with diagrams, filed into per-section folders.

## When to Use

- User shares a Udemy course (name or URL) and wants its structure/context.
- User pastes lecture transcripts and wants study notes as PDF.
- User wants notes auto-organized to mirror the course curriculum.

Confirm the notes root folder with the user on first use (default:
`~/udemy-notes/<course-slug>/`). Ask whether they want PDF only (default)
or also the editable `.excalidraw` scene.

## Part A — Extract course info

### Proven access route (do not deviate)

1. **The managed automation browser (`browser_exec`) FAILS on udemy.com** —
   Cloudflare "Just a moment..." never clears for it. Do not loop on it.
   Wayback/archive.today have no snapshots of course pages — dead end.
2. **The desktop in-app preview browser WORKS, no login** — the public
   course landing page exposes the entire curriculum:
   - Find the URL: ask the user, or `web_search` the exact course title +
     "Udemy" (slug pattern: `udemy.com/course/<slug>/`).
   - `desktop_preview` action=open with the course URL.
   - `drive_preview` action=elements → click **"Expand all sections"**
     (its label flips to "Collapse all sections" — that confirms success).
   - `desktop_preview` action=read, paged by char offsets (start/count),
     until `total_chars` is covered. The curriculum block runs from the
     first section title to the last lecture, between "Course content"
     and "Requirements"; instructor bio/description/reviews follow it.
   - On non-desktop surfaces without the preview pane, fall back to any
     real-browser tool the environment provides (e.g. a chrome-devtools
     or Playwright MCP attached to the user's own Chrome profile).
3. If login is ever truly needed (player-only data): the user logs in
   manually in the browser pane, or `browser_vault` save_login (masked
   prompt). Never ask for or type passwords in chat.

### Parsing rules (numbering matches the course player)

Raw block shape per section:

```
Section Title
N lectures • <length>
Lecture Title
[Preview]            <- optional marker line
mm:ss
...
Quiz                 <- standalone line, UNNUMBERED
```

- Section header = a title line immediately followed by `N lectures? • ...`.
- A lecture = title, optional `Preview` line, then a `\d+:\d{2}` duration.
  **Pitfall:** `Preview` sits BETWEEN title and duration — naive parsers
  number the duration string as a lecture and drift.
- Items with no duration = coding exercises/articles; they DO consume
  numbers. `Quiz` lines do NOT. Resource downloads ("Download Resources",
  0:0x) DO.
- Global numbering = sequential over all non-quiz items across sections.
  The declared "N lectures" counts videos only (exercises are extra).
- Save the raw block to `raw.txt`, then run
  `python scripts/parse_curriculum.py raw.txt -o curriculum.json
  --name "<course>" --url "<url>"` (stdlib only). It prints per-section
  number ranges — **validate against the user's course-player screenshot
  when available**, and check the video count equals the page's declared
  total ("345 lectures" etc.).

### Also extract (course context)

From the same page text: title/subtitle, instructor name + bio + teaching
style, last-updated, stats (sections/lectures/hours/exercises/articles/
resources/rating), "What you'll learn" bullets, description/learning path,
and free-preview lectures (titles with a `Preview` marker — the parser
flags them `preview: true`). Save as `course-info.json` beside
curriculum.json.

### Storage convention

Per-course data dir: `~/udemy-course-data/<course-slug>/`
(curriculum.json + course-info.json + raw.txt). Reuse existing data on
later runs — don't re-extract. Keep data OUT of the notes folder: the
notes root holds only section folders with PDFs.

## Part B — Generate notes (hand-drawn template)

### Template spec

Decoded from a real student's Excalidraw-exported notes; reproduces the
look of hand-written board notes:

- White canvas, single left column, A4 portrait pages (794x1123 px), margin 56.
- Main title: Virgil hand-drawn (fontFamily 1), magenta `#c2255c`, ~36px, centered.
- Section headings: Virgil ~20-24px — orange `#e8590c` main sections, green
  `#2f9e44` solutions/secondary, red `#e03131` problems/drawbacks, magenta
  for command emphasis / important notes.
- Body: Cascadia mono (fontFamily 3), blue `#1971c2`, 16px; `-->` for
  definitions/sub-points, `*` bullets, `1. 2. 3.` steps, `Eg:` examples,
  `OR` between alternate definitions.
- Commands: magenta mono inside thin dark-outlined rounded boxes with a
  gray `Commands:` label (when the lesson has commands).
- Diagrams: pale-yellow `#ffec99` rounded nodes, border `#f08c00`, gray
  arrows (dotted for loop-back edges), blue mono labels.
- Content stays faithful to the transcript; no invented material.

### Folder organization

Mirror the course curriculum — one subfolder per section, PDFs named by
the course-wide lecture number:

```
<notes-root>/
  Section 1 - <Section Title>/
    01 - <Lecture Title>.pdf
    02 - <Lecture Title>.pdf
  Section 3 - <Section Title>/
    06 - <Lecture Title>.pdf
```

Match each transcript to its lecture by title (fuzzy ok — player titles
sometimes differ slightly from the public page), then file as
`Section N - Title/NN - Lecture Title.pdf`. Skip resource-download items.

### Procedure

0. Load the course's curriculum.json (match lecture → section folder +
   number `n`) and course-info.json (instructor style, learning path).
   Auto-generated transcripts mis-hear words (e.g. "strained"=trained,
   "clear email"=clean email) — normalize silently, never invent content.
   Free-preview lectures (`preview: true`) can be fetched from the public
   page if a transcript is missing.
1. Work in a scratch dir (e.g. `$TMPDIR/notes-work/`), never in the notes
   root. `scripts/make_notes.py` is a stdlib-only layout library — copy
   `examples/example_board.py` as a starting driver, rewrite its content
   sections from the transcript, keep the helpers. See
   `references/excalidraw-schema.md` for element rules. Outputs
   `NN-slug.excalidraw` + same-layout `NN-slug.html`.
2. Run the driver: it prints per-page end-y (must stay < 1123) and the
   overlap count (must be 0). Pages stack vertically with a 90px gap;
   each page gets a named `frame` so the user can export per page on
   excalidraw.com.
3. PDF: the HTML uses @font-face Virgil/Cascadia from
   `https://excalidraw.com/Virgil.woff2` / `Cascadia.woff2` (both live).
   In `browser_exec`: open the HTML via file://, wait for
   `document.fonts.check('16px Virgil') && document.fonts.check('16px Cascadia')`,
   then `cdp('Page.printToPDF', printBackground=True, preferCSSPageSize=True)`
   and save the base64 to the PDF path. Any headless-Chrome tool works.
4. Verify visually: rasterize PDF pages (pypdfium2, or the `pdf` skill's
   `pdf_page_image.py` if installed) and inspect each page with
   `vision_analyze` for overlaps/overflow/cut-off text.
5. Optional engine check: render the scene with the real Excalidraw React
   component (see Pitfalls) to confirm the `.excalidraw` loads.
6. Move ONLY the final PDF into the notes root (create the section folder
   if new). Deliver with one `MEDIA:` line per PDF plus a one-list content
   summary. Leave intermediates in scratch; deliver the `.excalidraw`
   only if the user asked for it.

## Pitfalls

- `desktop_preview read` is char-paged; loop start += count until
  total_chars. `drive_preview` refs die on navigation — re-run elements
  after any page change. Click results return deltas; trust them.
- Public-page lecture titles can differ slightly from player titles;
  match fuzzily, keep the player's numbering. Coupon query params
  (?couponCode=...) are harmless. Prices/ratings are live data — note the
  extraction date if cited.
- Large JS payloads (>~10KB) in one `browser_exec` js() call fail with
  "Separator is found, but chunk is longer than limit" — chunk into ~6KB
  appends to a window variable if ever needed.
- excalidraw.com file loading cannot be automated reliably: no persistent
  file input, synthesized DragEvent drops are ignored, showOpenFilePicker
  needs a user gesture. Verify via a local HTML page instead: esm.sh
  imports of `@excalidraw/excalidraw@0.17.6` come back CJS-wrapped — use
  `EX.Excalidraw || EX.default.Excalidraw || EX.default` (same for React /
  createRoot), CSS from
  `https://esm.sh/@excalidraw/excalidraw@0.17.6/dist/prod/index.css`,
  `initialData={elements, appState:{viewBackgroundColor:'#ffffff'}}`,
  `viewModeEnabled: true`, then screenshot.
- Excalidraw text does not wrap: the library pre-wraps (mono ~0.6em/char,
  Virgil ~0.5em/char) and sizes heights = lines x fontSize x 1.25.
- `write_file` stale-write guard: read_file before overwriting session files.
