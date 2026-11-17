# PPT Smith v4 Contracts

v4 contracts connect **model-directed presentation authoring** to deterministic
execution and verification. A capable model remains responsible for source
understanding, narrative, visible content, data interpretation, visual
encoding, component choice/composition, speaker notes, and rendered visual
review. The engine verifies provenance, native editability, template fidelity,
capacity, rendering, and declared quality floors; it does not replace authorial
judgment.

## Route authority

1. **Bespoke is the quality ceiling and default route.** The model writes a
   source-grounded IR and native authoring code, starting from a blank deck or
   using an uploaded deck as visual evidence.
2. **Template is model-directed native reuse.** The engine extracts a complete
   reviewed Component Atlas. The model audits every feasible component, chooses
   and combines matching components, and writes a new template-styled native
   component only when the Atlas proves there is no feasible match.
3. **Standard is diagnostic compatibility.** It can execute constrained IR for
   debugging and fallback workflows, but it is not the V4 quality benchmark and
   must not be presented as equivalent to Bespoke or Template delivery.

## Delivery principles

1. **Source-grounded authoring.** Facts, metrics, charts, tables, images, and
   speaker notes retain structural source references and evidence IDs.
2. **Concise slides, complete notes.** Visible content is presentation-grade;
   detail moves into speaker notes rather than being truncated with ellipses.
3. **Native visual encoding.** Reconstructable quantitative exhibits become
   editable charts, tables, KPI systems, or diagrams. Source-page screenshots
   are forbidden. Only audited standalone illustrations, photos, and genuinely
   non-reconstructable figures may remain raster assets.
4. **Template reuse before invention.** A Template page must disclose the full
   feasible component set, selected components, rejected candidates, and any
   newly authored component.
5. **Fail closed.** Missing evidence, silent truncation, unbound business text,
   incomplete Component Atlas metadata, style drift, insufficient density,
   failed real rendering, or missing visual review prevents final delivery.

## Files

| File | Status | Purpose |
|---|---|---|
| `presentation-ir.schema.json` | active 4.1.0 | Model-authored content, visual intent, component intent, and speaker-note contract |
| `examples/presentation-ir-model-directed.json` | reference | Source-grounded quantitative Template page with notes and component audit |
| `examples/presentation-ir-minimal.json` | diagnostic | Small Standard-compatible contract; not a production-quality benchmark |
| `examples/presentation-ir-enriched.json` | reference | Rich facts, metrics, relations, and hints |
| `style-contract-v4.schema.json` | active 4.0.0 | Reusable tokens and rendering constraints |
| `decision-trace.schema.json` | active 4.0.0 | Machine-readable decision and degradation trace |
| `render-plan.schema.json` | active 4.0.0 | Native builder execution contract |
| `production-request.schema.json` | active 1.0.0 | Route, page policy, and template hash contract |
| `narrative-contract.schema.json` | active 1.0.0 | Bespoke narrative and evidence contract |
| `template-evidence.schema.json` | active 1.0.0 | Read-only evidence extracted from an uploaded template |

Validation:

```bash
python3 scripts/validate_contracts.py --strict \
  --presentation-ir schemas/v4/examples/presentation-ir-model-directed.json
```

The v3 contracts remain available for the existing v3 pipeline. V4 inherits
v3's high-customization authoring standard while adding reviewed template
component extraction, reuse, composition, and fidelity gates.
