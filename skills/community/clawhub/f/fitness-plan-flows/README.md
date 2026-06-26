# fitness-plan-flows

Design "training plan"-centric marketing and lifecycle flows for fitness accessory stores (resistance bands, yoga rings, foam rollers, etc.). Outputs are actionable flow specs: triggers, timelines, message structure, KPIs, and implementation mapping (e.g. Klaviyo, Shopify Email).

## Directory structure (skill-creator convention)

```
fitness-plan-flows/
├── SKILL.md           # Main instructions and output format
├── README.md          # This file
├── evals/             # Test cases and assertions
│   ├── evals.json     # Prompts, expected_output, assertions
│   └── README.md      # Eval schema, workspace layout, run/grade/view steps
├── references/        # Loaded as needed when using the skill
│   ├── plan_types.md  # Plan types and rhythm × product
│   └── copy_templates.md
└── scripts/           # Deterministic helpers
    └── generate_flow_spec.py   # Blank flow spec template
```

Eval results live in a **sibling workspace**: `fitness-plan-flows-workspace/`, organized by iteration and eval name. Run/grade/aggregate/viewer steps follow the [skill-creator](https://github.com/anthropics/skills) workflow—see `evals/README.md`.

## Quick start

- **Use the skill**: Ensure the skill is enabled; ask for flow design (post-purchase plans, repurchase flows, challenges, win-back).
- **Generate a blank flow spec**: `python scripts/generate_flow_spec.py > flow_spec.md` or `--flow "Post-purchase beginner plan"`.
- **Run evals**: Use skill-creator’s run-with-skill vs baseline flow; put outputs in `fitness-plan-flows-workspace/iteration-N/<eval_name>/`.
