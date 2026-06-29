---
name: one-shot-research-poster
description: Build print-ready academic conference posters from papers, PDFs, LaTeX projects, arXiv/OpenReview/project pages, reference posters, and user assets in one user request with internal render/repair iterations. Use when the agent must deliver a real final poster package, not a browser screenshot: verified paper claims, official venue logistics, conference and affiliation logos, complete paper figures, local assets, exact-size HTML/CSS, final PDF, final PNG preview, editable source, and a gate report. Defaults to a hard-gated posterly-style production pipeline; uses interactive poster editors only as optional layout assistants.
---

# One-Shot Research Poster

## Success Contract

The task is not complete until the poster package contains:

- editable poster source, normally `poster.html`;
- final one-page print PDF;
- final PNG preview rendered from the PDF or the same print-emulated browser export;
- local assets directory containing every figure, logo, and QR code referenced by the poster;
- `GATE_REPORT.json` or an equivalent validation report;
- claim-evidence audit for important numbers, theorems, datasets, baselines, venue logistics, and affiliation text;
- official conference logo plus key affiliation logos, or a recorded reason why a logo could not be used.

A browser screenshot alone is a failure. An interactive editor alone is a failure. A poster that only looks good in screen mode is a failure. If any required artifact or hard gate cannot be produced, say the poster is blocked or incomplete and name the missing gate.

One-shot means one user request, not zero internal iteration. Drive the work end-to-end with minimal clarification: ask at most one compact clarification batch, then make reasonable choices, render, measure, fix, and re-render internally until the hard gates pass. Do not imply that the first draft is final; the promise is that the user does not need to manually coordinate the production pipeline.

## Engine Policy

Use this order:

1. **posterly-style production path, default.** Use `posterly` when available, or build an equivalent exact-size HTML/CSS workflow with Chromium print rendering and hard gates. This is the only default path for a final PDF.
2. **posterskill-style interactive editor, optional assistant.** Use `ethanweber/posterskill` ideas for reference-poster matching, web/project asset discovery, aspect-ratio-aware image placement, and `window.posterAPI` whitespace optimization. Bake the resulting layout back into stable source and still run the production gates.
3. **Fallback custom HTML.** If neither repo is available, create exact-size local HTML/CSS and implement equivalent checks: one-page PDF, correct physical dimensions, local assets, no TODOs, no remote image URLs, figure edge audit, and final PNG inspection.

Never choose a path whose natural output is only a screenshot. See `references/engine-selection.md` and `references/failure-analysis.md` before using a non-posterly path.

## Required Workflow

### 1. Create A Poster Package

Create a single working folder, for example:

```text
poster/
  poster.html
  poster.pdf
  poster.png
  GATE_REPORT.json
  CLAIM_EVIDENCE.md
  POSTER_STATE.json
  images/
  sources/
```

Record every source decision in `POSTER_STATE.json`: paper path or URL, venue page URL, canvas size, poster date/time, room, poster number, QR target, logo sources, figure sources, and user constraints.

### 2. Ingest And Verify Sources

Prefer paper source over PDF. If only PDF is available, extract text and render page images so figures can be checked visually against the source.

Use official sources for current or externally changing facts:

- venue poster size, upload format, logo policy, QR policy, and minimum font rules;
- schedule, room, poster location, session date, and time;
- conference logo for the user-specified venue, for example ICML, CVPR, NeurIPS, ICLR, ACL, EMNLP, ICCV, ECCV, or SIGGRAPH;
- affiliation logos for the first author, corresponding author, and other key institutions when they are not already provided;
- arXiv/OpenReview/project URLs and paper metadata.

Store fetched assets locally. Do not leave remote image URLs in the final poster.

Logo discovery is active, not passive. If the user says "ICML poster," look for an official ICML logo. If the user says "CVPR poster," look for an official CVPR logo. Then identify author affiliations from the paper source/PDF/arXiv/OpenReview page and fetch key institution logos. When the author list is long, keep a compact set: first-author affiliation, corresponding-author affiliation, and any dominant shared affiliation; omit secondary logos that would crowd the title. Record omitted logos and why.

### 3. Build The Claim-Evidence Audit

Before writing final poster prose, create a compact table:

```text
poster claim | source | evidence | status
```

Statuses: `OK`, `NUMERIC-MISMATCH`, `OVERCLAIM`, `MISSING-PRECONDITION`, `NOT-IN-SOURCE`, `INTENTIONAL-SUMMARY`.

Audit these especially carefully:

- headline percentages and metric improvements;
- dataset and baseline names;
- theorem statements and assumptions;
- "training-free", "reference-free", "plug-and-play", "no retraining", and similar scope claims;
- venue logistics and affiliation/correspondence line.

Do not invent numbers. If the paper gives a nuanced or conditional statement, preserve the condition or weaken the poster text.

### 4. Prepare Figures, Logos, And QR Codes

Use real paper figures/tables unless the user requests a conceptual redraw. For each used paper figure:

- crop from the rendered paper page or paper source at high resolution;
- preserve method headings, axis labels, tick labels, legends, captions needed for interpretation, and table row/column labels;
- compare the crop against the source page after placement;
- mark paper figures with provenance metadata when using a manifest, for example `data-source="paper"` and `data-asset-id="fig5"`;
- run `scripts/figure_edge_audit.py` on figure crops and visually inspect any edge warning.

For logos:

- fetch the official conference mark for the specified venue when public, or use a user-provided logo;
- fetch key affiliation marks for the first author, corresponding author, and dominant shared institutions;
- when there are many authors or many affiliations, prioritize first author + corresponding author + dominant institution and avoid a logo wall;
- run `scripts/logo_asset_plan.py` for raster logos;
- use `scripts/logo_selection_plan.py` when author/affiliation metadata is available;
- decide whether each logo needs a white chip, transparent placement, border, or scaling;
- keep logo lockups readable without competing with the title.

For QR codes:

- generate offline as a local image;
- label the QR target clearly;
- verify it remains readable in the rendered PNG/PDF.

### 5. Compose Exact-Size HTML/CSS

Use a print canvas with a real `@page { size: ... }` rule. Match official dimensions rather than assuming a default venue size.

Design rules:

- keep all assets local;
- keep colors, fonts, spacing, and card variants tokenized where the engine supports it;
- use paper figures with `object-fit: contain`, not hard clipping;
- do not use `overflow: hidden` on a figure container unless the crop has been audited;
- never hide axis labels or method headings to make a figure fit;
- keep header text, authors, affiliations, conference/institution logos, QR, and footer logistics aligned as a single system;
- remove low-value repeated text instead of shrinking everything.

Header and footer rules:

- the conference/institution should be visually obvious when logos are available;
- remove redundant acceptance text when the venue logo already communicates it;
- put room, poster number, session time, paper/code link, and contact in the footer or QR label;
- do not let footer text collide with shadows or page edges.

### 6. Run The Production Gates

For posterly, use the canonical loop:

```bash
python tools/run_gates.py poster.html --report GATE_REPORT.json
python tools/render_preview.py poster.html --pdf poster.pdf --png poster.png
python tools/poster_check.py verify-final poster.pdf --from-html poster.html
python scripts/check_poster_deliverables.py poster
```

If `FIGURE_MANIFEST.json` exists, run:

```bash
python tools/run_gates.py poster.html --manifest FIGURE_MANIFEST.json --report GATE_REPORT.json
```

If using a fallback engine, reproduce the same gate meanings:

- static HTML gate: no TODO/FILL_IN, no missing local assets, no remote image URLs, no raw LaTeX residue;
- style/layout gate: exact page size, no clipped content, no accidental extra pages;
- asset gate: paper figures are real, local, sufficiently sharp, and complete;
- render gate: final PDF and PNG exist and are derived from the print canvas;
- content gate: claim-evidence audit has no unresolved hard issues.

Do not report success until every hard gate passes or an explicitly user-approved waiver is recorded.

### 7. Final Visual Inspection

Inspect the final rendered PNG, not only the HTML. Check:

- title, authors, affiliations, logos, QR, and footer are readable;
- every figure shows top and bottom content completely;
- image grids preserve method names above the grid;
- plots preserve x-axis and y-axis labels;
- tables are legible and not over-cropped;
- no duplicate card repeats the same claim without a new role;
- no text overlaps, clipped shadows, clipped logos, or stray white logo rectangles;
- the PDF is one page with the correct physical size.

Run `scripts/audit_poster_text.py` on the final HTML and remove repeated phrases unless they serve distinct reader modes: scan, mechanism, evidence, practical deployment, or logistics.

### 8. Deliver

Return the paths to the final PDF, PNG, HTML/source, local assets, and gate report. State any non-running optional gates, such as a missing figure manifest, clearly.

## What To Borrow From The Reference Systems

From `posterly`:

- exact print canvas;
- Playwright/Chromium rendering;
- `preflight -> style -> asset -> measure -> polish` gates;
- final PDF dimension verification;
- local QR and asset discipline;
- tokenized templates and bounded layout fixes.

From `ethanweber/posterskill`:

- read paper source plus project/author websites;
- discover logos/images with Playwright when simple downloads fail;
- use the author/project website as one logo source, but prefer official venue and institution pages when available;
- match reference poster style when the user provides examples;
- measure image aspect ratios before assigning cards;
- use `window.posterAPI.getWaste()` or equivalent browser measurement to reduce wasted figure space;
- allow temporary interactive adjustment, then bake the result into stable source.

The combined skill succeeds when the interactive/editor ideas feed the production renderer, not when they replace it.

## Resources

- `references/engine-selection.md`: when to use posterly, posterskill, or fallback HTML.
- `references/failure-analysis.md`: why screenshot-only outputs happen and the design rules that prevent them.
- `references/logo-discovery.md`: active conference and affiliation logo discovery, prioritization, and provenance rules.
- `references/poster-system-comparison.md`: detailed comparison of the three workflows.
- `references/content-qa.md`: claim-evidence and duplicate-content review rules.
- `references/visual-qa.md`: figure completeness, logo handling, and final render inspection rules.
- `scripts/check_poster_deliverables.py`: hard check for required final artifacts and local assets.
- `scripts/audit_poster_text.py`: extract poster text and flag repeated phrases/sections.
- `scripts/figure_edge_audit.py`: detect figure crops with ink touching edges.
- `scripts/logo_selection_plan.py`: prioritize conference, first-author, corresponding-author, and dominant-affiliation logos.
- `scripts/logo_asset_plan.py`: inspect logo dimensions, transparency, white backgrounds, and placement treatment.
