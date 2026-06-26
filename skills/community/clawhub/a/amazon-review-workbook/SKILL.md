---
name: amazon-review-workbook
description: Collect all customer reviews from an Amazon product URL or product-reviews URL through a logged-in Chrome session on port 9222, export a 14-column factual workbook, optionally fill translations through DeepLX, and then help the model tag the rows into a final delivery-ready spreadsheet. Use when the user sends an Amazon link and wants review scraping, competitor review analysis, review export, or a delivery-ready spreadsheet with usernames, review links, review time, helpful votes, translation, summary, sentiment, categories, and tags.
---

# Amazon Review Workbook

Turn an Amazon product or review link into a two-phase delivery workbook.

This skill is designed to be portable: the scripts live inside the skill folder and do not depend on `dashcamauto` or any other local repo.

## Quick Path

1. If this is the first run on a machine, read [references/setup.md](references/setup.md).
2. Run a quick health check:

```bash
python scripts/amazon_review_workbook.py doctor --url "<amazon-url>"
```

3. Run factual collection:

```bash
python scripts/amazon_review_workbook.py intake --url "<amazon-url>" --output-dir "<workspace>/amazon-review-output"
```

4. If DeepLX is configured and reachable, fill `评论中文版`:

```bash
python scripts/amazon_review_workbook.py translate --input-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_factual.json" --output-dir "<workspace>/amazon-review-output"
```

5. Check coverage before deciding whether keyword expansion is worth the extra requests:

```bash
python scripts/amazon_review_workbook.py coverage-check --url "<amazon-url>" --db-path "<workspace>/amazon-review-output/amazon_review_cache.sqlite3"
```

6. Build canonical tags and a lightweight tagging payload:

```bash
python scripts/amazon_review_workbook.py taxonomy-bootstrap --input-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_translated.json" --output-dir "<workspace>/amazon-review-output"
python scripts/amazon_review_workbook.py prepare-tagging --input-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_translated.json" --output-dir "<workspace>/amazon-review-output" --canonical-tags-json "<workspace>/amazon-review-output/canonical_tags.json"
```

`taxonomy-bootstrap` is only for building a stable canonical vocabulary for the batch. `prepare-tagging` consumes the full factual or translated JSON and emits a trimmed `*_tagging_input.json` that contains pending rows only plus cache metadata. Do not use that trimmed file as the merge source.

7. Read [references/tagging-guidelines.md](references/tagging-guidelines.md), let the model fill only the pending rows in a separate labels JSON, then merge the labels back into the full base JSON and build the final workbook:

```bash
python scripts/amazon_review_workbook.py merge-build --base-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_translated.json" --labels-json "<workspace>/amazon-review-output/amazon_<asin>_labels.json" --output-dir "<workspace>/amazon-review-output" --taxonomy-version "v1" --strict
```

## Workflow

### 1. Verify prerequisites

- Confirm `doctor` reports a valid `asin`.
- Confirm `chrome_debug_ready` is `true`.
- If you plan to use `translate`, confirm `deeplx_env_ready` is `true`.
- If `deeplx_reachable` is `false`, do not block the workflow; let the model fill `评论中文版` during tagging.

If any of these fail, read [references/setup.md](references/setup.md) before continuing.

### 2. Use the smallest command that fits

- For raw review collection only: use `collect`
- For factual extraction plus workbook scaffolding: use `intake`
- For deciding whether a keyword pass is still needed: use `coverage-check`
- For rebuilding the tuned keyword state from historical data: use `keyword-autotune`
- For machine translation of `评论中文版`: use `translate`
- For canonical tag sampling: use `taxonomy-bootstrap`
- For cache-aware lightweight model input: use `prepare-tagging`
- For writing the final labeled workbook: use `merge-build`

Examples:

```bash
python scripts/amazon_review_workbook.py collect --url "<amazon-url>" --output-dir "<workspace>/amazon-review-output"
python scripts/amazon_review_workbook.py translate --input-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_factual.json" --output-dir "<workspace>/amazon-review-output"
python scripts/amazon_review_workbook.py coverage-check --url "<amazon-url>" --db-path "<workspace>/amazon-review-output/amazon_review_cache.sqlite3"
python scripts/amazon_review_workbook.py keyword-autotune --output-dir "<workspace>/amazon-review-output" --db-path "<workspace>/amazon-review-output/amazon_review_cache.sqlite3"
python scripts/amazon_review_workbook.py taxonomy-bootstrap --input-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_translated.json" --output-dir "<workspace>/amazon-review-output"
python scripts/amazon_review_workbook.py prepare-tagging --input-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_translated.json" --output-dir "<workspace>/amazon-review-output" --canonical-tags-json "<workspace>/amazon-review-output/canonical_tags.json"
python scripts/amazon_review_workbook.py merge-build --base-json "<workspace>/amazon-review-output/amazon_<asin>_review_rows_translated.json" --labels-json "<workspace>/amazon-review-output/amazon_<asin>_labels.json" --output-dir "<workspace>/amazon-review-output" --taxonomy-version "v1" --strict
```

### 3. Keep the workbook stable

The factual and final workbooks always use the 14-column schema in [references/output-schema.md](references/output-schema.md).

Do not silently add or remove columns. If a field is unavailable from the page, leave it blank rather than inventing a value.

### 4. Tag rows only after grounding on the factual file

The model should not invent from the product page alone. Ground semantic tagging on the factual JSON/workbook created by `intake` or `translate`.

Keep the two JSON shapes distinct:

- `*_tagging_input.json` from `prepare-tagging` is the cropped machine prompt payload for the model
- `--base-json` for `merge-build` must be the full factual/translated record set, not the cropped tagging payload
- `--labels-json` is the model's completed semantic output for the pending rows only

If `translate` prints `translation_mode=model_fallback`, fill `评论中文版` in the same tagging pass instead of waiting for DeepLX.

Use [references/tagging-guidelines.md](references/tagging-guidelines.md) when filling:

- `评论概括`
- `情感倾向`
- `类别分类`
- `标签`
- `重点标记`

The preferred fast path is:

1. `taxonomy-bootstrap` to build a canonical tag vocabulary for this batch
2. `prepare-tagging` to create a minimal pending-row payload
3. model labeling only for pending rows, written into a separate labels JSON
4. `merge-build` to update cache and export the final workbook from the full base JSON

## Collection Defaults

- `intake` and `collect` no longer run keyword expansion implicitly in `deep` mode. `deep` now means the 18 combo pass only.
- Run `coverage-check` after intake to compare current rows vs Amazon's visible `reviews` count before deciding to spend more requests.
- Use `--keywords` only when you explicitly want a keyword pass.
- Use `--keywords` with no values to run the built-in keyword preset for the selected `--keyword-profile`.
- Use `--keywords foo bar baz` to provide an explicit keyword list.
- Default pacing now inserts a `2.5s` gap between combos/keywords to reduce rate-limit risk.
- Built-in profiles:
  - `generic`: universal consumer-product terms
  - `electronics`: universal terms + common app/setup/hardware terms
  - `dashcam`: electronics profile + recording/night/parking/GPS/Wi-Fi/mount terms
- Default keyword reuse policy is `successful`: keywords that have produced results before are skipped on later runs; recent zero-result keywords are also suppressed for `72h` to avoid immediate retries.
- If you really want to brute-force rerun every keyword, use `--keyword-reuse-scope none`.
- A tuned state file at `<output-dir>/keyword_tuning_state.json` is now read automatically when present, and refreshed after keyword runs so the skill gradually reorders towards higher-yield terms.
- `keyword-autotune` can also ingest old keyword-run JSON reports via `--report-glob` to seed the tuned state from historical experiments.

## Failure Boundaries

Do not claim success if any of these is true:

- The script did not reach a real review page.
- The expected XLSX/CSV for the current phase was not generated.
- Review links, review time, or helpful votes were guessed rather than extracted.
- The model tagged rows without first grounding on the factual JSON/workbook.
- The cropped `*_tagging_input.json` was used as `--base-json` for `merge-build`.
- The model re-labeled rows that were already cached for the same taxonomy version.
- The workflow still claims a 13-column contract after `评论用户名` was added as a real output column.

## Resources

- [references/setup.md](references/setup.md): first-run machine setup and environment requirements
- [references/output-schema.md](references/output-schema.md): fixed 14-column workbook contract
- [references/tagging-guidelines.md](references/tagging-guidelines.md): semantic labeling rules after factual collection
- [scripts/amazon_review_workbook.py](scripts/amazon_review_workbook.py): portable CLI for doctor/collect/intake/coverage-check/keyword-autotune/translate/taxonomy-bootstrap/prepare-tagging/merge-build
- [scripts/review_delivery_schema.py](scripts/review_delivery_schema.py): workbook schema, normalization, and XLSX/CSV writer
- [scripts/deeplx_translate.py](scripts/deeplx_translate.py): optional DeepLX translation helper
- [scripts/label_workflow.py](scripts/label_workflow.py): cache, heuristics, bootstrap, and merge logic for faster labeling
