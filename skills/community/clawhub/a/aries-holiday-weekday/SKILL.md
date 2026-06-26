---
name: aries-holiday-weekday
description: Query gov.cn Chinese holiday notices to determine workdays, holidays, and make-up workdays. Use when the user needs to check whether a specific date is a workday, generate a month's date list with workday status, or inspect holiday names and make-up shifts from official State Council notices.
---

# Aries Holiday Weekday

## Overview

Use this skill to answer date questions that depend on China's holiday schedule rather than a simple Monday-to-Friday rule. It handles statutory holidays, weekend make-up workdays, and ordinary weekdays using official gov.cn notices.

## Input Modes

Support two input shapes:

1. `YYYY-MM`
2. `YYYY-MM-DD`

If the input is a month, return every date in that month with:

- Date
- Weekday
- Workday status
- Holiday or make-up shift name if present

If the input is a single date, return the same fields for that date only.

## Workflow

Resolve the target year's holiday data first:

1. Look for `cache/YYYY.json` inside this skill.
2. If the file exists, use it to answer directly.
3. If the file does not exist, say `正在获取{年份}年最新节假日安排` once, then call `gov_search()` from `scripts/query_holiday.py` to search gov.cn for `节假日安排`.
4. Use this prompt to pick the best search result:

   `从下列查询结果的标题中选择最适配 {年份}节假日安排的一个，并给我对应查询结果的链接：{查询结果}`

5. Fetch the selected notice page body with `fetch_notice_body(url)`.
6. Use this prompt to turn the notice body into JSON:

   `这是国务院关于节假日安排的通知，请从这个通知里解析出节假日放假的日期和因为假期调休为工作日的日期：{通知内容}，以json的形式体现`

7. Validate the JSON before caching it. At minimum, it should contain:
   - `year`
   - `notice_title`
   - `notice_url`
   - `special_days`
8. Save the validated result as `cache/{年份}.json`.
9. If you need a one-shot helper, use `refresh_year(year)` from `scripts/query_holiday.py`, or the CLI `refresh` command.

## Interpretation Rules

- Do not infer workday status from weekdays alone.
- Treat weekend make-up shifts as workdays.
- Treat holiday rest days as non-workdays even if they fall on Monday to Friday.
- If the cache has a matching date, use it first.
- If the cache does not list a date, fall back to the normal weekday rule: Monday to Friday are workdays, Saturday and Sunday are not.
- Do not mention cache hits, cache refresh, or other internal retrieval steps in the user-facing answer; only present the final skill result.
- If you need a progress line, use only `正在获取{年份}年最新节假日安排` and nothing about cache.

## Output Format

For a month query, output a compact table:

- `date`
- `weekday`
- `workday`
- `kind`
- `holiday`

For a single-date query, output a short structured summary with the same fields.

## Script

Use `scripts/query_holiday.py` as the primary entry point for deterministic search, notice-body extraction, cache loading, cache refresh, and date classification.
