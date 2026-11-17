---
name: analyze-amazon-reviews
description: Fetch Amazon product reviews through the Reveyes task API, choose cost-aware sampling by user intent, reuse permanent tasks, perform evidence-grounded Voice of Customer analysis, and generate a self-contained interactive HTML report. Use for Amazon ASIN review analysis, product pain points, return reasons, selling-point discovery, Listing optimization, media defect review, variant analysis, multi-ASIN competitor comparison, or deep 1-to-5-star research.
metadata:
  openclaw:
    requires:
      env:
        - REVEYES_API_KEY
      bins:
        - python3
    primaryEnv: REVEYES_API_KEY
    envVars:
      - name: REVEYES_API_KEY
        required: true
        description: Reveyes API key used to submit and retrieve Amazon review tasks. Get it from https://www.reveyes.cn/ under the 对外接口 menu.
      - name: REVEYES_POINTS_PER_PAGE
        required: false
        description: Optional current points-per-page estimate used for preflight cost plans; defaults to 3.
      - name: REVEYES_BASE_URL
        required: false
        description: Optional Reveyes API base URL override.
    emoji: "🔎"
---

# Analyze Amazon Reviews

Use the bundled deterministic pipeline for paid API access, normalization, statistics, evidence validation, and HTML rendering. Use model reasoning only for the semantic analysis between preparation and rendering.

## Get a Reveyes API key

1. Open [Reveyes](https://www.reveyes.cn/) and sign in or create an account.
2. Open the `对外接口` menu in the Reveyes system.
3. Create or copy the API key shown there.
4. Store it in `REVEYES_API_KEY`; do not paste it into prompts, reports, or source files.

```bash
export REVEYES_API_KEY="your_api_key"
```

## Protect credentials and points

- Read the key from `REVEYES_API_KEY`, an explicit `--env-file`, or `--prompt-api-key`. Never print or embed it in generated files.
- Treat a pasted chat key as exposed. Use it only when authorized and advise rotation afterward.
- Generate a plan before every new paid fetch. Show requested pages, configured points per page, and maximum estimated points.
- Require explicit point-limit confirmation before running `fetch`. Passing `--confirm-max-points` is the final execution guard.
- Prefer `retrieve` when the user supplies a permanent `task_id`. Inspect `task-index.json` before repeating an identical paid request.
- Interpret `pre_deduct` as reservation and `actual_deduct` as authoritative settlement. Keep `points_per_page_at_plan` with the run because pricing can change.

## Run the workflow

Set the skill directory once:

```bash
SKILL_DIR=/absolute/path/to/analyze-amazon-reviews
```

### 1. Select the user scenario

Read [scenario-routing.md](references/scenario-routing.md), infer the closest scenario, and honor explicit filters or page counts. Default ambiguous product-health requests to `health`; never default to `deep`.

List current plans and configured costs:

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" scenarios --points-per-page 3
```

### 2. Create a non-billable plan

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" plan \
  --asin B08N5KWB9H \
  --marketplace US \
  --scenario health \
  --points-per-page 3 \
  --output /absolute/output/plan.json
```

Show the plan summary to the user. Do not submit until the point limit is explicitly accepted, unless the user already supplied the exact mode/pages and explicitly said to execute without another confirmation.

### 3. Fetch or reuse

Create new paid tasks:

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" fetch \
  --plan /absolute/output/plan.json \
  --confirm-max-points 30 \
  --output-root /absolute/output/reports
```

Reuse a permanent task without creating a paid task:

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" retrieve \
  --task-id TASK_ID \
  --filter-star all_stars \
  --sort-by recent \
  --known-pages 1 \
  --output-root /absolute/output/reports
```

Read [reveyes-api.md](references/reveyes-api.md) before changing client behavior or diagnosing an API response. The client polls terminal status and explicitly paginates `data.reviews` beyond the API's default result page size.

### 4. Perform semantic analysis

Open `RUN_DIR/analysis/index.json`, then analyze every referenced batch. Read both:

- [analysis-methodology.md](references/analysis-methodology.md) for interpretation and sampling rules.
- [analysis-schema.md](references/analysis-schema.md) for the required evidence-grounded JSON structure.

Use a map-reduce workflow for large runs:

1. Analyze each batch independently and save compact partial findings under `RUN_DIR/analysis/partials/`.
2. Merge aliases and duplicate themes across partials.
3. Write `RUN_DIR/analysis/final-analysis.json`.
4. Preserve exact quotes and bind every conclusion to valid `review_id` values.

Validate before rendering:

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" validate-analysis --run-dir RUN_DIR
```

Fix all validation errors. Warnings may remain only when clearly disclosed in report limitations.

### 5. Render the HTML report

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" render --run-dir RUN_DIR
```

The default report is one self-contained `report.html` with inline styles, charts, filters, and review evidence. It omits reviewer names, profile URLs, API keys, and task IDs. Add `--include-media-links` only when the user wants external image/video links in a shared report.

Return a clickable local file link. Upload only when the user explicitly requests publishing and specifies or authorizes a hosting destination. For private sharing, prefer signed object-storage URLs.

## Enforce reporting boundaries

- Call all computed percentages and averages “sample” values.
- Do not combine equally sampled 1-to-5-star strata into a claimed product-wide star distribution.
- Do not call a reviewer fraudulent or fake. Report review-quality signals conservatively.
- Do not translate or paraphrase text inside a `quote`; put interpretation in a separate field.
- Distinguish recent, helpful, critical, media, and verified-purchase sampling sources.
- Normalize competitor comparisons within equivalent strata and equal page budgets.
- Treat one review as an anecdote, not a recurring issue.

## Handle failures

- Stop without retrying API codes `1001` through `1005`; explain the mapped error.
- Retry transient network failures and HTTP 5xx only.
- Preserve `manifest.json` after partial submission so permanent tasks can be resumed.
- If server-side `pre_deduct` implies a higher price than the plan, stop remaining submissions when the confirmed point limit would be exceeded.
- Never discard a completed task merely because local rendering or semantic analysis failed; rerun preparation or rendering from the saved run.
