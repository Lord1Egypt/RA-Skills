# Production Profiles

Resolve a production profile before creating production artifacts. The profile controls how much internal work is required, which gates are hard gates, and what the user-facing package may contain.

Use:

```bash
python3 scripts/resolve_production_profile.py \
  --requirements requirements.json \
  --ppt-ir .ppt-work/contracts/ppt-ir.json \
  --output .ppt-work/contracts/production-profile.json
```

User override wins. If the request explicitly asks for `fast`, `standard`, or `premium`, use that profile and record the override in `production-profile.json`.

## Profile Matrix

| Profile | Use When | User-Facing Delivery | Status Ceiling |
|---|---|---|---|
| `fast` | internal draft, content validation, simple article, explicit speed request | `deck.pptx`, `delivery-manifest.json` | `verified` |
| `standard` | formal internal report, ordinary client communication, product / technical / business report | `deck.pptx`, `deck-preview.pdf`, `verification-report.md`, `delivery-manifest.json` | `verified` |
| `premium` | public release, high-value customer, template asset, strong brand requirement, complex diagrams, explicit full validation | `deck.pptx`, `deck-preview.pdf`, `verification-report.md`, `delivery-manifest.json`, optional `assets/`, optional `source-package/` | `final` |

## Selection Inputs

The resolver uses these requirement fields when available:

```text
user_request
audience
public_or_internal
delivery_value
editability_requirement
source_complexity
diagram_complexity
brand_requirement
deadline_mode
```

Reason codes:

```text
USER_REQUESTED_FAST
USER_REQUESTED_STANDARD
USER_REQUESTED_PREMIUM
PUBLIC_DELIVERY
INTERNAL_DRAFT
COMPLEX_SOURCE
COMPLEX_DIAGRAMS
HIGH_EDITABILITY_REQUIREMENT
BRAND_ASSETS_REQUIRED
LOW_RISK_SIMPLE_CONTENT
```

## Internal Workspace

All process artifacts go under `.ppt-work/`:

```text
.ppt-work/
├── analysis/
│   ├── source-analysis.md
│   ├── content-lock.md
│   └── storyboard.md
├── contracts/
│   ├── ppt-ir.json
│   ├── style-contract.json
│   ├── asset-manifest.json
│   ├── delivery-plan.json
│   ├── production-profile.json
│   └── build-manifest.json
├── assets/
├── references/
├── builds/
│   ├── draft/
│   └── final/
├── renders/
│   ├── representative-renders/
│   └── full-renders/
├── qa/
├── logs/
└── checkpoints/
```

Do not scatter working files into the user's final directory. The final directory should contain only user-facing delivery files and `delivery-manifest.json`.

Failure rule: preserve `.ppt-work/` whenever any hard gate fails. Premium should preserve `.ppt-work/` by default because the audit trail is part of the production value.

## Fast

Required internal artifacts:

- `.ppt-work/analysis/content-lock.md`
- `.ppt-work/contracts/ppt-ir.json`
- `.ppt-work/contracts/style-contract.json`
- `.ppt-work/contracts/delivery-plan.json`
- `.ppt-work/contracts/build-manifest.json`

Hard gates:

- contracts valid
- PPTX package readable
- no whole-slide raster
- no missing media

Fast may skip storyboard, full QA, benchmark, render, and verification report unless the user asks for them.

## Standard

Required internal artifacts:

- Fast artifacts
- `.ppt-work/analysis/storyboard.md`
- `.ppt-work/contracts/asset-manifest.json` when assets are used
- `.ppt-work/qa/qa-report.json`
- representative render evidence when a renderer is available

Hard gates:

- structural inspection
- editability check
- color contract check
- representative render when available
- zero QA errors

If no renderer is available, preserve the unavailable render report and cap status honestly. Do not claim visual QA passed.

## Premium

Required internal artifacts:

- Standard artifacts
- `.ppt-work/references/visual-references/`
- `.ppt-work/renders/full-renders/`
- `.ppt-work/renders/contact-sheet.png`
- `.ppt-work/qa/repair-cycles/`
- `.ppt-work/qa/benchmark-score.json`

Hard gates:

- full-deck real render
- read back
- complete QA
- automatic repair attempt for repairable errors
- rubric score at least 14
- zero QA errors
- zero whole-slide raster
- all fallbacks disclosed

Premium cannot reach `final` without real render evidence. `RENDER_ENGINE_UNAVAILABLE` must cap status below `final`.

## Trusted Delivery Status

Only tools calculate trusted status. Builders and agents must not handwrite `final` or subjectively mark `verified`.

Status order:

```text
planned -> created -> rendered -> read_back -> verified -> final
failed
```

Rules:

- `planned`: contracts exist, no PPTX output yet.
- `created`: PPTX exists and package structure is readable.
- `rendered`: at least one trusted renderer produced render evidence.
- `read_back`: object-level structure was inspected and core objects were recognized.
- `verified`: profile hard gates passed.
- `final`: Premium only, with render, read back, zero QA errors, zero whole-slide raster, editability threshold met, rubric score met, and fallbacks disclosed.
- `failed`: a hard gate or critical stage failed.

Package with:

```bash
python3 scripts/package_delivery.py \
  --workdir .ppt-work \
  --profile standard \
  --output output/final \
  --manifest output/final/delivery-manifest.json \
  --strict
```

Use `--zip` only when the recipient needs one archive. Use `--include-assets` and `--include-sources` only when those files are intended for the user.
