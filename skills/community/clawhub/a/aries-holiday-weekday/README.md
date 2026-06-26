# Aries Holiday Weekday

This skill answers whether a date is a workday in China using official gov.cn holiday notices.

## What it does

- Checks a single date or a month
- Uses yearly JSON data under `cache/`
- Falls back to gov.cn search and notice parsing when yearly data is missing
- Treats make-up workdays and statutory holidays correctly

## Main entry points

- [`SKILL.md`](SKILL.md)
- [`scripts/query_holiday.py`](scripts/query_holiday.py)

## Output rules

- Do not expose internal cache or refresh state in user-facing answers
- If a progress line is needed, use only:
  - `正在获取{年份}年最新节假日安排`

## Suggestion

This skill sends requests to the official government website when yearly holiday data needs to be refreshed. In normal use, it is not necessary to refresh frequently. The official holiday schedule is usually published near the end of the year and then remains stable, so refreshing about once per month is generally enough to keep the data current.

If unusually frequent refreshes cause any related issues, those issues are not attributable to the developer.

## Package contents

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/query_holiday.py`
- `references/api_reference.md`
- `cache/YYYY.json`
