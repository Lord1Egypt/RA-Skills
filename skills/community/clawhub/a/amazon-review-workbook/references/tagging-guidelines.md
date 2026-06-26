# Tagging Guidelines

Use this guide after `prepare-tagging`.

`prepare-tagging` produces the cropped machine prompt payload for the model. It is not the final workbook and it is not the merge source. The model should read the pending-row payload, fill only those rows, and write a separate labels JSON that `merge-build` can merge back into the full base JSON.

Before spending more requests on keyword expansion, prefer running:

```bash
python scripts/amazon_review_workbook.py coverage-check --url "<amazon-url>" --db-path "<out-dir>/amazon_review_cache.sqlite3"
```

If `coverage_ratio` is already high enough for the job, skip `--keywords`.

When you do need a keyword pass:

- prefer `--keyword-profile generic` for broad consumer products
- prefer `--keyword-profile electronics` for devices with apps/setup/accessories
- prefer `--keyword-profile dashcam` for our core dashcam scenario
- keep the default `--keyword-reuse-scope successful` so already-productive keywords are not rerun

To rebuild the tuned ordering from old experiments, run:

```bash
python scripts/amazon_review_workbook.py keyword-autotune --output-dir "<out-dir>" --db-path "<out-dir>/amazon_review_cache.sqlite3" --report-glob "<path-to-old-reports>/*keywords*.json"
```

## Columns The Model Should Fill

- `评论中文版` if still blank
- `评论概括`
- `情感倾向`
- `类别分类`
- `标签`
- `重点标记`

## Rules

- `评论中文版`: faithful translation; do not add new meaning
- `评论概括`: one sentence, focus on the main user point
- `情感倾向`: only `Positive`, `Negative`, or `Neutral`
- `类别分类`: choose 1-2 categories, join with ` / `
- `标签`: 1-3 short Chinese tags, ideally <= 10 chars each, join with `，`
- `重点标记`: prefer business-useful dimensions, join with `，`

## Allowed Categories

- `Praise on product`
- `Questions/Worrying`
- `Negative emotions`
- `Suggestion`
- `Nothing particular`
- `Being supportive to the brand`
- `Expecting`
- `Being Sarcastic`
- `Competitor comparison`
- `Status update`

## Preferred Focus Dimensions

- `性价比`
- `质量`
- `功能改进建议`
- `竞品/型号`
- `软件/设置`
- `安装/适配`
- `品牌/售后`
- `物流/包装`
- `配件/兼容性`

## Quality Gates

- Do not invent country, rating, review time, or helpful votes.
- Do not rewrite the review into marketing copy.
- Keep tags merged and stable; avoid synonym explosion.
- If a review is mostly descriptive and low-signal, `类别分类` can be `Nothing particular`.
- If a row is ambiguous, prefer conservative labels over over-claiming.

## Faster Workflow

### 1. Build canonical tags first

Before labeling a large batch, generate representative samples:

```bash
python scripts/amazon_review_workbook.py taxonomy-bootstrap --input-json "<translated-or-factual-json>" --output-dir "<out-dir>"
```

Then ask the model to read that bootstrap file and produce a short `canonical_tags.json`.

### 2. Prepare a lightweight tagging payload

```bash
python scripts/amazon_review_workbook.py prepare-tagging --input-json "<translated-or-factual-json>" --output-dir "<out-dir>" --canonical-tags-json "<out-dir>/canonical_tags.json"
```

This payload:

- strips the model input down to the minimum fields
- skips rows already found in cache
- pre-fills some heuristic sentiment/category/focus fields
- includes fixed category and focus enumerations

### 3. Let the model label only pending rows

Use the generated `*_tagging_input.json`, not the full workbook rows.

Model output should be a JSON array or an object with `items`, where each item contains:

- `seq` or `review_id`
- `评论中文版` if still blank
- `评论概括`
- `情感倾向`
- `类别分类`
- `标签`
- `重点标记`

### 4. Merge labels and update cache

```bash
python scripts/amazon_review_workbook.py merge-build --base-json "<translated-or-factual-json>" --labels-json "<model-output-json>" --output-dir "<out-dir>" --taxonomy-version "v1" --strict
```

This command:

- merges labeled rows back into the full base JSON
- reuses cached labels for identical reviews
- writes new labels into the cache
- exports the final workbook
