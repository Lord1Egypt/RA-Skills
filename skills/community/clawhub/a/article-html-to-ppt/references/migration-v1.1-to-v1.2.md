# Migration v1.1 to v1.2

This guide explains how to move older article-html-to-ppt manifests, templates, and handoffs into the v1.2 contract chain.

## Version Scope

v1.2.0 includes:

- narrower trigger and production profile routing
- PPT IR and formal JSON schemas
- Style Contract v2
- QA, Build, Delivery Plan, and Delivery Manifest contracts
- compatible migration scripts and deprecated template pointers

Diagram compiler, render harness, benchmark calibration, production profiles, and builder adapter contracts already exist in later commits in this workspace. Treat them as forward-compatible v1.5/v2.0 work, not as a reason to make every deck Premium.

## Field Migration

| v1.1 field | v1.2 field | Notes |
| --- | --- | --- |
| `judgment_title` | `title` + `title_role=judgment` | Only judgment slides need judgment titles. Cover, agenda, section, reference, instruction, and closing slides use non-judgment title roles. |
| `expression_mode` | `primary_expression` | Keep one primary expression and add support in `supporting_expressions` only when needed. |
| `hybrid_panel` | concrete primary expression + `supporting_expressions` | Deprecated. Migrate to `structured_cards`, `relationship_visual`, `data_visual`, or `conceptual_scene` plus interpretation support. |
| `visual_component_plan` | typed `objects[]` + `delivery_contract` | Each object gets id, type, semantic role, editability, priority, and route expectations. |
| `source_labels` | `source_refs[]` | Source references use `source_id`, locator, claim type, and optional notes. |
| `style_system` + `palette_name` | `style_contract_ref` + Style Contract v2 | Builders must read exact colors, typography, grid, shape, chart, diagram, image, icon, and footer tokens from the contract. |
| `score` | `qa-report.json` + rubric evidence | Scores are evidence, not a hand-written status shortcut. |

Use the migration script for old slide manifests:

```bash
python3 scripts/migrate_manifest_v1_to_v2.py old-slide-manifest.json \
  --output .ppt-work/contracts/ppt-ir.json
```

Then validate:

```bash
python3 scripts/validate_contracts.py \
  --ppt-ir .ppt-work/contracts/ppt-ir.json \
  --style .ppt-work/contracts/style-contract.json \
  --strict
```

## File Migration

| v1.1 artifact | v1.2 artifact |
| --- | --- |
| `slide_manifest.json` | `.ppt-work/contracts/ppt-ir.json` |
| loose design notes | `.ppt-work/contracts/style-contract.json` |
| visual QA checklist | `.ppt-work/qa/qa-report.json` |
| build notes | `.ppt-work/contracts/build-manifest.json` |
| delivery notes | `delivery-manifest.json` |

Internal process files belong under `.ppt-work/`. User-facing folders should contain the delivery package and `delivery-manifest.json`, not the entire working trail.

## Palette Aliases

Legacy aliases stay compatible for one migration cycle:

| Legacy alias | v1.2 palette |
| --- | --- |
| `mckinsey`, `palette-cl-mckinsey` | `navy-consulting` |
| `bcg`, `palette-cl-bcg` | `forest-consulting` |
| `linear`, `palette-pr-linear` | `graphite-lavender` |
| `stripe`, `palette-pr-stripe` | `graphite-steel` |
| `ibm-whitepaper`, `palette-tb-ibm-whitepaper` | `engineering-blue` |

Do not infer colors from words like "premium", "modern", or "tech". Resolve an explicit Style Contract.

## Production Profiles

Use `fast`, `standard`, or `premium` to control depth:

- `fast`: internal draft, content validation, simple article, or explicit speed request.
- `standard`: normal formal internal report, product review, technical review, or client/business deck.
- `premium`: public release, high-value client, template asset, strong brand requirement, complex diagrams, or explicit full validation request.

Premium is not the default. It exists because some decks need an audit trail, full render/readback evidence, benchmark scoring, and stricter fallback disclosure. If those conditions are not present, choose `standard` unless the user requests otherwise.

## Status Migration

Old "done" or "final" labels must become trusted status:

- `planned`: contracts exist, no deck built.
- `created`: PPTX exists and package is readable.
- `rendered`: real render evidence exists.
- `read_back`: deck was read back or inspected after render/build.
- `verified`: selected profile gates passed.
- `final`: Premium only, with real render evidence, readback, zero QA errors, no whole-slide raster, rubric pass, and disclosed fallbacks.
- `failed`: a hard gate failed.

Never handwrite `final`. Use `scripts/package_delivery.py` and the verifier outputs.

## Deprecated Templates

Compatibility templates remain for one migration cycle:

- `templates/slide-manifest-template.json`
- `templates/design-language-schema.json`
- old v1 manifest examples in `examples/contracts/v1/`

New work should use:

- `templates/ppt-ir-example.json`
- `templates/style-contract-example.json`
- `templates/build-manifest-example.json`
- `templates/qa-report-example.json`
- `templates/delivery-plan-example.json`
- `templates/delivery-manifest-example.json`

Deprecation target: remove v1 slide-manifest-only workflows after v1.3 unless a live downstream workflow still depends on them.
