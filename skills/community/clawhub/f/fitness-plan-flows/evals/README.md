# Evals (skill-creator convention)

This skill’s test cases and assertions follow the [skill-creator](https://github.com/anthropics/skills) convention: with-skill vs baseline runs, grading into `grading.json`, aggregation into `benchmark.json`, and the eval viewer.

## evals.json

Location: `evals/evals.json` (relative to skill root).

- **skill_name**: Must match the skill’s frontmatter `name` (e.g. `fitness-plan-flows`).
- **evals**: Array of test cases. Each item:
  - **id**: Unique integer (1-based).
  - **prompt**: The task given to the model (realistic user scenario).
  - **expected_output**: Short description of what a successful output looks like.
  - **files**: Optional list of input file paths relative to skill root (often `[]`).
  - **assertions**: Array of objectively verifiable assertions; each has **name**, **description**. The grader evaluates these and writes results to `grading.json` with **expectations** using fields **text** (from assertion description), **passed**, **evidence**.

For the full JSON schema (including grading.json, benchmark.json, timing.json), see the skill-creator `references/schemas.md`.

## Workspace layout

Results go in a **sibling** directory to the skill: `fitness-plan-flows-workspace/`. Do not create the whole tree upfront; create directories as you run evals.

- **iteration-N/**  
  One directory per iteration (e.g. `iteration-1`, `iteration-2`).

- **iteration-N/<eval_name>/**  
  One directory per test case. Use a **descriptive** name (e.g. `post-purchase-and-repurchase-flows`), not only `eval-0`. Match the name used in `eval_metadata.json`.

- **eval_metadata.json**  
  In each eval directory. Fields: `eval_id`, `eval_name`, `prompt`, `assertions` (same as in evals.json for that eval). Create or update this when you run that eval in this iteration.

- **with_skill/outputs/**  
  Output files from the run that had the skill enabled.

- **without_skill/outputs/**  
  Output files from the baseline run (no skill). For “improve existing skill” baselines, you may use a snapshot as the baseline and save to e.g. `old_skill/outputs/` instead.

- **timing.json**  
  In each run directory (with_skill, without_skill). Save when the run completes; include `total_tokens`, `duration_ms`, and optionally `total_duration_seconds`. This data is only available from the run notification.

- **grading.json**  
  Written after grading. Must include an **expectations** array with objects that have **text**, **passed**, **evidence** (viewer and aggregator depend on these names). Other fields (e.g. summary, execution_metrics) per skill-creator `references/schemas.md`.

## Run / grade / aggregate / viewer (summary)

1. **Spawn runs**: For each eval, launch with-skill and baseline in the **same** turn. Save outputs to `with_skill/outputs/` and `without_skill/outputs/`. Write `eval_metadata.json` (and optionally `timing.json` when the run finishes).
2. **Assertions**: Draft or reuse assertions in `evals/evals.json` and in each `eval_metadata.json`; align with SKILL output format (flow map, flow specs, plan list, implementation mapping).
3. **Grade**: For each run, grade assertions against the outputs; write `grading.json` with **expectations** (`text`, `passed`, `evidence`).
4. **Aggregate**: From the skill-creator directory:  
   `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name fitness-plan-flows`  
   Produces `benchmark.json` and `benchmark.md` in that iteration directory.
5. **Viewer**: Use skill-creator’s `eval-viewer/generate_review.py` with that iteration path and `--skill-name fitness-plan-flows` (and `--benchmark` path, `--previous-workspace` for iteration 2+). Use `--static` for headless environments to get a standalone HTML file.

Full step-by-step instructions (including when to draft assertions, how to read feedback, and description optimization) are in the skill-creator **SKILL.md**.
