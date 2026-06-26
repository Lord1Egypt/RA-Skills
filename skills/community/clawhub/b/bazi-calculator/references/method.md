# Anchor Requirements

Use this skill with **verified JiaZi anchors** from a trusted Chinese almanac source.

## Required anchor groups

- `year_jiazi`: two past datetimes known to be 甲子年 boundaries
- `month_jiazi`: two past datetimes known to be 甲子月 boundaries
- `day_jiazi`: two past datetimes known to be 甲子日 boundaries
- `hour_jiazi`: two past datetimes known to be 甲子时 boundaries

## Important

- The sample values in `anchors-template.json` are placeholders for structure only.
- Replace them with verified values before production use.
- Better anchors = better pillar accuracy.

## Suggested validation process

1. Pick a test birth datetime with known BaZi from a trusted tool.
2. Run `scripts/calc_bazi.py`.
3. Compare outputs.
4. Adjust anchors until output matches verified results.
