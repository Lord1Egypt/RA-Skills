# Calculations

Use the bundled `scripts/daily-summary.mjs` command for user-facing totals. These rules describe the expected behavior.

## Wet Food Dry Equivalent

For wet feed records:

```text
dry_equivalent_grams = grams * ratio_used
```

For dry feed records:

```text
dry_equivalent_grams = grams
```

When a record already contains `dry_equivalent_grams`, use that saved value for summaries. This preserves historical behavior when the user changes the default ratio later.

## Daily Food Totals

Group records by `pet_id` and `date`.

```text
dry_total = sum grams where feed_type is dry
wet_total = sum grams where feed_type is wet
dry_equivalent_total = sum dry_equivalent_grams for all feed records
```

Round output gram totals to two decimal places.

## Water Estimate

Manual water:

```text
manual_water_total = sum water_records.grams
```

Wet-food-derived water:

```text
wet_water_from_food = sum(wet record grams - wet record dry_equivalent_grams)
```

Total water:

```text
total_water = manual_water_total + wet_water_from_food
```

Calculate wet-food-derived water per record before summing. Do not use a current global ratio to recalculate old wet food records.

## Daily Weight

Use `settings.weight_daily_policy`.

- `latest`: choose the same-day weight record with the largest `measured_at` value.
- `average`: average all same-day `weight_kg` values and round to three decimal places.

If no same-day weight record exists, output an empty value for CSV or `null` for JSON.

## Date Handling

Dates are local calendar strings in `YYYY-MM-DD` format. Do not convert them through UTC when grouping; treat the string as the grouping key.
