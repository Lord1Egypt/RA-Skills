# V4 compatibility authoring contract

Read for Bespoke or Template authoring only. The current default create workflow uses the declarative task contract.

## Required model workflow

### 1. Establish the production request

Confirm or infer the audience, decision, language, route, page-range contract,
template-use mode, delivery format, and editability requirements. A source-page
count is not an output-slide count.

### 2. Read and structure the entire source

Stage source files locally, then obtain deterministic anchors:

```bash
python3 -m engine parse --source report:text:source.txt --json-out parsed.json
```

For PDF, preserve page identity and extract tables, charts, illustrations, and
captions as distinct source objects where possible. Reconcile the deterministic
parse with the actual source pages; do not rely on an early subset.

### 3. Author the content contracts

Before choosing geometry, produce:

- Content & Evidence Map;
- Narrative Contract and page budget;
- source-backed Presentation IR;
- per-slide assertion, evidence, topology, visible-content, and speaker-notes
  contracts;
- chart/table/diagram payloads for every reconstructable quantitative exhibit;
- Exhibit Interpretation Contract for every retained illustration.

Visible copy should contain one assertion and a small number of complete,
high-value labels. Detailed reasoning belongs in speaker notes. Planner-created
ellipsis, OCR fragments, generic labels, and tiny source prose are forbidden.

Final visible copy must also reject unresolved generator values such as
`undefined`, `null`, `NaN`, `[object Object]`, TODO/TBD, and Chinese placeholder
equivalents. Duplicate or overlapping slide-number objects are delivery
failures, not harmless decoration.

The IR schema is [schemas/v4/presentation-ir.schema.json](../../schemas/v4/presentation-ir.schema.json).

### 4. Analyze the template when using Template route

```bash
python3 -m engine component-atlas \
  --template-pptx template.pptx \
  --review component-review.json \
  --json-out component-atlas.json
```

The review must identify reusable charts, tables, timelines, processes, KPI
cards, comparisons, matrices, image frames, relationship diagrams, section
recipes, style primitives, and equivalent instances. It must also state whether
each component can stand alone, its minimum information units, recommended
page recipes and companions, annotation requirements, and prohibited uses.
Geometry alone is not a semantic component review.

For every uploaded template, derive a template-local adaptation contract:
content and decoration bounds, background semantics, supported aspect ratios,
responsive modes, minimum visible information, numeric annotation floors, and
series role. Do not encode component ids, page numbers, colours, fonts, or
sample-report rules from a previously tested template. Oversized source-page
backgrounds are not reusable component content unless the reviewed contract
proves a semantic role.

### 5. Let the model compose the deck

For every slide, compare its topology, data shape, required slots, text bounds,
and element capacity with the Atlas. Record:

- feasible template components;
- selected component(s) and slot bindings;
- rejected candidates and reasons;
- any model-authored native component required;
- speaker notes and evidence IDs.

The model may specify composition and geometry for Bespoke pages and for new
Template components. Existing reviewed Template components retain their native
geometry unless an explicitly supported placement transform is used.

External visual assets used by a Template component require a declared source,
license or permission basis, and content hash. Do not copy icons or graphics
from style references merely because they resemble the uploaded template.

### 6. Execute and verify

Useful route commands include:

```bash
python3 -m engine plan-bespoke ...
python3 -m engine author-bespoke ...
python3 -m engine plan-model-template-components ...
python3 -m engine component-atlas-report ...
python3 -m engine compose-components ...
python3 -m engine strict-template ... --final-delivery
python3 -m engine review-template ...
```

`plan-manuscript-components` remains available for legacy diagnostics. It is
not a substitute for a model-authored slide plan. A `model_authored` Template
component is executed through `build(slide, context)` and may use only native
objects plus explicitly hash-bound standalone source illustrations declared in
the IR.

Always run structural inspection and a real renderer. A generated PPTX is only
a candidate until visual review is bound to that candidate.

### 7. Review the rendered deck

Inspect every slide, not only a contact-sheet thumbnail. Reject for:

- weak or incomplete content expression;
- source-page screenshots used as authored slides;
- reconstructable data shown only as raster images;
- visible truncation or planner-created ellipsis;
- sparse text/outline pages without purposeful composition;
- feasible template components left unused without explanation;
- inconsistent template style, hierarchy, spacing, density, or rhythm;
- a reviewed component used as the whole page without supporting evidence,
  interpretation, or implication;
- repeated declared variants that do not correspond to genuinely different
  compositions;
- repeated real-rendered visual skeletons even when their recipe names or
  left/right orientation differ;
- components mechanically scaled into unsupported target aspect ratios;
- comparison series without a shared anchor and scale, or long series that
  should be consolidated or moved to an appendix;
- missing or inadequate speaker notes.
- rendered semantic modules that do not account for the model's declared
  information units;
- body text below the Template readability floor;
- unresolved generator values or duplicate slide-number objects.

## Final-delivery gates

A final deck requires all applicable gates:

- source and numeric provenance pass;
- important-evidence coverage pass;
- every body slide has a complete assertion;
- every body slide has speaker notes with evidence and source anchors;
- every reconstructable chart/table is native and editable;
- every feasible reviewed template component is reused or has a documented
  rejection reason;
- no page screenshot contains source prose/navigation/header/footer;
- no generic placeholder or planner-generated ellipsis is visible;
- component binding, structural inspection, real rendering, asset integrity,
  deck rhythm, content density, and style completeness pass;
- hash-bound human or capable-model visual review approves the candidate.

If any gate fails, return a candidate/revision state and the exact blocker. Do
not call it final.
