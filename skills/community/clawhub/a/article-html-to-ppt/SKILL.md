---
name: "article-html-to-ppt"
license: "Apache-2.0"
description: "Create PPTX, reconstruct slides, or reuse PPTX templates; produce editable native objects, real previews and hash-bound review. Use for revisions too."
metadata:
  display_name: "PPT Smith"
  english_alias: "PPT Smith"
  public_slug: "meowclaw-pptsmith"
  version: "5.3.1"
  compatibility_aliases: ["article-html-to-ppt", "meowclaw-decksmith"]
---

# PPT Smith

## 1. Select the user's intent

| User wants | Route | Read when selected |
| --- | --- | --- |
| Make a presentation from a document, optionally with brand/style references | `create` (default) | [Declarative workflow](references/declarative-design.md) |
| Reconstruct supplied complete slide designs as editable objects | `recreate` | [Declarative workflow](references/declarative-design.md) |
| Edit or duplicate original PPTX template pages | `template` | [Native template workflow](references/native-template-workflow.md) |
| Continue an Atlas/component-plan template task | `template` | [Component workflow](references/routes/v4-template-route.md) |

Infer intent, audience, language and page budget from the request. Ask only about material conflicts, such as exact image reconstruction versus native template preservation. A style image does not imply exact reconstruction. A PPTX supplied only as a style reference uses create; preserve masters/native layouts only when requested. For template-inspired redesign, read [template visual design](references/template-visual-design.md). A source page count does not prescribe slide count.

Complete when the route, native-preservation requirement and existing task format are clear.

## 2. Establish content and design

Read the full source once, preserve page/evidence anchors, then use the relevant evidence for each slide. The model owns narrative, assertion titles, visual encoding and page-specific design. The backend executes those decisions; it does not replace them with generic extractive layouts. Insufficient authoring capability returns `MODEL_AUTHORING_REQUIRED`.

Choose typography, palette, composition and visual rhythm for the current content, audience and references. Do not copy the last task's colours, card layout, footer or brand. Reusable components are primitives, not mandatory page styles.

For decorative business reports, original template design, or revisions about repetitive layouts, sparse pages, inconsistent visual order or missing chapter/ending pages, read [decorative business design](references/decorative-business-design.md). Plan each page's content relationship, reading path and information-bearing graphic before drawing. Separate stable deck conventions (title/navigation regions, type hierarchy, margins and graphic weight) from variable body compositions. Plan the narrative roles and ending before fixing the page budget; a summary is not automatically a closing page.

Use the optional `decorative_business` review profile to bind page composition plans and require an independent whole-deck review. It extends create, not the number of routes. A different silhouette does not prove a different layout; deliberate series repetition must still satisfy the user's requested degree of variation. Use the [page planning sheet](templates/decorative-page-plan.md); consult the [original refinement case](references/cases/decorative-business-refinement.md) for density/craft and the [two-round business report case](references/cases/business-deck-diversity-coherence.md) for variety, coherence and narrative completeness. These are transferable design lessons, not fixed palettes, page counts or layout menus.

Keep checked text/data in content records, geometry in scene records, and detailed reasoning, sources and qualifications in speaker notes. Unknown chart data stays unknown. Reconstructable charts/tables use native data; isolated pictures are replaceable assets, not editable internal objects. Do not insert a whole-page screenshot to claim editable reconstruction. Disclose deliberate simplifications and accepted raster exceptions.

Complete when checked content, source anchors, visual intent and unresolved decisions are recorded separately from execution geometry.

## 3. Author and revise native objects

For create/recreate run `python3 -m engine design capabilities`. The host supplies model capabilities; local code cannot infer whether the current model sees or generates images.

For **create**, author structured design, render a native candidate to PNG, inspect and revise it. Image generation is optional for independent illustrations or an explicitly requested external design target. No image tool is needed for ordinary native design. Do not convert your own preview into a fake external reference or claim self-comparison proves design quality.

For **recreate**, visually read the supplied complete target, verify its content against the source, and preserve approved geometry. Do not invent source numbers from chart pixel heights. Keep original targets, approved changes and actual PPTX previews distinct.

For **template** original-page editing, run `python3 -m engine template capabilities`, then follow the [native template workflow](references/native-template-workflow.md). Inspect actual source-page/object IDs, clone original pages, edit in revision-checked transactions and inherit real source styles. The host agent authors the presentation; fixed tools execute operations without another model runtime, website service or task-authored code. Existing Atlas/component tasks retain their [component workflow](references/routes/v4-template-route.md).

Use the compact author format and page-scoped context described in the selected guide. Fixed tools expand validated references into native objects. Do not execute task-authored scripts to bypass unsupported features.

Run the real-office font preflight before expanding a large deck. Check representative compositions first; continue without mandatory user approval unless the request needs a consequential choice. Fontconfig matching alone does not prove actual Chinese font rendering.

Default tool feedback is a summary. Read full reports only for relevant failures; keep task state and evidence in files. Use guarded object patches instead of rewriting the deck. For changed builds, inherit independent page review only through the verified inheritance command; changed content, notes, geometry, assets, fonts or renderer invalidate the affected evidence.

Complete when the current candidate and its affected pages are identified by revision and hash; failed edits leave the previous valid work intact.

## 4. Verify and deliver

Actual PPTX rendering, checked content/data, resolved fonts, structural editability, target-software edit/save/reopen checks, and independent visual review are required. Review every new or changed page at readable resolution; a contact sheet alone cannot verify small text.

Also inspect the assembled deck separately for body-layout variety, visual coherence and narrative completeness. Check title/navigation stability, numeric baselines, graphic weight, chapter transitions and the actual summary/decision/closing order alongside information topology and visual layers. Review nonrectangular text against the visible shape interior. Use actual full-size pages or crops to resolve suspected collisions seen in a contact sheet. Automated composition diagnostics locate evidence; they cannot approve originality, visual richness or craft. Recheck the merged candidate after parallel authoring, and never inherit a whole-deck design verdict from separate page approvals.

Original design without an external target uses `reconstruction: not_applicable`; design, content, fonts and editability still require approval. Reconstruction with a target requires fidelity approval. Reused review must retain its original reviewer observations and evidence, never a fabricated second identity. A generator's own review is not independent.

`candidate_unreviewed`, `draft`, and `render_incomplete` are not final. Deliver only when the exact candidate passes the selected route's gates. User-visible output includes editable PPTX, actual preview and material editing limitations.

Quality acceptance is separate from OS isolation. `--isolation auto` chooses available macOS isolation or host execution. Host may deliver after quality acceptance, while reporting OS isolation unverified. `--require-os-isolation` remains binding; do not downgrade it. Do not claim untested PowerPoint/WPS or cross-platform parity.

Complete when required checks apply to the exact delivered file. Missing rendering or independent visual review remains incomplete; do not inherit the website's advisory-review delivery policy.

## Compatibility only

For explicit advanced Python compatibility execution, local contribution export, standalone packaging, or Office session safety, read [security boundaries](references/security-boundaries.md). Obtain the documented user authorization; quality approval is not code trust or OS isolation.

Legacy `new_design` and `style_transfer` init arguments map to create; register requested style references explicitly. Existing saved legacy tasks retain their old target contract. Draft is a state/diagnostic option, not another production promise.

Bespoke remains an advanced compatibility authoring route where needed: read [its guide](references/routes/v4-bespoke-route.md). Template preserves native assets and never silently falls back to blank-slide reconstruction. Their detailed [V4 authoring contract](references/routes/v4-authoring-contract.md) loads only for those routes.

Standard / Engineering remains available for internal diagnostics and explicit engineering drafts, not as a substitute for final model-authored design. Do not load all compatibility guides for a normal create task.
