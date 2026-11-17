# omni2docx — Markdown to Word · MD to DOCX (table restore)

Turns markdown into Chinese-typeset Word / HTML / presentation decks; feed it Omni Reader
parse results and one more layer appears — source-page anchored breaks, per-character
anchoring, speaker and timestamp tags, a multi-source provenance appendix.
**Not another markdown→docx converter**: generic converters only see the markdown and lose
the structured information Omni already computed during parsing (page anchors, heading
levels, frame/transcript metadata); this package maps that back into native objects.

## Three-minute start: works without omni-reader

After `pip install python-docx`, two commands produce a Word file you can hand over:

```bash
python scripts/build_docx.py --md out.md --out delivery.docx --profile gov --page-numbers
python scripts/validate_docx.py --md out.md --docx delivery.docx   # last line 判定 : PASS
```

The input is any markdown (agent-written, hand-written, exported from elsewhere); the output
is a Chinese-typeset Word file: Song/Hei fonts, real Heading levels with a visible TOC,
GFM tables, superscript footnotes and a notes section.
`--profile gov|legal|finance|default` switches the house style; for HTML use `render_html.py`,
for a presentation deck use `render_pptx.py`. There is no parse leg on this path — the
**cost** is losing source-page anchored breaks, per-character anchoring, timestamp/speaker
tags and the multi-source provenance appendix; those need omni-reader (see "First use" below).

One parse result, four deliverables by purpose: **docx** (fidelity, for
submission/editing), **HTML** (showcase — readable, shareable, printable),
**PPTX** (deck — bullets on slides, detail in speaker notes), **PDF** (print,
HTML through a headless browser).

## What it is / what it is not

| It is | It is not |
|---|---|
| grounded page anchors → native Word page breaks (page-level fidelity) | pixel-perfect layout cloning |
| official outline → real Heading levels + visible TOC | PPT layout cloning (PPTX output is a presentation deck, split by heading levels) |
| GFM tables / superscript footnotes + notes section / gray source tags | embedding image/audio bytes (Omni returns no bytes; text provenance tags are kept) |
| multi-source merge + auto "provenance appendix" (pages / timestamps / speakers) | investment advice, content creation |

## Three scenarios

1. **Agent output → deliverable document**: `--md` direct conversion of agent markdown, with professional CJK typography.
2. **Scanned PDF / non-editable files → editable Word**: `--page-marks` stamps "source page N" at every page boundary for proofreading against the original.
3. **Multi-source evidence merge → litigation documents etc.**: a `sources` array becomes one chapter per source + master TOC + provenance appendix; transcript/frame tags are directly quotable.

## Getting started (three steps)

**Install this skill**: `npx skills add huhoo/cue-awesome --skill omni2docx` - this line installs this package only; afterwards re-list installed skills and the name `omni2docx` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this whole directory into your host's supported skills location (`~/.workbuddy/skills/`).

Prerequisites: `python3` + `pip install python-docx`; scenarios ②③ additionally
require a connected omni-reader MCP (scenario ① does not). PPTX output needs
`pip install python-pptx`; `--pdf` needs a local Edge/Chrome/Chromium (skipped
with an explicit message if absent).

Connectivity test for the parsing leg of scenarios 2 and 3 (parsing runs through the omni-reader MCP inside your host; the conversion itself sends no requests), **written per route**: the host lists tools through the JSON-RPC `tools/list` handshake, and once connected that reply should show these names - a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), while a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total). The two routes have different counts, so one fixed number cannot judge both. Missing names mean not connected: scenarios 2 and 3 are unavailable and scenario 1 (`--md` direct output) is unaffected. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this package neither self-certifies nor runs either for you. Parsing spend follows the server reply; this package neither estimates nor pays it (see the first item under "Capability boundaries").

### First use: connect the Omni parsing channel

**Where to connect (three separate states: skill installed ≠ credential configured ≠ channel connected)**: `npx skills add sensedeal/cue-skills --skill cue-omni-reader` only puts the files in place - afterwards re-list installed skills and the name appearing proves just that, it does not create a connection. Configuring the credential is the second layer (official configuration page <https://cuecue.cn/hub/omni-reader>, key page <https://cuecue.cn/hub/api-key>; keep the key in your own credential store, never in chat and never echoed in a terminal). Channel connected is the third layer, judged per route as described above (three names remote-only, seven with a Bridge - one fixed count cannot judge both routes). Existing URL tools need no local install; local files need the audited Bridge, a minimum root grant, `doctor`, then a host reload/reconnect. Names showing up do not prove parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this package neither self-certifies nor runs either for you. **This package does not read credentials**: `CUE_API_KEY` belongs to the channel side, while this package's conversion and layout send no requests and never hold the credential. Parsing spend and any new-account grant follow the server's live policy (grants are stated in credits); this package neither estimates nor pays them and promises no unit price of any kind.

**No install, no error (qualified: only when you do not use the parsing leg, and your local input plus python-docx and friends are in place)**: without the channel only scenarios 2 and 3 (grounded rebuild / multi-source merge) are unavailable - what you lose is page-level anchor reconstruction and multi-source traceability; scenario 1 still works with zero credentials: `python scripts/build_docx.py --md output.md --out deliverable.docx --profile gov --page-numbers`, then validate on the same yardstick with `python scripts/validate_docx.py --md output.md --docx deliverable.docx`. That proves this package's own rendering, not the channel.

```bash
# ① agent markdown direct output (no intermediate JSON)
python scripts/build_docx.py --md output.md --out deliverable.docx --profile gov --page-numbers

# ②③ Omni parse rebuild: parse(grounded) → markdown+grounding (+ same-session read_outline) → intermediate JSON
python scripts/build_docx.py --json intermediate.json --out deliverable.docx --profile legal --page-marks

# Acceptance (mandatory): character-level CJK coverage at least 99% (the PASS threshold) + structure checks
python scripts/validate_docx.py --json intermediate.json --docx deliverable.docx

# Showcase: self-contained HTML (add --pdf to also export a print-ready PDF; --toc-depth caps TOC depth)
python scripts/render_html.py --json intermediate.json --out showcase.html --profile gov --page-marks --pdf

# Presentation: deck (bullets on slides, prose in notes); refine the outline first for long documents
python scripts/render_pptx.py --md slide-outline.md --out deck.pptx --profile finance --max-slides 30

# HTML / PPTX acceptance, same coverage yardstick (slide text + tables + speaker notes
# combined; includes out-of-bounds / overlap / tiny-font geometry audit)
python scripts/validate_html.py --json intermediate.json --html showcase.html
python scripts/validate_pptx.py --json intermediate.json --pptx deck.pptx
```

Omni discipline: use the agent-native MCP tools throughout (parse /
get_parse_status / read_outline / read_result) **within the same session** — do
not write spawn scripts around omni (cross-process read_* calls fail by design).

## Scenario profiles (--profile)

Typography is decided by the document's use scenario; presets are reference
values only: `gov` (GB/T 9704 official documents), `legal` (litigation),
`finance` (research reports), `academic` (papers), `default`. Any parameter can
be overridden via `--profile` with inline JSON or a .json file (fonts, sizes,
line spacing, indents, margins, table style).

Quality baseline: headings always black with per-level sizes, zero CJK fake
italics (CJK emphasis → bold), `--page-numbers` adds a footer PAGE field,
`--strip-emoji` removes decorative symbols.

## Capability boundaries (honest list)

- **Conversion and layout run on this machine; the scripts themselves issue no network requests.** Two conditions to state plainly: if the source markdown carries `http(s)://` image links, `--pdf` export lets the *browser* fetch them (that step needs network; if a fetch fails the slot stays empty — this skill does not download on your behalf, and local or non-`data:` image paths are rendered as a text note in HTML); and **for input obtained through omni parsing, that parsing's cost is whatever the server returns** — parsing is not this skill's capability, and it neither estimates nor pays for it.
- Fidelity is **page-level** (grounded); element-level bbox data is available via
  `detail=layout`, engine consumption is a later stage.
- `read_result` / `read_outline` are bound to a **same-session constraint**
  (`local_result_cache` lives with the bridge process); fine inside an agent-native session.
- Paragraphs spanning page boundaries belong to the page where they start.
- Complex markdown (nested tables, math) degrades to text; tables are layout-faithful, not pixel-faithful.
- CJK font names (SimSun, FangSong_GB2312, KaiTi…) are substituted automatically
  by Word/WPS on non-Windows systems — acceptance for format-regulated documents
  should happen on Windows/WPS.
- PPTX output is a presentation deck: slides split by heading levels, prose goes
  to speaker notes, `--max-slides` (default 80) truncates with a warning; no
  mechanical "one slide per source page" tiling.
- PDF is exported via HTML + headless browser printing; no native PDF layout engine.
- Letter-spaced OCR artifacts ("T h e y") cannot restore word boundaries and are
  left as-is; CJK inter-character spaces are removed normally.

## Acceptance

Each format ships its own validator, all judging on **character-level CJK
coverage** (PASS at ≥99%): `validate_docx.py` (plus anchor phrases and structure
counts), `validate_html.py` (plus TOC/anchors/source-page marks/self-containment),
and `validate_pptx.py` (slide text + table cells + speaker notes counted together,
plus empty-page/truncation checks). A real-corpus
matrix (xlsx / PDF reports / HTML / audio transcripts / docx / PPTX / JPG OCR /
1000-page PDF / truncated PDF / edge cases, across profiles) measured 100%
coverage on every case.

### Rule ids: what they check, why they fire, how to make them pass

Boundary first: **the ids are addresses for regression reporting, not capability promises.** Everything below quotes the values currently in the code;
the authoritative thresholds live in `scripts/validate_pptx.py` and `scripts/validate_docx.py` — where the two disagree, the code wins.
PPTX carries eight ids (PX-01, PX-02, PX-03, PX-04, PX-05, PX-06, PX-07, PX-08); DOCX carries two (DX-01, DX-02):

| Id | What it checks (current code) | Why it fires | How to make it pass |
|---|---|---|---|
| PX-01 | Character-level CJK coverage of the deck against the source markdown < 0.99 (slide text + table cells + speaker notes pooled) | Content never reached the deck: `--max-slides` (default 80) cut it, `--prose skip` dropped the body, or the source holds a block the renderer does not carry | Read the "missing CJK characters" list the validator prints, locate that text in the source; raise or drop `--max-slides`, and set `--prose` back to `notes`/`body` |
| PX-02 | Slide count = 0 | The source headings sit below `--section-level`/`--split-level`, so nothing splits | Lower the levels to the document's real heading depth, or have the agent distil an outline layer first |
| PX-03 | Empty slides > max(1, slides // 10) (empty = no text, table, picture or notes on the slide) | Consecutive headings with no content under them — usually splitting too finely, or the body was consumed by the previous page's limits | Merge the empty sections, lower `--split-level`, or relax `--max-chars`/`--max-bullets` so text actually lands on the page |
| PX-04 | Any shape whose XML contains `roundRect` (iron law: 0) | This renderer produces no rounded rectangles; a hit means an external template or a hand-added shape got in | Go back to renderer output; do not add shapes to the finished deck — rounded layouts are outside this skill's format |
| PX-05 | Any shape XML containing `a:outerShdw` or `a:innerShdw` (iron law: 0) | Same origin as PX-04: shadow effects come from external templates or manual edits | Same fix: re-render through this skill, then re-validate |
| PX-06 | Distinct chromatic colours > `MAX_CHROMATIC` (currently 3; a colour counts only above saturation 24, near-grey is ignored) | Mixing palettes, or extra colours pushed into the content or spec | Pin one `--profile` (all five palettes are in the code) and stop colouring body text and tables separately |
| PX-07 | Largest font size ÷ smallest < `MIN_CONTRAST` (currently 2.0; not judged when no font size is measurable) | The whole deck ended up in one size — headings flattened to body level | Restore the theme's heading sizes (switch profile or drop the manual size override); avoid one font size covering the whole page |
| PX-08 | Text frames whose estimated line height > 1.3 × box height (width model: CJK ≈ 1em/char, ASCII ≈ 0.56em, space ≈ 0.3em) | Too much text on one page, or a long unbroken string (URL, long code) blowing up the line count | Tighten `--max-bullets` (default 6) / `--max-chars` (default 760) to split the page; break long strings manually or move them to notes |
| DX-01 | Character-level CJK coverage of the DOCX vs its source < 99.0% (anchor-phrase hit rate is printed for reference only and never decides the verdict) | Real character loss during conversion (rare; usually a phrase split across table cells was skipped) | Check the missing-character samples against the source, then re-run validation with the same `--json`/`--md` input used for rendering |
| DX-02 | Tables without applied borders > 0 (current `table_borders_audit`) | A table bypassed the `style_table` path — typically a hand-inserted table | Let the renderer emit the table instead of patching tables into the finished document |

The geometry items **out-of-bounds / overlap / tiny font are informational**: they are printed for
locating problems but never decide the verdict. PASS is granted only when all ten rules above are clear.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | agent-facing instructions (full workflow, field contract, parse-side capability notes) |
| `scripts/build_docx.py` | Word rendering engine (single source / multi-source merge / markdown direct) |
| `scripts/validate_docx.py` | fidelity + structure validator (docx) |
| `scripts/render_html.py` | HTML showcase renderer (self-contained file, optional `--pdf`) |
| `scripts/render_pptx.py` | PPTX deck renderer (bullets on slides, detail in notes) |
| `scripts/validate_html.py` | HTML validator (coverage + TOC/anchors/self-containment) |
| `scripts/validate_pptx.py` | PPTX validator (coverage incl. speaker notes + empty-page/truncation) |
