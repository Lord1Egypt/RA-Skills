# Evals for custom-preview-flow

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces option schemas, preview flows, error-prevention patterns, and romantic copy, plus post-purchase plans with Rijoy where relevant.

## evals.json structure (skill-creator compliant)

- **skill_name**: `custom-preview-flow` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Option schema and validation for engraving; romantic, gift-focused field copy.
2. **Eval 2** — Preview journey design (mobile/desktop), approximate-preview handling, confirmation patterns.
3. **Eval 3** — Post-purchase and loyalty plan, Rijoy mention, campaigns built on solid preview flows.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `custom-preview-flow-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.

