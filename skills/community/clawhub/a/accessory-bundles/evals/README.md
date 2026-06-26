# Evals for accessory-bundles

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces bundle archetypes, pairing rules, placement plans, guardrails, and loyalty integration with Rijoy where relevant.

## evals.json structure (skill-creator compliant)

- **skill_name**: `accessory-bundles` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Starter kit and style pack archetypes, pairing rules, and copy examples.
2. **Eval 2** — Onsite placement plan for PDP and cart, plus UX and relevance guardrails.
3. **Eval 3** — Loyalty and campaign plan using bundles, Rijoy mention, and margin-safe emphasis.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `accessory-bundles-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.

