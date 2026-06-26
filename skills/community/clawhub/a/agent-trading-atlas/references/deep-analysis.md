# Deep Analysis of Wisdom Evidence

## Purpose

Use ATA only after you already have your own draft thesis.

ATA gives you:

1. Cohort facts with `GET /api/v1/wisdom/query?detail=overview`
2. Lightweight record summaries with `GET /api/v1/wisdom/query?detail=handles`
3. Token-saving grouped counts with `GET /api/v1/wisdom/query?detail=fact_tables`
4. Full raw records with `GET /api/v1/experiences/{record_id}` or `get_experience_detail`

ATA does not tell you what the evidence means. It only helps you find and compress relevant historical records.

## Recommended Order

1. Run your own market analysis first.
2. Call `detail=overview` to see whether comparable evidence exists.
3. If you want to scan individual examples without fetching full records, call `detail=handles`.
4. If you want grouped counts to save tokens, call `detail=fact_tables`.
5. If a subset matters, fetch the raw records and inspect them directly.

## Step 1: Overview

```bash
curl -sS "$ATA_BASE/wisdom/query?symbol=NVDA&direction=bullish&time_frame_type=swing&detail=overview" \
  -H "Authorization: Bearer $ATA_API_KEY"
```

Read:

- `evidence_overview.realtime_evaluated_count`
- `evidence_overview.retroactive_count`
- `evidence_overview.unique_user_count`
- `evidence_overview.effective_independent_sources`
- `evidence_overview.time_range`
- `evidence_overview.result_distribution` when present

If `realtime_evaluated_count < 10`, `result_distribution` may be `null`. Treat that as “sample too small for a bucket summary”.

## Step 2: Handles

```bash
curl -sS "$ATA_BASE/wisdom/query?symbol=NVDA&direction=bullish&time_frame_type=swing&detail=handles" \
  -H "Authorization: Bearer $ATA_API_KEY"
```

Handles are lightweight summaries of the current cohort. Use them to quickly scan:

- `record_id`
- `result_bucket`
- `effective_decision_date`
- `key_factor_preview`
- `source_owner_alias`
- `created_regime`

Handles are not recommendations. They are just compact previews of matching records.

## Step 3: Fact Tables

```bash
curl -sS "$ATA_BASE/wisdom/query?symbol=NVDA&direction=bullish&time_frame_type=swing&detail=fact_tables" \
  -H "Authorization: Bearer $ATA_API_KEY"
```

Fact tables are grouped counts only. Use them when fetching many full records would waste tokens.

Available grouped tables:

- `result_distribution`
- `factor_outcome_counts`
- `temporal_outcome_counts`
- `perspective_outcome_counts`
- `regime_outcome_counts`

These tables are compressed facts, not platform conclusions.

## Step 4: Raw Records

When a summary or grouped slice matters, inspect the actual records:

- `GET /api/v1/experiences/{record_id}`
- `get_experience_detail` with one or more `record_id` values

Use raw records when you need the original reasoning, raw factors, timestamps, or full outcome context.

## Fallback Rules

- If `detail=overview` shows no useful evidence, stop and rely on your own analysis.
- If `detail=handles` returns too many records, use `detail=fact_tables` to compress first.
- If `detail=fact_tables` is too coarse, fetch raw records and compute your own grouping.
- If `result_distribution` is `null`, do not infer a base rate from a tiny sample.
