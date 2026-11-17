# Production Readiness Gates

Use these gates for non-trivial decks. Production now starts by resolving a profile and ends with a user-facing delivery package plus `delivery-manifest.json`.

## Gate 0: Production Profile Lock

Run `scripts/resolve_production_profile.py` before deciding artifact depth:

```bash
python3 scripts/resolve_production_profile.py \
  --requirements requirements.json \
  --ppt-ir .ppt-work/contracts/ppt-ir.json \
  --output .ppt-work/contracts/production-profile.json
```

Pass when:

- the selected profile is `fast`, `standard`, or `premium`;
- user override wins when the user explicitly asked for a profile;
- required artifacts, required gates, and allowed skips are recorded;
- all process files are planned under `.ppt-work/`;
- the final user directory is planned as a delivery package, not a dump of intermediate files.

Fail when:

- a simple internal draft is forced into Premium without user or risk justification;
- public, high-value, brand-heavy, or complex-diagram work is downgraded without disclosure;
- working files are placed directly in the user-facing final directory.

## Gate 1: Content Lock

Every slide must declare one `title_role`.

Slides with `title_role=judgment`:

- must state an answer, conclusion, implication, recommendation, or contrast;
- must not use a generic topic title;
- must connect the judgment to evidence.

Slides with `title_role=navigation|section|instruction|reference|closing`:

- must use a title appropriate to that role;
- are not required to manufacture a judgment;
- must still make the slide purpose immediately understandable.

Pass when:

- every slide has a `slide_role`;
- every slide has a `title_role`;
- judgment slides have evidence-supported judgments;
- major claims are sourced, inferred, or marked as assumptions;
- no important source section is silently dropped;
- paragraphs are transformed into semantic structure.

Fail when:

- a judgment slide uses only a generic topic title;
- a section or agenda slide invents an unsupported conclusion merely to satisfy the old judgment-title rule;
- `title_role` does not match `slide_role`;
- judgment and evidence contradict each other;
- a major claim has no source, inference label, or assumption label.

## Gate 2: Expression Mode Lock

Every slide must choose exactly one `primary_expression`.

Supporting expressions are optional, but they must:

- directly support the primary expression;
- occupy less visual weight than the primary anchor;
- not introduce a second storyline;
- not duplicate information already expressed by the primary component.

Every slide must record:

```text
primary_expression
primary_expression_reason
supporting_expressions
audience_question
primary_anchor
```

Pass when:

- every slide has one valid `primary_expression`;
- supporting expressions clarify rather than compete;
- the selected expression answers the audience question;
- relationships, flows, systems, ecosystems, causal chains, and spatial metaphors are not hidden in prose/cards/tables without a documented simplification reason.

Fail when:

- no primary expression is selected;
- two components compete as primary anchors;
- supporting content consumes more visual weight than the primary expression;
- `hybrid_panel` is used as a catch-all instead of identifying the true primary expression;
- relationship content is converted into generic cards without a documented simplification reason.

## Gate 3: Architecture Lock

Keep the one-primary-anchor rule. The existence of `supporting_expressions` does not violate the one-anchor rule.

Pass when:

- one object or object group is unmistakably dominant;
- supporting components explain, qualify, label, or interpret the primary anchor;
- visual hierarchy remains clear at thumbnail size;
- every slide has one page archetype;
- density has a structural reason;
- high-density slides preserve grouping and scan path.

Fail when:

- multiple objects compete as the main anchor;
- supporting material becomes visually dominant;
- density hides the page message;
- the page archetype contradicts the audience question.

## Gate 4: Spec Priority Lock

Pass when every object has role and priority, low-priority objects are deleted or weakened, and grid/connector/icon/table budgets are explicit.

Numeric budgets are default diagnostic budgets, not universal hard limits.

Default examples:

- technical relationship page: 3-9 meaningful connectors;
- architecture page: up to 8 primary nodes;
- normal KPI page: up to 4 KPI cards;
- normal image-supported page: up to 3 images;
- normal table page: up to 5x6 visible cells.

Use this severity model:

```text
budget_severity:
  within_budget: pass
  moderately_over_budget: warning
  severely_over_budget_with_clear_structure: review
  severely_over_budget_without_clear_structure: fail
```

Budget judgment depends on:

- `slide_role`
- `page_archetype`
- `presentation_context`
- `audience`
- `content_complexity`
- `physical_slide_size`

Examples:

- A normal body slide with 11 connectors usually warrants a warning.
- An architecture slide whose only primary anchor is a relationship map may need 11 connectors without failing.
- Any slide fails when many connectors cross, pass through nodes, obscure labels, or leave the main path unclear.

## Gate 5: Visual Reference Lock

Use for polished, formal, public, client-facing, or style-sensitive decks.

Pass when cover and one representative content page are previewed and can be reconstructed as hybrid-editable PPT.

Fail when the preview proves that the style contract cannot be executed, key text becomes unreadable, or the visual direction contradicts audience/context.

## Gate 6: Diagram IR Lock

Use for every slide whose `primary_expression=relationship_visual`.

Pass when:

- the diagram object has exactly one of `diagram_ir_ref` or inline `diagram_ir`;
- Diagram IR validates against `schemas/diagram-ir.schema.json`;
- nodes, groups, edges, boundaries, annotations, and main paths are semantic, not decorative;
- edge relation semantics are defined before line styles;
- one primary main path or dominant relationship structure is clear;
- connector-web risk is low, or simplification/split/hybrid delivery is explicitly planned;
- `analyze_diagram_complexity.py` output is available for complex diagrams.

Fail when:

- Builder is asked to draw a relationship diagram directly from prose;
- relationship-heavy content is converted to generic cards;
- all edges have the same visual priority;
- boundaries are missing where ownership/trust/security/failure matters;
- nodes contain paragraphs rather than labels;
- whole-slide rasterization hides labels, nodes, and title in one image.

## Gate 7: Delivery Route Lock

Resolve delivery routes before PPT build. This gate converts PPT IR objects into explicit implementation choices using Component Registry, Style Contract, Builder capability, profile, and object complexity.

Pass when:

- every object has a registered `component_type`;
- `delivery-plan.json` exists and validates;
- ordinary text, cards, tables, matrices, metric cards, and simple charts remain native/editable;
- complex relationship visuals use Diagram IR analysis, then select `native_diagram`, `hybrid_overlay`, or `svg_component` according to complexity and Builder support;
- `native_required` objects never silently downgrade to SVG or image;
- every fallback has reason codes and declared editable core;
- planned route is ready to be copied into Build Manifest after implementation.

Fail when:

- route is chosen ad hoc during drawing;
- ordinary components are rasterized;
- Builder support is unknown in a premium build;
- fallback removes title, label, legend, source, or core data editability without disclosure;
- whole-slide rasterization appears without explicit user approval.

## Gate 8: PPT Implementation Lock

Pass when:

- message-bearing content is editable;
- raster components are bounded and disclosed;
- actual component routes match `delivery-plan.json`, or deviations are recorded in `build-manifest.json`;
- all key text fits;
- representative slides render nonblank when a render route is available;
- object/media counts match expectations;
- verification evidence honestly caps build status.

Fail when:

- whole-slide rasterization is used without explicit user approval;
- core message-bearing text is not editable;
- text clips or overlaps;
- required media is missing;
- render/readback evidence is claimed but not actually available.

## Gate 9: Independent Quality Scoring

Record the actual deck review using `schemas/rubric-score.schema.json`.

Read the result as two independent gates:

- hard gate: QA `fatal`/`error` issues block pass;
- rubric gate: total score must be at least 14 and no dimension may be 0.

If no model or human scorer is configured, `manual_review_required` is the correct result. Do not convert provisional automatic metrics into final approval.

## Gate 10: Delivery Package And Trusted Status

Package only user-facing files:

```bash
python3 scripts/package_delivery.py \
  --workdir .ppt-work \
  --profile <fast|standard|premium> \
  --output output/final \
  --manifest output/final/delivery-manifest.json \
  --strict
```

Pass when:

- required delivery files exist for the selected profile;
- `deck.pptx` is a readable PPTX package;
- all delivered files have `sha256:` hashes;
- `delivery-manifest.json` validates against `schemas/delivery-manifest.schema.json`;
- privacy scan finds no absolute paths, usernames, tokens, temp files, private URLs, or undeclared private assets;
- Build Manifest records resume metadata when a stage fails;
- failed builds preserve `.ppt-work/`.

Trusted status must be calculated, not asserted:

```text
planned -> created -> rendered -> read_back -> verified -> final
failed
```

Only Premium can be `final`. Premium without real render evidence must remain below `final`, even if structure checks pass. Any QA `error` or `fatal` blocks `final`. Renderer absence must be reported truthfully as `RENDER_ENGINE_UNAVAILABLE`; do not fake render evidence or screenshots.

Fail when:

- `final` is written by the Builder or by subjective judgment;
- Premium is marked `final` without full render and readback;
- a delivery package includes `.ppt-work/` internals by default;
- a local path, token, debug log, or temp artifact leaks into user-facing files.
