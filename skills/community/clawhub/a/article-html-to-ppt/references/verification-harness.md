# Verification Harness Contract

A deck is not complete because `deck.pptx` exists. The skill must report a trusted status based on evidence.

## Status

- `planned`: contracts exist, no PPTX.
- `created`: PPTX exists and package structure is readable.
- `rendered`: at least one renderer produced output.
- `read_back`: object structure was inspected.
- `verified`: hard QA passed.
- `final`: Premium profile only, with all hard gates passed.
- `failed`: build or QA failed.

## QA Issue Shape

Every issue must include:

- `issue_code`
- `slide_id`
- `object_id` when available
- `severity`
- `category`
- `evidence`
- `message`
- `repair_action`
- `repair_status`

Stage 6 executable QA reports use `schemas/qa-report.schema.json` and canonical
severities:

- `info`
- `warning`
- `error`
- `fatal`

For compatibility with older v2 report language, reports also include a
`compatibility_severity` alias:

- `info|warning` -> `review`
- `error` -> `fail`
- `fatal` -> `blocked`

## Executable Verification

Use `scripts/verify_deck.py` after building a deck:

```bash
python3 scripts/verify_deck.py deck.pptx \
  --ppt-ir .ppt-work/contracts/ppt-ir.json \
  --style .ppt-work/contracts/style-contract.json \
  --delivery .ppt-work/contracts/delivery-plan.json \
  --build .ppt-work/contracts/build-manifest.json \
  --render \
  --output .ppt-work/qa/qa-report.json \
  --write-inspection-report .ppt-work/qa/pptx-inspection.json \
  --write-render-report .ppt-work/qa/render-report.json
```

Exit codes:

- `0`: pass
- `1`: verification failure
- `2`: renderer unavailable
- `3`: bad input
- `4`: internal error

The verifier embeds the structural PPTX inspection and optional render report
inside the QA report. If `--render` is requested and no real render engine is
available, the report must include `RENDER_ENGINE_UNAVAILABLE`, return exit code
`2`, and cap `build_status_cap` at `created`. Do not substitute synthetic
screenshots or claim visual QA passed.

Use `scripts/repair_deck.py` only for safe deterministic repairs. The repair
loop writes a report of attempted repairs and remaining issues. It must not mark
visual or render issues repaired unless a real renderer is available and a
recheck passes.

## Required Issue Codes

- `CONTENT_SOURCE_MISSING`
- `TITLE_ROLE_INVALID`
- `EXPRESSION_PRIMARY_MISSING`
- `PRIMARY_ANCHOR_COMPETITION`
- `STYLE_COLOR_DRIFT`
- `TEXT_OVERFLOW`
- `OBJECT_OVERLAP`
- `OBJECT_OUT_OF_BOUNDS`
- `WHOLE_SLIDE_RASTER`
- `ORDINARY_COMPONENT_RASTERIZED`
- `EDITABLE_CORE_RASTERIZED`
- `MISSING_MEDIA`
- `PRIVATE_ABSOLUTE_PATH`
- `BLANK_SLIDE`
- `DIAGRAM_CONNECTOR_WEB`
- `DIAGRAM_EDGE_CROSSING`
- `DIAGRAM_BOUNDARY_UNCLEAR`
- `FONT_FALLBACK`
- `RENDER_FAILED`
- `READBACK_UNAVAILABLE`

## Renderer Availability

Preferred renderers:

1. PowerPoint
2. Keynote
3. OfficeCLI
4. LibreOffice
5. QuickLook only as a preview fallback

If no renderer is available, report `RENDER_ENGINE_UNAVAILABLE` and cap status at
`created` unless inspection provides stronger evidence. Structural readback can
support `read_back`, but it cannot prove nonblank visual rendering without a
renderer.

## Delivery Manifest Metrics

Standard and Premium reports should include:

- `logical_slide_count`
- `physical_slide_count`
- `native_text_ratio`
- `editable_core_ratio`
- `rasterized_area_ratio`
- `whole_slide_raster_count`
- `native_table_count`
- `native_chart_count`
- `native_connector_count`
- `media_count`
- `average_object_count`
- `fragmentation_score`
- `color_contract_compliance`
- `source_coverage_ratio`
- `render_success_ratio`
- `qa_error_count`
- `qa_warning_count`
- `rubric_score`
