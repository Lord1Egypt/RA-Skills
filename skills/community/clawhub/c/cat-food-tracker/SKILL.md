---
name: cat-food-tracker
description: Work with cat feeding, weight, and water tracking records. Use when validating CatFoodCalculator-style JSON backups, calculating dry-equivalent cat food totals, estimating water intake from wet food, summarizing pet feeding records by day, converting summaries to CSV, or helping users clean up offline pet feeding data.
license: MIT
---

# Cat Food Tracker

Use this skill to process cat feeding tracker data reliably. Prefer the bundled scripts for validation, daily summaries, and CSV output instead of doing arithmetic manually.

## Workflow

1. Identify the input shape. Supported input is a JSON object with optional `settings`, `pets`, `feed_records`, `weight_records`, and `water_records` arrays. If the user provides CSV or free-form data, first convert it into this shape.
2. Validate JSON backups with `scripts/validate-backup.mjs` before calculating or transforming records.
3. Generate daily summaries with `scripts/daily-summary.mjs` when the user asks for totals, dry-equivalent food, water intake, daily history, or CSV export.
4. Read the focused reference files only when needed:
   - `references/domain-model.md` for accepted fields and enums.
   - `references/calculations.md` for formulas, rounding, and grouping behavior.
   - `references/import-export.md` for backup validation and CSV expectations.

## Commands

Run validation:

```bash
node {baseDir}/scripts/validate-backup.mjs backup.json --pretty
```

Read backup JSON from stdin:

```bash
cat backup.json | node {baseDir}/scripts/validate-backup.mjs - --pretty
```

Create daily JSON summaries:

```bash
node {baseDir}/scripts/daily-summary.mjs backup.json --pretty
```

Create daily CSV summaries:

```bash
node {baseDir}/scripts/daily-summary.mjs backup.json --format csv
```

Filter by pet or date range:

```bash
node {baseDir}/scripts/daily-summary.mjs backup.json --pet-id pet-1 --from 2026-04-01 --to 2026-04-30 --format csv
```

## Public Data Handling

Treat cat names and feeding histories as private user data. Do not include real backup files, pet names, or feeding history in examples, logs, commits, or published skill packages unless the user explicitly asks.

If an input has unsupported fields, validate first and explain that this skill keeps only the supported CatFoodCalculator-style schema. If records reference missing pets, report the warnings from the scripts and still summarize using the `pet_id`.

## When Editing Or Extending

Keep formulas in `scripts/cat-food-core.mjs` and `references/calculations.md` aligned. If adding a field to the backup schema, update `references/domain-model.md`, `references/import-export.md`, validation in `cat-food-core.mjs`, and the self-test examples.
