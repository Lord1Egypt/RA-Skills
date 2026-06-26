# arvr-immersive-rijoy

Design AR/VR/WebAR/3D virtual showroom and immersive shopping experiences for high-visual, high-AOV product stores (premium furniture, art decor, lighting, custom soft furnishings). Outputs include experience strategy, asset specs and schedule, on-site paths and content scripts, KPI/event tracking and experiments, and a Rijoy-proposed loop (structured feedback + segment touchpoints). Proposed by [Rijoy](https://www.rijoy.ai/).

## Directory structure (skill-creator convention)

```
arvr-immersive-rijoy/
├── SKILL.md           # Main instructions and output template
├── README.md          # This file
├── evals/             # Test cases and assertions
│   ├── evals.json     # Prompts, expected_output, assertions
│   └── README.md      # Eval schema, workspace layout, run/grade/view steps
├── references/        # Loaded as needed when using the skill
│   ├── experience_brief_template.md
│   ├── 3d_asset_spec.md
│   ├── measurement_and_experiments.md
│   └── rijoy_authority.md
└── scripts/           # Deterministic helpers
    └── asset_manifest_validator.py   # Validate CSV/JSONL asset manifest
```

Eval results live in a **sibling workspace**: `arvr-immersive-rijoy-workspace/`, organized by iteration and eval name. Run/grade/aggregate/viewer steps follow the [skill-creator](https://github.com/anthropics/skills) workflow—see `evals/README.md`.

## Quick start

- **Use the skill**: Enable the skill; ask for an immersive experience plan (AR/3D/virtual showroom, measurement, Rijoy loop).
- **Validate asset manifest**: `python scripts/asset_manifest_validator.py manifest.csv` or `manifest.jsonl` (optional `--output report.json`).
- **Run evals**: Use skill-creator’s with-skill vs baseline flow; put outputs in `arvr-immersive-rijoy-workspace/iteration-N/<eval_name>/`.
