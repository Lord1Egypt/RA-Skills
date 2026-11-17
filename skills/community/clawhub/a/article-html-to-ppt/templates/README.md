# Templates

These files are copyable starting points. Every JSON template in this directory
validates against its schema in `schemas/`, so you can copy one, edit the
content, and run it through the pipeline without first fixing structural errors.

Validate any contract before building:

```bash
python3 scripts/validate_contracts.py --ppt-ir my-deck.ppt-ir.json --style my-style.json
```

## Authoring notes

Use sample text only to understand the contract; replace it with the current source material.

| Template | Note |
| --- | --- |
| `ppt-ir-example.json` | Contract is `schemas/ppt-ir.schema.json`. Structure your own deck from this shape; do not treat the sample content as defaults. |
| `style-contract-example.json` | Illustrative token set. Validate real contracts with `schemas/style-contract.schema.json`, or start from one of the five master systems in `references/five-style-master-systems.md`. |
| `delivery-plan-example.json` | Do not handwrite a delivery plan for production. Generate it with `scripts/resolve_component_delivery.py` so route selection reflects an actual capability probe. |
| `build-manifest-example.json` | Emitted by a Builder. Contract is `schemas/build-manifest.schema.json`; never handwrite a status into it. |
| `qa-report-example.json` | Emitted by `scripts/verify_deck.py`. Contract is `schemas/qa-report.schema.json`. |
| `component-registry-example.json` | Illustrative excerpt. The machine source is `references/component-registry.json`. |
| `diagram-ir-example.json` | Contract is `schemas/diagram-ir.schema.json`. Normalize with `scripts/normalize_diagram_ir.py` before layout. |
| `capability-report-example.json` | Emitted by `scripts/capability_probe.py`. Never handwrite a capability claim; the probe is the only authority on what a Builder supports. |
| `delivery-manifest-example.json` | Emitted by `scripts/package_delivery.py`. Contract is `schemas/delivery-manifest.schema.json`. |
| `rubric-score-example.json` | Emitted by `scripts/score_deck.py`. For Premium final, the reference rubric must be supplied explicitly. |

## Public example inputs

Small contract examples are in `examples/contracts/valid/`. Reusable style
contracts are in `styles/`; local development fixtures are not distributed.

```bash
python3 scripts/validate_contracts.py --ppt-ir examples/contracts/valid/ppt-ir.json --style examples/contracts/valid/style-contract.json --strict
```

For document-driven creation and image reconstruction, follow the current
[Skill entry](../SKILL.md) and [declarative workflow](../references/declarative-design.md).

## Markdown templates

| Template | Use |
| --- | --- |
| `content-lock-template.md` | Lock source truth and evidence boundaries before storyboarding. |
| `storyboard-template.md` | Judgment titles, expression mode, and visual anchor per slide. |
| `ppt-production-artifact-checklist.md` | Which artifacts a profile requires. |
| `slide-manifest-template.json` | Per-slide object manifest for hybrid delivery. |
| `visual-qa-gate-template.json` | Visual review record for Standard and Premium. |
