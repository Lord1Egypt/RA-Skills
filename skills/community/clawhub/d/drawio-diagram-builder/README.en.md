---
name: drawio-diagram-builder
description: Create, edit, replicate, and iteratively refine editable research and technical diagrams in diagrams.net/draw.io (.drawio XML) from prompts, papers, repositories, screenshots, or existing diagrams.
---

# Research Draw.io Diagram Builder

## Prerequisites

Before starting, verify these are available. If anything is missing, tell the user immediately — do not proceed without them.

| Requirement | Why |
|-------------|-----|
| **Python 3** (3.7+) | All preview/validation scripts are Python. Run `python --version` to check. |
| **Browser automation** | The iterative refinement loop depends on taking screenshots of a local preview. You need one of: Playwright MCP, Puppeteer MCP, browser-evaluate/screenshot tools, or equivalent. |
| **Vision / image-reading tool** (required when user provides reference images as style guides) | Style extraction (see `references/style-extraction.md`) requires sampling pixel colors from reference images. Fallback: ask the user for the palette. |
| **Internet access** | Preview loads `https://embed.diagrams.net/` in an iframe. Offline won't work. |
| **File write access** | You will create `.drawio` files. |

Script paths in this document are relative to the skill directory. Resolve them like `<skill-dir>/scripts/serve_drawio_preview.py`.

## Core Principle

Produce an editable draw.io diagram first, especially for research and technical figures. Do not use an embedded screenshot as the final answer when the user asks for redraw, replica, vector, editable, or 100% reproduction. Raster images may be used only as references, temporary overlays, or explicitly approved assets.

Prefer direct `.drawio` XML authoring plus browser screenshot feedback for complex or high-fidelity diagrams.

## Tool Strategy

Use this priority order:

1. **Direct `.drawio` XML generation/editing** — reliable, reproducible. Write XML with explicit `mxGeometry` positions.
2. **Local preview HTML + diagrams.net iframe postMessage** — run `scripts/serve_drawio_preview.py` (one command, starts server + opens browser) or `scripts/make_drawio_preview.py` + `python -m http.server`.
3. **Browser automation screenshots** — navigate browser to `http://127.0.0.1:<port>/drawio-preview.html`, wait for the draw.io embed to load (2-5 seconds), take a full-page or viewport screenshot.
4. **draw.io MCP / `@drawio/mcp`** — only for small diagrams or quick opening. On Windows, large encoded URLs fail.
5. **draw.io desktop/CLI export** — if installed. Treat as optional; always have the local iframe preview fallback.

Load `references/drawio-workflow.md` for the detailed end-to-end process. Load `references/self-supervision-and-intake.md` for any non-trivial diagram, mixed prompt-plus-image input, project-context diagram, or iterative visual repair. Load `references/style-extraction.md` when the user provides reference images as style guides. Load `references/topconf-paper-style.md` when the user asks for a computer-science paper, top-conference, camera-ready, method, ML pipeline, multimodal architecture, benchmark, or polished research figure. Load `references/xml-authoring.md` when writing or repairing XML shapes, styles, edges, and text layout. Load `references/xml-preflight.md` before rendering any diagram. Load `references/primitive-icons.md` when a reference figure contains small modality, memory, warning, tool, clock, document, or other paper-style icons. Load `assets/icons/ICON-MANIFEST.md` when generic SVG icon assets would improve fidelity.

For any reference-image replication request, load `references/reference-replication-protocol.md` before creating XML.

## Standard Workflow

1. **Verify prerequisites** — confirm Python 3 and browser automation are available.

2. **Collect input context**
   - Read the user's prompt, reference images, paper sections, codebase files, or domain notes.
   - Identify the task type: research figure creation, paper-method diagramming, visual replication, architecture diagramming, or iterative polish.
   - For top-conference paper figures with weak style input, use `references/topconf-paper-style.md` and the bundled images under `assets/reference-images/` as style/layout fallback. Do not invent scientific content.
   - **If reference images were provided as style guides, extract their visual language BEFORE drawing.** Load and follow `references/style-extraction.md`.

3. **Build the diagram brief and visual specification**
   - For mixed inputs or complex tasks, create a brief: user goal, source inventory, requirement traceability, semantic model, style contract, and open assumptions.
   - Record canvas size, major regions, hierarchy, labels, colors, line styles, fonts, arrows, icons, captions, and spacing.
   - Define the meaning of every connector before drawing it.
   - For reference-image replication, create required intermediate artifacts before XML.

4. **Author the `.drawio` file**
   - The `.drawio` file is the primary artifact. Preview HTML is only a derived artifact.
   - Use one `mxfile` with one or more `diagram` pages.
   - Use explicit `mxGeometry` positions and sizes for high-fidelity work.
   - Build important icons and arrows with editable draw.io primitives. Use `references/primitive-icons.md` for common recipes. Use bundled SVG icons from `assets/icons/` when fidelity matters.
   - Keep colors, strokes, fonts, and rounded corners consistent.
   - **Before rendering, run the pre-flight checker:**
     ```bash
     python <skill-dir>/scripts/validate_visual_quality.py <file>.drawio
     ```
     **Zero FAILs required before the first preview HTML is generated.**

5. **Preview without long URLs**
   - **Preferred**: run `scripts/serve_drawio_preview.py <file>.drawio --port 8765`.
   - **Manual**: run `scripts/make_drawio_preview.py <file>.drawio --out drawio-preview.html`, then `python -m http.server 8765 --bind 127.0.0.1`.
   - Open `http://127.0.0.1:8765/drawio-preview.html?rev=1` in the browser.
   - Wait 2-5 seconds for the diagrams.net embed iframe to initialize.
   - Take a screenshot of the rendered diagram.

6. **Iterate from evidence**
   - **HARD GATE: Minimum 3 screenshot → inventory → fix → verify cycles for any high-fidelity or user-critical diagram.**
   - Compare the screenshot against the reference or requested spec.
   - **The screenshot MUST be a canvas-only crop, NOT the full browser window.** A full browser screenshot includes the diagrams.net sidebar, toolbar, and chrome.
   - **MANDATORY: Create a COMPLETE defect inventory scanning all 9 zones (text, arrows, boxes, spacing, color, typography, layout, icons, style coherence) BEFORE fixing anything.**
   - **MANDATORY: Fix ALL P0 and P1 defects, then verify each fix against the new screenshot.**
   - Run the self-supervision audit: requirement audit, semantic audit, visual hygiene audit, style audit, and regression audit.
   - Regenerate the preview HTML, refresh the browser (add `?rev=N`), screenshot again, and repeat.

7. **Validate before handoff**
   - **HARD GATE: Self-score card (mandatory).** Score on a 1-10 scale:
     | Dimension | Score (1-10) |
     |-----------|-------------|
     | Text readability | /10 |
     | Arrow accuracy | /10 |
     | Color coherence | /10 |
     | Layout consistency | /10 |
     | Style match to reference/spec | /10 |
     | **TOTAL** | **/50** |
     - **TOTAL < 30 or any dimension ≤ 4 → BLOCKED.** Continue iterating.
     - **TOTAL 30–39 (and no dimension ≤ 4) → BORDERLINE.**
     - **TOTAL ≥ 40 and every dimension ≥ 6 → ALLOWED.**
   - **HARD GATE: Red-team audit completed and logged.** At least 15 findings (≥10 if self-score ≥45/50).
   - **HARD GATE: At least 3 screenshot cycles documented in defect log.**
   - Run `scripts/validate_drawio.py <file>.drawio`.
   - Confirm: XML parses, page count is expected, ids and references are valid, required geometry exists.
   - Provide the `.drawio` path, the latest screenshot path, the self-score card, and the defect log summary.

## Editing Rules

- Edit `.drawio` files by writing or patching XML directly.
- Preserve user files and unrelated generated files.
- Never claim the diagram is complete without visual verification (a screenshot).
- Never claim the diagram is complete if any hard gate is unmet.
- When the user asks for "100% reproduction", treat that as an iterative standard.

## Bundled Helpers

- `VERSION`: installed skill version marker.
- `scripts/check_skill_update.py`: compare the installed skill version with the canonical GitHub version.
- `scripts/make_drawio_preview.py`: build a local short-URL preview HTML.
- `scripts/serve_drawio_preview.py`: generate the preview HTML and serve it on `127.0.0.1`.
- `scripts/validate_drawio.py`: parse, structurally validate, and sanity-check `.drawio` files.
- `scripts/validate_visual_quality.py`: **pre-render static checker.** Parses XML and computes visual defects without rendering.
- `scripts/validate_replication_artifacts.py`: validate replication protocol artifacts.
- `assets/icons/ICON-MANIFEST.md`: local MIT-licensed SVG icon inventory and usage rules.
- `assets/reference-images/REFERENCE-IMAGES.md`: bundled top-conference-style figure references.
- `references/drawio-workflow.md`: full professional workflow.
- `references/self-supervision-and-intake.md`: mixed-input intake and 5-dimension audit.
- `references/xml-preflight.md`: explains every pre-render static check.
- `references/style-extraction.md`: mandatory style extraction protocol.
- `references/topconf-paper-style.md`: top-conference figure style guide.
- `references/primitive-icons.md`: reusable editable primitive recipes.
- `references/reference-replication-protocol.md`: low-freedom protocol for high-fidelity replication.
- `references/xml-authoring.md`: XML, layout, style, edge, text, icon, and iteration patterns.

## Common Failure Handling

- **Windows long URL failure**: Use local preview HTML with postMessage instead of `.url` files or huge `#create=` URLs.
- **Skipping pre-flight**: The most common cause of a garbage first screenshot. Run `validate_visual_quality.py` before rendering.
- **Full browser screenshot**: The diagram is too small to read. Crop to the canvas.
- **Text overlap or overflow**: Split paragraphs into smaller text cells, reduce font size, increase container width.
- **Wrong icon fidelity**: Build editable approximations from primitives, or use bundled SVG icons.
- **Missing generic icons**: Check `assets/icons/ICON-MANIFEST.md` before searching the web.
- **Stale preview**: Add a query string such as `?rev=3`, regenerate preview HTML, or reopen the tab.
- **Preview iframe not loading**: Wait 3-5 seconds — the `embed.diagrams.net` iframe can be slow. Verify internet access if it still fails.
