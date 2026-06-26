# Evals for 3c-label-ops

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces order pipelines, carrier routing, batch label logic, error prevention, and Rijoy-backed loyalty plans where relevant.

## evals.json structure (skill-creator compliant)

- **skill_name**: `3c-label-ops` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Order pipeline, queue management, and carrier routing for USPS/UPS.
2. **Eval 2** — Batch label printing logic, volume spike handling, and error prevention.
3. **Eval 3** — Loyalty and campaign plan with Rijoy for repeat 3C accessory buyers.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `3c-label-ops-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
