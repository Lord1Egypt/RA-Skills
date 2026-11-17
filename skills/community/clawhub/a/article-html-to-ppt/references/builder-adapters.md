# Builder Adapters And Capability Probe

Phase 9 adds an explicit environment contract before PPT production. Do not assume OfficeCLI, PptxGenJS, python-pptx, PowerPoint, LibreOffice, HTML rendering, SVG rendering, or fonts exist on the current machine.

## Capability Probe

Run the probe after resolving the Style Contract and before selecting a Builder:

```bash
python3 scripts/capability_probe.py \
  --style .ppt-work/contracts/style-contract.json \
  --registry references/component-registry.json \
  --output .ppt-work/capability-report.json \
  --strict
```

The report records:

- environment basics without exposing full local paths
- builder availability, versions, smoke-test results, features, and component support
- renderer availability for PowerPoint, LibreOffice, and related engines
- format support such as HTML render, SVG render/embed, PDF-to-PNG, PPTX read/write
- installed and missing fonts from the Style Contract
- warnings and errors that affect routing

Core builders must not be considered available from command existence alone. They need a minimal import, version, or smoke check:

- `pptxgenjs`: `node` plus `require("pptxgenjs")` and a tiny slide construction smoke check.
- `python_pptx`: package import plus create/save a minimal PPTX.
- `officecli`: command plus project-specific version/help smoke check; keep unavailable if smoke is not proven.
- `html_svg`: may be available for visual-only SVG generation, but never for native PPT objects.

## Adapter Interface

Every builder adapter follows this contract:

```python
class BuilderAdapter(Protocol):
    name: str

    def probe(self) -> BuilderCapability: ...
    def supports(self, component_type: str, delivery_route: str) -> SupportLevel: ...
    def plan(self, ppt_ir: dict, style_contract: dict, delivery_plan: dict) -> BuildPlan: ...
    def build(self, build_plan: BuildPlan, output_dir: Path) -> BuildResult: ...
    def inspect_output(self, pptx_path: Path) -> BuildInspection: ...
```

Optional extensions may add `render_preview`, `read_back`, and `cleanup`.

## Support Levels

Use only these support levels:

- `full`: native route is supported with expected editability.
- `partial`: route is usable with documented limitations and editable-core review.
- `visual_only`: route is suitable only for SVG/image/HTML preview or hybrid visual layers.
- `unsupported`: route cannot be used by this builder.
- `unknown`: support has not been proven.

Premium rules:

- Reject `unknown` support.
- Reject `visual_only` for native routes.
- `native_required` accepts only `full` support on a native route.
- Missing capability reports stop Standard and Premium route resolution.
- Missing renderers prevent claiming final Premium visual QA.

Fast may use static registry defaults when no capability report exists, but it must warn.

## Selection Inputs

Builder selection uses:

- PPT IR object requirements and editability
- Delivery Plan route requirements when available
- Component Registry static support and fallback policy
- Capability Report real environment availability
- Production profile (`fast`, `standard`, `premium`)
- Optional user builder override

Scoring considers native component coverage, editable-core coverage, renderer compatibility, font compatibility, profile compatibility, and fallback count. A user-requested builder wins only when it is available and valid for the requested routes.

## Build Manifest

Build Manifest should record:

```json
{
  "builder": {
    "requested": "auto",
    "selected": "pptxgenjs",
    "version": "4.x",
    "selection_score": 0.92,
    "selection_reasons": ["BUILDER_SELECTED_BY_SCORE"]
  },
  "environment": {
    "capability_report": ".ppt-work/capability-report.json"
  }
}
```

If no valid builder exists, stop at contracts and visual references instead of silently downgrading.
