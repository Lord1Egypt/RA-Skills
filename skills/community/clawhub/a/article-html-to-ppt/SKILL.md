---
name: "article-html-to-ppt"
license: "Apache-2.0"
description: "Create editable PPTX from documents or pasted outlines and per-slide content with optional style directions; reconstruct slide designs, reuse native PPTX templates, and revise decks with real previews and hash-bound review. 支持文档/大纲转可编辑PPTX、设计图复刻、原生PPTX模板改页与逐页视觉审核。"
metadata:
  display_name: "PPT Smith"
  english_alias: "PPT Smith"
  public_slug: "meowclaw-pptsmith"
  version: "5.4.0"
  compatibility_aliases: ["article-html-to-ppt", "meowclaw-decksmith"]
---

# PPT Smith

## 1. Select the user's intent

| User wants | Route | Read when selected |
| --- | --- | --- |
| Make a presentation from a document, optionally with brand/style references | `create` (default) | [Declarative workflow](references/declarative-design.md) |
| Make a presentation from a pasted outline / per-slide content (no uploaded file) | `create` | [Outline-to-deck authoring](references/outline-to-deck.md), then [Declarative workflow](references/declarative-design.md) |
| Reconstruct supplied complete slide designs as editable objects | `recreate` | [Declarative workflow](references/declarative-design.md) |
| Edit or duplicate original PPTX template pages | `template` | [Native template workflow](references/native-template-workflow.md) |
| Continue an Atlas/component-plan template task | `template` | [Component workflow](references/routes/v4-template-route.md) |

- Infer intent, audience, language, and page budget from the request. Ask only about material conflicts (e.g., exact image reconstruction vs. native template preservation).
- A style image does not imply exact reconstruction. A PPTX supplied only as a style reference uses `create` (read [template visual design](references/template-visual-design.md)); preserve masters/native layouts only when requested.
- Source document page count does not prescribe slide count, whereas an explicitly supplied slide sequence/count is a binding user constraint unless restructuring is permitted. For long multi-chapter reports (e.g., 10+ distinct topics/trends), budget enough pages so chapters stay balanced rather than cramming 4–5 distinct topics onto one slide or collapsing parallel chapters into one divider.

**Done when:** route, native-preservation requirement, and existing task format are clear.

## 2. Establish content and design

- **Source & anchors:** Read the full source once and preserve page/section anchors. Save extracted text with anchors in the task directory for PDF/DOCX/web inputs. Pasted text is a valid source (`provenance.kind: user`); never demand or fabricate an uploaded file.
- **Per-slide manuscripts:** Separate business content from design instructions; analyze hierarchy, groups, relationships, and direction before choosing layouts. Default to complete on-slide coverage (including tables, data, and qualifications); summarize, omit, or move content to speaker notes only with user permission. Follow [outline-to-deck authoring](references/outline-to-deck.md).
- **Model ownership:** The model owns narrative, assertion titles, visual encoding, and page-specific design; fixed tools execute decisions rather than replacing them with generic extractive layouts. Insufficient authoring capability returns `MODEL_AUTHORING_REQUIRED`.
- **Industry & brand-grounded visual system:** Match typography, palette, density, and layout language to the deck's industry and audience instead of a one-size-fits-all look. When the source or content carries a clear brand (e.g., consulting firm report, company earnings, product launch), extract its visual traits—sampling the source document's cover, charts, and styling first, or applying established brand cues when text-only—unless the user requests a different or neutral style. Never fabricate unprovided logos or carry over a prior unrelated task's brand, palette, card layout, or footer.
- **Decorative business reports & diversity:** For decorative business reports, original template design, or fixing repetitive/sparse decks, read [decorative business design](references/decorative-business-design.md) and use the [page planning sheet](templates/decorative-page-plan.md). Use `--review-profile decorative_business` to bind page composition plans and require an independent whole-deck review. Separate stable deck conventions from variable body compositions, and plan a genuine closing within the page budget. (Consult case studies referenced inside that guide only when diagnosing repetition or revision regressions.)
- **Data honesty & separation:** Keep checked text/data in content records, geometry in scene records, and supplementary reasoning/sources in speaker notes (manuscript qualifications stay on-slide). Unknown chart data stays unknown; reconstructable charts/tables use native data; isolated pictures are replaceable assets, never whole-page screenshots masquerading as editable reconstruction. Disclose simplifications and accepted raster exceptions.

**Done when:** checked content, source anchors, visual intent, and unresolved decisions are recorded separately from execution geometry.

## 3. Author and revise native objects

- **Probe capabilities first:** Run `python3 -m engine design capabilities` (`create`/`recreate`) or `python3 -m engine template capabilities` (`template`). Local CLI checks installed tools, browser surface, and fontconfig matches—never host model vision or image-generation abilities.
- **Recover when the host blocks Chromium:** If the HTML probe reports `nested_browser_sandbox_blocked`, use the host's approved execution path to retry the probe and HTML import with Chromium's own sandbox enabled. Use compact author JSON if the host cannot run the browser.
- **`create` (default HTML design surface):** When `html_design_surface.available` is true, author pages in restricted HTML/CSS and compile via `python3 -m engine design html-import` ([HTML design surface](references/html-design-authoring.md)). The fixed tool measures layout in headless Chromium, rejects scripts/external resources, places registered `data-asset` images, traces content to source text, and blocks writes on `design_lint` errors (`imported_with_lint_errors`). HTML previews are iteration drafts, never external targets.
- **Lightweight metadata & fallback:** After importing pages, use `set-meta` (`design.brief`), `set-page` (`notes`, `composition`, `background`), and `add-page` / `remove-page` / `reorder-pages` instead of exporting the entire deck. Use [compact author JSON](references/declarative-authoring.md) for `patch` or when no browser is available. No image tool is needed for ordinary native design; never treat your own preview as an external reference.
- **`recreate`:** Visually read the supplied complete target, verify content against the source, and preserve approved geometry without inventing numbers from pixel heights. Keep targets, approved changes, and actual PPTX previews distinct.
- **`template`:** Follow [native template workflow](references/native-template-workflow.md): inspect actual source-page/object IDs, clone original pages, edit in revision-checked transactions, and inherit real source styles. Existing Atlas tasks keep their [component workflow](references/routes/v4-template-route.md).
- **Preflight & incremental hygiene:** Run real-office font preflight before expanding a large deck (fontconfig alone does not prove actual CJK rendering). Use page-scoped context and guarded patches instead of rewriting the deck; never run task-authored scripts to bypass unsupported features. Reuse independent page reviews only via `review-template --inherit-from`; any change to content, notes, geometry, assets, fonts, or renderer invalidates affected evidence.

**Done when:** the candidate and affected pages are identified by revision and hash, with failed edits leaving prior valid state intact.

## 4. Verify and deliver

- **Required gates:** Actual PPTX rendering, checked content/data, resolved fonts, structural editability, target-software edit/save/reopen checks, and independent visual review at readable resolution (a contact sheet alone cannot verify small text).
- **Whole-deck check:** Inspect body-layout variety, visual coherence, and narrative completeness separately—title/navigation stability, numeric baselines, graphic weight, chapter transitions, summary/decision/closing order, and nonrectangular text safety margins. Verify that table-of-contents sections, section dividers, and body eyebrows share **one consistent numbering system** with every top-level section covered (if dividers are used), all section dividers share one visual style without uneven card walls, left-to-right column order matches numbered headings, and single-axis charts never mix incompatible units (e.g., GW and %). Resolve suspected collisions on full-size pages/crops. Automated diagnostics locate evidence; they never approve craft or originality. Always recheck the merged candidate after parallel authoring.
- **Review integrity:** Original designs without an external target use `reconstruction: not_applicable`; reconstruction with a target requires fidelity approval. Inherited page reviews retain original observations and hashes, while whole-deck review is always fresh. A generator's own review is never independent, and fabricated second identities are forbidden.
- **Delivery & isolation:** `candidate_unreviewed`, `draft`, and `render_incomplete` are not final. Deliver only when the exact file passes all route gates, with editable PPTX, actual previews, and material editing limitations. Quality acceptance is separate from OS isolation: `--isolation auto` selects macOS isolation or host execution (reporting OS isolation unverified on host), while `--require-os-isolation` is binding and must not be downgraded. Never claim untested PowerPoint/WPS or cross-platform parity, and never inherit advisory-review website policies.

**Done when:** all required checks apply to the exact delivered file.

## Compatibility only

- Legacy `new_design` and `style_transfer` map to `create`; register style references explicitly. Saved legacy tasks keep their original contract. `draft` is diagnostic only.
- Bespoke remains an advanced compatibility route ([guide](references/routes/v4-bespoke-route.md); [V4 authoring contract](references/routes/v4-authoring-contract.md) loads only for legacy Bespoke/Atlas routes).
- `template` preserves native assets and never silently falls back to blank-slide reconstruction. Standard/Engineering is for internal diagnostics and explicit engineering drafts only.
