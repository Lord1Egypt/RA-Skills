---
name: "article-html-to-ppt"
description: "Convert articles into verified PPTX, dynamic PPTX, HTML previews, or Feishu Slides."
---

# Article HTML To PPT

## Core Principle

Convert articles into speakable, professionally designed slide decks. The workflow is: normalize source, build evidence-backed storyboard, lock slide content, define a formal brand-consistent visual direction, produce reviewable preview artifacts, export to the requested deck format, then verify honestly.

This skill treats **direct PPTX generation** as a first-class export path. When the environment has PptxGenJS or an equivalent local helper, generate a real `.pptx` file instead of stopping at guidance.

When the user asks for **dynamic PPT**, **dynamic presentation**, **animated PPT**, or says the exported PPT should dynamically display during presentation, default to a **native PPTX progressive-build deck**: duplicate each logical slide into multiple build steps so each click reveals more content in PowerPoint/Keynote presentation mode. Add native slide transitions when possible. HTML dynamic decks are optional companion artifacts, not the default answer for “dynamic PPT”.

Object-level PowerPoint animations inside a single slide remain experimental because they require fragile OOXML timing/animation structures or target-player automation. Do not promise object-level animation unless a prototype is verified in PowerPoint/Keynote.

A deck is not final merely because files were created. If the export cannot be rendered, opened, read back, or visually checked, say so and deliver the best verified artifact with clear limits.

## Quality Contract

Borrow the useful parts of CyberPPT without copying its heavy workflow:

- **Evidence first:** important claims, numbers, examples, diagrams, and recommendations must trace back to source material or be labeled as reconstruction/assumption.
- **Storyline before slides:** create a real narrative path before producing layouts. For high-value decks, compare 2-3 possible storylines and choose one.
- **Content lock before visual generation:** freeze each slide's title, key message, evidence, chart/table inputs, captions, source labels, and sensitivity notes before generating visual previews or PPTX.
- **Manifest while building:** write or maintain a `slide_manifest.json` for non-trivial decks so the deliverable can be audited later.
- **Dual hard gates:** core text must remain editable where the export format supports it, and visual structure must not be downgraded into a flat screenshot unless the user explicitly accepts that tradeoff.
- **Lightweight QA, not ceremony:** use practical checks suited to the target export. Do not require full bbox reverse engineering or Windows PowerPoint COM unless the task truly needs consulting-grade QA and the environment supports it.

## When To Use

Use this skill when the user asks to:

- turn an article, Markdown draft, HTML article, WeChat draft, report, or review-approved manuscript into slides
- create PPT/PPTX/PowerPoint/Feishu Slides from article content
- directly generate a `.pptx` file from article or HTML content
- create a dynamic PPT/PPTX that reveals content during presentation
- create native PowerPoint/Keynote-compatible step-by-step presentation behavior
- make an HTML slide preview before exporting slides
- create an optional reveal.js or web presentation companion
- adapt MeowClawLab / 夜猫子弦月 content into a presentation
- preserve image prompts, captions, figure notes, visual identity, source rights, or desensitization constraints in the deck

Do not use this for ordinary document editing, raw article writing, or a one-off visual image request.

## Inputs To Collect Or Infer

Required:

- Source content: Markdown, HTML, Docx text, article path, pasted text, or URL content already retrieved by a suitable skill.
- Export target: `pptx`, `native-dynamic-pptx`, `html-preview`, `dynamic-html`, `feishu-slides`, `object-animation-pptx-experimental`, or `multi`.
- Usage boundary: private draft, internal review, public sharing, client delivery, training, or publication.

Optional:

- Audience and scenario.
- Duration or slide count.
- Visual system id and overrides.
- Assets: cover image, logo, screenshots, diagrams, existing PPT template.
- Dynamic behavior: step-by-step reveals, section transitions, speaker notes, auto-slide timing, embedded media, or object-level animation.
- QA level: `light`, `standard`, or `consulting-grade`.

## P0 Preflight And Checkpoints

### CHECKPOINT 1: Source Rights And Use Boundary

Before generating an export intended for sharing, classify the source:

- `owned`: written by the user or their team.
- `licensed`: user provided permission, template, or explicit reuse rights.
- `external-reference`: public article or third-party source used for analysis or private transformation.
- `unknown`: rights are unclear.

Rules:

- For `owned` or `licensed`, continue normally.
- For `external-reference`, produce a private/internal working deck unless the user confirms public redistribution is allowed.
- For `unknown`, ask for confirmation before uploading a public or broadly shared deck.
- Always preserve source attribution when the deck depends on a public article.
- Do not download, rehost, or imply ownership of third-party images unless rights are clear.

### CHECKPOINT 2: Export Capability Matrix

Before export, state what the current environment can actually do.

| Capability | Stable Route | Check | If Missing |
| --- | --- | --- | --- |
| Direct PPTX | PptxGenJS or equivalent helper | `node -e "require.resolve('pptxgenjs')"` or helper exists | Install only with user approval, or deliver HTML/Feishu route |
| Native dynamic PPTX | Progressive-build slides + optional native transitions | PPTX builder can duplicate slide states | Deliver static PPTX; explain limit |
| PPTX render check | LibreOffice/PowerPoint/Keynote/QuickLook/screenshot route | Can open/export/screenshot generated PPTX | Mark PPTX as created but not visually verified |
| Feishu Slides create/write | Lark/Feishu slides skill or lark-cli route | Scopes available | Ask for auth or deliver local PPTX/preview |
| Dynamic HTML companion | reveal.js/plain HTML runtime | Can generate local HTML and open/render it | Omit companion |
| Object-level animated PPTX | OOXML/PowerPoint automation support | Prototype renders in target player | Treat as experimental; do not promise |
| Image upload/use | Asset rights and upload scope available | Upload/use allowed | Use placeholders/prompts with captions |

The final handoff must distinguish:

- `Created`: artifact was generated or uploaded.
- `Rendered`: artifact was opened or rendered locally.
- `Read back`: exported platform content was inspected after creation.
- `Final`: all required checks passed, or remaining limits were accepted by the user.

### CHECKPOINT 3: Evidence And Content Lock Gate

Run this before visual preview or export for every non-trivial deck.

Create a `content_lock.md` or equivalent section inside `storyboard.md` that freezes:

- deck thesis and intended audience
- selected storyline and rejected alternatives if compared
- each slide's title, one-message takeaway, speaker point, visual job, and priority
- source sections, citations, quoted facts, and file paths/URLs when useful
- chart/table inputs and whether they are sourced, calculated, estimated, or reconstructed
- image prompts, screenshot requirements, figure labels, source/rights labels, and reconstruction labels
- sensitivity notes, redactions, and items that must not appear in slide-visible text
- allowed simplifications and explicit assumptions

Rules:

- After content lock, do not let visual generation or PPTX layout rewrite facts, metrics, names, or recommendations.
- If a slide needs content changes after visual work begins, update the content lock and note the reason.
- If source evidence is insufficient, label the claim as assumption/reconstruction or ask for the missing source when the risk is high.
- For quick drafts, a compact content lock table is enough; do not inflate small tasks with unnecessary paperwork.

### CHECKPOINT 4: Formal Brand Consistency Gate

Before batch-generating all slides, validate representative pages whenever practical:

- Cover or opening slide.
- Evidence or example slide.
- Framework / process / checklist slide.
- Closing slide if the deck is public or client-facing.

Each gate page must pass one clear message, stable grid, consistent typography, consistent footer/source/brand marker, visible fact/reconstruction labels, and no obvious text overflow.

### CHECKPOINT 5: Native Dynamic PPT Gate

Use this checkpoint when the user requests dynamic PPT or exported PPT presentation motion.

Classify the dynamic request:

- `native-dynamic-pptx`: stable default. Generate a PPTX where each logical slide is expanded into multiple build steps. Each click reveals more content by advancing to the next visually similar slide. Add slide transitions when supported.
- `pptx-with-notes`: stable. Static PPTX with speaker notes and presenter-friendly structure.
- `dynamic-html-companion`: optional companion for web-native motion, not a substitute when the user asked for PPTX.
- `object-animation-pptx-experimental`: object-level animation inside one slide. Experimental only.

Rules:

- If the user says “dynamic PPT”, do not answer with only HTML.
- Prefer native progressive-build PPTX because it works across PowerPoint/Keynote without fragile object animation XML.
- Keep build-step slides visually identical except for newly revealed content.
- Add slide transitions such as fade when possible and verify transition XML exists.
- Report logical slide count and build-step slide count separately.
- If object-level animation is required, prototype 1-2 slides first and verify in the target player.

## Workflow

### 1. Normalize Source

Extract title, thesis, section headings, claims, evidence, examples, frameworks, image suggestions, caveats, and sensitivity notes. Preserve citations or file paths when useful. Do not invent screenshots, metrics, quotes, or examples.

For public or third-party sources, keep a concise evidence map that links each major slide to the source section or URL. For owned drafts, preserve internal source paths only in non-public reports; do not expose private local paths inside slide-visible text.

### 2. Build And Choose Storyline

Create a storyboard before making slides. For high-value or client-facing decks, sketch 2-3 candidate storylines first, then choose the strongest one based on audience, evidence strength, and presentation goal.

Each frame should include:

- slide title
- speaker point
- visual job
- body bullets or diagram elements
- source section and evidence status
- caption / footnote requirement
- brand consistency notes
- export notes: PPTX layout mapping and dynamic build steps

### 3. Create Content Lock

Use `templates/content-lock-template.md` when useful. The content lock is the source of truth for slide facts and structure.

Minimum content lock fields for each slide:

- `slide_id`
- `locked_title`
- `one_message`
- `source_evidence`
- `must_keep_editable_text`
- `visual_job`
- `asset_or_prompt`
- `caption_or_evidence_label`
- `sensitivity_or_redaction_notes`
- `allowed_assumptions`

For decks with charts, tables, reconstructions, or public sharing, include chart data lineage and source/rights labels.

### 4. Derive Formal Content-Fit Visual Direction

Write a short `visual_design_brief` with article type, formality target, brand posture, metaphor, emotional temperature, visual density, evidence mode, audience posture, and rejected directions. Then select a visual archetype from `references/visual-design-archetypes.md` or define one.

Prefer a small set of reusable, ownable visual systems and sample pages. Do not copy CyberPPT's consulting style library wholesale; adapt the idea of real style samples to MeowClawLab / user-specific visual identities.

### 5. Apply Brand System As Primary Design Frame

Select a brand/column visual system from `references/visual-systems.md` if present. Use it for palette, typography, title rhythm, footer/source pattern, shape language, captions, and grid.

Keep a single deck to one dominant visual system. Use contrast modes sparingly and only for deliberate section shifts, not random decoration.

### 6. Design Slide-Specific Visual Jobs

Assign every slide a visual job: hook, contrast, explain, evidence, framework, process, boundary, or close.

When using generated visuals or reconstructed diagrams, label them honestly. Never represent a reconstruction, synthetic UI, or inferred process as a historical screenshot.

### 7. Generate Preview Or Direct PPTX

For non-trivial decks, create an HTML preview before final export unless the user asks for direct PPTX only. If the user asks for direct or native-dynamic PPTX, still build a storyboard, content lock, manifest, and verification report.

### 8. Export

#### 8.1 Direct PPTX Export

Use PptxGenJS or an existing local helper as the preferred direct `.pptx` route.

Minimum requirements:

- 16:9 wide layout unless user asks otherwise
- theme fonts and colors
- shared layout helpers or slide masters
- PowerPoint-safe text, shapes, tables, charts, images, and SVGs
- speaker notes when useful
- captions and source/rights labels
- no private paths in slide-visible text
- `deck.pptx` plus `pptx-build-report.json`, `slide_manifest.json`, and/or `verification-report.md`

#### 8.2 Native Dynamic PPTX Export

Use this when the user wants exported PPT to dynamically display during presentation.

Implementation pattern:

1. Start from the locked logical storyboard.
2. For each logical slide, define reveal steps.
3. Generate one PPTX slide per reveal step.
4. Keep stable coordinates, typography, background, and footer across all steps in the same logical slide.
5. Add only the newly revealed bullet, diagram part, or emphasis between steps.
6. Add native slide transitions if supported.
7. Embed speaker notes for each build step or logical slide.
8. Write `deck-dynamic-native.pptx`.
9. Report both counts: `logical slides` and `native build-step slides`.

Verification:

- inspect `.pptx` zip for expected slide count
- confirm notes count when speaker notes are generated
- confirm transition XML exists if transitions are added
- render via QuickLook/PowerPoint/Keynote/LibreOffice/screenshot route when available
- if only first-slide render is possible, say so

#### 8.3 Feishu Slides Export

Use the Lark/Feishu slides skill or lark-cli route when available. Creation success is not final; readback/screenshot requires extra scopes.

For Feishu Slides, preserve the same content lock and manifest discipline even if the export API does not expose every visual property.

#### 8.4 Dynamic HTML Companion

Use reveal.js or custom HTML only as an optional companion format or when the user explicitly asks for a web presentation. Do not substitute it for native dynamic PPTX when the user asked for PPT.

#### 8.5 Object-Level Animated PPTX Experimental

Only attempt PowerPoint-native object animation inside a single slide if a proven helper, OOXML patcher, or PowerPoint automation route exists.

Rules:

- prototype 1-2 slides first
- render or manually inspect in the target player
- if verification fails, deliver native dynamic PPTX instead
- mark result as experimental

### 9. Write Slide Manifest

For standard or higher QA, write `slide_manifest.json` using `templates/slide-manifest-template.json` as the shape.

The manifest should record:

- deck metadata: source, rights boundary, export target, visual system, logical slide count, physical slide count
- per-slide locked content pointer
- generated objects: editable text, shapes, charts, tables, images, screenshots, icons, background assets
- asset provenance and rights labels
- dynamic build mapping: logical slide id to physical slide ids
- verification status per slide when available

Rules:

- `must_keep_editable_text` should map to actual editable text objects for PPTX/Feishu outputs when possible.
- If a slide intentionally uses a full-slide image or rasterized visual, mark why and what editing tradeoff was accepted.
- Do not treat `pictures=0` as a success metric; diagrams, screenshots, and brand imagery can be legitimate. The point is preserving core text editability and semantic structure.

### 10. Verify Before Completion

At minimum:

- Check logical slide count and build-step slide count.
- Check text overflow in preview and/or exported target.
- Check whether visual design is professional and brand-consistent.
- Check captions, figure labels, and desensitization notes.
- Check that core text is editable where the export route supports editable objects.
- Check that no private local paths, tokens, unpublished names, or raw review trails appear in slide-visible text.
- For native dynamic PPTX, verify slide count, notes count, transition XML if added, and at least one render/screenshot when possible.
- Do not call a deck `final` if only creation succeeded but rendering/readback failed or was unavailable.

For standard/high-value decks, also write `visual_qa_gate.json` or `verification-report.md` with:

- `nonblank_render`: pass/fail/unknown
- `text_overflow`: pass/fail/unknown
- `editable_core_text`: pass/fail/unknown
- `visual_structure_preserved`: pass/fail/unknown
- `source_labels_present`: pass/fail/unknown
- `rasterization_tradeoffs`: none/list
- `remaining_manual_checks`: list

## Failure Modes And Required Responses

| Failure Mode | Trigger | Required Response |
| --- | --- | --- |
| User wanted dynamic PPT but got HTML | User asks for PPT motion/presentation mode | Generate native dynamic PPTX; HTML only as companion |
| Direct PPTX dependency missing | PptxGenJS/helper unavailable | Ask before installing; otherwise deliver preview/Feishu route |
| PPTX creation succeeds but cannot render | No renderer/checker available | Mark as created but not visually verified |
| Native build-step deck too long | Too many reveal steps | Group reveals, reduce bullets, or use section-level builds |
| Object animation requested | User needs same-slide PowerPoint object animation | Prototype; mark experimental; do not promise |
| Source rights unclear | External article or third-party images | Ask or mark as private/internal; preserve attribution |
| Visual fragmentation | Backgrounds/layouts change too much | Reduce to one dominant background family and one contrast mode |
| Fake evidence | Reconstructed UI or synthetic diagram | Label as reconstruction or assumption visibly |
| Missing content lock | Visual/export work begins before slide facts are frozen | Pause, create compact content lock, then continue |
| Manifest mismatch | Generated deck count/assets differ from manifest | Update manifest or fix deck before handoff |
| Editable text lost | Core text only exists in a flattened image | Rebuild as editable text or clearly mark accepted tradeoff |
| Privacy leak | Tokens, raw local paths, unpublished names | Redact before export and mention redaction class |

## Red-Light Blacklist

Never do these:

- Never answer a request for dynamic PPT with only HTML.
- Never claim object-level PowerPoint animations are supported unless a verified prototype worked in the target player.
- Never call a generated PPTX final when it was only created but not rendered or inspected.
- Never let visual generation or layout rewrite locked facts, metrics, names, or recommendations.
- Never claim reconstructed UI, inferred process, or synthetic image is a historical screenshot.
- Never upload a public deck from an external copyrighted article without confirming usage rights.
- Never include private local paths, tokens, account names, unpublished leads, or raw review trails in public decks.

## Output Package

For a complete deck task, produce one primary deliverable plus a short handoff.

Recommended files:

- `storyboard.md`
- `content_lock.md` or content-lock section inside storyboard
- `visual-design-brief.md` or `visual-system.json`
- `slide_manifest.json` for standard/high-value decks
- `slides-preview.html` when useful
- `deck.pptx` for static PPTX
- `deck-dynamic-native.pptx` for native dynamic PPTX
- `dynamic-deck.html` only as companion or web export
- Feishu Slides link when requested
- `pptx-build-report.json` or `native-dynamic-pptx-report.json`
- `visual_qa_gate.json` or `verification-report.md`

Handoff should include source rights, usage boundary, export target, logical slide count, build-step slide count if dynamic, chosen visual system, content lock status, manifest status, capability matrix, verification performed, and remaining manual checks.

## Collaboration Rules

For one-shot conversions, prefer run/one-shot execution and write durable output files. Do not rely on long chat history as deck state. When delegating, pass the source path, rights boundary, capability matrix, storyboard requirements, content lock requirements, brand direction, export target, dynamic PPT requirements, manifest requirements, QA level, and expected final deliverable.
