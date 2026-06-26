---
name: deck-pipeline
description: |
  Production-grade Claude Code system that takes presentation decks from raw
  Chinese draft to McKinsey-polished English — with full audit trail, layout
  integrity checks, and a swappable PROFILE block for project-specific
  defaults. Built on a 4-stage pipeline (Sense Pass → McKinsey Translation →
  Layout Audit → Handoff). Also runs polish-only on any single-language deck.

  TRIGGER when the user:
    • hands over a .pptx containing Chinese and asks for English / translation
    • asks for "deck pipeline", "deck polish", "deck globalizer"
    • asks for layout polish, font cleanup, overflow fixing on any deck
    • asks to update / reverse-sync a bilingual comparison Excel against a deck

  SUPPRESS with "Ignore deck-pipeline".
version: 0.1.0
license: MIT
---

# Deck Pipeline

> **A 4-stage, audit-trailed Chinese→English deck globalization system with a swappable project profile.**

This skill bundles the generic deck-globalization engine (originally upstream
DeckGlobalizer v2.1.1) and an editable PROFILE block (palette, fonts,
glossary, style preferences). The two are **separated** by section so the
profile can be swapped per project / brand without touching the engine.

For a marketing-style overview, see `README.md` in this directory.
For implementation, see `scripts/` and the per-stage runbooks below.

---

## 0. Modes & activation

| Mode | Trigger | Stages |
|---|---|---|
| **Full pipeline** | CN deck (± EN draft) + user wants English output | 1 → 2 → 3 → 4 |
| **Polish-only**   | Single-language deck + "layout / format only / skip translation" | 1 → 3 → 4 |
| **Reverse-sync only** | User hand-edited a PPT after a comparison Excel was generated | 3.5 (sync sub-routine) |

Detect the mode in the first turn. If ambiguous, ask one yes/no question
("This deck is already in EN — should I just polish layout, or also rewrite
McKinsey-style?"). Do not guess silently.

---

## 1. PROFILE block — defaults (swappable)

Edit this block to retarget the skill for your project / brand. Everything
below this block is **profile-agnostic**.

```yaml
PROFILE:
  # ---- L1 Tokens ----
  palette:
    # Replace with your brand colors.
    ink:          "#1A1A1A"
    primary:      "#000000"   # accent / brand primary
    soft:         "#FFFFFF"   # soft fill behind banners
    page_bg:      "#FFFFFF"
  fonts:
    # Choose a serif title face + a sans-serif body face for best contrast.
    title:        "Georgia"
    body:         "Verdana"
    title_bold:   true
  unit_table:
    # Chinese number magnitudes → English. 亿 is 100M, NOT "billion".
    "百万":       "M"
    "千万":       "10M"
    "亿":         "100M"
    "十亿":       "1B"
    "百亿":       "10B"
    "千亿":       "100B"
    "万亿":       "1T"
    # Currency suffix is left to the user — append "$" / "RMB" / "€" as appropriate.

  # ---- L2 Constants ----
  size_ladder:           [22, 14, 10, 8, 6, 4]   # H1, H2, body, caption, footnote, source
  floors:
    body:     7
    caption:  6
    source:   4
  compression_step:      0.1     # discrete -0.1pt iterations only
  line_height_default:   1.25
  line_height_fallback:  1.15    # used before sub-floor compression
  quote_style:           "single"  # 'McKinsey' single quotes
  footer_format:         "Confidential · For Intended Recipients Only · {month} {year}"
  separator_in_footer:   "·"     # middle dot, NOT em-dash

  # ---- L1 Glossary (extensible) ----
  # Replace the example entries below with your project's locked terms.
  # Categories are illustrative; you can rename / add / remove.
  glossary:
    locked:
      people_orgs:
        # "<source term>": "<canonical translation>"
        # e.g. "John Smith": "John Smith"
        # e.g. "Acme Capital": "Acme Capital"
        {}
      business_terms:
        # Common Chinese business-deck idioms with industry-standard
        # English mappings. Edit / extend as needed.
        "流水":     "gross revenue"
        "私域":     "owned audience"
        "出海":     "global expansion"
      domain_specific:
        # Project / industry / domain terms.
        # "<source term>": "<canonical translation>"
        {}
    rejected_rewrites:
      # Entries the user vetoed during prior sessions.
      # Format: { source: "...", proposed: "...", reason: "..." }
      []
    pending: []
    session_added: []

  # ---- Style rules ----
  # McKinsey is the default baseline. Additional style references can be
  # uploaded and distilled via scripts/style_distill.py; their rules layer
  # ON TOP of the McKinsey base.
  style_baseline: "mckinsey"
  mckinsey:
    title_is_takeaway:      true   # title = the so-what, not the topic
    lead_with_so_what:      true
    parallel_structure:     true   # bullets share tense, opening part-of-speech
    strong_action_verbs:    true   # cut "is/has", prefer concrete verb
    cut_filler:
      - "in order to → to"
      - "a number of → many"
      - "due to the fact that → because"
      - "at this point in time → now"
    case:                   "sentence"   # lowercase unless proper noun or locked term
    em_dash_policy:         "use em-dash for parentheticals; use · (middle dot) in lists/footers"
  style_references:
    # Each entry is a PDF / .pptx reference. style_distill.py reads it and
    # emits rules (cadence, signature phrases, paragraph length, tone) that
    # layer on top of the McKinsey base. Conflicts: more recent entry wins;
    # user is asked at first conflict.
    # Example:
    # - path: "/path/to/sample.pdf"
    #   weight: 0.7
    []

  # ---- Structural anchor heuristics ----
  anchor_detection:
    min_pages: 3              # appears on ≥3 slides
    match_on:                 # signature components
      - position_xy
      - fill_color
      - font_size_class
    auto_protect: true

  # ---- Overflow estimator ----
  overflow:
    severity:
      high: 1.5
      med:  1.15
      low:  1.0
    surface_only: "high"      # surface MED/LOW only when explicitly asked
    defer_to_user_threshold: 10   # if HIGH > 10 → ask user to render externally

  # ---- CN ↔ EN slide alignment ----
  # Default is 1:1 (EN slide N maps to CN slide N).
  # Set overrides only when the two decks have been restructured.
  # Pass this config to excel_sync.py via `--cn-offset <yaml>`.
  cn_en_slide_offset:
    default: 0           # offset added to EN slide number (0 = 1:1)
    overrides: {}        # e.g. {"9-26": -1, "20": null}
                         # int = relative offset; null = no CN counterpart
```

> **Profile-agnostic note:** all sections below treat `PROFILE` as an
> opaque dict. Do not hardcode project-specific values anywhere outside the
> PROFILE block.

---

## 2. Pipeline stages

Each stage has: **inputs · what it does · outputs · stop-and-ask conditions.**

### Stage 1 — Sense Pass

**Inputs:** one or two `.pptx` paths (CN, optional EN draft)
**What it does:**
1. Run `scripts/sense_pass.py` to extract:
   - palette (top fill colors)
   - font usage histogram
   - size distribution
   - title-zone shapes (top ≤ 600K EMU)
   - layout heuristics
2. Cross-check sensed values against `PROFILE.palette` / `PROFILE.fonts`.
   If a sensed font is NOT in the whitelist AND NOT in `SKIP_POLLUTION`,
   record it as **font pollution**.
3. Surface **candidate glossary entries**: any CN noun phrase that appears
   ≥2 times and isn't already in `glossary.locked`.

**Outputs:**
- `Style_Manifest.md` (in-memory; not written to disk unless requested)
- `pollution_report` (slide → font → count)
- `candidate_glossary` (term → count → sample context)

**Stop-and-ask:**
- Candidate glossary surfaces a term Claude can't confidently translate →
  ask user, write answer to `glossary.session_added`.
- Sensed primary palette color differs from `PROFILE.palette.primary` →
  ask whether to update profile or keep existing.

---

### Stage 2 — McKinsey Translation (skipped in polish-only mode)

**Inputs:** Stage 1 outputs + the CN deck (and optional EN draft for diff context) + any uploaded `style_references`.

**Style layering**: McKinsey base rules (`PROFILE.mckinsey`) apply first. If
`PROFILE.style_references` is non-empty, run `scripts/style_distill.py` on
each reference before translation begins; the distilled rules (cadence,
signature phrases, paragraph length, tone) layer on top. More recent entry
wins on conflict; ask user at the first conflict.

**Page-by-page execution (hard requirement):**
1. **Overall confirmation first** — after Stage 1, show the user the planned
   per-page edit count + sample of style rules in effect; wait for "go".
2. **Then loop slides 1 → N**, one at a time:
   - Collect paragraph-level CN text on this slide via `scripts/extract.py`.
   - For each paragraph, produce EN per the layered style rules:
     - lowercase by default; title = so-what; parallel bullets; strong verbs;
       filler-word table applied; glossary `locked` inline
     - any unknown term → STOP, ask user, write to `session_added`
   - Build the slide's edit batch as a JSON object.
   - Run `scripts/apply.py` with the slide's batch → writes that slide's
     changes into `<file>-en-polished-<date>.pptx` AND appends rows to
     `<file>-bilingual-diff-<date>.xlsx` immediately.
   - **Checkpoint**: print "P{n} done — N changes applied. Continue?" and
     wait for user OK before moving to P{n+1}.
   - User can interject "back to P{n-1}" or "stop here" between pages.

**Why per-page (not all-at-once):**
- The user can review and steer mid-stream.
- A bad assumption on P3 doesn't propagate to P27 unnoticed.
- Excel grows incrementally — survives any mid-session interruption.
- Token-efficient: only one slide's context in active scratchpad.

---

### Stage 3 — Layout Audit

**Inputs:** the post-translation deck (or, in polish-only mode, the raw deck)
**What it does:**

#### 3a. Font pollution cleanup
Run `scripts/layout_audit.py --fix`:
- For every run whose `font.name` is NOT in the title/body whitelist
  OR ends in a style suffix (`Bold` / `Regular` / `Italic` / `Light`):
  - Strip the suffix
  - Set `font.name` to the pure family
  - Set `font.bold` / `font.italic` attributes accordingly
- Skip any face in the configured `SKIP_POLLUTION` set.

#### 3b. Structural-anchor detection
Run `scripts/anchor_detect.py`:
- For each shape, compute a signature: `(rounded_position, fill_color, font_size_class)`.
- Group across slides. Any signature occurring on ≥ `PROFILE.anchor_detection.min_pages`
  pages becomes an **anchor**.
- Build `per_page_protect[page] = [anchor_shape_ids...]`.
- Surface the anchor list to the user. They can add/remove.

#### 3c. Overflow estimation
Run `scripts/overflow_recheck.py`:
- Honor `auto_size` (skip if SHAPE_TO_FIT_TEXT or TEXT_TO_FIT_SHAPE).
- Read actual `margin_*`.
- Use `PROFILE.line_height_default = 1.25` initially. If a shape is flagged,
  try 1.15 as a what-if before flagging as HIGH.
- Per-character width by class (narrow `iIl`, wide `MW`, digits, upper, space).
- Greedy word-wrap simulation.
- Emit only HIGH (`ratio > PROFILE.overflow.severity.high`) by default.

If HIGH count > `PROFILE.overflow.defer_to_user_threshold`:
- **Do not** dump 30+ rendered PNGs into the session.
- Tell the user: "Render to PDF/PNG via Keynote or PowerPoint, tell me which
  pages look broken, I'll fix those targeted pages."

#### 3d. Compression (when user OKs a fix)
For each shape needing fix:
1. Is it in `per_page_protect[page]`? → SKIP (it's an anchor).
2. Try widening: increase shape `width` until ratio < 1.0 OR shape collides.
3. Still > 1.0? Try line-height 1.25 → 1.15.
4. Still > 1.0? Iterate `font.size -= PROFILE.compression_step` (0.1pt) until
   floor (`PROFILE.floors.<body|caption|source>`) hit.
5. Still > 1.0 at floor? **STOP. Escalate to user.** List the shape, its
   current size, the calculated ratio, and ask whether to break the floor.

#### 3e. Late-stage glossary re-scan
Run `scripts/glossary_audit.py`:
- For each text run in the deck, check against `glossary.locked`:
  - If a CN-side phrase exists locked but a non-canonical EN translation
    appears → flag.
  - If the same source term is translated two different ways in the deck
    (wavering) → flag.
- Surface flagged rows. Auto-fix if all flags point to the same canonical
  translation; ask otherwise.

#### 3f. Reverse sync (sub-routine, also Mode 3.5 entry point)
Run `scripts/excel_sync.py --reverse`:
- Diff current PPT against the Excel's `en_optimized` column.
- For each mismatched row:
  - Try ordinal-position match (slide + paragraph-index).
  - If no match, try `difflib.get_close_matches` against same-slide texts.
  - Update Excel cell on success.
- Report any leftover unmatched rows.

**Outputs:**
- `<file>-final-<date>.pptx` (full pipeline) or `<file>-final-<date>.pptx` (polish-only)
- Updated Excel (if applicable)

---

### Stage 4 — Handoff

**Inputs:** all prior-stage outputs
**What it does:**
1. Write `HANDOFF.md` to the same directory as the deck — see `scripts/handoff.py`.
2. Print a one-paragraph deliverables summary to the user.

**Stop-and-ask:** none.

---

## 3. Operational rules (apply across stages)

### 3.1 File-write discipline

Before writing **any** `.pptx` or `.xlsx`:
1. Check for `~$<filename>` lock file in the same directory.
2. If present → **STOP.** Tell the user: "`<filename>` is open in
   PowerPoint/Excel. Save and close it, then say 'go' to continue."
3. After writing, immediately readback-verify (next rule).

### 3.2 Excel companion three guard-rails

1. **Pre-write check** — load existing Excel (if any), confirm header row is
   `[page, kind, cn, en_original, en_optimized, notes]`. If columns missing
   → rebuild header before writing data.
2. **Post-write readback** — immediately reload the saved file and assert
   `max_column ≥ 7` and header is intact.
3. **Reverse sync** available on demand: see Stage 3f.

### 3.3 Font compression discipline

See Stage 3d. The single rule: **never** bulk-reduce font sizes.
Always discrete `-0.1pt`, always after exhausting widening + line-height
fallback, always with anchor protection.

### 3.4 Glossary discipline

- Ask once per session per unknown term. Then it's in `session_added` for
  the rest of the session.
- At handoff, promote `session_added` to a `glossary_proposed_additions.yaml`
  file next to the deck. The user can copy them into PROFILE for the next run.
- **Never** silently apply a translation Claude is unsure about. Stop and ask.

### 3.5 Magnitude verification

Any number with a CN magnitude word (百万 / 千万 / 亿 / 百亿 / 千亿 / 万亿)
must be re-verified against `PROFILE.unit_table` before being written to EN.
Treat this as a HARD CHECK; do NOT take prior-session translations on faith.

### 3.6 CN-alignment confidence

When auto-aligning the Excel's `cn` column by paragraph ordinal:
- Slides with > 15 changes → auto-tag `notes` column as `needs-review`.
- Always present this as best-effort, never as ground truth.

---

## 4. Scripts (in `scripts/`)

| Script | Role | Stage |
|---|---|---|
| `sense_pass.py` | extract design DNA, font usage, palette | 1 |
| `extract.py`    | paragraph-level text extraction | 1, 2, 3 |
| `apply.py`      | apply EN edits + write Excel with highlight | 2 |
| `layout_audit.py` | font pollution cleanup, suffix audit | 3a |
| `anchor_detect.py` | cross-page anchor signature detection | 3b |
| `overflow_recheck.py` | overflow estimator with severity tiers | 3c |
| `glossary_audit.py` | late-stage glossary re-scan + wavering | 3e |
| `excel_sync.py` | bidirectional PPT ↔ Excel sync (configurable slide offset) | 3f |
| `handoff.py`    | write HANDOFF.md | 4 |
| `style_distill.py` | distill style fingerprint from a reference PDF/.pptx | pre-2 |

Each script is invokable standalone; the skill wires them together.

---

## 5. Deliverables (recap)

**Full pipeline (4 files):**
- `<file>-en-polished-<date>.pptx`
- `<file>-final-<date>.pptx`
- `<file>-bilingual-diff-<date>.xlsx`
- `HANDOFF.md`

**Polish-only (3 files):**
- `<file>-final-<date>.pptx`
- `<file>-layout-changes-<date>.xlsx`
- `HANDOFF.md`

**Mode 3.5 (reverse-sync only):**
- updated `<file>-bilingual-diff-<date>.xlsx`

---

## 6. Known limitations

1. Overflow estimator is a **hint, not a verdict** — final visual check
   requires external rendering (Keynote / PowerPoint export to PDF).
2. `python-pptx` cannot render slides. There is no built-in preview.
3. CN auto-alignment by paragraph ordinal can drift on heavily-restructured
   pages — configure `PROFILE.cn_en_slide_offset.overrides` for known cases.
4. The skill assumes the CN source is semantic ground truth — typos in CN
   propagate to EN unless the user catches them.
5. File-lock collisions silently corrupt output. The pre-write `~$xxx` check
   is the only line of defense.

---

## 7. Changelog

See `CHANGELOG.md`.

---

## 8. Credits

Generic deck-globalization engine derived from upstream **DeckGlobalizer v2.1.1**
by tinadu-ai (<https://clawhub.ai/tinadu-ai/deckglobalizer>). Original
three-phase architecture (Visual Audit / Semantic Alignment /
Page-by-Page Execution) credited and retained.
