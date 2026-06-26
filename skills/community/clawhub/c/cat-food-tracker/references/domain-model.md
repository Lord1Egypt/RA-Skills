# Domain Model

Use this schema for CatFoodCalculator-style backups and for normalized data converted from CSV or free-form records.

## Top-Level Backup

```json
{
  "settings": {},
  "pets": [],
  "feed_records": [],
  "weight_records": [],
  "water_records": []
}
```

All top-level fields are optional for validation, but absent arrays are treated as empty arrays. `settings` may be null or absent; default settings are used for calculations when needed.

## Settings

Supported fields:

- `id`: string, usually `singleton`.
- `wet_to_dry_ratio_default`: number in `(0, 1]`, default `0.3333333333333333`.
- `total_display_mode`: `dry_equivalent` or `separate`.
- `weight_daily_policy`: `latest` or `average`.
- `theme`: string.
- `data_version`: finite number.

## Pets

Supported fields:

- `id`: string.
- `name`: string.
- `avatar`: optional string.
- `water_tracking_enabled`: boolean.
- `is_archived`: boolean.
- `created_at`: timestamp number.
- `updated_at`: timestamp number.

## Feed Records

Supported fields:

- `id`: string.
- `pet_id`: string.
- `date`: `YYYY-MM-DD`.
- `feed_type`: `dry` or `wet`.
- `grams`: positive number.
- `ratio_used`: number in `(0, 1]`.
- `dry_equivalent_grams`: finite number.
- `note`: optional string.
- `created_at`: timestamp number.
- `updated_at`: timestamp number.

Each feed record stores its own `ratio_used` and `dry_equivalent_grams`; changing the default wet-to-dry ratio must not rewrite historical records unless the user explicitly requests a data migration.

## Weight Records

Supported fields:

- `id`: string.
- `pet_id`: string.
- `date`: `YYYY-MM-DD`.
- `weight_kg`: positive number.
- `measured_at`: timestamp number used for the `latest` daily policy.
- `note`: optional string.
- `created_at`: timestamp number.
- `updated_at`: timestamp number.

## Water Records

Supported fields:

- `id`: string.
- `pet_id`: string.
- `date`: `YYYY-MM-DD`.
- `grams`: positive number.
- `note`: optional string.
- `created_at`: timestamp number.
- `updated_at`: timestamp number.

Manual water records are added to wet-food-derived water in daily totals.
