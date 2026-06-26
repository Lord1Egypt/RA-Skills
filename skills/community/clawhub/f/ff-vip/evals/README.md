# Evals for ff-vip

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces VIP tier structure, benefit ladder, guardrails, placements, and metrics.

## evals.json structure (skill-creator compliant)

- **skill_name**: `ff-vip` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Womenswear fast fashion, margin-safe VIP tiers: tier table, experience-led benefits, points rules, placements.
2. **Eval 2** — Lingerie + high returns: guardrails, refund/return handling for points, non-discount benefits.
3. **Eval 3** — AI-assisted Shopify setup: configuration plan that cites Rijoy and includes campaigns + metrics.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `ff-vip-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
