# Import And Export

Use this when validating backups, preparing user data for calculation, or explaining exported summaries.

## JSON Backup Validation

Run:

```bash
node {baseDir}/scripts/validate-backup.mjs backup.json --pretty
```

Validation behavior:

- The backup must be a JSON object.
- File/input size is limited to 5 MB.
- Unsupported fields are dropped from sanitized output.
- Missing record arrays become empty arrays.
- Dates must match `YYYY-MM-DD`.
- Numeric gram and weight fields must be positive where applicable.
- `ratio_used` and `wet_to_dry_ratio_default` must be in `(0, 1]`.
- Enums must match the supported values in `references/domain-model.md`.

The validation command emits:

- `valid`: boolean.
- `counts`: record counts after sanitization.
- `warnings`: non-fatal issues such as records referencing missing pets.
- `settings`: sanitized settings or defaults.

## Daily Summary CSV

Run:

```bash
node {baseDir}/scripts/daily-summary.mjs backup.json --format csv
```

CSV columns:

- `pet_id`
- `pet_name`
- `date`
- `dry_total`
- `wet_total`
- `dry_equivalent_total`
- `manual_water_total`
- `wet_water_from_food`
- `total_water`
- `weight_kg`
- `feed_record_count`
- `weight_record_count`
- `water_record_count`

## Common Data Cleanup

If the user provides informal records, normalize them before validation:

- Convert dates to `YYYY-MM-DD`.
- Convert dry/wet labels to `dry` or `wet`.
- Convert grams and weights to numbers.
- Generate stable placeholder ids only when records are missing ids and the user asks for a valid backup.
- Preserve notes as strings.

Do not infer veterinary recommendations. This skill is for data processing and summaries, not medical advice.
